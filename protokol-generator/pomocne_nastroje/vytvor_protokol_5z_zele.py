#!/usr/bin/env python3
"""Vytvoří schválený teoretický protokol ZELE 5Z z ruční předlohy."""

from __future__ import annotations

from copy import deepcopy
import base64
import cmath
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

TEMPLATE = ROOT / "vzory" / "vzor_vypoctovych_sekci.docx"
MEASUREMENT = ROOT / "5Z-zele-5"
OUTPUT = MEASUREMENT / "vystup"
GRAPHICS = OUTPUT / "grafika"
WORK = MEASUREMENT / "pracovni"
DOCX_OUT = OUTPUT / "protokol.docx"

q = base.q
w = base.w
m = base.m
math_r = base.math_r
math_sub = base.math_sub
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


def draw_coil(draw: ImageDraw.ImageDraw, x: int, y: int, loops: int = 4, radius: int = 28, width: int = 7) -> int:
    """Nakreslí vodorovnou tlumivku a vrátí koncovou souřadnici x."""
    for index in range(loops):
        left = x + index * 2 * radius
        draw.arc((left, y - radius, left + 2 * radius, y + radius), 180, 360, fill="black", width=width)
    return x + loops * 2 * radius


def draw_indexed_label(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    symbol: str,
    index: str,
    suffix: str = "",
    *,
    size: int = 52,
    fill: str = "black",
) -> None:
    """Vykreslí technickou značku se skutečně sníženým indexem."""
    x, y = position
    main_font = font(base.FONT_ITALIC, size)
    index_font = font(base.FONT_ITALIC, round(size * 0.62))
    draw.text((x, y), symbol, font=main_font, fill=fill)
    symbol_width = draw.textlength(symbol, font=main_font)
    draw.text((x + symbol_width + 1, y + size * 0.48), index, font=index_font, fill=fill)
    index_width = draw.textlength(index, font=index_font)
    if suffix:
        draw.text((x + symbol_width + index_width + 7, y), suffix, font=main_font, fill=fill)


def write_embedded_svg(png_path: Path, svg_path: Path, width: int, height: int) -> None:
    """Uchová kompatibilní zdrojový SVG se stejnou kresbou jako kontrolní PNG."""
    encoded = base64.b64encode(png_path.read_bytes()).decode()
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="white"/>
  <image href="data:image/png;base64,{encoded}" width="{width}" height="{height}"/>
