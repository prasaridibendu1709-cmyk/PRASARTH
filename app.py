"""Soil test -> fertiliser advice app (English / Hindi / Bengali).

Run locally:  streamlit run app.py
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import re

import streamlit as st

import engine
import i18n
from pdf_report import MissingFontError, build_pdf

st.set_page_config(page_title="Soil → Fertiliser Advice", page_icon="🌱", layout="centered")

SOIL_FIELDS = ["n", "oc", "clay", "k", "p", "cec"]
API_NAME = {
    "n": "nitrogen",
    "oc": "organic_carbon",
    "clay": "clay",
    "k": "potassium",
    "p": "phosphorus",
    "cec": "cec",
}
EXTRACT_PROMPT = """You are reading a photo or screenshot of the result screen of a ScaNxt BhuParikshak soil testing device.
Return ONLY a JSON object with these keys:
  "scan_date": the Scan Date as YYYY-MM-DD (it is printed like 2026-Mar-18:16:58:39, i.e. year-month-day:time), or null
  "scan_id": the Scan ID text, or null
  "texture": the soil texture label shown next to Clay (for example "Clay Loam"), or null
  "nitrogen", "organic_carbon", "clay", "potassium", "phosphorus", "cec": each an object {"min": number, "max": number}
The Value column shows a range like "233.25 - 242.58". If only one number is shown, use it for both min and max.
Copy numbers exactly as printed. If something cannot be read, use null for it. Do not guess."""


# ---------------------------------------------------------------- helpers ----
def _secret(name: str):
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


def read_with_gemini(image_bytes: bytes, mime: str) -> dict:
    """Ask the free Gemini API to read the numbers from the report photo."""
    key = _secret("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("no_key")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    resp = client.models.generate_content(
        model=_secret("GEMINI_MODEL") or "gemini-2.5-flash",
        contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime), EXTRACT_PROMPT],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
    )
    return json.loads(resp.text)


def apply_extraction(data: dict) -> None:
    """Put the numbers read from the photo into the form fields."""
    for f in SOIL_FIELDS:
        v = data.get(API_NAME[f]) or {}
        try:
            lo = float(v["min"]) if v.get("min") is not None else None
            hi = float(v["max"]) if v.get("max") is not None else lo
            if lo is None and hi is not None:
                lo = hi
        except (TypeError, ValueError):
            lo = hi = None
        st.session_state[f"{f}_min"] = lo
        st.session_state[f"{f}_max"] = hi
    try:
        st.session_state["scan_date"] = dt.date.fromisoformat(data.get("scan_date") or "")
    except ValueError:
        pass
    if data.get("scan_id"):
        st.session_state["scan_id"] = str(data["scan_id"])
    if data.get("texture"):
        st.session_state["texture"] = str(data["texture"])


def clean_filename(name: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    return stem or "farmer"


@st.cache_data
def crops_table():
    return engine.load_crops()


# -------------------------------------------------------------------- page ----
lang = st.radio(
    "Language / भाषा / ভাষা",
    i18n.LANGS,
    format_func=i18n.LANG_NAMES.get,
    horizontal=True,
)
ui = i18n.UI[lang]
crops = crops_table()

st.title("🌱 " + ui["app_title"])
st.write(ui["app_sub"])

# 1. Farmer details --------------------------------------------------------
st.subheader(ui["s1"])
farmer = st.text_input(ui["farmer_name"], key="farmer")
village = st.text_input(ui["village"], key="village")
block = st.text_input(ui["block"], key="block")

# 2. Soil report -----------------------------------------------------------
st.subheader(ui["s2"])
upload = st.file_uploader(ui["upload"], type=["jpg", "jpeg", "png"], key="report_photo")
photo_bytes = None
if upload is not None:
    photo_bytes = upload.getvalue()
    st.image(photo_bytes, use_container_width=True)
    if st.button("🔍 " + ui["read_btn"]):
        with st.spinner(ui["reading"]):
            try:
                apply_extraction(read_with_gemini(photo_bytes, upload.type or "image/jpeg"))
                st.session_state["read_msg"] = "read_ok"
            except RuntimeError:
                st.session_state["read_msg"] = "no_key"
            except Exception:
                st.session_state["read_msg"] = "read_fail"
msg = st.session_state.get("read_msg")
if msg == "read_ok":
    st.success(ui["read_ok"])
elif msg in ("read_fail", "no_key"):
    st.warning(ui[msg])

st.date_input(ui["scan_date"], value=None, key="scan_date", format="DD/MM/YYYY")
st.text_input(ui["scan_id"], key="scan_id")
st.caption(ui["values_hint"])

soil, ratings = {}, {}
for f in SOIL_FIELDS:
    st.markdown(f"**{ui['p_' + f]}**")
    c1, c2, c3 = st.columns(3)
    lo = c1.number_input(ui["min"], min_value=0.0, value=None, step=0.01, format="%.2f", key=f"{f}_min")
    hi = c2.number_input(ui["max"], min_value=0.0, value=None, step=0.01, format="%.2f", key=f"{f}_max")
    if lo is None and hi is not None:
        lo = hi
    if hi is None and lo is not None:
        hi = lo
    if lo is not None and hi is not None:
        soil[f] = (min(lo, hi), max(lo, hi))
        if f in engine.THRESHOLDS and f != "clay":
            ratings[f] = engine.classify(f, (lo + hi) / 2)
            icon = {"low": "🔴", "medium": "🟡", "high": "🟢"}[ratings[f]]
            c3.markdown(f"<br>{icon} **{ui['r_' + ratings[f]]}**", unsafe_allow_html=True)
st.text_input(ui["texture"], key="texture")

# 3. Crop and land ---------------------------------------------------------
st.subheader(ui["s3"])
season = st.selectbox(
    ui["season"], engine.seasons_available(crops), format_func=lambda s: ui["season_" + s], key="season"
)
season_crops = engine.crops_for_season(crops, season)
crop_names = {c["crop"]: c["names"][lang] for c in season_crops}
crop_key = st.selectbox(ui["crop"], list(crop_names), format_func=crop_names.get, key=f"crop_{season}")
crop = next(c for c in season_crops if c["crop"] == crop_key)
a1, a2 = st.columns(2)
area = a1.number_input(ui["area"], min_value=0.0, value=None, step=0.1, key="area")
unit = a2.selectbox(ui["unit"], list(engine.HA_PER_UNIT), format_func=lambda u: ui["unit_" + u], key="unit")

# Generate -----------------------------------------------------------------
if st.button("✅ " + ui["generate"], type="primary", use_container_width=True):
    needed = all(k in soil for k in ("n", "oc", "k", "p"))
    if not (farmer.strip() and needed and area and st.session_state.get("scan_date")):
        st.session_state.pop("report", None)
        st.error(ui["fill_required"])
    else:
        rt = {k: v for k, v in ratings.items()}
        st.session_state["report"] = {
            "farmer": farmer.strip(),
            "village": village.strip(),
            "block": block.strip(),
            "test_date": st.session_state["scan_date"],
            "scan_id": (st.session_state.get("scan_id") or "").strip(),
            "soil": {k: soil[k] for k in soil},
            "texture": (st.session_state.get("texture") or "").strip(),
            "ratings": rt,
            "crop": crop,
            "season": season,
            "area": float(area),
            "unit": unit,
            "rec": engine.recommend(crop, rt, float(area), unit),
            "advice_items": engine.advice_items(rt, crop),
            "photo": photo_bytes,
            "today": dt.date.today(),
        }

# Results ------------------------------------------------------------------
report = st.session_state.get("report")
if report:
    st.divider()
    st.subheader(ui["result_title"])
    rec = report["rec"]
    rows = []
    for step in rec["schedule"]:
        when = ui["when_basal"] if step["days"] == 0 else ui["when_days"].format(d=step["days"])
        rows.append(
            {
                ui["col_when"]: when,
                ui["col_fym"]: engine.fmt_amount(step["fym"]),
                ui["col_dap"]: engine.fmt_amount(step["dap"]),
                ui["col_mop"]: engine.fmt_amount(step["mop"]),
                ui["col_urea"]: engine.fmt_amount(step["urea"]),
            }
        )
    t = rec["totals"]
    rows.append(
        {
            ui["col_when"]: ui["row_total"],
            ui["col_fym"]: engine.fmt_amount(t["fym"]),
            ui["col_dap"]: engine.fmt_amount(t["dap"]),
            ui["col_mop"]: engine.fmt_amount(t["mop"]),
            ui["col_urea"]: engine.fmt_amount(t["urea"]),
        }
    )
    st.table(rows)
    for line in i18n.render_advice(lang, report["advice_items"], report["crop"]):
        st.markdown("- " + line)
    try:
        pdf_bytes = build_pdf(report, lang)
        st.download_button(
            "📄 " + ui["download"],
            data=pdf_bytes,
            file_name=f"fertiliser_advice_{clean_filename(report['farmer'])}_{report['today']:%Y%m%d}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )
    except MissingFontError as e:
        st.error(ui["pdf_failed"] + str(e))
    except Exception as e:  # keep the on-screen advice visible even if the PDF fails
        st.error(ui["pdf_failed"] + f"{type(e).__name__}: {e}")
