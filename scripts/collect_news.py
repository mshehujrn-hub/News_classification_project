import os
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_category_news(url, category_name, source_name="BBC", target_count=75):
    print(f"Fetching headlines for category: '{category_name}'...")
    headlines_list = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed to fetch {category_name}. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        for item in items:
            if len(headlines_list) >= target_count:
                break
                
            title_tag = item.find('title')
            headline = title_tag.text.strip() if title_tag else ""
            
            # Normalize date formatting
            date_string = datetime.now().strftime("%Y-%m-%d")
            pub_date_tag = item.find('pubDate')
            
            if pub_date_tag:
                try:
                    parsed_date = datetime.strptime(pub_date_tag.text[:16].strip(), "%a, %d %b %Y")
                    date_string = parsed_date.strftime("%Y-%m-%d")
                except Exception:
                    pass 
            
            # Ensure uniqueness
            if headline and headline not in [h['headline'] for h in headlines_list]:
                headlines_list.append({
                    "headline": headline,
                    "category": category_name,
                    "source": source_name,
                    "date": date_string
                })
                
        print(f"Successfully collected {len(headlines_list)} items for {category_name}.")
        return headlines_list

    except Exception as e:
        print(f"An error occurred while fetching {category_name}: {e}")
        return []

def main():
    # Back strictly to the 4 required categories
    categories_urls = {
        "Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "Sports": "https://feeds.bbci.co.uk/sport/rss.xml",
        "Politics": "https://feeds.bbci.co.uk/news/politics/rss.xml"
    }
    
    all_data = []
    
    for category, url in categories_urls.items():
        # Set target to 75 to hit 200+ total rows using only these 4 categories
        category_data = fetch_category_news(url, category, target_count=75)
        all_data.extend(category_data)
    
    csv_path = os.path.join('..', 'data', 'news_dataset.csv')
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    fields = ["headline", "category", "source", "date"]
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_data)
        
    print(f"\nSuccess! Total records collected: {len(all_data)}")

if __name__ == "__main__":
    main()