</svg>''',
        encoding="utf-8",
    )


def draw_main_scheme(png_path: Path, svg_path: Path) -> None:
    width, height = 1800, 925
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    wire = 7
    top, bottom = 250, 735
    source_x = 210
    branch_x = 550
    lamp_x = 1320
    starter_x = 1570

    # Zdroj a hlavní vodiče.
    draw.line((source_x, top, 620, top), fill="black", width=wire)
    coil_end = draw_coil(draw, 620, top, loops=4, radius=34, width=wire)
    draw.line((coil_end, top, lamp_x, top), fill="black", width=wire)
    draw.line((source_x, bottom, starter_x, bottom), fill="black", width=wire)
    draw.line((source_x, top, source_x, 390), fill="black", width=wire)
    draw.ellipse((source_x - 65, 390, source_x + 65, 520), outline="black", width=wire)
    draw.arc((source_x - 40, 420, source_x + 5, 470), 190, 350, fill="black", width=5)
    draw.arc((source_x - 5, 440, source_x + 40, 490), 10, 170, fill="black", width=5)
    draw.line((source_x, 520, source_x, bottom), fill="black", width=wire)

    # Kompenzační kondenzátor paralelně k celému svítidlu.
    draw.line((branch_x, top, branch_x, 415), fill="black", width=wire)
    draw.line((branch_x - 55, 415, branch_x + 55, 415), fill="black", width=wire)
    draw.line((branch_x - 55, 455, branch_x + 55, 455), fill="black", width=wire)
    draw.line((branch_x, 455, branch_x, bottom), fill="black", width=wire)
    draw.ellipse((branch_x - 10, top - 10, branch_x + 10, top + 10), fill="black")
    draw.ellipse((branch_x - 10, bottom - 10, branch_x + 10, bottom + 10), fill="black")

    # Zářivková trubice a startér.
    draw.line((lamp_x, top, lamp_x, 355), fill="black", width=wire)
    draw.rounded_rectangle((lamp_x - 48, 355, lamp_x + 48, 625), radius=42, outline="black", width=wire)
    draw.line((lamp_x, 625, lamp_x, bottom), fill="black", width=wire)
    draw.line((lamp_x, 330, starter_x, 330), fill="black", width=wire)
    draw.line((starter_x, 330, starter_x, 415), fill="black", width=wire)
    draw.ellipse((starter_x - 55, 415, starter_x + 55, 525), outline="black", width=wire)
    draw.line((starter_x - 25, 475, starter_x + 25, 445), fill="black", width=5)
    draw.line((starter_x, 525, starter_x, bottom), fill="black", width=wire)

    # Směry proudů a napětí.
    arrow(draw, (275, 175), (455, 175), width=6)
    arrow(draw, (980, 175), (1160, 175), width=6)
    arrow(draw, (485, 315), (485, 475), width=5)
    arrow(draw, (80, 330), (80, 620), width=5)

    draw.text((325, 90), "I′", font=font(base.FONT_ITALIC, 58), fill="black")
    draw.text((1050, 90), "I", font=font(base.FONT_ITALIC, 58), fill="black")
    draw_indexed_label(draw, (390, 345), "I", "C")
    draw.text((35, 430), "U", font=font(base.FONT_ITALIC, 58), fill="black")
    draw.text((750, 315), "tlumivka", font=font(base.FONT_REG, 48), fill="black")
    draw_indexed_label(draw, (610, 455), "C", "K")
    draw.text((1210, 650), "zářivková trubice", font=font(base.FONT_REG, 42), fill="black")
    draw.text((1460, 355), "startér", font=font(base.FONT_REG, 42), fill="black")
    image.save(png_path, dpi=(300, 300))
    write_embedded_svg(png_path, svg_path, width, height)


def draw_equivalent_scheme(png_path: Path, svg_path: Path) -> None:
    width, height = 1800, 900
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    wire = 7
    top, bottom = 230, 710
    source_x, cap_x, load_x = 260, 690, 1370

    draw.line((source_x, top, 760, top), fill="black", width=wire)
    coil_end = draw_coil(draw, 760, top, loops=4, radius=32, width=wire)
    draw.line((coil_end, top, 1210, top), fill="black", width=wire)
    draw.rectangle((1210, top - 45, 1410, top + 45), outline="black", width=wire)
    draw.line((1410, top, load_x + 40, top), fill="black", width=wire)
    draw.line((load_x + 40, top, load_x + 40, bottom), fill="black", width=wire)
    draw.line((source_x, bottom, load_x + 40, bottom), fill="black", width=wire)

    draw.line((source_x, top, source_x, 365), fill="black", width=wire)
    draw.ellipse((source_x - 70, 365, source_x + 70, 505), outline="black", width=wire)
    draw.arc((source_x - 42, 400, source_x + 8, 455), 190, 350, fill="black", width=5)
    draw.arc((source_x - 8, 420, source_x + 42, 475), 10, 170, fill="black", width=5)
    draw.line((source_x, 505, source_x, bottom), fill="black", width=wire)

    draw.line((cap_x, top, cap_x, 400), fill="black", width=wire)
    draw.line((cap_x - 60, 400, cap_x + 60, 400), fill="black", width=wire)
    draw.line((cap_x - 60, 445, cap_x + 60, 445), fill="black", width=wire)
    draw.line((cap_x, 445, cap_x, bottom), fill="black", width=wire)
    draw.ellipse((cap_x - 10, top - 10, cap_x + 10, top + 10), fill="black")
    draw.ellipse((cap_x - 10, bottom - 10, cap_x + 10, bottom + 10), fill="black")

    arrow(draw, (325, 150), (500, 150), width=6)
    arrow(draw, (1020, 150), (1185, 150), width=6)
    arrow(draw, (615, 300), (615, 475), width=5)
    arrow(draw, (115, 330), (115, 610), width=5)
    draw.text((385, 65), "I′", font=font(base.FONT_ITALIC, 58), fill="black")
    draw.text((1090, 65), "I", font=font(base.FONT_ITALIC, 58), fill="black")
    draw_indexed_label(draw, (520, 345), "I", "C")
    draw.text((60, 425), "U", font=font(base.FONT_ITALIC, 58), fill="black")
    draw_indexed_label(draw, (865, 315), "X", "L")
    draw.text((1290, 320), "R", font=font(base.FONT_ITALIC, 52), fill="black")
    draw_indexed_label(draw, (750, 455), "C", "K")
    image.save(png_path, dpi=(300, 300))
    write_embedded_svg(png_path, svg_path, width, height)


def draw_phasor(png_path: Path, svg_path: Path) -> None:
    # Nezaokrouhlené hodnoty pro geometrii.
    voltage = 230.0
    power = 30.0
    cos_phi = 0.31
    cos_phi_p = 0.95
    phi = math.acos(cos_phi)
    phi_p = math.acos(cos_phi_p)
    current = power / (voltage * cos_phi)
    current_p = power / (voltage * cos_phi_p)
    reactive = power * math.tan(phi)
    reactive_p = power * math.tan(phi_p)
    current_c = (reactive - reactive_p) / voltage
    active_component = power / voltage
    reactive_component = reactive / voltage
    reactive_component_p = reactive_p / voltage

    width, height = 1800, 1050
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    origin = (520.0, 505.0)
    px_per_mm = 18.0
    voltage_scale = px_per_mm / 6.0
    current_scale = px_per_mm / 0.02

    u_end = (origin[0] + voltage * voltage_scale, origin[1])
    i_end = (
        origin[0] + active_component * current_scale,
        origin[1] + reactive_component * current_scale,
    )
    ic_end = (origin[0], origin[1] - current_c * current_scale)
    ip_end = (
        origin[0] + active_component * current_scale,
        origin[1] + reactive_component_p * current_scale,
    )

    # Pomocné osy a vektory.
    draw.line((180, origin[1], 1610, origin[1]), fill="#555555", width=3)
    draw.line((origin[0], 95, origin[0], 965), fill="#555555", width=3)
    arrow(draw, origin, u_end, width=8, fill="#1f4fff")
    arrow(draw, origin, i_end, width=8, fill="#d7191c")
    arrow(draw, origin, ic_end, width=8, fill="#d7191c")
    arrow(draw, origin, ip_end, width=8, fill="#d7191c")

    # Konstrukční přičtení I_C od konce I ke konci I′.
    for y in range(round(ip_end[1]), round(i_end[1]), 30):
        draw.line((i_end[0], y, i_end[0], min(y + 15, i_end[1])), fill="#666666", width=3)

    # Oblouky fázových úhlů.
    r1, r2 = 190, 125
    draw.arc((origin[0] - r1, origin[1] - r1, origin[0] + r1, origin[1] + r1), 0, math.degrees(phi), fill="black", width=4)
    draw.arc((origin[0] - r2, origin[1] - r2, origin[0] + r2, origin[1] + r2), 0, math.degrees(phi_p), fill="black", width=4)

    draw.ellipse((origin[0] - 9, origin[1] - 9, origin[0] + 9, origin[1] + 9), fill="black")
    draw.text((u_end[0] - 40, u_end[1] + 30), "U = 230,000 V", font=font(base.FONT_ITALIC, 40), fill="#1f4fff")
    draw.text((i_end[0] + 25, i_end[1] - 10), "I = 0,421 A", font=font(base.FONT_ITALIC, 40), fill="#b00000")
    draw_indexed_label(draw, (ic_end[0] + 25, ic_end[1] - 10), "I", "C", " = 0,357 A", size=40, fill="#b00000")
    draw.text((ip_end[0] + 30, ip_end[1] - 40), "I′ = 0,137 A", font=font(base.FONT_ITALIC, 40), fill="#b00000")
    draw.text((origin[0] + 130, origin[1] + 115), "φ′ = 18,195°", font=font(base.FONT_ITALIC, 36), fill="black")
    draw.text((origin[0] + 125, origin[1] + 265), "φ = 71,941°", font=font(base.FONT_ITALIC, 36), fill="black")
    draw.text((1080, 90), "1 mm ≙ 6 V", font=font(base.FONT_REG, 36), fill="black")
    draw.text((1080, 145), "1 mm ≙ 0,02 A", font=font(base.FONT_REG, 36), fill="black")
    image.save(png_path, dpi=(300, 300))

    # Skutečný vektorový SVG zdroj fázorové konstrukce.
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs><marker id="arr-blue" markerWidth="14" markerHeight="14" refX="12" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1f4fff"/></marker><marker id="arr-red" markerWidth="14" markerHeight="14" refX="12" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#d7191c"/></marker></defs>
<rect width="{width}" height="{height}" fill="white"/>
<line x1="180" y1="{origin[1]}" x2="1610" y2="{origin[1]}" stroke="#555" stroke-width="3"/>
<line x1="{origin[0]}" y1="95" x2="{origin[0]}" y2="965" stroke="#555" stroke-width="3"/>
<line x1="{origin[0]}" y1="{origin[1]}" x2="{u_end[0]:.2f}" y2="{u_end[1]:.2f}" stroke="#1f4fff" stroke-width="8" marker-end="url(#arr-blue)"/>
<line x1="{origin[0]}" y1="{origin[1]}" x2="{i_end[0]:.2f}" y2="{i_end[1]:.2f}" stroke="#d7191c" stroke-width="8" marker-end="url(#arr-red)"/>
<line x1="{origin[0]}" y1="{origin[1]}" x2="{ic_end[0]:.2f}" y2="{ic_end[1]:.2f}" stroke="#d7191c" stroke-width="8" marker-end="url(#arr-red)"/>
<line x1="{origin[0]}" y1="{origin[1]}" x2="{ip_end[0]:.2f}" y2="{ip_end[1]:.2f}" stroke="#d7191c" stroke-width="8" marker-end="url(#arr-red)"/>
<line x1="{i_end[0]:.2f}" y1="{i_end[1]:.2f}" x2="{ip_end[0]:.2f}" y2="{ip_end[1]:.2f}" stroke="#666" stroke-width="3" stroke-dasharray="15 15"/>
<text x="{u_end[0]-40:.2f}" y="{u_end[1]+70:.2f}" font-family="Times New Roman,serif" font-size="40" fill="#1f4fff">U = 230,000 V</text>
<text x="{i_end[0]+25:.2f}" y="{i_end[1]:.2f}" font-family="Times New Roman,serif" font-size="40" fill="#b00000">I = 0,421 A</text>
<text x="{ic_end[0]+25:.2f}" y="{ic_end[1]:.2f}" font-family="Times New Roman,serif" font-size="40" fill="#b00000">Iᴄ = 0,357 A</text>
<text x="{ip_end[0]+30:.2f}" y="{ip_end[1]-20:.2f}" font-family="Times New Roman,serif" font-size="40" fill="#b00000">I′ = 0,137 A</text>
<text x="1080" y="120" font-family="Times New Roman,serif" font-size="36">1 mm ≙ 6 V</text>
<text x="1080" y="175" font-family="Times New Roman,serif" font-size="36">1 mm ≙ 0,02 A</text>
</svg>''',
        encoding="utf-8",
    )


