"""Builds the advice sheet PDF in English, Hindi or Bengali (uses fpdf2)."""
from __future__ import annotations

import io
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

import engine
import i18n

FONT_DIR = Path(__file__).with_name("fonts")
FONT_PREFIX = {"en": "NotoSans", "hi": "NotoSansDevanagari", "bn": "NotoSansBengali"}

GREEN = (27, 127, 75)
LIGHT_GREEN = (232, 245, 238)
RATING_FILL = {"low": (254, 226, 226), "medium": (254, 243, 199), "high": (220, 252, 231)}


class MissingFontError(Exception):
    """Raised when the Noto font files are not in the fonts/ folder."""


def _find_font(prefix: str) -> Path | None:
    for pattern in (
        f"{prefix}-Regular.ttf",
        f"{prefix}-*Regular*.ttf",
        f"{prefix}[[]*.ttf",
        f"{prefix}-VariableFont*.ttf",
    ):
        hits = sorted(FONT_DIR.glob(pattern))
        if hits:
            return hits[0]
    return None


class _PDF(FPDF):
    footer_text = ""

    def footer(self):
        self.set_y(-12)
        self.set_font("main", size=8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, f"{self.footer_text}   |   {self.page_no()}", align="C")


def _setup_fonts(pdf: _PDF, lang: str) -> None:
    main = _find_font(FONT_PREFIX[lang])
    latin = _find_font(FONT_PREFIX["en"])
    missing = []
    if main is None:
        missing.append(f"{FONT_PREFIX[lang]}-Regular.ttf")
    if latin is None and lang != "en":
        missing.append(f"{FONT_PREFIX['en']}-Regular.ttf")
    if missing:
        raise MissingFontError(
            "Missing font file(s) in the 'fonts' folder: " + ", ".join(missing)
        )
    pdf.add_font("main", "", str(main))
    if lang != "en":
        # Latin letters (DAP, MOP, KVK, numbers) come from Noto Sans.
        pdf.add_font("latin", "", str(latin))
        pdf.set_fallback_fonts(["latin"])
    pdf.set_text_shaping(True)  # needed for Hindi / Bengali conjuncts


def _section(pdf: _PDF, text: str) -> None:
    pdf.ln(3)
    pdf.set_font("main", size=12)
    pdf.set_fill_color(*LIGHT_GREEN)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 8, "  " + text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(1.5)


def _table(pdf: _PDF, widths, rows, header=None, fills=None, aligns=None) -> None:
    pdf.set_font("main", size=10)
    fills = fills or {}
    with pdf.table(
        col_widths=widths,
        line_height=6.5,
        text_align=aligns or "LEFT",
        headings_style=FontFace(color=(255, 255, 255), fill_color=GREEN),
        borders_layout="ALL",
        first_row_as_headings=header is not None,
    ) as table:
        if header is not None:
            row = table.row()
            for h in header:
                row.cell(h)
        for i, r in enumerate(rows):
            row = table.row()
            for j, value in enumerate(r):
                style = fills.get((i, j))
                row.cell(str(value), style=style) if style else row.cell(str(value))


def _g(x: float) -> str:
    return f"{x:g}"


def _range_text(lo: float, hi: float) -> str:
    return _g(lo) if lo == hi else f"{_g(lo)} - {_g(hi)}"


def _compress_photo(raw: bytes) -> io.BytesIO:
    from PIL import Image, ImageOps

    img = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
    img.thumbnail((1100, 1100))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=70)
    buf.seek(0)
    return buf


