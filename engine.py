"""Mati Sathi calculation engine (no Streamlit / PDF code here, so it can be tested alone).

Everything an agronomist may want to tune is in the "SETTINGS" blocks near the top.
All numbers marked ASSUMPTION are working values that should be confirmed by PRASARI's
agronomy team (and ideally BAU Ranchi / ICAR / KVK recommendations) before wide use.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

BASE = Path(__file__).parent
CROPS_CSV = BASE / "crops.csv"
REGIONS_CSV = BASE / "regions.csv"

# ============================ SETTINGS: soil rules ============================
# Dose adjustment for N, P and K according to the soil rating on the device.  ASSUMPTION
RATING_FACTOR = {"low": 1.25, "medium": 1.00, "high": 0.75}
# Compost / FYM adjustment according to the organic carbon rating.              ASSUMPTION
FYM_FACTOR = {"low": 1.5, "medium": 1.0, "high": 0.75}
# Ranges printed on the ScaNxt BhuParikshak screen (low below first, high above second).
THRESHOLDS = {"n": (280, 560), "p": (11, 25), "k": (120, 280), "oc": (0.5, 0.75), "cec": (12, 25)}
# Land units -> hectares (1 bigha = 33 decimal = 0.33 acre).
HA_PER_UNIT = {"hectare": 1.0, "acre": 0.404686, "decimal": 0.00404686, "bigha": 0.133546}
ACRE_HA = 0.404686

# ======================== SETTINGS: approach rules ============================
APPROACHES = ["inorganic", "partial", "organic", "natural"]
# Partial organic: chemical NPK = 75% of the soil-adjusted dose, rest from compost/FYM + bio-fertiliser.
# (ICAR NRM report: 75% NP + biofertiliser matched 100% NP yield in rice trials.)
PARTIAL_CHEM_SHARE = 0.75
# Complete organic: practical limits so the plan stays affordable / carry-able.  ASSUMPTION
MAX_OILCAKE_KG_HA = 750
MAX_ASH_KG_HA = 1000
ORGANIC_FYM_MULT = 1.5  # complete organic uses more compost/FYM than the crop's base rate
# Share of oil-cake given at sowing; the rest goes with the later top-dress stages.
OILCAKE_BASAL_SHARE = 0.6
# Natural farming package (practice-based, not nutrient-calculated). Follow your NF trainer.  ASSUMPTION
GJM_KG_PER_ACRE = 200
JEEV_L_PER_ACRE = 200
NF_DAYS = [0, 21, 42, 63]
# Liming (ICAR NRM report: 0.2-0.4 t/ha in furrow for soils below pH 5.5).
PH_ACID = 5.5
LIME_KG_HA = (200, 400)  # use the upper end below pH 5.0
# Sprays
SPRAY_L_PER_ACRE = 200
PUMP_L = 15

# ======================== SETTINGS: products ==================================
# nut = total % (N, P2O5, K2O); avail = share usable by the first crop (N, P, K).
# Organic content: ICAR table (FYM, compost, vermicompost, poultry, neem cake); others standard
# textbook values.  Availability factors are textbook values for first-year crops.   ASSUMPTION
# price = indicative Rs per kg (or per litre). UPDATE from your local shop.            ASSUMPTION
PRODUCTS: dict[str, dict] = {
    "urea":   dict(unit="kg", bag=45, price=6.0,  nut=(46, 0, 0),    avail=(1, 1, 1)),
    "dap":    dict(unit="kg", bag=50, price=27.0, nut=(18, 46, 0),   avail=(1, 1, 1)),
    "mop":    dict(unit="kg", bag=50, price=35.0, nut=(0, 0, 60),    avail=(1, 1, 1)),
    "fym":    dict(unit="kg", bag=None, price=1.5, nut=(0.70, 0.35, 0.56), avail=(0.30, 0.60, 0.70)),
    "oilcake": dict(unit="kg", bag=50, price=30.0, nut=(3.6, 0.84, 1.38), avail=(0.65, 0.60, 0.70)),
    "rockp":  dict(unit="kg", bag=50, price=12.0, nut=(0, 20, 0),    avail=(0, 0.40, 0)),
    "bonem":  dict(unit="kg", bag=50, price=25.0, nut=(2, 20, 0),    avail=(0.5, 0.60, 0)),
    "ash":    dict(unit="kg", bag=None, price=2.0, nut=(0, 1, 5),    avail=(0, 0.60, 0.70)),
    "lime":   dict(unit="kg", bag=50, price=6.0,  nut=(0, 0, 0),     avail=(0, 0, 0)),
    "gjm":    dict(unit="kg", bag=None, price=0.0, nut=(0, 0, 0),    avail=(0, 0, 0)),
    "jeev":   dict(unit="L",  bag=None, price=0.0, nut=(0, 0, 0),    avail=(0, 0, 0)),
    # spray products (price per kg or per litre of product)
    "wsf192": dict(unit="kg", bag=None, price=220.0, nut=(0, 0, 0), avail=(0, 0, 0)),
    "mkp":    dict(unit="kg", bag=None, price=260.0, nut=(0, 0, 0), avail=(0, 0, 0)),
    "kno3":   dict(unit="kg", bag=None, price=150.0, nut=(0, 0, 0), avail=(0, 0, 0)),
    "cano3":  dict(unit="kg", bag=None, price=80.0,  nut=(0, 0, 0), avail=(0, 0, 0)),
    "borax":  dict(unit="kg", bag=None, price=150.0, nut=(0, 0, 0), avail=(0, 0, 0)),
    "znso4":  dict(unit="kg", bag=None, price=90.0,  nut=(0, 0, 0), avail=(0, 0, 0)),
    "micro":  dict(unit="kg", bag=None, price=450.0, nut=(0, 0, 0), avail=(0, 0, 0)),
    "dap2":   dict(unit="kg", bag=None, price=27.0,  nut=(0, 0, 0), avail=(0, 0, 0)),
    "urea2":  dict(unit="kg", bag=None, price=6.0,   nut=(0, 0, 0), avail=(0, 0, 0)),
    "panch":  dict(unit="L",  bag=None, price=0.0,   nut=(0, 0, 0), avail=(0, 0, 0)),
    "vwash":  dict(unit="L",  bag=None, price=0.0,   nut=(0, 0, 0), avail=(0, 0, 0)),
    "jeevs":  dict(unit="L",  bag=None, price=0.0,   nut=(0, 0, 0), avail=(0, 0, 0)),
}

# Spray rules by crop category: (stage, product, concentration, nutrient_tag)
# concentration = g (or mL) of product per litre of water. nutrient_tag: the spray is skipped
# if the soil already rates HIGH for that nutrient (saves money). None = always given.
# Doses are common label / extension values (0.5% = 5 g/L; 2% DAP or urea = 20 g/L).  ASSUMPTION
CHEM_SPRAYS = {
    "cereal":    [("veg", "wsf192", 5, None), ("fill", "kno3", 5, "k")],
    "pulse":     [("flower", "dap2", 20, "p"), ("fill", "kno3", 5, "k"), ("fill", "urea2", 20, "n")],
    "oilseed":   [("veg", "wsf192", 5, None), ("flower", "mkp", 5, "p")],
    "veg_fruit": [("veg", "wsf192", 5, None), ("flower", "mkp", 5, "p"), ("fill", "kno3", 5, "k")],
    "veg_cole":  [("veg", "wsf192", 5, None), ("fill", "kno3", 5, "k")],
    "root_bulb": [("veg", "wsf192", 5, None), ("fill", "kno3", 5, "k")],
}
MICRO_SPRAYS = {  # crop `micro` flag -> (stage, product, conc, extra)
    "zn": ("veg", "znso4", 5, "with_lime"),
    "b": ("flower", "borax", 2, ""),
    "ca": ("fill", "cano3", 5, ""),
    "mm": ("flower", "micro", 2.5, ""),
}
BIO_SPRAYS = [("veg", "jeevs", 100, None), ("flower", "panch", 30, None), ("fill", "vwash", 100, None)]  # mL/L

# ======================== SETTINGS: regions ===================================
# flags drive the advice lines (see i18n.py).  Rain and pH are typical values from the
# West Bengal agro-climatic zone table; Jharkhand uses the state-wide 1200-1600 mm;
# Meghalaya 2500 to 10000+ mm (very wide). pH shown only where a source gave it.
ZONES = {
    "wb_hill":        dict(rain="2500-3500 mm", ph="4.2-5.8", flags=["acid", "high_rain", "slope"]),
    "wb_terai":       dict(rain="2100-2300 mm", ph="4.0-6.0", flags=["acid", "high_rain", "boron"]),
    "wb_new_alluvial": dict(rain="1500-1600 mm", ph="6.9-7.2", flags=["intensive"]),
    "wb_old_alluvial": dict(rain="1400-1500 mm", ph="6.5-7.0", flags=["intensive"]),
    "wb_laterite":    dict(rain="1200-1300 mm", ph="5.0-6.0", flags=["acid", "drought", "lowoc"]),
    "wb_coastal":     dict(rain="1600-1800 mm", ph="6.5-8.5", flags=["saline", "flood"]),
    "jh_central_ne":  dict(rain="1200-1600 mm", ph="", flags=["acid", "drought", "lowoc", "slope"]),
    "jh_western":     dict(rain="1200-1600 mm", ph="", flags=["acid", "lowoc"]),
    "jh_southeast":   dict(rain="1200-1600 mm", ph="", flags=["acid", "lowoc", "slope"]),
    "ml_khasi":       dict(rain="2500-10000+ mm", ph="", flags=["acid", "high_rain", "slope"]),
    "ml_jaintia":     dict(rain="2500-10000+ mm", ph="", flags=["acid", "high_rain", "slope"]),
    "ml_garo":        dict(rain="2500-4000 mm", ph="", flags=["acid", "high_rain"]),
}
STATES = ["West Bengal", "Jharkhand", "Meghalaya"]
SEASON_ORDER = ["kharif", "rabi", "zaid"]
# ==============================================================================


# ------------------------------------------------------------------ data load --
def load_crops(path: Path = CROPS_CSV) -> list[dict]:
    crops = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for line_no, raw in enumerate(csv.DictReader(f), start=2):
            r = {k.strip(): (v or "").strip() for k, v in raw.items() if k}
            if not r.get("crop"):
                continue
            split = [float(x) for x in r["n_split"].split(":")]
            days = [int(x) for x in r["n_days"].split(":")]
            if len(split) != len(days) or not split:
                raise ValueError(f"crops.csv line {line_no}: n_split and n_days must match")
            if r["category"] not in CHEM_SPRAYS:
                raise ValueError(f"crops.csv line {line_no}: unknown category {r['category']}")
            total = sum(split)
            crops.append({
                "crop": r["crop"], "season": r["season"].lower(), "category": r["category"],
                "micro": [m for m in r["micro"].split("|") if m],
                "n": float(r["n"]), "p": float(r["p2o5"]), "k": float(r["k2o"]),
                "fym": float(r["fym_t_ha"]),
                "split": [x / total for x in split], "days": days,
                "names": {l: r[f"name_{l}"] for l in ("en", "hi", "bn")},
                "advice": {l: r[f"advice_{l}"] for l in ("en", "hi", "bn")},
            })
    return crops


def load_regions(path: Path = REGIONS_CSV) -> list[dict]:
    out = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["zone"] not in ZONES:
                raise ValueError(f"regions.csv: unknown zone {r['zone']}")
            out.append({"state": r["state"], "district": r["district"], "lat": float(r["lat"]),
                        "lon": float(r["lon"]), "zone": r["zone"], "new": r["new"] == "new"})
    return out


def districts_of(regions: list[dict], state: str) -> list[dict]:
    return sorted((r for r in regions if r["state"] == state), key=lambda r: r["district"])


def seasons_available(crops):
    present = {c["season"] for c in crops}
    return [s for s in SEASON_ORDER if s in present]


def crops_for_season(crops, season):
    return [c for c in crops if c["season"] == season]


# -------------------------------------------------------------- soil rating ----
def classify(param: str, value: float) -> str:
    lo, hi = THRESHOLDS[param]
    return "low" if value < lo else "high" if value > hi else "medium"


def ratings_from_values(soil: dict) -> dict:
    out = {}
    for p in THRESHOLDS:
        if p in soil:
            lo, hi = soil[p]
            out[p] = classify(p, (lo + hi) / 2)
    return out


def classify_ph(ph: float | None) -> str | None:
    if ph is None:
        return None
    return "acid" if ph < PH_ACID else "alkaline" if ph > 8.0 else "ok"


# ------------------------------------------------------------ calculations ----
def _avail_nut(key: str, kg: float) -> tuple[float, float, float]:
    p = PRODUCTS[key]
    return tuple(kg * p["nut"][i] / 100 * p["avail"][i] for i in range(3))  # type: ignore


def _add(stages: list[dict], idx: int, key: str, qty: float) -> None:
    if qty > 1e-9:
        stages[idx]["items"].append((key, qty))


def _chem_plan(crop, target, fym_kg, ha, share, stages):
    """Urea / DAP / MOP plan for `share` of the soil-adjusted target (1.0 or 0.75)."""
    n_t, p_t, k_t = (target[x] * share for x in ("n", "p", "k"))
    dap = p_t / 0.46
    dap_n = dap * 0.18
    mop = k_t / 0.60
    stage_n = [n_t * f for f in crop["split"]]
    stage_n[0] = max(0.0, stage_n[0] - dap_n)
    s = sum(stage_n)
    urea_n_total = max(0.0, n_t - dap_n)
    scale = urea_n_total / s if s > 0 else 0.0
    _add(stages, 0, "fym", fym_kg)
    _add(stages, 0, "dap", dap)
    _add(stages, 0, "mop", mop)
    for i, n in enumerate(stage_n):
        _add(stages, i, "urea", n * scale / 0.46)


def _organic_plan(crop, target, fym_kg, ha, acid_zone, stages):
    items0 = {"fym": fym_kg}
    n_c, p_c, k_c = _avail_nut("fym", fym_kg)
    # nitrogen -> oil cake
    oil = min(max(0.0, target["n"] - n_c) / (0.036 * 0.65), MAX_OILCAKE_KG_HA * ha)
    a = _avail_nut("oilcake", oil)
    n_c += a[0]; p_c += a[1]; k_c += a[2]
    # phosphorus -> rock phosphate (acid soils) or bone meal
    rem_p = max(0.0, target["p"] - p_c)
    if acid_zone:
        rp = rem_p / (0.20 * 0.40)
        items0["rockp"] = rp
        a = _avail_nut("rockp", rp)
    else:
        bm = rem_p / (0.20 * 0.60)
        items0["bonem"] = bm
        a = _avail_nut("bonem", bm)
    n_c += a[0]; p_c += a[1]; k_c += a[2]
    # potash -> wood ash
    rem_k = max(0.0, target["k"] - k_c)
    ash = min(rem_k / (0.05 * 0.70), MAX_ASH_KG_HA * ha)
    items0["ash"] = ash
    a = _avail_nut("ash", ash)
    n_c += a[0]; p_c += a[1]; k_c += a[2]
    # schedule: oil cake split between sowing and later stages
    later = len(stages) - 1
    for key, qty in items0.items():
        _add(stages, 0, key, qty)
    if later == 0:
        _add(stages, 0, "oilcake", oil)
    else:
        _add(stages, 0, "oilcake", oil * OILCAKE_BASAL_SHARE)
        for i in range(1, len(stages)):
            _add(stages, i, "oilcake", oil * (1 - OILCAKE_BASAL_SHARE) / later)
    return {"n": n_c, "p": p_c, "k": k_c}


def recommend(crop: dict, ratings: dict, area: float, unit: str, approach: str,
              acid_zone: bool = False, ph: float | None = None) -> dict:
    """Full nutrient plan for the land. Returns stages, totals, coverage and cost."""
    if approach not in APPROACHES:
        raise ValueError(approach)
    ha = area * HA_PER_UNIT[unit]
    dose_ha = {x: crop[x] * RATING_FACTOR[ratings[x]] for x in ("n", "p", "k")}
    target = {x: dose_ha[x] * ha for x in dose_ha}
    fym_kg = crop["fym"] * 1000 * ha * FYM_FACTOR[ratings["oc"]]
    if approach == "organic":
        fym_kg *= ORGANIC_FYM_MULT

    if approach == "natural":
        days = NF_DAYS
    else:
        days = crop["days"]
    stages = [{"days": d, "items": []} for d in days]

    supplied: dict | None
    if approach in ("inorganic", "partial"):
        share = 1.0 if approach == "inorganic" else PARTIAL_CHEM_SHARE
        _chem_plan(crop, target, fym_kg, ha, share, stages)
        a_fym = _avail_nut("fym", fym_kg)
        chem = {"n": 0.0, "p": 0.0, "k": 0.0}
        for st in stages:
            for key, q in st["items"]:
                a = _avail_nut(key, q) if key == "fym" else None
                if key in ("urea", "dap", "mop"):
                    nut = PRODUCTS[key]["nut"]
                    chem["n"] += q * nut[0] / 100
                    chem["p"] += q * nut[1] / 100
                    chem["k"] += q * nut[2] / 100
        supplied = {"n": chem["n"] + a_fym[0], "p": chem["p"] + a_fym[1], "k": chem["k"] + a_fym[2]}
    elif approach == "organic":
        supplied = _organic_plan(crop, target, fym_kg, ha, acid_zone, stages)
    else:  # natural farming
        acre = area * HA_PER_UNIT[unit] / ACRE_HA
        _add(stages, 0, "gjm", GJM_KG_PER_ACRE * acre)
        for i in range(len(stages)):
            _add(stages, i, "jeev", JEEV_L_PER_ACRE * acre)
        supplied = None

    # liming
    lime_kg = 0.0
    if ph is not None and ph < PH_ACID:
        lime_kg = (LIME_KG_HA[1] if ph < 5.0 else LIME_KG_HA[0]) * ha
        _add(stages, 0, "lime", lime_kg)

    totals: dict[str, float] = {}
    for st in stages:
        for key, q in st["items"]:
            totals[key] = totals.get(key, 0.0) + q

    coverage = None
    if supplied is not None:
        coverage = {x: (supplied[x] / target[x] * 100 if target[x] > 0 else 100.0) for x in ("n", "p", "k")}

    sprays = spray_plan(crop, ratings, approach, area, unit)
    spray_totals = {}
    for sp in sprays:
        spray_totals[sp["product"]] = spray_totals.get(sp["product"], 0.0) + sp["total_qty"]

    all_totals = dict(totals)
    for k, v in spray_totals.items():
        all_totals[k] = all_totals.get(k, 0.0) + v
    cost = sum(PRODUCTS[k]["price"] * q for k, q in all_totals.items())

    return {
        "approach": approach, "area_ha": ha, "area_acre": ha / ACRE_HA,
        "dose_ha": dose_ha, "target": target, "supplied": supplied, "coverage": coverage,
        "stages": stages, "totals": totals, "sprays": sprays, "all_totals": all_totals,
        "cost": cost, "lime_kg": lime_kg,
    }


def spray_plan(crop: dict, ratings: dict, approach: str, area: float, unit: str) -> list[dict]:
    """Water-soluble / liquid sprays by crop stage (skips nutrients the soil already has plenty of)."""
    acre = area * HA_PER_UNIT[unit] / ACRE_HA
    litres = SPRAY_L_PER_ACRE * acre
    rules: list[tuple] = []
    if approach in ("inorganic", "partial"):
        for stage, prod, conc, tag in CHEM_SPRAYS[crop["category"]]:
            if tag and ratings.get(tag) == "high":
                continue
            rules.append((stage, prod, conc, tag, ""))
        for m in crop["micro"]:
            stage, prod, conc, extra = MICRO_SPRAYS[m]
            rules.append((stage, prod, conc, None, extra))
    else:
        for stage, prod, conc, tag in BIO_SPRAYS:
            rules.append((stage, prod, conc, tag, ""))
    order = {"veg": 0, "flower": 1, "fill": 2}
    rules.sort(key=lambda r: order[r[0]])
    out = []
    for stage, prod, conc, tag, extra in rules:
        liquid = PRODUCTS[prod]["unit"] == "L"
        total = conc * litres / 1000  # kg or L
        out.append({
            "stage": stage, "product": prod, "conc": conc, "unit": "mL" if liquid else "g",
            "per_pump": conc * PUMP_L, "total_qty": total, "litres": litres,
            "pumps": max(1, math.ceil(litres / PUMP_L)), "extra": extra,
        })
    return out


# ------------------------------------------------------------------- advice ----
def weather_keys(rain_past7: float, rain_next3: float, tmax_next3: float) -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    if rain_next3 >= 30:
        out.append(("wx_heavy", {"mm": round(rain_next3)}))
    elif rain_next3 >= 5:
        out.append(("wx_good", {"mm": round(rain_next3)}))
    elif rain_past7 < 10:
        out.append(("wx_dry", {}))
    if tmax_next3 >= 37:
        out.append(("wx_hot", {"t": round(tmax_next3)}))
    return out


def advice_items(ratings: dict, crop: dict, approach: str, zone: str, irrigation: str,
                 ph: float | None, plan: dict) -> list[tuple[str, dict]]:
    items: list[tuple[str, dict]] = []
    for nut in ("n", "p", "k"):
        items.append(("adj", {"nutrient": nut, "rating": ratings[nut]}))
    items.append(("oc_low" if ratings["oc"] == "low" else "oc_ok", {}))
    if ratings.get("cec") == "low":
        items.append(("cec_low", {}))
    items.append((f"note_{approach}", {
        "pct_n": round(plan["coverage"]["n"]) if plan.get("coverage") else 0,
        "pct_p": round(plan["coverage"]["p"]) if plan.get("coverage") else 0,
        "pct_k": round(plan["coverage"]["k"]) if plan.get("coverage") else 0,
    }))
    if approach in ("partial", "organic", "natural"):
        items.append(("biofert_legume" if crop["category"] == "pulse" else "biofert_other", {}))
    if approach == "organic" and plan["totals"].get("oilcake"):
        items.append(("mix_cake", {}))
    if approach == "organic" and plan.get("coverage") and plan["coverage"]["n"] < 70:
        items.append(("org_gap", {}))
    kind = classify_ph(ph)
    if kind == "acid":
        ha = plan["area_ha"]
        lo, hi = LIME_KG_HA[0] * ha, LIME_KG_HA[1] * ha
        items.append(("ph_acid", {"ph": f"{ph:g}", "lo": f"{lo:.0f}", "hi": f"{hi:.0f}"}))
    elif kind == "ok":
        items.append(("ph_ok", {"ph": f"{ph:g}"}))
    elif kind == "alkaline":
        items.append(("ph_alk", {"ph": f"{ph:g}"}))
    for flag in ZONES[zone]["flags"]:
        if flag == "acid" and kind is not None:
            continue  # pH was measured; the specific pH advice above replaces the general line
        items.append((f"zone_{flag}", {}))
    items.append(("rainfed" if irrigation == "rainfed" else "irrigated", {}))
    items.append(("crop", {}))
    if approach in ("inorganic", "partial"):
        items.append(("basal", {}))
        if len(crop["days"]) > 1:
            items.append(("urea_tip", {}))
            if ratings["n"] == "low":
                items.append(("n_low_split", {}))
    else:
        items.append(("basal_org", {}))
    if plan["sprays"]:
        items.append(("spray_tip", {}))
    return items


# ----------------------------------------------------------------- formatting --
def fmt_qty(key: str, qty: float) -> str:
    """Farmer-friendly amount: grams / mL for small, rounded kg for large."""
    unit = PRODUCTS[key]["unit"]
    if qty <= 0.0005:
        return "-"
    if unit == "L":
        return f"{qty * 1000:.0f} mL" if qty < 1 else f"{qty:.1f} L" if qty < 100 else f"{qty:.0f} L"
    if qty < 1:
        return f"{max(10, round(qty * 100) * 10)} g"
    if qty < 100:
        return f"{qty:.1f} kg"
    return f"{round(qty / 5) * 5:.0f} kg"


def bags_text(key: str, qty: float) -> str:
    bag = PRODUCTS[key]["bag"]
    if not bag or qty <= 0:
        return "-"
    n = qty / bag
    return f"{n:.1f}" if n < 10 else f"{n:.0f}"


def fmt_gml(value: float, unit: str) -> str:
    return f"{value:g} {unit}"
