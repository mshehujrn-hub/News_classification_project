import pandas as pd

def build_dataset():
    # 1. Define your data matching the columns in the image
    news_data = {
        'headline': [
            'Apple launches new AI chip',
            'WHO releases health report',
            'Stock market rises today'
            # 💡 You can easily add more scraped headlines here!
        ],
        'category': [
            'Technology',
            'Health',
            'Business'
            # 💡 Keep the category order perfectly aligned with the headlines above
        ]
    }
    
    # 2. Convert into a structured data table (DataFrame)
    df = pd.DataFrame(news_data)
    
    # 3. Save it as a CSV file (index=False removes the messy automatic row numbers)
    output_file = 'news_dataset.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Dataset successfully created and saved as: {output_file}")
    print("\nPreview of your structured dataset:")
    print(df)

if __name__ == "__main__":
    build_dataset()