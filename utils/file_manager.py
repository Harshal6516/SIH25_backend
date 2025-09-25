"""
File Manager for Kerala Agriculture News Scraper
SIMPLE FORMAT: Only Title, Content, and Keywords
AUTO-DELETE: Removes daily files after consolidation
"""
import os
import json
import glob
from datetime import datetime

class FileManager:
    """Manages file operations for scraped agriculture articles"""
    
    def __init__(self):
        self.setup_directories()
        self.daily_files_created = []  # Track daily files for deletion
        
    def setup_directories(self):
        """Create necessary output directories"""
        directories = [
            'output',
            'output/daily',
            'output/weekly',
            'output/monthly',
            'output/consolidated'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def save_articles_to_text(self, articles, source_name):
        """Save articles in simple format - ONLY title, content, keywords"""
        if not articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/daily/{source_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KERALA AGRICULTURE NEWS\n")
                f.write("=" * 50 + "\n")
                f.write(f"Source: {articles[0].get('source', 'Unknown')}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Articles: {len(articles)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, article in enumerate(articles, 1):
                    # Extract only title, content, keywords
                    title = article.get('title', 'No Title').strip()
                    content = article.get('content', 'No Content').strip()
                    keywords = article.get('keywords', [])
                    
                    # Format keywords as comma-separated string
                    keywords_str = ', '.join(keywords) if keywords else 'No keywords'
                    
                    # Write in simple format
                    f.write(f"ARTICLE {i}\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {keywords_str}\n")
                    f.write("\n" + "=" * 50 + "\n\n")
            
            # Track this file for later deletion
            self.daily_files_created.append(filename)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving articles: {str(e)}")
            return None
    
    def save_consolidated_text(self, all_articles, prefix="kerala_agriculture"):
        """Save consolidated articles in simple format and DELETE daily files"""
        if not all_articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/consolidated/{prefix}_consolidated_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KERALA AGRICULTURE NEWS - CONSOLIDATED\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Articles: {len(all_articles)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, article in enumerate(all_articles, 1):
                    title = article.get('title', 'No Title').strip()
                    content = article.get('content', 'No Content').strip()
                    keywords = article.get('keywords', [])
                    source = article.get('source', 'Unknown')
                    
                    keywords_str = ', '.join(keywords) if keywords else 'No keywords'
                    
                    f.write(f"ARTICLE {i}\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"SOURCE: {source}\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {keywords_str}\n")
                    f.write("\n" + "=" * 60 + "\n\n")
            
            # AUTO-DELETE daily files after successful consolidation
            self.cleanup_daily_files()
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving consolidated file: {str(e)}")
            return None
    
    def cleanup_daily_files(self):
        """Delete all daily files after consolidation"""
        deleted_count = 0
        failed_count = 0
        
        print(f"\n🗑️  CLEANING UP DAILY FILES...")
        
        # Method 1: Delete tracked files from this session
        for daily_file in self.daily_files_created:
            try:
                if os.path.exists(daily_file):
                    os.remove(daily_file)
                    deleted_count += 1
                    print(f"✅ Deleted: {os.path.basename(daily_file)}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed to delete {os.path.basename(daily_file)}: {str(e)}")
        
        # Method 2: Delete any remaining files in daily folder
        try:
            daily_pattern = "output/daily/*.txt"
            remaining_files = glob.glob(daily_pattern)
            
            for file_path in remaining_files:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"✅ Deleted remaining: {os.path.basename(file_path)}")
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Failed to delete remaining {os.path.basename(file_path)}: {str(e)}")
                    
        except Exception as e:
            print(f"⚠️  Error cleaning daily folder: {str(e)}")
        
        # Summary
        print(f"🗑️  CLEANUP COMPLETE:")
        print(f"   ✅ Deleted: {deleted_count} files")
        if failed_count > 0:
            print(f"   ❌ Failed: {failed_count} files")
        print(f"   📁 Daily folder cleaned")
        
        # Clear the tracking list
        self.daily_files_created.clear()
    
    def save_simple_summary(self, all_articles):
        """Save a simple summary of scraped articles"""
        if not all_articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/kerala_agriculture_summary_{timestamp}.txt"
        
        try:
            # Count by source
            source_counts = {}
            total_content_length = 0
            all_keywords = {}
            
            for article in all_articles:
                source = article.get('source', 'Unknown')
                source_counts[source] = source_counts.get(source, 0) + 1
                
                content_length = len(article.get('content', ''))
                total_content_length += content_length
                
                for keyword in article.get('keywords', []):
                    all_keywords[keyword] = all_keywords.get(keyword, 0) + 1
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KERALA AGRICULTURE NEWS SCRAPING SUMMARY\n")
                f.write("=" * 50 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Articles: {len(all_articles)}\n")
                f.write(f"Total Sources: {len(source_counts)}\n")
                f.write(f"Average Content Length: {total_content_length // len(all_articles)} characters\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("ARTICLES BY SOURCE:\n")
                f.write("-" * 30 + "\n")
                for source, count in sorted(source_counts.items()):
                    f.write(f"{source}: {count} articles\n")
                
                f.write("\nTOP KEYWORDS:\n")
                f.write("-" * 30 + "\n")
                top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:15]
                for keyword, count in top_keywords:
                    f.write(f"{keyword}: {count} times\n")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving summary: {str(e)}")
            return None
    
    def save_json_backup(self, all_articles):
        """Save JSON backup (optional, contains all fields)"""
        if not all_articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/backup_kerala_agriculture_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, indent=2, ensure_ascii=False)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving JSON backup: {str(e)}")
            return None
    
    def manual_cleanup_daily(self):
        """Manual method to clean daily files if needed"""
        try:
            daily_files = glob.glob("output/daily/*.txt")
            deleted = 0
            
            for file_path in daily_files:
                try:
                    os.remove(file_path)
                    deleted += 1
                except Exception as e:
                    print(f"❌ Error deleting {file_path}: {str(e)}")
            
            print(f"🗑️  Manual cleanup: Deleted {deleted} daily files")
            return deleted
            
        except Exception as e:
            print(f"❌ Manual cleanup failed: {str(e)}")
            return 0
