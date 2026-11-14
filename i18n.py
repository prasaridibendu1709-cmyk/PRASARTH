"""All on-screen and PDF text in English, Hindi and Bengali.

Each entry is (English, Hindi, Bengali). To change a sentence, edit it here.
NOTE: Hindi and Bengali wording should be read once by a native speaker from your team.
"""
from __future__ import annotations

LANGS = ["en", "hi", "bn"]
LANG_NAMES = {"en": "English", "hi": "हिन्दी", "bn": "বাংলা"}
ORG_NAME = "PRASARI"

_T = {
    # ---- name, header ------------------------------------------------------
    "app_name": (""PRASARTH""),
    "app_tag": (
        "Soil test to complete crop nutrition plan",
        "मिट्टी जांच से पूरी फसल पोषण योजना",
        "মাটি পরীক্ষা থেকে সম্পূর্ণ ফসল পুষ্টি পরিকল্পনা",
    ),
    "org_line": ("A PRASARI initiative", "प्रसारी की एक पहल", "প্রসারীর একটি উদ্যোগ"),
    "how1": ("Test the soil", "मिट्टी जांचें", "মাটি পরীক্ষা করুন"),
    "how2": ("Fill the details", "जानकारी भरें", "তথ্য দিন"),
    "how3": ("Print the plan", "योजना प्रिंट करें", "পরিকল্পনা ছাপুন"),
    # ---- sections ----------------------------------------------------------
    "s1": ("Farmer details", "किसान की जानकारी", "কৃষকের তথ্য"),
    "s2": ("Place", "स्थान", "স্থান"),
    "s3": ("Soil test report", "मिट्टी जांच रिपोर्ट", "মাটি পরীক্ষার রিপোর্ট"),
    "s4": ("Crop and land", "फसल और जमीन", "ফসল ও জমি"),
    "s5": ("How do you want to feed the soil?", "आप मिट्टी को पोषण कैसे देना चाहते हैं?", "আপনি মাটিকে কীভাবে পুষ্টি দিতে চান?"),
    "more": ("More details (optional)", "अधिक जानकारी (वैकल्पिक)", "আরও তথ্য (ঐচ্ছিক)"),
    # ---- farmer / place ----------------------------------------------------
    "farmer_name": ("Farmer's name", "किसान का नाम", "কৃষকের নাম"),
    "village": ("Village", "गांव", "গ্রাম"),
    "block": ("Block", "प्रखंड", "ব্লক"),
    "mobile": ("Farmer's mobile number", "किसान का मोबाइल नंबर", "কৃষকের মোবাইল নম্বর"),
    "plot": ("Plot / Khata number", "प्लॉट / खाता नंबर", "প্লট / খতিয়ান নম্বর"),
    "prepared_by": ("Report prepared by (Didi / CRP name)", "रिपोर्ट बनाने वाले का नाम (दीदी / सीआरपी)", "রিপোর্ট তৈরি করেছেন (দিদি / সিআরপি)"),
    "shg": ("SHG / organisation", "स्वयं सहायता समूह / संस्था", "স্বনির্ভর গোষ্ঠী / সংস্থা"),
    "state": ("State", "राज्य", "রাজ্য"),
    "district": ("District", "जिला", "জেলা"),
    "district_new": ("new district, announced 2026", "नया जिला, 2026 में घोषित", "নতুন জেলা, 2026-এ ঘোষিত"),
    "irrigation": ("Water for the crop", "फसल के लिए पानी", "ফসলের জন্য জল"),
    "irr_rainfed": ("Rain only (rainfed)", "केवल बारिश (वर्षा आधारित)", "শুধু বৃষ্টি (বৃষ্টিনির্ভর)"),
    "irr_irrigated": ("Irrigation available", "सिंचाई उपलब्ध", "সেচের সুবিধা আছে"),
    "ph_label": ("Soil pH (optional - only if you measured it)", "मिट्टी का pH (वैकल्पिक - अगर मापा हो)", "মাটির pH (ঐচ্ছিক - মাপা থাকলে)"),
    "state_n_districts": ("districts", "जिले", "জেলা"),
    "zone_label": ("Farming zone", "कृषि क्षेत्र", "কৃষি অঞ্চল"),
    "rain_label": ("Typical rainfall", "सामान्य वर्षा", "সাধারণ বৃষ্টিপাত"),
    "ph_typ": ("Typical soil pH", "सामान्य मिट्टी pH", "সাধারণ মাটির pH"),
    "ph_unknown": ("mostly acidic", "ज्यादातर अम्लीय", "বেশিরভাগ অম্লীয়"),
    # ---- weather -----------------------------------------------------------
    "wx_title": ("Weather near you", "आपके पास का मौसम", "আপনার এলাকার আবহাওয়া"),
    "wx_past": ("Rain in last 7 days", "पिछले 7 दिनों की बारिश", "গত 7 দিনের বৃষ্টি"),
    "wx_next": ("Rain expected, next 3 days", "अगले 3 दिन संभावित बारिश", "আগামী 3 দিনে সম্ভাব্য বৃষ্টি"),
    "wx_temp": ("Hottest day ahead", "आगे का सबसे गर्म दिन", "সামনের সবচেয়ে গরম দিন"),
    "wx_fail": ("Weather could not be loaded (internet needed). The plan is still valid.", "मौसम नहीं मिल सका (इंटरनेट चाहिए)। योजना फिर भी सही है।", "আবহাওয়া আনা যায়নি (ইন্টারনেট লাগবে)। পরিকল্পনা তবুও ঠিক আছে।"),
    # ---- soil report -------------------------------------------------------
    "upload": ("Upload photo or screenshot of the report (optional)", "रिपोर्ट की फोटो या स्क्रीनशॉट अपलोड करें (वैकल्पिक)", "রিপোর্টের ছবি বা স্ক্রিনশট আপলোড করুন (ঐচ্ছিক)"),
    "read_btn": ("Try to read values from photo", "फोटो से मान पढ़ने की कोशिश करें", "ছবি থেকে মান পড়ার চেষ্টা করুন"),
    "reading": ("Reading the report...", "रिपोर्ट पढ़ी जा रही है...", "রিপোর্ট পড়া হচ্ছে..."),
    "read_ok": ("Values read. Please check them against the photo and correct if needed.", "मान पढ़ लिए गए। कृपया फोटो से मिलाकर जांचें और जरूरत हो तो सुधारें।", "মান পড়া হয়েছে। অনুগ্রহ করে ছবির সঙ্গে মিলিয়ে দেখুন এবং প্রয়োজনে ঠিক করুন।"),
    "read_fail": ("Could not read the photo automatically. Please type the values shown on the report.", "फोटो अपने-आप नहीं पढ़ी जा सकी। कृपया रिपोर्ट में दिखे मान खुद भरें।", "ছবিটি নিজে থেকে পড়া যায়নি। অনুগ্রহ করে রিপোর্টে দেখানো মানগুলি নিজে লিখুন।"),
    "no_key": ("Automatic reading is not switched on. Please type the values shown on the report.", "अपने-आप पढ़ने की सुविधा चालू नहीं है। कृपया रिपोर्ट में दिखे मान खुद भरें।", "নিজে থেকে পড়ার সুবিধা চালু নেই। অনুগ্রহ করে রিপোর্টে দেখানো মানগুলি নিজে লিখুন।"),
    "tech": ("Technical details (send to the app team)", "तकनीकी जानकारी (ऐप टीम को भेजें)", "প্রযুক্তিগত তথ্য (অ্যাপ টিমকে পাঠান)"),
    "scan_date": ("Soil test date", "मिट्टी जांच की तारीख", "মাটি পরীক্ষার তারিখ"),
    "scan_id": ("Scan ID (optional)", "स्कैन आईडी (वैकल्पिक)", "স্ক্যান আইডি (ঐচ্ছিক)"),
    "values_hint": ("Enter the range shown on the device (lowest and highest value).", "डिवाइस पर दिखी रेंज भरें (सबसे कम और सबसे ज्यादा मान)।", "ডিভাইসে দেখানো রেঞ্জ লিখুন (সর্বনিম্ন ও সর্বোচ্চ মান)।"),
    "min": ("From", "से", "থেকে"),
    "max": ("To", "तक", "পর্যন্ত"),
    "texture": ("Soil texture (optional)", "मिट्टी की बनावट (वैकल्पिक)", "মাটির গঠন (ঐচ্ছিক)"),
    # ---- crop --------------------------------------------------------------
    "season": ("Season", "मौसम", "মৌসুম"),
    "crop": ("Crop", "फसल", "ফসল"),
    "area": ("Land area", "जमीन का क्षेत्रफल", "জমির পরিমাণ"),
    "unit": ("Unit", "इकाई", "একক"),
    "season_kharif": ("Kharif (Jun-Oct)", "खरीफ (जून-अक्टूबर)", "খরিফ (জুন-অক্টোবর)"),
    "season_rabi": ("Rabi (Nov-Mar)", "रबी (नवंबर-मार्च)", "রবি (নভেম্বর-মার্চ)"),
    "season_zaid": ("Zaid / Summer (Mar-Jun)", "जायद / गर्मी (मार्च-जून)", "জায়েদ / গ্রীষ্ম (মার্চ-জুন)"),
    "unit_acre": ("Acre", "एकड़", "একর"),
    "unit_hectare": ("Hectare", "हेक्टेयर", "হেক্টর"),
    "unit_decimal": ("Decimal", "डिसमिल", "শতক"),
    "unit_bigha": ("Bigha (33 decimal)", "बीघा (33 डिसमिल)", "বিঘা (33 শতক)"),
    # ---- approaches --------------------------------------------------------
    "ap_inorganic": ("🧪 Chemical (inorganic)", "🧪 रासायनिक (अकार्बनिक)", "🧪 রাসায়নিক (অজৈব)"),
    "ap_partial": ("🌗 Partial organic (integrated)", "🌗 आंशिक जैविक (समन्वित)", "🌗 আংশিক জৈব (সমন্বিত)"),
    "ap_organic": ("🌿 Complete organic", "🌿 पूर्ण जैविक", "🌿 সম্পূর্ণ জৈব"),
    "ap_natural": ("🐄 Natural farming (Jeevamrit)", "🐄 प्राकृतिक खेती (जीवामृत)", "🐄 প্রাকৃতিক চাষ (জীবামৃত)"),
    "apc_inorganic": (
        "Urea, DAP and potash worked out from your soil test, plus compost. Quick results.",
        "मिट्टी जांच के अनुसार यूरिया, डीएपी, पोटाश और साथ में कम्पोस्ट। तेज असर।",
        "মাটি পরীক্ষা অনুযায়ী ইউরিয়া, ডিএপি, পটাশ এবং সঙ্গে কম্পোস্ট। দ্রুত ফল।",
    ),
    "apc_partial": (
        "Compost + bio-fertiliser + about 25% less chemical. Saves money and builds the soil.",
        "कम्पोस्ट + जैव उर्वरक + रासायनिक लगभग 25% कम। खर्च बचाए, मिट्टी सुधारे।",
        "কম্পোস্ট + জৈব সার + রাসায়নিক প্রায় 25% কম। খরচ বাঁচায়, মাটি ভালো করে।",
    ),
    "apc_organic": (
        "Only compost, oil-cake, rock phosphate and ash. No chemicals. Slower, but the soil gets better every year.",
        "सिर्फ कम्पोस्ट, खली, रॉक फॉस्फेट और राख। कोई रसायन नहीं। असर धीमा, पर मिट्टी हर साल बेहतर।",
        "শুধু কম্পোস্ট, খোল, রক ফসফেট ও ছাই। কোনো রাসায়নিক নয়। ধীরে কাজ করে, কিন্তু প্রতি বছর মাটি ভালো হয়।",
    ),
    "apc_natural": (
        "Home-made Jeevamrit and Ghanjeevamrit from cow dung, urine and jaggery. Lowest cost.",
        "गोबर, गोमूत्र और गुड़ से घर पर बने जीवामृत और घनजीवामृत। सबसे कम खर्च।",
        "গোবর, গোমূত্র ও গুড় দিয়ে ঘরে বানানো জীবামৃত ও ঘনজীবামৃত। সবচেয়ে কম খরচ।",
    ),
    "generate": ("Make my plan", "मेरी योजना बनाएं", "আমার পরিকল্পনা বানান"),
    "fill_required": (
        "Please fill in: farmer name, place, test date, nitrogen, organic carbon, potassium, phosphorus and land area.",
        "कृपया भरें: किसान का नाम, स्थान, जांच की तारीख, नाइट्रोजन, जैविक कार्बन, पोटैशियम, फॉस्फोरस और जमीन का क्षेत्रफल।",
        "অনুগ্রহ করে লিখুন: কৃষকের নাম, স্থান, পরীক্ষার তারিখ, নাইট্রোজেন, জৈব কার্বন, পটাশিয়াম, ফসফরাস ও জমির পরিমাণ।",
    ),
    # ---- soil parameters / ratings ----------------------------------------
    "p_n": ("Nitrogen (N)", "नाइट्रोजन (N)", "নাইট্রোজেন (N)"),
    "p_oc": ("Organic carbon (%)", "जैविक कार्बन (%)", "জৈব কার্বন (%)"),
    "p_clay": ("Clay (%)", "चिकनी मिट्टी (%)", "কাদার পরিমাণ (%)"),
    "p_k": ("Potassium (K)", "पोटैशियम (K)", "পটাশিয়াম (K)"),
    "p_p": ("Phosphorus (P)", "फॉस्फोरस (P)", "ফসফরাস (P)"),
    "p_cec": ("Cation exchange (CEC)", "धनायन विनिमय क्षमता (CEC)", "ক্যাটায়ন বিনিময় ক্ষমতা (CEC)"),
    "r_low": ("Low", "कम", "কম"),
    "r_medium": ("Medium", "मध्यम", "মাঝারি"),
    "r_high": ("High", "अधिक", "বেশি"),
    # ---- results -----------------------------------------------------------
    "result_title": ("Your crop nutrition plan", "आपकी फसल पोषण योजना", "আপনার ফসল পুষ্টি পরিকল্পনা"),
    "tab_buy": ("🛒 What to buy", "🛒 क्या खरीदें", "🛒 কী কিনবেন"),
    "tab_when": ("📅 When to apply", "📅 कब डालें", "📅 কখন দেবেন"),
    "tab_spray": ("💦 Sprays", "💦 छिड़काव", "💦 স্প্রে"),
    "tab_advice": ("💡 Advice", "💡 सलाह", "💡 পরামর্শ"),
    "col_product": ("Product", "सामग्री", "সামগ্রী"),
    "col_qty": ("Quantity for your land", "आपकी जमीन के लिए मात्रा", "আপনার জমির জন্য পরিমাণ"),
    "col_bags": ("Bags", "बोरी", "বস্তা"),
    "col_cost": ("About Rs", "लगभग रु.", "প্রায় টাকা"),
    "total_cost": ("Approximate total cost", "अनुमानित कुल खर्च", "আনুমানিক মোট খরচ"),
    "cost_note": (
        "Prices are only a guide (government-fixed for urea/DAP, shop price for others). Compost, ash and home-made inputs are free if you make them yourself.",
        "कीमतें केवल अनुमान हैं (यूरिया/डीएपी की सरकारी दर, बाकी की दुकान की दर)। कम्पोस्ट, राख और घर के बने घोल खुद बनाएं तो मुफ्त।",
        "দাম শুধু আন্দাজ (ইউরিয়া/ডিএপি সরকারি দর, বাকিগুলো দোকানের দর)। কম্পোস্ট, ছাই ও ঘরে বানানো জিনিস নিজে বানালে বিনামূল্যে।",
    ),
    "col_when": ("When", "कब", "কখন"),
    "when_basal": ("At sowing / planting", "बुवाई / रोपाई के समय", "বপন / রোপণের সময়"),
    "when_days": ("{d} days after sowing / planting", "बुवाई / रोपाई के {d} दिन बाद", "বপন / রোপণের {d} দিন পর"),
    "row_total": ("Total", "कुल", "মোট"),
    "cov_title": ("How much of the crop's need this plan supplies", "यह योजना फसल की कितनी जरूरत पूरी करती है", "এই পরিকল্পনা ফসলের কতটা চাহিদা মেটায়"),
    "cov_n": ("Nitrogen", "नाइट्रोजन", "নাইট্রোজেন"),
    "cov_p": ("Phosphorus", "फॉस्फोरस", "ফসফরাস"),
    "cov_k": ("Potash", "पोटाश", "পটাশ"),
    "sp_stage": ("Crop stage", "फसल की अवस्था", "ফসলের পর্যায়"),
    "sp_product": ("Spray", "छिड़काव", "স্প্রে"),
    "sp_pump": ("Mix in one 15-litre pump", "एक 15 लीटर पंप में मिलाएं", "একটি 15 লিটার পাম্পে মেশান"),
    "sp_total": ("Total for your land", "आपकी जमीन के लिए कुल", "আপনার জমির জন্য মোট"),
    "sp_pumps": ("Pumps", "पंप", "পাম্প"),
    "sp_none": ("No spray needed for this plan.", "इस योजना में छिड़काव जरूरी नहीं।", "এই পরিকল্পনায় স্প্রে দরকার নেই।"),
    "stg_veg": ("Leafy growth stage", "पत्तियों के बढ़ने की अवस्था", "পাতা বাড়ার পর্যায়"),
    "stg_flower": ("Flowering", "फूल आने पर", "ফুল আসার সময়"),
    "stg_fill": ("Fruit / grain / pod filling", "फल / दाना / फली भरते समय", "ফল / দানা / শুঁটি ভরার সময়"),
    "with_lime": ("+ slaked lime 2.5 g per litre", "+ बुझा चूना 2.5 ग्राम प्रति लीटर", "+ কলিচুন প্রতি লিটারে 2.5 গ্রাম"),
    "download": ("Download PDF report", "PDF रिपोर्ट डाउनलोड करें", "PDF রিপোর্ট ডাউনলোড করুন"),
    "pdf_failed": ("The PDF could not be made: ", "PDF नहीं बन सका: ", "PDF তৈরি করা যায়নি: "),
    # ---- PDF ---------------------------------------------------------------
    "pdf_title": ("Soil Test & Crop Nutrition Plan", "मिट्टी जांच एवं फसल पोषण योजना", "মাটি পরীক্ষা ও ফসল পুষ্টি পরিকল্পনা"),
    "pdf_advice_date": ("Plan date", "योजना की तारीख", "পরিকল্পনার তারিখ"),
    "pdf_place": ("Place and conditions", "स्थान और परिस्थिति", "স্থান ও পরিস্থিতি"),
    "pdf_soil": ("Soil test result", "मिट्टी जांच परिणाम", "মাটি পরীক্ষার ফলাফল"),
    "col_param": ("Parameter", "जांच", "পরীক্ষা"),
    "col_value": ("Value", "मान", "মান"),
    "col_rating": ("Rating", "स्तर", "স্তর"),
    "pdf_crop": ("Crop, land and approach", "फसल, जमीन और तरीका", "ফসল, জমি ও পদ্ধতি"),
    "approach": ("Approach", "तरीका", "পদ্ধতি"),
    "pdf_dose": ("Nutrient need after soil adjustment (kg per hectare)", "मिट्टी के अनुसार पोषक तत्व की जरूरत (किग्रा प्रति हेक्टेयर)", "মাটি অনুযায়ী পুষ্টি উপাদানের প্রয়োজন (কেজি প্রতি হেক্টর)"),
    "pdf_buy": ("What to buy (shopping list)", "क्या खरीदें (खरीद सूची)", "কী কিনবেন (কেনার তালিকা)"),
    "pdf_when": ("When and how much to apply", "कब और कितना डालें", "কখন ও কত দেবেন"),
    "pdf_spray": ("Spray plan (water-soluble / liquid)", "छिड़काव योजना (पानी में घुलनशील / तरल)", "স্প্রে পরিকল্পনা (জলে দ্রবণীয় / তরল)"),
    "pdf_advice": ("Special advice for you", "आपके लिए विशेष सलाह", "আপনার জন্য বিশেষ পরামর্শ"),
    "pdf_photo": ("Photo of the soil test report", "मिट्टी जांच रिपोर्ट की फोटो", "মাটি পরীক্ষার রিপোর্টের ছবি"),
    "sign_prepared": ("Prepared by", "रिपोर्ट बनाने वाले", "রিপোর্ট তৈরি করেছেন"),
    "sign_farmer": ("Farmer's signature", "किसान के हस्ताक्षर", "কৃষকের স্বাক্ষর"),
    "disclaimer": (
        "This plan is a general guide based on a ScaNxt BhuParikshak scan; the scan gives indicative values and the doses are general recommendations. "
        "For exact advice, please consult your local agriculture officer or Krishi Vigyan Kendra (KVK).",
        "यह योजना ScaNxt भू-परीक्षक स्कैन पर आधारित एक सामान्य मार्गदर्शन है; स्कैन के मान अनुमानित होते हैं और मात्राएं सामान्य सिफारिशें हैं। "
        "सटीक सलाह के लिए अपने स्थानीय कृषि अधिकारी या कृषि विज्ञान केंद्र (KVK) से संपर्क करें।",
        "এই পরিকল্পনা ScaNxt ভূ-পরীক্ষক স্ক্যানের উপর ভিত্তি করে একটি সাধারণ নির্দেশিকা; স্ক্যানের মান আনুমানিক এবং মাত্রাগুলি সাধারণ সুপারিশ। "
        "সঠিক পরামর্শের জন্য আপনার স্থানীয় কৃষি আধিকারিক বা কৃষি বিজ্ঞান কেন্দ্রের (KVK) সঙ্গে যোগাযোগ করুন।",
    ),
}
UI = {lang: {k: v[i] for k, v in _T.items()} for i, lang in enumerate(LANGS)}

