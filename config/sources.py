"""
VERIFIED WORKING Kerala Agriculture Sources - 2025 Updated
Focus: Agriculture practices, crops, weather for Kerala ONLY
All sources tested and verified to provide useful content
"""

ALL_SOURCES = {
    # VERIFIED GOVERNMENT SOURCES - WORKING
    
    
    "fib_kerala_working": {
        "name": "Farm Information Bureau Kerala - Kerala Karshakan",
        "base_url": "https://fibkerala.gov.in/",
        "news_urls": [
            "https://fibkerala.gov.in/node/33"  # Kerala Karshakan e-journal - VERIFIED WORKING
        ],
        "selectors": {
            "title": "h1, h2, .field-name-title, .title",
            "content": ".field-name-body, .node-content, .content, p",
            "date": ".submitted, .post-date, .date"
        },
        "category": "government",
        "language": "mixed",
        "scrape_method": "requests_bs4"
    },
    
    "kau_comprehensive": {
        "name": "Kerala Agricultural University - Complete Portal",
        "base_url": "https://kau.in/",
        "news_urls": [
            "https://kau.in/news",
            "https://kau.in/farm-advisory-service-team-through-karshaka-santhwanam",
            "https://kau.in/aas-bulletin"  # Agromet Advisory Bulletin
        ],
        "selectors": {
            "title": "h1, h2, .title, .post-title, .news-title",
            "content": ".content, .post-content, .article-body, .news-content, p",
            "date": ".date, .post-date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "celkau_agri_portal": {
        "name": "KAU Agri-Infotech Portal",
        "base_url": "https://www.celkau.in/",
        "news_urls": [
            "https://www.celkau.in/",
            "https://www.celkau.in/agrimeteorology.aspx"
        ],
        "selectors": {
            "title": "h1, h2, .title, .course-title",
            "content": ".content, .course-content, .main-content, p, table",
            "date": ".date, .course-date"
        },
        "category": "government_tech",
        "language": "mixed",
        "scrape_method": "requests_bs4"
    },
    
    "aims_kerala": {
        "name": "Agriculture Information Management System Kerala",
        "base_url": "https://aims.kerala.gov.in/",
        "news_urls": [
            "https://aims.kerala.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, .title, .service-title",
            "content": ".content, .service-content, .main-content, p",
            "date": ".date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "kathir_kerala": {
        "name": "KATHIR - Kerala Agriculture Technology Hub",
        "base_url": "https://kathir.kerala.gov.in/",
        "news_urls": [
            "https://kathir.kerala.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, .title, .tech-title",
            "content": ".content, .tech-content, .main-content, p",
            "date": ".date"
        },
        "category": "government_tech",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "cpss_kerala": {
        "name": "Crop Pest Surveillance System Kerala",
        "base_url": "https://www.cpsskerala.in/",
        "news_urls": [
            "https://www.cpsskerala.in/"
        ],
        "selectors": {
            "title": "h1, h2, .title, .advisory-title",
            "content": ".content, .advisory-content, .main-content, p",
            "date": ".date"
        },
        "category": "pest_management",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # WORKING MALAYALAM NEWS SOURCES
    "mathrubhumi_agriculture": {
        "name": "Mathrubhumi Agriculture News",
        "base_url": "https://www.mathrubhumi.com/",
        "news_urls": [
            "https://www.mathrubhumi.com/agriculture",
            "https://www.mathrubhumi.com/agriculture/news"
        ],
        "selectors": {
            "title": "h1, h2, .story-headline, .news-title, .article-title",
            "content": ".story-content, .article-body, .news-body, .content, .full-story, p",
            "date": ".story-date, .publish-date, .news-date"
        },
        "category": "malayalam_media",
        "language": "malayalam",
        "scrape_method": "requests_bs4"
    },
    

    
    # WORKING RESEARCH INSTITUTES
    "cpcri_coconut": {
        "name": "CPCRI - Central Plantation Crops Research Institute",
        "base_url": "https://cpcri.icar.gov.in/",
        "news_urls": [
            "https://cpcri.icar.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .title, .research-title",
            "content": ".content, .research-content, .main-content, p",
            "date": ".date, .research-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "ctcri_tuber": {
        "name": "CTCRI - Central Tuber Crops Research Institute",
        "base_url": "https://ctcri.icar.gov.in/",
        "news_urls": [
            "https://ctcri.icar.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .title, .research-title",
            "content": ".content, .research-content, .main-content, p",
            "date": ".date, .research-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "cmfri_fisheries": {
        "name": "CMFRI - Central Marine Fisheries Research Institute",
        "base_url": "https://cmfri.icar.gov.in/",
        "news_urls": [
            "https://cmfri.icar.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .title, .research-title",
            "content": ".content, .research-content, .main-content, p",
            "date": ".date, .research-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # WORKING COMMODITY BOARDS
    "coconut_development_board": {
        "name": "Coconut Development Board",
        "base_url": "https://coconutboard.gov.in/",
        "news_urls": [
            "https://coconutboard.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .title, .news-title",
            "content": ".content, .news-content, .main-content, p",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "spices_board_india": {
        "name": "Spices Board of India",
        "base_url": "https://www.spicesboard.gov.in/",
        "news_urls": [
            "https://www.spicesboard.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .title, .news-title",
            "content": ".content, .news-content, .main-content, p",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # NEW WORKING SOURCES - VERIFIED 2025
    "mongabay_kerala_climate": {
        "name": "Mongabay Kerala Climate Agriculture",
        "base_url": "https://india.mongabay.com/",
        "news_urls": [
            "https://india.mongabay.com/short-article/kerala-unveils-plan-to-tackle-climate-risks-and-build-resilient-agriculture/"
        ],
        "selectors": {
            "title": "h1, h2, .entry-title, .article-title",
            "content": ".entry-content, .article-content, .content, p",
            "date": ".entry-date, .article-date, .date"
        },
        "category": "climate_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "indian_express_kerala_agri": {
        "name": "Indian Express Kerala Agriculture",
        "base_url": "https://indianexpress.com/",
        "news_urls": [
            "https://indianexpress.com/article/india/kerala-to-bring-game-changer-bill-to-legalise-lease-farming-10220798/"
        ],
        "selectors": {
            "title": "h1, .headline, .story-headline",
            "content": ".story, .full-details, .content, p",
            "date": ".date, .story-date"
        },
        "category": "policy_news",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "kerala_soils_portal": {
        "name": "Kerala Soil Survey - Agriculture Websites",
        "base_url": "https://www.keralasoils.gov.in/",
        "news_urls": [
            "https://www.keralasoils.gov.in/en/agriculture-websites"
        ],
        "selectors": {
            "title": "h1, h2, .title, .page-title",
            "content": ".content, .main-content, table, p",
            "date": ".date"
        },
        "category": "soil_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "vikaspedia_kerala_agri": {
        "name": "Vikaspedia Kerala Agriculture Advisory",
        "base_url": "https://agriculture.vikaspedia.in/",
        "news_urls": [
            "https://agriculture.vikaspedia.in/viewcontent/agriculture/crop-production/tips-for-farmers/icar-agri-advisory-for-rabi-2021-22/icar-rabi-season-agro-advisory-for-kerala?lgn=en"
        ],
        "selectors": {
            "title": "h1, h2, .title, .advisory-title",
            "content": ".content, .advisory-content, .main-content, p",
            "date": ".date"
        },
        "category": "advisory",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # WORKING SPECIALIZED SOURCES
    "krishi_jagran": {
        "name": "Krishi Jagran",
        "base_url": "https://www.krishijagran.com/",
        "news_urls": [
            "https://www.krishijagran.com/"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-title, .title",
            "content": ".article-content, .news-content, .content, .post-content, p",
            "date": ".date, .article-date"
        },
        "category": "specialized_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agriculture_today": {
        "name": "Agriculture Today",
        "base_url": "https://www.agriculturetoday.in/",
        "news_urls": [
            "https://www.agriculturetoday.in/"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .post-title",
            "content": ".article-content, .post-content, .content, p",
            "date": ".article-date, .post-date"
        },
        "category": "specialized_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # WORKING FARMER PORTALS
    "farmer_portal_gov": {
        "name": "National Farmer Portal",
        "base_url": "https://farmer.gov.in/",
        "news_urls": [
            "https://farmer.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, .title, .service-title",
            "content": ".content, .service-content, .main-content, p",
            "date": ".date"
        },
        "category": "farmer_portal",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "mkisan_portal": {
        "name": "mKisan Portal",
        "base_url": "https://mkisan.gov.in/",
        "news_urls": [
            "https://mkisan.gov.in/"
        ],
        "selectors": {
            "title": "h1, h2, .title, .advisory-title",
            "content": ".content, .advisory-content, .main-content, p",
            "date": ".date"
        },
        "category": "farmer_portal",
        "language": "english",
        "scrape_method": "requests_bs4"
    }
}

# ENHANCED FARMER ADVISORY KEYWORDS
KERALA_AGRICULTURE_KEYWORDS = [
    # Farmer advisory terms
    "farmer advisory", "agricultural guidance", "farming tips", "cultivation guide",
    "crop management", "pest management", "disease control", "fertilizer application",
    "irrigation management", "harvest time", "post harvest", "storage techniques",
    "market prices", "price forecast", "selling guide", "crop insurance",
    
    # Kerala location terms
    "kerala", "kerala agriculture", "kerala farming", "kerala farmers",
    "kerala weather", "kerala monsoon", "kerala crops", "kerala cultivation",
    "kottayam", "ernakulam", "kochi", "thiruvananthapuram", "kozhikode",
    "thrissur", "palakkad", "malappuram", "kannur", "kasaragod", "kollam",
    "pathanamthitta", "alappuzha", "idukki", "wayanad",
    
    # Kerala crops & specialties - detailed
    "coconut", "rice", "paddy", "rubber", "pepper", "cardamom", "ginger",
    "turmeric", "coconut farming", "rice cultivation", "paddy cultivation",
    "rubber plantation", "spice cultivation", "banana", "plantain",
    "cashew", "arecanut", "vanilla", "clove", "nutmeg", "cinnamon",
    "jackfruit", "mango", "tapioca", "cassava", "yam", "elephant yam",
    "coconut oil", "copra", "coir", "betel vine", "cocoa", "coffee",
    "gac fruit", "tilapia", "fish farming", "tissue culture",
    
    # Current 2025 terms
    "climate resilient agriculture", "creea report", "lease farming bill",
    "k-crail labs", "carbon neutral farming", "precision agriculture",
    "biogas units", "solar pumps", "pest surveillance", "karshaka santhwanam",
    
    # Farming practices
    "farming", "agriculture", "cultivation", "crop", "harvest", "irrigation",
    "organic farming", "sustainable farming", "pest control", "fertilizer",
    "seeds", "planting", "sowing", "weeding", "pruning", "crop rotation",
    "polyculture", "mixed farming", "precision agriculture", "drip irrigation",
    
    # Weather and advisory
    "monsoon", "rainfall", "weather forecast", "weather advisory",
    "agromet bulletin", "climate change", "drought", "flood", "storm",
    "temperature", "humidity", "cyclone", "weather warning",
    
    # Technology and innovation
    "farm technology", "digital agriculture", "mobile app", "online advisory",
    "agri portal", "farm mechanization", "greenhouse", "smart farming",
    
    # Malayalam terms - comprehensive
    "കൃഷി", "കർഷകൻ", "കർഷകർ", "നെല്ല്", "തേങ്ങ", "റബ്ബർ", "ഇഞ്ചി",
    "ഏലം", "കുരുമുളക്", "വാഴ", "കാപ്പി", "ചായ", "കശുമാവ്", "അടക്ക",
    "മഴ", "വരൾച്ച", "കാലാവസ്ഥ", "മൺസൂൺ", "വിള", "വിളവ്", "വിത്ത്",
    "കേരളം", "കേരള കൃഷി", "കേരള കർഷകർ",
    "കൃഷി മാർഗ്ഗനിർദ്ദേശം", "കർഷക ഉപദേശം", "കൃഷി രീതികൾ", "വിള പരിപാലനം",
    "കീട നിയന്ത്രണം", "രോഗ നിയന്ത്രണം", "വളം പ്രയോഗം", "വിളവെടുപ്പ്",
    "വിപണി വില", "വില പ്രവചനം", "കാലാവസ്ഥാ മുന്നറിയിപ്പ്",
    "ഗാക് ഫ്രൂട്ട്", "തിലാപ്പിയ", "മത്സ്യകൃഷി", "ടിഷ്യൂ കൾച്ചർ",
    "വാഴക്കൃഷി", "തേങ്ങാവില", "വില വർധന", "പുതിയ ഇനം"
]

# MINIMAL REJECT KEYWORDS
REJECT_KEYWORDS = [
    "cinema", "movie", "sports", "cricket", "politics", "election",
    "സിനിമ", "ക്രിക്കറ്റ്", "രാഷ്ട്രീയം"
]
