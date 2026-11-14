"""Fertiliser calculation engine.

No Streamlit or PDF code lives here, so it can be tested on its own
(see test_engine.py). Everything an agronomist may want to tune is in the
"Settings" block just below.
"""
from __future__ import annotations

import csv
from pathlib import Path

CROPS_CSV = Path(__file__).with_name("crops.csv")

# ---- Settings (tune with your agronomist) -----------------------------------
# Dose adjustment for N, P and K according to the soil rating on the device.
RATING_FACTOR = {"low": 1.25, "medium": 1.00, "high": 0.75}
# Farmyard manure (FYM) adjustment according to the organic carbon rating.
FYM_FACTOR = {"low": 1.5, "medium": 1.0, "high": 0.75}
# Nutrient content of the fertilisers.
UREA_N = 0.46
DAP_N, DAP_P2O5 = 0.18, 0.46
MOP_K2O = 0.60
# Land units -> hectares (1 bigha = 33 decimal = 0.33 acre).
HA_PER_UNIT = {
    "hectare": 1.0,
    "acre": 0.404686,
    "decimal": 0.00404686,
    "bigha": 0.133546,
}
# (low if below first number, high if above second number). These match the
# ranges printed on the ScaNxt BhuParikshak screen.
THRESHOLDS = {
    "n": (280, 560),
    "p": (11, 25),
    "k": (120, 280),
    "oc": (0.5, 0.75),
    "cec": (12, 25),
}
# ------------------------------------------------------------------------------

SEASON_ORDER = ["kharif", "rabi", "zaid"]


def load_crops(path: Path = CROPS_CSV) -> list[dict]:
    """Read crops.csv into a list of dicts."""
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
            total = sum(split)
            crops.append(
                {
                    "crop": r["crop"],
                    "season": r["season"].lower(),
                    "n": float(r["n"]),
                    "p": float(r["p2o5"]),
                    "k": float(r["k2o"]),
                    "fym": float(r["fym_t_ha"]),
                    "split": [x / total for x in split],
                    "days": days,
                    "names": {l: r[f"name_{l}"] for l in ("en", "hi", "bn")},
                    "advice": {l: r[f"advice_{l}"] for l in ("en", "hi", "bn")},
                }
            )
    return crops


def seasons_available(crops: list[dict]) -> list[str]:
    present = {c["season"] for c in crops}
    return [s for s in SEASON_ORDER if s in present]


def crops_for_season(crops: list[dict], season: str) -> list[dict]:
    return [c for c in crops if c["season"] == season]


def classify(param: str, value: float) -> str:
    """Return 'low', 'medium' or 'high' for a soil parameter value."""
    lo, hi = THRESHOLDS[param]
    if value < lo:
        return "low"
    if value > hi:
        return "high"
    return "medium"


def ratings_from_values(soil: dict) -> dict:
    """soil: {'n': (min, max), ...} -> {'n': 'low', ...} using the mid value."""
    out = {}
    for param in THRESHOLDS:
        if param in soil:
            lo, hi = soil[param]
            out[param] = classify(param, (lo + hi) / 2)
    return out


def recommend(crop: dict, ratings: dict, area: float, unit: str) -> dict:
    """Work out the fertiliser quantities for the given land."""
    ha = area * HA_PER_UNIT[unit]
    dose_ha = {x: crop[x] * RATING_FACTOR[ratings[x]] for x in ("n", "p", "k")}
    n_kg, p_kg, k_kg = (dose_ha[x] * ha for x in ("n", "p", "k"))

    dap = p_kg / DAP_P2O5
    dap_n = dap * DAP_N
    mop = k_kg / MOP_K2O

    # The nitrogen in DAP counts towards the first (basal) nitrogen share.
    urea_n_total = max(0.0, n_kg - dap_n)
    stage_n = [n_kg * f for f in crop["split"]]
    stage_n[0] = max(0.0, stage_n[0] - dap_n)
    s = sum(stage_n)
    scale = urea_n_total / s if s > 0 else 0.0
    urea_stage = [x * scale / UREA_N for x in stage_n]

    fym = crop["fym"] * 1000 * ha * FYM_FACTOR[ratings["oc"]]

    schedule = []
    for i, (d, urea) in enumerate(zip(crop["days"], urea_stage)):
        schedule.append(
            {
                "days": d,
                "fym": fym if i == 0 else 0.0,
                "dap": dap if i == 0 else 0.0,
                "mop": mop if i == 0 else 0.0,
                "urea": urea,
            }
        )
    return {
        "area_ha": ha,
        "ratings": ratings,
        "base_ha": {x: crop[x] for x in ("n", "p", "k")},
        "dose_ha": dose_ha,
        "dose_area_kg": {"n": n_kg, "p": p_kg, "k": k_kg},
        "totals": {"fym": fym, "dap": dap, "mop": mop, "urea": sum(urea_stage)},
        "schedule": schedule,
    }


def advice_items(ratings: dict, crop: dict) -> list[tuple[str, dict]]:
    """Which advice lines apply. Text lives in i18n.py (render_advice)."""
    items: list[tuple[str, dict]] = []
    for nut in ("n", "p", "k"):
        items.append(("adj", {"nutrient": nut, "rating": ratings[nut]}))
    items.append(("oc_low" if ratings["oc"] == "low" else "oc_ok", {}))
    if ratings.get("cec") == "low":
        items.append(("cec_low", {}))
    items.append(("crop", {}))
    items.append(("basal", {}))
    if len(crop["days"]) > 1:
        items.append(("urea_tip", {}))
        if ratings["n"] == "low":
            items.append(("n_low_split", {}))
    return items


def fmt_amount(kg: float) -> str:
    """Farmer-friendly amount: grams for small, rounded kg for large."""
    if kg <= 0.0005:
        return "-"
    if kg < 1:
        return f"{max(10, round(kg * 100) * 10)} g"
    if kg < 100:
        return f"{kg:.1f} kg"
    return f"{round(kg / 5) * 5:.0f} kg"
