"""
Agriculture Sources - NO FILTERING
"""

ALL_SOURCES = {
    "economic_times_agriculture": {
        "name": "Economic Times Agriculture",
        "base_url": "https://economictimes.indiatimes.com/",
        "news_urls": [
            "https://economictimes.indiatimes.com/news/economy/agriculture?from=mdr"
        ],
        "selectors": {
            "title": "h1, h2, h3, .story-headline, .headline, .artTitle, .eachStory h3",
            "content": ".artText, .story-content, .article-content, .summary, .eachStory, p",
            "date": ".date, .publish-date, .story-date, .time"
        },
        "category": "business_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "times_of_india_agriculture": {
        "name": "Times of India Agriculture",
        "base_url": "https://timesofindia.indiatimes.com/",
        "news_urls": [
            "https://timesofindia.indiatimes.com/topic/agriculture/news"
        ],
        "selectors": {
            "title": "h1, h2, h3, .headline, .story-headline, ._2-bYW, .EOHY_ZZ",
            "content": ".story-content, .article-content, ._s30J, .ga-headlines, .content, p",
            "date": "time, .publish_on, .date, ._3k8Kt"
        },
        "category": "news_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    }
}

# NO KEYWORD FILTERING - These are just for reference, not used for filtering
KERALA_AGRICULTURE_KEYWORDS = []
REJECT_KEYWORDS = []
