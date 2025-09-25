"""
SIMPLE Base Scraper for Kerala Agriculture Content
Focus: Clean headlines + content from reliable, paywall-free sources
"""
import requests
import time
import random
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re

class BaseScraper(ABC):
    """Simple base class focused on Kerala agriculture content only"""
    
    def __init__(self, source_config):
        self.source_config = source_config
        self.session = requests.Session()
        self.setup_session()
        self.setup_logging()
        
    def setup_session(self):
        """Configure requests session with proper headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        })
        self.session.timeout = 15
        
    def setup_logging(self):
        """Setup simple logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_page(self, url):
        """Fetch webpage content with retry mechanism"""
        for attempt in range(3):
            try:
                self.logger.info(f"Fetching (attempt {attempt + 1}): {url}")
                response = self.session.get(url, allow_redirects=True)
                response.raise_for_status()
                
                # Check if page contains actual content
                if len(response.text) < 500:
                    self.logger.warning(f"Page too short, might be empty: {url}")
                    continue
                    
                return response.text
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < 2:
                    time.sleep(2 + attempt)  # Progressive delay
            except Exception as e:
                self.logger.error(f"Unexpected error for {url}: {str(e)}")
                break
        
        self.logger.error(f"Failed to fetch {url} after 3 attempts")
        return None
    
    def parse_html(self, html_content):
        """Parse HTML content with BeautifulSoup"""
        try:
            return BeautifulSoup(html_content, 'lxml')
        except Exception:
            # Fallback to html.parser if lxml fails
            return BeautifulSoup(html_content, 'html.parser')
    
    def clean_text(self, text):
        """Enhanced text cleaning for agriculture content"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove common subscription/paywall messages
        paywall_patterns = [
            r'activate your premium subscription.*?today',
            r'copyright.*?all rights reserved',
            r'subscribe now.*?continue reading',
            r'premium content.*?login',
            r'register to read.*?more',
            r'this content is.*?subscribers only',
            r'subscribe to.*?unlimited access',
            r'sign up.*?continue',
            r'login.*?continue reading',
            r'become a member.*?access'
        ]
        
        for pattern in paywall_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove navigation elements
        navigation_patterns = [
            r'home\s*>\s*news\s*>\s*agriculture',
            r'breadcrumb.*?navigation',
            r'you are here:.*?agriculture',
            r'related articles:',
            r'also read:',
            r'share this article',
            r'follow us on',
            r'subscribe to our newsletter'
        ]
        
        for pattern in navigation_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up remaining artifacts
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'[\r\t]+', ' ', text)  # Remove tabs and carriage returns
        
        return text.strip()
    
    def is_kerala_agriculture_content(self, title, content, url=""):
        """Enhanced check for Kerala agriculture content"""
        from config.sources import KERALA_AGRICULTURE_KEYWORDS, REJECT_KEYWORDS
        
        combined_text = (title + " " + content + " " + url).lower()
        
        # First, reject obvious non-agriculture content
        reject_count = 0
        for reject_term in REJECT_KEYWORDS:
            if reject_term.lower() in combined_text:
                reject_count += 1
        
        if reject_count > 0:
            self.logger.debug(f"❌ REJECTED - Contains {reject_count} rejected terms")
            return False
        
        # Check for minimum content quality
        if len(content) < 100:
            self.logger.debug(f"❌ REJECTED - Content too short ({len(content)} chars)")
            return False
        
        # Must contain Kerala references
        kerala_terms = ["kerala", "കേരളം", "kochi", "thiruvananthapuram", "ernakulam", 
                       "kottayam", "thrissur", "kozhikode", "malappuram"]
        has_kerala = any(term in combined_text for term in kerala_terms)
        
        # Must contain agriculture terms
        agriculture_count = sum(1 for keyword in KERALA_AGRICULTURE_KEYWORDS 
                              if keyword.lower() in combined_text)
        
        # Scoring system for relevance
        relevance_score = 0
        if has_kerala:
            relevance_score += 2
        if agriculture_count >= 3:
            relevance_score += 3
        elif agriculture_count >= 2:
            relevance_score += 2
        elif agriculture_count >= 1:
            relevance_score += 1
        
        # Check for specific Kerala agriculture indicators
        kerala_agri_indicators = [
            "coconut farming", "rice cultivation", "rubber plantation", "spice cultivation",
            "cardamom", "pepper farming", "kerala agriculture", "kerala farming",
            "kau", "kerala agricultural university", "കേരള കൃഷി"
        ]
        
        for indicator in kerala_agri_indicators:
            if indicator in combined_text:
                relevance_score += 2
                break
        
        is_relevant = relevance_score >= 4
        
        if is_relevant:
            self.logger.info(f"✅ KERALA AGRICULTURE: Score={relevance_score}, Kerala={has_kerala}, Agri={agriculture_count}")
        else:
            self.logger.debug(f"❌ NOT RELEVANT: Score={relevance_score}, Kerala={has_kerala}, Agri={agriculture_count}")
        
        return is_relevant
    
    def extract_simple_content(self, soup, url):
        """Enhanced content extraction for agriculture content"""
        selectors = self.source_config['selectors']
        
        # Extract Title with multiple fallbacks
        title = "No Title"
        title_selectors = selectors.get('title', 'h1').replace(' ', '').split(',')
        
        for selector in title_selectors:
            try:
                title_elem = soup.select_one(selector.strip())
                if title_elem:
                    title_text = self.clean_text(title_elem.get_text())
                    if len(title_text) > 10 and title_text.lower() not in ['home', 'news', 'agriculture', 'kerala']:
                        title = title_text
                        break
            except Exception as e:
                self.logger.debug(f"Title selector '{selector}' failed: {e}")
                continue
        
        # Fallback title extraction
        if title == "No Title":
            fallback_selectors = ['h1', 'h2', '.headline', '.title', '.post-title', '.article-title']
            for selector in fallback_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem:
                        title_text = self.clean_text(elem.get_text())
                        if len(title_text) > 10:
                            title = title_text
                            break
                except:
                    continue
        
        # Extract Content with multiple fallbacks
        content = ""
        content_selectors = selectors.get('content', '.content').replace(' ', '').split(',')
        
        for selector in content_selectors:
            try:
                content_elem = soup.select_one(selector.strip())
                if content_elem:
                    # Remove unwanted elements
                    unwanted_elements = [
                        'script', 'style', 'nav', 'footer', 'header',
                        '.ads', '.advertisement', '.subscription', '.paywall',
                        '.social-share', '.related-articles', '.author-bio',
                        '.tags', '.breadcrumb', '.navigation', '.menu',
                        '.sidebar', '.widget', '.popup', '.modal'
                    ]
                    
                    for unwanted in unwanted_elements:
                        for elem in content_elem.select(unwanted):
                            elem.decompose()
                    
                    content = content_elem.get_text(separator='\n', strip=True)
                    if len(content) > 150:  # Reasonable content length
                        break
            except Exception as e:
                self.logger.debug(f"Content selector '{selector}' failed: {e}")
                continue
        
        # Enhanced fallback content extraction
        if not content or len(content) < 100:
            # Try semantic HTML5 elements
            semantic_selectors = ['article', 'main', '.main-content', '.post-body', '.entry-content']
            for selector in semantic_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem:
                        for unwanted in elem(['script', 'style', 'nav', 'footer', 'header']):
                            unwanted.decompose()
                        content = elem.get_text(separator='\n', strip=True)
                        if len(content) > 150:
                            break
                except:
                    continue
        
        # Final fallback - extract from paragraphs
        if not content or len(content) < 100:
            paragraphs = soup.find_all('p')
            content_parts = []
            for p in paragraphs:
                p_text = self.clean_text(p.get_text())
                if len(p_text) > 30:  # Substantial paragraph
                    content_parts.append(p_text)
            content = '\n\n'.join(content_parts[:10])  # Max 10 paragraphs
        
        content = self.clean_text(content)
        
        # Only return if it's Kerala agriculture content
        if self.is_kerala_agriculture_content(title, content, url):
            return {
                'title': title,
                'content': content
            }
        else:
            return None
    
    def find_kerala_agriculture_urls(self, soup, base_url):
        """Find URLs likely to contain Kerala agriculture content"""
        urls = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            link_text = link.get_text().strip()
            
            if not href or len(link_text) < 8:
                continue
            
            # Skip obvious non-agriculture links
            skip_patterns = [
                'javascript:', 'mailto:', 'tel:', '#',
                'facebook.com', 'twitter.com', 'instagram.com',
                'youtube.com', 'linkedin.com'
            ]
            
            if any(pattern in href.lower() for pattern in skip_patterns):
                continue
            
            # Only include agriculture-related links
            agriculture_terms = [
                'agriculture', 'farming', 'crop', 'kerala', 'weather',
                'cultivation', 'harvest', 'irrigation', 'organic',
                'coconut', 'rice', 'rubber', 'spice', 'cardamom',
                'കൃഷി', 'കർഷക', 'കേരള'
            ]
            
            has_agriculture_term = any(term in (href + " " + link_text).lower() 
                                     for term in agriculture_terms)
            
            if has_agriculture_term:
                # Convert to full URL
                if href.startswith('/'):
                    full_url = base_url.rstrip('/') + href
                elif href.startswith('http'):
                    full_url = href
                else:
                    continue
                
                # Validate URL format
                if len(full_url) > 30 and full_url not in urls:
                    urls.append(full_url)
        
        return urls[:8]  # Limit to 8 URLs per source for efficiency
    
    def extract_keywords(self, text):
        """Extract Kerala agriculture keywords from text"""
        from config.sources import KERALA_AGRICULTURE_KEYWORDS
        
        keywords = []
        text_lower = text.lower()
        
        for keyword in KERALA_AGRICULTURE_KEYWORDS:
            if keyword.lower() in text_lower:
                keywords.append(keyword)
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def rate_limit(self):
        """Respectful rate limiting between requests"""
        delay = 1.5 + random.uniform(0, 1)  # 1.5-2.5 seconds
        time.sleep(delay)
    
    @abstractmethod
    def scrape_articles(self):
        """Abstract method for scraping - to be implemented by subclasses"""
        pass
    
    def run(self):
        """Main method to run the scraper"""
        self.logger.info(f"Starting Kerala Agriculture scraper for {self.source_config['name']}")
        
        try:
            articles = self.scrape_articles()
            self.logger.info(f"Completed scraping: {len(articles)} Kerala agriculture articles found")
            return articles
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            return []
