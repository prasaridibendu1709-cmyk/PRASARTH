"""All on-screen and PDF text in English, Hindi and Bengali.

Each entry is (English, Hindi, Bengali). To change a sentence, edit it here.
"""
from __future__ import annotations

LANGS = ["en", "hi", "bn"]
LANG_NAMES = {"en": "English", "hi": "हिन्दी", "bn": "বাংলা"}

_T = {
    # ---- app screen --------------------------------------------------------
    "app_title": ("Soil Test → Fertiliser Advice", "मिट्टी जांच → उर्वरक सलाह", "মাটি পরীক্ষা → সারের পরামর্শ"),
    "app_sub": (
        "Upload your ScaNxt BhuParikshak report, choose your crop, and get a printable advice sheet.",
        "अपनी ScaNxt भू-परीक्षक रिपोर्ट अपलोड करें, फसल चुनें और प्रिंट योग्य सलाह पत्र पाएं।",
        "আপনার ScaNxt ভূ-পরীক্ষক রিপোর্ট আপলোড করুন, ফসল বেছে নিন এবং ছাপানোর উপযোগী পরামর্শপত্র পান।",
    ),
    "s1": ("1. Farmer details", "1. किसान की जानकारी", "1. কৃষকের তথ্য"),
    "farmer_name": ("Farmer's name", "किसान का नाम", "কৃষকের নাম"),
    "village": ("Village", "गांव", "গ্রাম"),
    "block": ("Block / District", "प्रखंड / जिला", "ব্লক / জেলা"),
    "s2": ("2. Soil test report", "2. मिट्टी जांच रिपोर्ट", "2. মাটি পরীক্ষার রিপোর্ট"),
    "upload": (
        "Upload photo or screenshot of the report",
        "रिपोर्ट की फोटो या स्क्रीनशॉट अपलोड करें",
        "রিপোর্টের ছবি বা স্ক্রিনশট আপলোড করুন",
    ),
    "read_btn": ("Read values from photo", "फोटो से मान पढ़ें", "ছবি থেকে মান পড়ুন"),
    "reading": ("Reading the report...", "रिपोर्ट पढ़ी जा रही है...", "রিপোর্ট পড়া হচ্ছে..."),
    "read_ok": (
        "Values read. Please check them against the photo and correct if needed.",
        "मान पढ़ लिए गए। कृपया फोटो से मिलाकर जांचें और जरूरत हो तो सुधारें।",
        "মান পড়া হয়েছে। অনুগ্রহ করে ছবির সঙ্গে মিলিয়ে দেখুন এবং প্রয়োজনে ঠিক করুন।",
    ),
    "read_fail": (
        "Could not read the photo automatically. Please type the values shown on the report.",
        "फोटो अपने-आप नहीं पढ़ी जा सकी। कृपया रिपोर्ट में दिखे मान खुद भरें।",
        "ছবিটি নিজে থেকে পড়া যায়নি। অনুগ্রহ করে রিপোর্টে দেখানো মানগুলি নিজে লিখুন।",
    ),
    "no_key": (
        "Automatic reading is not switched on. Please type the values shown on the report.",
        "अपने-आप पढ़ने की सुविधा चालू नहीं है। कृपया रिपोर्ट में दिखे मान खुद भरें।",
        "নিজে থেকে পড়ার সুবিধা চালু নেই। অনুগ্রহ করে রিপোর্টে দেখানো মানগুলি নিজে লিখুন।",
    ),
    "scan_date": ("Soil test date", "मिट्टी जांच की तारीख", "মাটি পরীক্ষার তারিখ"),
    "scan_id": ("Scan ID (optional)", "स्कैन आईडी (वैकल्पिक)", "স্ক্যান আইডি (ঐচ্ছিক)"),
    "values_hint": (
        "Enter the range shown on the device (lowest and highest value).",
        "डिवाइस पर दिखी रेंज भरें (सबसे कम और सबसे ज्यादा मान)।",
        "ডিভাইসে দেখানো রেঞ্জ লিখুন (সর্বনিম্ন ও সর্বোচ্চ মান)।",
    ),
    "min": ("From", "से", "থেকে"),
    "max": ("To", "तक", "পর্যন্ত"),
    "texture": ("Soil texture (optional)", "मिट्टी की बनावट (वैकल्पिक)", "মাটির গঠন (ঐচ্ছিক)"),
    "s3": ("3. Crop and land", "3. फसल और जमीन", "3. ফসল ও জমি"),
    "season": ("Season", "मौसम", "মৌসুম"),
    "crop": ("Crop", "फसल", "ফসল"),
    "area": ("Land area", "जमीन का क्षेत्रफल", "জমির পরিমাণ"),
    "unit": ("Unit", "इकाई", "একক"),
    "generate": ("Get advice", "सलाह प्राप्त करें", "পরামর্শ নিন"),
    "fill_required": (
        "Please fill in: farmer name, test date, nitrogen, organic carbon, potassium, phosphorus and land area.",
        "कृपया भरें: किसान का नाम, जांच की तारीख, नाइट्रोजन, जैविक कार्बन, पोटैशियम, फॉस्फोरस और जमीन का क्षेत्रफल।",
        "অনুগ্রহ করে লিখুন: কৃষকের নাম, পরীক্ষার তারিখ, নাইট্রোজেন, জৈব কার্বন, পটাশিয়াম, ফসফরাস ও জমির পরিমাণ।",
    ),
    "result_title": ("Your fertiliser advice", "आपकी उर्वरक सलाह", "আপনার সারের পরামর্শ"),
    "download": ("Download PDF", "PDF डाउनलोड करें", "PDF ডাউনলোড করুন"),
    "pdf_failed": (
        "The PDF could not be made: ",
        "PDF नहीं बन सका: ",
        "PDF তৈরি করা যায়নি: ",
    ),
    # ---- seasons, units, ratings -------------------------------------------
    "season_kharif": ("Kharif (Jun–Oct)", "खरीफ (जून–अक्टूबर)", "খরিফ (জুন–অক্টোবর)"),
    "season_rabi": ("Rabi (Nov–Mar)", "रबी (नवंबर–मार्च)", "রবি (নভেম্বর–মার্চ)"),
    "season_zaid": ("Zaid / Summer (Mar–Jun)", "जायद / गर्मी (मार्च–जून)", "জায়েদ / গ্রীষ্ম (মার্চ–জুন)"),
    "unit_acre": ("Acre", "एकड़", "একর"),
    "unit_hectare": ("Hectare", "हेक्टेयर", "হেক্টর"),
    "unit_decimal": ("Decimal", "डिसमिल", "শতক"),
    "unit_bigha": ("Bigha (33 decimal)", "बीघा (33 डिसमिल)", "বিঘা (33 শতক)"),
    "r_low": ("Low", "कम", "কম"),
    "r_medium": ("Medium", "मध्यम", "মাঝারি"),
    "r_high": ("High", "अधिक", "বেশি"),
    # ---- soil parameters ---------------------------------------------------
    "p_n": ("Nitrogen (N)", "नाइट्रोजन (N)", "নাইট্রোজেন (N)"),
    "p_oc": ("Organic carbon (%)", "जैविक कार्बन (%)", "জৈব কার্বন (%)"),
    "p_clay": ("Clay (%)", "चिकनी मिट्टी (%)", "কাদার পরিমাণ (%)"),
    "p_k": ("Potassium (K)", "पोटैशियम (K)", "পটাশিয়াম (K)"),
    "p_p": ("Phosphorus (P)", "फॉस्फोरस (P)", "ফসফরাস (P)"),
    "p_cec": (
        "Cation exchange (CEC)",
        "धनायन विनिमय क्षमता (CEC)",
        "ক্যাটায়ন বিনিময় ক্ষমতা (CEC)",
    ),
    # ---- PDF ---------------------------------------------------------------
    "pdf_title": ("Soil Test & Fertiliser Advice", "मिट्टी जांच एवं उर्वरक सलाह", "মাটি পরীক্ষা ও সারের পরামর্শ"),
    "pdf_advice_date": ("Advice date", "सलाह की तारीख", "পরামর্শের তারিখ"),
    "pdf_soil": ("Soil test result", "मिट्टी जांच परिणाम", "মাটি পরীক্ষার ফলাফল"),
    "col_param": ("Parameter", "जांच", "পরীক্ষা"),
    "col_value": ("Value", "मान", "মান"),
    "col_rating": ("Rating", "स्तर", "স্তর"),
    "pdf_crop": ("Crop and land", "फसल और जमीन", "ফসল ও জমি"),
    "pdf_dose": (
        "Nutrient dose after soil adjustment (kg per hectare)",
        "मिट्टी के अनुसार पोषक तत्व की मात्रा (किग्रा प्रति हेक्टेयर)",
        "মাটি অনুযায়ী পুষ্টি উপাদানের মাত্রা (কেজি প্রতি হেক্টর)",
    ),
    "pdf_fert": ("Fertiliser recommendation for your land", "आपकी जमीन के लिए उर्वरक सलाह", "আপনার জমির জন্য সারের পরামর্শ"),
    "col_when": ("When", "कब", "কখন"),
    "col_fym": ("Compost / FYM", "कम्पोस्ट / गोबर खाद", "কম্পোস্ট / গোবর সার"),
    "col_dap": ("DAP", "डीएपी (DAP)", "ডিএপি (DAP)"),
    "col_mop": ("MOP (Potash)", "एमओपी (पोटाश)", "এমওপি (পটাশ)"),
    "col_urea": ("Urea", "यूरिया (Urea)", "ইউরিয়া (Urea)"),
    "when_basal": ("At sowing / planting", "बुवाई / रोपाई के समय", "বপন / রোপণের সময়"),
    "when_days": (
        "{d} days after sowing / planting",
        "बुवाई / रोपाई के {d} दिन बाद",
        "বপন / রোপণের {d} দিন পর",
    ),
    "row_total": ("Total", "कुल", "মোট"),
    "pdf_advice": ("Special advice", "विशेष सलाह", "বিশেষ পরামর্শ"),
    "pdf_photo": ("Photo of the soil test report", "मिट्टी जांच रिपोर्ट की फोटो", "মাটি পরীক্ষার রিপোর্টের ছবি"),
    "disclaimer": (
        "This advice is a general guide based on a ScaNxt BhuParikshak scan. The scan gives indicative values. "
        "For exact advice, please consult your local agriculture officer or Krishi Vigyan Kendra (KVK).",
        "यह सलाह ScaNxt भू-परीक्षक स्कैन पर आधारित एक सामान्य मार्गदर्शन है। स्कैन के मान अनुमानित होते हैं। "
        "सटीक सलाह के लिए अपने स्थानीय कृषि अधिकारी या कृषि विज्ञान केंद्र (KVK) से संपर्क करें।",
        "এই পরামর্শ ScaNxt ভূ-পরীক্ষক স্ক্যানের উপর ভিত্তি করে একটি সাধারণ নির্দেশিকা। স্ক্যানের মান আনুমানিক। "
        "সঠিক পরামর্শের জন্য আপনার স্থানীয় কৃষি আধিকারিক বা কৃষি বিজ্ঞান কেন্দ্রের (KVK) সঙ্গে যোগাযোগ করুন।",
    ),
}

