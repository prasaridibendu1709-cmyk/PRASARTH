"""Builds the printable plan PDF in English, Hindi or Bengali (uses fpdf2)."""
from __future__ import annotations

import io
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

import engine
import i18n

BASE = Path(__file__).parent
FONT_DIR = BASE / "fonts"
LOGO = BASE / "assets" / "logo.png"
FONT_PREFIX = {"en": "NotoSans", "hi": "NotoSansDevanagari", "bn": "NotoSansBengali"}

GREEN = (27, 127, 75)
DARK = (15, 81, 50)
LIGHT_GREEN = (232, 245, 238)
RATING_FILL = {"low": (254, 226, 226), "medium": (254, 243, 199), "high": (220, 252, 231)}


class MissingFontError(Exception):
    """Raised when the Noto font files are not in the fonts/ folder."""


def _find_font(prefix: str) -> Path | None:
    for pattern in (f"{prefix}-Regular.ttf", f"{prefix}-*Regular*.ttf", f"{prefix}[[]*.ttf", f"{prefix}-VariableFont*.ttf"):
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
        raise MissingFontError("Missing font file(s) in the 'fonts' folder: " + ", ".join(missing))
    pdf.add_font("main", "", str(main))
    if lang != "en":
        pdf.add_font("latin", "", str(latin))  # Latin letters, digits and the rupee sign
        pdf.set_fallback_fonts(["latin"])
    pdf.set_text_shaping(True)  # needed for Hindi / Bengali conjuncts


def _section(pdf: _PDF, text: str) -> None:
    if pdf.get_y() > 255:
        pdf.add_page()
    pdf.ln(3)
    pdf.set_font("main", size=12)
    pdf.set_fill_color(*LIGHT_GREEN)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 8, "  " + text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(1.5)