STATE_NAMES = {
    "en": {"West Bengal": "West Bengal", "Jharkhand": "Jharkhand", "Meghalaya": "Meghalaya"},
    "hi": {"West Bengal": "पश्चिम बंगाल", "Jharkhand": "झारखंड", "Meghalaya": "मेघालय"},
    "bn": {"West Bengal": "পশ্চিমবঙ্গ", "Jharkhand": "ঝাড়খণ্ড", "Meghalaya": "মেঘালয়"},
}

_Z = {
    "wb_hill": ("Hill zone (Darjeeling-Kalimpong)", "पहाड़ी क्षेत्र (दार्जिलिंग-कलिम्पोंग)", "পাহাড়ি অঞ্চল (দার্জিলিং-কালিম্পং)"),
    "wb_terai": ("Terai and Teesta alluvial zone", "तराई एवं तीस्ता जलोढ़ क्षेत्र", "তরাই ও তিস্তা পলল অঞ্চল"),
    "wb_new_alluvial": ("Gangetic (new) alluvial zone", "गंगा का नया जलोढ़ क्षेत्र", "গাঙ্গেয় (নতুন) পলল অঞ্চল"),
    "wb_old_alluvial": ("Old alluvial zone", "पुराना जलोढ़ क्षेत्र", "প্রাচীন পলল অঞ্চল"),
    "wb_laterite": ("Red laterite and gravelly zone", "लाल लैटेराइट एवं कंकरीला क्षेत्र", "লাল ল্যাটেরাইট ও কাঁকুরে অঞ্চল"),
    "wb_coastal": ("Coastal saline zone", "तटीय लवणीय क्षेत्र", "উপকূলীয় লবণাক্ত অঞ্চল"),
    "jh_central_ne": ("Central and North-Eastern Plateau", "मध्य एवं उत्तर-पूर्वी पठार", "মধ্য ও উত্তর-পূর্ব মালভূমি"),
    "jh_western": ("Western Plateau", "पश्चिमी पठार", "পশ্চিম মালভূমি"),
    "jh_southeast": ("South-Eastern Plateau", "दक्षिण-पूर्वी पठार", "দক্ষিণ-পূর্ব মালভূমি"),
    "ml_khasi": ("Khasi Hills region", "खासी पहाड़ी क्षेत्र", "খাসি পাহাড় অঞ্চল"),
    "ml_jaintia": ("Jaintia Hills region", "जयंतिया पहाड़ी क्षेत्र", "জয়ন্তিয়া পাহাড় অঞ্চল"),
    "ml_garo": ("Garo Hills region", "गारो पहाड़ी क्षेत्र", "গারো পাহাড় অঞ্চল"),
}
ZONE_NAMES = {lang: {k: v[i] for k, v in _Z.items()} for i, lang in enumerate(LANGS)}

