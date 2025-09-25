"""
COMPREHENSIVE Kerala Agriculture Multi-Source Scraper
Focus: 22+ reliable, paywall-free sources for Kerala agriculture content
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.sources import ALL_SOURCES
from scrapers.base_scraper import BaseScraper
from utils.file_manager import FileManager
from datetime import datetime
import time

class ComprehensiveKeralaAgriScraper(BaseScraper):
    """Comprehensive scraper for Kerala agriculture from 22+ reliable sources"""
    
    def scrape_articles(self):
        """Scrape Kerala agriculture articles with comprehensive approach"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"🌾 Processing URL: {news_url}")
                
                # Get main page
                html = self.get_page(news_url)
                if not html:
                    self.logger.warning(f"Could not fetch content from {news_url}")
                    continue
                
                soup = self.parse_html(html)
                
                # Method 1: Try to extract content from main page itself
                page_data = self.extract_simple_content(soup, news_url)
                if page_data:
                    article = {
                        'url': news_url,
                        'source': self.source_config['name'],
                        'category': self.source_config['category'],
                        'language': self.source_config['language'],
                        'scraped_at': datetime.now().isoformat(),
                        'title': page_data['title'],
                        'content': page_data['content'],
                        'date': '',
                        'author': '',
                        'images': [],
                        'keywords': self.extract_keywords(page_data['title'] + " " + page_data['content'])
                    }
                    articles.append(article)
                    self.logger.info(f"✅ Main page content: {page_data['title'][:70]}...")
                
                # Method 2: Find individual article URLs and scrape them
                article_urls = self.find_kerala_agriculture_urls(soup, self.source_config['base_url'])
                
                if article_urls:
                    self.logger.info(f"Found {len(article_urls)} potential article URLs")
                    
                    for i, article_url in enumerate(article_urls, 1):
                        try:
                            self.logger.info(f"Processing article {i}/{len(article_urls)}: {article_url}")
                            
                            article_html = self.get_page(article_url)
                            if article_html:
                                article_soup = self.parse_html(article_html)
                                article_data = self.extract_simple_content(article_soup, article_url)
                                
                                if article_data:
                                    article = {
                                        'url': article_url,
                                        'source': self.source_config['name'],
                                        'category': self.source_config['category'],
                                        'language': self.source_config['language'],
                                        'scraped_at': datetime.now().isoformat(),
                                        'title': article_data['title'],
                                        'content': article_data['content'],
                                        'date': '',
                                        'author': '',
                                        'images': [],
                                        'keywords': self.extract_keywords(article_data['title'] + " " + article_data['content'])
                                    }
                                    articles.append(article)
                                    self.logger.info(f"✅ Article content: {article_data['title'][:70]}...")
                                else:
                                    self.logger.debug(f"❌ Article filtered out: {article_url}")
                            else:
                                self.logger.warning(f"Could not fetch article: {article_url}")
                            
                            # Rate limiting between article requests
                            self.rate_limit()
                            
                        except Exception as e:
                            self.logger.error(f"❌ Error processing article {article_url}: {str(e)}")
                            continue
                else:
                    self.logger.info("No article URLs found on this page")
                
            except Exception as e:
                self.logger.error(f"❌ Error processing URL {news_url}: {str(e)}")
                continue
        
        return articles