def build_pdf(report: dict, lang: str) -> bytes:
    """report keys: farmer, village, block, test_date (date), scan_id, soil,
    texture, ratings, crop (row from crops.csv), season, area, unit, rec,
    advice_items, photo (bytes or None), today (date)."""
    ui = i18n.UI[lang]
    crop = report["crop"]
    rec = report["rec"]

    pdf = _PDF(format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(True, margin=16)
    _setup_fonts(pdf, lang)
    pdf.footer_text = "ScaNxt BhuParikshak"
    pdf.add_page()

    # Title bar
    pdf.set_font("main", size=18)
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, ui["pdf_title"], fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(3)

    # Farmer details
    rows = [
        (ui["farmer_name"], report["farmer"]),
        (ui["village"], report["village"] or "-"),
        (ui["block"], report["block"] or "-"),
        (ui["scan_date"], report["test_date"].strftime("%d-%m-%Y")),
    ]
    if report.get("scan_id"):
        rows.append((ui["scan_id"].split(" (")[0], report["scan_id"]))
    rows.append((ui["pdf_advice_date"], report["today"].strftime("%d-%m-%Y")))
    _table(pdf, (55, 131), rows)

    # Soil test result
    _section(pdf, ui["pdf_soil"])
    soil_rows, fills = [], {}
    for key in ("n", "oc", "clay", "k", "p", "cec"):
        if key not in report["soil"]:  # clay / CEC are optional
            continue
        lo, hi = report["soil"][key]
        rating = report["ratings"].get(key)
        if rating:
            rating_text = ui["r_" + rating]
            fills[(len(soil_rows), 2)] = FontFace(fill_color=RATING_FILL[rating])
        else:
            rating_text = report.get("texture") or "-" if key == "clay" else "-"
        soil_rows.append((ui["p_" + key], _range_text(lo, hi), rating_text))
    _table(pdf, (80, 55, 51), soil_rows, header=(ui["col_param"], ui["col_value"], ui["col_rating"]), fills=fills)

    # Crop and land
    _section(pdf, ui["pdf_crop"])
    area_text = f"{_g(report['area'])} {ui['unit_' + report['unit']]}"
    d = rec["dose_ha"]
    crop_rows = [
        (ui["crop"], crop["names"][lang]),
        (ui["season"], ui["season_" + report["season"]]),
        (ui["area"], area_text),
        (ui["pdf_dose"], f"N {d['n']:.0f}  |  P2O5 {d['p']:.0f}  |  K2O {d['k']:.0f}"),
    ]
    _table(pdf, (80, 106), crop_rows)

    # Fertiliser schedule
    _section(pdf, ui["pdf_fert"])
    sched_rows = []
    for step in rec["schedule"]:
        when = ui["when_basal"] if step["days"] == 0 else ui["when_days"].format(d=step["days"])
        sched_rows.append(
            (
                when,
                engine.fmt_amount(step["fym"]),
                engine.fmt_amount(step["dap"]),
                engine.fmt_amount(step["mop"]),
                engine.fmt_amount(step["urea"]),
            )
        )
    t = rec["totals"]
    sched_rows.append(
        (
            ui["row_total"],
            engine.fmt_amount(t["fym"]),
            engine.fmt_amount(t["dap"]),
            engine.fmt_amount(t["mop"]),
            engine.fmt_amount(t["urea"]),
        )
    )
    last = len(sched_rows) - 1
    total_fill = {(last, j): FontFace(fill_color=LIGHT_GREEN) for j in range(5)}
    _table(
        pdf,
        (56, 32, 30, 32, 36),
        sched_rows,
        header=(ui["col_when"], ui["col_fym"], ui["col_dap"], ui["col_mop"], ui["col_urea"]),
        fills=total_fill,
    )

    # Special advice
    _section(pdf, ui["pdf_advice"])
    pdf.set_font("main", size=10)
    for line in i18n.render_advice(lang, report["advice_items"], crop):
        pdf.set_x(14)
        pdf.multi_cell(0, 5.8, "•  " + line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    # Disclaimer
    pdf.ln(2)
    pdf.set_font("main", size=8.5)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(0, 4.8, ui["disclaimer"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Photo of the original report
    if report.get("photo"):
        pdf.add_page()
        _section(pdf, ui["pdf_photo"])
        pdf.image(_compress_photo(report["photo"]), x=30, w=150)

    return bytes(pdf.output())
