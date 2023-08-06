"""source of truth for ipydrawio version."""

# Copyright 2023 ipydrawio contributors
# Copyright 2020 jupyterlab-drawio contributors
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

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
__ns__ = "@deathbeds"
__ext__ = [
    "ipydrawio",  # source the version from here
    "ipydrawio-webpack",
    "ipydrawio-jupyter-templates",
    "ipydrawio-notebook",
]

IN_TREE = (HERE / "../../_").resolve()
IN_PREFIX = Path(sys.prefix) / f"share/jupyter/labextensions/{__ns__}"

__prefix__ = IN_TREE if IN_TREE.exists() else IN_PREFIX

PKG_JSON = __prefix__ / __ext__[0] / "package.json"

__js__ = json.loads(PKG_JSON.read_text(encoding="utf-8"))


__version__ = __js__["version"]

__all__ = ["__version__", "__js__", "__ns__", "__ext__", "__prefix__"]
