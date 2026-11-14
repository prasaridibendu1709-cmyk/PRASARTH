# Soil Test → Fertiliser Advice (English / हिन्दी / বাংলা)

A free web app. Staff or farmers upload the ScaNxt BhuParikshak report photo, pick the crop, season and land area, and download a PDF advice sheet.

## What is inside
| File | Purpose |
|---|---|
| `app.py` | The app screen (Streamlit) |
| `engine.py` | Fertiliser calculation. Settings you may tune are at the top |
| `crops.csv` | Crop table: doses, split schedule, names and crop advice in 3 languages. Open in Excel/Sheets to edit or add crops |
| `i18n.py` | All screen and PDF text in 3 languages |
| `pdf_report.py` | Makes the PDF |
| `fonts/` | You add 3 free font files here (see `fonts/PUT_FONTS_HERE.txt`) |
| `test_engine.py` | Self-check for the calculation (`python test_engine.py`) |

## Set-up (about 30 minutes, all free; do it on a laptop)
1. **Fonts.** Download Noto Sans, Noto Sans Devanagari and Noto Sans Bengali from https://fonts.google.com/noto and copy the three `...-Regular.ttf` files into `fonts/`.
2. **GitHub.** Create a free account, make a new repository, upload everything in this folder (keep the folder structure; do not upload any real key).
3. **Photo reading key (optional but recommended).** Go to https://aistudio.google.com/app/apikey and create a free API key. Without it the app still works, staff just type the numbers from the report. Check Google's current free-tier limits and data terms before using it with real farmer photos.
4. **Deploy.** Go to https://share.streamlit.io, sign in with GitHub, choose the repository, main file `app.py`, click *Advanced settings → Secrets* and paste:
   `GEMINI_API_KEY = "your-key"`. Click Deploy.
5. **Share** the app link (and a QR code) on WhatsApp / at SHG meetings. Free apps may sleep when unused and take about half a minute to wake.

If photo reading stops working with a model-name error, add `GEMINI_MODEL = "<current model name from AI Studio>"` to Secrets.

## Run on your own computer instead
```
pip install -r requirements.txt
streamlit run app.py
```

## IMPORTANT before using with farmers
* The doses in `crops.csv` are **indicative starting values** (typical NPK recommendations for eastern India). Have your agronomy team check each crop against BAU Ranchi / ICAR / state department recommendations and edit the CSV.
* The soil adjustment (Low +25%, High −25%) and the compost adjustment are simple rules in `engine.py`. Confirm or change them.
* Rating limits (e.g. N low below 280, P high above 25) copy the ranges printed on the device screen. Phosphorus "low below 11" and the nitrogen "high above 560" limit are standard values, not shown on the screen; confirm them.
* The device gives indicative values, and the PDF says so.

## Add a new crop
Add a row in `crops.csv`. `n_split` = share of nitrogen at each stage (e.g. `50:25:25`); `n_days` = days after sowing/planting for each stage (e.g. `0:21:45`). Use `100` and `0` for a single dose at sowing.
