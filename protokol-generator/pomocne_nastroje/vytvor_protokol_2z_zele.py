#!/usr/bin/env python3
"""Vytvoří schválený teoretický protokol ZELE 2Z z ruční předlohy 1Z."""

from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path
import base64
import math
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "vzory" / "vzor_vypoctovych_sekci.docx"
SOURCE_ASSIGNMENT = ROOT / "Zadání semestrálního projektu ZELE.pdf"
MEASUREMENT = ROOT / "2Z-zele-2"
OUTPUT = MEASUREMENT / "vystup"
GRAPHICS = OUTPUT / "grafika"
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
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(prefix: str, name: str) -> str:
    return f"{{{NS[prefix]}}}{name}"


def w(name: str, attrs: dict[str, str] | None = None) -> ET.Element:
    node = ET.Element(q("w", name))
    for key, value in (attrs or {}).items():
        node.set(q("w", key), value)
    return node


def m(name: str, attrs: dict[str, str] | None = None) -> ET.Element:
    node = ET.Element(q("m", name))
    for key, value in (attrs or {}).items():
        node.set(q("m", key), value)
    return node


def math_r(text: str, *, plain: bool = False, bold: bool = False) -> ET.Element:
    run = m("r")
    mrpr = ET.SubElement(run, q("m", "rPr"))
    if plain:
        ET.SubElement(mrpr, q("m", "sty"), {q("m", "val"): "p"})
    wrpr = ET.SubElement(run, q("w", "rPr"))
    ET.SubElement(
        wrpr,
        q("w", "rFonts"),
        {q("w", "ascii"): "Cambria Math", q("w", "hAnsi"): "Cambria Math"},
    )
    if bold:
        ET.SubElement(wrpr, q("w", "b"))
        ET.SubElement(wrpr, q("w", "bCs"))
    ET.SubElement(wrpr, q("w", "sz"), {q("w", "val"): "22"})
    ET.SubElement(wrpr, q("w", "szCs"), {q("w", "val"): "22"})
    text_node = ET.SubElement(run, q("m", "t"))
    if text.startswith(" ") or text.endswith(" "):
        text_node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    text_node.text = text
    return run


def math_sub(base: str | ET.Element, subscript: str | ET.Element) -> ET.Element:
    node = m("sSub")
    ET.SubElement(node, q("m", "sSubPr"))
    base_node = ET.SubElement(node, q("m", "e"))
    base_node.append(math_r(base) if isinstance(base, str) else base)
    sub_node = ET.SubElement(node, q("m", "sub"))
    sub_node.append(math_r(subscript, plain=True) if isinstance(subscript, str) else subscript)
    return node


def math_sup(base: str | ET.Element, exponent: str | ET.Element) -> ET.Element:
    node = m("sSup")
    ET.SubElement(node, q("m", "sSupPr"))
    base_node = ET.SubElement(node, q("m", "e"))
    base_node.append(math_r(base) if isinstance(base, str) else base)
    sup_node = ET.SubElement(node, q("m", "sup"))
    sup_node.append(math_r(exponent, plain=True) if isinstance(exponent, str) else exponent)
    return node


def math_frac(numerator: list[ET.Element], denominator: list[ET.Element]) -> ET.Element:
    node = m("f")
    ET.SubElement(node, q("m", "fPr"))
    num = ET.SubElement(node, q("m", "num"))
    den = ET.SubElement(node, q("m", "den"))
    for child in numerator:
        num.append(child)
    for child in denominator:
        den.append(child)
    return node


def math_rad(children: list[ET.Element]) -> ET.Element:
    node = m("rad")
    props = ET.SubElement(node, q("m", "radPr"))
    ET.SubElement(props, q("m", "degHide"), {q("m", "val"): "1"})
    ET.SubElement(node, q("m", "deg"))
    content = ET.SubElement(node, q("m", "e"))
    for child in children:
        content.append(child)
    return node


def math_bar(child: ET.Element) -> ET.Element:
    node = m("bar")
    props = ET.SubElement(node, q("m", "barPr"))
    ET.SubElement(props, q("m", "pos"), {q("m", "val"): "top"})
    content = ET.SubElement(node, q("m", "e"))
    content.append(child)
    return node


def math_abs(children: list[ET.Element]) -> ET.Element:
    """Nativní OMML modul s párovými svislými oddělovači."""
    node = m("d")
    props = ET.SubElement(node, q("m", "dPr"))
    ET.SubElement(props, q("m", "begChr"), {q("m", "val"): "|"})
    ET.SubElement(props, q("m", "endChr"), {q("m", "val"): "|"})
    content = ET.SubElement(node, q("m", "e"))
    for child in children:
        content.append(child)
    return node


def variable(base: str, subscript: str | None = None, *, bar: bool = False) -> ET.Element:
    node = math_sub(base, subscript) if subscript is not None else math_r(base)
    return math_bar(node) if bar else node


def add_text_run(paragraph: ET.Element, text: str, *, bold: bool = False, font: str = "Times New Roman", size: int = 24) -> None:
    run = ET.SubElement(paragraph, q("w", "r"))
    rpr = ET.SubElement(run, q("w", "rPr"))
    ET.SubElement(
        rpr,
        q("w", "rFonts"),
        {q("w", "ascii"): font, q("w", "hAnsi"): font, q("w", "cs"): font},
    )
    if bold:
        ET.SubElement(rpr, q("w", "b"))
        ET.SubElement(rpr, q("w", "bCs"))
    ET.SubElement(rpr, q("w", "sz"), {q("w", "val"): str(size)})
    ET.SubElement(rpr, q("w", "szCs"), {q("w", "val"): str(size)})
    text_node = ET.SubElement(run, q("w", "t"))
    if text.startswith(" ") or text.endswith(" "):
        text_node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    text_node.text = text


