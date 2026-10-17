#!/usr/bin/env python3
"""Vytvoří schválený teoretický protokol ZELE 3Z z ruční předlohy."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import math
from pathlib import Path
import re
import subprocess
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
MEASUREMENT = ROOT / "3Z-zele-3"
SOURCE_ASSIGNMENT = MEASUREMENT / "podklady" / "Zadání semestrálního projektu ZELE.pdf"
OUTPUT = MEASUREMENT / "vystup"
GRAPHICS = OUTPUT / "grafika"
WORK = MEASUREMENT / "pracovni"
DOCX_OUT = OUTPUT / "protokol.docx"

q = base.q
w = base.w
math_r = base.math_r
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


def draw_motor(png_path: Path, svg_path: Path) -> None:
    """Vytvoří čisté technické zobrazení třífázového asynchronního motoru."""
    width, height = 1800, 850
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    outline = "#111111"
    body_fill = "#e8eaed"
    dark_fill = "#c4c8cc"
    accent = "#6f777d"

    # Patky a základna.
    draw.rounded_rectangle((395, 650, 1450, 710), radius=20, fill=dark_fill, outline=outline, width=7)
    draw.polygon([(500, 575), (680, 575), (735, 660), (455, 660)], fill=body_fill, outline=outline)
    draw.polygon([(1170, 575), (1350, 575), (1400, 660), (1120, 660)], fill=body_fill, outline=outline)
    draw.ellipse((485, 672, 535, 722), fill="white", outline=outline, width=5)
    draw.ellipse((1310, 672, 1360, 722), fill="white", outline=outline, width=5)

    # Těleso motoru, čelní štíty a hřídel.
    draw.rounded_rectangle((480, 210, 1390, 590), radius=155, fill=body_fill, outline=outline, width=8)
    draw.ellipse((390, 225, 690, 580), fill=dark_fill, outline=outline, width=8)
    draw.ellipse((430, 270, 650, 535), fill="#f5f5f5", outline=outline, width=6)
    draw.ellipse((500, 350, 580, 455), fill=accent, outline=outline, width=5)
    draw.rounded_rectangle((175, 375, 510, 430), radius=12, fill=dark_fill, outline=outline, width=7)
    draw.rectangle((120, 387, 185, 418), fill=accent, outline=outline, width=5)
    draw.ellipse((1310, 225, 1480, 580), fill=dark_fill, outline=outline, width=8)

    # Chladicí žebra.
    for x in range(690, 1320, 70):
        draw.line((x, 245, x, 555), fill=accent, width=9)
        draw.line((x + 18, 255, x + 18, 545), fill="#ffffff", width=3)

    # Svorkovnice.
    draw.rounded_rectangle((830, 95, 1170, 245), radius=28, fill=dark_fill, outline=outline, width=7)
    draw.rectangle((875, 60, 1125, 115), fill=body_fill, outline=outline, width=7)
    for x in (900, 980, 1060):
        draw.ellipse((x, 145, x + 34, 179), fill="white", outline=outline, width=4)

    # Směr otáčení a popis stroje.
    draw.arc((1450, 235, 1690, 475), 205, 485, fill=outline, width=7)
    draw.polygon([(1636, 245), (1692, 236), (1660, 286)], fill=outline)
    draw.text((710, 350), "M", font=font(base.FONT_ITALIC, 120), fill=outline)
    draw.text((820, 400), "3~", font=font(base.FONT_REG, 64), fill=outline)
    draw.text((660, 745), "trojfázový asynchronní motor", font=font(base.FONT_REG, 48), fill=outline)
    image.save(png_path, dpi=(300, 300))

    # Stejná kresba jako skutečný vektorový zdroj.
    fins = "".join(
        f'<line x1="{x}" y1="245" x2="{x}" y2="555"/><line x1="{x+18}" y1="255" x2="{x+18}" y2="545" stroke="white" stroke-width="3"/>'
        for x in range(690, 1320, 70)
    )
    terminals = "".join(f'<circle cx="{x+17}" cy="162" r="17" fill="white"/>' for x in (900, 980, 1060))
    svg_path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="1800" height="850" fill="white"/>
<g stroke="#111" stroke-width="7" fill="#e8eaed">
<rect x="395" y="650" width="1055" height="60" rx="20" fill="#c4c8cc"/>
<path d="M500 575H680L735 660H455Z"/><path d="M1170 575H1350L1400 660H1120Z"/>
<circle cx="510" cy="697" r="25" fill="white"/><circle cx="1335" cy="697" r="25" fill="white"/>
<rect x="480" y="210" width="910" height="380" rx="155"/>
<ellipse cx="540" cy="402.5" rx="150" ry="177.5" fill="#c4c8cc"/>
<ellipse cx="540" cy="402.5" rx="110" ry="132.5" fill="#f5f5f5"/>
<ellipse cx="540" cy="402.5" rx="40" ry="52.5" fill="#6f777d"/>
<rect x="175" y="375" width="335" height="55" rx="12" fill="#c4c8cc"/><rect x="120" y="387" width="65" height="31" fill="#6f777d"/>
<ellipse cx="1395" cy="402.5" rx="85" ry="177.5" fill="#c4c8cc"/>
<g stroke="#6f777d" stroke-width="9">{fins}</g>
<rect x="830" y="95" width="340" height="150" rx="28" fill="#c4c8cc"/><rect x="875" y="60" width="250" height="55"/>
{terminals}
</g>
<path d="M1512 453A120 120 0 1 1 1650 260" fill="none" stroke="#111" stroke-width="7"/>
<path d="M1636 245L1692 236L1660 286Z" fill="#111"/>
<text x="710" y="455" font-family="Times New Roman,serif" font-style="italic" font-size="120">M</text>
<text x="820" y="464" font-family="Arial,sans-serif" font-size="64">3~</text>
<text x="660" y="795" font-family="Times New Roman,serif" font-size="48">trojfázový asynchronní motor</text>
</svg>''',
        encoding="utf-8",
    )


def crop_characteristic(png_path: Path) -> None:
    """Vyrenderuje a přesně ořízne původní charakteristiku ze 3. stránky zadání."""
    with tempfile.TemporaryDirectory(prefix="zele3-characteristic-") as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [
                "pdftoppm", "-f", "3", "-l", "3", "-singlefile",
                "-r", "300", "-png", str(SOURCE_ASSIGNMENT), str(prefix),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        rendered = prefix.with_suffix(".png")
        with Image.open(rendered) as page:
            # Souřadnice přesného rámečku byly určeny na renderu 1406 × 1988 px.
            reference_size = (1406, 1988)
            reference_crop = (92, 568, 1365, 1100)
            sx = page.width / reference_size[0]
            sy = page.height / reference_size[1]
            box = tuple(round(value * (sx if index % 2 == 0 else sy)) for index, value in enumerate(reference_crop))
            crop = page.crop(box).convert("RGB")
            crop.save(png_path, dpi=(300, 300))


def make_assets() -> None:
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    draw_motor(GRAPHICS / "motor.png", GRAPHICS / "motor.svg")
    crop_characteristic(GRAPHICS / "momentova_charakteristika_original.png")


def gap() -> ET.Element:
    return math_r("                            ", plain=True)


def add_pair(
    out: list[ET.Element],
    eq_arch: ET.Element,
    result_arch: ET.Element,
    general: list[ET.Element],
    substitution: list[ET.Element],
    result: list[ET.Element],
) -> None:
    out.append(math_paragraph(eq_arch, general + [gap()] + substitution, keep_next=True))
    out.append(math_paragraph(result_arch, result, result=True))


def ratio(numerator: list[ET.Element], denominator: list[ET.Element]) -> ET.Element:
    return math_frac(numerator, denominator)


def cos_phi_n() -> list[ET.Element]:
    return [math_r("cos", plain=True), math_r("("), variable("φ", "n"), math_r(")")]


def build_body(body: ET.Element) -> list[ET.Element]:
    children = list(body)
    h, text, subheading = children[1], children[54], children[5]
    caption_arch, eq_arch, result_arch = children[16], children[17], children[20]
    image_arch, break_arch = children[13], children[14]
    out: list[ET.Element] = []

    out.append(heading(h, "ZADÁNÍ:"))
    out.append(body_text(text, "Trojfázový asynchronní motor pracuje při jmenovitém napětí Uₙ a jmenovité frekvenci fₙ. Ze zadaných štítkových a katalogových údajů určete synchronní otáčky nₛ, otáčky při zatížení polovinou jmenovitého momentu nₓ, jmenovitý moment, záběrný proud, záběrný moment a jmenovitou účinnost."))
    out.append(body_text(text, "Přiložená momentová charakteristika je pouze orientační. Hodnoty z ní nelze odměřovat; pro výpočet otáček při polovičním momentu se použije přibližně lineární pracovní oblast motoru."))
    out.append(heading(subheading, "Zadané hodnoty:"))
    out.append(inline_values(children[6], [
        [variable("U", "n"), math_r(" = 400 V", plain=True)],
        [variable("f", "n"), math_r(" = 50 Hz", plain=True)],
        [math_r("2p = 2", plain=True)],
    ]))
    out.append(inline_values(children[7], [
        [variable("P", "n"), math_r(" = 7200 W", plain=True)],
        [variable("n", "n"), math_r(" = 2951 min⁻¹", plain=True)],
        [variable("I", "n"), math_r(" = 13 A", plain=True)],
    ]))
    out.append(inline_values(children[6], [
        cos_phi_n() + [math_r(" = 0,88", plain=True)],
        [ratio([variable("M", "z")], [variable("M", "n")]), math_r(" = 2,1", plain=True)],
        [ratio([variable("I", "z")], [variable("I", "n")]), math_r(" = 9", plain=True)],
    ]))

    out.append(heading(h, "MOMENTOVÁ CHARAKTERISTIKA:"))
    out.append(body_text(text, "Náčrtek zachycuje obecný tvar momentové charakteristiky asynchronního motoru. Je pouze orientační a slouží k vymezení přibližně lineární běžné pracovní oblasti; žádná číselná hodnota se z něj neodečítá.", keep_next=True))
    out.append(set_drawing(image_arch, "rId8", 6.2, 2.59, "Orientační momentová charakteristika asynchronního motoru"))
    out.append(page_break(break_arch))

    out.append(heading(children[15], "VÝPOČTY:"))
    out.append(body_text(text, "Všechny zobrazené mezivýsledky se zaokrouhlují na tři desetinná místa a v této podobě se použijí v následujícím kroku."))

    out.append(caption(caption_arch, "Počet pólových dvojic:"))
    add_pair(
        out, eq_arch, result_arch,
        [variable("p"), math_r(" = "), ratio([math_r("2p", plain=True)], [math_r("2", plain=True)])],
        [variable("p"), math_r(" = "), ratio([math_r("2", plain=True)], [math_r("2", plain=True)])],
        [variable("p"), math_r(" = 1", plain=True)],
    )

    out.append(caption(caption_arch, "Synchronní otáčky motoru:"))
    add_pair(
        out, eq_arch, result_arch,
        [variable("n", "S"), math_r(" = "), ratio([math_r("60·"), variable("f", "n")], [variable("p")])],
        [variable("n", "S"), math_r(" = "), ratio([math_r("60·50", plain=True)], [math_r("1", plain=True)])],
        [variable("n", "S"), math_r(" = 3000,000 min⁻¹", plain=True)],
    )

    out.append(caption(caption_arch, "Jmenovitá účinnost motoru:"))
    add_pair(
        out, eq_arch, result_arch,
        [variable("η", "n"), math_r(" = "), ratio([variable("P", "n")], [math_rad([math_r("3", plain=True)]), math_r("·"), variable("U", "n"), math_r("·"), variable("I", "n"), math_r("·")] + cos_phi_n()), math_r("·100")],
        [variable("η", "n"), math_r(" = "), ratio([math_r("7200", plain=True)], [math_rad([math_r("3", plain=True)]), math_r("·400·13·0,88", plain=True)]), math_r("·100", plain=True)],
        [variable("η", "n"), math_r(" = 90,842 %", plain=True)],
    )

    out.append(caption(caption_arch, "Záběrný proud motoru:"))
    add_pair(
        out, eq_arch, result_arch,
        [variable("I", "z"), math_r(" = "), variable("I", "n"), math_r("·"), ratio([variable("I", "z")], [variable("I", "n")])],
        [variable("I", "z"), math_r(" = 13·9", plain=True)],
        [variable("I", "z"), math_r(" = 117,000 A", plain=True)],
    )

    out.append(caption(caption_arch, "Jmenovitý moment motoru:"))
    out.append(math_paragraph(
        eq_arch,
        [variable("M", "n"), math_r(" = "), ratio([variable("P", "n")], [math_r("2·π·"), ratio([variable("n", "n")], [math_r("60", plain=True)])]), math_r(" = "), ratio([variable("P", "n"), math_r("·60")], [math_r("2·π·"), variable("n", "n")])],
        keep_next=True,
    ))
    out.append(math_paragraph(eq_arch, [variable("M", "n"), math_r(" = "), ratio([math_r("7200·60", plain=True)], [math_r("2·π·2951", plain=True)])], keep_next=True))
    out.append(math_paragraph(result_arch, [variable("M", "n"), math_r(" = 23,299 N·m", plain=True)], result=True))

    out.append(caption(caption_arch, "Záběrný moment motoru:"))
    add_pair(
        out, eq_arch, result_arch,
        [variable("M", "z"), math_r(" = "), variable("M", "n"), math_r("·"), ratio([variable("M", "z")], [variable("M", "n")])],
        [variable("M", "z"), math_r(" = 23,299·2,1", plain=True)],
        [variable("M", "z"), math_r(" = 48,928 N·m", plain=True)],
    )

    out.append(caption(caption_arch, "Otáčky při polovině jmenovitého momentu:"))
    out.append(body_text(text, "V běžné pracovní oblasti je pokles otáček oproti synchronním otáčkám přibližně úměrný zatěžovacímu momentu."))
    out.append(math_paragraph(
        eq_arch,
        [ratio([variable("n", "S"), math_r(" − "), variable("n", "X")], [variable("M", "X")]), math_r(" = "), ratio([variable("n", "S"), math_r(" − "), variable("n", "n")], [variable("M", "n")])],
    ))
    out.append(body_text(text, "Protože Mₓ = 0,5Mₙ, je poměr Mₓ/Mₙ přesně 0,5."))
    add_pair(
        out, eq_arch, result_arch,
        [variable("n", "X"), math_r(" = "), variable("n", "S"), math_r(" − 0,5("), variable("n", "S"), math_r(" − "), variable("n", "n"), math_r(")")],
        [variable("n", "X"), math_r(" = 3000 − 0,5(3000 − 2951)", plain=True)],
        [variable("n", "X"), math_r(" = 2975,500 min⁻¹", plain=True)],
    )

    out.append(heading(h, "ZHODNOCENÍ:"))
    out.append(body_text(text, "Dvoupólovému asynchronnímu motoru napájenému frekvencí 50 Hz odpovídají synchronní otáčky nₛ = 3000,000 min⁻¹. Jmenovité otáčky 2951 min⁻¹ jsou nižší, protože motor při zatížení pracuje se skluzem."))
    out.append(body_text(text, "Při zatížení polovinou jmenovitého momentu vycházejí z lineární aproximace běžné pracovní oblasti otáčky nₓ = 2975,500 min⁻¹. Tato hodnota nebyla odečtena z orientačního náčrtku momentové charakteristiky."))
    out.append(body_text(text, "Jmenovitý moment motoru je Mₙ = 23,299 N·m. Záběrný proud 117,000 A je devítinásobkem jmenovitého proudu a záběrný moment 48,928 N·m je 2,1násobkem jmenovitého momentu. Jmenovitá účinnost vychází ηₙ = 90,842 %."))
    out.append(body_text(text, "Výsledky popisují idealizovaný teoretický výpočet z jmenovitých a katalogových údajů. Nebyly experimentálně ověřeny a nezohledňují toleranci parametrů, změnu napájecího napětí, zahřívání ani nelinearity skutečné momentové charakteristiky mimo běžnou pracovní oblast."))
    return out


def modify_title(table: ET.Element, body_children: list[ET.Element]) -> None:
    rows = table.findall(q("w", "tr"))
    for node in table.findall(f".//{q('w', 't')}"):
        if node.text == "SEMESTRÁLNÍ PROJEKT ZELE 1Z":
            node.text = "SEMESTRÁLNÍ PROJEKT ZELE 3Z"
        elif node.text == "1Z":
            node.text = "3Z"
        elif node.text == "Stejnosměrná zátěž napájená ze dvou reálných zdrojů":
            node.text = "Trojfázový asynchronní motor"

    scheme_cell = rows[6].findall(q("w", "tc"))[0]
    existing = scheme_cell.findall(q("w", "p"))
    heading_p = deepcopy(existing[0])
    drawing_source = next(p for p in existing if p.find(f".//{q('w', 'drawing')}") is not None)
    drawing_p = set_drawing(drawing_source, "rId7", 6.35, 3.00, "Trojfázový asynchronní motor")
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
            value_cell([variable("U", "n"), math_r(" = 400 V", plain=True)], 1700),
            value_cell([variable("f", "n"), math_r(" = 50 Hz", plain=True)], 1700),
            value_cell([math_r("2p = 2", plain=True)], 1700),
        ],
        [
            value_cell([variable("P", "n"), math_r(" = 7200 W", plain=True)]),
            value_cell([variable("n", "n"), math_r(" = 2951 min⁻¹", plain=True)]),
            value_cell([variable("I", "n"), math_r(" = 13 A", plain=True)]),
        ],
        [
            value_cell(cos_phi_n() + [math_r(" = 0,88", plain=True)]),
            value_cell([ratio([variable("M", "z")], [variable("M", "n")]), math_r(" = 2,1", plain=True)]),
            value_cell([ratio([variable("I", "z")], [variable("I", "n")]), math_r(" = 9", plain=True)]),
        ],
    ], [3400, 3400, 3449])
    trailing = w("p")
    trailing_props = ET.SubElement(trailing, q("w", "pPr"))
    ET.SubElement(trailing_props, q("w", "spacing"), {
        q("w", "before"): "0", q("w", "after"): "0", q("w", "line"): "1", q("w", "lineRule"): "exact",
    })
    replace_cell_content(scheme_cell, [heading_p, fixed_spacer(260), drawing_p, values, trailing])


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
        core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Semestrální projekt ZELE 3Z</dc:title>", core, flags=re.DOTALL)
        core = re.sub(r"<dc:subject>.*?</dc:subject>", "<dc:subject>Trojfázový asynchronní motor</dc:subject>", core, flags=re.DOTALL)
        replacements = {
            "word/document.xml": ET.tostring(root, encoding="utf-8", xml_declaration=True),
            "docProps/core.xml": core.encode("utf-8"),
            "word/media/image1.png": (GRAPHICS / "motor.png").read_bytes(),
            "word/media/image2.png": (GRAPHICS / "momentova_charakteristika_original.png").read_bytes(),
        }
        with tempfile.NamedTemporaryFile(dir=OUTPUT, suffix=".docx", delete=False) as temp:
            temp_path = Path(temp.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    zout.writestr(item, replacements.get(item.filename, zin.read(item.filename)))
            temp_path.replace(DOCX_OUT)
            DOCX_OUT.chmod(0o664)
        finally:
            if temp_path.exists():
                temp_path.unlink()


def write_audit() -> None:
    U_n, f_n, poles = 400.0, 50.0, 2.0
    P_n, n_n, I_n = 7200.0, 2951.0, 13.0
    cos_phi_n_value, moment_ratio, current_ratio = 0.88, 2.1, 9.0
    p = poles / 2
    n_s = 60 * f_n / p
    eta = P_n / (math.sqrt(3) * U_n * I_n * cos_phi_n_value) * 100
    i_z = I_n * current_ratio
    m_n = P_n * 60 / (2 * math.pi * n_n)
    m_n_rounded = round(m_n, 3)
    m_z = m_n_rounded * moment_ratio
    n_x = n_s - 0.5 * (n_s - n_n)
    text = f"""Kontrola výpočtu ZELE 3Z

Přesné hodnoty:
nS = {n_s:.12f} min⁻¹
eta_n = {eta:.12f} %
I_z = {i_z:.12f} A
Mn = {m_n:.12f} N·m
M_z z průběžně zaokrouhleného M_n = {m_z:.12f} N·m
nX = {n_x:.12f} min⁻¹

Zobrazené hodnoty při průběžném zaokrouhlování:
nS = 3000,000 min⁻¹
nX = 2975,500 min⁻¹
Mn = 23,299 N·m
I_z = 117,000 A
M_z = 48,928 N·m
eta_n = 90,842 %

Použitý vzor:
Příklad 24 – hlavní postup.
Příklad 25 – lineární pracovní oblast pro nX.
"""
    (WORK / "kontrola_vypoctu.txt").write_text(text, encoding="utf-8")


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
