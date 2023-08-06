"""``ipdrawio-export`` manager."""

# Copyright 2023 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import atexit
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib
from base64 import b64decode, b64encode
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

import lxml.etree as E
from jupyterlab.commands import get_app_dir
from PIL import Image
from pypdf import PdfMerger, PdfReader, PdfWriter
from requests import Session
from requests_cache import CachedSession
from tornado.concurrent import run_on_executor
from traitlets import Bool, Dict, Instance, Int, Unicode, default
from traitlets.config import LoggingConfigurable

from .constants import (
    DOT_CHROMIUM,
    DRAWIO_APP,
    DRAWIO_EXPORT_JS,
    ENV_DRAWIO_NODE_ENV,
    ENV_DRAWIO_PORT,
    ENV_DRAWIO_SERVER_URL,
    ENV_IPYDRAWIO_DATA_DIR,
    ENV_IPYDRAWIO_PORT,
    ENV_IPYDRAWIO_PUPPETEER_CACHE_DIR,
    ENV_JUPYTER_DATA_DIR,
    ENV_PUPPETEER_CACHE_DIR,
    PNG_DRAWIO_INFO,
    PUPPETEER_INSTALL,
    WORK_DIR,
)

# http error code
FOUR_HUNDRED = 400

VEND = Path(__file__).parent / "vendor/draw-image-export2"

DRAWIO_STATIC = (Path(get_app_dir()) / DRAWIO_APP).resolve()

JLPM = Path(shutil.which("jlpm")).resolve()

NODE = Path(
    shutil.which("node") or shutil.which("node.exe") or shutil.which("node.cmd"),
).resolve()


