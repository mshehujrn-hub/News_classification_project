# Data Collection Report: News Headline Dataset

## Data Source
The data for this dataset was programmatically sourced from **BBC News** utilizing their public RSS (Really Simple Syndication) feeds. The specific feed endpoints included:
* **Technology**
* **Health**
* **Business**

## Collection Method
The collection was performed via an automated, **Object-Oriented Programming (OOP) Python pipeline**. 

The system was designed with structural modularity:
* **`NewsArticle` Class:** A dedicated object blueprint responsible for initializing, sanitizing (stripping whitespace), and formatting individual article metadata (including the headline, category, and source) into clean dictionary formats.
* **`DatasetManager` / Scraper Pipeline:** Utilized the `requests` library to fetch live XML feed payloads and `BeautifulSoup` to parse and isolate the `<title>` tags. The extracted data was programmatically structured into `NewsArticle` objects before being merged by the `DatasetManager` into a unified pool.
* **Data Export:** The final structured collection was converted into a Pandas DataFrame and exported cleanly to `news_dataset.csv` without auto-generated index columns.

## Challenges & Solutions
1. **API Limitations & Layout Fragility:** Standard search query APIs proved volatile and frequently returned empty results due to parameter formatting restrictions. Scraping raw website HTML was also avoided due to layout fragility.
   * *Solution:* Shifted to server-side public RSS feeds which provide reliable, static XML trees.
2. **Volatile Feed Depths:** Live news channels naturally fluctuate in depth based on daily publishing cycles. On quiet days, some individual categories fell short of the traditional 50-item mark.
   * *Solution:* Programmed the system to dynamically capture all available active items per channel, allowing deeper feeds to offset shorter ones and easily build a robust final dataset.
3. **Data Quality & Formatting Noise:** The raw text fields extracted from XML feeds contained inconsistent surrounding whitespace, escape characters, and formatting anomalies.
   * *Solution:* Utilized string sanitization methods inside the `NewsArticle` initialization logic to automatically strip and format strings upon object creation, guaranteeing a clean dataset.

## Dataset Size
A total of **126 unique news records** spread across 3 distinct categories were successfully harvested, filtered against duplication, and saved into the final dataset:

| Category | Record Count |
| :--- | :--- |
| **Technology** | 21 |
| **Health** | 52 |
| **Business** | 53 |
| **Total** | **126** |