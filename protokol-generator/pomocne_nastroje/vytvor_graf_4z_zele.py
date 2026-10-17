#!/usr/bin/env python3
"""Vytvoří editovatelný XLSX graf P(f) pro protokol ZELE 4Z přes LibreOffice UNO."""

from __future__ import annotations

import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

import uno
from com.sun.star.awt import Rectangle, Size


def property_value(name: str, value: object):
    item = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
    item.Name = name
    item.Value = value
    return item


def connect_office(port: int = 20984):
    profile = Path(tempfile.mkdtemp(prefix="zele4_calc_"))
    command = [
        "libreoffice",
        f"-env:UserInstallation={uno.systemPathToFileUrl(str(profile))}",
        "--headless",
        "--nologo",
        "--nodefault",
        "--nofirststartwizard",
        f"--accept=socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext",
    ]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    for _ in range(80):
        try:
            context = resolver.resolve(
                f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext"
            )
            return context, process, profile
        except Exception:
            if process.poll() is not None:
                raise RuntimeError("LibreOffice se při vytváření XLSX předčasně ukončil")
            time.sleep(0.25)
    process.terminate()
    process.wait(timeout=10)
    shutil.rmtree(profile, ignore_errors=True)
    raise RuntimeError("Nepodařilo se připojit k LibreOffice UNO")


def set_text(cell, text: str, *, bold: bool = False, background: int | None = None) -> None:
    cell.String = text
    cell.CharFontName = "Arial"
    cell.CharHeight = 10
    if bold:
        cell.CharWeight = 150
    if background is not None:
        cell.CellBackColor = background


def set_number(cell, value: float, number_format: int) -> None:
    cell.Value = value
    cell.CharFontName = "Arial"
    cell.CharHeight = 10
    cell.NumberFormat = number_format


def get_number_format(document, code: str = "0,000") -> int:
    locale = uno.createUnoStruct("com.sun.star.lang.Locale")
    locale.Language = "cs"
    locale.Country = "CZ"
    formats = document.NumberFormats
    key = formats.queryKey(code, locale, True)
    if key == -1:
        key = formats.addNew(code, locale)
    return key


def style_sheet(sheet, widths: tuple[int, ...]) -> None:
    for index, width in enumerate(widths):
        sheet.Columns.getByIndex(index).Width = width
    sheet.Rows.getByIndex(0).Height = 700