def clear_after_ppr(paragraph: ET.Element) -> None:
    ppr = paragraph.find(q("w", "pPr"))
    for child in list(paragraph):
        if child is not ppr:
            paragraph.remove(child)


def heading(archetype: ET.Element, text: str) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    add_text_run(paragraph, text, bold=True, font="Arial", size=24)
    return paragraph


def body_text(archetype: ET.Element, text: str, *, keep_next: bool = False) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    ppr = paragraph.find(q("w", "pPr"))
    if ppr is None:
        ppr = ET.Element(q("w", "pPr"))
        paragraph.insert(0, ppr)
    keep = ppr.find(q("w", "keepNext"))
    if keep_next and keep is None:
        ppr.insert(0, w("keepNext"))
    if not keep_next and keep is not None:
        ppr.remove(keep)
    add_text_run(paragraph, "     " + text, size=24)
    return paragraph


def caption(archetype: ET.Element, text: str) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    add_text_run(paragraph, text, size=24)
    return paragraph


def math_paragraph(
    archetype: ET.Element,
    children: list[ET.Element],
    *,
    result: bool = False,
    keep_next: bool = False,
) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    ppr = paragraph.find(q("w", "pPr"))
    if ppr is None:
        ppr = ET.Element(q("w", "pPr"))
        paragraph.insert(0, ppr)
    if keep_next and ppr.find(q("w", "keepNext")) is None:
        ppr.insert(0, w("keepNext"))
    math_para = ET.SubElement(paragraph, q("m", "oMathPara"))
    props = ET.SubElement(math_para, q("m", "oMathParaPr"))
    ET.SubElement(props, q("m", "jc"), {q("m", "val"): "left"})
    omath = ET.SubElement(math_para, q("m", "oMath"))
    if result:
        omath.append(math_r("                                                               ", plain=True, bold=True))
    for child in children:
        if result and child.tag == q("m", "r"):
            # Výsledkové řádky jsou tučné stejně jako v ruční předloze.
            text = child.find(q("m", "t"))
            omath.append(math_r(text.text or "", plain=child.find(f"{q('m','rPr')}/{q('m','sty')}") is not None, bold=True))
        else:
            omath.append(child)
    if result:
        # Výsledky jsou v ruční předloze skutečně tučné i u indexů a zlomků.
        for style in omath.iter(q("m", "sty")):
            style.set(q("m", "val"), "b")
        for run_props in omath.iter(q("w", "rPr")):
            if run_props.find(q("w", "b")) is None:
                run_props.insert(0, w("b"))
            if run_props.find(q("w", "bCs")) is None:
                run_props.insert(1, w("bCs"))
    return paragraph


def borderless_table(rows: list[list[ET.Element]], widths: list[int]) -> ET.Element:
    """Pevná neviditelná tabulka pro stabilní sazbu ve Wordu i LibreOffice."""
    table = w("tbl")
    props = ET.SubElement(table, q("w", "tblPr"))
    ET.SubElement(props, q("w", "tblW"), {q("w", "w"): str(sum(widths)), q("w", "type"): "dxa"})
    ET.SubElement(props, q("w", "tblInd"), {q("w", "w"): "0", q("w", "type"): "dxa"})
    ET.SubElement(props, q("w", "tblLayout"), {q("w", "type"): "fixed"})
    borders = ET.SubElement(props, q("w", "tblBorders"))
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        ET.SubElement(borders, q("w", side), {q("w", "val"): "nil"})
    margins = ET.SubElement(props, q("w", "tblCellMar"))
    for side in ("top", "left", "bottom", "right"):
        ET.SubElement(margins, q("w", side), {q("w", "w"): "0", q("w", "type"): "dxa"})
    grid = ET.SubElement(table, q("w", "tblGrid"))
    for width in widths:
        ET.SubElement(grid, q("w", "gridCol"), {q("w", "w"): str(width)})
    for row_items in rows:
        row = ET.SubElement(table, q("w", "tr"))
        row_props = ET.SubElement(row, q("w", "trPr"))
        ET.SubElement(row_props, q("w", "cantSplit"))
        for index, width in enumerate(widths):
            cell = ET.SubElement(row, q("w", "tc"))
            cell_props = ET.SubElement(cell, q("w", "tcPr"))
            ET.SubElement(cell_props, q("w", "tcW"), {q("w", "w"): str(width), q("w", "type"): "dxa"})
            if index < len(row_items):
                cell.append(row_items[index])
            else:
                cell.append(w("p"))
    return table


def inline_values(archetype: ET.Element, groups: list[list[ET.Element]]) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    for index, group in enumerate(groups):
        if index:
            add_text_run(paragraph, "          ", size=22)
        omath = ET.SubElement(paragraph, q("m", "oMath"))
        for child in group:
            omath.append(child)
    return paragraph


def page_break(archetype: ET.Element) -> ET.Element:
    paragraph = deepcopy(archetype)
    clear_after_ppr(paragraph)
    run = ET.SubElement(paragraph, q("w", "r"))
    ET.SubElement(run, q("w", "br"), {q("w", "type"): "page"})
    return paragraph


