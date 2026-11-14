"""Self-checks for the engine. Run:  python test_engine.py"""
import engine as E

crops = E.load_crops()
regions = E.load_regions()
assert len(crops) == 17
assert len(regions) == 63, len(regions)
for st, n in (("West Bengal", 27), ("Jharkhand", 24), ("Meghalaya", 12)):
    assert len(E.districts_of(regions, st)) == n, st
assert all(r["zone"] in E.ZONES for r in regions)
assert len({(r["state"], r["district"]) for r in regions}) == 63  # no duplicates
for r in regions:  # coordinates must be inside India's north-east/east box
    assert 20 < r["lat"] < 28 and 83 < r["lon"] < 93, r
dumka = next(r for r in regions if r["district"] == "Dumka")
assert dumka["zone"] == "jh_central_ne"

# sample report from the ScaNxt screen
soil = {"n": (233.25, 242.58), "oc": (0.91, 0.91), "k": (170.95, 184.1), "p": (29.26, 31.92), "cec": (14.8, 18.5)}
ratings = E.ratings_from_values(soil)
assert ratings == {"n": "low", "oc": "high", "k": "medium", "p": "high", "cec": "medium"}, ratings

wheat = next(c for c in crops if c["crop"] == "wheat")
ha = E.ACRE_HA

# ---- inorganic: same numbers as v1 --------------------------------------------------
r = E.recommend(wheat, ratings, 1, "acre", "inorganic", acid_zone=True)
assert abs(r["totals"]["dap"] - 45 * ha / 0.46) < 1e-6
assert abs(r["totals"]["mop"] - 40 * ha / 0.60) < 1e-6
n_fert = r["totals"]["urea"] * 0.46 + r["totals"]["dap"] * 0.18
assert abs(n_fert - 150 * ha) < 1e-6
assert len(r["stages"]) == 3 and r["stages"][0]["days"] == 0

# ---- partial: 75% chemical -------------------------------------------------------------
rp = E.recommend(wheat, ratings, 1, "acre", "partial", acid_zone=True)
assert abs(rp["totals"]["dap"] - 0.75 * r["totals"]["dap"]) < 1e-6
assert abs(rp["totals"]["mop"] - 0.75 * r["totals"]["mop"]) < 1e-6
assert rp["totals"]["urea"] < r["totals"]["urea"]
assert rp["cost"] < r["cost"] + 1  # cheaper chemical bill, same compost

# ---- organic ----------------------------------------------------------------------------
ro = E.recommend(wheat, ratings, 1, "acre", "organic", acid_zone=True)
assert "urea" not in ro["totals"] and "dap" not in ro["totals"] and "mop" not in ro["totals"]
assert "oilcake" in ro["totals"] and "fym" in ro["totals"]
assert "rockp" in ro["totals"] or ro["coverage"]["p"] >= 100  # P is high here, so may be zero
assert ro["totals"]["oilcake"] <= E.MAX_OILCAKE_KG_HA * ha + 1e-6
assert 0 < ro["coverage"]["n"] < 100  # nitrogen cannot be fully met organically for wheat: honest coverage
assert ro["coverage"]["p"] >= 99.9 and ro["coverage"]["k"] >= 99.9, ro["coverage"]
# oil cake splits across stages and adds up
tot_oil = sum(q for st in ro["stages"] for k, q in st["items"] if k == "oilcake")
assert abs(tot_oil - ro["totals"]["oilcake"]) < 1e-9
# neutral soil -> bone meal instead of rock phosphate (use a low-P rating so P is needed)
low_p = dict(ratings, p="low")
rn = E.recommend(wheat, low_p, 1, "acre", "organic", acid_zone=False)
assert "bonem" in rn["totals"] and "rockp" not in rn["totals"]
ra = E.recommend(wheat, low_p, 1, "acre", "organic", acid_zone=True)
assert "rockp" in ra["totals"] and "bonem" not in ra["totals"]

# pulses are easy to cover organically (low N need)
gram = next(c for c in crops if c["crop"] == "chickpea")
rg = E.recommend(gram, ratings, 1, "acre", "organic", acid_zone=True)
assert rg["coverage"]["n"] >= 99.9, rg["coverage"]
assert len(rg["stages"]) == 1

# ---- natural farming -------------------------------------------------------------------
rnf = E.recommend(wheat, ratings, 2, "acre", "natural")
assert rnf["coverage"] is None
assert abs(rnf["totals"]["gjm"] - 2 * E.GJM_KG_PER_ACRE) < 1e-6
assert abs(rnf["totals"]["jeev"] - 2 * E.JEEV_L_PER_ACRE * len(E.NF_DAYS)) < 1e-6
assert [s["days"] for s in rnf["stages"]] == E.NF_DAYS

# ---- liming ---------------------------------------------------------------------------
rl = E.recommend(wheat, ratings, 1, "acre", "inorganic", acid_zone=True, ph=4.8)
assert abs(rl["lime_kg"] - 400 * ha) < 1e-6 and rl["totals"]["lime"] == rl["lime_kg"]
rl2 = E.recommend(wheat, ratings, 1, "acre", "inorganic", acid_zone=True, ph=5.3)
assert abs(rl2["lime_kg"] - 200 * ha) < 1e-6
rl3 = E.recommend(wheat, ratings, 1, "acre", "inorganic", acid_zone=True, ph=6.2)
assert rl3["lime_kg"] == 0 and "lime" not in rl3["totals"]
assert E.classify_ph(None) is None and E.classify_ph(5.2) == "acid" and E.classify_ph(6.5) == "ok" and E.classify_ph(8.4) == "alkaline"

