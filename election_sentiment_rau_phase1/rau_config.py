# Rau Assembly Constituency Phase-1 configuration.
# You can freely edit this file as your political/local knowledge improves.

CONSTITUENCY = {
    "state": "Madhya Pradesh",
    "constituency_no": 210,
    "constituency": "Rau",
    "district": "Indore",
    "region": "Malwa / Indore"
}

# These terms are used to attribute content to Rau.
RAU_LOCATION_TERMS = [
    "Rau", "Rau Indore", "Rau assembly", "Rau Vidhan Sabha",
    "Rau constituency", "राऊ", "राऊ विधानसभा", "राऊ इंदौर",
    "राऊ सीट", "राऊ क्षेत्र",
    "Ralamandal", "Ralamandal Indore", "रालामंडल",
    "Piplya Patwari", "पिपल्या पटवारी",
    "Palda", "पालदा",
    "Bicholi Hapsi", "बिचौली हप्सी",
    "Rangwasa", "रंगवासा",
    "Tejaji Nagar", "तेजाजी नगर",
    "Dev Guradia", "Devguradia", "देवगुराड़िया",
    "Mhow Naka", "Rajendra Nagar Indore"
]

PARTIES = {
    "BJP": ["BJP", "Bharatiya Janata Party", "भाजपा", "भारतीय जनता पार्टी"],
    "Congress": ["Congress", "INC", "कांग्रेस", "Indian National Congress"]
}

CANDIDATES_LEADERS = {
    "Madhu Verma": ["Madhu Verma", "मधु वर्मा", "Mahadev Verma"],
    "Jitu Patwari": ["Jitu Patwari", "Jeetu Patwari", "जीतू पटवारी", "जितू पटवारी"],
    "Mohan Yadav": ["Mohan Yadav", "मोहन यादव"],
    "Kamal Nath": ["Kamal Nath", "कमलनाथ"],
    "Shivraj Singh Chouhan": ["Shivraj Singh Chouhan", "Shivraj", "शिवराज सिंह चौहान", "शिवराज"],
    "Jyotiraditya Scindia": ["Jyotiraditya Scindia", "Scindia", "ज्योतिरादित्य सिंधिया", "सिंधिया"]
}

ISSUES = {
    "Water": ["water", "paani", "पानी", "जल", "drinking water"],
    "Roads": ["road", "roads", "sadak", "सड़क", "गड्ढा"],
    "Employment": ["employment", "unemployment", "job", "jobs", "बेरोजगारी", "रोजगार"],
    "Electricity": ["electricity", "bijli", "बिजली"],
    "Women welfare": ["ladli behna", "लाड़ली बहना", "mahila", "महिला"],
    "Farmer": ["farmer", "kisan", "किसान", "mandi", "मंडी"],
    "Corruption": ["corruption", "भ्रष्टाचार", "ghotala", "घोटाला"],
    "Voter list": ["voter list", "Form 7", "फॉर्म 7", "मतदाता", "नाम कटे", "SIR"],
    "Law and order": ["crime", "अपराध", "मारपीट", "clash", "police", "थाना"],
    "Development": ["development", "vikas", "विकास", "infrastructure"]
}

# Manual seed channels. These names are searched by YouTube API and resolved into channel IDs.
# Add local vloggers/influencers here as you discover them.
MANUAL_YOUTUBE_CHANNELS = [
    "News18 MP Chhattisgarh",
    "TV9 Madhya Pradesh Chhattisgarh",
    "Zee Madhya Pradesh Chhattisgarh",
    "ETV Bharat Madhya Pradesh",
    "MP News TV",
    "IBC24",
    "4PM MP",
    "Jansansar News Indore",
    "Indore News",
    "Dainik Bhaskar Indore",
    "Patrika Indore",
    "Rau Indore News",
    "Jansampark MP"
]

# Automatic discovery searches for videos/channels.
RAU_YOUTUBE_SEARCH_QUERIES = [
    "Rau Vidhan Sabha",
    "Rau Indore politics",
    "Rau assembly election",
    "Rau Madhu Verma",
    "Rau Jitu Patwari",
    "राऊ विधानसभा",
    "राऊ इंदौर राजनीति",
    "राऊ मधु वर्मा",
    "राऊ जीतू पटवारी",
    "राऊ विधानसभा फॉर्म 7",
    "राऊ विधानसभा पानी",
    "Rau voter list",
    "Rau water issue"
]

NEWS_QUERIES = [
    "Rau Indore politics",
    "Rau assembly constituency",
    "Rau Vidhan Sabha",
    "Rau Madhu Verma",
    "Rau Jitu Patwari",
    "Rau voter list",
    "Rau Form 7",
    "Rau water issue",
    "Rau Indore development",
    "Rau Indore crime",
    "Bicholi Hapsi politics",
    "Palda Indore politics",
    "Ralamandal Indore politics",
    "Devguradia Indore issue"
]

TREND_GROUPS = [
    ["Rau Indore", "Rau Vidhan Sabha", "Madhu Verma", "Jitu Patwari", "Rau election"],
    ["राऊ इंदौर", "राऊ विधानसभा", "मधु वर्मा", "जीतू पटवारी", "राऊ चुनाव"],
    ["Rau water", "Rau voter list", "Rau development", "Rau road", "Rau electricity"]
]
