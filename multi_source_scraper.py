"""
ENHANCED Kerala Agriculture Multi-Source Scraper
Focus: DEEP SCRAPING - Goes beyond first page to find more articles
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.sources import ALL_SOURCES
from scrapers.base_scraper import BaseScraper
from utils.file_manager import FileManager
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

class EnhancedKeralaAgriScraper(BaseScraper):
    """Enhanced scraper that performs DEEP SCRAPING of websites"""
    
    def __init__(self, source_config):
        super().__init__(source_config)
        self.scraped_urls = set()  # Track scraped URLs to avoid duplicates
    
    def scrape_articles(self):
        """DEEP SCRAPING - Goes beyond first page to find more articles"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"🔍 DEEP SCRAPING URL: {news_url}")
                
                # PHASE 1: Get and process main page
                html = self.get_page(news_url)
                if not html:
                    self.logger.warning(f"Could not fetch content from {news_url}")
                    continue
                
                soup = self.parse_html(html)
                
                # Extract content from main page
                main_content = self.extract_content_from_page(soup, news_url)
                if main_content:
                    articles.extend(main_content)
                    self.logger.info(f"✅ Main page: {len(main_content)} articles")
                
                # PHASE 2: Find article listing pages (pagination, categories)
                listing_pages = self.find_more_pages(soup, self.source_config['base_url'])
                self.logger.info(f"📄 Found {len(listing_pages)} additional pages")
                
                # PHASE 3: Process each additional page
                for page_url in listing_pages[:5]:  # Limit to 5 additional pages
                    try:
                        self.logger.info(f"📋 Processing additional page: {page_url}")
                        
                        page_html = self.get_page(page_url)
                        if page_html:
                            page_soup = self.parse_html(page_html)
                            page_content = self.extract_content_from_page(page_soup, page_url)
                            if page_content:
                                articles.extend(page_content)
                                self.logger.info(f"✅ Additional page: {len(page_content)} articles")
                        
                        self.rate_limit()
                        
                    except Exception as e:
                        self.logger.debug(f"Error processing page {page_url}: {str(e)}")
                        continue
                
                # PHASE 4: Find individual article links and scrape them
                individual_links = self.find_individual_articles(soup, self.source_config['base_url'])
                self.logger.info(f"🔗 Found {len(individual_links)} individual article links")
                
                for article_url in individual_links[:10]:  # Limit to 10 individual articles
                    try:
                        if article_url in self.scraped_urls:
                            continue
                        
                        self.logger.info(f"📰 Scraping individual article: {article_url}")
                        
                        article_html = self.get_page(article_url)
                        if article_html:
                            article_soup = self.parse_html(article_html)
                            article_content = self.extract_content_from_page(article_soup, article_url)
                            if article_content:
                                articles.extend(article_content)
                                self.logger.info(f"✅ Individual article: {len(article_content)} articles")
                        
                        self.scraped_urls.add(article_url)
                        self.rate_limit()
                        
                    except Exception as e:
                        self.logger.debug(f"Error processing article {article_url}: {str(e)}")
                        continue
                
            except Exception as e:
                self.logger.error(f"❌ Error processing URL {news_url}: {str(e)}")
                continue
        
        return articles
    
    def find_more_pages(self, soup, base_url):
        """Find additional pages (pagination, categories, archives)"""
        additional_pages = []
        
        # Method 1: Look for pagination links
        pagination_selectors = [
            '.pagination a', '.pager a', '.page-numbers a',
            'a[href*="page"]', 'a[href*="Page"]', 
            'a[rel="next"]', '.next a', '.more a'
        ]
        
        for selector in pagination_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href and len(additional_pages) < 10:  # Limit to 10 pages
                        full_url = urljoin(base_url, href)
                        if full_url not in additional_pages:
                            additional_pages.append(full_url)
            except:
                continue
        
        # Method 2: Look for category/section links
        category_keywords = ['agriculture', 'farming', 'crop', 'news', 'agri', 'rural']
        category_selectors = [
            '.menu a', '.nav a', '.category a', '.section a',
            'a[href*="category"]', 'a[href*="section"]', 'a[href*="news"]'
        ]
        
        for selector in category_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    link_text = link.get_text().strip().lower()
                    
                    # Check if link text suggests agriculture content
                    if any(keyword in (href + " " + link_text).lower() for keyword in category_keywords):
                        if href and len(additional_pages) < 15:
                            full_url = urljoin(base_url, href)
                            if full_url not in additional_pages:
                                additional_pages.append(full_url)
            except:
                continue
        
        # Method 3: Look for archive/date-based links
        archive_selectors = [
            'a[href*="2025"]', 'a[href*="2024"]', 
            'a[href*="archive"]', 'a[href*="recent"]'
        ]
        
        for selector in archive_selectors:
            try:
                links = soup.select(selector)
                for link in links[:5]:  # Only first 5 archive links
                    href = link.get('href')
                    if href and len(additional_pages) < 20:
                        full_url = urljoin(base_url, href)
                        if full_url not in additional_pages:
                            additional_pages.append(full_url)
            except:
                continue
        
        return additional_pages
    
    def find_individual_articles(self, soup, base_url):
        """Find links to individual articles"""
        article_links = []
        
        # Comprehensive selectors for article links
        article_selectors = [
            # Title-based selectors
            '.article-title a', '.news-title a', '.post-title a',
            '.story-title a', '.headline a', '.entry-title a',
            'h1 a', 'h2 a', 'h3 a',
            
            # Container-based selectors
            '.article a', '.news-item a', '.post a', '.story a',
            '.content-item a', '.news-content a',
            
            # List-based selectors
            'li a', 'ul a', '.list a', '.listing a',
            
            # Generic link selectors with filters
            'a[href*="article"]', 'a[href*="news"]', 'a[href*="post"]'
        ]
        
        for selector in article_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    link_text = link.get_text().strip()
                    
                    if not href or len(link_text) < 10:
                        continue
                    
                    # Check if it looks like an article link
                    if self.is_article_link(href, link_text):
                        full_url = urljoin(base_url, href)
                        if full_url not in article_links and len(article_links) < 25:
                            article_links.append(full_url)
            except:
                continue
        
        return article_links
    
    def is_article_link(self, href, link_text):
        """Check if a link appears to be an article"""
        # Skip obvious non-article links
        skip_patterns = [
            'javascript:', 'mailto:', 'tel:', '#',
            '/login', '/register', '/contact', '/about',
            'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'linkedin.com', 'whatsapp.com'
        ]
        
        for pattern in skip_patterns:
            if pattern in href.lower():
                return False
        
        # Skip short or generic link texts
        if len(link_text) < 15 or len(link_text) > 150:
            return False
        
        generic_texts = [
            'home', 'about', 'contact', 'login', 'register',
            'more', 'read more', 'click here', 'next', 'previous',
            'share', 'like', 'follow', 'subscribe', 'privacy',
            'terms', 'policy', 'disclaimer'
        ]
        
        if link_text.lower().strip() in generic_texts:
            return False
        
        # Prefer links with agriculture keywords
        agriculture_keywords = [
            'agriculture', 'farming', 'crop', 'farmer', 'cultivation',
            'harvest', 'plant', 'grow', 'coconut', 'rice', 'rubber',
            'kerala', 'weather', 'rain', 'price', 'market', 'scheme',
            'കൃഷി', 'കർഷക', 'നെല്ല്', 'തേങ്ങ', 'റബ്ബർ', 'കേരളം'
        ]
        
        combined_text = (href + " " + link_text).lower()
        has_agriculture = any(keyword in combined_text for keyword in agriculture_keywords)
        
        # Also accept links that look like news titles
        looks_like_news = (
            len(link_text.split()) >= 4 and  # At least 4 words
            any(char.isalpha() for char in link_text) and  # Contains letters
            not link_text.isupper()  # Not all caps (likely menu item)
        )
        
        return has_agriculture or looks_like_news
    
    def extract_content_from_page(self, soup, url):
        """Extract multiple articles from a single page"""
        articles = []
        
        # Method 1: Look for multiple article containers on the page
        article_containers = self.find_article_containers(soup)
        
        if article_containers:
            self.logger.info(f"📦 Found {len(article_containers)} article containers")
            for container in article_containers:
                try:
                    article_data = self.extract_from_container(container, url)
                    if article_data:
                        articles.append(self.create_article_dict(article_data, url))
                except:
                    continue
        
        # Method 2: Try to extract single article from entire page
        if not articles:
            single_article = self.extract_single_article(soup, url)
            if single_article:
                articles.append(self.create_article_dict(single_article, url))
        
        return articles
    
    def find_article_containers(self, soup):
        """Find individual article containers on listing pages"""
        containers = []
        
        # Common patterns for article containers
        container_selectors = [
            '.article', '.news-item', '.post', '.story',
            '.content-item', '.news-article', '.article-preview',
            '.entry', '.post-preview', '.news-summary'
        ]
        
        for selector in container_selectors:
            try:
                found_containers = soup.select(selector)
                for container in found_containers:
                    # Check if container has meaningful content
                    text_content = container.get_text().strip()
                    if len(text_content) > 100:  # Must have substantial content
                        containers.append(container)
            except:
                continue
        
        # If no containers found, try generic div/section patterns
        if not containers:
            generic_selectors = [
                'div[class*="article"]', 'div[class*="news"]', 'div[class*="post"]',
                'section[class*="article"]', 'section[class*="news"]'
            ]
            
            for selector in generic_selectors:
                try:
                    found_containers = soup.select(selector)
                    for container in found_containers[:5]:  # Limit to avoid noise
                        text_content = container.get_text().strip()
                        if len(text_content) > 150:
                            containers.append(container)
                except:
                    continue
        
        return containers[:10]  # Limit to 10 containers per page
    
    def extract_from_container(self, container, url):
        """Extract article data from a container"""
        # Get title
        title = "Agriculture News"
        title_selectors = ['h1', 'h2', 'h3', '.title', '.headline', '.article-title']
        
        for selector in title_selectors:
            try:
                title_elem = container.select_one(selector)
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    if len(title) > 10:
                        break
            except:
                continue
        
        # Get content
        content = self.clean_text(container.get_text())
        
        # Validate content
        is_good, reason = self.is_meaningful_content(title, content)
        if is_good:
            return {'title': title, 'content': content}
        else:
            self.logger.debug(f"Container content rejected: {reason}")
            return None
    
    def extract_single_article(self, soup, url):
        """Extract single article from page using existing methods"""
        # Use the existing content extraction logic from base_scraper
        return self.extract_content(soup, url)
    
    def create_article_dict(self, content_data, url):
        """Create standardized article dictionary"""
        return {
            'url': url,
            'source': self.source_config['name'],
            'category': self.source_config['category'],
            'language': self.source_config['language'],
            'scraped_at': datetime.now().isoformat(),
            'title': content_data['title'],
            'content': content_data['content'],
            'date': '',
            'author': '',
            'images': [],
            'keywords': self.extract_keywords(content_data['title'] + " " + content_data['content'])
        }