# ---- product names ----------------------------------------------------------
_P = {
    "urea": ("Urea", "यूरिया", "ইউরিয়া"),
    "dap": ("DAP", "डीएपी (DAP)", "ডিএপি (DAP)"),
    "mop": ("MOP (Potash)", "एमओपी (पोटाश)", "এমওপি (পটাশ)"),
    "fym": ("Compost / FYM (cow-dung manure)", "कम्पोस्ट / गोबर की खाद", "কম্পোস্ট / গোবর সার"),
    "oilcake": ("Neem / mustard cake (khali)", "नीम / सरसों की खली", "নিম / সরষের খোল"),
    "rockp": ("Rock phosphate", "रॉक फॉस्फेट", "রক ফসফেট"),
    "bonem": ("Bone meal", "हड्डी का चूरा", "হাড়ের গুঁড়ো"),
    "ash": ("Wood / plant ash", "लकड़ी / पौधों की राख", "কাঠ / গাছের ছাই"),
    "lime": ("Agricultural lime (in furrow)", "कृषि चूना (कूंड में)", "কৃষি চুন (নালায়)"),
    "gjm": ("Ghanjeevamrit", "घनजीवामृत", "ঘনজীবামৃত"),
    "jeev": ("Jeevamrit (liquid, with irrigation)", "जीवामृत (तरल, सिंचाई के साथ)", "জীবামৃত (তরল, সেচের সঙ্গে)"),
    "wsf192": ("19:19:19 water-soluble NPK", "19:19:19 पानी में घुलनशील NPK", "19:19:19 জলে দ্রবণীয় NPK"),
    "mkp": ("0:52:34 (MKP) water-soluble", "0:52:34 (एमकेपी) घुलनशील", "0:52:34 (এমকেপি) দ্রবণীয়"),
    "kno3": ("13:0:45 potassium nitrate", "13:0:45 पोटैशियम नाइट्रेट", "13:0:45 পটাশিয়াম নাইট্রেট"),
    "cano3": ("Calcium nitrate", "कैल्शियम नाइट्रेट", "ক্যালসিয়াম নাইট্রেট"),
    "borax": ("Borax", "बोरेक्स", "বোরাক্স"),
    "znso4": ("Zinc sulphate", "जिंक सल्फेट", "জিঙ্ক সালফেট"),
    "micro": ("Multi-micronutrient mixture", "मल्टी-माइक्रोन्यूट्रिएंट मिश्रण", "মাল্টি-মাইক্রোনিউট্রিয়েন্ট মিশ্রণ"),
    "dap2": ("DAP 2% (soak overnight, spray the clear liquid)", "डीएपी 2% (रात भर भिगोएं, साफ घोल छिड़कें)", "ডিএপি 2% (রাতভর ভিজিয়ে রাখুন, পরিষ্কার জল স্প্রে করুন)"),
    "urea2": ("Urea 2% solution", "यूरिया 2% घोल", "ইউরিয়া 2% দ্রবণ"),
    "panch": ("Panchagavya 3%", "पंचगव्य 3%", "পঞ্চগব্য 3%"),
    "vwash": ("Vermiwash (1:10)", "वर्मीवॉश (1:10)", "ভার্মিওয়াশ (1:10)"),
    "jeevs": ("Jeevamrit spray (1:10)", "जीवामृत छिड़काव (1:10)", "জীবামৃত স্প্রে (1:10)"),
}
PRODUCT_NAMES = {lang: {k: v[i] for k, v in _P.items()} for i, lang in enumerate(LANGS)}