def make_assets() -> None:
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    draw_main_scheme(GRAPHICS / "schema_zapojeni.png", GRAPHICS / "schema_zapojeni.svg")
    draw_equivalent_scheme(GRAPHICS / "nahradni_schema.png", GRAPHICS / "nahradni_schema.svg")
    draw_phasor(GRAPHICS / "fazorovy_diagram.png", GRAPHICS / "fazorovy_diagram.svg")


def gap() -> ET.Element:
    return math_r("                                  ", plain=True)


def add_pair(out: list[ET.Element], eq_arch: ET.Element, result_arch: ET.Element,
             general: list[ET.Element], substitution: list[ET.Element], result: list[ET.Element]) -> None:
    out.append(math_paragraph(eq_arch, general + [gap()] + substitution, keep_next=True))
    out.append(math_paragraph(result_arch, result, result=True))


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
    out.append(body_text(text, "Klasické zářivkové svítidlo je tvořeno zářivkovou trubicí, tlumivkou a startérem. Zářivková trubice spolu s tlumivkou se v ustáleném stavu chová jako odporově-induktivní zátěž. Parazitní vlastnosti a nelinearity se v teoretickém modelu zanedbávají. Startér sepne pouze na okamžik při zapnutí a při běžném svícení je rozepnutý."))
    out.append(body_text(text, "Kompenzační kondenzátor není pro samotnou funkci svítidla nezbytný. Jeho úlohou je zmenšit induktivní jalový odběr svítidla, a tím zvýšit jeho účiník na zadanou hodnotu."))
    out.append(body_text(text, "Určete kapacitu kompenzačního kondenzátoru Cₖ, jeho napěťové dimenzování, proud svítidla bez kompenzace I a proud svítidla po kompenzaci I′."))
    out.append(heading(subheading, "Zadané hodnoty:"))
    out.append(inline_values(children[6], [
        [variable("U"), math_r(" = 230 V", plain=True)],
        [variable("f"), math_r(" = 50 Hz", plain=True)],
        [variable("P"), math_r(" = 30 W", plain=True)],
    ]))
    out.append(inline_values(children[7], [
        [math_r("cos", plain=True), variable("φ"), math_r(" = 0,31", plain=True)],
        [math_r("cos", plain=True), math_r("φ′"), math_r(" = 0,95", plain=True)],
    ]))
    out.append(heading(h, "NÁHRADNÍ SCHÉMA:"))
    out.append(body_text(text, "Zářivková trubice s tlumivkou je nahrazena sériovou odporově-induktivní větví R–Xʟ. Kondenzátor Cₖ je připojen paralelně k celému svítidlu. Pro proudy platí fázorový vztah Ī′ = Ī + Īᴄ.", keep_next=True))
    out.append(set_drawing(image_arch, "rId8", 6.2, 3.1, "Náhradní schéma svítidla"))
    out.append(page_break(break_arch))

    out.append(heading(children[15], "VÝPOČTY:"))
    out.append(body_text(text, "Všechny zobrazené mezivýsledky se zaokrouhlují na tři desetinná místa a v této podobě se použijí v následujícím kroku."))

    out.append(caption(caption_arch, "Fázové posuvy před kompenzací a po kompenzaci:"))
    add_pair(out, eq_arch, result_arch,
             [variable("φ"), math_r(" = "), math_r("arccos", plain=True), math_r("("), math_r("cos", plain=True), variable("φ"), math_r(")")],
             [variable("φ"), math_r(" = arccos(0,31)", plain=True)],
             [variable("φ"), math_r(" = 71,941°", plain=True)])
    add_pair(out, eq_arch, result_arch,
             [math_r("φ′"), math_r(" = "), math_r("arccos", plain=True), math_r("("), math_r("cos", plain=True), math_r("φ′"), math_r(")")],
             [math_r("φ′"), math_r(" = arccos(0,95)", plain=True)],
             [math_r("φ′"), math_r(" = 18,195°", plain=True)])

    out.append(caption(caption_arch, "Potřebný jalový výkon kompenzačního kondenzátoru:"))
    add_pair(out, eq_arch, result_arch,
             [variable("Q", "C"), math_r(" = "), variable("P"), math_r("["), math_r("tan", plain=True), variable("φ"), math_r(" − "), math_r("tan", plain=True), math_r("φ′"), math_r("]")],
             [variable("Q", "C"), math_r(" = 30(tan 71,941° − tan 18,195°)", plain=True)],
             [variable("Q", "C"), math_r(" = 82,147 var", plain=True)])

    out.append(caption(caption_arch, "Proud kompenzačního kondenzátoru:"))
    add_pair(out, eq_arch, result_arch,
             [variable("I", "C"), math_r(" = "), math_frac([variable("Q", "C")], [variable("U")])],
             [variable("I", "C"), math_r(" = "), math_frac([math_r("82,147", plain=True)], [math_r("230", plain=True)])],
             [variable("I", "C"), math_r(" = 0,357 A", plain=True)])

    out.append(caption(caption_arch, "Kapacitní reaktance kondenzátoru:"))
    add_pair(out, eq_arch, result_arch,
             [variable("X", "C"), math_r(" = "), math_frac([variable("U")], [variable("I", "C")])],
             [variable("X", "C"), math_r(" = "), math_frac([math_r("230", plain=True)], [math_r("0,357", plain=True)])],
             [variable("X", "C"), math_r(" = 644,258 Ω", plain=True)])

    out.append(caption(caption_arch, "Kapacita kompenzačního kondenzátoru:"))
    add_pair(out, eq_arch, result_arch,
             [variable("ω"), math_r(" = 2·π·"), variable("f")],
             [variable("ω"), math_r(" = 2·π·50", plain=True)],
             [variable("ω"), math_r(" = 314,159 rad·s⁻¹", plain=True)])
    out.append(math_paragraph(eq_arch, [variable("X", "C"), math_r(" = "), math_frac([math_r("1", plain=True)], [variable("ω"), math_r("·"), variable("C", "K")]), math_r("   →   "), variable("C", "K"), math_r(" = "), math_frac([math_r("1", plain=True)], [variable("ω"), math_r("·"), variable("X", "C")])]))
    out.append(math_paragraph(eq_arch, [variable("C", "K"), math_r(" = "), math_frac([math_r("1", plain=True)], [math_r("314,159·644,258", plain=True)])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("C", "K"), math_r(" = 4,941·10⁻⁶ F = 4,941 µF", plain=True)], result=True))
    out.append(body_text(text, "Jde o teoreticky vypočtenou hodnotu. Praktická normalizovaná kapacita se nevybírá, protože ji zadání nepožaduje."))

    out.append(caption(caption_arch, "Napěťové dimenzování kondenzátoru:"))
    add_pair(out, eq_arch, result_arch,
             [variable("U", "m"), math_r(" = "), math_rad([math_r("2", plain=True)]), math_r("·"), variable("U")],
             [variable("U", "m"), math_r(" = "), math_rad([math_r("2", plain=True)]), math_r("·230", plain=True)],
             [variable("U", "m"), math_r(" = 325,269 V ≈ 325 V", plain=True)])
    out.append(body_text(text, "Hodnota 325,269 V je amplituda napájecího napětí, nikoli AC jmenovitá hodnota uvedená na kondenzátoru. Kondenzátor musí být výrobcem určen pro trvalý provoz alespoň při 230 V AC / 50 Hz, bezpečně snášet vypočtenou amplitudu a provozní přepětí. Vhodný je fóliový kompenzační kondenzátor, nikoli běžný polarizovaný elektrolytický kondenzátor."))

    out.append(caption(caption_arch, "Proudy před kompenzací a po kompenzaci:"))
    add_pair(out, eq_arch, result_arch,
             [variable("I"), math_r(" = "), math_frac([variable("P")], [variable("U"), math_r("·"), math_r("cos", plain=True), variable("φ")])],
             [variable("I"), math_r(" = "), math_frac([math_r("30", plain=True)], [math_r("230·0,31", plain=True)])],
             [variable("I"), math_r(" = 0,421 A", plain=True)])
    add_pair(out, eq_arch, result_arch,
             [math_r("I′"), math_r(" = "), math_frac([variable("P")], [variable("U"), math_r("·"), math_r("cos", plain=True), math_r("φ′")])],
             [math_r("I′"), math_r(" = "), math_frac([math_r("30", plain=True)], [math_r("230·0,95", plain=True)])],
             [math_r("I′"), math_r(" = 0,137 A", plain=True)])

    out.append(caption(caption_arch, "Komplexní kontrola proudů:"))
    add_pair(out, eq_arch, result_arch,
             [variable("Q"), math_r(" = "), variable("P"), math_r("·"), math_r("tan", plain=True), variable("φ")],
             [variable("Q"), math_r(" = 30·tan 71,941°", plain=True)],
             [variable("Q"), math_r(" = 92,008 var", plain=True)])
    add_pair(out, eq_arch, result_arch,
             [math_r("Q′"), math_r(" = "), variable("Q"), math_r(" − "), variable("Q", "C")],
             [math_r("Q′"), math_r(" = 92,008 − 82,147", plain=True)],
             [math_r("Q′"), math_r(" = 9,861 var", plain=True)])
    out.append(math_paragraph(eq_arch, [variable("I", bar=True), math_r(" = "), math_frac([variable("P")], [variable("U")]), math_r(" − j"), math_frac([variable("Q")], [variable("U")])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("I", bar=True), math_r(" = 0,130 − j0,400 A", plain=True)], result=True))
    out.append(math_paragraph(eq_arch, [variable("I", "C", bar=True), math_r(" = j"), math_frac([variable("Q", "C")], [variable("U")])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("I", "C", bar=True), math_r(" = j0,357 A", plain=True)], result=True))
    out.append(math_paragraph(eq_arch, [math_r("Ī′"), math_r(" = "), variable("I", bar=True), math_r(" + "), variable("I", "C", bar=True)]))
    out.append(math_paragraph(eq_arch, [math_r("Ī′"), math_r(" = (0,130 − j0,400) + j0,357", plain=True)], keep_next=True))
    out.append(math_paragraph(result_arch, [math_r("Ī′"), math_r(" = 0,130 − j0,043 A", plain=True)], result=True))
    out.append(body_text(text, "Velikosti komplexních proudů po zaokrouhlení potvrzují I = 0,421 A a I′ = 0,137 A. Drobná odchylka úhlu určeného pouze ze zobrazených složek je důsledkem průběžného zaokrouhlení."))

    out.append(page_break(break_arch))
    out.append(heading(h, "FÁZOROVÝ DIAGRAM:"))
    out.append(body_text(text, "Napájecí napětí je referenčním fázorem. Proud I zaostává o 71,941°, proud kondenzátoru Iᴄ předbíhá o 90° a proud po kompenzaci I′ zaostává o 18,195°. Geometrie diagramu je vytvořena z nezaokrouhlených hodnot; zobrazené popisky jsou zaokrouhleny na tři desetinná místa.", keep_next=True))
    out.append(set_drawing(image_arch, "rId11", 6.2, 3.62, "Fázorový diagram kompenzace"))

    out.append(heading(h, "ZHODNOCENÍ:"))
    out.append(body_text(text, "Pro zářivkové svítidlo s činným výkonem 30 W a původním účiníkem 0,31 byla vypočtena teoretická kapacita paralelního kompenzačního kondenzátoru Cₖ = 4,941 µF."))
    out.append(body_text(text, "Amplituda napájecího napětí je 325,269 V. Tato hodnota není AC jmenovitý údaj kondenzátoru; součástka musí být výrobcem určena pro trvalý provoz alespoň při 230 V AC / 50 Hz, bezpečně snášet uvedenou amplitudu a mít vhodnou napěťovou rezervu."))
    out.append(body_text(text, "Proud svítidla bez kompenzace je 0,421 A. Po zvýšení účiníku na 0,95 klesne proud odebíraný ze sítě na 0,137 A. Činný výkon zůstává 30 W; kondenzátor zmenšuje induktivní jalovou složku proudu, a tím proudové zatížení vedení a související ztráty."))
    out.append(body_text(text, "Komplexní kontrola potvrdila, že kapacitní proud j0,357 A zmenší imaginární složku původního proudu z −j0,400 A na −j0,043 A. Výsledky popisují idealizovaný teoretický model a nebyly experimentálně ověřeny. Nezahrnují nelinearity trubice, parazitní vlastnosti tlumivky, tolerance kondenzátoru ani změny napájecího napětí."))
    return out