def fixed_spacer(height_twips: int) -> ET.Element:
    """Pevná svislá mezera, kterou Word i LibreOffice vykreslí shodně."""
    paragraph = w("p")
    props = ET.SubElement(paragraph, q("w", "pPr"))
    ET.SubElement(
        props,
        q("w", "spacing"),
        {
            q("w", "before"): "0",
            q("w", "after"): "0",
            q("w", "line"): str(height_twips),
            q("w", "lineRule"): "exact",
        },
    )
    run = ET.SubElement(paragraph, q("w", "r"))
    run_props = ET.SubElement(run, q("w", "rPr"))
    ET.SubElement(run_props, q("w", "sz"), {q("w", "val"): "2"})
    ET.SubElement(run_props, q("w", "szCs"), {q("w", "val"): "2"})
    text_node = ET.SubElement(run, q("w", "t"))
    text_node.text = "\u00a0"
    return paragraph


def set_drawing(paragraph: ET.Element, rel_id: str, width_in: float, height_in: float, name: str) -> ET.Element:
    paragraph = deepcopy(paragraph)
    blip = paragraph.find(f".//{q('a', 'blip')}")
    if blip is None:
        raise RuntimeError("Archetyp obrázku neobsahuje a:blip")
    blip.set(q("r", "embed"), rel_id)
    cx = str(round(width_in * 914400))
    cy = str(round(height_in * 914400))
    extent = paragraph.find(f".//{q('wp', 'extent')}")
    xfrm_extent = paragraph.find(f".//{q('a', 'xfrm')}/{q('a', 'ext')}")
    if extent is not None:
        extent.set("cx", cx)
        extent.set("cy", cy)
    if xfrm_extent is not None:
        xfrm_extent.set("cx", cx)
        xfrm_extent.set("cy", cy)
    docpr = paragraph.find(f".//{q('wp', 'docPr')}")
    if docpr is not None:
        docpr.set("name", name)
    return paragraph


def replace_cell_content(cell: ET.Element, paragraphs: list[ET.Element]) -> None:
    tcpr = cell.find(q("w", "tcPr"))
    saved = deepcopy(tcpr) if tcpr is not None else None
    for child in list(cell):
        cell.remove(child)
    if saved is not None:
        cell.append(saved)
    for paragraph in paragraphs:
        cell.append(paragraph)


FONT_REG = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], *, width: int = 6, fill: str = "black") -> None:
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 22 + width
    spread = math.pi / 7
    p1 = (end[0] - length * math.cos(angle - spread), end[1] - length * math.sin(angle - spread))
    p2 = (end[0] - length * math.cos(angle + spread), end[1] - length * math.sin(angle + spread))
    draw.polygon((end, p1, p2), fill=fill)


