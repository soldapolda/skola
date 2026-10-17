#!/usr/bin/env python3
"""Vytvoří schválený teoretický protokol ZELE 4Z z ruční předlohy."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import math
from pathlib import Path
import re
import tempfile
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "pomocne_nastroje" / "vytvor_protokol_2z_zele.py"
spec = importlib.util.spec_from_file_location("zele2_base", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Nelze načíst pomocné funkce protokolu 2Z")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

GRAPH_HELPER_PATH = ROOT / "pomocne_nastroje" / "vytvor_graf_4z_zele.py"
graph_spec = importlib.util.spec_from_file_location("zele4_graph", GRAPH_HELPER_PATH)
if graph_spec is None or graph_spec.loader is None:
    raise RuntimeError("Nelze načíst generátor grafu 4Z")
graph_helper = importlib.util.module_from_spec(graph_spec)
graph_spec.loader.exec_module(graph_helper)

TEMPLATE = ROOT / "vzory" / "vzor_vypoctovych_sekci.docx"
MEASUREMENT = ROOT / "4Z-zele-4"
OUTPUT = MEASUREMENT / "vystup"
GRAPHICS = OUTPUT / "grafika"
WORK = MEASUREMENT / "pracovni"
DOCX_OUT = OUTPUT / "protokol.docx"
XLSX_OUT = OUTPUT / "graf_P_f.xlsx"

q = base.q
w = base.w
math_r = base.math_r
math_sup = base.math_sup
math_frac = base.math_frac
math_rad = base.math_rad
variable = base.variable
heading = base.heading
body_text = base.body_text
caption = base.caption
math_paragraph = base.math_paragraph
inline_values = base.inline_values
page_break = base.page_break
fixed_spacer = base.fixed_spacer
set_drawing = base.set_drawing
replace_cell_content = base.replace_cell_content
borderless_table = base.borderless_table
font = base.font
arrow = base.arrow


def draw_coil(draw: ImageDraw.ImageDraw, x: int, y: int, loops: int = 4, radius: int = 30, width: int = 7) -> int:
    for index in range(loops):
        left = x + index * 2 * radius
        draw.arc((left, y - radius, left + 2 * radius, y + radius), 180, 360, fill="black", width=width)
    return x + loops * 2 * radius


def draw_resistor(draw: ImageDraw.ImageDraw, x: int, y: int, length: int = 260, height: int = 48, width: int = 7) -> int:
    lead = 35
    draw.line((x, y, x + lead, y), fill="black", width=width)
    draw.rectangle((x + lead, y - height, x + length - lead, y + height), outline="black", width=width)
    draw.line((x + length - lead, y, x + length, y), fill="black", width=width)
    return x + length


def draw_source(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int, width: int = 7) -> None:
    center = (top + bottom) // 2
    radius = 70
    draw.line((x, top, x, center - radius), fill="black", width=width)
    draw.ellipse((x - radius, center - radius, x + radius, center + radius), outline="black", width=width)
    draw.arc((x - 42, center - 30, x + 8, center + 25), 190, 350, fill="black", width=5)
    draw.arc((x - 8, center - 10, x + 42, center + 45), 10, 170, fill="black", width=5)
    draw.line((x, center + radius, x, bottom), fill="black", width=width)


def draw_indexed_label(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    symbol: str,
    index: str,
    suffix: str = "",
    *,
    size: int = 44,
    fill: str = "black",
) -> float:
    x, y = position
    main_font = font(base.FONT_ITALIC, size)
    index_font = font(base.FONT_ITALIC, round(size * 0.62))
    draw.text((x, y), symbol, font=main_font, fill=fill)
    symbol_width = draw.textlength(symbol, font=main_font)
    draw.text((x + symbol_width + 1, y + size * 0.48), index, font=index_font, fill=fill)
    index_width = draw.textlength(index, font=index_font)
    if suffix:
        draw.text((x + symbol_width + index_width + 7, y), suffix, font=main_font, fill=fill)
    return x + symbol_width + index_width + 7 + draw.textlength(suffix, font=main_font)


def write_main_svg(path: Path) -> None:
    path.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="850" viewBox="0 0 1800 850">
<defs><marker id="a" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z"/></marker></defs>
<rect width="1800" height="850" fill="white"/>
<g fill="none" stroke="black" stroke-width="7">
<path d="M220 270H390 M390 270a30 30 0 0 1 60 0a30 30 0 0 1 60 0a30 30 0 0 1 60 0a30 30 0 0 1 60 0 M630 270H665 M855 270H970 M970 270a30 30 0 0 1 60 0a30 30 0 0 1 60 0a30 30 0 0 1 60 0a30 30 0 0 1 60 0 M1210 270H1245 M1435 270H1580V680H220"/>
<rect x="665" y="222" width="190" height="96"/><rect x="1245" y="222" width="190" height="96"/>
<path d="M220 270V405 M220 545V680"/><circle cx="220" cy="475" r="70"/><path d="M180 460q25-30 50 0t50 0"/>
<path d="M280 100H365" marker-end="url(#a)"/><path d="M105 390V585" marker-end="url(#a)"/>
</g>
<g font-family="Times New Roman,serif" font-style="italic" font-size="54"><text x="420" y="200">L₁</text><text x="720" y="200">R₁</text><text x="1000" y="200">L₂</text><text x="1300" y="200">R₂</text><text x="305" y="85">I</text><text x="55" y="490">U</text></g>
<g font-family="Times New Roman,serif" font-size="42"><text x="455" y="390">první reálná cívka</text><text x="1080" y="390">druhá reálná cívka</text></g>
</svg>''', encoding="utf-8")


def write_equivalent_svg(path: Path) -> None:
    path.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="760" viewBox="0 0 1800 760">
<defs><marker id="a" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z"/></marker></defs>
<rect width="1800" height="760" fill="white"/>
<g fill="none" stroke="black" stroke-width="7">
<path d="M260 220H560 M820 220H1030 M1030 220a34 34 0 0 1 68 0a34 34 0 0 1 68 0a34 34 0 0 1 68 0a34 34 0 0 1 68 0 M1302 220H1540V620H260"/>
<rect x="595" y="172" width="190" height="96"/><path d="M560 220H595 M785 220H820"/>
<path d="M260 220V350 M260 490V620"/><circle cx="260" cy="420" r="70"/><path d="M220 405q25-30 50 0t50 0"/>
<path d="M400 115H590" marker-end="url(#a)"/><path d="M140 345V535" marker-end="url(#a)"/>
</g>
<g font-family="Times New Roman,serif" font-style="italic" font-size="56"><text x="670" y="150">R</text><text x="1120" y="150">L</text><text x="470" y="80">I</text><text x="88" y="435">U</text></g>
<g font-family="Times New Roman,serif" font-size="40"><text x="560" y="340">R = R₁ + R₂</text><text x="1040" y="340">L = L₁ + L₂</text></g>
</svg>''', encoding="utf-8")


def draw_main_scheme(png_path: Path, svg_path: Path) -> None:
    width, height = 1800, 850
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    wire, top, bottom, source_x = 7, 270, 680, 220
    draw.line((source_x, top, 390, top), fill="black", width=wire)
    x = draw_coil(draw, 390, top)
    x = draw_resistor(draw, x + 35, top)
    draw.line((x, top, 970, top), fill="black", width=wire)
    x = draw_coil(draw, 970, top)
    x = draw_resistor(draw, x + 35, top)
    draw.line((x, top, 1580, top), fill="black", width=wire)
    draw.line((1580, top, 1580, bottom), fill="black", width=wire)
    draw.line((1580, bottom, source_x, bottom), fill="black", width=wire)
    draw_source(draw, source_x, top, bottom, wire)
    arrow(draw, (280, 100), (365, 100), width=6)
    arrow(draw, (105, 390), (105, 585), width=6)
    italic, regular = font(base.FONT_ITALIC, 54), font(base.FONT_REG, 42)
    for position, label in [((420, 125), "L₁"), ((720, 125), "R₁"), ((1000, 125), "L₂"), ((1300, 125), "R₂")]:
        draw.text(position, label, font=italic, fill="black")
    draw.text((305, 30), "I", font=italic, fill="black")
    draw.text((55, 430), "U", font=italic, fill="black")
    draw.text((455, 350), "první reálná cívka", font=regular, fill="black")
    draw.text((1080, 350), "druhá reálná cívka", font=regular, fill="black")
    image.save(png_path, dpi=(300, 300))
    write_main_svg(svg_path)


def draw_equivalent_scheme(png_path: Path, svg_path: Path) -> None:
    width, height = 1800, 760
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    wire, top, bottom, source_x = 7, 220, 620, 260
    draw.line((source_x, top, 560, top), fill="black", width=wire)
    x = draw_resistor(draw, 560, top)
    draw.line((x, top, 1030, top), fill="black", width=wire)
    x = draw_coil(draw, 1030, top, radius=34)
    draw.line((x, top, 1540, top), fill="black", width=wire)
    draw.line((1540, top, 1540, bottom), fill="black", width=wire)
    draw.line((1540, bottom, source_x, bottom), fill="black", width=wire)
    draw_source(draw, source_x, top, bottom, wire)
    arrow(draw, (400, 115), (590, 115), width=6)
    arrow(draw, (140, 345), (140, 535), width=6)
    italic, regular = font(base.FONT_ITALIC, 56), font(base.FONT_REG, 40)
    draw.text((670, 85), "R", font=italic, fill="black")
    draw.text((1120, 85), "L", font=italic, fill="black")
    draw.text((470, 45), "I", font=italic, fill="black")
    draw.text((88, 375), "U", font=italic, fill="black")
    draw.text((560, 305), "R = R₁ + R₂", font=regular, fill="black")
    draw.text((1040, 305), "L = L₁ + L₂", font=regular, fill="black")
    image.save(png_path, dpi=(300, 300))
    write_equivalent_svg(svg_path)


def draw_phasor_diagram(png_path: Path, svg_path: Path) -> None:
    width, height = 1800, 700
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    ur, ul, voltage, phi = 10.864, 33.271, 35.000, 71.917
    origin = (370.0, 620.0)
    scale = 15.5
    resistance_end = (origin[0] + ur * scale, origin[1])
    total_end = (resistance_end[0], origin[1] - ul * scale)

    draw.line((origin[0] - 40, origin[1], 1120, origin[1]), fill="#777777", width=3)
    arrow(draw, origin, resistance_end, width=8, fill="#2F6B3B")
    arrow(draw, resistance_end, total_end, width=8, fill="#C00000")
    arrow(draw, origin, total_end, width=8, fill="#1F4E79")
    arrow(draw, (720, origin[1] - 28), (1040, origin[1] - 28), width=5, fill="black")

    radius = 110
    draw.arc(
        (origin[0] - radius, origin[1] - radius, origin[0] + radius, origin[1] + radius),
        288.083,
        360,
        fill="black",
        width=4,
    )
    draw.ellipse((origin[0] - 8, origin[1] - 8, origin[0] + 8, origin[1] + 8), fill="black")
    italic = font(base.FONT_ITALIC, 44)
    regular = font(base.FONT_REG, 38)
    draw.text((425, 510), "φ = 71,917°", font=italic, fill="black")
    draw_indexed_label(draw, (390, 630), "U", "R", " = 10,864 V", fill="#2F6B3B")
    draw_indexed_label(draw, (resistance_end[0] + 25, 300), "U", "L", " = 33,271 V", fill="#C00000")
    draw.text((230, 285), "U = 35,000 V", font=italic, fill="#1F4E79")
    draw.text((790, 545), "I (referenční směr)", font=italic, fill="black")
    draw.text((1180, 120), "Napěťový trojúhelník", font=regular, fill="black")
    draw_indexed_label(draw, (1180, 190), "U", "R", " je ve směru I", size=38)
    draw_indexed_label(draw, (1180, 260), "U", "L", " je kolmé na I", size=38)
    image.save(png_path, dpi=(300, 300))

    x0, y0 = origin
    xr, yr = resistance_end
    xt, yt = total_end
    arc_x = x0 + radius * math.cos(math.radians(phi))
    arc_y = y0 - radius * math.sin(math.radians(phi))
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
<marker id="green" markerWidth="13" markerHeight="13" refX="11" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z" fill="#2F6B3B"/></marker>
<marker id="red" markerWidth="13" markerHeight="13" refX="11" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z" fill="#C00000"/></marker>
<marker id="blue" markerWidth="13" markerHeight="13" refX="11" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z" fill="#1F4E79"/></marker>
<marker id="black" markerWidth="13" markerHeight="13" refX="11" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z"/></marker>
</defs>
<rect width="{width}" height="{height}" fill="white"/>
<line x1="{x0-40:.2f}" y1="{y0:.2f}" x2="1120" y2="{y0:.2f}" stroke="#777" stroke-width="3"/>
<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{xr:.2f}" y2="{yr:.2f}" stroke="#2F6B3B" stroke-width="8" marker-end="url(#green)"/>
<line x1="{xr:.2f}" y1="{yr:.2f}" x2="{xt:.2f}" y2="{yt:.2f}" stroke="#C00000" stroke-width="8" marker-end="url(#red)"/>
<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{xt:.2f}" y2="{yt:.2f}" stroke="#1F4E79" stroke-width="8" marker-end="url(#blue)"/>
<line x1="720" y1="{y0-28:.2f}" x2="1040" y2="{y0-28:.2f}" stroke="black" stroke-width="5" marker-end="url(#black)"/>
<path d="M{x0+radius:.2f} {y0:.2f} A{radius} {radius} 0 0 0 {arc_x:.2f} {arc_y:.2f}" fill="none" stroke="black" stroke-width="4"/>
<circle cx="{x0:.2f}" cy="{y0:.2f}" r="8"/>
<g font-family="Times New Roman,serif" font-style="italic" font-size="44"><text x="425" y="555">φ = 71,917°</text><text x="390" y="680" fill="#2F6B3B">U<tspan baseline-shift="sub" font-size="28">R</tspan> = 10,864 V</text><text x="{xr+25:.2f}" y="300" fill="#C00000">U<tspan baseline-shift="sub" font-size="28">L</tspan> = 33,271 V</text><text x="230" y="285" fill="#1F4E79">U = 35,000 V</text><text x="790" y="565">I (referenční směr)</text></g>
<g font-family="Times New Roman,serif" font-size="38"><text x="1180" y="150">Napěťový trojúhelník</text><text x="1180" y="220">U<tspan baseline-shift="sub" font-size="25">R</tspan> je ve směru I</text><text x="1180" y="290">U<tspan baseline-shift="sub" font-size="25">L</tspan> je kolmé na I</text></g>
</svg>''', encoding="utf-8")


def make_assets() -> None:
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    draw_main_scheme(GRAPHICS / "schema_zapojeni.png", GRAPHICS / "schema_zapojeni.svg")
    draw_equivalent_scheme(GRAPHICS / "nahradni_schema.png", GRAPHICS / "nahradni_schema.svg")
    draw_phasor_diagram(GRAPHICS / "fazorovy_diagram.png", GRAPHICS / "fazorovy_diagram.svg")


def gap() -> ET.Element:
    return math_r("                                  ", plain=True)


def add_pair(out: list[ET.Element], eq_arch: ET.Element, result_arch: ET.Element,
             general: list[ET.Element], substitution: list[ET.Element], result: list[ET.Element]) -> None:
    out.append(math_paragraph(eq_arch, general + [gap()] + substitution, keep_next=True))
    out.append(math_paragraph(result_arch, result, result=True))


def squared(node: ET.Element | str) -> ET.Element:
    return math_sup(node if isinstance(node, ET.Element) else math_r(node, plain=True), "2")


def build_body(body: ET.Element) -> list[ET.Element]:
    children = list(body)
    h, text, subheading = children[1], children[54], children[5]
    caption_arch, eq_arch, result_arch = children[16], children[17], children[20]
    image_arch, break_arch = children[13], children[14]
    out: list[ET.Element] = []

    out.append(heading(h, "ZADÁNÍ:"))
    out.append(body_text(text, "Dvě reálné cívky jsou spojeny do série a připojeny ke zdroji střídavého napětí o konstantní efektivní hodnotě a proměnné frekvenci. Mezi cívkami není žádná vzájemná magnetická vazba."))
    out.append(body_text(text, "Vypočítejte frekvenci, při které je celkový činný výkon obvodu roven zadané hodnotě. Dále určete proud obvodem a fázový posuv mezi napájecím napětím a proudem."))
    out.append(heading(subheading, "Zadané hodnoty:"))
    out.append(inline_values(children[6], [
        [variable("U"), math_r(" = 35 V", plain=True)],
        [variable("L", "1"), math_r(" = 36 mH", plain=True)],
        [variable("R", "1"), math_r(" = 32 Ω", plain=True)],
    ]))
    out.append(inline_values(children[7], [
        [variable("L", "2"), math_r(" = 41 mH", plain=True)],
        [variable("R", "2"), math_r(" = 24 Ω", plain=True)],
        [variable("P"), math_r(" = 2,1 W", plain=True)],
    ]))
    out.append(heading(h, "NÁHRADNÍ SCHÉMA:"))
    out.append(body_text(text, "Protože jsou obě reálné cívky zapojeny sériově a není mezi nimi vzájemná magnetická vazba, nahradí se jedním sériovým obvodem s celkovým odporem R = R₁ + R₂ a celkovou indukčností L = L₁ + L₂.", keep_next=True))
    out.append(set_drawing(image_arch, "rId8", 6.2, 2.62, "Náhradní schéma dvou reálných cívek"))
    out.append(page_break(break_arch))

    out.append(heading(children[15], "VÝPOČTY:"))
    out.append(body_text(text, "Všechny zobrazené mezivýsledky se zaokrouhlují na tři desetinná místa a v této podobě se použijí v následujícím kroku."))
    out.append(caption(caption_arch, "Celkový činný odpor obvodu:"))
    add_pair(out, eq_arch, result_arch,
             [variable("R"), math_r(" = "), variable("R", "1"), math_r(" + "), variable("R", "2")],
             [variable("R"), math_r(" = 32 + 24", plain=True)],
             [variable("R"), math_r(" = 56,000 Ω", plain=True)])
    out.append(caption(caption_arch, "Celková indukčnost obvodu:"))
    add_pair(out, eq_arch, result_arch,
             [variable("L"), math_r(" = "), variable("L", "1"), math_r(" + "), variable("L", "2")],
             [variable("L"), math_r(" = 36 + 41", plain=True)],
             [variable("L"), math_r(" = 77,000 mH = 0,077 H", plain=True)])
    out.append(caption(caption_arch, "Proud obvodem z činného výkonu:"))
    out.append(math_paragraph(eq_arch, [variable("P"), math_r(" = "), squared(variable("I")), math_r("·"), variable("R"), math_r("   →   "), variable("I"), math_r(" = "), math_rad([math_frac([variable("P")], [variable("R")])])], keep_next=True))
    out.append(math_paragraph(eq_arch, [variable("I"), math_r(" = "), math_rad([math_frac([math_r("2,1", plain=True)], [math_r("56,000", plain=True)])])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("I"), math_r(" = 0,194 A", plain=True)], result=True))
    out.append(caption(caption_arch, "Napětí na odporové části obvodu:"))
    add_pair(out, eq_arch, result_arch,
             [variable("U", "R"), math_r(" = "), variable("R"), math_r("·"), variable("I")],
             [variable("U", "R"), math_r(" = 56,000·0,194", plain=True)],
             [variable("U", "R"), math_r(" = 10,864 V", plain=True)])
    out.append(caption(caption_arch, "Napětí na induktivní části obvodu:"))
    add_pair(out, eq_arch, result_arch,
             [variable("U", "L"), math_r(" = "), math_rad([squared(variable("U")), math_r(" − "), squared(variable("U", "R"))])],
             [variable("U", "L"), math_r(" = "), math_rad([squared("35"), math_r(" − "), squared("10,864")])],
             [variable("U", "L"), math_r(" = 33,271 V", plain=True)])
    out.append(caption(caption_arch, "Celková induktivní reaktance:"))
    add_pair(out, eq_arch, result_arch,
             [variable("X", "L"), math_r(" = "), math_frac([variable("U", "L")], [variable("I")])],
             [variable("X", "L"), math_r(" = "), math_frac([math_r("33,271", plain=True)], [math_r("0,194", plain=True)])],
             [variable("X", "L"), math_r(" = 171,500 Ω", plain=True)])
    out.append(caption(caption_arch, "Frekvence napájecího napětí:"))
    out.append(math_paragraph(eq_arch, [variable("X", "L"), math_r(" = 2·π·"), variable("f"), math_r("·"), variable("L"), math_r("   →   "), variable("f"), math_r(" = "), math_frac([variable("X", "L")], [math_r("2·π·"), variable("L")])], keep_next=True))
    out.append(math_paragraph(eq_arch, [variable("f"), math_r(" = "), math_frac([math_r("171,500", plain=True)], [math_r("2·π·0,077", plain=True)])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("f"), math_r(" = 354,481 Hz", plain=True)], result=True))
    out.append(caption(caption_arch, "Fázový posuv mezi napětím a proudem:"))
    add_pair(out, eq_arch, result_arch,
             [variable("φ"), math_r(" = "), math_r("arctan", plain=True), math_r("("), math_frac([variable("U", "L")], [variable("U", "R")]), math_r(")")],
             [variable("φ"), math_r(" = "), math_r("arctan", plain=True), math_r("("), math_frac([math_r("33,271", plain=True)], [math_r("10,864", plain=True)]), math_r(")")],
             [variable("φ"), math_r(" = 71,917°", plain=True)])
    out.append(body_text(text, "Fázový posuv je kladný, protože obvod má induktivní charakter. Napájecí napětí předbíhá proud, respektive proud se za napětím zpožďuje o 71,917°."))

    # Jediná nová stránka vložená mezi původní výpočty a původní zhodnocení.
    out.append(page_break(break_arch))
    out.append(heading(h, "FÁZOROVÝ DIAGRAM:"))
    out.append(set_drawing(image_arch, "rId11", 6.2, 2.41, "Fázorový diagram napětí a proudu"))
    graph_paragraph = set_drawing(image_arch, "rId12", 6.2, 5.18, "Graf závislosti činného výkonu na frekvenci")
    break_run = ET.SubElement(graph_paragraph, q("w", "r"))
    ET.SubElement(break_run, q("w", "br"), {q("w", "type"): "page"})
    out.append(graph_paragraph)

    evaluation_heading = heading(h, "ZHODNOCENÍ:")
    evaluation_properties = evaluation_heading.find(q("w", "pPr"))
    if evaluation_properties is not None:
        evaluation_spacing = evaluation_properties.find(q("w", "spacing"))
        if evaluation_spacing is not None:
            # Při vynuceném zlomu LibreOffice jinak aplikuje 140 twipů,
            # které u původního přirozeného zlomu na začátku stránky potlačil.
            evaluation_spacing.set(q("w", "before"), "0")
    out.append(evaluation_heading)
    out.append(body_text(text, "Pro sériové spojení dvou reálných cívek byla stanovena výsledná frekvence f = 354,481 Hz, při které je podle použitého modelu celkový činný výkon 2,1 W. Proud obvodem je I = 0,194 A."))
    out.append(body_text(text, "Celkový fázový posuv je φ = 71,917°. Obvod má odporově-induktivní charakter, a proto se proud za napájecím napětím zpožďuje. Výpočet předpokládá lineární parametry cívek a nulovou vzájemnou magnetickou vazbu."))
    out.append(body_text(text, "V důsledku schváleného průběžného zaokrouhlování dává kontrolní dosazení zobrazeného proudu zpětně P = I²R = 2,108 W. Rozdíl 0,008 W, tedy přibližně 0,363 %, je způsoben výhradně použitím mezivýsledků zaokrouhlených na tři desetinná místa."))
    out.append(body_text(text, "Jde o výsledek teoretického výpočtu. Nebyl experimentálně ověřen a nezohledňuje frekvenční závislost odporů, parazitní kapacity, ztráty v magnetických obvodech ani tolerance parametrů cívek."))
    return out


def modify_title(table: ET.Element, body_children: list[ET.Element]) -> None:
    rows = table.findall(q("w", "tr"))
    for node in table.findall(f".//{q('w', 't')}"):
        if node.text == "SEMESTRÁLNÍ PROJEKT ZELE 1Z":
            node.text = "SEMESTRÁLNÍ PROJEKT ZELE 4Z"
        elif node.text == "1Z":
            node.text = "4Z"
        elif node.text == "Stejnosměrná zátěž napájená ze dvou reálných zdrojů":
            node.text = "Sériové spojení dvou reálných cívek"
    scheme_cell = rows[6].findall(q("w", "tc"))[0]
    existing = scheme_cell.findall(q("w", "p"))
    heading_p = deepcopy(existing[0])
    drawing_source = next(p for p in existing if p.find(f".//{q('w', 'drawing')}") is not None)
    drawing_p = set_drawing(drawing_source, "rId7", 6.50, 3.07, "Dvě reálné cívky spojené do série")
    value_arch = body_children[6]

    def value_cell(parts: list[ET.Element], before: int = 0) -> ET.Element:
        paragraph = inline_values(value_arch, [parts])
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

    values = borderless_table([
        [value_cell([variable("U"), math_r(" = 35 V", plain=True)], 2650),
         value_cell([variable("L", "1"), math_r(" = 36 mH", plain=True)], 2650),
         value_cell([variable("R", "1"), math_r(" = 32 Ω", plain=True)], 2650)],
        [value_cell([variable("L", "2"), math_r(" = 41 mH", plain=True)]),
         value_cell([variable("R", "2"), math_r(" = 24 Ω", plain=True)]),
         value_cell([variable("P"), math_r(" = 2,1 W", plain=True)])],
    ], [3400, 3400, 3449])
    trailing = w("p")
    trailing_props = ET.SubElement(trailing, q("w", "pPr"))
    ET.SubElement(trailing_props, q("w", "spacing"), {q("w", "before"): "0", q("w", "after"): "0", q("w", "line"): "1", q("w", "lineRule"): "exact"})
    replace_cell_content(scheme_cell, [heading_p, fixed_spacer(400), drawing_p, values, trailing])


def build_docx() -> None:
    with zipfile.ZipFile(TEMPLATE, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        root.attrib.pop(q("mc", "Ignorable"), None)
        body = root.find(q("w", "body"))
        if body is None:
            raise RuntimeError("Předloha neobsahuje w:body")
        original = list(body)
        modify_title(original[0], original)
        section = deepcopy(original[-1])
        new_body = build_body(body)
        for child in list(body)[1:]:
            body.remove(child)
        for child in new_body:
            body.append(child)
        body.append(section)
        core = zin.read("docProps/core.xml").decode("utf-8")
        core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Semestrální projekt ZELE 4Z</dc:title>", core, flags=re.DOTALL)
        core = re.sub(r"<dc:subject>.*?</dc:subject>", "<dc:subject>Sériové spojení dvou reálných cívek</dc:subject>", core, flags=re.DOTALL)
        rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        extra_rels = (
            '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image3.png"/>'
            '<Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image4.png"/>'
        )
        rels = rels.replace("</Relationships>", extra_rels + "</Relationships>")
        replacements = {
            "word/document.xml": ET.tostring(root, encoding="utf-8", xml_declaration=True),
            "docProps/core.xml": core.encode("utf-8"),
            "word/_rels/document.xml.rels": rels.encode("utf-8"),
            "word/media/image1.png": (GRAPHICS / "schema_zapojeni.png").read_bytes(),
            "word/media/image2.png": (GRAPHICS / "nahradni_schema.png").read_bytes(),
        }
        with tempfile.NamedTemporaryFile(dir=OUTPUT, suffix=".docx", delete=False) as temp:
            temp_path = Path(temp.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    zout.writestr(item, replacements.get(item.filename, zin.read(item.filename)))
                zout.write(GRAPHICS / "fazorovy_diagram.png", "word/media/image3.png")
                zout.write(GRAPHICS / "graf_P_f.png", "word/media/image4.png")
            temp_path.replace(DOCX_OUT)
            DOCX_OUT.chmod(0o664)
        finally:
            if temp_path.exists():
                temp_path.unlink()


def write_audit() -> None:
    audit = """Kontrola výpočtu ZELE 4Z
Průběžně zaokrouhlené hodnoty:
R = 56,000 Ω; L = 77,000 mH = 0,077 H; I = 0,194 A
UR = 10,864 V; UL = 33,271 V; XL = 171,500 Ω
f = 354,481 Hz; φ = 71,917°

Kontrola z plné přesnosti:
I = 0,193649167 A; UR = 10,844353370 V; UL = 33,277620107 V
XL = 171,844891314 Ω; f = 355,194336348 Hz; φ = 71,950491872°

Kontrola výkonu ze zobrazeného proudu:
P = 0,194² · 56 = 2,108 W
Rozdíl = 0,008 W = 0,363 %; příčinou je schválené průběžné zaokrouhlování.
"""
    (WORK / "kontrola_vypoctu.txt").write_text(audit, encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    make_assets()
    graph_helper.create_graph(XLSX_OUT, GRAPHICS / "graf_P_f.png")
    build_docx()
    write_audit()
    print(DOCX_OUT)


if __name__ == "__main__":
    main()
