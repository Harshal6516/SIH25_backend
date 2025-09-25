"""
File Manager for Agriculture Content
"""
import os
import json
from datetime import datetime

class FileManager:
    """File manager for agriculture articles"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """Create directories"""
        os.makedirs('output', exist_ok=True)
        os.makedirs('output/daily', exist_ok=True)
        os.makedirs('output/consolidated', exist_ok=True)
    
    def save_articles_to_text(self, articles, source_name):
        """Save articles to text file"""
        if not articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/daily/{source_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AGRICULTURE NEWS SCRAPER\n")
                f.write("=" * 50 + "\n")
                f.write(f"Source: {source_name}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Articles: {len(articles)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, article in enumerate(articles, 1):
                    title = article.get('title', 'No Title')
                    content = article.get('content', 'No Content')
                    keywords = article.get('keywords', [])
                    
                    f.write(f"ARTICLE {i}\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {', '.join(keywords)}\n")
                    f.write("\n" + "=" * 50 + "\n\n")
            
            return filename
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return None
    
    def save_consolidated_text(self, all_articles):
        """Save consolidated file"""
        if not all_articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/consolidated/agriculture_news_consolidated_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AGRICULTURE NEWS - CONSOLIDATED\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Articles: {len(all_articles)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, article in enumerate(all_articles, 1):
                    title = article.get('title', 'No Title')
                    content = article.get('content', 'No Content')
                    keywords = article.get('keywords', [])
                    source = article.get('source', 'Unknown')
                    
                    f.write(f"ARTICLE {i}\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"SOURCE: {source}\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {', '.join(keywords)}\n")
                    f.write("\n" + "=" * 60 + "\n\n")
            
            return filename
            
        except Exception as e:
            print(f"Error saving consolidated file: {str(e)}")
            return None
