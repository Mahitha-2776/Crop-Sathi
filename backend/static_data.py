VALID_SOIL_TYPES = {
    "alluvial", "black", "red", "laterite", "desert", "mountain",
    "loamy", "sandy", "clay"
}

SOIL_RECOMMENDATIONS = {
    "alluvial": "Rich in potash, but often deficient in phosphorus. Consider NPK fertilizers with a focus on P.",
    "black": "High in clay, good water retention. Ensure good drainage. Generally rich in nutrients.",
    "red": "Deficient in nitrogen, phosphorus, and humus. Requires balanced fertilization and organic matter.",
    "laterite": "Low in nitrogen, potash, and organic matter. Acidic in nature; liming may be necessary.",
    "desert": "Sandy and low in organic matter. Requires frequent irrigation and addition of organic manure.",
    "mountain": "Variable, often acidic and low in phosphorus. Soil testing is highly recommended.",
    "loamy": "Ideal for most crops. Well-balanced. Maintain health with crop rotation and organic inputs.",
    "sandy": "Poor water retention and low in nutrients. Requires frequent, smaller applications of fertilizer and water.",
    "clay": "High nutrient content but poor drainage. Improve structure with organic matter like compost.",
    "default": "General soil. A balanced NPK fertilizer is a good starting point. Consider getting a soil test for specific recommendations."
}

CROP_DATA = {
    "rice": {"stages": ["nursery", "transplanting", "vegetative", "flowering", "harvesting"], "water_requirement_mm": 1200},
    "wheat": {"stages": ["sowing", "germination", "tillering", "heading", "ripening"], "water_requirement_mm": 500},
    "maize": {"stages": ["planting", "vegetative", "tasseling", "silking", "maturity"], "water_requirement_mm": 600},
    "cotton": {"stages": ["sowing", "seedling", "squaring", "flowering", "boll-formation"], "water_requirement_mm": 800},
    "sugarcane": {"stages": ["planting", "germination", "tillering", "grand-growth", "maturity"], "water_requirement_mm": 2000},
    "soybean": {"stages": ["planting", "vegetative", "flowering", "pod-development", "maturity"], "water_requirement_mm": 550},
    "tomato": {"stages": ["nursery", "transplanting", "vegetative", "flowering", "fruiting"], "water_requirement_mm": 700},
    "potato": {"stages": ["planting", "sprouting", "vegetative", "tuber-initiation", "tuber-bulking"], "water_requirement_mm": 600},
    "chickpea": {"stages": ["sowing", "vegetative", "flowering", "pod-formation", "maturity"], "water_requirement_mm": 400},
    "mustard": {"stages": ["sowing", "vegetative", "flowering", "pod-formation", "ripening"], "water_requirement_mm": 350},
    "mango": {"stages": ["planting", "vegetative", "flowering", "fruit-set", "harvesting"], "water_requirement_mm": 1000},
    "banana": {"stages": ["planting", "vegetative", "shooting", "bunch-development", "harvesting"], "water_requirement_mm": 1500},
    "onion": {"stages": ["nursery", "transplanting", "vegetative", "bulb-development", "harvesting"], "water_requirement_mm": 450},
    "brinjal": {"stages": ["nursery", "transplanting", "vegetative", "flowering", "fruiting"], "water_requirement_mm": 650},
}