# ---- sprays ---------------------------------------------------------------------------
# P rating is HIGH in the sample, so P-based sprays (MKP / DAP 2%) must be skipped
tomato = next(c for c in crops if c["crop"] == "tomato" and c["season"] == "rabi")
st = E.spray_plan(tomato, ratings, "inorganic", 1, "acre")
prods = [s["product"] for s in st]
assert "mkp" not in prods and "wsf192" in prods and "kno3" in prods and "cano3" in prods, prods
low_all = {"n": "low", "p": "low", "k": "low", "oc": "low", "cec": "low"}
st2 = E.spray_plan(tomato, low_all, "inorganic", 1, "acre")
assert "mkp" in [s["product"] for s in st2]
s0 = st2[0]
assert s0["stage"] == "veg" and s0["conc"] == 5 and abs(s0["per_pump"] - 75) < 1e-9
assert abs(s0["total_qty"] - 5 * 200 / 1000) < 1e-9 and s0["pumps"] == 14  # 200 L / 15 L = 13.3 -> 14
stg = [s["stage"] for s in st2]
assert stg == sorted(stg, key=lambda x: {"veg": 0, "flower": 1, "fill": 2}[x])
# organic sprays are liquids
so = E.spray_plan(tomato, ratings, "organic", 1, "acre")
assert [s["product"] for s in so] == ["jeevs", "panch", "vwash"] and so[0]["unit"] == "mL"
assert abs(so[0]["total_qty"] - 100 * 200 / 1000) < 1e-9  # 20 L jeevamrit per acre spray
# paddy gets zinc with lime note
paddy = next(c for c in crops if c["crop"] == "paddy")
sp = E.spray_plan(paddy, low_all, "inorganic", 1, "acre")
assert any(s["product"] == "znso4" and s["extra"] == "with_lime" for s in sp)

# ---- invariants across every crop / rating / unit / approach ------------------------------
for c in crops:
    for rn_ in ("low", "medium", "high"):
        for rp_ in ("low", "medium", "high"):
            rt = dict(ratings, n=rn_, p=rp_)
            for unit in E.HA_PER_UNIT:
                for ap in E.APPROACHES:
                    x = E.recommend(c, rt, 3.5, unit, ap, acid_zone=(rp_ == "low"))
                    assert x["cost"] >= 0
                    assert all(q >= 0 for q in x["all_totals"].values())
                    if ap in ("inorganic", "partial"):
                        share = 1.0 if ap == "inorganic" else E.PARTIAL_CHEM_SHARE
                        need = x["target"]["n"] * share
                        got = x["totals"].get("urea", 0) * 0.46 + x["totals"].get("dap", 0) * 0.18
                        assert abs(got - need) < 1e-6 or (x["totals"].get("urea", 0) == 0 and got > need), (c["crop"], ap)

# ---- weather rules ----------------------------------------------------------------------
assert E.weather_keys(5, 40, 30)[0][0] == "wx_heavy"
assert E.weather_keys(5, 12, 30)[0][0] == "wx_good"
assert E.weather_keys(2, 0, 30)[0][0] == "wx_dry"
assert E.weather_keys(50, 0, 30) == []
assert any(k == "wx_hot" for k, _ in E.weather_keys(50, 0, 40))

# ---- advice items -----------------------------------------------------------------------
for ap in E.APPROACHES:
    plan = E.recommend(wheat, ratings, 1, "acre", ap, acid_zone=True)
    items = E.advice_items(ratings, wheat, ap, "jh_central_ne", "rainfed", None, plan)
    keys = [k for k, _ in items]
    assert f"note_{ap}" in keys and "zone_acid" in keys and "rainfed" in keys and "crop" in keys, keys
items = E.advice_items(ratings, wheat, "inorganic", "jh_central_ne", "irrigated", 5.0,
                       E.recommend(wheat, ratings, 1, "acre", "inorganic", True, 5.0))
keys = [k for k, _ in items]
assert "ph_acid" in keys and "zone_acid" not in keys and "irrigated" in keys

# ---- formatting -------------------------------------------------------------------------
assert E.fmt_qty("dap", 0) == "-" and E.fmt_qty("dap", 0.034) == "30 g" and E.fmt_qty("dap", 39.6) == "39.6 kg"
assert E.fmt_qty("urea", 2023) == "2025 kg" and E.fmt_qty("jeev", 200) == "200 L" and E.fmt_qty("jeev", 0.5) == "500 mL"
assert E.bags_text("urea", 90) == "2.0" and E.bags_text("fym", 500) == "-"

print("All engine checks passed")
for ap in E.APPROACHES:
    x = E.recommend(wheat, ratings, 1, "acre", ap, acid_zone=True)
    cov = "" if not x["coverage"] else " coverage N/P/K %: " + "/".join(f"{x['coverage'][k]:.0f}" for k in "npk")
    print(f"\n{ap.upper()}  (wheat, 1 acre, sample soil)  approx cost Rs {x['cost']:.0f}{cov}")
    for s in x["stages"]:
        print("  day", s["days"], ", ".join(f"{k} {E.fmt_qty(k, q)}" for k, q in s["items"]))
    for sp_ in x["sprays"]:
        print("  spray", sp_["stage"], sp_["product"], f"{sp_['conc']:g} {sp_['unit']}/L", f"-> {E.fmt_qty(sp_['product'], sp_['total_qty'])}")
