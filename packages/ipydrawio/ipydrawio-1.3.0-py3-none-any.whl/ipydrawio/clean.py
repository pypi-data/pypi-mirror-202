"""Utilities for making drawio files clean."""

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

import logging
from pathlib import Path

from .constants import (
    IPYNB_METADATA,
    MIMETYPE,
    MX_CLEAN_ATTRS,
    MX_FILE_TAG,
    MX_GRAPH_TAG,
    MX_PRESERVE_ENTITIES,
    NOTEBOOK_EXTENSIONS,
    SVG_NS_TAG,
    XML_EXTENSIONS,
)

try:
    import lxml.etree as ET

    HAS_LXML = True
except ImportError:  # pragma: no cover
    HAS_LXML = False

try:
    import nbformat

    HAS_NBFORMAT = True
except ImportError:  # pragma: no cover
    HAS_NBFORMAT = False

_log = logging.getLogger(__name__)


def inject_entity_placeholders(in_xml: str) -> str:
    for name, entity in MX_PRESERVE_ENTITIES.items():
        in_xml = in_xml.replace(entity, f"__IPYDRAWIO__{name}")
    return in_xml


def restore_entity_placeholders(out_xml: str) -> str:
    for name, entity in MX_PRESERVE_ENTITIES.items():
        out_xml = out_xml.replace(f"__IPYDRAWIO__{name}", entity)

    return out_xml


def clean_drawio_xml(
    in_xml: str,
    pretty=True,
    indent=2,
    tabs=False,
    mx_attrs=MX_CLEAN_ATTRS,
    log=_log,
) -> str:
    """Clean up one diagram."""
    if not HAS_LXML:  # pragma: no cover
        raise RuntimeError("install lxml to enable cleaning drawio XML")

    if pretty and not in_xml.strip().startswith("<svg"):
        in_xml = inject_entity_placeholders(in_xml)

    root = ET.fromstring(in_xml)

    indent_chars = indent * ("\t" if tabs else " ")

    if root.tag == MX_GRAPH_TAG:
        if pretty:
            ET.indent(root, space=indent_chars)
            out_xml = ET.tostring(root, pretty_print=True, encoding=str)
            return out_xml
        return None
    elif root.tag == MX_FILE_TAG:
        mx = root
    elif root.tag == SVG_NS_TAG:
        content = root.attrib["content"]
        if pretty:
            content = inject_entity_placeholders(content)
        mx = ET.fromstring(content)

    for key in mx_attrs:
        if key in mx.attrib:
            del mx.attrib[key]

    if pretty:
        ET.indent(mx, space=indent_chars)
        out_xml = ET.tostring(mx, pretty_print=True, encoding=str)
        out_xml = restore_entity_placeholders(out_xml)
    else:
        out_xml = ET.tostring(mx, encoding=str)

    if root.tag == SVG_NS_TAG:
        root.attrib["content"] = out_xml
        if pretty:
            ET.indent(root, space=indent_chars)
            out_xml = ET.tostring(root, pretty_print=True, encoding=str)

    if in_xml == out_xml:
        return None
    return out_xml


def clean_drawio_xml_file(
    path: Path,
    pretty=True,
    indent=2,
    tabs=False,
    mx_attrs=MX_CLEAN_ATTRS,
    log=_log,
) -> bool:
    if not HAS_LXML:  # pragma: no cover
        raise RuntimeError("install lxml to enable cleaning drawio XML")

    in_xml = path.read_text(encoding="utf-8")
    out_xml = clean_drawio_xml(in_xml, pretty, indent, tabs, mx_attrs, log)
    if out_xml is not None:
        path.write_text(out_xml, encoding="utf-8")
        return True
    log.info(f"... no change to {path}")
    return False


def clean_drawio_notebook_node(
    nb_node,
    pretty=True,
    indent=2,
    tabs=False,
    mx_attrs=MX_CLEAN_ATTRS,
    log=_log,
) -> bool:
    """Strip headers and identifying information from drawio notebook node metadata/outputs."""
    changed = False

    meta = nb_node["metadata"].get(IPYNB_METADATA)
    if meta:
        in_xml = meta["xml"]
        out_xml = clean_drawio_xml(in_xml, pretty, indent, tabs, mx_attrs, log)
        if out_xml:
            meta["xml"] = out_xml
            changed = True

    for cell in nb_node["cells"]:
        for output in cell.get("outputs", []):
            in_xml = output.get("data", {}).get(MIMETYPE)
            if not in_xml:
                continue
            out_xml = clean_drawio_xml(in_xml, pretty, indent, tabs, mx_attrs, log)
            if out_xml:
                output["data"][MIMETYPE] = out_xml
                changed = True

    return changed


def clean_drawio_notebook_file(
    path: Path,
    pretty=True,
    indent=2,
    tabs=False,
    mx_attrs=MX_CLEAN_ATTRS,
    log=_log,
) -> bool:
    """Strip headers and identifying information from drawio notebook file metadata/outputs."""
    if not HAS_LXML and HAS_NBFORMAT:  # pragma: no cover
        raise RuntimeError(
            "install lxml and nbformat to enable cleaning drawio notebooks",
        )

    nb_node = nbformat.reads(
        path.read_text(encoding="utf-8"),
        as_version=nbformat.NO_CONVERT,
    )

    if clean_drawio_notebook_node(nb_node, pretty, indent, tabs, mx_attrs, log):
        path.write_text(nbformat.writes(nb_node), encoding="utf-8")
        return True

    log.info(f"... no change to {path}")
    return False


def clean_drawio_file(
    path: Path,
    pretty=True,
    indent=2,
    tabs=False,
    mx_attrs=MX_CLEAN_ATTRS,
    log=_log,
) -> bool:
    """Strip headers and identifying information from drawio files."""
    log.info(f"cleaning {path}...")

    if path.suffix in XML_EXTENSIONS:
        return clean_drawio_xml_file(path, pretty, indent, tabs, mx_attrs, log)
    elif path.suffix in NOTEBOOK_EXTENSIONS:
        return clean_drawio_notebook_file(path, pretty, indent, tabs, mx_attrs, log)
    else:
        raise NotImplementedError(f"Can't clean {path.suffix}")