def modify_title(table: ET.Element, body_children: list[ET.Element]) -> None:
    rows = table.findall(q("w", "tr"))
    for node in table.findall(f".//{q('w', 't')}"):
        if node.text == "SEMESTRÁLNÍ PROJEKT ZELE 1Z":
            node.text = "SEMESTRÁLNÍ PROJEKT ZELE 5Z"
        elif node.text == "1Z":
            node.text = "5Z"
        elif node.text == "Stejnosměrná zátěž napájená ze dvou reálných zdrojů":
            node.text = "Kompenzace účiníku zářivkového svítidla"

    scheme_cell = rows[6].findall(q("w", "tc"))[0]
    existing = scheme_cell.findall(q("w", "p"))
    heading_p = deepcopy(existing[0])
    drawing_source = next(p for p in existing if p.find(f".//{q('w', 'drawing')}") is not None)
    drawing_p = set_drawing(drawing_source, "rId7", 6.50, 3.34, "Schéma zářivkového svítidla")
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
        [
            value_cell([variable("U"), math_r(" = 230 V", plain=True)], 2450),
            value_cell([variable("f"), math_r(" = 50 Hz", plain=True)], 2450),
            value_cell([variable("P"), math_r(" = 30 W", plain=True)], 2450),
        ],
        [
            value_cell([math_r("cos", plain=True), variable("φ"), math_r(" = 0,31", plain=True)]),
            value_cell([math_r("cos", plain=True), math_r("φ′"), math_r(" = 0,95", plain=True)]),
            w("p"),
        ],
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

        rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        rels = rels.replace(
            "</Relationships>",
            '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image3.png"/></Relationships>',
        )
        core = zin.read("docProps/core.xml").decode("utf-8")
        core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Semestrální projekt ZELE 5Z</dc:title>", core, flags=re.DOTALL)
        core = re.sub(r"<dc:subject>.*?</dc:subject>", "<dc:subject>Kompenzace účiníku zářivkového svítidla</dc:subject>", core, flags=re.DOTALL)

        replacements = {
            "word/document.xml": ET.tostring(root, encoding="utf-8", xml_declaration=True),
            "word/_rels/document.xml.rels": rels.encode("utf-8"),
            "docProps/core.xml": core.encode("utf-8"),
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
            temp_path.replace(DOCX_OUT)
            DOCX_OUT.chmod(0o664)
        finally:
            if temp_path.exists():
                temp_path.unlink()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    make_assets()
    build_docx()
    print(DOCX_OUT)


if __name__ == "__main__":
    main()