PEST_DATABASE = {
    "rice": {
        "vegetative": [{"pest": "Stem Borer", "risk": "High"}, {"pest": "Leaf Folder", "risk": "Medium"}],
        "flowering": [{"pest": "Brown Plant Hopper", "risk": "High"}, {"pest": "Gall Midge", "risk": "Low"}, {"pest": "Blast Fungus", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "wheat": {
        "tillering": [{"pest": "Aphid", "risk": "High"}, {"pest": "Termites", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "cotton": {
        "squaring": [{"pest": "Bollworm", "risk": "High"}, {"pest": "Jassids", "risk": "Medium"}, {"pest": "Whitefly", "risk": "Medium"}],
        "boll-formation": [{"pest": "Whitefly", "risk": "High"}, {"pest": "Pink Bollworm", "risk": "High"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "sugarcane": {
        "tillering": [{"pest": "Early Shoot Borer", "risk": "High"}, {"pest": "Termites", "risk": "Medium"}],
        "grand-growth": [{"pest": "Top Borer", "risk": "High"}, {"pest": "Whitefly", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "soybean": {
        "vegetative": [{"pest": "Girdle Beetle", "risk": "Medium"}, {"pest": "Aphid", "risk": "Low"}],
        "pod-development": [{"pest": "Pod Borer", "risk": "High"}, {"pest": "Whitefly", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "tomato": {
        "vegetative": [{"pest": "Early Blight", "risk": "Medium"}],
        "fruiting": [{"pest": "Fruit Borer", "risk": "High"}, {"pest": "Whitefly", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "potato": {
        "vegetative": [{"pest": "Late Blight", "risk": "High"}],
        "tuber-bulking": [{"pest": "Potato Tuber Moth", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "chickpea": {
        "pod-formation": [{"pest": "Pod Borer", "risk": "High"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "mustard": {
        "flowering": [{"pest": "Aphid", "risk": "High"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "mango": {
        "flowering": [{"pest": "Mango Hopper", "risk": "High"}, {"pest": "Powdery Mildew", "risk": "Medium"}],
        "fruit-set": [{"pest": "Fruit Fly", "risk": "High"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "banana": {
        "vegetative": [{"pest": "Rhizome Weevil", "risk": "Medium"}],
        "bunch-development": [{"pest": "Sigatoka Leaf Spot", "risk": "High"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "onion": {
        "vegetative": [{"pest": "Thrips", "risk": "High"}],
        "bulb-development": [{"pest": "Purple Blotch", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "brinjal": {
        "fruiting": [{"pest": "Shoot and Fruit Borer", "risk": "High"}, {"pest": "Whitefly", "risk": "Medium"}],
        "default": [{"pest": "General Pests", "risk": "Low"}]
    },
    "default": [{"pest": "General Pests", "risk": "Low"}]
}

PESTICIDE_RECOMMENDATIONS = {
    "Stem Borer": "Use Cartap Hydrochloride.",
    "Brown Plant Hopper": "Use Pymetrozine.",
    "Leaf Folder": "Use Chlorantraniliprole.",
    "Gall Midge": "Use Fipronil.",
    "Blast Fungus": "Use Tricyclazole.",
    "Termites": "Use Chlorpyrifos.",
    "Jassids": "Use Acetamiprid.",
    "Pink Bollworm": "Use pheromone traps and specific insecticides like Thiodicarb.",
    "Aphid": "Use Imidacloprid.",
    "Bollworm": "Use Emamectin Benzoate.",
    "Whitefly": "Use Diafenthiuron.",
    "Early Shoot Borer": "Use Chlorantraniliprole.",
    "Top Borer": "Use Fipronil granules.",
    "Girdle Beetle": "Use Thiamethoxam.",
    "Pod Borer": "Use Indoxacarb.",
    "Fruit Borer": "Use Chlorantraniliprole or Flubendiamide.",
    "Early Blight": "Use Mancozeb or Chlorothalonil fungicide.",
    "Late Blight": "Use Mancozeb or Metalaxyl fungicide.",
    "Potato Tuber Moth": "Use pheromone traps and cover tubers well with soil.",
    "Mango Hopper": "Use Imidacloprid or Thiamethoxam.",
    "Powdery Mildew": "Use wettable sulfur or Hexaconazole.",
    "Fruit Fly": "Use pheromone traps and bait sprays.",
    "Rhizome Weevil": "Apply Carbofuran granules at planting.",
    "Sigatoka Leaf Spot": "Use Propiconazole or Mancozeb.",
    "Thrips": "Use Fipronil or Spinosad.",
    "Purple Blotch": "Use Mancozeb or Chlorothalonil.",
    "Shoot and Fruit Borer": "Use Emamectin Benzoate. Remove and destroy affected parts.",
    "Default": "Follow local agricultural guidelines for pesticides."
}

GOVT_SCHEMES = {
    "default": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Soil Health Card", "description": "Provides soil nutrient status and recommendations.", "link": "#"},
    ],
    "rice": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "National Food Security Mission (NFSM)", "description": "Promotes rice production with subsidies on seeds and machinery.", "link": "#"},
    ],
    "cotton": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Cotton Development Programme", "description": "Focuses on improving yield and quality.", "link": "#"},
    ],
    "sugarcane": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Fair and Remunerative Price (FRP)", "description": "Ensures a guaranteed price for sugarcane farmers.", "link": "#"},
    ],
    "soybean": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "National Mission on Oilseeds", "description": "Promotes soybean cultivation and provides support.", "link": "#"},
    ],
    "chickpea": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "National Food Security Mission (NFSM) - Pulses", "description": "Promotes production of pulses through various interventions.", "link": "#"},
    ],
    "mustard": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "National Mission on Oilseeds", "description": "Promotes mustard cultivation and provides support.", "link": "#"},
    ],
    "mango": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Mission for Integrated Development of Horticulture (MIDH)", "description": "Promotes holistic growth of the horticulture sector.", "link": "#"},
    ],
    "banana": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Mission for Integrated Development of Horticulture (MIDH)", "description": "Promotes holistic growth of the horticulture sector.", "link": "#"},
    ],
    "onion": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Mission for Integrated Development of Horticulture (MIDH)", "description": "Promotes holistic growth of the horticulture sector.", "link": "#"},
    ],
    "brinjal": [
        {"name": "PM-KISAN", "description": "Direct income support of ₹6,000/year.", "link": "#"},
        {"name": "Mission for Integrated Development of Horticulture (MIDH)", "description": "Promotes holistic growth of the horticulture sector.", "link": "#"},
    ]
}

MESSAGE_TEMPLATES = {
    "English": {
        "greeting": "Hello {name}, here is your advisory for {crop}:",
        "weather": "Weather: {description}, Temp: {temp}°C.",
        "pest_risk": "Highest Pest Risk: {pest}.",
        "recommendation": "Recommendation: {recommendation}",
        "crop_health_healthy": "Satellite Health: Your crop appears to be growing well (NDVI: {ndvi:.2f}).",
        "crop_health_moderate": "Satellite Health: Crop shows moderate density (NDVI: {ndvi:.2f}). Monitor for uneven growth.",
        "crop_health_stressed": "Satellite Health: Crop may be stressed (NDVI: {ndvi:.2f}). Field inspection is recommended.",
        "precaution_rain": "Heavy rain expected. Ensure proper drainage to prevent waterlogging.",
        "precaution_default": "Monitor crop health daily for any signs of stress or pests.",
        "daily_advice": "Current weather is {description} with a temperature of {temp}°C and humidity of {humidity}%. {precaution_text}",
        "water_availability_good": "Good",
        "water_availability_moderate": "Moderate",
        "water_requirement": "{value} mm/season",
        "water_recommendation": "Ensure regular irrigation as per the crop stage. {detail}",
        "water_detail_rain": "Less frequent irrigation may be needed due to recent/expected rain.",
        "water_detail_no_rain": "Monitor soil moisture closely.",
        "schemes_loading": "Loading schemes...",
        "forecast_loading": "Weather forecast will appear here...",
        "forecast_unavailable": "Forecast not available.",
        "water_info_unavailable": "Water information not available.",
        "market_data_unavailable": "Could not load market data.",
        "password_reset": "Your Crop Sathi password reset link is: {reset_url}",
        "no_pest_risk": "Highest Pest Risk: None.",
        "weather_unavailable": "Weather data unavailable."
    },
    "Hindi": {
        "greeting": "नमस्ते {name}, {crop} के लिए आपकी सलाह यहाँ दी गई है:",
        "weather": "मौसम: {description}, तापमान: {temp}°C.",
        "pest_risk": "सबसे बड़ा कीट जोखिम: {pest}.",
        "recommendation": "सिफारिश: {recommendation}",
        "crop_health_healthy": "सैटेलाइट स्वास्थ्य: आपकी फसल अच्छी तरह से बढ़ रही है (NDVI: {ndvi:.2f})।",
        "crop_health_moderate": "सैटेलाइट स्वास्थ्य: फसल मध्यम घनत्व दिखाती है (NDVI: {ndvi:.2f})। असमान वृद्धि के लिए निगरानी करें।",
        "crop_health_stressed": "सैटेलाइट स्वास्थ्य: फसल तनाव में हो सकती है (NDVI: {ndvi:.2f})। खेत का निरीक्षण करने की सलाह दी जाती है।",
        "precaution_rain": "भारी बारिश की उम्मीद है। जलभराव को रोकने के लिए उचित जल निकासी सुनिश्चित करें।",
        "precaution_default": "किसी भी तनाव या कीटों के संकेतों के लिए प्रतिदिन फसल के स्वास्थ्य की निगरानी करें।",
        "daily_advice": "वर्तमान मौसम {description} है, तापमान {temp}°C और आर्द्रता {humidity}% है। {precaution_text}",
        "water_availability_good": "अच्छा",
        "water_availability_moderate": "मध्यम",
        "water_requirement": "{value} मिमी/मौसम",
        "water_recommendation": "फसल की अवस्था के अनुसार नियमित सिंचाई सुनिश्चित करें। {detail}",
        "water_detail_rain": "हाल की/अपेक्षित बारिश के कारण कम सिंचाई की आवश्यकता हो सकती है।",
        "water_detail_no_rain": "मिट्टी की नमी पर कड़ी नजर रखें।",
        "schemes_loading": "योजनाएं लोड हो रही हैं...",
        "forecast_loading": "मौसम का पूर्वानुमान यहां दिखाई देगा...",
        "forecast_unavailable": "पूर्वानुमान उपलब्ध नहीं है।",
        "water_info_unavailable": "पानी की जानकारी उपलब्ध नहीं है।",
        "market_data_unavailable": "बाजार डेटा लोड नहीं हो सका।",
        "password_reset": "आपका क्रॉप साथी पासवर्ड रीसेट लिंक है: {reset_url}",
        "no_pest_risk": "सबसे बड़ा कीट जोखिम: कोई नहीं।",
        "weather_unavailable": "मौसम की जानकारी उपलब्ध नहीं है।"
    },
    "Telugu": {
        "greeting": "నమస్కారం {name}, {crop} కోసం మీ సలహా ఇక్కడ ఉంది:",
        "weather": "వాతావరణం: {description}, ఉష్ణోగ్రత: {temp}°C.",
        "pest_risk": "అత్యధిక పెస్ట్ ప్రమాదం: {pest}.",
        "recommendation": "సిఫార్సు: {recommendation}",
        "crop_health_healthy": "శాటిలైట్ ఆరోగ్యం: మీ పంట బాగా పెరుగుతున్నట్లు కనిపిస్తోంది (NDVI: {ndvi:.2f}).",
        "crop_health_moderate": "శాటిలైట్ ఆరోగ్యం: పంట మధ్యస్థ సాంద్రతను చూపుతుంది (NDVI: {ndvi:.2f}). అసమాన పెరుగుదల కోసం పర్యవేక్షించండి.",
        "crop_health_stressed": "శాటిలైట్ ఆరోగ్యం: పంట ఒత్తిడికి గురై ఉండవచ్చు (NDVI: {ndvi:.2f}). క్షేత్రస్థాయి తనిఖీ మంచిది.",
        "precaution_rain": "భారీ వర్షం కురిసే అవకాశం ఉంది. నీరు నిలిచిపోకుండా సరైన డ్రైనేజీ ఉండేలా చూసుకోండి.",
        "precaution_default": "ఒత్తిడి లేదా తెగుళ్ల సంకేతాల కోసం ప్రతిరోజూ పంట ఆరోగ్యాన్ని పర్యవేక్షించండి.",
        "daily_advice": "ప్రస్తుత వాతావరణం {description}, ఉష్ణోగ్రత {temp}°C మరియు తేమ {humidity}%. {precaution_text}",
        "water_availability_good": "మంచిది",
        "water_availability_moderate": "మధ్యస్థం",
        "water_requirement": "{value} మిమీ/సీజన్",
        "water_recommendation": "పంట దశకు అనుగుణంగా క్రమం తప్పకుండా నీటిపారుదల ఉండేలా చూసుకోండి. {detail}",
        "water_detail_rain": "ఇటీవలి/ఆశించిన వర్షం కారణంగా తక్కువ తరచుగా నీటిపారుదల అవసరం కావచ్చు.",
        "water_detail_no_rain": "నేల తేమను నిశితంగా గమనించండి.",
        "schemes_loading": "పథకాలు లోడ్ అవుతున్నాయి...",
        "forecast_loading": "వాతావరణ సూచన ఇక్కడ కనిపిస్తుంది...",
        "forecast_unavailable": "సూచన అందుబాటులో లేదు.",
        "water_info_unavailable": "నీటి సమాచారం అందుబాటులో లేదు.",
        "market_data_unavailable": "మార్కెట్ డేటా లోడ్ చేయడం సాధ్యం కాలేదు.",
        "password_reset": "మీ క్రాప్ సాతీ పాస్‌వర్డ్ రీసెట్ లింక్: {reset_url}",
        "no_pest_risk": "అత్యధిక పెస్ట్ ప్రమాదం: ఏదీ లేదు.",
        "weather_unavailable": "వాతావరణ సమాచారం అందుబాటులో లేదు."
    }
}

MARKET_PRICES = {
    "rice": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 1980}, {"date": "2024-09-16", "price": 1995},
            {"date": "2024-09-17", "price": 2010}, {"date": "2024-09-18", "price": 2005},
            {"date": "2024-09-19", "price": 2025}, {"date": "2024-09-20", "price": 2030},
            {"date": "2024-09-21", "price": 2050},
        ]
    },
    "wheat": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 2100}, {"date": "2024-09-16", "price": 2115},
            {"date": "2024-09-17", "price": 2110}, {"date": "2024-09-18", "price": 2125},
            {"date": "2024-09-19", "price": 2135}, {"date": "2024-09-20", "price": 2130},
            {"date": "2024-09-21", "price": 2145},
        ]
    },
    "cotton": {
        "unit": "₹/candy",
        "history": [
            {"date": "2024-09-15", "price": 56500}, {"date": "2024-09-16", "price": 56800},
            {"date": "2024-09-17", "price": 57100}, {"date": "2024-09-18", "price": 57000},
            {"date": "2024-09-19", "price": 57250}, {"date": "2024-09-20", "price": 57300},
            {"date": "2024-09-21", "price": 57500},
        ]
    },
    "sugarcane": {
        "unit": "₹/tonne",
        "history": [
            {"date": "2024-09-15", "price": 3400}, {"date": "2024-09-16", "price": 3410},
            {"date": "2024-09-17", "price": 3405}, {"date": "2024-09-18", "price": 3420},
            {"date": "2024-09-19", "price": 3425}, {"date": "2024-09-20", "price": 3430},
            {"date": "2024-09-21", "price": 3450},
        ]
    },
    "soybean": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 4300}, {"date": "2024-09-16", "price": 4320},
            {"date": "2024-09-17", "price": 4310}, {"date": "2024-09-18", "price": 4350},
            {"date": "2024-09-19", "price": 4375}, {"date": "2024-09-20", "price": 4380},
            {"date": "2024-09-21", "price": 4400},
        ]
    },
    "tomato": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 2200}, {"date": "2024-09-16", "price": 2250},
            {"date": "2024-09-17", "price": 2180}, {"date": "2024-09-18", "price": 2230},
            {"date": "2024-09-19", "price": 2300}, {"date": "2024-09-20", "price": 2320},
            {"date": "2024-09-21", "price": 2350},
        ]
    },
    "potato": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 1800}, {"date": "2024-09-16", "price": 1810},
            {"date": "2024-09-17", "price": 1805}, {"date": "2024-09-18", "price": 1825},
            {"date": "2024-09-19", "price": 1850}, {"date": "2024-09-20", "price": 1840},
            {"date": "2024-09-21", "price": 1860},
        ]
    },
    "chickpea": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 5100}, {"date": "2024-09-16", "price": 5150},
            {"date": "2024-09-17", "price": 5125}, {"date": "2024-09-18", "price": 5180},
            {"date": "2024-09-19", "price": 5200}, {"date": "2024-09-20", "price": 5210},
            {"date": "2024-09-21", "price": 5250},
        ]
    },
    "mustard": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 5500}, {"date": "2024-09-16", "price": 5520},
            {"date": "2024-09-17", "price": 5510}, {"date": "2024-09-18", "price": 5540},
            {"date": "2024-09-19", "price": 5580}, {"date": "2024-09-20", "price": 5600},
            {"date": "2024-09-21", "price": 5620},
        ]
    },
    "mango": {
        "unit": "₹/tonne",
        "history": [
            {"date": "2024-09-15", "price": 45000}, {"date": "2024-09-16", "price": 45500},
            {"date": "2024-09-17", "price": 46000}, {"date": "2024-09-18", "price": 45800},
            {"date": "2024-09-19", "price": 46200}, {"date": "2024-09-20", "price": 46500},
            {"date": "2024-09-21", "price": 47000},
        ]
    },
    "banana": {
        "unit": "₹/dozen",
        "history": [
            {"date": "2024-09-15", "price": 40}, {"date": "2024-09-16", "price": 42},
            {"date": "2024-09-17", "price": 41}, {"date": "2024-09-18", "price": 43},
            {"date": "2024-09-19", "price": 45}, {"date": "2024-09-20", "price": 44},
            {"date": "2024-09-21", "price": 46},
        ]
    },
    "onion": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 2500}, {"date": "2024-09-16", "price": 2550},
            {"date": "2024-09-17", "price": 2480}, {"date": "2024-09-18", "price": 2520},
            {"date": "2024-09-19", "price": 2600}, {"date": "2024-09-20", "price": 2610},
            {"date": "2024-09-21", "price": 2650},
        ]
    },
    "brinjal": {
        "unit": "₹/quintal",
        "history": [
            {"date": "2024-09-15", "price": 2000}, {"date": "2024-09-16", "price": 2050},
            {"date": "2024-09-17", "price": 2020}, {"date": "2024-09-18", "price": 2080},
            {"date": "2024-09-19", "price": 2100}, {"date": "2024-09-20", "price": 2120},
            {"date": "2024-09-21", "price": 2150},
        ]
    },
}
