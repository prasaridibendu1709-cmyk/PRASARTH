"""PRASARTH - soil test to complete crop nutrition plan (English / Hindi / Bengali).

Run locally:  streamlit run app.py
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import urllib.request
from pathlib import Path

import streamlit as st

import engine
import i18n
from pdf_report import MissingFontError, build_pdf

BASE = Path(__file__).parent
LOGO = BASE / "assets" / "logo.png"


def _page_icon():
    if LOGO.exists():
        try:
            from PIL import Image
            return Image.open(LOGO)
        except Exception:
            pass
    return "🌱"


st.set_page_config(page_title="PRASARTH", page_icon=_page_icon(), layout="centered")

SOIL_FIELDS = ["n", "oc", "clay", "k", "p", "cec"]
API_NAME = {"n": "nitrogen", "oc": "organic_carbon", "clay": "clay", "k": "potassium", "p": "phosphorus", "cec": "cec"}
EXTRACT_PROMPT = """You are reading a photo or screenshot of the result screen of a ScaNxt BhuParikshak soil testing device.
Return ONLY a JSON object with these keys:
  "scan_date": the Scan Date as YYYY-MM-DD (it is printed like 2026-Mar-18:16:58:39, i.e. year-month-day:time), or null
  "scan_id": the Scan ID text, or null
  "texture": the soil texture label shown next to Clay (for example "Clay Loam"), or null
  "nitrogen", "organic_carbon", "clay", "potassium", "phosphorus", "cec": each an object {"min": number, "max": number}
