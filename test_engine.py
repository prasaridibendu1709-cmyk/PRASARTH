"""Quick checks for the calculation engine. Run:  python test_engine.py"""
import engine

crops = engine.load_crops()
assert len(crops) == 17, len(crops)
assert engine.seasons_available(crops) == ["kharif", "rabi", "zaid"]
for c in crops:
    assert abs(sum(c["split"]) - 1) < 1e-9
    assert all(c["names"][l] and c["advice"][l] for l in ("en", "hi", "bn")), c["crop"]

# The sample report: N 233.25-242.58, OC 0.91, K 170.95-184.1, P 29.26-31.92, CEC 14.8-18.5
soil = {
    "n": (233.25, 242.58),
    "oc": (0.91, 0.91),
    "k": (170.95, 184.1),
    "p": (29.26, 31.92),
    "cec": (14.8, 18.5),
}
ratings = engine.ratings_from_values(soil)
assert ratings == {"n": "low", "oc": "high", "k": "medium", "p": "high", "cec": "medium"}, ratings

wheat = next(c for c in crops if c["crop"] == "wheat" and c["season"] == "rabi")
rec = engine.recommend(wheat, ratings, 1, "acre")
d = rec["dose_ha"]
assert (d["n"], d["p"], d["k"]) == (150.0, 45.0, 40.0), d

t = rec["totals"]
ha = 0.404686
# P2O5 18.2 kg -> DAP 39.6 kg ; K2O 16.2 kg -> MOP 27.0 kg
assert abs(t["dap"] - 45 * ha / 0.46) < 1e-6
assert abs(t["mop"] - 40 * ha / 0.60) < 1e-6
# Nitrogen balance: urea N + DAP N must equal the nitrogen dose
n_from_fert = t["urea"] * engine.UREA_N + t["dap"] * engine.DAP_N
assert abs(n_from_fert - 150 * ha) < 1e-6, n_from_fert
assert len(rec["schedule"]) == 3 and rec["schedule"][0]["dap"] == t["dap"]
assert abs(sum(s["urea"] for s in rec["schedule"]) - t["urea"]) < 1e-9

# Pulses: single stage, no top-dressing
gram = next(c for c in crops if c["crop"] == "chickpea")
r2 = engine.recommend(gram, ratings, 10, "decimal")
assert len(r2["schedule"]) == 1
fert_n2 = r2["totals"]["urea"] * 0.46 + r2["totals"]["dap"] * 0.18
assert abs(fert_n2 - 20 * 1.25 * 0.0404686) < 1e-6 or r2["totals"]["urea"] == 0.0, fert_n2

# Nitrogen balance holds for every crop/rating/unit combination
for c in crops:
    for rn in ("low", "medium", "high"):
        for rp in ("low", "medium", "high"):
            rt = dict(ratings, n=rn, p=rp)
            for unit in engine.HA_PER_UNIT:
                r = engine.recommend(c, rt, 3.5, unit)
                tot = r["totals"]
                assert tot["urea"] >= 0 and tot["dap"] >= 0 and tot["mop"] >= 0
                fert_n = tot["urea"] * engine.UREA_N + tot["dap"] * engine.DAP_N
                need = r["dose_area_kg"]["n"]
                # Normally equal; if DAP alone already gives more N than needed, urea is 0
                assert abs(fert_n - need) < 1e-6 or (tot["urea"] == 0 and fert_n > need), (c["crop"], rn, rp, unit)

assert engine.fmt_amount(0) == "-"
assert engine.fmt_amount(0.034) == "30 g"
assert engine.fmt_amount(0.004) == "10 g"
assert engine.fmt_amount(39.6) == "39.6 kg"
assert engine.fmt_amount(2023) == "2025 kg"

items = engine.advice_items(ratings, wheat)
keys = [k for k, _ in items]
assert keys.count("adj") == 3 and "n_low_split" in keys and "oc_ok" in keys

print("All engine checks passed")
print(f"Sample (wheat, 1 acre): DAP {engine.fmt_amount(t['dap'])}, MOP {engine.fmt_amount(t['mop'])}, "
      f"urea {engine.fmt_amount(t['urea'])}, FYM {engine.fmt_amount(t['fym'])}")
for s in rec["schedule"]:
    print("  day", s["days"], {k: engine.fmt_amount(s[k]) for k in ("fym", "dap", "mop", "urea")})
