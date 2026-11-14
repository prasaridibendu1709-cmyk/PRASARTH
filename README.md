# Mati Sathi (मिट्टी साथी / মাটির সাথী) - version 2
Soil test -> complete crop nutrition plan, in English / हिन्दी / বাংলা. A PRASARI initiative.
(The app name is only a suggestion. Change it in `i18n.py`, the `app_name` line.)

## What is new in version 2
* New look: header with the PRASARI logo and app name, 3-step strip, numbered cards, colour chips for Low / Medium / High.
* **Four ways to feed the soil:** Chemical, Partial organic (about 25% less chemical + compost + bio-fertiliser), Complete organic (compost, oil-cake, rock phosphate / bone meal, ash) and Natural farming (Jeevamrit).
* **Special sprays:** water-soluble 19:19:19, 0:52:34, 13:0:45, calcium nitrate, borax, zinc sulphate, multi-micronutrients, DAP/urea 2% for pulses; for organic and natural farming: Jeevamrit, Panchagavya, Vermiwash. Sprays for a nutrient the soil already has in plenty are left out. Mix quantity is given per 15-litre pump.
* **Shopping list** with bags and an approximate cost, plus **When to apply** schedule.
* **State and district:** West Bengal (23 districts + 4 announced new ones), Jharkhand (24), Meghalaya (12). Each district maps to a farming zone with typical rainfall and soil problems (acidity, drought, salinity, heavy rain...), which drives the advice (liming, split doses, mulching, boron/zinc etc.).
* **Live weather** for the district (free Open-Meteo): last 7 days and next 3 days of rain. Heavy rain coming -> "do not top-dress or spray now".
* Optional soil pH, rain-fed / irrigated choice, farmer mobile, plot number, "prepared by" (Didi / CRP) and SHG name, with signature lines in the PDF.

## Files
| File | Purpose |
|---|---|
| `app.py` | The app screen |
| `engine.py` | All calculations. Settings you may tune are at the top (marked ASSUMPTION) |
| `crops.csv` | 17 crop rows (doses, split schedule, names and crop advice in 3 languages). Edit in Excel/Sheets |
| `regions.csv` | All districts: state, district, latitude, longitude, farming zone |
| `i18n.py` | All text in 3 languages |
| `pdf_report.py` | Makes the PDF |
| `assets/logo.png` | **You add this:** the PRASARI logo (see below) |
| `fonts/` | Three Noto font files (already uploaded in version 1) |
| `test_engine.py` | Self-check for the calculations |

## How to upgrade your live app (no coding)
1. Unzip `soil_advisor_v2.zip`. Put the PRASARI logo in the `assets` folder and name it exactly `logo.png` (PNG, preferably square-ish, under 500 KB).
2. Open your GitHub repository -> **Add file** -> **Upload files**. Drag in everything from the v2 folder **except the `fonts` folder** (your fonts are already there) - include `assets`. Files with the same name are replaced.
3. Click **Commit changes**. Wait one minute; your Streamlit app updates by itself. If it does not, open the app and choose **Reboot** from the menu.
4. `crops.csv` has new columns, so it must be replaced (step 2 does that).

## Installing the app on a phone
It is a web app, so there is nothing to download from the Play Store. Add it to the home screen:
* **Android (Chrome):** open the app link -> tap the **three dots** (top right) -> **Add to Home screen** (or **Install app**) -> Add. An icon appears on the home screen.
* **iPhone (Safari):** open the link in Safari -> tap **Share** -> **Add to Home Screen** -> Add.
It opens like an app from the icon, but it **needs an internet connection** (see "Next ideas").

## Before wide use - please validate (important)
* All doses in `crops.csv` and the rules in `engine.py` are **starting values**, not official recommendations. Have your agronomy team check each crop against BAU Ranchi / ICAR / State Agriculture Department / KVK recommendations.
* Organic nutrient contents are from standard tables; first-year availability factors, the 25% rule for low/high soil, spray concentrations (e.g. 0.5% = 5 g/L) and all prices are working assumptions (marked ASSUMPTION in `engine.py`). **Prices must be updated from your local market.**
* The device does not measure pH. The app therefore uses the district's typical soil condition and asks for pH only if someone measured it.
* District zones are one zone per district for simplicity. Some districts mix zones (for example parts of Murshidabad and Dakshin Dinajpur). Refine `regions.csv` with your field knowledge.
* West Bengal's four new districts (Basirhat, Sundarbans, Jangipur, Arambagh) were announced in the June 2026 state budget; check whether they have been formally notified. They are marked with * and use the parent area's zone.
* Hindi and Bengali text should be read once by a native speaker from your team.
* Open-Meteo is free for non-commercial use; check its current terms before large-scale use.

## Run on your own computer (optional)
```
pip install -r requirements.txt
streamlit run app.py
```