def scrape_comprehensive_kerala_agriculture():
    """Main function with ENHANCED DEEP SCRAPING"""
    print("🌾 ENHANCED KERALA AGRICULTURE NEWS SCRAPER")
    print("🔍 DEEP SCRAPING - Goes beyond first page")
    print("🎯 MULTI-PAGE EXTRACTION - Finds more articles")
    print("📍 FOCUS: Agriculture practices, crops, weather for Kerala")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Total Sources: {len(ALL_SOURCES)}")
    print(f"📊 Source Categories:")
    
    # Show source categories
    categories = {}
    for source_config in ALL_SOURCES.values():
        cat = source_config['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"   📂 {cat}: {count} sources")
    
    print()
    
    all_articles = []
    successful_sources = 0
    total_content_length = 0
    
    for i, (source_name, source_config) in enumerate(ALL_SOURCES.items(), 1):
        print(f"\n📊 Progress: {i}/{len(ALL_SOURCES)}")
        print(f"📰 {source_config['name']}")
        print(f"🔗 Category: {source_config['category']} | Language: {source_config['language']}")
        print(f"🌐 URLs to deep scrape: {len(source_config['news_urls'])}")
        
        try:
            scraper = EnhancedKeralaAgriScraper(source_config)
            articles = scraper.run()
            
            if articles:
                all_articles.extend(articles)
                successful_sources += 1
                
                # Calculate content statistics
                source_content_length = sum(len(article.get('content', '')) for article in articles)
                total_content_length += source_content_length
                avg_content_length = source_content_length / len(articles)
                
                print(f"✅ DEEP SCRAPING SUCCESS: {len(articles)} Kerala agriculture articles")
                print(f"📊 Average content length: {avg_content_length:.0f} characters")
                print(f"🔍 Deep scraping effectiveness: {len([a for a in articles if 'individual' in a.get('url', '')])}/{len(articles)} from deep links")
                
                # Save individual source file
                try:
                    file_manager = FileManager()
                    source_filename = file_manager.save_articles_to_text(articles, f"deep_kerala_agri_{source_name}")
                    print(f"💾 Saved to: {source_filename}")
                except Exception as e:
                    print(f"⚠️  Could not save individual file: {e}")
                
                # Show sample content with more detail
                print(f"🌾 Sample deep-scraped articles:")
                for j, article in enumerate(articles[:3], 1):
                    title = article.get('title', 'No title')
                    content_length = len(article.get('content', ''))
                    keywords = ', '.join(article.get('keywords', [])[:4])
                    source_url = article.get('url', '')
                    print(f"   {j}. {title[:60]}...")
                    print(f"      📊 {content_length} chars | 🔑 {keywords}")
                    print(f"      🔗 {source_url[:80]}...")
            else:
                print(f"⚠️  No Kerala agriculture content found through deep scraping")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Respectful delay between sources (longer for deep scraping)
        print("⏳ Waiting before next source (deep scraping requires patience)...")
        time.sleep(4)
    
    # Enhanced final results
    if all_articles:
        print(f"\n🎉 DEEP SCRAPING COMPLETE!")
        print("="*65)
        print(f"✅ Successful sources: {successful_sources}/{len(ALL_SOURCES)}")
        print(f"🌾 Total articles found: {len(all_articles)}")
        print(f"📊 Total content: {total_content_length:,} characters")
        print(f"📊 Average per article: {total_content_length / len(all_articles):.0f} characters")
        
        # Enhanced analytics
        unique_urls = len(set(article.get('url', '') for article in all_articles))
        print(f"🔗 Unique URLs scraped: {unique_urls}")
        print(f"🔍 Deep scraping efficiency: {len(all_articles) / unique_urls:.1f} articles per URL")
        
        # Category and language breakdown
        category_stats = {}
        language_stats = {}
        all_keywords = {}
        
        for article in all_articles:
            cat = article.get('category', 'unknown')
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            lang = article.get('language', 'unknown')
            language_stats[lang] = language_stats.get(lang, 0) + 1
            
            for keyword in article.get('keywords', [])[:5]:
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1
        
        print(f"\n📈 Deep Scraping Results:")
        print(f"📂 By Category:")
        for cat, count in sorted(category_stats.items()):
            percentage = (count / len(all_articles)) * 100
            print(f"   {cat}: {count} articles ({percentage:.1f}%)")
        
        print(f"\n🌐 By Language:")
        for lang, count in sorted(language_stats.items()):
            percentage = (count / len(all_articles)) * 100
            print(f"   {lang}: {count} articles ({percentage:.1f}%)")
        
        print(f"\n🔑 Top Agriculture Keywords:")
        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:12]
        for keyword, count in top_keywords:
            print(f"   🌾 {keyword}: {count} mentions")
        
        # Save with enhanced file naming
        try:
            file_manager = FileManager()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            consolidated_filename = file_manager.save_consolidated_text(all_articles, f"deep_scraped_kerala_agri_{timestamp}")
            print(f"\n📁 DEEP SCRAPED CONTENT SAVED:")
            print(f"📄 {consolidated_filename}")
            print(f"🚀 Ready for your Kerala farmer advisory app!")
            
        except Exception as e:
            print(f"⚠️  Could not save consolidated file: {e}")
        
        return all_articles
    
    else:
        print("❌ Deep scraping found no Kerala agriculture content")
        print("💡 Try checking internet connection or source accessibility")
        return []

if __name__ == "__main__":
    scrape_comprehensive_kerala_agriculture()
