""""main importable for ipydrawio."""

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


from ipydrawio_widgets import XML, Diagram

from ._version import __ext__, __js__, __ns__, __prefix__, __version__


def _ipydrawio_labextension_paths(prefix=__prefix__, extensions=__ext__):
    """Reused by other ipydrawio extensions with other prefixes/extensions."""
    return [{"src": str(prefix / e), "dest": f"{__ns__}/{e}"} for e in extensions]


_jupyter_labextension_paths = _ipydrawio_labextension_paths


__all__ = [
    "__js__",
    "__version__",
    "_jupyter_labextension_paths",
    "Diagram",
    "XML",
]
