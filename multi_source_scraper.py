"""
Agriculture News Scraper - Economic Times + Times of India
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.sources import ALL_SOURCES
from scrapers.base_scraper import BaseScraper
from utils.file_manager import FileManager
from datetime import datetime
import time

class AgricultureNewsScraper(BaseScraper):
    """Agriculture News Scraper for ET and TOI"""
    
    def scrape_articles(self):
        """Scrape agriculture articles using site-specific methods"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"🔍 Processing: {news_url}")
                
                html = self.get_page(news_url)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                
                # Extract articles using site-specific methods
                extracted_articles = self.extract_synopsis_articles(soup, news_url)
                
                for article_data in extracted_articles:
                    article = {
                        'url': news_url,
                        'source': self.source_config['name'],
                        'category': self.source_config['category'],
                        'language': self.source_config['language'],
                        'scraped_at': datetime.now().isoformat(),
                        'title': article_data['title'],
                        'content': article_data['content'],
                        'keywords': self.extract_keywords(article_data['title'] + " " + article_data['content'])
                    }
                    articles.append(article)
                
                self.rate_limit()
                
            except Exception as e:
                self.logger.error(f"Error processing {news_url}: {str(e)}")
                continue
        
        return articles

def main():
    """Main function"""
    print("🌾 AGRICULTURE NEWS SCRAPER")
    print("📰 Economic Times + Times of India")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_articles = []
    
    for source_name, source_config in ALL_SOURCES.items():
        print(f"📰 Processing: {source_config['name']}")
        print(f"🔗 URL: {source_config['news_urls'][0]}")
        
        try:
            scraper = AgricultureNewsScraper(source_config)
            articles = scraper.run()
            
            if articles:
                all_articles.extend(articles)
                print(f"✅ SUCCESS: {len(articles)} articles extracted")
                
                # Show content quality
                avg_content_length = sum(len(a.get('content', '')) for a in articles) // len(articles)
                print(f"📊 Average content length: {avg_content_length} characters")
                
                # Save individual file
                file_manager = FileManager()
                filename = file_manager.save_articles_to_text(articles, source_name)
                print(f"💾 Saved: {filename}")
                
                # Show samples
                print(f"📰 Sample articles:")
                for i, article in enumerate(articles[:3], 1):
                    title = article.get('title', '')[:70]
                    content_len = len(article.get('content', ''))
                    keywords = ', '.join(article.get('keywords', [])[:3])
                    print(f"   {i}. {title}...")
                    print(f"      Length: {content_len} chars | Keywords: {keywords}")
                print()
            else:
                print("⚠️  No articles found")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("⏳ Moving to next source...")
        time.sleep(2)
    
    # Save consolidated file
    if all_articles:
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"✅ Total articles: {len(all_articles)}")
        
        # Quality summary
        total_content = sum(len(a.get('content', '')) for a in all_articles)
        avg_content = total_content // len(all_articles)
        print(f"📊 Average article length: {avg_content} characters")
        
        # Top keywords
        all_keywords = {}
        for article in all_articles:
            for keyword in article.get('keywords', []):
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1
        
        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n🔑 Top Keywords:")
        for keyword, count in top_keywords:
            print(f"   🌾 {keyword}: {count} articles")
        
        file_manager = FileManager()
        consolidated_file = file_manager.save_consolidated_text(all_articles)
        print(f"\n📁 Consolidated file: {consolidated_file}")
        print(f"🚀 Ready for your farmer advisory app!")
        
        return all_articles
    else:
        print("❌ No articles found")
        return []

if __name__ == "__main__":
    main()
