"""constants for ``ipydrawio-export``."""

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


from ipydrawio.constants import IPYNB_METADATA

#: the header to look for in PNG metadata
PNG_DRAWIO_INFO = "mxfile"

#: a path to the drawio static assets
DRAWIO_APP = "../labextensions/@deathbeds/ipydrawio-webpack/static/dio"

# environment variables
#: environment variable for the well-known Jupyter data directory environment variable
ENV_JUPYTER_DATA_DIR = "JUPYTER_DATA_DIR"
#: environment variable for a custom data directory for ``ipydrawio-export``
ENV_IPYDRAWIO_DATA_DIR = "IPYDRAWIO_DATA_DIR"
#: environment variable for the URL for the drawio server
ENV_DRAWIO_SERVER_URL = "DRAWIO_SERVER_URL"
#: environment variable for a port to bind the drawio server to, otherwise pick an unused port
ENV_IPYDRAWIO_PORT = "IPYDRAWIO_PORT"
#: environment variable for the cache directory for the chromium download
ENV_PUPPETEER_CACHE_DIR = "PUPPETEER_CACHE_DIR"
#: environment variable for a custom cache directory for the chromium download
ENV_IPYDRAWIO_PUPPETEER_CACHE_DIR = "IPYDRAWIO_PUPPETEER_CACHE_DIR"

#: always appended to ``*_DATA_DIR``
WORK_DIR = "ipydrawio_export"

__all__ = [
    "IPYNB_METADATA",
    "PNG_DRAWIO_INFO",
    "DRAWIO_APP",
    "ENV_JUPYTER_DATA_DIR",
    "ENV_IPYDRAWIO_DATA_DIR",
    "WORK_DIR",
]

# drawio export server
#: the port of the drawio server
ENV_DRAWIO_PORT = "PORT"
#: the nodejs environment string ``production`` given to the drawio server
ENV_DRAWIO_NODE_ENV = "NODE_ENV"
#: the name of the puppeteer install script
PUPPETEER_INSTALL = "install.js"
#: the directory for the downloaded chromium
DOT_CHROMIUM = ".chromium"
#: the path to the export script
DRAWIO_EXPORT_JS = "export.js"