def draw_main_scheme(png_path: Path, svg_path: Path) -> None:
    # Poměr stran odpovídá prostoru schématu v ručně upravené titulní straně 1Z.
    width, height = 1800, 925
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    wire = 7
    top, bottom = 235, 755
    left, right = 270, 1570
    source_x = 300

    # Zdroj a sběrnice.
    draw.line((left, top, 500, top), fill="black", width=wire)
    draw.line((570, top, right, top), fill="black", width=wire)
    draw.line((left, bottom, right, bottom), fill="black", width=wire)
    draw.line((source_x, top, source_x, 375), fill="black", width=wire)
    draw.ellipse((source_x - 62, 375, source_x + 62, 499), outline="black", width=wire)
    draw.arc((source_x - 35, 405, source_x + 5, 450), 190, 350, fill="black", width=5)
    draw.arc((source_x - 5, 425, source_x + 35, 470), 10, 170, fill="black", width=5)
    draw.line((source_x, 499, source_x, bottom), fill="black", width=wire)

    # Jistič B16.
    draw.line((500, top, 515, top - 55), fill="black", width=wire)
    draw.line((515, top - 55, 565, top - 55), fill="black", width=wire)
    draw.line((565, top - 55, 565, top), fill="black", width=wire)
    draw.text((485, 110), "B16", font=font(FONT_SANS_BOLD, 52), fill="black")
    arrow(draw, (390, 170), (530, 170), width=6)
    draw.text((435, 95), "I", font=font(FONT_ITALIC, 60), fill="black")

    # Tři paralelní spotřebiče.
    xs = (800, 1120, 1440)
    for index, x in enumerate(xs):
        upper, lower = (385, 605) if index == 0 else (410, 560)
        draw.line((x, top, x, upper), fill="black", width=wire)
        draw.line((x, lower, x, bottom), fill="black", width=wire)
        draw.ellipse((x - 10, top - 10, x + 10, top + 10), fill="black")
        draw.ellipse((x - 10, bottom - 10, x + 10, bottom + 10), fill="black")
    draw.rectangle((xs[0] - 45, 385, xs[0] + 45, 605), outline="black", width=wire)
    for x in xs[1:]:
        draw.ellipse((x - 75, 410, x + 75, 560), outline="black", width=wire)
        draw.text((x - 43, 435), "M", font=font(FONT_REG, 70), fill="black")

    draw.text((60, 405), "230 V", font=font(FONT_REG, 54), fill="black")
    arrow(draw, (175, 350), (175, 575), width=5)
    for index, x in enumerate(xs, 1):
        draw.text((x - 112, 805), f"spotřebič {index}", font=font(FONT_REG, 43), fill="black")
    image.save(png_path, dpi=(300, 300))

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="925" viewBox="0 0 1800 925">
<rect width="1800" height="925" fill="white"/>
<image href="data:image/png;base64,{base64.b64encode(png_path.read_bytes()).decode()}" width="1800" height="925"/>
</svg>'''
    svg_path.write_text(svg, encoding="utf-8")


def draw_phasor(png_path: Path, svg_path: Path) -> None:
    width, height = 1600, 1000
    origin = (190, 170)
    scale = 23.62  # 2 mm/A při 300 dpi
    vectors = [
        ("I₁ = 10,000 A", 10.000, 0.000, 4, "#222222"),
        ("I₃ = 41,128 A", 41.128, -42.269, 5, "#555555"),
        ("I = 50,449 A", 50.449, -34.869, 9, "#000000"),
        # Krátký fázor I2 se kreslí poslední, aby jej delší vektory nepřekryly.
        ("I₂ = 1,518 A", 1.518, -50.950, 6, "#555555"),
    ]
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    # Referenční napětí bez osového rozkladu.
    for x in range(origin[0], 1460, 35):
        draw.line((x, origin[1], min(x + 18, 1460), origin[1]), fill="#888888", width=3)
    arrow(draw, origin, (1470, origin[1]), width=3, fill="#777777")
    draw.text((1360, 95), "U = U∠0°", font=font(FONT_ITALIC, 40), fill="#555555")
    draw.ellipse((origin[0] - 8, origin[1] - 8, origin[0] + 8, origin[1] + 8), fill="black")

    endpoints: list[tuple[str, float, float, int, str, tuple[float, float]]] = []
    for label, magnitude, angle_deg, stroke, color in vectors:
        angle_rad = math.radians(angle_deg)
        end = (
            origin[0] + magnitude * scale * math.cos(angle_rad),
            origin[1] - magnitude * scale * math.sin(angle_rad),
        )
        arrow(draw, origin, end, width=stroke, fill=color)
        endpoints.append((label, magnitude, angle_deg, stroke, color, end))

    # Popisy se umísťují ručně, aby se nepřekrývaly.
    label_positions = ((410, 105), (830, 850), (1180, 690), (285, 270))
    for item, pos in zip(endpoints, label_positions):
        draw.text(pos, item[0], font=font(FONT_ITALIC, 40 if item[0].startswith("I =") else 36), fill=item[4])
    i2_end = endpoints[-1][-1]
    draw.line((i2_end[0] + 5, i2_end[1] + 4, 285, 264), fill="#555555", width=2)
    draw.text((1120, 900), "měřítko: 2 mm ≙ 1 A", font=font(FONT_REG, 32), fill="black")
    image.save(png_path, dpi=(300, 300))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">',
        '<defs><marker id="arr" markerWidth="14" markerHeight="14" refX="12" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="context-stroke"/></marker></defs>',
        '<rect width="1600" height="1000" fill="white"/>',
        f'<line x1="{origin[0]}" y1="{origin[1]}" x2="1470" y2="{origin[1]}" stroke="#777" stroke-width="3" stroke-dasharray="18 17" marker-end="url(#arr)"/>',
        '<text x="1360" y="120" font-family="Times New Roman,serif" font-size="40" font-style="italic">U = U∠0°</text>',
    ]
    for label, magnitude, angle_deg, stroke, color, end in endpoints:
        lines.append(f'<line x1="{origin[0]}" y1="{origin[1]}" x2="{end[0]:.2f}" y2="{end[1]:.2f}" stroke="{color}" stroke-width="{stroke}" marker-end="url(#arr)"/>')
    for item, pos in zip(endpoints, label_positions):
        lines.append(f'<text x="{pos[0]}" y="{pos[1]+38}" font-family="Times New Roman,serif" font-size="38" font-style="italic">{item[0]}</text>')
    i2_end = endpoints[-1][-1]
    lines.append(f'<line x1="{i2_end[0]+5:.2f}" y1="{i2_end[1]+4:.2f}" x2="285" y2="264" stroke="#555" stroke-width="2"/>')
    lines.extend(['<text x="1120" y="940" font-family="Times New Roman,serif" font-size="32">měřítko: 2 mm ≙ 1 A</text>', '</svg>'])
    svg_path.write_text("\n".join(lines), encoding="utf-8")


def extract_and_annotate_characteristic(original_path: Path, annotated_path: Path, svg_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "curve"
        subprocess.run(
            ["pdfimages", "-f", "2", "-l", "2", "-png", str(SOURCE_ASSIGNMENT), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        candidates = list(Path(tmp).glob("curve-*.png"))
        if not candidates:
            raise RuntimeError("Z PDF se nepodařilo získat vypínací charakteristiku")
        largest = max(candidates, key=lambda path: Image.open(path).width * Image.open(path).height)
        image = Image.open(largest).convert("RGB")
        image.save(original_path)

    factor = 3
    resampling = getattr(Image, "Resampling", Image)
    image = image.resize((image.width * factor, image.height * factor), resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    # Lokální kalibrace logaritmické osy mezi skutečnými mřížkovými
    # čarami 3 a 4. Globální interpolace mezi 1 a 30 posouvala hodnotu
    # 3,153 přibližně do polohy 3,3 a chybně ji vedla přes magnetickou
    # část pásma B.
    x_tick_3, x_tick_4 = 254 * factor, 303 * factor
    y_for_one = 414 * factor
    y_scale = 99.5 * factor
    ratio = 3.153
    x = x_tick_3 + math.log10(ratio / 3) / math.log10(4 / 3) * (x_tick_4 - x_tick_3)
    # V opravené poloze protíná svislice pouze tepelné toleranční
    # pásmo: dolní hranici přibližně v 6 s a horní v 21 s.
    t_min, t_max = 6.0, 21.0
    y_max = y_for_one - y_scale * math.log10(t_max)
    y_min = y_for_one - y_scale * math.log10(t_min)
    dash = 24
    gap = 16
    line_width = 7

    def dashed_line(start: tuple[float, float], end: tuple[float, float]) -> None:
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        offset = 0.0
        while offset < length:
            stop = min(offset + dash, length)
            draw.line(
                (
                    start[0] + ux * offset,
                    start[1] + uy * offset,
                    start[0] + ux * stop,
                    start[1] + uy * stop,
                ),
                fill="black",
                width=line_width,
            )
            offset += dash + gap

    dashed_line((x, 5 * factor), (x, 749 * factor))
    dashed_line((85 * factor, y_max), (x, y_max))
    dashed_line((85 * factor, y_min), (x, y_min))
    radius = 14
    for y in (y_max, y_min):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white", outline="black", width=7)
    label_font = font(FONT_SANS_BOLD, 34)
    draw.rectangle((x + 20, 30, x + 175, 90), fill="white")
    draw.text((x + 30, 35), "3,153", font=label_font, fill="black")
    image.save(annotated_path, dpi=(300, 300))

    encoded = base64.b64encode(original_path.read_bytes()).decode()
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1971" height="2454" viewBox="0 0 1971 2454">
<rect width="1971" height="2454" fill="white"/>
<image href="data:image/png;base64,{encoded}" width="1971" height="2454" image-rendering="auto"/>
<g fill="none" stroke="black" stroke-width="7" stroke-dasharray="24 16">
  <line x1="{x:.1f}" y1="15" x2="{x:.1f}" y2="2247"/>
  <line x1="255" y1="{y_max:.1f}" x2="{x:.1f}" y2="{y_max:.1f}"/>
  <line x1="255" y1="{y_min:.1f}" x2="{x:.1f}" y2="{y_min:.1f}"/>
</g>
<circle cx="{x:.1f}" cy="{y_max:.1f}" r="14" fill="white" stroke="black" stroke-width="7"/>
<circle cx="{x:.1f}" cy="{y_min:.1f}" r="14" fill="white" stroke="black" stroke-width="7"/>
<rect x="{x+20:.1f}" y="30" width="155" height="60" fill="white"/>
<text x="{x+30:.1f}" y="72" font-family="Arial,sans-serif" font-size="34" font-weight="bold">3,153</text>
</svg>''',
        encoding="utf-8",
    )


