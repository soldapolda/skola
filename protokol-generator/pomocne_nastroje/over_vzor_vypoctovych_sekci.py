#!/usr/bin/env python3
"""Ověří strukturální shodu DOCX s ručně schváleným vzorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
W = "{%s}" % NS["w"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def png_size(data: bytes) -> list[int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return list(struct.unpack(">II", data[16:24]))
    return None


def inspect_docx(path: Path) -> dict:
    raw = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        members = sorted(archive.namelist())
        root = ET.fromstring(archive.read("word/document.xml"))
        section = root.find(".//w:sectPr", NS)
        page_size = section.find("w:pgSz", NS) if section is not None else None
        margins = section.find("w:pgMar", NS) if section is not None else None
        media = {}
        for name in members:
            if name.startswith("word/media/"):
                data = archive.read(name)
                media[name] = {
                    "sha256": sha256(data),
                    "size_bytes": len(data),
                    "pixels": png_size(data),
                }

    page_breaks = [
        node
        for node in root.findall(".//w:br", NS)
        if node.get(W + "type") == "page"
    ]
    extents = [
        [int(node.get("cx", "0")), int(node.get("cy", "0"))]
        for node in root.findall(".//wp:extent", NS)
    ]
    return {
        "path": str(path),
        "sha256": sha256(raw),
        "size_bytes": len(raw),
        "zip_integrity": "ok" if bad_member is None else bad_member,
        "package_members": members,
        "tables": len(root.findall(".//w:tbl", NS)),
        "drawings": len(root.findall(".//w:drawing", NS)),
        "math_objects": len(root.findall(".//m:oMath", NS)),
        "math_paragraphs": len(root.findall(".//m:oMathPara", NS)),
        "manual_page_breaks": len(page_breaks),
        "drawing_extents_emu": extents,
        "page_size_twips": {
            "width": int(page_size.get(W + "w", "0")) if page_size is not None else 0,
            "height": int(page_size.get(W + "h", "0")) if page_size is not None else 0,
            "orientation": page_size.get(W + "orient", "portrait") if page_size is not None else None,
        },
        "margins_twips": {
            key: int(margins.get(W + key, "0")) if margins is not None else 0
            for key in ("top", "right", "bottom", "left")
        },
        "media": media,
    }


def comparable(report: dict) -> dict:
    return {key: value for key, value in report.items() if key != "path"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    reference = inspect_docx(args.reference)
    output = inspect_docx(args.output)
    exact = comparable(reference) == comparable(output)
    result = {
        "exact_match": exact,
        "reference": reference,
        "output": output,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if exact else 1


if __name__ == "__main__":
    sys.exit(main())
