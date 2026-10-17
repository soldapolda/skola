#!/usr/bin/env python3
"""Vytvoří schválený teoretický protokol ZELE 1Z z referenčního DOCX.

Skript záměrně nepoužívá externí knihovnu pro Word. Zachová původní titulní
tabulku a upravuje pouze potřebné části OOXML. Všechny samostatné výpočty jsou
v dokumentu uloženy jako nativní objekty OMML.
"""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path
import math
import re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "vzory" / "protokol_1.docx"
MEASUREMENT = ROOT / "1Z-zele-1"
OUTPUT = MEASUREMENT / "vystup"
SCHEMES = OUTPUT / "schemata"
WORK = MEASUREMENT / "pracovni"
DOCX_OUT = OUTPUT / "protokol.docx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(prefix: str, name: str) -> str:
    return f"{{{NS[prefix]}}}{name}"


def w_el(name: str, attrs: dict[str, str] | None = None) -> ET.Element:
    el = ET.Element(q("w", name))
    for key, value in (attrs or {}).items():
        el.set(q("w", key), value)
    return el


def m_el(name: str, attrs: dict[str, str] | None = None) -> ET.Element:
    el = ET.Element(q("m", name))
    for key, value in (attrs or {}).items():
        el.set(q("m", key), value)
    return el


def add_run(
    paragraph: ET.Element,
    text: str,
    *,
    font: str = "Times New Roman",
    size: int = 24,
    bold: bool = False,
    italic: bool = False,
    subscript: bool = False,
    superscript: bool = False,
) -> ET.Element:
    run = ET.SubElement(paragraph, q("w", "r"))
    rpr = ET.SubElement(run, q("w", "rPr"))
    ET.SubElement(
        rpr,
        q("w", "rFonts"),
        {q("w", "ascii"): font, q("w", "hAnsi"): font, q("w", "cs"): font},
    )
    if bold:
        ET.SubElement(rpr, q("w", "b"))
    if italic:
        ET.SubElement(rpr, q("w", "i"))
    ET.SubElement(rpr, q("w", "sz"), {q("w", "val"): str(size)})
    ET.SubElement(rpr, q("w", "szCs"), {q("w", "val"): str(size)})
    if subscript:
        ET.SubElement(rpr, q("w", "vertAlign"), {q("w", "val"): "subscript"})
    if superscript:
        ET.SubElement(rpr, q("w", "vertAlign"), {q("w", "val"): "superscript"})
    node = ET.SubElement(run, q("w", "t"))
    if text.startswith(" ") or text.endswith(" "):
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    node.text = text
    return run


def paragraph(
    text: str = "",
    *,
    align: str = "both",
    before: int = 0,
    after: int = 100,
    line: int = 276,
    line_rule: str = "auto",
    keep_next: bool = False,
    page_break_before: bool = False,
    first_line: int | None = None,
) -> ET.Element:
    p = w_el("p")
    ppr = ET.SubElement(p, q("w", "pPr"))
    # CT_PPr má pevné pořadí prvků; LibreOffice je při importu přísnější než Word.
    if keep_next:
        ET.SubElement(ppr, q("w", "keepNext"))
    if page_break_before:
        ET.SubElement(ppr, q("w", "pageBreakBefore"))
    ET.SubElement(
        ppr,
        q("w", "spacing"),
        {
            q("w", "before"): str(before),
            q("w", "after"): str(after),
            q("w", "line"): str(line),
            q("w", "lineRule"): line_rule,
        },
    )
    if first_line is not None:
        ET.SubElement(ppr, q("w", "ind"), {q("w", "firstLine"): str(first_line)})
    ET.SubElement(ppr, q("w", "jc"), {q("w", "val"): align})
    if text:
        add_run(p, text)
    return p


def heading(text: str, *, page_break_before: bool = False) -> ET.Element:
    p = paragraph(
        align="left",
        before=140,
        after=70,
        line=240,
        keep_next=True,
        page_break_before=page_break_before,
    )
    add_run(p, text, font="Arial", size=24, bold=True)
    return p


def page_break() -> ET.Element:
    p = paragraph(after=0, line=240)
    run = ET.SubElement(p, q("w", "r"))
    ET.SubElement(run, q("w", "br"), {q("w", "type"): "page"})
    return p


def spacer(height: int) -> ET.Element:
    """Pevný prázdný řádek, který LibreOffice započítá i po vysoké OMML rovnici."""
    p = paragraph(align="left", after=0, line=height, line_rule="exact")
    add_run(p, "\u00a0", size=2)
    return p


def set_cell_content(cell: ET.Element, children: list[ET.Element]) -> None:
    tcpr = cell.find(q("w", "tcPr"))
    saved = deepcopy(tcpr) if tcpr is not None else None
    for child in list(cell):
        cell.remove(child)
    if saved is not None:
        cell.append(saved)
    for child in children:
        cell.append(child)


def title_label_value(label: str, value: str, *, centered: bool = False) -> ET.Element:
    p = paragraph(align="center" if centered else "left", after=0, line=220)
    add_run(p, label, size=24)
    add_run(p, value, size=24, bold=True)
    return p


def math_run(text: str, *, plain: bool = False) -> ET.Element:
    run = m_el("r")
    rpr = ET.SubElement(run, q("m", "rPr"))
    if plain:
        ET.SubElement(rpr, q("m", "sty"), {q("m", "val"): "p"})
    node = ET.SubElement(run, q("m", "t"))
    if text.startswith(" ") or text.endswith(" "):
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    node.text = text
    return run