def make_assets() -> None:
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    draw_main_scheme(GRAPHICS / "principialni_schema.png", GRAPHICS / "principialni_schema.svg")
    draw_phasor(GRAPHICS / "fazorovy_diagram.png", GRAPHICS / "fazorovy_diagram.svg")
    extract_and_annotate_characteristic(
        GRAPHICS / "vypinaci_charakteristika_original.png",
        GRAPHICS / "vypinaci_charakteristika_anotovana.png",
        GRAPHICS / "vypinaci_charakteristika_anotovana.svg",
    )


def gap() -> ET.Element:
    return math_r("                                  ", plain=True)


def result_text(text: str) -> list[ET.Element]:
    return [math_r(text, plain=True, bold=True)]


def build_body(body: ET.Element) -> list[ET.Element]:
    children = list(body)
    h = children[1]
    text = children[54]
    subheading = children[5]
    caption_arch = children[16]
    eq_arch = children[17]
    result_arch = children[20]
    image_arch = children[13]
    break_arch = children[14]

    out: list[ET.Element] = []
    out.append(heading(h, "ZADÁNÍ:"))
    out.append(body_text(text, "Střídavý rozvod je napájen zdrojem konstantního střídavého napětí 230 V o frekvenci 50 Hz. Jedná se o idealizovaný případ zásuvkového rozvodu v obytné budově."))
    out.append(body_text(text, "Rozvod je jištěn jističem se jmenovitým proudem 16 A a vypínací charakteristikou B. K rozvodu jsou paralelně připojeny tři spotřebiče se zadanými činnými výkony a účiníky."))
    out.append(body_text(text, "Úkolem je vypočítat proud protékající jističem, zjistit, zda jistič vypne, a v případě vypnutí určit z dodané charakteristiky minimální a maximální vypínací čas."))
    out.append(heading(subheading, "Zadané hodnoty:"))
    out.append(inline_values(children[6], [
        [variable("U"), math_r(" = 230 V", plain=True)],
        [variable("f"), math_r(" = 50 Hz", plain=True)],
        [variable("I", "n"), math_r(" = 16 A", plain=True)],
        [math_r("char. B", plain=True)],
    ]))
    out.append(inline_values(children[7], [
        [variable("U", "n1"), math_r(" = 230 V", plain=True)],
        [variable("P", "1"), math_r(" = 2300 W", plain=True)],
        [math_r("cos", plain=True), variable("φ", "1"), math_r(" = 1", plain=True)],
    ]))
    out.append(inline_values(children[8], [
        [variable("U", "n2"), math_r(" = 230 V", plain=True)],
        [variable("P", "2"), math_r(" = 220 W", plain=True)],
        [math_r("cos", plain=True), variable("φ", "2"), math_r(" = 0,63", plain=True)],
    ]))
    out.append(inline_values(children[9], [
        [variable("U", "n3"), math_r(" = 230 V", plain=True)],
        [variable("P", "3"), math_r(" = 7000 W", plain=True)],
        [math_r("cos", plain=True), variable("φ", "3"), math_r(" = 0,74", plain=True)],
    ]))
    out.append(heading(h, "NÁHRADNÍ SCHÉMA:"))
    out.append(body_text(text, "Všechny tři spotřebiče jsou paralelně připojeny k ideálnímu zdroji napětí. Spotřebič 1 má jednotkový účiník. Spotřebiče 2 a 3 jsou induktivní zátěže, a proto se celkový proud musí určit fázorovým součtem.", keep_next=True))
    out.append(set_drawing(image_arch, "rId8", 5.8, 2.98, "Principiální schéma"))
    out.append(page_break(break_arch))

    out.append(heading(children[15], "VÝPOČTY:"))
    out.append(body_text(text, "Při výpočtu proudu jednotlivých spotřebičů se vychází ze vztahu pro činný výkon střídavého jednofázového spotřebiče:", keep_next=True))
    out.append(math_paragraph(eq_arch, [variable("P"), math_r(" = "), variable("U"), math_r("·"), variable("I"), math_r("·", plain=True), math_r("cos", plain=True), variable("φ")]))
    out.append(body_text(text, "Z tohoto vztahu se vyjádří proud:", keep_next=True))
    out.append(math_paragraph(eq_arch, [variable("I"), math_r(" = "), math_frac([variable("P")], [variable("U"), math_r("·"), math_r("cos", plain=True), variable("φ")])]))
    out.append(body_text(text, "Napětí se zvolí jako referenční fázor. Induktivní proudy zaostávají za napětím a mají záporný fázový úhel i zápornou imaginární část. Každý zobrazený mezivýsledek se zaokrouhlí na tři desetinná místa a použije v následujícím kroku.", keep_next=True))
    out.append(math_paragraph(eq_arch, [variable("U", bar=True), math_r(" = 230∠0° V", plain=True)]))

    def add_load(index: str, power: str, pf: str, current: str, angle: str, real: str, imag: str) -> None:
        out.append(caption(caption_arch, f"Spotřebič {index}:"))
        sign = "+" if imag.startswith("0") else "−"
        # Stejný princip jako v ruční předloze: obecný vztah a dosazení
        # jsou v jediném OMML odstavci. Word 2016 tak zachová kompaktní
        # vertikální rytmus i polohu pravého sloupce.
        out.append(math_paragraph(eq_arch, [
            variable("I", index), math_r(" = "),
            math_frac([variable("P", index)], [variable("U"), math_r("·"), math_r("cos", plain=True), variable("φ", index)]),
            gap(),
            variable("I", index), math_r(" = "),
            math_frac([math_r(power, plain=True)], [math_r(f"230·{pf}", plain=True)]),
        ], keep_next=True))
        out.append(math_paragraph(result_arch, [variable("I", index), math_r(f" = {current} A", plain=True)], result=True))

        out.append(math_paragraph(eq_arch, [
            variable("φ", index), math_r(" = "), math_r("arccos", plain=True), math_r("("),
            math_r("cos", plain=True), variable("φ", index), math_r(")"),
            gap(),
            variable("φ", index), math_r(" = "), math_r("arccos", plain=True), math_r(f"({pf})", plain=True),
        ], keep_next=True))
        out.append(math_paragraph(result_arch, [variable("φ", index), math_r(f" = {angle}°", plain=True)], result=True))

        out.append(math_paragraph(eq_arch, [
            variable("I", index, bar=True), math_r(" = "), variable("I", index), math_r("("),
            math_r("cos", plain=True), variable("φ", index), math_r(" − j·", plain=True),
            math_r("sin", plain=True), variable("φ", index), math_r(")"),
        ]))
        out.append(math_paragraph(eq_arch, [
            variable("I", index, bar=True), math_r(f" = {current}(cos {angle}° − j·sin {angle}°)", plain=True),
        ], keep_next=True))
        out.append(math_paragraph(result_arch, [
            variable("I", index, bar=True), math_r(f" = {real} {sign} j{imag} A", plain=True),
        ], result=True))

    add_load("1", "2300", "1", "10,000", "0,000", "10,000", "0,000")
    add_load("2", "220", "0,63", "1,518", "50,950", "0,956", "1,179")
    add_load("3", "7000", "0,74", "41,128", "42,269", "30,435", "27,663")

    out.append(caption(caption_arch, "Celkový proud jističem:"))
    out.append(math_paragraph(eq_arch, [variable("I", bar=True), math_r(" = "), variable("I", "1", bar=True), math_r(" + "), variable("I", "2", bar=True), math_r(" + "), variable("I", "3", bar=True)]))
    out.append(math_paragraph(eq_arch, [variable("I", bar=True), math_r(" = (10,000 + j0,000) + (0,956 − j1,179) + (30,435 − j27,663)", plain=True)], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("I", bar=True), math_r(" = 41,391 − j28,842 A", plain=True)], result=True))
    out.append(math_paragraph(eq_arch, [
        variable("I"), math_r(" = "), math_abs([variable("I", bar=True)]),
        gap(),
        variable("I"), math_r(" = "),
        math_rad([math_sup(math_r("41,391", plain=True), "2"), math_r(" + "), math_sup(math_r("(−28,842)", plain=True), "2")]),
    ], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("I"), math_r(" = 50,449 A", plain=True)], result=True))
    out.append(math_paragraph(eq_arch, [
        variable("φ", "I"), math_r(" = "), math_r("atan2", plain=True), math_r("(Im "),
        variable("I", bar=True), math_r("; Re "), variable("I", bar=True), math_r(")"),
        gap(),
        variable("φ", "I"), math_r(" = atan2(−28,842; 41,391)", plain=True),
    ], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("φ", "I"), math_r(" = −34,869°", plain=True)], result=True))
    out.append(math_paragraph(result_arch, [variable("I", bar=True), math_r(" = 50,449∠−34,869° A", plain=True)], result=True))

    out.append(caption(caption_arch, "Fázorový diagram proudů:"))
    out.append(body_text(text, "Proudy I₁, I₂, I₃ a jejich výslednice I jsou zakresleny od společného počátku vůči referenčnímu napětí. Diagram nepoužívá samostatně označené osové složky.", keep_next=True))
    out.append(set_drawing(image_arch, "rId11", 6.1, 3.81, "Fázorový diagram proudů"))

    out.append(caption(caption_arch, "Posouzení jističe:"))
    out.append(math_paragraph(eq_arch, [
        variable("I"), math_r(" = 50,449 A", plain=True),
        gap(),
        variable("I", "n"), math_r(" = 16 A", plain=True),
    ]))
    out.append(math_paragraph(eq_arch, [
        math_frac([variable("I")], [variable("I", "n")]),
        gap(),
        math_frac([variable("I")], [variable("I", "n")]), math_r(" = "),
        math_frac([math_r("50,449", plain=True)], [math_r("16", plain=True)]),
    ], keep_next=True))
    out.append(math_paragraph(result_arch, [
        math_frac([variable("I")], [variable("I", "n")]), math_r(" = 3,153", plain=True),
    ], result=True))
    out.append(body_text(text, "Proud jističem je 3,153násobkem jeho jmenovitého proudu. Jistič B16 proto vypne."))

    out.append(page_break(break_arch))
    out.append(heading(h, "VYPÍNACÍ CHARAKTERISTIKA JISTIČE:"))
    out.append(caption(caption_arch, "Velikost nadproudu: 3,153"))
    out.append(inline_values(result_arch, [
        [variable("t", "min"), math_r(" ≈ 6 s", plain=True)],
        [variable("t", "max"), math_r(" ≈ 21 s", plain=True)],
    ]))
    out.append(body_text(text, "Časy jsou přibližně odečteny z tolerančního pásma charakteristiky B pro velikost nadproudu 3,153.", keep_next=True))
    out.append(set_drawing(image_arch, "rId12", 6.0, 7.47, "Anotovaná vypínací charakteristika"))

    out.append(page_break(break_arch))
    out.append(heading(h, "ZHODNOCENÍ:"))
    out.append(body_text(text, "Výpočtem byly stanoveny proudy jednotlivých spotřebičů. Spotřebičem 1 protéká proud 10,000 A, spotřebičem 2 proud 1,518 A a spotřebičem 3 proud 41,128 A. Protože mají spotřebiče rozdílné účiníky a fázové posuny, nebyly velikosti proudů aritmeticky sečteny."))
    out.append(body_text(text, "Jednotlivé proudy byly převedeny na komplexní fázory. Jejich součtem byl získán výsledný proud 41,391 − j28,842 A, tedy 50,449∠−34,869° A. Jmenovitý proud jističe je 16 A, takže vypočtený proud představuje 3,153násobek jeho jmenovité hodnoty."))
    out.append(body_text(text, "Jistič s charakteristikou B při tomto zatížení vypne. Z dodané vypínací charakteristiky byl odečten minimální čas přibližně 6 s a maximální čas přibližně 21 s. Při nadproudu 3,153 prochází konstrukční svislice tepelnou částí tolerančního pásma B, nikoli jeho okamžitou elektromagnetickou oblastí."))
    out.append(body_text(text, "Výpočet popisuje ustálený teoretický stav při konstantním napětí 230 V. Neuvažuje úbytky napětí na vedení ani rozběhové proudy motorů, protože tyto hodnoty nebyly zadány. Skutečný okamžik vypnutí by dále ovlivnila počáteční teplota jističe, výrobní tolerance a předchozí zatížení."))
    return out


