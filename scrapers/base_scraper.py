"""
DEEP WEBSITE SCRAPER - Goes Beyond First Page
Finds article listings, follows pagination, scrapes individual articles
"""
import requests
import time
import random
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re
import unicodedata
from urllib.parse import urljoin, urlparse

class BaseScraper(ABC):
    """Deep scraper that explores websites thoroughly"""
    
    def __init__(self, source_config):
        self.source_config = source_config
        self.session = requests.Session()
        self.scraped_urls = set()  # Track scraped URLs to avoid duplicates
        self.setup_session()
        self.setup_logging()
        
    def setup_session(self):
        """Configure requests session"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })
        self.session.timeout = 15
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_page(self, url):
        """Fetch webpage"""
        if url in self.scraped_urls:
            return None  # Already scraped
        
        for attempt in range(2):
            try:
                response = self.session.get(url, allow_redirects=True)
                response.raise_for_status()
                
                if response.apparent_encoding:
                    response.encoding = response.apparent_encoding
                else:
                    response.encoding = 'utf-8'
                
                self.scraped_urls.add(url)
                return response.text
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < 1:
                    time.sleep(2)
        return None
    
    def parse_html(self, html_content):
        """Parse HTML"""
        return BeautifulSoup(html_content, 'html.parser')
    
    def clean_text(self, text):
        """Clean text"""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove UI noise
        ui_noise = [
            'Share Filter BY DATE Last Hour Today This Week This Month This Hour TYPE Video Photo Article Podcast DURATION Short Medium Long Agriculture News',
            'Home > News > Agriculture',
            'Follow us on',
            'Subscribe now',
            'Related Articles',
            'Advertisement',
            'Sponsored Content'
        ]
        
        for noise in ui_noise:
            text = text.replace(noise, '')
        
        return text.strip()
    
    def is_meaningful_content(self, title, content):
        """Validate content"""
        if not title or not content:
            return False, "Empty content"
        
        if len(content) < 50:
            return False, f"Too short ({len(content)} chars)"
        
        words = content.split()
        if len(words) < 10:
            return False, f"Too few words ({len(words)})"
        
        from config.sources import KERALA_AGRICULTURE_KEYWORDS, REJECT_KEYWORDS
        
        combined_text = (title + " " + content).lower()
        
        # Check rejects
        reject_terms = ['cinema', 'movie', 'cricket', 'sports', 'politics']
        reject_count = sum(1 for term in reject_terms if term in combined_text)
        if reject_count > 0:
            return False, "Contains non-agriculture terms"
        
        # Check agriculture relevance
        agriculture_terms = [
            'agriculture', 'farming', 'crop', 'farmer', 'cultivation', 'harvest',
            'coconut', 'rice', 'rubber', 'spice', 'kerala', 'weather', 'rain',
            'price', 'market', 'export', 'import', 'government', 'scheme',
            'കൃഷി', 'കർഷക', 'നെല്ല്', 'തേങ്ങ', 'റബ്ബർ', 'കേരളം'
        ]
        
        agri_score = sum(1 for term in agriculture_terms if term in combined_text)
        
        if agri_score >= 1:
            return True, "Good content"
        else:
            return False, f"No agriculture relevance"
    
    def find_article_listing_pages(self, soup, base_url):
        """Find pages that contain article listings"""
        listing_pages = []
        
        # Look for pagination links
        pagination_selectors = [
            '.pagination a', '.pager a', '.page-numbers a',
            'a[href*="page"]', 'a[href*="Page"]',
            '.next a', '.more a', 'a[rel="next"]'
        ]
        
        for selector in pagination_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        if full_url not in listing_pages and len(listing_pages) < 5:  # Limit to 5 pages
                            listing_pages.append(full_url)
            except:
                continue
        
        # Look for category/section links
        category_selectors = [
            'a[href*="agriculture"]', 'a[href*="farming"]', 'a[href*="crop"]',
            'a[href*="news"]', 'a[href*="category"]', 'a[href*="section"]',
            '.menu a', '.nav a', '.category a'
        ]
        
        for selector in category_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    link_text = link.get_text().strip().lower()
                    
                    # Check if link text suggests agriculture content
                    if any(term in link_text for term in ['agriculture', 'farming', 'crop', 'news']):
                        if href:
                            full_url = urljoin(base_url, href)
                            if full_url not in listing_pages and len(listing_pages) < 10:
                                listing_pages.append(full_url)
            except:
                continue
        
        return listing_pages
    
    def find_individual_article_links(self, soup, base_url):
        """Find links to individual articles on listing pages"""
        article_links = []
        
        # Common patterns for article links
        article_link_patterns = [
            # Links with article-indicating classes/attributes
            '.article-title a', '.news-title a', '.post-title a',
            '.headline a', '.story-headline a', '.entry-title a',
            'h1 a', 'h2 a', 'h3 a',
            
            # Links in article containers
            '.article a', '.news-item a', '.post a',
            '.story a', '.content a[href*="article"]',
            
            # Links with date patterns (likely articles)
            'a[href*="2025"]', 'a[href*="2024"]',
            
            # Links in list structures
            'li a', '.list a', 'ul a'
        ]
        
        for pattern in article_link_patterns:
            try:
                links = soup.select(pattern)
                for link in links:
                    href = link.get('href')
                    link_text = link.get_text().strip()
                    
                    if not href or len(link_text) < 10:
                        continue
                    
                    # Check if it looks like an article
                    if self.looks_like_article_link(href, link_text):
                        full_url = urljoin(base_url, href)
                        if full_url not in article_links and len(article_links) < 20:
                            article_links.append(full_url)
            except:
                continue
        
        return article_links
    
    def looks_like_article_link(self, href, link_text):
        """Check if a link looks like it leads to an article"""
        # Skip navigation/UI links
        skip_patterns = [
            'javascript:', 'mailto:', 'tel:', '#',
            '/login', '/register', '/contact', '/about',
            'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'whatsapp.com'
        ]
        
        for pattern in skip_patterns:
            if pattern in href.lower():
                return False
        
        # Skip very short or generic link text
        generic_texts = [
            'home', 'about', 'contact', 'login', 'register',
            'more', 'read more', 'click here', 'next', 'previous',
            'share', 'like', 'follow', 'subscribe'
        ]
        
        if link_text.lower().strip() in generic_texts:
            return False
        
        # Prefer links that look like article titles
        article_indicators = [
            'agriculture', 'farming', 'crop', 'farmer', 'cultivation',
            'harvest', 'coconut', 'rice', 'rubber', 'kerala', 'price',
            'market', 'weather', 'government', 'scheme', 'news',
            'കൃഷി', 'കർഷക', 'കേരളം', 'വില'
        ]
        
        combined_text = (href + " " + link_text).lower()
        has_agriculture = any(term in combined_text for term in article_indicators)
        
        # Also accept if it looks like a news article (has reasonable length title)
        looks_like_title = len(link_text) > 15 and len(link_text) < 200
        
        return has_agriculture or looks_like_title
    
    def scrape_deep_content(self, base_urls):
        """Deep scraping - goes beyond first page"""
        articles = []
        
        for base_url in base_urls:
            try:
                self.logger.info(f"🔍 DEEP SCRAPING: {base_url}")
                
                # Step 1: Get the main page
                html = self.get_page(base_url)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                
                # Step 2: Extract content from main page if any
                main_content = self.extract_content(soup, base_url)
                if main_content:
                    articles.append(self.create_article_dict(main_content, base_url))
                
                # Step 3: Find article listing pages (pagination, categories)
                listing_pages = self.find_article_listing_pages(soup, base_url)
                self.logger.info(f"📄 Found {len(listing_pages)} listing pages")
                
                # Step 4: Process each listing page
                for listing_url in listing_pages:
                    try:
                        self.logger.info(f"📋 Processing listing: {listing_url}")
                        
                        listing_html = self.get_page(listing_url)
                        if listing_html:
                            listing_soup = self.parse_html(listing_html)
                            
                            # Step 5: Find individual article links
                            article_links = self.find_individual_article_links(listing_soup, base_url)
                            self.logger.info(f"🔗 Found {len(article_links)} article links")
                            
                            # Step 6: Scrape each individual article
                            for article_url in article_links[:10]:  # Limit to prevent overload
                                try:
                                    self.logger.info(f"📰 Scraping article: {article_url}")
                                    
                                    article_html = self.get_page(article_url)
                                    if article_html:
                                        article_soup = self.parse_html(article_html)
                                        article_content = self.extract_content(article_soup, article_url)
                                        
                                        if article_content:
                                            articles.append(self.create_article_dict(article_content, article_url))
                                            self.logger.info(f"✅ ARTICLE SCRAPED: {article_content['title'][:50]}...")
                                    
                                    self.rate_limit()
                                    
                                except Exception as e:
                                    self.logger.debug(f"Error scraping article {article_url}: {str(e)}")
                                    continue
                        
                        self.rate_limit()
                        
                    except Exception as e:
                        self.logger.debug(f"Error processing listing {listing_url}: {str(e)}")
                        continue
                
            except Exception as e:
                self.logger.error(f"Error deep scraping {base_url}: {str(e)}")
                continue
        
        return articles
    
    def extract_content(self, soup, url):
        """Extract content using multiple methods"""
        methods = [
            self.try_configured_selectors,
            self.try_article_selectors,
            self.try_paragraph_extraction
        ]
        
        for method in methods:
            try:
                result = method(soup)
                if result:
                    title, content = result
                    is_good, reason = self.is_meaningful_content(title, content)
                    if is_good:
                        return {'title': title, 'content': content}
                    else:
                        self.logger.debug(f"Content rejected: {reason}")
            except:
                continue
        
        return None
    
    def try_configured_selectors(self, soup):
        """Try configured selectors"""
        selectors = self.source_config.get('selectors', {})
        
        # Title
        title = "Agriculture News"
        title_selectors = selectors.get('title', 'h1').split(', ')
        
        for title_sel in title_selectors:
            try:
                title_elem = soup.select_one(title_sel.strip())
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    if len(title) > 5:
                        break
            except:
                continue
        
        # Content
        content_selectors = selectors.get('content', '.content').split(', ')
        
        for content_sel in content_selectors:
            try:
                content_elem = soup.select_one(content_sel.strip())
                if content_elem:
                    for noise in content_elem(['script', 'style', 'nav']):
                        noise.decompose()
                    
                    content = self.clean_text(content_elem.get_text())
                    if len(content) > 50:
                        return (title, content)
            except:
                continue
        
        return None
    
    def try_article_selectors(self, soup):
        """Try common article selectors"""
        title = "Agriculture Info"
        
        for title_sel in ['h1', 'h2', '.title', '.headline', '.story-headline']:
            try:
                title_elem = soup.select_one(title_sel)
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    if len(title) > 5:
                        break
            except:
                continue
        
        content_selectors = [
            'article', '.article-content', '.story-content', '.news-content',
            '.post-content', '.content', '.main-content', 'main'
        ]
        
        for content_sel in content_selectors:
            try:
                content_elem = soup.select_one(content_sel)
                if content_elem:
                    for noise in content_elem(['script', 'style', 'nav', 'footer']):
                        noise.decompose()
                    
                    content = self.clean_text(content_elem.get_text())
                    if len(content) > 50:
                        return (title, content)
            except:
                continue
        
        return None
    
    def try_paragraph_extraction(self, soup):
        """Extract from paragraphs"""
        title = "Agriculture News"
        
        for title_sel in ['h1', 'h2', 'h3']:
            try:
                title_elem = soup.select_one(title_sel)
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    if len(title) > 5:
                        break
            except:
                continue
        
        paragraphs = soup.find_all('p')
        content_parts = []
        
        for p in paragraphs:
            p_text = self.clean_text(p.get_text())
            if len(p_text) > 20:
                content_parts.append(p_text)
        
        if len(content_parts) >= 2:
            content = ' '.join(content_parts[:10])
            return (title, content)
        
        return None
    
    def create_article_dict(self, content_data, url):
        """Create article dictionary"""
        return {
            'url': url,
            'source': self.source_config['name'],
            'category': self.source_config['category'],
            'language': self.source_config['language'],
            'scraped_at': datetime.now().isoformat(),
            'title': content_data['title'],
            'content': content_data['content'],
            'keywords': self.extract_keywords(content_data['title'] + " " + content_data['content'])
        }
    
    def extract_keywords(self, text):
        """Extract keywords"""
        from config.sources import KERALA_AGRICULTURE_KEYWORDS
        
        keywords = []
        text_lower = text.lower()
        
        for keyword in KERALA_AGRICULTURE_KEYWORDS[:20]:
            if keyword.lower() in text_lower:
                keywords.append(keyword)
        
        return keywords[:8]
    
    def rate_limit(self):
        """Rate limiting"""
        time.sleep(1.5 + random.uniform(0, 1))
    
    @abstractmethod
    def scrape_articles(self):
        pass
    
    def run(self):
        """Run deep scraper"""
        self.logger.info(f"Starting DEEP SCRAPER for {self.source_config['name']}")
        articles = self.scrape_articles()
        self.logger.info(f"Found {len(articles)} articles through deep scraping")
        return articles