def math_group(*children: ET.Element) -> ET.Element:
    group = m_el("e")
    for child in children:
        group.append(child)
    return group


def math_sub(base: str | ET.Element, sub: str | ET.Element) -> ET.Element:
    node = m_el("sSub")
    ET.SubElement(node, q("m", "sSubPr"))
    base_el = ET.SubElement(node, q("m", "e"))
    base_el.append(math_run(base) if isinstance(base, str) else base)
    sub_el = ET.SubElement(node, q("m", "sub"))
    sub_el.append(math_run(sub) if isinstance(sub, str) else sub)
    return node


def math_sup(base: str | ET.Element, sup: str | ET.Element) -> ET.Element:
    node = m_el("sSup")
    ET.SubElement(node, q("m", "sSupPr"))
    base_el = ET.SubElement(node, q("m", "e"))
    base_el.append(math_run(base) if isinstance(base, str) else base)
    sup_el = ET.SubElement(node, q("m", "sup"))
    sup_el.append(math_run(sup) if isinstance(sup, str) else sup)
    return node


def math_frac(numerator: list[ET.Element], denominator: list[ET.Element]) -> ET.Element:
    node = m_el("f")
    ET.SubElement(node, q("m", "fPr"))
    num = ET.SubElement(node, q("m", "num"))
    den = ET.SubElement(node, q("m", "den"))
    for child in numerator:
        num.append(child)
    for child in denominator:
        den.append(child)
    return node


def equation(children: list[ET.Element], *, after: int = 100, line: int = 480) -> ET.Element:
    # Minimální výška chrání zlomky a indexy před překrytím následujícím
    # odstavcem při importu ve starších verzích Wordu a v LibreOffice.
    p = paragraph(align="center", after=after, line=line, line_rule="atLeast")
    # Inline OMML uvnitř vystředěného odstavce je platný WordprocessingML.
    # m:oMathPara je naopak blokový prvek a nesmí být vnořen do w:p.
    omath = ET.SubElement(p, q("m", "oMath"))
    for child in children:
        omath.append(child)
    return p


def title_values_paragraph(groups: list[tuple[str, str, str]]) -> ET.Element:
    p = paragraph(align="center", after=10, line=220)
    for index, (base, sub, value) in enumerate(groups):
        if index:
            add_run(p, "      ", size=21)
        omath = ET.SubElement(p, q("m", "oMath"))
        omath.append(math_sub(base, sub))
        omath.append(math_run(f" = {value}", plain=True))
    return p


def drawing_paragraph(rel_id: str, name: str, width_in: float, height_in: float) -> ET.Element:
    cx = str(round(width_in * 914400))
    cy = str(round(height_in * 914400))
    p = paragraph(align="center", after=20, line=240)
    run = ET.SubElement(p, q("w", "r"))
    drawing = ET.SubElement(run, q("w", "drawing"))
    inline = ET.SubElement(
        drawing,
        q("wp", "inline"),
        {"distT": "0", "distB": "0", "distL": "0", "distR": "0"},
    )
    ET.SubElement(inline, q("wp", "extent"), {"cx": cx, "cy": cy})
    ET.SubElement(inline, q("wp", "effectExtent"), {"l": "0", "t": "0", "r": "0", "b": "0"})
    ET.SubElement(inline, q("wp", "docPr"), {"id": "100" if rel_id.endswith("11") else "101", "name": name})
    frame_pr = ET.SubElement(inline, q("wp", "cNvGraphicFramePr"))
    ET.SubElement(frame_pr, q("a", "graphicFrameLocks"), {"noChangeAspect": "1"})
    graphic = ET.SubElement(inline, q("a", "graphic"))
    graphic_data = ET.SubElement(
        graphic,
        q("a", "graphicData"),
        {"uri": "http://schemas.openxmlformats.org/drawingml/2006/picture"},
    )
    pic = ET.SubElement(graphic_data, q("pic", "pic"))
    nv = ET.SubElement(pic, q("pic", "nvPicPr"))
    ET.SubElement(nv, q("pic", "cNvPr"), {"id": "0", "name": name})
    c_nv = ET.SubElement(nv, q("pic", "cNvPicPr"))
    ET.SubElement(c_nv, q("a", "picLocks"), {"noChangeAspect": "1"})
    fill = ET.SubElement(pic, q("pic", "blipFill"))
    ET.SubElement(fill, q("a", "blip"), {q("r", "embed"): rel_id})
    stretch = ET.SubElement(fill, q("a", "stretch"))
    ET.SubElement(stretch, q("a", "fillRect"))
    sppr = ET.SubElement(pic, q("pic", "spPr"))
    xfrm = ET.SubElement(sppr, q("a", "xfrm"))
    ET.SubElement(xfrm, q("a", "off"), {"x": "0", "y": "0"})
    ET.SubElement(xfrm, q("a", "ext"), {"cx": cx, "cy": cy})
    geom = ET.SubElement(sppr, q("a", "prstGeom"), {"prst": "rect"})
    ET.SubElement(geom, q("a", "avLst"))
    return p