def scrape_comprehensive_kerala_agriculture():
    """Main function to scrape comprehensive Kerala agriculture content"""
    print("🌾 COMPREHENSIVE KERALA AGRICULTURE NEWS SCRAPER")
    print("🎯 22+ RELIABLE SOURCES - NO PAYWALLS")
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
        print(f"🌐 URLs: {len(source_config['news_urls'])} URLs to process")
        
        try:
            scraper = ComprehensiveKeralaAgriScraper(source_config)
            articles = scraper.run()
            
            if articles:
                all_articles.extend(articles)
                successful_sources += 1
                
                # Calculate content statistics
                source_content_length = sum(len(article.get('content', '')) for article in articles)
                total_content_length += source_content_length
                avg_content_length = source_content_length / len(articles)
                
                print(f"✅ SUCCESS: {len(articles)} Kerala agriculture articles")
                print(f"📊 Average content length: {avg_content_length:.0f} characters")
                
                # Save individual source file
                try:
                    file_manager = FileManager()
                    source_filename = file_manager.save_articles_to_text(articles, f"kerala_agri_{source_name}")
                    print(f"💾 Saved to: {source_filename}")
                except Exception as e:
                    print(f"⚠️  Could not save individual file: {e}")
                
                # Show sample content
                print(f"🌾 Sample articles:")
                for j, article in enumerate(articles[:2], 1):
                    title = article.get('title', 'No title')
                    content_length = len(article.get('content', ''))
                    keywords = ', '.join(article.get('keywords', [])[:3])
                    print(f"   {j}. {title[:65]}...")
                    print(f"      Content: {content_length} chars | Keywords: {keywords}")
            else:
                print(f"⚠️  No Kerala agriculture content found")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
        
        # Respectful delay between sources
        print("⏳ Waiting before next source...")
        time.sleep(3)
    
    # Final results and consolidation
    if all_articles:
        print(f"\n🎉 COMPREHENSIVE KERALA AGRICULTURE SCRAPING COMPLETE!")
        print("="*65)
        print(f"✅ Successful sources: {successful_sources}/{len(ALL_SOURCES)}")
        print(f"🌾 Total Kerala agriculture articles: {len(all_articles)}")
        print(f"📊 Total content collected: {total_content_length:,} characters")
        print(f"📊 Average content per article: {total_content_length / len(all_articles):.0f} characters")
        
        # Category breakdown
        category_stats = {}
        language_stats = {}
        all_keywords = {}
        
        for article in all_articles:
            # Category stats
            cat = article.get('category', 'unknown')
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            # Language stats
            lang = article.get('language', 'unknown')
            language_stats[lang] = language_stats.get(lang, 0) + 1
            
            # Keyword stats
            for keyword in article.get('keywords', [])[:5]:
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1
        
        print(f"\n📈 Content Breakdown:")
        print(f"📂 By Category:")
        for cat, count in sorted(category_stats.items()):
            percentage = (count / len(all_articles)) * 100
            print(f"   {cat}: {count} articles ({percentage:.1f}%)")
        
        print(f"\n🌐 By Language:")
        for lang, count in sorted(language_stats.items()):
            percentage = (count / len(all_articles)) * 100
            print(f"   {lang}: {count} articles ({percentage:.1f}%)")
        
        print(f"\n🔑 Top Kerala Agriculture Keywords:")
        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        for keyword, count in top_keywords:
            print(f"   🌾 {keyword}: {count} occurrences")
        
        # Save consolidated file
        try:
            file_manager = FileManager()
            consolidated_filename = file_manager.save_consolidated_text(all_articles)
            print(f"\n📁 CONSOLIDATED FILE SAVED:")
            print(f"📄 {consolidated_filename}")
            print(f"📱 Perfect for your Kerala farmer advisory app!")
            
            # Create summary file
            summary_content = f"""
KERALA AGRICULTURE NEWS SCRAPING SUMMARY
========================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sources Processed: {len(ALL_SOURCES)}
Successful Sources: {successful_sources}
Total Articles: {len(all_articles)}
Total Content: {total_content_length:,} characters

CATEGORY BREAKDOWN:
{chr(10).join([f"- {cat}: {count} articles" for cat, count in sorted(category_stats.items())])}

LANGUAGE BREAKDOWN:
{chr(10).join([f"- {lang}: {count} articles" for lang, count in sorted(language_stats.items())])}

TOP KEYWORDS:
{chr(10).join([f"- {keyword}: {count} times" for keyword, count in top_keywords[:15]])}
"""
            
            with open('output/kerala_agriculture_summary.txt', 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"📊 Summary saved to: output/kerala_agriculture_summary.txt")
            
        except Exception as e:
            print(f"⚠️  Could not save consolidated file: {e}")
        
        return all_articles
    
    else:
        print("❌ No Kerala agriculture content found from any source")
        return []

if __name__ == "__main__":
    scrape_comprehensive_kerala_agriculture()
