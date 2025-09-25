"""
Enhanced Scraper - Gets ALL TOI Articles with Less Strict Filtering
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
    """Enhanced scraper to get ALL TOI articles"""
    
    def __init__(self, source_config):
        self.source_config = source_config
        self.session = requests.Session()
        self.setup_session()
        self.setup_logging()
        
    def setup_session(self):
        """Configure requests session"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
        self.session.timeout = 20
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_page(self, url):
        """Fetch webpage"""
        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_html(self, html_content):
        """Parse HTML"""
        return BeautifulSoup(html_content, 'html.parser')
    
    def clean_text(self, text):
        """Basic text cleaning"""
        if not text:
            return ""
        
        text = text.replace('*agriculture*', 'agriculture')
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def light_refine_content(self, text):
        """Light content refinement - only remove obvious junk"""
        if not text:
            return ""
        
        # Only remove the most obvious junk
        light_junk_patterns = [
            r'Advertisement',
            r'Must Watch',
            r'Subscribe now',
            r'Follow us on',
            r'Share this',
            r'Read more about',
            r'Also read:',
            r'Copyright.*?reserved',
            r'\(Reuters\)|\(PTI\)|\(ANI\)',
        ]
        
        for pattern in light_junk_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def is_meaningful_content(self, title, content):
        """Very lenient validation - accept more content"""
        if not title or not content:
            return False, "Empty content"
        
        # Much more lenient requirements
        if len(content) < 20:  # Very low threshold
            return False, f"Content too short ({len(content)} chars)"
        
        if len(title) < 8:  # Very low threshold
            return False, f"Title too short ({len(title)} chars)"
        
        # Accept almost everything
        return True, "Content accepted"
    
    def extract_synopsis_articles(self, soup, url):
        """Extract ALL articles with multiple aggressive methods"""
        articles = []
        
        self.logger.info(f"🔍 AGGRESSIVE extraction from: {url}")
        
        if 'timesofindia' in url.lower():
            self.logger.info("📰 Using ALL TOI extraction methods")
            
            # Use ALL methods for TOI
            methods = [
                self.extract_toi_complete_articles,
                self.extract_toi_by_paragraphs,
                self.extract_toi_by_sentences,
                self.extract_toi_by_text_blocks,
                self.extract_toi_by_patterns,
                self.extract_toi_raw_text
            ]
            
            for i, method in enumerate(methods, 1):
                try:
                    self.logger.info(f"📋 TOI Method {i}: {method.__name__}")
                    method_articles = method(soup, url)
                    
                    if method_articles:
                        # Add new articles (avoid duplicates by title)
                        existing_titles = {article['title'].lower() for article in articles}
                        new_articles = [a for a in method_articles if a['title'].lower() not in existing_titles]
                        articles.extend(new_articles)
                        self.logger.info(f"✅ Method {i} found {len(method_articles)} articles ({len(new_articles)} new)")
                    else:
                        self.logger.info(f"⚠️  Method {i} found no articles")
                        
                except Exception as e:
                    self.logger.debug(f"Method {i} failed: {str(e)}")
                    continue
            
        else:
            self.logger.info("📈 Using Economic Times extraction")
            articles = self.extract_et_complete_articles(soup, url)
        
        self.logger.info(f"🎯 TOTAL ARTICLES FOUND: {len(articles)}")
        return articles
    
    def extract_toi_complete_articles(self, soup, url):
        """Method 1: Extract from TOI structure"""
        articles = []
        
        full_text = soup.get_text(separator='\n')
        paragraphs = full_text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if len(para) < 50:
                continue
            
            clean_para = self.clean_text(para)
            sentences = clean_para.split('. ')
            
            if len(sentences) >= 2:
                title = sentences[0].strip()
                content = '. '.join(sentences[1:]).strip()
                
                if len(title) > 15 and len(content) > 30:
                    refined_title = self.light_refine_content(title)
                    refined_content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                    if is_good:
                        articles.append({'title': refined_title, 'content': refined_content})
        
        return articles
    
    def extract_toi_by_paragraphs(self, soup, url):
        """Method 2: Extract by splitting paragraphs differently"""
        articles = []
        
        full_text = soup.get_text(separator='\n')
        
        # Split by single newlines and group
        lines = [line.strip() for line in full_text.split('\n') if len(line.strip()) > 30]
        
        i = 0
        while i < len(lines) - 1:
            # Take current line as title, next few as content
            potential_title = self.clean_text(lines[i])
            
            # Collect next few lines as content
            content_lines = []
            j = i + 1
            while j < len(lines) and j < i + 4:  # Get next 1-3 lines
                content_lines.append(lines[j])
                j += 1
            
            potential_content = ' '.join(content_lines)
            potential_content = self.clean_text(potential_content)
            
            if len(potential_title) > 20 and len(potential_content) > 50:
                refined_title = self.light_refine_content(potential_title)
                refined_content = self.light_refine_content(potential_content)
                
                is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                if is_good:
                    articles.append({'title': refined_title, 'content': refined_content})
                    i = j  # Skip processed lines
                else:
                    i += 1
            else:
                i += 1
        
        return articles
    
    def extract_toi_by_sentences(self, soup, url):
        """Method 3: Extract by sentence grouping"""
        articles = []
        
        full_text = soup.get_text()
        sentences = full_text.split('. ')
        
        i = 0
        while i < len(sentences) - 2:
            # Group sentences: 1 as title, 2-4 as content
            title = self.clean_text(sentences[i])
            content_sentences = sentences[i+1:i+4]
            content = '. '.join(content_sentences)
            content = self.clean_text(content)
            
            if len(title) > 25 and len(content) > 60:
                refined_title = self.light_refine_content(title)
                refined_content = self.light_refine_content(content)
                
                is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                if is_good:
                    articles.append({'title': refined_title, 'content': refined_content})
                    i += 4  # Skip processed sentences
                else:
                    i += 1
            else:
                i += 1
        
        return articles
    
    def extract_toi_by_text_blocks(self, soup, url):
        """Method 4: Extract by text block analysis"""
        articles = []
        
        # Find all div, p, and span elements with substantial text
        text_elements = soup.find_all(['div', 'p', 'span', 'article', 'section'])
        
        for element in text_elements:
            text = self.clean_text(element.get_text())
            
            if 80 <= len(text) <= 800:  # Reasonable article length
                # Try to split into title and content
                lines = text.split('\n')
                if len(lines) >= 2:
                    title = lines[0].strip()
                    content = '\n'.join(lines[1:]).strip()
                else:
                    sentences = text.split('. ')
                    if len(sentences) >= 3:
                        title = sentences[0].strip()
                        content = '. '.join(sentences[1:]).strip()
                    else:
                        continue
                
                if len(title) > 15 and len(content) > 40:
                    refined_title = self.light_refine_content(title)
                    refined_content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                    if is_good:
                        articles.append({'title': refined_title, 'content': refined_content})
        
        return articles
    
    def extract_toi_by_patterns(self, soup, url):
        """Method 5: Extract using specific patterns from your attachment"""
        articles = []
        
        full_text = soup.get_text()
        
        # Patterns based on your TOI attachment
        specific_patterns = [
            r'([^.]*agriculture\s+scientists[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*Federation[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*NABARD[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*ICAR[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*minister[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*government[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*University[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
            r'([^.]*Bihar[^.]{20,}\.)\s*([^.]+\.(?:\s*[^.]+\.){1,4})',
        ]
        
        for pattern in specific_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                title, content = match
                title = self.light_refine_content(title)
                content = self.light_refine_content(content)
                
                if len(title) > 20 and len(content) > 30:
                    is_good, reason = self.is_meaningful_content(title, content)
                    if is_good:
                        articles.append({'title': title, 'content': content})
        
        return articles
    
    def extract_toi_raw_text(self, soup, url):
        """Method 6: Raw text extraction with aggressive splitting"""
        articles = []
        
        # Get raw text and try different splitting methods
        raw_text = soup.get_text()
        
        # Method A: Split by multiple newlines
        blocks = raw_text.split('\n\n\n')
        for block in blocks:
            block = self.clean_text(block)
            if 100 <= len(block) <= 1000:
                sentences = block.split('. ')
                if len(sentences) >= 3:
                    title = sentences[0]
                    content = '. '.join(sentences[1:])
                    
                    title = self.light_refine_content(title)
                    content = self.light_refine_content(content)
                    
                    if len(title) > 15 and len(content) > 50:
                        is_good, reason = self.is_meaningful_content(title, content)
                        if is_good:
                            articles.append({'title': title, 'content': content})
        
        # Method B: Split by periods and group aggressively
        all_sentences = raw_text.split('. ')
        
        i = 0
        while i < len(all_sentences) - 3:
            title_candidate = self.clean_text(all_sentences[i])
            content_candidate = '. '.join(all_sentences[i+1:i+5])
            content_candidate = self.clean_text(content_candidate)
            
            # Check if it looks like a valid article
            if (30 <= len(title_candidate) <= 200 and 
                len(content_candidate) > 100 and
                any(word in title_candidate.lower() for word in ['agriculture', 'farmer', 'crop', 'government', 'india', 'state', 'minister', 'university', 'council'])):
                
                title_candidate = self.light_refine_content(title_candidate)
                content_candidate = self.light_refine_content(content_candidate)
                
                is_good, reason = self.is_meaningful_content(title_candidate, content_candidate)
                if is_good:
                    articles.append({'title': title_candidate, 'content': content_candidate})
                    i += 5
                else:
                    i += 1
            else:
                i += 1
        
        return articles
    
    def extract_et_complete_articles(self, soup, url):
        """Extract complete articles from Economic Times"""
        articles = []
        
        containers = soup.select('.eachStory')
        
        for container in containers:
            try:
                title_elem = container.find(['h1', 'h2', 'h3']) or container.select_one('.story-headline, .headline, .title')
                title = "Economic Times News"
                
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                
                content = self.clean_text(container.get_text())
                if title in content:
                    content = content.replace(title, '').strip()
                
                title = self.light_refine_content(title)
                content = self.light_refine_content(content)
                
                is_good, reason = self.is_meaningful_content(title, content)
                if is_good:
                    articles.append({'title': title, 'content': content})
                
            except Exception as e:
                continue
        
        return articles
    
    def extract_keywords(self, text):
        """Extract keywords"""
        refined_text = self.light_refine_content(text)
        words = refined_text.lower().split()
        keywords = []
        
        for word in words:
            if len(word) > 4 and word.isalpha():
                keywords.append(word)
        
        return list(dict.fromkeys(keywords))[:8]
    
    def rate_limit(self):
        """Rate limiting"""
        time.sleep(1.5)
    
    @abstractmethod
    def scrape_articles(self):
        pass
    
    def run(self):
        """Run aggressive scraper"""
        self.logger.info(f"Starting AGGRESSIVE scraper for {self.source_config['name']}")
        articles = self.scrape_articles()
        self.logger.info(f"Found {len(articles)} articles with aggressive extraction")
        return articles
