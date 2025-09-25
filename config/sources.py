"""
EXPANDED Kerala Agriculture Sources - ALL FREE, NO PAYWALLS
Focus: Agriculture practices, crops, weather for Kerala ONLY
"""

ALL_SOURCES = {
    # EXISTING GOVERNMENT SOURCES (keep these)
    "kerala_agriculture_dept": {
        "name": "Kerala Agriculture Department",
        "base_url": "https://keralaagriculture.gov.in/",
        "news_urls": [
            "https://keralaagriculture.gov.in/en/news/",
            "https://keralaagriculture.gov.in/"
        ],
        "selectors": {
            "title": "h1, .post-title, .entry-title, .title",
            "content": ".post-content, .entry-content, .content, .main-content, article",
            "date": ".post-date, .entry-date, .date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "fib_kerala": {
        "name": "Farm Information Bureau Kerala",
        "base_url": "https://fibkerala.gov.in/",
        "news_urls": [
            "https://fibkerala.gov.in/node/56",
            "https://fibkerala.gov.in/node/33"
        ],
        "selectors": {
            "title": "h1, .field-name-title, .title",
            "content": ".field-name-body, .node-content, .content",
            "date": ".submitted, .post-date, .date"
        },
        "category": "government",
        "language": "mixed",
        "scrape_method": "requests_bs4"
    },
    
    "kerala_agricultural_university": {
        "name": "Kerala Agricultural University",
        "base_url": "https://kau.in/",
        "news_urls": [
            "https://kau.in/news"
        ],
        "selectors": {
            "title": "h1, .title, .post-title, .news-title",
            "content": ".content, .post-content, .article-body, .news-content",
            "date": ".date, .post-date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "imd_kerala_weather": {
        "name": "IMD Kerala Weather",
        "base_url": "https://mausam.imd.gov.in/thiruvananthapuram/",
        "news_urls": [
            "https://mausam.imd.gov.in/thiruvananthapuram/"
        ],
        "selectors": {
            "title": "h1, h2, .weather-title, .forecast-title",
            "content": ".weather-content, .forecast-content, table, .weather-data",
            "date": ".date, .forecast-date, .weather-date"
        },
        "category": "weather",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # NEW MALAYALAM NEWS SOURCES - ADDED FOR REAL NEWS
    "mathrubhumi_agriculture": {
        "name": "Mathrubhumi Agriculture News",
        "base_url": "https://www.mathrubhumi.com/",
        "news_urls": [
            "https://www.mathrubhumi.com/agriculture",
            "https://www.mathrubhumi.com/agriculture/news"
        ],
        "selectors": {
            "title": "h1, h2, .story-headline, .news-title, .article-title",
            "content": ".story-content, .article-body, .news-body, .content, p",
            "date": ".story-date, .publish-date, .news-date"
        },
        "category": "malayalam_media",
        "language": "malayalam",
        "scrape_method": "requests_bs4"
    },
    
    "mathrubhumi_english_agriculture": {
        "name": "Mathrubhumi English Agriculture",
        "base_url": "https://english.mathrubhumi.com/",
        "news_urls": [
            "https://english.mathrubhumi.com/features/agriculture"
        ],
        "selectors": {
            "title": "h1, h2, .story-headline, .news-title, .article-title",
            "content": ".story-content, .article-body, .news-body, .content, p",
            "date": ".story-date, .publish-date, .news-date"
        },
        "category": "english_media",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "manorama_agriculture": {
        "name": "Manorama Agriculture News",
        "base_url": "https://www.manoramaonline.com/",
        "news_urls": [
            "https://www.manoramaonline.com/agri-news/agriculture.html"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-headline, .story-title",
            "content": ".article-content, .news-body, .story-content, p",
            "date": ".article-date, .news-date, .publish-date"
        },
        "category": "malayalam_media",
        "language": "malayalam",
        "scrape_method": "requests_bs4"
    },
    
    # EXISTING GOVERNMENT SOURCES CONTINUE
    "kottayam_collector_agriculture": {
        "name": "Kottayam Collector Office Agriculture",
        "base_url": "https://kottayam.nic.in/",
        "news_urls": [
            "https://kottayam.nic.in/agriculture/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "ernakulam_collector_agriculture": {
        "name": "Ernakulam Collector Office Agriculture",
        "base_url": "https://ernakulam.nic.in/",
        "news_urls": [
            "https://ernakulam.nic.in/agriculture/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "kerala_state_planning_board": {
        "name": "Kerala State Planning Board",
        "base_url": "https://spb.kerala.gov.in/",
        "news_urls": [
            "https://spb.kerala.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # COOPERATIVE SOCIETIES - Free, Agriculture-Focused
    "milma_kerala": {
        "name": "MILMA Kerala Dairy",
        "base_url": "https://www.milma.com/",
        "news_urls": [
            "https://www.milma.com/news",
            "https://www.milma.com/"
        ],
        "selectors": {
            "title": "h1, .news-title, .title",
            "content": ".news-content, .content, .main-content",
            "date": ".news-date, .date"
        },
        "category": "cooperative",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "supplyco_kerala": {
        "name": "SUPPLYCO Kerala",
        "base_url": "https://supplycokerala.com/",
        "news_urls": [
            "https://supplycokerala.com/"
        ],
        "selectors": {
            "title": "h1, .news-title, .title",
            "content": ".news-content, .content, .main-content",
            "date": ".news-date, .date"
        },
        "category": "cooperative",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "horticorp_kerala": {
        "name": "Kerala State Horticorp",
        "base_url": "https://horticorp.kerala.gov.in/",
        "news_urls": [
            "https://horticorp.kerala.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "government",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # COMMODITY BOARDS - Spice & Agriculture Boards
    "spices_board_india": {
        "name": "Spices Board of India",
        "base_url": "https://www.spicesboard.gov.in/",
        "news_urls": [
            "https://www.spicesboard.gov.in/news-events.html"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "cardamom_board": {
        "name": "Cardamom Board of India",
        "base_url": "https://cardamomboard.gov.in/",
        "news_urls": [
            "https://cardamomboard.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "coconut_development_board": {
        "name": "Coconut Development Board",
        "base_url": "https://coconutboard.gov.in/",
        "news_urls": [
            "https://coconutboard.gov.in/news.html"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "rubber_board": {
        "name": "Rubber Board of India",
        "base_url": "https://rubberboard.gov.in/",
        "news_urls": [
            "https://rubberboard.gov.in/news.htm"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "commodity_board",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # RESEARCH INSTITUTES - Agriculture Research
    "ctcri_cassava": {
        "name": "CTCRI - Central Tuber Crops Research Institute",
        "base_url": "https://ctcri.icar.gov.in/",
        "news_urls": [
            "https://ctcri.icar.gov.in/news.php"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "cpcri_coconut": {
        "name": "CPCRI - Central Plantation Crops Research Institute",
        "base_url": "https://cpcri.icar.gov.in/",
        "news_urls": [
            "https://cpcri.icar.gov.in/news.php"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "cmfri_fisheries": {
        "name": "CMFRI - Central Marine Fisheries Research Institute",
        "base_url": "https://cmfri.icar.gov.in/",
        "news_urls": [
            "https://cmfri.icar.gov.in/news.php"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "research",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # NEW SPECIALIZED AGRICULTURE SOURCES - ADDED
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
    
    # EXISTING PORTALS CONTINUE
    "agri_tech_portal": {
        "name": "Agriculture Technology Portal",
        "base_url": "https://www.agritech.tnau.ac.in/",
        "news_urls": [
            "https://www.agritech.tnau.ac.in/agriculture.html"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "specialized_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "farmer_portal": {
        "name": "National Farmer Portal",
        "base_url": "https://farmer.gov.in/",
        "news_urls": [
            "https://farmer.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "specialized_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "kisan_call_center": {
        "name": "Kisan Call Center Portal",
        "base_url": "https://mkisan.gov.in/",
        "news_urls": [
            "https://mkisan.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .news-title",
            "content": ".content, .news-content, .main-content",
            "date": ".date, .news-date"
        },
        "category": "specialized_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # WEATHER SOURCES - Kerala Specific
    "kerala_meteorological_center": {
        "name": "Kerala Meteorological Center",
        "base_url": "https://mausam.imd.gov.in/kochi/",
        "news_urls": [
            "https://mausam.imd.gov.in/kochi/"
        ],
        "selectors": {
            "title": "h1, h2, .weather-title",
            "content": ".weather-content, .forecast-content, table",
            "date": ".date, .forecast-date"
        },
        "category": "weather",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "kerala_disaster_management": {
        "name": "Kerala Disaster Management Authority",
        "base_url": "https://sdma.kerala.gov.in/",
        "news_urls": [
            "https://sdma.kerala.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .alert-title",
            "content": ".content, .alert-content, .main-content",
            "date": ".date, .alert-date"
        },
        "category": "weather",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # OPEN DATA PORTALS - Government Data
    "kerala_open_data": {
        "name": "Kerala Open Data Portal",
        "base_url": "https://kerala.data.gov.in/",
        "news_urls": [
            "https://kerala.data.gov.in/"
        ],
        "selectors": {
            "title": "h1, .title, .dataset-title",
            "content": ".content, .dataset-content, .main-content",
            "date": ".date, .dataset-date"
        },
        "category": "open_data",
        "language": "english",
        "scrape_method": "requests_bs4"
    }
}

# ENHANCED KERALA AGRICULTURE KEYWORDS - UPDATED WITH CURRENT NEWS TERMS
KERALA_AGRICULTURE_KEYWORDS = [
    # Kerala location terms
    "kerala", "kerala agriculture", "kerala farming", "kerala farmers",
    "kerala weather", "kerala monsoon", "kerala crops", "kerala cultivation",
    "kottayam", "ernakulam", "kochi", "thiruvananthapuram", "kozhikode",
    "thrissur", "palakkad", "malappuram", "kannur", "kasaragod", "kollam",
    "pathanamthitta", "alappuzha", "idukki", "wayanad",
    
    # Kerala crops & specialties
    "coconut", "rice", "paddy", "rubber", "pepper", "cardamom", "ginger",
    "turmeric", "coconut farming", "rice cultivation", "paddy cultivation",
    "rubber plantation", "spice cultivation", "banana", "plantain",
    "cashew", "arecanut", "vanilla", "clove", "nutmeg", "cinnamon",
    "jackfruit", "mango", "tapioca", "cassava", "yam", "elephant yam",
    "coconut oil", "copra", "coir", "betel vine", "cocoa", "coffee",
    "gac fruit", "tilapia", "fish farming", "tissue culture", 
    
    # Current news terms - ADDED FOR REAL NEWS
    "price rise", "market price", "export", "import", "demand", "supply",
    "weather station", "climate resilience", "lease farming", "bill",
    "new variety", "patent", "research", "technology", "innovation",
    "gopika rice", "integrated farming", "banana cultivation", "rubber price",
    
    # Farming practices
    "farming", "agriculture", "cultivation", "crop", "harvest", "irrigation",
    "organic farming", "sustainable farming", "pest control", "fertilizer",
    "seeds", "planting", "sowing", "weeding", "pruning", "crop rotation",
    "polyculture", "mixed farming", "precision agriculture", "drip irrigation",
    
    # Weather for Kerala
    "monsoon", "rainfall", "weather forecast", "southwest monsoon",
    "northeast monsoon", "pre monsoon", "post monsoon", "drought",
    "flood", "temperature", "humidity", "cyclone", "weather advisory",
    "rainfall prediction", "weather warning", "storm", "heavy rain",
    
    # Agricultural technology
    "farm machinery", "tractor", "harvester", "sprayer", "greenhouse",
    "nursery", "seedling", "transplanting", "mulching", "composting",
    
    # Malayalam terms - ENHANCED WITH CURRENT NEWS
    "കൃഷി", "കർഷകൻ", "കർഷകർ", "നെല്ല്", "തേങ്ങ", "റബ്ബർ", "ഇഞ്ചി",
    "ഏലം", "കുരുമുളക്", "വാഴ", "കാപ്പി", "ചായ", "കശുമാവ്", "അടക്ക",
    "മഴ", "വരൾച്ച", "കാലാവസ്ഥ", "മൺസൂൺ", "വിള", "വിളവ്", "വിത്ത്",
    "കേരളം", "കേരള കൃഷി", "കേരള കർഷകർ",
    # Current Malayalam news terms
    "ഗാക് ഫ്രൂട്ട്", "തിലാപ്പിയ", "മത്സ്യകൃഷി", "ടിഷ്യൂ കൾച്ചർ", 
    "വാഴക്കൃഷി", "തേങ്ങാവില", "വില വർധന", "പുതിയ ഇനം", 
    "ഗോപിക", "നെൽവിത്ത്", "റബ്ബർ വില", "ചൈനയിൽ ആവശ്യം"
]

# SIMPLE REJECT KEYWORDS
REJECT_KEYWORDS = [
    "politics", "election", "minister speech", "court", "police", "arrest",
    "cinema", "movie", "actor", "sports", "cricket", "football",
    "school", "college", "exam", "student", "railway", "bus",
    "entertainment", "celebrity", "fashion", "music", "dance",
    "സിനിമ", "രാഷ്ട്രീയം", "തിരഞ്ഞെടുപ്പ്", "കോടതി", "പോലീസ്", "ക്രിക്കറ്റ്"
]
