# Data Collection Report: News Headline Dataset

## Data Source
The data for this dataset was programmatically sourced from **BBC News** utilizing their public RSS (Really Simple Syndication) feeds. The specific feed endpoints included Technology, Business, Sports, and Politics.

## Collection Method
The collection was performed via **Web Scraping** using a custom automated Python pipeline. The script utilized the `requests` library to manage HTTP protocol handshakes and fetch live feed data. It then passed the raw XML payloads into `BeautifulSoup` to isolate, clean, and map specific XML tags (`<title>`, `<pubDate>`) into a flat, tabular layout. Finally, the clean rows were exported directly to a standardized CSV format.

## Challenges & Solutions
1. **API Limitations & Layout Fragility:** Standard search query APIs (like CNBC) proved volatile and frequently returned empty results due to parameter formatting restrictions. Scraping raw website HTML was also avoided due to layout fragility.
   * *Solution:* Shifted to server-side public RSS feeds which provide reliable, static XML trees.
2. **Volatile Feed Depths:** Live news channels naturally fluctuate in depth based on daily publishing cycles. On quiet days, some individual categories fell short of the traditional 50-item mark.
   * *Solution:* Increased the program's loop thresholds to capture up to 75 records per channel, allowing the deeper channels (Sports and Politics) to pick up extra rows to automatically offset the shorter channels and comfortably clear the 200+ total record requirement.
3. **Data Quality & Formatting Noise:** The raw time fields (`pubDate`) contained irregular padding, days of the week text, and regional timezone metadata.
   * *Solution:* Standardized the text arrays dynamically through Python's `datetime` parser to normalize all timestamps into clean `YYYY-MM-DD` strings.

## Dataset Size
A total of **over 200 unique news records** spread across 4 distinct categories were successfully harvested, filtered against duplication, and saved into the final dataset.