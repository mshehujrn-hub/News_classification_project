import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. BONUS CHALLENGE: NewsArticle Class
class NewsArticle:
    def __init__(self, headline: str, category: str, source: str):
        self.headline = headline.strip()
        self.category = category.strip()
        self.source = source.strip()

    def to_dict(self) -> dict:
        return {
            "headline": self.headline,
            "category": self.category,
            "source": self.source,
        }

    def __repr__(self) -> str:
        return f"NewsArticle('{self.headline[:25]}...', '{self.category}', '{self.source}')"

# 2. STEP 1: NewsScraper Class
class NewsScraper:
    def __init__(self, url: str, category: str):
        self.url = url
        self.category = category
        self.headlines = []
        self.articles = []
        self.html_content = ""
        self.source = "BBC News"

    def fetch_page(self) -> bool:
        print(f"\n[Scraper] Accessing {self.category} feed: {self.url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                self.html_content = response.text
                return True
            else:
                print(f"[Error] Failed to fetch. Status Code: {response.status_code}")
                return False
        except Exception as e:
            print(f"[Error] Connection failed: {e}")
            return False

    def parse_headlines(self) -> list:
        if not self.html_content:
            return []
        self.headlines = []
        self.articles = []
        try:
            soup = BeautifulSoup(self.html_content, "xml")
            items = soup.find_all("item")
            for item in items:
                title_tag = item.find("title")
                if title_tag and title_tag.text:
                    headline_text = title_tag.text.strip()
                    self.headlines.append(headline_text)
                    
                    # Store NewsArticle objects inside your scraper (Bonus Challenge)
                    article = NewsArticle(
                        headline=headline_text,
                        category=self.category,
                        source=self.source
                    )
                    self.articles.append(article)
            print(f"[Scraper] Successfully extracted {len(self.articles)} headlines.")
        except Exception as e:
            print(f"[Error] Parse execution failed: {e}")
        return self.articles

    def display_summary(self):
        print(f"--- Preview of Scraped {self.category} Category ---")
        for idx, article in enumerate(self.articles[:3], 1):
            print(f"  {idx}. {article.headline}")
        print("-" * 50)

    def save_to_csv(self, filename: str = "temp_scraped_data.csv"):
        if not self.articles:
            return
        df = pd.DataFrame([art.to_dict() for art in self.articles])
        df.to_csv(filename, index=False, encoding="utf-8")

# 3. STEP 2: DatasetManager Class
class DatasetManager:
    def __init__(self):
        self.all_data = []
        self.df = None

    def add_records(self, data: list):
        added_count = 0
        for item in data:
            if isinstance(item, NewsArticle):
                self.all_data.append(item)
                added_count += 1
        print(f"[Manager] Merged {added_count} articles into master pool.")

    def create_dataframe(self) -> pd.DataFrame:
        if not self.all_data:
            self.df = pd.DataFrame(columns=["headline", "category", "source"])
            return self.df
        records = [article.to_dict() for article in self.all_data]
        self.df = pd.DataFrame(records)
        return self.df

    def export_dataset(self, filename: str = "news_dataset.csv"):
        if self.df is None or self.df.empty:
            self.create_dataframe()
        self.df.to_csv(filename, index=False, encoding="utf-8")
        print(f"\n[Manager] Final dataset exported cleanly to: '{filename}'")

# 4. STEP 3: Generation & Pipeline Execution
if __name__ == "__main__":
    print("=========================================")
    print("   Starting OOP News Scraping Pipeline   ")
    print("=========================================")

    manager = DatasetManager()

    feed_targets = [
        {"url": "http://feeds.bbci.co.uk/news/technology/rss.xml", "category": "Technology"},
        {"url": "http://feeds.bbci.co.uk/news/health/rss.xml", "category": "Health"},
        {"url": "http://feeds.bbci.co.uk/news/business/rss.xml", "category": "Business"}
    ]

    for target in feed_targets:
        scraper = NewsScraper(url=target["url"], category=target["category"])
        if scraper.fetch_page():
            articles = scraper.parse_headlines()
            scraper.display_summary()
            manager.add_records(articles)

    df_final = manager.create_dataframe()

    print("\n=========================================")
    print("         Final DataFrame Preview         ")
    print("=========================================")
    print(df_final.head(10))
    print(f"Total Rows Gathered: {len(df_final)}")
    print("=========================================")

    manager.export_dataset("news_dataset.csv")
    print("\nProcess completed successfully! Ready for submission.")