def modify_title(table: ET.Element, body_children: list[ET.Element]) -> None:
    rows = table.findall(q("w", "tr"))
    for node in table.findall(f".//{q('w', 't')}"):
        if node.text == "SEMESTRÁLNÍ PROJEKT ZELE 1Z":
            node.text = "SEMESTRÁLNÍ PROJEKT ZELE 2Z"
        elif node.text == "1Z":
            node.text = "2Z"
        elif node.text == "Stejnosměrná zátěž napájená ze dvou reálných zdrojů":
            node.text = "Střídavý rozvod jištěný jističem"

    scheme_cell = rows[6].findall(q("w", "tc"))[0]
    existing_paragraphs = scheme_cell.findall(q("w", "p"))
    heading_p = deepcopy(existing_paragraphs[0])
    drawing_source = next(
        paragraph
        for paragraph in existing_paragraphs
        if paragraph.find(f".//{q('w', 'drawing')}") is not None
    )
    drawing_p = set_drawing(drawing_source, "rId7", 6.50, 3.34, "Principiální schéma")
    value_arch = body_children[6]
    def value_cell(children: list[ET.Element], *, before: int = 0) -> ET.Element:
        paragraph = inline_values(value_arch, [children])
        if before:
            props = paragraph.find(q("w", "pPr"))
            if props is None:
                props = ET.Element(q("w", "pPr"))
                paragraph.insert(0, props)
            spacing = props.find(q("w", "spacing"))
            if spacing is None:
                spacing = ET.SubElement(props, q("w", "spacing"))
            spacing.set(q("w", "before"), str(before))
        return paragraph

    values_table = borderless_table([
        [
            value_cell([variable("U"), math_r(" = 230 V", plain=True)], before=2500),
            value_cell([variable("f"), math_r(" = 50 Hz", plain=True)], before=2500),
            value_cell([variable("I", "n"), math_r(" = 16 A", plain=True)], before=2500),
            value_cell([math_r("char. B", plain=True)], before=2500),
        ],
        [
            value_cell([variable("P", "1"), math_r(" = 2300 W", plain=True)]),
            value_cell([math_r("cos", plain=True), variable("φ", "1"), math_r(" = 1", plain=True)]),
            value_cell([variable("P", "2"), math_r(" = 220 W", plain=True)]),
            value_cell([math_r("cos", plain=True), variable("φ", "2"), math_r(" = 0,63", plain=True)]),
        ],
        [
            value_cell([variable("P", "3"), math_r(" = 7000 W", plain=True)]),
            value_cell([math_r("cos", plain=True), variable("φ", "3"), math_r(" = 0,74", plain=True)]),
            w("p"),
            w("p"),
        ],
    ], [2500, 2700, 2400, 2849])
    trailing = w("p")
    trailing_props = ET.SubElement(trailing, q("w", "pPr"))
    ET.SubElement(trailing_props, q("w", "spacing"), {q("w", "before"): "0", q("w", "after"): "0", q("w", "line"): "1", q("w", "lineRule"): "exact"})
    replace_cell_content(
        scheme_cell,
        [heading_p, fixed_spacer(400), drawing_p, values_table, trailing],
    )