class IPyDrawioExportManager(LoggingConfigurable):

    """manager of (currently) another node-based server."""

    drawio_server_url = Unicode(help="URL for the drawio server").tag(config=True)
    drawio_port = Int(help="port for the drawio server").tag(config=True)
    drawing_name = Unicode("drawing.dio.xml", help="name for temporary XML").tag(
        config=True,
    )
    core_params = Dict(help="URL parameters for export").tag(config=True)
    drawio_export_workdir = Unicode(help="working directory for the drawio server").tag(
        config=True,
    )
    pdf_cache = Unicode(
        allow_none=True,
        help="path to cache for generated PDF pages",
    ).tag(config=True)
    attach_xml = Bool(help="attach source XML to PDF document").tag(config=True)
    attachment_name = Unicode("diagram.drawio", help="name of document to attach").tag(
        config=True,
    )
    init_wait_sec = Int(2, help="time to wait until contacting drawio server").tag(
        config=True,
    )
    export_retries = Int(5, help="number of retries for export").tag(config=True)
    is_provisioning = Bool(False)
    is_starting = Bool(False)
    _server = Instance(subprocess.Popen, allow_none=True)
    _session = Instance(Session)

    executor = ThreadPoolExecutor(1)

    def initialize(self):
        atexit.register(self.stop_server)

    @run_on_executor
    def _pdf(self, pdf_request):
        """TODO: enable more customization... I guess over HTTP headers?
        X-JPYDIO-embed: 1.
        """
        data = dict(pdf_request)
        data.update(**self.core_params)

        retries = self.export_retries
        status_code = None
        res = None
        pdf_text = None

        while retries:
            if self._server.returncode is not None:  # pragma: no cover
                self.start_server()
                time.sleep(self.init_wait_sec)
            try:
                self.log.warning(
                    "[ipydrawio-export] exporting (%s retries remaining)...",
                    retries,
                )
                res = self._session.post(self.url, timeout=None, data=data)
                pdf_text = res.text
                pdf_text_len = len(res.text)
                status_code = res.status_code
                self.log.info(
                    "[ipydrawio-export] ... %s response: %s bytes",
                    status_code,
                    pdf_text_len,
                )
            except Exception as err:  # pragma: no cover
                self.log.warning(f"[ipydrawio-export] Pre-HTTP Error: {err}")
                time.sleep((self.export_retries - retries) * self.init_wait_sec)

            if status_code is not None:
                if status_code <= FOUR_HUNDRED:
                    break

                if res:  # pragma: no cover
                    self.log.warning(
                        f"[ipydrawio-export] HTTP {res.status_code}: {res.text}",
                    )

                status_code = None
                res = None
                pdf_text = None

                self.log.warning(
                    "[ipydrawio-export] retrying, %s remaining...",
                    retries,
                )

            retries -= 1  # pragma: no cover

        if pdf_text and self.attach_xml and self.attachments:
            self.log.info(
                "[ipydrawio-export] attaching drawio XML as %s",
                self.attachment_name,
            )
            with tempfile.TemporaryDirectory() as td:
                tdp = Path(td)
                output_pdf = tdp / "original.pdf"
                output_pdf.write_bytes(b64decode(pdf_text))
                final_pdf = tdp / "final.pdf"
                final = PdfWriter()
                final.append_pages_from_reader(PdfReader(str(output_pdf), "rb"))
                xml = pdf_request["xml"]
                if hasattr(xml, "encode"):
                    xml = xml.encode("utf-8")
                final.add_attachment(self.attachment_name, xml)
                with final_pdf.open("wb") as fpt:
                    final.write(fpt)

                pdf_text = b64encode(final_pdf.read_bytes())
                self.log.debug(
                    f"[ipydrawio-export] {len(pdf_text)} bytes (with attachment)",
                )

        return pdf_text

    @run_on_executor
    def _merge(self, pdf_requests):
        tree = E.fromstring("""<mxfile version="13.3.6"></mxfile>""")
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            merger = PdfMerger()
            for i, pdf_request in enumerate(pdf_requests):
                self.log.warning("adding page %s", i)
                for diagram in self.extract_diagrams(pdf_request):
                    tree.append(diagram)
                next_pdf = tdp / f"doc-{i}.pdf"
                if pdf_request.get("pdf") is None:  # pragma: no cover
                    raise ValueError("PDF request is empty")
                wrote = next_pdf.write_bytes(b64decode(pdf_request["pdf"]))
                if wrote:
                    merger.append(PdfReader(str(next_pdf)))
            output_pdf = tdp / "output.pdf"
            final_pdf = tdp / "final.pdf"
            merger.write(str(output_pdf))
            composite_xml = E.tostring(tree).decode("utf-8")
            final = PdfWriter()
            final.append_pages_from_reader(PdfReader(str(output_pdf), "rb"))
            if self.attach_xml:
                final.add_attachment(
                    self.attachment_name,
                    composite_xml.encode("utf-8"),
                )
            with final_pdf.open("wb") as fpt:
                final.write(fpt)
            return b64encode(final_pdf.read_bytes()).decode("utf-8")

    async def pdf(self, pdf_requests):
        if not self._server:  # pragma: no cover
            await self.start_server()

        for pdf_request in pdf_requests:
            pdf_request["pdf"] = await self._pdf(pdf_request)

        if len(pdf_requests) == 1:
            return pdf_requests[0]["pdf"]

        return await self._merge(pdf_requests)

    def stop_server(self):
        if self._server is not None:
            self.log.warning("[ipydrawio-export] shutting down")
            self._server.terminate()
            self._server.wait()
            self._server = None

    async def status(self):
        return {
            "has_jlpm": JLPM is not None,
            "is_provisioned": self.is_provisioned,
            "is_provisioning": self.is_provisioning,
            "is_starting": self.is_starting,
            "is_running": self.is_running,
        }

    @property
    def url(self):
        return f"http://localhost:{self.drawio_port}"

    @default("drawio_port")
    def _default_drawio_port(self):
        port = os.environ.get(
            ENV_IPYDRAWIO_PORT,
            os.environ.get(ENV_DRAWIO_PORT),
        )
        if port is None:
            self.log.debug("[ipydrawio-export] getting unused port...")
            port = self.get_unused_port()
        self.log.debug(f"[ipydrawio-export] port: {port}")
        return port

    @default("drawio_server_url")
    def _default_drawio_server_url(self):
        url = DRAWIO_STATIC.as_uri()
        self.log.debug(f"[ipydrawio-export] URL: {url}")
        return url

    @default("_session")
    def _default_session(self):  # pragma: no cover
        if self.pdf_cache is not None:
            self.log.debug("[ipydrawio-export] requests session: cached")
            return CachedSession(self.pdf_cache, allowable_methods=["POST"])

        self.log.debug("[ipydrawio-export] requests session: regular")
        return Session()

    @default("core_params")
    def _default_core_params(self):
        return {"format": "pdf", "base64": "1"}

    @default("drawio_export_workdir")
    def _default_drawio_export_workdir(self):
        data_root = Path(sys.prefix) / "share/jupyter"

        if ENV_JUPYTER_DATA_DIR in os.environ:
            data_root = Path(os.environ[ENV_JUPYTER_DATA_DIR])

        if ENV_IPYDRAWIO_DATA_DIR in os.environ:
            data_root = Path(os.environ[ENV_IPYDRAWIO_DATA_DIR])

        workdir = str(data_root if data_root.name == WORK_DIR else data_root / WORK_DIR)

        self.log.debug(f"[ipydrawio-export] workdir: {workdir}")
        return workdir

    @default("attach_xml")
    def _default_attach_xml(self):
        return True

    def extract_diagrams(self, pdf_request):
        node = None

        errors = []
        try:
            node = E.fromstring(pdf_request["xml"])
        except Exception as err:
            errors += [err]

        if node is None:
            try:
                img = Image.open(BytesIO(b64decode(pdf_request["xml"].encode("utf-8"))))
                node = E.fromstring(urllib.parse.unquote(img.info[PNG_DRAWIO_INFO]))
            except Exception as err:
                errors += [err]

        if node is None:
            self.log.warning("errors encountered extracting xml %s", errors)
            return

        tag = node.tag

        if tag == "mxfile":
            for diagram in node.xpath("//diagram"):
                yield diagram
        elif tag == "mxGraphModel":
            diagram = E.Element("diagram")
            diagram.append(node)
            yield diagram
        elif tag == "{http://www.w3.org/2000/svg}svg":
            diagrams = E.fromstring(node.attrib["content"]).xpath("//diagram")
            for diagram in diagrams:
                yield diagram

    def _start_process(self):
        env = dict(os.environ)
        env_updates = {
            ENV_DRAWIO_PORT: self.drawio_port,
            ENV_DRAWIO_SERVER_URL: self.drawio_server_url,
            ENV_DRAWIO_NODE_ENV: "production",
            ENV_PUPPETEER_CACHE_DIR: self.drawio_export_chromium,
        }
        env.update({k: f"{v}" for k, v in env_updates.items()})

        self.log.debug(f"[ipydrawio-export] extra env: {env_updates}")

        args = [NODE, self.drawio_export_app / DRAWIO_EXPORT_JS]
        self._server = subprocess.Popen([*map(str, args)], env=env)
        return self._server

    async def start_server(self):
        self.stop_server()
        self.log.debug("[ipydrawio-export] starting")
        self.is_starting = True

        if not self.is_provisioned:  # pragma: no cover
            await self.provision()

        self._start_process()

        self.log.warning(
            f"[ipydrawio-export] waiting {self.init_wait_sec}s for server to start",
        )

        await asyncio.sleep(self.init_wait_sec)

        self.log.warning("[ipydrawio-export] server started")

        self.is_starting = False

    @property
    def is_provisioned(self):
        return self.drawio_export_integrity.exists()

    @property
    def is_running(self):
        return self._server is not None and self._server.returncode is None

    @property
    def drawio_export_app(self):
        return Path(self.drawio_export_workdir) / VEND.name

    @property
    def drawio_export_node_modules(self):
        return self.drawio_export_app / "node_modules"

    @property
    def drawio_export_chromium(self):
        cache_dir = os.environ.get(
            ENV_IPYDRAWIO_PUPPETEER_CACHE_DIR,
            os.environ.get(ENV_PUPPETEER_CACHE_DIR),
        )
        if cache_dir is None:
            cache_dir = self.drawio_export_app / DOT_CHROMIUM
        return Path(cache_dir)

    @property
    def drawio_export_puppeteer(self):
        return self.drawio_export_node_modules / "puppeteer"

    @property
    def drawio_export_integrity(self):
        return self.drawio_export_node_modules / ".yarn-integrity"

    @run_on_executor
    def provision(self, force=False):  # pragma: no cover
        self.is_provisioning = True
        env = dict(**os.environ)
        env[ENV_PUPPETEER_CACHE_DIR] = str(self.drawio_export_chromium)
        if not self.drawio_export_app.exists():
            if not self.drawio_export_app.parent.exists():
                self.drawio_export_app.parent.mkdir(parents=True)
            self.log.info(
                "[ipydrawio-export] initializing drawio export app %s",
                self.drawio_export_app,
            )
            shutil.copytree(VEND, self.drawio_export_app)
        else:
            self.log.info(
                "[ipydrawio-export] using existing drawio export folder %s",
                self.drawio_export_app,
            )

        if not self.drawio_export_node_modules.exists() or force:
            self.log.info(
                "[ipydrawio-export] installing drawio export dependencies %s",
                self.drawio_export_app,
            )
            subprocess.check_call(
                [str(JLPM), "--silent", "--ignore-scripts", "--no-optional"],
                cwd=str(self.drawio_export_app),
                env=env,
            )

        if not self.drawio_export_chromium.exists() or force:
            self.log.info(
                "[ipydrawio-export] installing puppeteer %s",
                self.drawio_export_chromium,
            )
            subprocess.check_call(
                [str(NODE), PUPPETEER_INSTALL],
                cwd=str(self.drawio_export_puppeteer),
                env=env,
            )
        self.is_provisioning = False

    def get_unused_port(self):
        """Get an unused port by trying to listen to any random port.

        Probably could introduce race conditions if inside a tight loop.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        sock.close()
        return port

    def attachments(self, pdf_path):
        """Iterate over the name, attachment pairs in the PDF."""
        reader = PdfReader(str(pdf_path), "rb")
        attachments = []
        try:
            attachments = reader.trailer["/Root"]["/Names"]["/EmbeddedFiles"]["/Names"]
        except KeyError:
            pass
        for i, name in enumerate(attachments, 1):
            if not isinstance(name, str):
                continue
            yield name, attachments[i].get_object()["/EF"]["/F"].get_data()
