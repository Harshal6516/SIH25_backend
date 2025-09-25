"""
AGRICULTURE NEWS AGGREGATORS - Like Inshorts for Agriculture
Focus: Dedicated agriculture news apps and websites with curated content
"""

ALL_SOURCES = {
    # AGRICULTURE NEWS AGGREGATORS (Like Inshorts)
    "krishi_jagran_news": {
        "name": "Krishi Jagran - Daily Agriculture News",
        "base_url": "https://krishijagran.com/",
        "news_urls": [
            "https://krishijagran.com/",
            "https://krishijagran.com/agriculture-world/",
            "https://krishijagran.com/crop-production/",
            "https://krishijagran.com/mandi-price-rates/"
        ],
        "selectors": {
            "title": "h1, h2, h3, .article-title, .news-title, .title",
            "content": ".article-content, .news-content, .post-content, .content, p",
            "date": ".article-date, .news-date, .post-date"
        },
        "category": "agriculture_aggregator",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agriwatch_news": {
        "name": "AgriWatch - Agriculture Market News",
        "base_url": "https://www.agriwatch.com/",
        "news_urls": [
            "https://www.agriwatch.com/",
            "https://www.agriwatch.com/news/"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-title",
            "content": ".article-content, .news-content, p",
            "date": ".article-date, .news-date"
        },
        "category": "agriculture_aggregator",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agriculture_today": {
        "name": "Agriculture Today - Daily Agri News",
        "base_url": "https://www.agriculturetoday.in/",
        "news_urls": [
            "https://www.agriculturetoday.in/",
            "https://www.agriculturetoday.in/category/news/",
            "https://www.agriculturetoday.in/category/crop-production/"
        ],
        "selectors": {
            "title": "h1, h2, .entry-title, .post-title, .article-title",
            "content": ".entry-content, .post-content, .article-content, p",
            "date": ".entry-date, .post-date, .article-date"
        },
        "category": "agriculture_aggregator",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agritech_tomorrow": {
        "name": "AgriTech Tomorrow - Technology News",
        "base_url": "https://www.agritechtomorrow.com/",
        "news_urls": [
            "https://www.agritechtomorrow.com/"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .story-title",
            "content": ".article-content, .story-content, p",
            "date": ".article-date, .story-date"
        },
        "category": "agriculture_tech",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agdaily_news": {
        "name": "AGDAILY - Agriculture News & Trends",
        "base_url": "https://www.agdaily.com/",
        "news_urls": [
            "https://www.agdaily.com/"
        ],
        "selectors": {
            "title": "h1, h2, .entry-title, .article-title",
            "content": ".entry-content, .article-content, p",
            "date": ".entry-date, .article-date"
        },
        "category": "agriculture_aggregator",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agweb_news": {
        "name": "AgWeb - Agriculture News & Markets",
        "base_url": "https://www.agweb.com/",
        "news_urls": [
            "https://www.agweb.com/"
        ],
        "selectors": {
            "title": "h1, h2, .headline, .article-title",
            "content": ".article-content, .story-content, p",
            "date": ".article-date, .story-date"
        },
        "category": "agriculture_market",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agriculture_dive": {
        "name": "Agriculture Dive - Industry News",
        "base_url": "https://www.agriculturedive.com/",
        "news_urls": [
            "https://www.agriculturedive.com/"
        ],
        "selectors": {
            "title": "h1, h2, .headline, .article-title",
            "content": ".article-content, .story-content, p",
            "date": ".article-date, .story-date"
        },
        "category": "agriculture_industry",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agfunder_news": {
        "name": "AgFunderNews - Food & Agriculture",
        "base_url": "https://agfundernews.com/",
        "news_urls": [
            "https://agfundernews.com/"
        ],
        "selectors": {
            "title": "h1, h2, .entry-title, .article-title",
            "content": ".entry-content, .article-content, p",
            "date": ".entry-date, .article-date"
        },
        "category": "agriculture_startup",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # INDIAN AGRICULTURE SPECIFIC AGGREGATORS
    "economic_times_agriculture": {
        "name": "Economic Times Agriculture Section",
        "base_url": "https://economictimes.indiatimes.com/",
        "news_urls": [
            "https://economictimes.indiatimes.com/news/economy/agriculture"
        ],
        "selectors": {
            "title": "h1, .headline, .artTitle",
            "content": ".artText, .story-content, p",
            "date": ".date, .publish-date"
        },
        "category": "business_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "hindu_business_line_agriculture": {
        "name": "Hindu Business Line Agriculture",
        "base_url": "https://www.thehindubusinessline.com/",
        "news_urls": [
            "https://www.thehindubusinessline.com/economy/agri-business/"
        ],
        "selectors": {
            "title": "h1, .headline, .story-headline",
            "content": ".story-content, .article-content, p",
            "date": ".date, .story-date"
        },
        "category": "business_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "indian_express_agriculture": {
        "name": "Indian Express Agriculture",
        "base_url": "https://indianexpress.com/",
        "news_urls": [
            "https://indianexpress.com/about/agriculture/"
        ],
        "selectors": {
            "title": "h1, .headline, .story-headline",
            "content": ".story, .full-details, p",
            "date": ".date, .story-date"
        },
        "category": "news_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    # MALAYALAM AGRICULTURE NEWS AGGREGATORS
    "mathrubhumi_agriculture": {
        "name": "Mathrubhumi Agriculture News",
        "base_url": "https://www.mathrubhumi.com/",
        "news_urls": [
            "https://www.mathrubhumi.com/agriculture/",
            "https://www.mathrubhumi.com/agriculture/news/"
        ],
        "selectors": {
            "title": "h1, h2, .story-headline, .article-title",
            "content": ".story-content, .article-body, p",
            "date": ".story-date, .publish-date"
        },
        "category": "malayalam_agriculture",
        "language": "malayalam",
        "scrape_method": "requests_bs4"
    },
    
    "manorama_agriculture": {
        "name": "Manorama Agriculture News",
        "base_url": "https://www.manoramaonline.com/",
        "news_urls": [
            "https://www.manoramaonline.com/agri-news/agriculture.html"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-headline",
            "content": ".article-content, .news-body, p",
            "date": ".article-date, .news-date"
        },
        "category": "malayalam_agriculture",
        "language": "malayalam",
        "scrape_method": "requests_bs4"
    },
    
    # SPECIALIZED COMMODITY NEWS
    "commodity_online": {
        "name": "Commodity Online - Agriculture",
        "base_url": "https://www.commodityonline.com/",
        "news_urls": [
            "https://www.commodityonline.com/agriculture"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-title",
            "content": ".article-content, .news-content, p",
            "date": ".article-date, .news-date"
        },
        "category": "commodity_news",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "agribusiness_global": {
        "name": "AgriBusiness Global News",
        "base_url": "https://www.agribusinessglobal.com/",
        "news_urls": [
            "https://www.agribusinessglobal.com/"
        ],
        "selectors": {
            "title": "h1, h2, .article-title, .news-title",
            "content": ".article-content, .news-content, p",
            "date": ".article-date, .news-date"
        },
        "category": "agribusiness_news",
        "language": "english",
        "scrape_method": "requests_bs4"
    }
}

# ENHANCED KEYWORDS FOR NEWS AGGREGATORS
KERALA_AGRICULTURE_KEYWORDS = [
    # News-focused keywords
    "agriculture news", "farming updates", "crop news", "market news",
    "price updates", "weather alerts", "government schemes", "policy changes",
    "subsidy news", "insurance updates", "export news", "import alerts",
    
    # Kerala specific
    "kerala agriculture", "kerala farmers", "kerala crops", "kerala weather",
    "kerala market prices", "kerala government", "kerala policy",
    
    # Crop specific
    "coconut prices", "rubber market", "pepper export", "cardamom trade",
    "rice procurement", "banana cultivation", "spice prices",
    "coconut oil rates", "rubber sheet prices", "black pepper rates",
    
    # Current trends
    "digital farming", "precision agriculture", "organic certification",
    "contract farming", "food processing", "startup agriculture",
    "agtech news", "farming technology", "agricultural innovation",
    
    # Market terms
    "mandi prices", "wholesale rates", "commodity prices", "futures trading",
    "agricultural exports", "crop insurance claims", "farmer subsidies",
    
    # Weather & climate
    "monsoon forecast", "rainfall prediction", "drought alert", "flood warning",
    "crop damage", "weather advisory", "climate change impact",
    
    # Malayalam news terms
    "കൃഷി വാർത്തകൾ", "കർഷക വാർത്തകൾ", "വിള വാർത്തകൾ", "വില വാർത്തകൾ",
    "കാലാവസ്ഥാ മുന്നറിയിപ്പ്", "സർക്കാർ പദ്ധതികൾ", "സബ്സിഡി വാർത്തകൾ",
    "തേങ്ങാ വില", "റബ്ബർ വില", "കുരുമുളക് കയറ്റുമതി", "ഏലം വിപണി"
]

# REJECT KEYWORDS
REJECT_KEYWORDS = [
    "cinema", "movie", "entertainment", "sports", "cricket", "politics",
    "സിനിമ", "ക്രിക്കറ്റ്", "കായികം"
]