The Value column shows a range like "233.25 - 242.58". If only one number is shown, use it for both min and max.
Copy numbers exactly as printed. If something cannot be read, use null for it. Do not guess."""

CSS = """
<style>
.block-container{padding-top:1.2rem;max-width:760px}
.hero{background:linear-gradient(135deg,#0f5132 0%,#1B7F4B 58%,#8cc56f 100%);color:#fff;padding:18px 20px;border-radius:20px;display:flex;gap:16px;align-items:center;box-shadow:0 6px 18px rgba(15,81,50,.25)}
.hero img{height:68px;background:#fff;border-radius:14px;padding:6px}
.hero h1{margin:0;font-size:1.9rem;line-height:1.1;color:#fff;padding:0}
.hero .tag{margin:4px 0 0;opacity:.95;font-size:1rem}
.hero .org{margin:2px 0 0;opacity:.8;font-size:.85rem}
.steps{display:flex;gap:8px;margin:12px 0 4px}
.steps div{flex:1;background:#EEF7F1;border-radius:14px;padding:10px 6px;text-align:center;font-weight:600;color:#0f5132;font-size:.92rem}
.steps span{display:block;font-size:1.4rem}
.sec{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.2rem;margin:22px 0 6px;color:#0f5132}
.sec .b{background:#1B7F4B;color:#fff;border-radius:50%;width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;font-size:.95rem}
.chip{display:inline-block;border-radius:999px;padding:3px 12px;font-weight:700;font-size:.9rem}
.chip.low{background:#fee2e2;color:#991b1b}
.chip.medium{background:#fef3c7;color:#92400e}
.chip.high{background:#dcfce7;color:#166534}
.zone{background:#EEF7F1;border-left:6px solid #1B7F4B;border-radius:10px;padding:10px 14px;margin:6px 0 2px;color:#0f5132}
.wx{display:flex;gap:8px;margin:6px 0}
.wx div{flex:1;background:#eaf3fb;border-radius:12px;padding:8px;text-align:center;font-size:.9rem;color:#0b3d62}
.wx b{display:block;font-size:1.25rem}
div.stButton>button[kind="primary"],div.stDownloadButton>button[kind="primary"]{font-size:1.15rem;padding:.7rem;border-radius:14px}
</style>
"""


# ---------------------------------------------------------------- helpers ----
def _secret(name: str):
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


def read_with_gemini(image_bytes: bytes, mime: str) -> dict:
    key = _secret("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("no_key")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    models = [_secret("GEMINI_MODEL")] if _secret("GEMINI_MODEL") else ["gemini-2.5-flash", "gemini-2.0-flash"]
    last = None
    for model in models:
        try:
            resp = client.models.generate_content(
                model=model,
                contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime), EXTRACT_PROMPT],
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
            )
            text = (resp.text or "").strip()
            text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
            return json.loads(text)
        except Exception as e:  # try the next model, keep the error to show
            last = e
    raise last  # type: ignore[misc]


def apply_extraction(data: dict) -> None:
    for f in SOIL_FIELDS:
        v = data.get(API_NAME[f]) or {}
        try:
            lo = float(v["min"]) if v.get("min") is not None else None
            hi = float(v["max"]) if v.get("max") is not None else lo
            if lo is None and hi is not None:
                lo = hi
        except (TypeError, ValueError, KeyError):
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


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_weather(lat: float, lon: float):
    """Free Open-Meteo forecast: last 7 days + next 3 days. Returns None if offline."""
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=%.3f&longitude=%.3f"
        "&daily=precipitation_sum,temperature_2m_max&past_days=7&forecast_days=3&timezone=Asia%%2FKolkata"
    ) % (lat, lon)
    try:
        with urllib.request.urlopen(url, timeout=6) as r:
            d = json.load(r)["daily"]
        rain = [x or 0.0 for x in d["precipitation_sum"]]
        tmax = [x or 0.0 for x in d["temperature_2m_max"]]
        return {"past7": sum(rain[:7]), "next3": sum(rain[7:10]), "tmax": max(tmax[7:10])}
    except Exception:
        return None


def clean_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_") or "farmer"


@st.cache_data
def load_data():
    return engine.load_crops(), engine.load_regions()


def logo_html() -> str:
    if LOGO.exists():
        b64 = base64.b64encode(LOGO.read_bytes()).decode()
        return f'<img src="data:image/png;base64,{b64}" alt="PRASARI"/>'
    return ""


def section(n: int, text: str) -> None:
    st.markdown(f'<div class="sec"><span class="b">{n}</span>{text}</div>', unsafe_allow_html=True)


# -------------------------------------------------------------------- page ----
crops, regions = load_data()
st.markdown(CSS, unsafe_allow_html=True)

lang = st.radio("Language / भाषा / ভাষা", i18n.LANGS, format_func=i18n.LANG_NAMES.get, horizontal=True)
ui = i18n.UI[lang]
pn = i18n.PRODUCT_NAMES[lang]

st.markdown(
    f'<div class="hero">{logo_html()}<div><h1>{ui["app_name"]}</h1>'
    f'<p class="tag">{ui["app_tag"]}</p><p class="org">{ui["org_line"]}</p></div></div>'
    f'<div class="steps"><div><span>🧪</span>{ui["how1"]}</div><div><span>📝</span>{ui["how2"]}</div>'
    f'<div><span>🖨️</span>{ui["how3"]}</div></div>',
    unsafe_allow_html=True,
)

# 1. Farmer ----------------------------------------------------------------
section(1, ui["s1"])
with st.container(border=True):
    farmer = st.text_input(ui["farmer_name"], key="farmer")
    c1, c2 = st.columns(2)
    village = c1.text_input(ui["village"], key="village")
    block = c2.text_input(ui["block"], key="block")
    with st.expander(ui["more"]):
        mobile = st.text_input(ui["mobile"], key="mobile")
        plot = st.text_input(ui["plot"], key="plot")
        prepared_by = st.text_input(ui["prepared_by"], key="prepared_by")
        shg = st.text_input(ui["shg"], key="shg")

# 2. Place -----------------------------------------------------------------
section(2, ui["s2"])
with st.container(border=True):
    p1, p2 = st.columns(2)
    state = p1.selectbox(ui["state"], engine.STATES, format_func=lambda s: i18n.STATE_NAMES[lang][s], key="state")
    dlist = engine.districts_of(regions, state)
    names = {r["district"]: r for r in dlist}
    district = p2.selectbox(
        ui["district"], list(names), key=f"district_{state}",
        format_func=lambda d: d + (" *" if names[d]["new"] else ""),
    )
    region = names[district]
    if region["new"]:
        st.caption("* " + ui["district_new"])
    zinfo = engine.ZONES[region["zone"]]
    st.markdown(
        f'<div class="zone"><b>{ui["zone_label"]}:</b> {i18n.ZONE_NAMES[lang][region["zone"]]}<br>'
        f'{ui["rain_label"]}: {zinfo["rain"]} &nbsp;|&nbsp; {ui["ph_typ"]}: {zinfo["ph"] or ui["ph_unknown"]}</div>',
        unsafe_allow_html=True,
    )
    irrigation = st.radio(
        ui["irrigation"], ["rainfed", "irrigated"], format_func=lambda k: ui["irr_" + k], horizontal=True, key="irrigation"
    )

# 3. Soil report -----------------------------------------------------------
section(3, ui["s3"])
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
                st.session_state.pop("read_err", None)
            except RuntimeError:
                st.session_state["read_msg"] = "no_key"
            except Exception as e:
                st.session_state["read_msg"] = "read_fail"
                st.session_state["read_err"] = f"{type(e).__name__}: {str(e)[:600]}"
msg = st.session_state.get("read_msg")
if msg == "read_ok":
    st.success(ui["read_ok"])
elif msg in ("read_fail", "no_key"):
    st.warning(ui[msg])
    if st.session_state.get("read_err"):
        with st.expander(ui["tech"]):
            st.code(st.session_state["read_err"])

with st.container(border=True):
    d1, d2 = st.columns(2)
    d1.date_input(ui["scan_date"], value=None, key="scan_date", format="DD/MM/YYYY")
    d2.text_input(ui["scan_id"], key="scan_id")
    st.caption(ui["values_hint"])
    soil, ratings = {}, {}
    for f in SOIL_FIELDS:
        st.markdown(f"**{ui['p_' + f]}**")
        c1, c2, c3 = st.columns([1, 1, 1])
        lo = c1.number_input(ui["min"], min_value=0.0, value=None, step=0.01, format="%.2f", key=f"{f}_min")
        hi = c2.number_input(ui["max"], min_value=0.0, value=None, step=0.01, format="%.2f", key=f"{f}_max")
        if lo is None and hi is not None:
            lo = hi
        if hi is None and lo is not None:
            hi = lo
        if lo is not None and hi is not None:
            soil[f] = (min(lo, hi), max(lo, hi))
            if f in engine.THRESHOLDS:
                ratings[f] = engine.classify(f, (lo + hi) / 2)
                c3.markdown(f'<br><span class="chip {ratings[f]}">{ui["r_" + ratings[f]]}</span>', unsafe_allow_html=True)
    st.text_input(ui["texture"], key="texture")
    ph = st.number_input(ui["ph_label"], min_value=3.0, max_value=10.0, value=None, step=0.1, format="%.1f", key="ph")

# 4. Crop and land ---------------------------------------------------------
section(4, ui["s4"])
with st.container(border=True):
    season = st.selectbox(ui["season"], engine.seasons_available(crops), format_func=lambda s: ui["season_" + s], key="season")
    season_crops = engine.crops_for_season(crops, season)
    crop_names = {c["crop"]: c["names"][lang] for c in season_crops}
    crop_key = st.selectbox(ui["crop"], list(crop_names), format_func=crop_names.get, key=f"crop_{season}")
    crop = next(c for c in season_crops if c["crop"] == crop_key)
    a1, a2 = st.columns(2)
    area = a1.number_input(ui["area"], min_value=0.0, value=None, step=0.1, key="area")
    unit = a2.selectbox(ui["unit"], list(engine.HA_PER_UNIT), format_func=lambda u: ui["unit_" + u], key="unit")

# 5. Approach --------------------------------------------------------------
section(5, ui["s5"])
approach = st.radio(
    ui["s5"], engine.APPROACHES, format_func=lambda a: ui["ap_" + a],
    captions=[ui["apc_" + a] for a in engine.APPROACHES], key="approach", label_visibility="collapsed",
)

# Generate -----------------------------------------------------------------
if st.button("✅ " + ui["generate"], type="primary", use_container_width=True):
    needed = all(k in soil for k in ("n", "oc", "k", "p"))
    if not (farmer.strip() and needed and area and st.session_state.get("scan_date")):
        st.session_state.pop("report", None)
        st.error(ui["fill_required"])
    else:
        acid_zone = "acid" in zinfo["flags"] or (ph is not None and ph < engine.PH_ACID)
        plan = engine.recommend(crop, ratings, float(area), unit, approach, acid_zone=acid_zone, ph=ph)
        st.session_state["report_id"] = st.session_state.get("report_id", 0) + 1
        st.session_state["report"] = {
            "id": st.session_state["report_id"],
            "farmer": farmer.strip(), "village": village.strip(), "block": block.strip(),
            "mobile": mobile.strip(), "plot": plot.strip(), "prepared_by": prepared_by.strip(), "shg": shg.strip(),
            "state": state, "district": district, "zone": region["zone"], "lat": region["lat"], "lon": region["lon"],
            "test_date": st.session_state["scan_date"], "scan_id": (st.session_state.get("scan_id") or "").strip(),
            "soil": dict(soil), "ratings": dict(ratings), "texture": (st.session_state.get("texture") or "").strip(),
            "ph": ph, "crop": crop, "season": season, "area": float(area), "unit": unit,
            "plan": plan,
            "advice_items": engine.advice_items(ratings, crop, approach, region["zone"], irrigation, ph, plan),
            "photo": photo_bytes, "today": dt.date.today(),
        }

# Results ------------------------------------------------------------------
report = st.session_state.get("report")
if report:
    st.divider()
    st.subheader("🌾 " + ui["result_title"])
    plan = report["plan"]

    k1, k2, k3 = st.columns(3)
    k1.metric(ui["crop"], report["crop"]["names"][lang])
    k2.metric(ui["area"], f"{report['area']:g} {ui['unit_' + report['unit']]}")
    k3.metric(ui["total_cost"], f"₹ {plan['cost']:,.0f}")

    # weather (free Open-Meteo; skipped quietly if offline)
    wx = fetch_weather(report["lat"], report["lon"])
    wx_items = []
    if wx:
        st.markdown(
            f'<b>{ui["wx_title"]}</b> ({report["district"]})<div class="wx">'
            f'<div><b>{wx["past7"]:.0f} mm</b>{ui["wx_past"]}</div>'
            f'<div><b>{wx["next3"]:.0f} mm</b>{ui["wx_next"]}</div>'
            f'<div><b>{wx["tmax"]:.0f} °C</b>{ui["wx_temp"]}</div></div>',
            unsafe_allow_html=True,
        )
        wx_items = engine.weather_keys(wx["past7"], wx["next3"], wx["tmax"])
    else:
        st.caption(ui["wx_fail"])

    if plan.get("coverage") and plan["approach"] == "organic":
        st.markdown(f"**{ui['cov_title']}**")
        for nut in ("n", "p", "k"):
            pct = min(100, round(plan["coverage"][nut]))
            st.progress(pct / 100, text=f"{ui['cov_' + nut]}: {pct}%")

    t_buy, t_when, t_spray, t_adv = st.tabs([ui["tab_buy"], ui["tab_when"], ui["tab_spray"], ui["tab_advice"]])

    with t_buy:
        order = ["fym", "urea", "dap", "mop", "oilcake", "rockp", "bonem", "ash", "lime", "gjm", "jeev",
                 "wsf192", "mkp", "kno3", "cano3", "borax", "znso4", "micro", "dap2", "urea2", "jeevs", "panch", "vwash"]
        rows = []
        for key in order:
            q = plan["all_totals"].get(key, 0)
            if q > 0:
                rows.append({
                    ui["col_product"]: pn[key], ui["col_qty"]: engine.fmt_qty(key, q),
                    ui["col_bags"]: engine.bags_text(key, q), ui["col_cost"]: f"{engine.PRODUCTS[key]['price'] * q:,.0f}",
                })
        st.table(rows)
        st.markdown(f"**{ui['total_cost']}: ₹ {plan['cost']:,.0f}**")
        st.caption(ui["cost_note"])

    with t_when:
        rows = []
        for stg in plan["stages"]:
            if not stg["items"]:
                continue
            when = ui["when_basal"] if stg["days"] == 0 else ui["when_days"].format(d=stg["days"])
            for i, (key, q) in enumerate(stg["items"]):
                rows.append({ui["col_when"]: when if i == 0 else "", ui["col_product"]: pn[key], ui["col_qty"]: engine.fmt_qty(key, q)})
        st.table(rows)

    with t_spray:
        if plan["sprays"]:
            rows = []
            for sp in plan["sprays"]:
                name = pn[sp["product"]] + (f" {ui[sp['extra']]}" if sp["extra"] else "")
                rows.append({
                    ui["sp_stage"]: ui["stg_" + sp["stage"]], ui["sp_product"]: name,
                    ui["sp_pump"]: f"{sp['per_pump']:g} {sp['unit']}",
                    ui["sp_total"]: f"{engine.fmt_qty(sp['product'], sp['total_qty'])} ({sp['pumps']} {ui['sp_pumps']})",
                })
            st.table(rows)
        else:
            st.info(ui["sp_none"])

    with t_adv:
        for line in i18n.render_advice(lang, wx_items + report["advice_items"], report["crop"]):
            st.markdown("- " + line)

    cache = st.session_state.setdefault("pdf_cache", {})
    ck = (report["id"], lang)
    try:
        if ck not in cache:
            cache.clear()
            cache[ck] = build_pdf(report, lang)
        st.download_button(
            "📄 " + ui["download"], data=cache[ck],
            file_name=f"plan_{clean_filename(report['farmer'])}_{report['today']:%Y%m%d}.pdf",
            mime="application/pdf", type="primary", use_container_width=True,
        )
    except MissingFontError as e:
        st.error(ui["pdf_failed"] + str(e))
    except Exception as e:  # keep the on-screen plan visible even if the PDF fails
        st.error(ui["pdf_failed"] + f"{type(e).__name__}: {e}")