# ---- advice sentences -------------------------------------------------------
_A = {
    "adj_low": ("{nutrient} is LOW in your soil, so the dose is increased by 25%.", "आपकी मिट्टी में {nutrient} कम है, इसलिए मात्रा 25% बढ़ा दी गई है।", "আপনার মাটিতে {nutrient} কম, তাই মাত্রা 25% বাড়ানো হয়েছে।"),
    "adj_medium": ("{nutrient} is MEDIUM, so the standard dose is recommended.", "{nutrient} मध्यम है, इसलिए सामान्य मात्रा की सलाह दी गई है।", "{nutrient} মাঝারি, তাই স্বাভাবিক মাত্রা সুপারিশ করা হয়েছে।"),
    "adj_high": ("{nutrient} is HIGH, so the dose is reduced by 25% and sprays for it are left out. Do not add extra.", "{nutrient} अधिक है, इसलिए मात्रा 25% घटा दी गई है और उसका छिड़काव छोड़ा गया है। अतिरिक्त न डालें।", "{nutrient} বেশি, তাই মাত্রা 25% কমানো হয়েছে এবং তার স্প্রে বাদ দেওয়া হয়েছে। বাড়তি দেবেন না।"),
    "oc_low": ("Organic carbon is LOW. Add more compost or farmyard manure and grow a green-manure crop (dhaincha / sunhemp) to improve the soil.", "जैविक कार्बन कम है। मिट्टी सुधारने के लिए अधिक कम्पोस्ट या गोबर की खाद डालें और हरी खाद (ढैंचा / सनई) उगाएं।", "জৈব কার্বন কম। মাটি ভালো করতে বেশি কম্পোস্ট বা গোবর সার দিন এবং সবুজ সার (ধৈঞ্চা / শন) চাষ করুন।"),
    "oc_ok": ("Organic carbon is good. Keep adding compost or farmyard manure every season to keep it that way.", "जैविक कार्बन अच्छा है। इसे बनाए रखने के लिए हर मौसम में कम्पोस्ट या गोबर की खाद डालते रहें।", "জৈব কার্বন ভালো আছে। এটি ধরে রাখতে প্রতি মৌসুমে কম্পোস্ট বা গোবর সার দিতে থাকুন।"),
    "cec_low": ("The soil holds nutrients poorly (low CEC). Give fertiliser in more small doses and add organic manure.", "मिट्टी पोषक तत्व कम रोक पाती है (कम CEC)। उर्वरक कई छोटी खुराकों में दें और जैविक खाद मिलाएं।", "মাটি পুষ্টি কম ধরে রাখে (কম CEC)। সার কয়েকটি ছোট কিস্তিতে দিন এবং জৈব সার মেশান।"),
    "note_inorganic": ("This plan gives the full chemical dose worked out from your soil test. Compost/FYM along with it keeps the soil alive, so do not skip it.", "इस योजना में मिट्टी जांच के अनुसार पूरी रासायनिक मात्रा दी गई है। साथ में कम्पोस्ट/गोबर की खाद मिट्टी को जीवित रखती है, इसे न छोड़ें।", "এই পরিকল্পনায় মাটি পরীক্ষা অনুযায়ী পুরো রাসায়নিক মাত্রা দেওয়া হয়েছে। সঙ্গে কম্পোস্ট/গোবর সার মাটিকে সজীব রাখে, বাদ দেবেন না।"),
    "note_partial": ("This plan uses 25% less chemical fertiliser because compost/FYM and bio-fertiliser supply part of the need. Do not skip the compost.", "इस योजना में रासायनिक उर्वरक 25% कम है क्योंकि कम्पोस्ट/गोबर की खाद और जैव उर्वरक कुछ जरूरत पूरी करते हैं। कम्पोस्ट न छोड़ें।", "এই পরিকল্পনায় রাসায়নিক সার 25% কম, কারণ কম্পোস্ট/গোবর সার ও জৈব সার কিছু চাহিদা মেটায়। কম্পোস্ট বাদ দেবেন না।"),
    "note_organic": ("Compost, oil-cake, rock phosphate / bone meal and ash supply about {pct_n}% of the nitrogen, {pct_p}% of the phosphorus and {pct_k}% of the potash the crop needs. In the first 1-2 years yield can be a little lower while the soil builds up.", "कम्पोस्ट, खली, रॉक फॉस्फेट / हड्डी का चूरा और राख से फसल की लगभग {pct_n}% नाइट्रोजन, {pct_p}% फॉस्फोरस और {pct_k}% पोटाश की जरूरत पूरी होती है। पहले 1-2 साल उपज थोड़ी कम हो सकती है जब तक मिट्टी बनती है।", "কম্পোস্ট, খোল, রক ফসফেট / হাড়ের গুঁড়ো ও ছাই থেকে ফসলের প্রায় {pct_n}% নাইট্রোজেন, {pct_p}% ফসফরাস ও {pct_k}% পটাশের চাহিদা মেটে। প্রথম 1-2 বছর মাটি তৈরি হওয়া পর্যন্ত ফলন একটু কম হতে পারে।"),
    "org_gap": ("Nitrogen is hard to supply fully from organic sources. Grow dhaincha / sunhemp green manure before the crop and a legume (pulse) in rotation to cover the rest.", "जैविक स्रोतों से नाइट्रोजन पूरी तरह देना कठिन है। बाकी के लिए फसल से पहले ढैंचा / सनई की हरी खाद और फेरबदल में दलहन उगाएं।", "জৈব উৎস থেকে নাইট্রোজেন পুরোপুরি দেওয়া কঠিন। বাকিটার জন্য ফসলের আগে ধৈঞ্চা / শনের সবুজ সার এবং পর্যায়ক্রমে ডাল চাষ করুন।"),
    "note_natural": ("This is a practice-based plan, not calculated from the soil test. Follow your natural-farming trainer's package, keep the soil mulched and add compost.", "यह अभ्यास पर आधारित योजना है, मिट्टी जांच से गणना की हुई नहीं। अपने प्राकृतिक खेती प्रशिक्षक के पैकेज का पालन करें, मिट्टी को मल्च से ढकें और कम्पोस्ट डालें।", "এটি অভ্যাসভিত্তিক পরিকল্পনা, মাটি পরীক্ষা থেকে হিসাব করা নয়। আপনার প্রাকৃতিক চাষের প্রশিক্ষকের প্যাকেজ মেনে চলুন, মাটি মালচ দিয়ে ঢেকে রাখুন ও কম্পোস্ট দিন।"),
    "biofert_legume": ("Treat the seed with Rhizobium and PSB culture (follow the packet) before sowing.", "बुवाई से पहले बीज को राइजोबियम और पीएसबी कल्चर से उपचारित करें (पैकेट के अनुसार)।", "বপনের আগে বীজ রাইজোবিয়াম ও পিএসবি কালচার দিয়ে শোধন করুন (প্যাকেট অনুযায়ী)।"),
    "biofert_other": ("Treat the seed or seedling roots with Azospirillum / Azotobacter and PSB culture (follow the packet).", "बीज या पौध की जड़ों को एजोस्पाइरिलम / एजोटोबैक्टर और पीएसबी कल्चर से उपचारित करें (पैकेट के अनुसार)।", "বীজ বা চারার শিকড় অ্যাজোস্পাইরিলাম / অ্যাজোটোব্যাক্টর ও পিএসবি কালচার দিয়ে শোধন করুন (প্যাকেট অনুযায়ী)।"),
    "mix_cake": ("Mix neem / mustard cake into the soil 10-15 days before sowing or planting so that it can break down.", "नीम / सरसों की खली को बुवाई या रोपाई से 10-15 दिन पहले मिट्टी में मिलाएं ताकि वह सड़ जाए।", "নিম / সরষের খোল বপন বা রোপণের 10-15 দিন আগে মাটিতে মিশিয়ে দিন, যাতে পচে যায়।"),
    "ph_acid": ("Your soil pH ({ph}) is acidic. Apply agricultural lime, {lo}-{hi} kg for your land, in the furrow at sowing. Do not mix lime with urea or DAP in a heap.", "आपकी मिट्टी का pH ({ph}) अम्लीय है। बुवाई के समय कूंड में कृषि चूना डालें, आपकी जमीन के लिए {lo}-{hi} किग्रा। चूने को यूरिया या डीएपी के साथ ढेर में न मिलाएं।", "আপনার মাটির pH ({ph}) অম্লীয়। বপনের সময় নালায় কৃষি চুন দিন, আপনার জমির জন্য {lo}-{hi} কেজি। চুন ইউরিয়া বা ডিএপির সঙ্গে স্তূপ করে মেশাবেন না।"),
    "ph_ok": ("Your soil pH ({ph}) is fine for most crops.", "आपकी मिट्टी का pH ({ph}) ज्यादातर फसलों के लिए ठीक है।", "আপনার মাটির pH ({ph}) বেশিরভাগ ফসলের জন্য ঠিক আছে।"),
    "ph_alk": ("Your soil pH ({ph}) is high (alkaline). Add plenty of compost, avoid wood ash and lime, and ask your KVK about gypsum.", "आपकी मिट्टी का pH ({ph}) ऊंचा (क्षारीय) है। खूब कम्पोस्ट डालें, राख और चूना न डालें, और जिप्सम के बारे में केवीके से पूछें।", "আপনার মাটির pH ({ph}) বেশি (ক্ষারীয়)। প্রচুর কম্পোস্ট দিন, ছাই ও চুন এড়িয়ে চলুন এবং জিপসাম সম্পর্কে কেভিকে-র কাছে জানুন।"),
    "zone_acid": ("Soils in your area are mostly acidic. If soil pH is below 5.5, apply agricultural lime 2-4 quintal per hectare (about 80-160 kg per acre) in the furrow at sowing. Acid soil locks phosphorus, so use rock phosphate or SSP together with compost.", "आपके क्षेत्र की मिट्टी ज्यादातर अम्लीय है। pH 5.5 से कम हो तो बुवाई के समय कूंड में कृषि चूना 2-4 क्विंटल प्रति हेक्टेयर (लगभग 80-160 किग्रा प्रति एकड़) डालें। अम्लीय मिट्टी फॉस्फोरस को बांध लेती है, इसलिए कम्पोस्ट के साथ रॉक फॉस्फेट या एसएसपी का उपयोग करें।", "আপনার এলাকার মাটি বেশিরভাগ অম্লীয়। pH 5.5-এর কম হলে বপনের সময় নালায় কৃষি চুন হেক্টর প্রতি 2-4 কুইন্টাল (একর প্রতি প্রায় 80-160 কেজি) দিন। অম্লীয় মাটি ফসফরাসকে আটকে রাখে, তাই কম্পোস্টের সঙ্গে রক ফসফেট বা এসএসপি ব্যবহার করুন।"),
    "zone_high_rain": ("Very heavy rain washes nutrients away. Give nitrogen and potash in 3 or more small doses, never just before heavy rain, and keep the soil covered with mulch or crop residue.", "बहुत तेज बारिश पोषक तत्व बहा ले जाती है। नाइट्रोजन और पोटाश 3 या अधिक छोटी खुराकों में दें, तेज बारिश से ठीक पहले कभी न दें, और मिट्टी को मल्च या फसल अवशेष से ढककर रखें।", "খুব বেশি বৃষ্টিতে পুষ্টি ধুয়ে যায়। নাইট্রোজেন ও পটাশ 3 বা তার বেশি ছোট কিস্তিতে দিন, প্রবল বৃষ্টির ঠিক আগে কখনও নয়, এবং মাটি মালচ বা ফসলের অবশেষ দিয়ে ঢেকে রাখুন।"),
    "zone_drought": ("Rain is uneven and dry spells are common here. Mulch the soil, add compost to hold water, and give top-dressing only when the soil has moisture.", "यहां बारिश अनियमित है और सूखे के दौर आम हैं। मिट्टी को मल्च से ढकें, पानी रोकने के लिए कम्पोस्ट डालें, और टॉप ड्रेसिंग तभी दें जब मिट्टी में नमी हो।", "এখানে বৃষ্টি অনিয়মিত এবং শুকনো সময় প্রায়ই আসে। মাটি মালচ দিয়ে ঢাকুন, জল ধরে রাখতে কম্পোস্ট দিন এবং মাটিতে আর্দ্রতা থাকলে তবেই উপরি-প্রয়োগ করুন।"),
    "zone_lowoc": ("These soils are low in organic matter and hold little water. Add compost every season and grow a green-manure crop before the main crop.", "इन मिट्टियों में जीवांश कम होता है और पानी कम रुकता है। हर मौसम कम्पोस्ट डालें और मुख्य फसल से पहले हरी खाद की फसल उगाएं।", "এই মাটিতে জৈব পদার্থ কম এবং জল কম ধরে। প্রতি মৌসুমে কম্পোস্ট দিন এবং মূল ফসলের আগে সবুজ সার চাষ করুন।"),
    "zone_saline": ("Salt in the soil and water can harm crops. Make drains to wash the salt out, add plenty of compost, use gypsum if the soil is sodic, and choose salt-tolerant varieties.", "मिट्टी और पानी में नमक फसलों को नुकसान पहुंचा सकता है। नमक बहाने के लिए नालियां बनाएं, खूब कम्पोस्ट डालें, क्षारीय मिट्टी में जिप्सम डालें और नमक सहने वाली किस्में चुनें।", "মাটি ও জলের লবণ ফসলের ক্ষতি করতে পারে। লবণ ধুয়ে ফেলতে নালা কাটুন, প্রচুর কম্পোস্ট দিন, ক্ষারীয় মাটিতে জিপসাম দিন এবং লবণ-সহনশীল জাত বেছে নিন।"),
    "zone_flood": ("Water can stand during the rains. Make drainage channels and use raised beds for vegetables.", "बारिश में पानी जमा हो सकता है। जल निकासी की नालियां बनाएं और सब्जियों के लिए ऊंची क्यारियां बनाएं।", "বর্ষায় জল জমতে পারে। নিকাশি নালা কাটুন এবং সবজির জন্য উঁচু বেড বানান।"),
    "zone_slope": ("On sloping land, make contour bunds or trenches and put fertiliser in the root zone, not on the surface, so that it does not wash away.", "ढलान वाली जमीन पर कंटूर मेड़ या खाई बनाएं और उर्वरक सतह पर नहीं, जड़ों के पास डालें ताकि बह न जाए।", "ঢালু জমিতে কনট্যুর বাঁধ বা নালা কাটুন এবং সার উপরে নয়, শিকড়ের কাছে দিন যাতে ধুয়ে না যায়।"),
    "zone_boron": ("Boron shortage is common in these soils (hollow stems, poor fruit set). For vegetables and mustard, apply borax about 4 kg per acre or spray 0.2% borax at flowering.", "इन मिट्टियों में बोरॉन की कमी आम है (खोखला तना, कम फल लगना)। सब्जियों और सरसों में बोरेक्स लगभग 4 किग्रा प्रति एकड़ डालें या फूल आने पर 0.2% बोरेक्स का छिड़काव करें।", "এই মাটিতে বোরনের অভাব সাধারণ (ফাঁপা কাণ্ড, কম ফল ধরা)। সবজি ও সরষেতে একর প্রতি প্রায় 4 কেজি বোরাক্স দিন বা ফুল আসার সময় 0.2% বোরাক্স স্প্রে করুন।"),
    "zone_intensive": ("Intensive cropping here can use up sulphur and zinc. Once every 2-3 years apply zinc sulphate (about 10 kg per acre) and a sulphur source such as gypsum or SSP.", "यहां सघन खेती से सल्फर और जिंक कम हो सकते हैं। 2-3 साल में एक बार जिंक सल्फेट (लगभग 10 किग्रा प्रति एकड़) और जिप्सम या एसएसपी जैसा सल्फर स्रोत डालें।", "এখানে ঘন চাষে সালফার ও জিঙ্ক কমে যেতে পারে। 2-3 বছরে একবার জিঙ্ক সালফেট (একর প্রতি প্রায় 10 কেজি) এবং জিপসাম বা এসএসপি-র মতো সালফার উৎস দিন।"),
    "rainfed": ("Rain-fed field: put fertiliser in moist soil at sowing, and top-dress only when the soil is moist.", "वर्षा आधारित खेत: बुवाई के समय नम मिट्टी में उर्वरक डालें और टॉप ड्रेसिंग तभी करें जब मिट्टी नम हो।", "বৃষ্টিনির্ভর জমি: বপনের সময় ভেজা মাটিতে সার দিন এবং মাটি ভেজা থাকলে তবেই উপরি-প্রয়োগ করুন।"),
    "irrigated": ("Irrigated field: give a light irrigation after each top-dressing so that the fertiliser reaches the roots.", "सिंचित खेत: हर टॉप ड्रेसिंग के बाद हल्की सिंचाई करें ताकि उर्वरक जड़ों तक पहुंचे।", "সেচযুক্ত জমি: প্রতিটি উপরি-প্রয়োগের পরে হালকা সেচ দিন যাতে সার শিকড়ে পৌঁছায়।"),
    "basal": ("Mix compost/FYM, DAP and MOP into the soil at the last ploughing or at sowing/planting.", "कम्पोस्ट/गोबर की खाद, डीएपी और एमओपी को आखिरी जुताई या बुवाई/रोपाई के समय मिट्टी में अच्छी तरह मिलाएं।", "কম্পোস্ট/গোবর সার, ডিএপি ও এমওপি শেষ চাষের সময় বা বপন/রোপণের সময় মাটিতে ভালো করে মিশিয়ে দিন।"),
    "basal_org": ("Mix compost/FYM and the other basal inputs into the soil at the last ploughing or at sowing/planting.", "कम्पोस्ट/गोबर की खाद और बाकी आधार सामग्री को आखिरी जुताई या बुवाई/रोपाई के समय मिट्टी में मिलाएं।", "কম্পোস্ট/গোবর সার ও অন্যান্য গোড়ার সামগ্রী শেষ চাষের সময় বা বপন/রোপণের সময় মাটিতে মিশিয়ে দিন।"),
    "urea_tip": ("Apply urea only when the soil has moisture, and not just before heavy rain.", "यूरिया तभी डालें जब मिट्टी में नमी हो, और तेज बारिश से ठीक पहले न डालें।", "মাটিতে আর্দ্রতা থাকলে তবেই ইউরিয়া দিন, প্রবল বৃষ্টির ঠিক আগে দেবেন না।"),
    "n_low_split": ("Nitrogen is low, so do not skip the urea top-dressing doses given in the schedule.", "नाइट्रोजन कम है, इसलिए तालिका में दी गई यूरिया टॉप ड्रेसिंग न छोड़ें।", "নাইট্রোজেন কম, তাই তালিকায় দেওয়া ইউরিয়া উপরি-প্রয়োগ বাদ দেবেন না।"),
    "spray_tip": ("Spray in the early morning or evening, not in hot sun or just before rain. Use a clean sprayer, and try a new product on a few plants first. Do not mix different products unless the label says it is safe.", "छिड़काव सुबह जल्दी या शाम को करें, तेज धूप में या बारिश से ठीक पहले नहीं। साफ स्प्रेयर इस्तेमाल करें और नया उत्पाद पहले कुछ पौधों पर आजमाएं। अलग-अलग उत्पाद तभी मिलाएं जब लेबल पर सुरक्षित लिखा हो।", "স্প্রে ভোরে বা সন্ধ্যায় করুন, কড়া রোদে বা বৃষ্টির ঠিক আগে নয়। পরিষ্কার স্প্রেয়ার ব্যবহার করুন এবং নতুন সামগ্রী আগে কয়েকটি গাছে পরীক্ষা করুন। লেবেলে নিরাপদ লেখা না থাকলে আলাদা সামগ্রী মিশাবেন না।"),
    # weather
    "wx_heavy": ("Heavy rain is expected ({mm} mm in 3 days). Do not apply urea or spray now; wait until the rain stops.", "तेज बारिश की संभावना है (3 दिन में {mm} मिमी)। अभी यूरिया या छिड़काव न करें; बारिश रुकने का इंतजार करें।", "প্রবল বৃষ্টির সম্ভাবনা (3 দিনে {mm} মিমি)। এখন ইউরিয়া বা স্প্রে করবেন না; বৃষ্টি থামা পর্যন্ত অপেক্ষা করুন।"),
    "wx_good": ("Some rain is expected ({mm} mm in 3 days). A good time for top-dressing if it is due.", "कुछ बारिश की संभावना है (3 दिन में {mm} मिमी)। अगर टॉप ड्रेसिंग का समय है तो यह अच्छा मौका है।", "কিছু বৃষ্টির সম্ভাবনা (3 দিনে {mm} মিমি)। উপরি-প্রয়োগের সময় হলে এটি ভালো সুযোগ।"),
    "wx_dry": ("It has been dry. Irrigate before top-dressing; in rain-fed fields wait for rain.", "मौसम सूखा रहा है। टॉप ड्रेसिंग से पहले सिंचाई करें; वर्षा आधारित खेत में बारिश का इंतजार करें।", "আবহাওয়া শুকনো। উপরি-প্রয়োগের আগে সেচ দিন; বৃষ্টিনির্ভর জমিতে বৃষ্টির অপেক্ষা করুন।"),
    "wx_hot": ("Very hot days ahead (up to {t} degrees C). Spray only very early in the morning or in the evening.", "आगे बहुत गर्म दिन हैं ({t} डिग्री सेल्सियस तक)। छिड़काव सिर्फ बहुत सुबह या शाम को करें।", "সামনে খুব গরম দিন ({t} ডিগ্রি সেলসিয়াস পর্যন্ত)। স্প্রে শুধু খুব ভোরে বা সন্ধ্যায় করুন।"),
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
            out.append(ADVICE[lang]["adj_" + kw["rating"]].format(nutrient=NUTRIENT_NAME[lang][kw["nutrient"]]))
        else:
            out.append(ADVICE[lang][key].format(**kw))
    return out