def build_docx() -> None:
    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        document_bytes = zin.read("word/document.xml")
        root = ET.fromstring(document_bytes)
        root.attrib.pop(q("mc", "Ignorable"), None)
        body = root.find(q("w", "body"))
        if body is None:
            raise RuntimeError("Předloha neobsahuje w:body")
        original_children = list(body)
        title_table = original_children[0]
        modify_title(title_table, original_children)
        section = deepcopy(original_children[-1])
        new_body = build_body(body)
        for child in list(body)[1:]:
            body.remove(child)
        for child in new_body:
            body.append(child)
        body.append(section)

        rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        extra = (
            '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image3.png"/>'
            '<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image4.png"/>'
        )
        rels = rels.replace("</Relationships>", extra + "</Relationships>")

        core = zin.read("docProps/core.xml").decode("utf-8")
        core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Semestrální projekt ZELE 2Z</dc:title>", core, flags=re.DOTALL)
        core = re.sub(r"<dc:subject>.*?</dc:subject>", "<dc:subject>Střídavý rozvod jištěný jističem</dc:subject>", core, flags=re.DOTALL)

        replacements = {
            "word/document.xml": ET.tostring(root, encoding="utf-8", xml_declaration=True),
            "word/_rels/document.xml.rels": rels.encode("utf-8"),
            "docProps/core.xml": core.encode("utf-8"),
            "word/media/image1.png": (GRAPHICS / "principialni_schema.png").read_bytes(),
            "word/media/image2.png": (GRAPHICS / "principialni_schema.png").read_bytes(),
        }
        with tempfile.NamedTemporaryFile(dir=OUTPUT, suffix=".docx", delete=False) as temp:
            temp_path = Path(temp.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    zout.writestr(item, replacements.get(item.filename, zin.read(item.filename)))
                zout.write(GRAPHICS / "fazorovy_diagram.png", "word/media/image3.png")
                zout.write(GRAPHICS / "vypinaci_charakteristika_anotovana.png", "word/media/image4.png")
            temp_path.replace(DOCX_OUT)
            DOCX_OUT.chmod(0o664)
        finally:
            if temp_path.exists():
                temp_path.unlink()


def write_audit() -> None:
    audit = """Kontrola výpočtu ZELE 2Z
I1 = 10,000 A; φ1 = 0,000°; Ī1 = 10,000 + j0,000 A
I2 = 1,518 A; φ2 = 50,950°; Ī2 = 0,956 − j1,179 A
I3 = 41,128 A; φ3 = 42,269°; Ī3 = 30,435 − j27,663 A
Ī = 41,391 − j28,842 A
I = 50,449 A; φI = −34,869°
I/In = 3,153
tmin ≈ 6 s; tmax ≈ 21 s
"""
    (WORK / "kontrola_vypoctu.txt").write_text(audit, encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    make_assets()
    build_docx()
    write_audit()
    print(DOCX_OUT)


if __name__ == "__main__":
    main()
