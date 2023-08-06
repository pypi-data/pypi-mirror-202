"""ipydrawio-export pdf tests"""

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

import pytest
from pypdf import PdfReader


@pytest.mark.parametrize("attach_xml", [0, 1])
def test_export_empty(tmp_path, export_app, any_diagram, attach_xml):
    manager = export_app.drawio_manager
    manager.attach_xml = bool(attach_xml)

    export_app.dio_files = [any_diagram]
    export_app.start()

    out = tmp_path / f"{any_diagram.stem}.pdf"
    assert out.exists(), f"{out} was not created"
    reader = PdfReader(str(out), "rb")
    assert len(reader.pages) == 1

    attachments = sorted(manager.attachments(out))
    assert len(attachments) == attach_xml


@pytest.mark.parametrize("attach_xml", [0, 1])
def test_export_merged(tmp_path, export_app, empty_dio, svg, png, ipynb, attach_xml):
    manager = export_app.drawio_manager
    manager.attach_xml = bool(attach_xml)

    export_app.dio_files = [empty_dio, svg, png, ipynb]
    export_app.start()

    out = tmp_path / f"{empty_dio.stem}.pdf"
    assert out.exists(), f"{out} was not created"

    reader = PdfReader(str(out), "rb")
    assert len(reader.pages) == 4, "unexpected number of pages"

    attachments = sorted(manager.attachments(out))
    assert len(attachments) == attach_xml, "unexpected attachment status"