def q3(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def decimal_cz(value: Decimal) -> str:
    return f"{value:.3f}".replace(".", ",")


def decimal_cz_n(value: Decimal, places: int) -> str:
    return f"{value:.{places}f}".replace(".", ",")


def calculations() -> dict[str, Decimal]:
    getcontext().prec = 40
    rho = Decimal("17.8e-9")
    ua = Decimal("7.5")
    ub = Decimal("12.5")
    ria_mohm = Decimal("73")
    rib_mohm = Decimal("54")
    la = Decimal("0.82")
    lb = Decimal("2")
    sa = Decimal("6e-6")
    sb = Decimal("7.3e-6")
    rs = Decimal("0.033")

    rva_mohm = q3(rho * la / sa * Decimal("1000"))
    rvb_mohm = q3(rho * lb / sb * Decimal("1000"))
    ra_mohm = q3(ria_mohm + rva_mohm)
    rb_mohm = q3(rib_mohm + rvb_mohm)
    ra = ra_mohm / Decimal("1000")
    rb = rb_mohm / Decimal("1000")

    us_raw = (ua / ra + ub / rb) / (Decimal("1") / ra + Decimal("1") / rb + Decimal("1") / rs)
    us = q3(us_raw)
    ia = q3((ua - us) / ra)
    ib = q3((ub - us) / rb)
    is_ = q3(us / rs)
    ps = q3(us * is_)
    dpa = q3(ia * ia * ra)
    dpb = q3(ib * ib * rb)
    dp = q3(dpa + dpb)
    eta = q3(ps / (ps + dp) * Decimal("100"))
    pin = q3(ua * ia + ub * ib)
    balance = q3(abs(pin - (ps + dp)))

    return {
        "rva_mohm": rva_mohm,
        "rvb_mohm": rvb_mohm,
        "ra_mohm": ra_mohm,
        "rb_mohm": rb_mohm,
        "ra": ra,
        "rb": rb,
        "us": us,
        "ia": ia,
        "ib": ib,
        "is": is_,
        "ps": ps,
        "dpa": dpa,
        "dpb": dpb,
        "dp": dp,
        "eta": eta,
        "pin": pin,
        "balance": balance,
    }


ITALIC_FONT = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf"
REGULAR_FONT = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(ITALIC_FONT if italic else REGULAR_FONT, size)


def pil_math(draw: ImageDraw.ImageDraw, xy: tuple[int, int], base: str, sub: str, *, size: int = 64) -> None:
    x, y = xy
    main_font = font(size)
    sub_font = font(round(size * 0.62))
    draw.text((x, y), base, font=main_font, fill="black")
    bbox = draw.textbbox((x, y), base, font=main_font)
    draw.text((bbox[2] + 2, y + round(size * 0.45)), sub, font=sub_font, fill="black")


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], width: int = 7) -> None:
    draw.line([start, end], fill="black", width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 24
    wing = math.pi / 6
    p1 = (end[0] - length * math.cos(angle - wing), end[1] - length * math.sin(angle - wing))
    p2 = (end[0] - length * math.cos(angle + wing), end[1] - length * math.sin(angle + wing))
    draw.polygon([end, p1, p2], fill="black")


def resistor_h(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int) -> None:
    lead = 40
    h = 62
    draw.line((x1, y, x1 + lead, y), fill="black", width=7)
    draw.rectangle((x1 + lead, y - h // 2, x2 - lead, y + h // 2), outline="black", width=7)
    draw.line((x2 - lead, y, x2, y), fill="black", width=7)


def resistor_v(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int) -> None:
    lead = 35
    w = 58
    draw.line((x, y1, x, y1 + lead), fill="black", width=7)
    draw.rectangle((x - w // 2, y1 + lead, x + w // 2, y2 - lead), outline="black", width=7)
    draw.line((x, y2 - lead, x, y2), fill="black", width=7)


def battery_v(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int) -> None:
    center = (top + bottom) // 2
    draw.line((x, top, x, center - 45), fill="black", width=7)
    draw.line((x - 65, center - 45, x + 65, center - 45), fill="black", width=8)
    draw.line((x - 38, center + 15, x + 38, center + 15), fill="black", width=8)
    draw.line((x, center + 15, x, bottom), fill="black", width=7)


def node(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill="black")


def draw_main_png(path: Path) -> None:
    img = Image.new("RGB", (1800, 980), "white")
    d = ImageDraw.Draw(img)
    left, center, right = 260, 900, 1540
    top, bottom = 190, 820

    d.line((left, top, left + 150, top), fill="black", width=7)
    resistor_h(d, left + 150, center, top)
    resistor_h(d, center, right - 150, top)
    d.line((right - 150, top, right, top), fill="black", width=7)
    resistor_v(d, left, top, top + 310)
    battery_v(d, left, top + 310, bottom)
    resistor_v(d, right, top, top + 310)
    battery_v(d, right, top + 310, bottom)
    d.line((left, bottom, right, bottom), fill="black", width=7)
    resistor_v(d, center, top, bottom)
    node(d, center, top)
    node(d, center, bottom)

    arrow(d, (360, 115), (520, 115))
    pil_math(d, (395, 40), "I", "A", size=60)
    arrow(d, (1440, 115), (1280, 115))
    pil_math(d, (1335, 40), "I", "B", size=60)
    arrow(d, (980, 265), (980, 410))
    pil_math(d, (1010, 290), "I", "S", size=60)

    pil_math(d, (565, 85), "R", "vA", size=58)
    pil_math(d, (1090, 85), "R", "vB", size=58)
    pil_math(d, (85, 310), "R", "iA", size=58)
    pil_math(d, (1580, 310), "R", "iB", size=58)
    pil_math(d, (995, 470), "R", "S", size=58)
    pil_math(d, (70, 520), "U", "iA", size=58)
    pil_math(d, (1570, 520), "U", "iB", size=58)
    pil_math(d, (735, 535), "U", "S", size=58)
    arrow(d, (150, 580), (150, 720), width=5)
    arrow(d, (1650, 580), (1650, 720), width=5)
    arrow(d, (820, 580), (820, 720), width=5)
    img.save(path, dpi=(300, 300))


def draw_equivalent_png(path: Path) -> None:
    img = Image.new("RGB", (1700, 900), "white")
    d = ImageDraw.Draw(img)
    left, center, right = 290, 850, 1410
    top, bottom = 150, 760
    d.line((left, top, right, top), fill="black", width=7)
    resistor_v(d, left, top, top + 300)
    battery_v(d, left, top + 300, bottom)
    resistor_v(d, right, top, top + 300)
    battery_v(d, right, top + 300, bottom)
    d.line((left, bottom, right, bottom), fill="black", width=7)
    resistor_v(d, center, top, bottom)
    node(d, center, top)
    node(d, center, bottom)

    arrow(d, (360, 85), (520, 85))
    pil_math(d, (390, 15), "I", "A", size=58)
    arrow(d, (1340, 85), (1180, 85))
    pil_math(d, (1230, 15), "I", "B", size=58)
    arrow(d, (930, 250), (930, 395))
    pil_math(d, (960, 275), "I", "S", size=58)
    pil_math(d, (135, 315), "R", "A", size=58)
    pil_math(d, (1440, 315), "R", "B", size=58)
    pil_math(d, (950, 460), "R", "S", size=58)
    pil_math(d, (95, 480), "U", "iA", size=58)
    pil_math(d, (1450, 480), "U", "iB", size=58)
    pil_math(d, (640, 515), "U", "S", size=58)
    arrow(d, (180, 535), (180, 675), width=5)
    arrow(d, (1535, 535), (1535, 675), width=5)
    arrow(d, (770, 535), (770, 675), width=5)
    img.save(path, dpi=(300, 300))


def svg_math(base: str, sub: str, x: int, y: int, size: int = 48, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Times New Roman, serif" '
        f'font-size="{size}" font-style="italic">{base}'
        f'<tspan baseline-shift="sub" font-size="{round(size * 0.62)}">{sub}</tspan></text>'
    )


def svg_arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" marker-end="url(#arrow)"/>'


def svg_resistor_h(x1: int, x2: int, y: int) -> str:
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x1+40}" y2="{y}" class="wire"/>'
        f'<rect x="{x1+40}" y="{y-30}" width="{x2-x1-80}" height="60" class="component"/>'
        f'<line x1="{x2-40}" y1="{y}" x2="{x2}" y2="{y}" class="wire"/>'
    )


def svg_resistor_v(x: int, y1: int, y2: int) -> str:
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y1+35}" class="wire"/>'
        f'<rect x="{x-29}" y="{y1+35}" width="58" height="{y2-y1-70}" class="component"/>'
        f'<line x1="{x}" y1="{y2-35}" x2="{x}" y2="{y2}" class="wire"/>'
    )


def svg_battery(x: int, top: int, bottom: int) -> str:
    center = (top + bottom) // 2
    return (
        f'<line x1="{x}" y1="{top}" x2="{x}" y2="{center-45}" class="wire"/>'
        f'<line x1="{x-65}" y1="{center-45}" x2="{x+65}" y2="{center-45}" class="plate"/>'
        f'<line x1="{x-38}" y1="{center+15}" x2="{x+38}" y2="{center+15}" class="plate"/>'
        f'<line x1="{x}" y1="{center+15}" x2="{x}" y2="{bottom}" class="wire"/>'
    )


def svg_document(body: str, width: int, height: int) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,5 L0,10 z" fill="#000"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fff"/>
  <style>.wire{{stroke:#000;stroke-width:7;fill:none}} .component{{stroke:#000;stroke-width:7;fill:#fff}} .plate{{stroke:#000;stroke-width:8}}</style>
  {body}
</svg>
'''


def write_svgs() -> None:
    left, center, right = 260, 900, 1540
    top, bottom = 190, 820
    main = [
        f'<line x1="{left}" y1="{top}" x2="{left+150}" y2="{top}" class="wire"/>',
        svg_resistor_h(left + 150, center, top),
        svg_resistor_h(center, right - 150, top),
        f'<line x1="{right-150}" y1="{top}" x2="{right}" y2="{top}" class="wire"/>',
        svg_resistor_v(left, top, top + 310),
        svg_battery(left, top + 310, bottom),
        svg_resistor_v(right, top, top + 310),
        svg_battery(right, top + 310, bottom),
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="wire"/>',
        svg_resistor_v(center, top, bottom),
        f'<circle cx="{center}" cy="{top}" r="12" fill="#000"/><circle cx="{center}" cy="{bottom}" r="12" fill="#000"/>',
        svg_arrow(360, 115, 520, 115), svg_math("I", "A", 425, 70),
        svg_arrow(1440, 115, 1280, 115), svg_math("I", "B", 1360, 70),
        svg_arrow(980, 265, 980, 410), svg_math("I", "S", 1010, 320),
        svg_math("R", "vA", 610, 120), svg_math("R", "vB", 1110, 120),
        svg_math("R", "iA", 90, 360), svg_math("R", "iB", 1580, 360),
        svg_math("R", "S", 995, 520),
        svg_math("U", "iA", 75, 560), svg_arrow(150, 580, 150, 720),
        svg_math("U", "iB", 1570, 560), svg_arrow(1650, 580, 1650, 720),
        svg_math("U", "S", 735, 580), svg_arrow(820, 580, 820, 720),
    ]
    (SCHEMES / "hlavni_schema.svg").write_text(svg_document("\n  ".join(main), 1800, 980), encoding="utf-8")

    left, center, right = 290, 850, 1410
    top, bottom = 150, 760
    equivalent = [
        f'<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" class="wire"/>',
        svg_resistor_v(left, top, top + 300), svg_battery(left, top + 300, bottom),
        svg_resistor_v(right, top, top + 300), svg_battery(right, top + 300, bottom),
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="wire"/>',
        svg_resistor_v(center, top, bottom),
        f'<circle cx="{center}" cy="{top}" r="12" fill="#000"/><circle cx="{center}" cy="{bottom}" r="12" fill="#000"/>',
        svg_arrow(360, 85, 520, 85), svg_math("I", "A", 420, 45),
        svg_arrow(1340, 85, 1180, 85), svg_math("I", "B", 1260, 45),
        svg_arrow(930, 250, 930, 395), svg_math("I", "S", 960, 300),
        svg_math("R", "A", 140, 350), svg_math("R", "B", 1440, 350), svg_math("R", "S", 950, 500),
        svg_math("U", "iA", 100, 520), svg_arrow(180, 535, 180, 675),
        svg_math("U", "iB", 1450, 520), svg_arrow(1535, 535, 1535, 675),
        svg_math("U", "S", 640, 555), svg_arrow(770, 535, 770, 675),
    ]
    (SCHEMES / "nahradni_schema.svg").write_text(svg_document("\n  ".join(equivalent), 1700, 900), encoding="utf-8")


def eq_sub(base: str, sub: str) -> ET.Element:
    return math_sub(base, sub)


def plain(text: str) -> ET.Element:
    return math_run(text, plain=True)


def italic(text: str) -> ET.Element:
    return math_run(text)


def build_body(calc: dict[str, Decimal]) -> list[ET.Element]:
    # Titulní tabulka sama přesně vyplňuje první stranu; ruční zalomení by
    # proto vytvořilo prázdnou druhou stranu.
    out: list[ET.Element] = []

    out.append(heading("ÚVOD:"))
    out.append(paragraph(
        "Předmětem projektu je teoretické posouzení napájení stejnosměrné zátěže ze dvou reálných "
        "stejnosměrných zdrojů A a B. Zdroje mají rozdílná vnitřní napětí a vnitřní odpory. "
        "Propojovací měděné vodiče mají nezanedbatelný odpor, a proto způsobují další úbytek napětí "
        "a výkonové ztráty. Zátěž je pro účely výpočtu uvažována jako ideální lineární rezistor. "
        "Situace odpovídá například napájení startéru z jedné nebo ze dvou autobaterií pomocí "
        "startovacích kabelů.",
        first_line=420,
    ))

    out.append(heading("ZADÁNÍ:"))
    out.append(paragraph(
        "Stejnosměrná zátěž je napájena ze dvou reálných stejnosměrných zdrojů A a B. "
        "Odpory měděných vodičů se vypočítají z jejich délky, průřezu a měrného elektrického "
        "odporu mědi. Jmenovitý odpor lineární zátěže lze obecně určit ze jmenovitého napětí "
        "a výkonu; v tomto individuálním zadání je však hodnota odporu zátěže zadána přímo.",
        first_line=420,
    ))
    out.append(equation([
        italic("R"), plain(" = "), math_frac([math_sup(eq_sub("U", "n"), "2")], [eq_sub("P", "n")]),
        plain("; pro výpočet "), eq_sub("R", "S"), plain(" = 33 mΩ")
    ]))
    out.append(paragraph(
        "Vypočítá se napětí na zátěži Uₛ, výkon na zátěži Pₛ, celkové výkonové ztráty ΔP "
        "na všech parazitních odporech a účinnost přenosu výkonu η.",
        first_line=420,
    ))

    out.append(heading("NÁHRADNÍ SCHÉMA:"))
    out.append(paragraph(
        "Pro výpočet jsou vnitřní odpor zdroje a odpor přívodního vodiče v každé větvi "
        "sloučeny do výsledných odporů Rₐ a Rᵦ.",
        first_line=420,
        keep_next=True,
    ))
    out.append(drawing_paragraph("rId12", "Náhradní schéma", 5.9, 3.12))

    # Samostatný zalamovací odstavec je v LibreOffice stabilnější než
    # w:pageBreakBefore přímo na nadpisu a zachová nadpis na vlastním řádku.
    out.append(page_break())
    out.append(heading("VÝPOČTY:"))
    out.append(paragraph(
        "V souladu se zadáním se každý mezivýsledek zaokrouhluje na tři desetinná místa a "
        "zaokrouhlená hodnota se používá v následujícím kroku. Malé odpory jsou proto "
        "zaokrouhlovány v mΩ a před dosazením převedeny na Ω.",
        first_line=420,
    ))

    out.append(paragraph("Převod průřezů vodičů do jednotek SI:", align="left", keep_next=True))
    out.append(equation([
        eq_sub("S", "A"), plain(" = 6 "), math_sup("mm", "2"), plain(" = 6·"), math_sup("10", "−6"), plain(" "), math_sup("m", "2"),
        plain(";   "), eq_sub("S", "B"), plain(" = 7,3 "), math_sup("mm", "2"), plain(" = 7,3·"), math_sup("10", "−6"), plain(" "), math_sup("m", "2")
    ]))

    out.append(paragraph("Odpor měděného vodiče ve větvi A:", align="left", keep_next=True))
    out.append(equation([
        eq_sub("R", "vA"), plain(" = "), eq_sub("ρ", "Cu"), math_frac([eq_sub("l", "A")], [eq_sub("S", "A")]),
        plain(" = 17,8·"), math_sup("10", "−9"), plain("·"), math_frac([plain("0,82")], [plain("6·"), math_sup("10", "−6")]),
        plain(f" = {decimal_cz(calc['rva_mohm'])} mΩ")
    ]))
    out.append(equation([
        eq_sub("R", "A"), plain(" = "), eq_sub("R", "iA"), plain(" + "), eq_sub("R", "vA"),
        plain(f" = 73,000 + {decimal_cz(calc['rva_mohm'])} = {decimal_cz(calc['ra_mohm'])} mΩ = {decimal_cz_n(calc['ra'], 6)} Ω")
    ]))

    out.append(paragraph("Odpor měděného vodiče ve větvi B:", align="left", keep_next=True))
    out.append(equation([
        eq_sub("R", "vB"), plain(" = "), eq_sub("ρ", "Cu"), math_frac([eq_sub("l", "B")], [eq_sub("S", "B")]),
        plain(" = 17,8·"), math_sup("10", "−9"), plain("·"), math_frac([plain("2")], [plain("7,3·"), math_sup("10", "−6")]),
        plain(f" = {decimal_cz(calc['rvb_mohm'])} mΩ")
    ]))
    out.append(equation([
        eq_sub("R", "B"), plain(" = "), eq_sub("R", "iB"), plain(" + "), eq_sub("R", "vB"),
        plain(f" = 54,000 + {decimal_cz(calc['rvb_mohm'])} = {decimal_cz(calc['rb_mohm'])} mΩ = {decimal_cz_n(calc['rb'], 6)} Ω")
    ]))

    out.append(paragraph(
        "Napětí na zátěži se určí metodou uzlových napětí. Proudy obou zdrojových větví "
        "směřují do společného uzlu a jejich součet se rovná proudu zátěží:",
        first_line=420,
        keep_next=True,
    ))
    out.append(equation([
        math_frac([eq_sub("U", "iA"), plain(" − "), eq_sub("U", "S")], [eq_sub("R", "A")]),
        plain(" + "),
        math_frac([eq_sub("U", "iB"), plain(" − "), eq_sub("U", "S")], [eq_sub("R", "B")]),
        plain(" = "), math_frac([eq_sub("U", "S")], [eq_sub("R", "S")])
    ]))
    out.append(spacer(300))
    out.append(equation([
        eq_sub("U", "S"), plain(" = "),
        math_frac(
            [math_frac([eq_sub("U", "iA")], [eq_sub("R", "A")]), plain(" + "), math_frac([eq_sub("U", "iB")], [eq_sub("R", "B")])],
            [math_frac([plain("1")], [eq_sub("R", "A")]), plain(" + "), math_frac([plain("1")], [eq_sub("R", "B")]), plain(" + "), math_frac([plain("1")], [eq_sub("R", "S")])]
        ),
        plain(f" = {decimal_cz(calc['us'])} V")
    ], after=160, line=900))
    out.append(spacer(560))

    out.append(paragraph("Proudy jednotlivými větvemi a zátěží:", align="left", keep_next=True))
    out.append(equation([
        eq_sub("I", "A"), plain(" = "), math_frac([eq_sub("U", "iA"), plain(" − "), eq_sub("U", "S")], [eq_sub("R", "A")]),
        plain(" = "), math_frac([plain(f"7,500 − {decimal_cz(calc['us'])}")], [plain(decimal_cz_n(calc['ra'], 6))]),
        plain(f" = {decimal_cz(calc['ia'])} A")
    ]))
    out.append(equation([
        eq_sub("I", "B"), plain(" = "), math_frac([eq_sub("U", "iB"), plain(" − "), eq_sub("U", "S")], [eq_sub("R", "B")]),
        plain(" = "), math_frac([plain(f"12,500 − {decimal_cz(calc['us'])}")], [plain(decimal_cz_n(calc['rb'], 6))]),
        plain(f" = {decimal_cz(calc['ib'])} A")
    ]))
    out.append(equation([
        eq_sub("I", "S"), plain(" = "), math_frac([eq_sub("U", "S")], [eq_sub("R", "S")]),
        plain(" = "), math_frac([plain(decimal_cz(calc['us']))], [plain("0,033")]),
        plain(f" = {decimal_cz(calc['is'])} A")
    ]))

    out.append(paragraph("Výkon na zátěži:", align="left", keep_next=True))
    out.append(equation([
        eq_sub("P", "S"), plain(" = "), eq_sub("U", "S"), plain("·"), eq_sub("I", "S"),
        plain(f" = {decimal_cz(calc['us'])}·{decimal_cz(calc['is'])} = {decimal_cz(calc['ps'])} W")
    ]))

    out.append(paragraph(
        "Ztráty ve větvích zahrnují vždy součet ztrát na vnitřním odporu zdroje a na odporu "
        "příslušného vodiče:",
        first_line=420,
        keep_next=True,
    ))
    out.append(equation([
        plain("Δ"), eq_sub("P", "A"), plain(" = "), math_sup(eq_sub("I", "A"), "2"), plain("·"), eq_sub("R", "A"),
        plain(" = "), math_sup(decimal_cz(calc['ia']), "2"), plain(f"·{decimal_cz_n(calc['ra'], 6)} = {decimal_cz(calc['dpa'])} W")
    ]))
    out.append(equation([
        plain("Δ"), eq_sub("P", "B"), plain(" = "), math_sup(eq_sub("I", "B"), "2"), plain("·"), eq_sub("R", "B"),
        plain(" = "), math_sup(decimal_cz(calc['ib']), "2"), plain(f"·{decimal_cz_n(calc['rb'], 6)} = {decimal_cz(calc['dpb'])} W")
    ]))
    out.append(equation([
        plain("ΔP = Δ"), eq_sub("P", "A"), plain(" + Δ"), eq_sub("P", "B"),
        plain(f" = {decimal_cz(calc['dpa'])} + {decimal_cz(calc['dpb'])} = {decimal_cz(calc['dp'])} W")
    ]))

    out.append(paragraph("Účinnost přenosu výkonu:", align="left", keep_next=True))
    out.append(equation([
        italic("η"), plain(" = "),
        math_frac([eq_sub("P", "S")], [eq_sub("P", "S"), plain(" + ΔP")]),
        plain("·100 % = "),
        math_frac([plain(decimal_cz(calc['ps']))], [plain(f"{decimal_cz(calc['ps'])} + {decimal_cz(calc['dp'])}")]),
        plain(f"·100 % = {decimal_cz(calc['eta'])} %")
    ]))

    out.append(paragraph(
        f"Kontrolní vstupní výkon zdrojů je {decimal_cz(calc['pin'])} W. Součet výkonu zátěže "
        f"a ztrát je {decimal_cz(calc['ps'] + calc['dp'])} W; rozdíl {decimal_cz(calc['balance'])} W "
        "vzniká výhradně schváleným průběžným zaokrouhlováním mezivýsledků.",
        first_line=420,
    ))

    out.append(heading("ZHODNOCENÍ:"))
    out.append(paragraph(
        f"Výpočtem bylo stanoveno napětí na zátěži Uₛ = {decimal_cz(calc['us'])} V, které je výrazně "
        "nižší než její jmenovité napětí 12 V. Příčinou je velmi malý odpor zátěže a s ním spojené "
        "velké proudy, které vyvolávají značné úbytky napětí na vnitřních odporech zdrojů a na "
        "odporech přívodních vodičů.",
        first_line=420,
    ))
    out.append(paragraph(
        f"Zdroj B dodává proud Iᵦ = {decimal_cz(calc['ib'])} A, zatímco zdroj A dodává pouze "
        f"Iₐ = {decimal_cz(calc['ia'])} A. Zdroj B se tedy na napájení zátěže podílí podstatně více, "
        "protože má vyšší vnitřní napětí a zároveň nižší výsledný odpor větve. Tomu odpovídá také "
        f"dominantní ztráta ve větvi B, která činí {decimal_cz(calc['dpb'])} W.",
        first_line=420,
    ))
    out.append(paragraph(
        f"Na zátěži se přenáší výkon Pₛ = {decimal_cz(calc['ps'])} W, zatímco celkové ztráty dosahují "
        f"ΔP = {decimal_cz(calc['dp'])} W. Výsledná účinnost přenosu je pouze η = {decimal_cz(calc['eta'])} %. "
        "Výpočet ukazuje, že u nízkoohmové zátěže mají i odpory v řádu desítek miliohmů zásadní vliv "
        "na provozní napětí, ztrátový výkon a účinnost. Uvedené závěry vycházejí z teoretického modelu; "
        "obvod nebyl v rámci tohoto projektu experimentálně měřen.",
        first_line=420,
    ))
    return out


def modify_title_table(table: ET.Element) -> None:
    rows = table.findall(q("w", "tr"))
    # Název měření
    title_cell = rows[1].findall(q("w", "tc"))[0]
    title_intro = paragraph(align="left", after=0, line=220)
    add_run(title_intro, " Název měření:", size=24)
    title_value = paragraph(align="center", after=0, line=220)
    add_run(title_value, "SEMESTRÁLNÍ PROJEKT ZELE 1Z", size=24, bold=True)
    set_cell_content(title_cell, [title_intro, title_value, paragraph(align="left", after=0, line=180)])

    number_cell = rows[2].findall(q("w", "tc"))[1]
    set_cell_content(number_cell, [title_label_value("Číslo měření: ", "1Z", centered=True)])

    subject_cell = rows[3].findall(q("w", "tc"))[0]
    subject_label = paragraph(align="left", after=0, line=215)
    add_run(subject_label, " Zkoušené předměty:", size=24)
    subject_value = paragraph(align="center", after=0, line=215)
    add_run(subject_value, "Stejnosměrná zátěž napájená ze dvou reálných zdrojů", size=22, bold=True)
    set_cell_content(subject_cell, [subject_label, subject_value])

    scheme_cell = rows[6].findall(q("w", "tc"))[0]
    scheme_heading = paragraph(align="left", after=0, line=220, keep_next=True)
    add_run(scheme_heading, " Schéma:", size=24, bold=True)
    scheme_children = [
        scheme_heading,
        drawing_paragraph("rId11", "Hlavní schéma", 6.15, 3.35),
        title_values_paragraph([("U", "iA", "7,5 V"), ("R", "iA", "73 mΩ"), ("l", "A", "0,82 m"), ("S", "A", "6 mm²")]),
        title_values_paragraph([("U", "iB", "12,5 V"), ("R", "iB", "54 mΩ"), ("l", "B", "2 m"), ("S", "B", "7,3 mm²")]),
        title_values_paragraph([("U", "n", "12 V"), ("R", "S", "33 mΩ"), ("ρ", "Cu", "17,8·10⁻⁹ Ω·m")]),
    ]
    set_cell_content(scheme_cell, scheme_children)


def add_relationship(rels_root: ET.Element, rel_id: str, target: str) -> None:
    ET.SubElement(
        rels_root,
        q("pr", "Relationship"),
        {
            "Id": rel_id,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            "Target": target,
        },
    )


def build_docx(calc: dict[str, Decimal]) -> None:
    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        document_root = ET.fromstring(zin.read("word/document.xml"))
        document_root.attrib.pop(q("mc", "Ignorable"), None)
        body = document_root.find(q("w", "body"))
        if body is None:
            raise RuntimeError("Šablona neobsahuje w:body")
        title_table = body.find(q("w", "tbl"))
        if title_table is None:
            raise RuntimeError("Šablona neobsahuje titulní tabulku")
        modify_title_table(title_table)

        sect_pr = deepcopy(body.find(q("w", "sectPr")))
        for child in list(body)[1:]:
            body.remove(child)
        for child in build_body(calc):
            body.append(child)
        if sect_pr is not None:
            body.append(sect_pr)

        # LibreOffice 7.3 odmítá vztahy tohoto staršího DOCX, pokud se celý
        # soubor document.xml.rels znovu serializuje s prefixem jmenného
        # prostoru. Proto zachováme původní serializaci a pouze vložíme dvě
        # standardní položky do jeho výchozího namespace.
        rels_xml = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        new_rels = (
            '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/image" Target="media/hlavni_schema.png"/>'
            '<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/image" Target="media/nahradni_schema.png"/>'
        )
        rels_xml = rels_xml.replace("</Relationships>", new_rels + "</Relationships>")

        core_xml = zin.read("docProps/core.xml").decode("utf-8")
        core_xml = re.sub(
            r"<dc:title>.*?</dc:title>",
            "<dc:title>Semestrální projekt ZELE 1Z</dc:title>",
            core_xml,
            flags=re.DOTALL,
        )
        core_xml = re.sub(
            r"<dc:subject>.*?</dc:subject>",
            "<dc:subject>Stejnosměrná zátěž napájená ze dvou reálných zdrojů</dc:subject>",
            core_xml,
            flags=re.DOTALL,
        )

        replacements = {
            "word/document.xml": ET.tostring(document_root, encoding="utf-8", xml_declaration=True),
            "word/_rels/document.xml.rels": rels_xml.encode("utf-8"),
            "docProps/core.xml": core_xml.encode("utf-8"),
        }
        with tempfile.NamedTemporaryFile(dir=OUTPUT, suffix=".docx", delete=False) as tmp:
            temp_path = Path(tmp.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = replacements.get(item.filename, zin.read(item.filename))
                    zout.writestr(item, data)
                zout.write(SCHEMES / "hlavni_schema.png", "word/media/hlavni_schema.png")
                zout.write(SCHEMES / "nahradni_schema.png", "word/media/nahradni_schema.png")
            temp_path.replace(DOCX_OUT)
        finally:
            if temp_path.exists():
                temp_path.unlink()


def write_calculation_audit(calc: dict[str, Decimal]) -> None:
    lines = [
        "Kontrolní mezivýsledky – průběžné zaokrouhlování na 3 desetinná místa",
        f"RvA = {decimal_cz(calc['rva_mohm'])} mΩ",
        f"RA = {decimal_cz(calc['ra_mohm'])} mΩ = {decimal_cz_n(calc['ra'], 6)} Ω",
        f"RvB = {decimal_cz(calc['rvb_mohm'])} mΩ",
        f"RB = {decimal_cz(calc['rb_mohm'])} mΩ = {decimal_cz_n(calc['rb'], 6)} Ω",
        f"US = {decimal_cz(calc['us'])} V",
        f"IA = {decimal_cz(calc['ia'])} A",
        f"IB = {decimal_cz(calc['ib'])} A",
        f"IS = {decimal_cz(calc['is'])} A",
        f"PS = {decimal_cz(calc['ps'])} W",
        f"ΔPA = {decimal_cz(calc['dpa'])} W",
        f"ΔPB = {decimal_cz(calc['dpb'])} W",
        f"ΔP = {decimal_cz(calc['dp'])} W",
        f"η = {decimal_cz(calc['eta'])} %",
        f"Příkon zdrojů = {decimal_cz(calc['pin'])} W",
        f"Bilanční rozdíl po průběžném zaokrouhlení = {decimal_cz(calc['balance'])} W",
    ]
    (WORK / "kontrola_vypoctu.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    SCHEMES.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    calc = calculations()
    write_svgs()
    draw_main_png(SCHEMES / "hlavni_schema.png")
    draw_equivalent_png(SCHEMES / "nahradni_schema.png")
    build_docx(calc)
    write_calculation_audit(calc)
    print(DOCX_OUT)


if __name__ == "__main__":
    main()