def create_workbook(document) -> tuple[object, object]:
    three_decimals = get_number_format(document)
    sheets = document.Sheets
    data = sheets.getByIndex(0)
    data.Name = "Data"
    sheets.insertNewByName("Výpočty", 1)
    sheets.insertNewByName("Graf", 2)
    calculations = sheets.getByName("Výpočty")
    graph = sheets.getByName("Graf")

    headers = ("Veličina", "Hodnota", "Jednotka", "Význam")
    for column, value in enumerate(headers):
        set_text(data.getCellByPosition(column, 0), value, bold=True, background=0xD9EAD3)
    inputs = [
        ("U", 35.0, "V", "Efektivní hodnota napájecího napětí"),
        ("L₁", 0.036, "H", "Indukčnost první cívky"),
        ("R₁", 32.0, "Ω", "Odpor první cívky"),
        ("L₂", 0.041, "H", "Indukčnost druhé cívky"),
        ("R₂", 24.0, "Ω", "Odpor druhé cívky"),
        ("P", 2.1, "W", "Požadovaný činný výkon"),
        ("Δf", 5.0, "Hz", "Základní krok dat grafu"),
        ("fₘₐₓ", 600.0, "Hz", "Horní mez grafu"),
    ]
    for row, (symbol, value, unit, meaning) in enumerate(inputs, 1):
        set_text(data.getCellByPosition(0, row), symbol, bold=True)
        set_number(data.getCellByPosition(1, row), value, three_decimals)
        set_text(data.getCellByPosition(2, row), unit)
        set_text(data.getCellByPosition(3, row), meaning)
    style_sheet(data, (2500, 2600, 2200, 9000))

    calc_headers = ("Veličina", "Vzorec / hodnota", "Jednotka", "Poznámka")
    for column, value in enumerate(calc_headers):
        set_text(calculations.getCellByPosition(column, 0), value, bold=True, background=0xD9EAD3)
    calculation_rows = [
        ("R", "=Data.B4+Data.B6", "Ω", "Celkový sériový odpor"),
        ("L", "=Data.B3+Data.B5", "H", "Celková indukčnost"),
        ("I – přesně", "=SQRT(Data.B7/B2)", "A", "Proud bez průběžného zaokrouhlení"),
        ("f – přesně", "=SQRT(Data.B2^2*B2/Data.B7-B2^2)/(2*PI()*B3)", "Hz", "Přesný průsečík P(f)=2,1 W"),
        ("R – zaokr.", "=ROUND(Data.B4+Data.B6;3)", "Ω", "Průběžně zaokrouhlený odpor"),
        ("L – zaokr.", "=ROUND(ROUND((Data.B3+Data.B5)*1000;3)/1000;3)", "H", "Průběžně zaokrouhlená indukčnost"),
        ("I – zaokr.", "=ROUND(SQRT(Data.B7/B6);3)", "A", "Výsledek použitý v protokolu"),
        ("U_R", "=ROUND(B8*B6;3)", "V", "Napětí na odporové části"),
        ("U_L", "=ROUND(SQRT(Data.B2^2-B9^2);3)", "V", "Napětí na induktivní části"),
        ("X_L", "=ROUND(B10/B8;3)", "Ω", "Induktivní reaktance"),
        ("f – protokol", "=ROUND(B11/(2*PI()*B7);3)", "Hz", "Průběžně zaokrouhlený výsledek"),
        ("P při f protokolu", "=Data.B2^2*B6/(B6^2+(2*PI()*B12*B7)^2)", "W", "Kontrolní výkon 2,108 W"),
    ]
    for row, (symbol, formula, unit, note) in enumerate(calculation_rows, 1):
        set_text(calculations.getCellByPosition(0, row), symbol, bold=True)
        calculations.getCellByPosition(1, row).Formula = formula
        calculations.getCellByPosition(1, row).CharFontName = "Arial"
        calculations.getCellByPosition(1, row).CharHeight = 10
        calculations.getCellByPosition(1, row).NumberFormat = three_decimals
        set_text(calculations.getCellByPosition(2, row), unit)
        set_text(calculations.getCellByPosition(3, row), note)
    style_sheet(calculations, (3700, 3800, 2200, 9000))

    graph_headers = (
        "f [Hz]",
        "P(f) [W]",
        "P požadovaný = 2,100 W",
        "Přesný: 355,194 Hz; 2,100 W",
        "Protokol: 354,481 Hz; 2,108 W",
    )
    for column, value in enumerate(graph_headers):
        set_text(graph.getCellByPosition(column, 0), value, bold=True, background=0xD9EAD3)

    frequencies = [float(value) for value in range(0, 601, 5)]
    frequencies.extend((354.481, 355.194336348))
    frequencies = sorted(set(frequencies))
    exact_frequency = 355.194336348
    rounded_frequency = 354.481
    for row, frequency in enumerate(frequencies, 1):
        set_number(graph.getCellByPosition(0, row), frequency, three_decimals)
        excel_row = row + 1
        graph.getCellByPosition(1, row).Formula = (
            f"=Data.B2^2*(Data.B4+Data.B6)/((Data.B4+Data.B6)^2+"
            f"(2*PI()*A{excel_row}*(Data.B3+Data.B5))^2)"
        )
        graph.getCellByPosition(1, row).NumberFormat = three_decimals
        graph.getCellByPosition(2, row).Formula = "=Data.B7"
        graph.getCellByPosition(2, row).NumberFormat = three_decimals
        if math.isclose(frequency, exact_frequency, abs_tol=1e-9):
            graph.getCellByPosition(3, row).Formula = f"=B{excel_row}"
            graph.getCellByPosition(3, row).NumberFormat = three_decimals
        if math.isclose(frequency, rounded_frequency, abs_tol=1e-9):
            graph.getCellByPosition(4, row).Formula = f"=B{excel_row}"
            graph.getCellByPosition(4, row).NumberFormat = three_decimals
    style_sheet(graph, (2500, 3000, 5400, 8500, 9000))
    document.calculateAll()
    return graph, frequencies


