"""
Agriculture Scraper with Testbook Schemes
- Economic Times Agriculture News
- Times of India Agriculture News  
- Testbook Agriculture Schemes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.sources import ALL_SOURCES
from scrapers.base_scraper import BaseScraper
from utils.file_manager import FileManager
from datetime import datetime
import time

class TestbookAgricultureScraper(BaseScraper):
    """Agriculture scraper with Testbook schemes"""
    
    def scrape_articles(self):
        """Scrape using site-specific methods"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"🔍 Processing: {news_url}")
                
                html = self.get_page(news_url)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                
                # Extract using site-specific methods
                extracted_content = self.extract_synopsis_articles(soup, news_url)
                
                for content_data in extracted_content:
                    article = {
                        'url': news_url,
                        'source': self.source_config['name'],
                        'category': self.source_config['category'],
                        'language': self.source_config['language'],
                        'scraped_at': datetime.now().isoformat(),
                        'title': content_data['title'],
                        'content': content_data['content'],
                        'keywords': self.extract_keywords(content_data['title'] + " " + content_data['content'])
                    }
                    articles.append(article)
                
                self.rate_limit()
                
            except Exception as e:
                self.logger.error(f"Error processing {news_url}: {str(e)}")
                continue
        
        return articles

def main():
    """Main function with Testbook schemes"""
    print("📚 TESTBOOK AGRICULTURE SCRAPER")
    print("📰 Economic Times + Times of India + Testbook Schemes")
    print("🎯 Comprehensive Government Scheme Information")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_articles = []
    successful_sources = 0
    
    for source_name, source_config in ALL_SOURCES.items():
        print(f"\n📊 Processing: {source_config['name']}")
        print(f"🔗 URL: {source_config['news_urls'][0]}")
        
        if 'testbook' in source_name.lower():
            print("📚 TESTBOOK SCHEME EXTRACTION:")
            print("   📋 PM-KISAN, PMFBY, PMKSY, eNAM, etc.")
            print("   📄 Detailed scheme descriptions and benefits")
            print("   🎯 Government policy information")
        elif 'economic' in source_name.lower():
            print("📈 ECONOMIC TIMES NEWS")
        elif 'times' in source_name.lower():
            print("📰 TIMES OF INDIA NEWS")
        
        try:
            scraper = TestbookAgricultureScraper(source_config)
            articles = scraper.run()
            
            if articles:
                all_articles.extend(articles)
                successful_sources += 1
                
                total_chars = sum(len(a.get('content', '')) for a in articles)
                avg_chars = total_chars // len(articles)
                
                print(f"✅ SUCCESS: {len(articles)} items extracted")
                print(f"📊 Total content: {total_chars:,} characters")
                print(f"📊 Average per item: {avg_chars} characters")
                
                # Save individual file
                file_manager = FileManager()
                filename = file_manager.save_articles_to_text(articles, source_name)
                print(f"💾 Saved: {filename}")
                
                # Show samples
                print(f"📋 Sample content:")
                for i, article in enumerate(articles[:3], 1):
                    title = article.get('title', '')[:70]
                    content_len = len(article.get('content', ''))
                    keywords = ', '.join(article.get('keywords', [])[:4])
                    
                    print(f"   {i}. {title}...")
                    print(f"      📊 {content_len} chars | 🔑 {keywords}")
                    
                    # For Testbook, show scheme preview
                    if 'testbook' in source_name.lower():
                        content_preview = article.get('content', '')[:150].replace('\n', ' ')
                        print(f"      📄 Preview: {content_preview}...")
                print()
            else:
                print("⚠️  No content extracted")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print("🔍 Continuing to next source...")
        
        time.sleep(2)
    
    # Final results
    if all_articles:
        print(f"\n🎉 TESTBOOK AGRICULTURE SCRAPING COMPLETE!")
        print(f"✅ Successful sources: {successful_sources}/{len(ALL_SOURCES)}")
        print(f"📊 Total items: {len(all_articles)}")
        
        # Content analysis
        scheme_count = len([a for a in all_articles if a.get('category') == 'government_schemes'])
        news_count = len(all_articles) - scheme_count
        
        print(f"\n📊 Content Mix:")
        print(f"   📰 News Articles: {news_count}")
        print(f"   📋 Government Schemes: {scheme_count}")
        
        # Top keywords
        all_keywords = {}
        for article in all_articles:
            for keyword in article.get('keywords', []):
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1
        
        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:8]
        print(f"\n🔑 Top Keywords:")
        for keyword, count in top_keywords:
            print(f"   🌾 {keyword}: {count} mentions")
        
        # Save consolidated
        file_manager = FileManager()
        consolidated_file = file_manager.save_consolidated_text(all_articles)
        print(f"\n📁 CONSOLIDATED FILE: {consolidated_file}")
        print(f"🚀 Complete agriculture data ready!")
        
        return all_articles
    else:
        print("❌ No content found")
        return []

if __name__ == "__main__":
    main()