def _table(pdf: _PDF, widths, rows, header=None, fills=None, size=10) -> None:
    pdf.set_font("main", size=size)
    fills = fills or {}
    with pdf.table(
        col_widths=widths, line_height=6.2, text_align="LEFT",
        headings_style=FontFace(color=(255, 255, 255), fill_color=GREEN),
        borders_layout="ALL", first_row_as_headings=header is not None,
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


def _rupees(x: float) -> str:
    return "-" if x < 0.5 else f"{round(x):,}"


def build_pdf(report: dict, lang: str) -> bytes:
    ui = i18n.UI[lang]
    pn = i18n.PRODUCT_NAMES[lang]
    crop, plan = report["crop"], report["plan"]

    pdf = _PDF(format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(True, margin=16)
    _setup_fonts(pdf, lang)
    pdf.footer_text = f"{ui['app_name']} - {i18n.ORG_NAME}"
    pdf.add_page()

    # ---- header band with logo ------------------------------------------------
    pdf.set_fill_color(*DARK)
    pdf.rect(0, 0, 210, 30, style="F")
    x_text = 12
    if LOGO.exists():
        try:
            pdf.set_fill_color(255, 255, 255)
            pdf.rect(10, 5, 22, 20, style="F")
            pdf.image(str(LOGO), x=11, y=6, h=18)
            x_text = 36
        except Exception:
            x_text = 12
    pdf.set_xy(x_text, 6)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("main", size=19)
    pdf.cell(0, 9, ui["pdf_title"], new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.set_x(x_text)
    pdf.set_font("main", size=10)
    pdf.cell(0, 6, f"{ui['app_name']}  |  {ui['org_line']}", new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.set_text_color(30, 30, 30)
    pdf.set_y(34)

    # ---- farmer ---------------------------------------------------------------
    rows = [(ui["farmer_name"], report["farmer"])]
    if report.get("mobile"):
        rows.append((ui["mobile"], report["mobile"]))
    rows.append((ui["village"] + " / " + ui["block"], " / ".join(x for x in (report["village"], report["block"]) if x) or "-"))
    if report.get("plot"):
        rows.append((ui["plot"], report["plot"]))
    rows.append((ui["scan_date"], report["test_date"].strftime("%d-%m-%Y")))
    if report.get("scan_id"):
        rows.append((ui["scan_id"].split(" (")[0], report["scan_id"]))
    rows.append((ui["pdf_advice_date"], report["today"].strftime("%d-%m-%Y")))
    _table(pdf, (62, 124), rows)

    # ---- place ----------------------------------------------------------------
    _section(pdf, ui["pdf_place"])
    zone = engine.ZONES[report["zone"]]
    state_name = i18n.STATE_NAMES[lang][report["state"]]
    place_rows = [
        (ui["state"] + " / " + ui["district"], f"{state_name} / {report['district']}"),
        (ui["zone_label"], i18n.ZONE_NAMES[lang][report["zone"]]),
        (ui["rain_label"], zone["rain"]),
        (ui["ph_typ"], zone["ph"] or ui["ph_unknown"]),
    ]
    _table(pdf, (62, 124), place_rows)

    # ---- soil -----------------------------------------------------------------
    _section(pdf, ui["pdf_soil"])
    soil_rows, fills = [], {}
    for key in ("n", "oc", "clay", "k", "p", "cec"):
        if key not in report["soil"]:
            continue
        lo, hi = report["soil"][key]
        rating = report["ratings"].get(key)
        if rating:
            rating_text = ui["r_" + rating]
            fills[(len(soil_rows), 2)] = FontFace(fill_color=RATING_FILL[rating])
        else:
            rating_text = (report.get("texture") or "-") if key == "clay" else "-"
        soil_rows.append((ui["p_" + key], _range_text(lo, hi), rating_text))
    if report.get("ph") is not None:
        soil_rows.append(("pH", _g(report["ph"]), "-"))
    _table(pdf, (80, 55, 51), soil_rows, header=(ui["col_param"], ui["col_value"], ui["col_rating"]), fills=fills)

    # ---- crop -----------------------------------------------------------------
    _section(pdf, ui["pdf_crop"])
    d = plan["dose_ha"]
    crop_rows = [
        (ui["crop"], crop["names"][lang]),
        (ui["season"], ui["season_" + report["season"]]),
        (ui["area"], f"{_g(report['area'])} {ui['unit_' + report['unit']]}"),
        (ui["approach"], ui["ap_" + plan["approach"]].lstrip("🧪🌗🌿🐄 ")),
        (ui["pdf_dose"], f"N {d['n']:.0f}  |  P2O5 {d['p']:.0f}  |  K2O {d['k']:.0f}"),
    ]
    _table(pdf, (80, 106), crop_rows)

    # ---- shopping list --------------------------------------------------------
    _section(pdf, ui["pdf_buy"])
    order = ["fym", "urea", "dap", "mop", "oilcake", "rockp", "bonem", "ash", "lime", "gjm", "jeev",
             "wsf192", "mkp", "kno3", "cano3", "borax", "znso4", "micro", "dap2", "urea2", "jeevs", "panch", "vwash"]
    buy_rows = []
    for key in order:
        q = plan["all_totals"].get(key, 0)
        if q <= 0:
            continue
        price = engine.PRODUCTS[key]["price"]
        buy_rows.append((pn[key], engine.fmt_qty(key, q), engine.bags_text(key, q), _rupees(price * q)))
    buy_rows.append((ui["total_cost"], "", "", _rupees(plan["cost"])))
    last = len(buy_rows) - 1
    total_fill = {(last, j): FontFace(fill_color=LIGHT_GREEN) for j in range(4)}
    _table(pdf, (86, 40, 24, 36), buy_rows,
           header=(ui["col_product"], ui["col_qty"], ui["col_bags"], ui["col_cost"]), fills=total_fill)
    pdf.set_font("main", size=8)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(0, 4.5, ui["cost_note"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(30, 30, 30)

    if plan.get("coverage") and plan["approach"] == "organic":
        c = plan["coverage"]
        pdf.ln(1)
        pdf.set_font("main", size=10)
        pdf.multi_cell(0, 5.5, f"{ui['cov_title']}:  {ui['cov_n']} {c['n']:.0f}%  |  {ui['cov_p']} {c['p']:.0f}%  |  {ui['cov_k']} {c['k']:.0f}%",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---- schedule -------------------------------------------------------------
    _section(pdf, ui["pdf_when"])
    sched_rows = []
    for st in plan["stages"]:
        if not st["items"]:
            continue
        when = ui["when_basal"] if st["days"] == 0 else ui["when_days"].format(d=st["days"])
        for i, (key, q) in enumerate(st["items"]):
            sched_rows.append((when if i == 0 else "", pn[key], engine.fmt_qty(key, q)))
    _table(pdf, (62, 84, 40), sched_rows, header=(ui["col_when"], ui["col_product"], ui["col_qty"]))

    # ---- sprays ---------------------------------------------------------------
    _section(pdf, ui["pdf_spray"])
    if plan["sprays"]:
        sp_rows = []
        for sp in plan["sprays"]:
            name = pn[sp["product"]] + (("  " + ui[sp["extra"]]) if sp["extra"] else "")
            sp_rows.append((
                ui["stg_" + sp["stage"]], name,
                f"{_g(sp['per_pump'])} {sp['unit']}",
                f"{engine.fmt_qty(sp['product'], sp['total_qty'])}  ({sp['pumps']} {ui['sp_pumps']})",
            ))
        _table(pdf, (44, 66, 34, 42), sp_rows, header=(ui["sp_stage"], ui["sp_product"], ui["sp_pump"], ui["sp_total"]), size=9)
    else:
        pdf.set_font("main", size=10)
        pdf.cell(0, 6, ui["sp_none"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---- advice ---------------------------------------------------------------
    _section(pdf, ui["pdf_advice"])
    pdf.set_font("main", size=10)
    for line in i18n.render_advice(lang, report["advice_items"], crop):
        if pdf.get_y() > 265:
            pdf.add_page()
            pdf.set_font("main", size=10)
        pdf.set_x(14)
        pdf.multi_cell(0, 5.8, "•  " + line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    # ---- signatures + disclaimer ------------------------------------------------
    if pdf.get_y() > 235:
        pdf.add_page()
    pdf.ln(6)
    pdf.set_font("main", size=10)
    y = pdf.get_y()
    pdf.line(14, y + 12, 90, y + 12)
    pdf.line(120, y + 12, 196, y + 12)
    pdf.set_xy(14, y + 13)
    pdf.cell(76, 5, f"{ui['sign_prepared']}: {report.get('prepared_by') or ''}")
    pdf.set_xy(120, y + 13)
    pdf.cell(76, 5, ui["sign_farmer"])
    if report.get("shg"):
        pdf.set_xy(14, y + 19)
        pdf.cell(76, 5, report["shg"])
    pdf.set_y(y + 27)
    pdf.set_font("main", size=8.5)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(0, 4.8, ui["disclaimer"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---- photo of the original report ------------------------------------------------
    if report.get("photo"):
        pdf.add_page()
        _section(pdf, ui["pdf_photo"])
        pdf.image(_compress_photo(report["photo"]), x=30, w=150)

    return bytes(pdf.output())