UI = {lang: {k: v[i] for k, v in _T.items()} for i, lang in enumerate(LANGS)}

# ---- advice sentences -------------------------------------------------------
_A = {
    "adj_low": (
        "{nutrient} is LOW in your soil, so the dose is increased by 25%.",
        "आपकी मिट्टी में {nutrient} कम है, इसलिए मात्रा 25% बढ़ा दी गई है।",
        "আপনার মাটিতে {nutrient} কম, তাই মাত্রা 25% বাড়ানো হয়েছে।",
    ),
    "adj_medium": (
        "{nutrient} is MEDIUM, so the standard dose is recommended.",
        "{nutrient} मध्यम है, इसलिए सामान्य मात्रा की सलाह दी गई है।",
        "{nutrient} মাঝারি, তাই স্বাভাবিক মাত্রা সুপারিশ করা হয়েছে।",
    ),
    "adj_high": (
        "{nutrient} is HIGH, so the dose is reduced by 25%. Do not add extra.",
        "{nutrient} अधिक है, इसलिए मात्रा 25% घटा दी गई है। अतिरिक्त न डालें।",
        "{nutrient} বেশি, তাই মাত্রা 25% কমানো হয়েছে। বাড়তি দেবেন না।",
    ),
    "oc_low": (
        "Organic carbon is LOW. Add more compost or farmyard manure and grow a green manure crop (like dhaincha) to improve the soil.",
        "जैविक कार्बन कम है। मिट्टी सुधारने के लिए अधिक कम्पोस्ट या गोबर की खाद डालें और हरी खाद (जैसे ढैंचा) उगाएं।",
        "জৈব কার্বন কম। মাটি ভালো করতে বেশি কম্পোস্ট বা গোবর সার দিন এবং সবুজ সার (যেমন ধৈঞ্চা) চাষ করুন।",
    ),
    "oc_ok": (
        "Organic carbon is good. Keep adding compost or farmyard manure every season to keep it that way.",
        "जैविक कार्बन अच्छा है। इसे बनाए रखने के लिए हर मौसम में कम्पोस्ट या गोबर की खाद डालते रहें।",
        "জৈব কার্বন ভালো আছে। এটি ধরে রাখতে প্রতি মৌসুমে কম্পোস্ট বা গোবর সার দিতে থাকুন।",
    ),
    "cec_low": (
        "The soil holds nutrients poorly (low CEC). Apply fertiliser in more split doses and add organic manure.",
        "मिट्टी पोषक तत्व कम रोक पाती है (कम CEC)। उर्वरक कई बार में बांटकर डालें और जैविक खाद मिलाएं।",
        "মাটি পুষ্টি কম ধরে রাখে (কম CEC)। সার কয়েক কিস্তিতে ভাগ করে দিন এবং জৈব সার মেশান।",
    ),
    "basal": (
        "Mix compost/FYM, DAP and MOP into the soil at the last ploughing or at sowing/planting.",
        "कम्पोस्ट/गोबर की खाद, डीएपी और एमओपी को आखिरी जुताई या बुवाई/रोपाई के समय मिट्टी में अच्छी तरह मिलाएं।",
        "কম্পোস্ট/গোবর সার, ডিএপি ও এমওপি শেষ চাষের সময় বা বপন/রোপণের সময় মাটিতে ভালো করে মিশিয়ে দিন।",
    ),
    "urea_tip": (
        "Apply urea only when the soil has moisture, and not just before heavy rain.",
        "यूरिया तभी डालें जब मिट्टी में नमी हो, और तेज बारिश से ठीक पहले न डालें।",
        "মাটিতে আর্দ্রতা থাকলে তবেই ইউরিয়া দিন, প্রবল বৃষ্টির ঠিক আগে দেবেন না।",
    ),
    "n_low_split": (
        "Nitrogen is low, so do not skip the urea top-dressing doses given in the schedule.",
        "नाइट्रोजन कम है, इसलिए तालिका में दी गई यूरिया टॉप ड्रेसिंग न छोड़ें।",
        "নাইট্রোজেন কম, তাই তালিকায় দেওয়া ইউরিয়া উপরি-প্রয়োগ বাদ দেবেন না।",
    ),
}
ADVICE = {lang: {k: v[i] for k, v in _A.items()} for i, lang in enumerate(LANGS)}

NUTRIENT_NAME = {
    "en": {"n": "Nitrogen", "p": "Phosphorus", "k": "Potassium"},
    "hi": {"n": "नाइट्रोजन", "p": "फॉस्फोरस", "k": "पोटैशियम"},
    "bn": {"n": "নাইট্রোজেন", "p": "ফসফরাস", "k": "পটাশিয়াম"},
}


def render_advice(lang: str, items: list[tuple[str, dict]], crop: dict) -> list[str]:
    """Turn the engine's advice items into sentences in the chosen language."""
    out = []
    for key, kw in items:
        if key == "crop":
            out.append(crop["advice"][lang])
        elif key == "adj":
            tpl = ADVICE[lang]["adj_" + kw["rating"]]
            out.append(tpl.format(nutrient=NUTRIENT_NAME[lang][kw["nutrient"]]))
        else:
            out.append(ADVICE[lang][key])
    return out
