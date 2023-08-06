"""CLI for ipydrawio."""

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

import sys
from pathlib import Path

import traitlets as T
from jupyter_core.application import JupyterApp, base_aliases, base_flags

from ._version import __version__
from .clean import clean_drawio_file
from .constants import MX_CLEAN_ATTRS

TRIMMED_FLAGS = {
    name: flag
    for name, flag in base_flags.items()
    if name not in ["show-config", "show-config-json", "generate-config", "y"]
}


class BaseApp(JupyterApp):
    version = __version__

    flags = TRIMMED_FLAGS

    @property
    def description(self):  # pragma: no cover
        return self.__doc__.splitlines()[0].strip()


class CleanApp(BaseApp):

    """clean drawio files."""

    dio_files = T.Tuple()
    pretty = T.Bool(True, help="pretty-print the XML").tag(config=True)
    mx_attrs = T.Tuple(MX_CLEAN_ATTRS, help="attributes to clean").tag(config=True)
    indent = T.Int(2, help="if pretty-printing, the indent level").tag(config=True)
    tabs = T.Bool(False, help="indent with tabs instead of spaces").tag(config=True)

    flags = dict(
        **TRIMMED_FLAGS,
        **{
            "no-pretty": (
                {"CleanApp": {"pretty": False}},
                "Do not pretty-print the XML",
            ),
            "tabs": (
                {"CleanApp": {"tabs": True}},
                "Indent with tabs instead of spaces",
            ),
        },
    )
    aliases = dict(
        **base_aliases,
        **{"mx-attrs": "CleanApp.mx_attrs", "indent": "CleanApp.indent"},
    )

    def parse_command_line(self, argv=None):
        super().parse_command_line(argv)
        self.dio_files = [Path(p).resolve() for p in self.extra_args]

    def start(self):
        for path in self.dio_files:
            try:
                clean_drawio_file(
                    path,
                    pretty=self.pretty,
                    mx_attrs=self.mx_attrs,
                    indent=self.indent,
                    tabs=self.tabs,
                    log=self.log,
                )
            except Exception as err:
                self.log.error(err)
                sys.exit(1)


class IPyDrawioApp(BaseApp):

    """ipydrawio utilities."""

    name = "ipydrawio"
    subcommands = {
        "clean": (CleanApp, CleanApp.__doc__.splitlines()[0]),
    }


main = launch_instance = IPyDrawioApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()