def create_chart(document, graph_sheet, point_count: int):
    rectangle = Rectangle()
    rectangle.X = 900
    rectangle.Y = 800
    rectangle.Width = 17000
    rectangle.Height = 14200
    data_range = graph_sheet.getCellRangeByName(f"A1:E{point_count + 1}").RangeAddress
    charts = graph_sheet.Charts
    charts.addNewByName("Graf_P_f", rectangle, (data_range,), True, True)
    chart = charts.getByName("Graf_P_f").EmbeddedObject
    diagram = chart.createInstance("com.sun.star.chart.XYDiagram")
    chart.Diagram = diagram
    chart.HasMainTitle = True
    chart.Title.String = "ZÁVISLOST ČINNÉHO VÝKONU NA FREKVENCI"
    chart.Title.CharFontName = "Arial"
    chart.Title.CharWeight = 150
    chart.Title.CharHeight = 14
    chart.HasLegend = True
    chart.Legend.Alignment = uno.Enum("com.sun.star.chart.ChartLegendPosition", "BOTTOM")
    chart.Legend.CharFontName = "Arial"
    chart.Legend.CharHeight = 9
    chart.Area.FillColor = 0xFFFFFF

    diagram.Lines = True
    diagram.SplineType = 1
    diagram.SplineOrder = 3
    diagram.SplineResolution = 20
    diagram.Wall.FillColor = 0xFFFFFF
    diagram.HasXAxisTitle = True
    diagram.XAxisTitle.String = "f [Hz]"
    diagram.XAxisTitle.CharFontName = "Arial"
    diagram.XAxisTitle.CharWeight = 150
    diagram.XAxisTitle.CharHeight = 10
    diagram.HasYAxisTitle = True
    diagram.YAxisTitle.String = "P [W]"
    diagram.YAxisTitle.CharFontName = "Arial"
    diagram.YAxisTitle.CharWeight = 150
    diagram.YAxisTitle.CharHeight = 10

    diagram.XAxis.AutoMin = False
    diagram.XAxis.Min = 0.0
    diagram.XAxis.AutoMax = False
    diagram.XAxis.Max = 600.0
    diagram.XAxis.AutoStepMain = False
    diagram.XAxis.StepMain = 100.0
    diagram.XAxis.LinkNumberFormatToSource = False
    diagram.XAxis.NumberFormat = get_number_format(document, "0")
    diagram.YAxis.AutoMin = False
    diagram.YAxis.Min = 0.0
    diagram.YAxis.AutoMax = False
    diagram.YAxis.Max = 25.0
    diagram.YAxis.AutoStepMain = False
    diagram.YAxis.StepMain = 5.0
    diagram.YAxis.LinkNumberFormatToSource = False
    diagram.YAxis.NumberFormat = get_number_format(document, "0")
    for axis in (diagram.XAxis, diagram.YAxis):
        axis.CharFontName = "Arial"
        axis.CharHeight = 8
        axis.LineColor = 0x333333
    diagram.HasXAxisGrid = True
    diagram.HasYAxisGrid = True
    diagram.XMainGrid.LineColor = 0x6B8E6B
    diagram.YMainGrid.LineColor = 0x6B8E6B

    # Řady: P(f), požadovaný výkon, přesný bod, výsledek protokolu.
    styles = [
        (0x2F6B3B, 55, -3, 0x2F6B3B, 0),
        (0xB36B25, 45, -3, 0xB36B25, 0),
        (0x1F4E79, 0, 3, 0x1F4E79, 260),
        (0xC00000, 0, 1, 0xC00000, 300),
    ]
    # Index 0 patří společným hodnotám osy x; čtyři datové řady začínají indexem 1.
    for index, (line_color, line_width, symbol, symbol_color, symbol_size) in enumerate(styles, 1):
        series = diagram.getDataRowProperties(index)
        series.LineColor = line_color
        if line_width:
            series.LineWidth = line_width
        else:
            series.LineStyle = 0
        series.SymbolType = symbol
        series.FillColor = symbol_color
        series.LineColor = symbol_color if not line_width else line_color
        if symbol_size:
            series.SymbolSize = Size(symbol_size, symbol_size)
    return graph_sheet.DrawPage.getByIndex(0)


def export_chart(context, shape, png_path: Path) -> None:
    exporter = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.drawing.GraphicExportFilter", context
    )
    exporter.setSourceDocument(shape)
    ok = exporter.filter((
        property_value("URL", uno.systemPathToFileUrl(str(png_path.resolve()))),
        property_value("MediaType", "image/png"),
    ))
    if not ok or not png_path.exists():
        raise RuntimeError("Nepodařilo se exportovat náhled grafu z XLSX")


def create_graph(xlsx_path: Path, png_path: Path) -> None:
    xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    context, process, profile = connect_office()
    document = None
    try:
        desktop = context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context
        )
        document = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, ())
        graph_sheet, frequencies = create_workbook(document)
        shape = create_chart(document, graph_sheet, len(frequencies))
        document.calculateAll()
        document.storeAsURL(
            uno.systemPathToFileUrl(str(xlsx_path.resolve())),
            (
                property_value("FilterName", "Calc MS Excel 2007 XML"),
                property_value("Overwrite", True),
            ),
        )
        export_chart(context, shape, png_path)
    finally:
        if document is not None:
            document.close(True)
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        shutil.rmtree(profile, ignore_errors=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "4Z-zele-4" / "vystup"
    create_graph(output / "graf_P_f.xlsx", output / "grafika" / "graf_P_f.png")
    print(output / "graf_P_f.xlsx")


if __name__ == "__main__":
    main()
