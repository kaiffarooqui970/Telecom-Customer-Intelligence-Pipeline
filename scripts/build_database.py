import pandas as pd
import sqlite3
import json
import os
from textblob import TextBlob

# Define file paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JSON_FILE = os.path.join(BASE_DIR, "data", "scraped_reviews.json")
DB_FILE = os.path.join(BASE_DIR, "data", "churn_analysis.db")

def calculate_sentiment(text):
    """
    Returns a sentiment category based on TextBlob polarity.
    Polarity ranges from -1.0 (very negative) to 1.0 (very positive).
    """
    if not text:
        return "Neutral"
    
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.1:
        return "Negative"
    elif polarity > 0.1:
        return "Positive"
    else:
        return "Neutral"

def build_database():
    print("⚙️ Starting Data Transformation Pipeline...")

    # 1. EXTRACT: Load the JSON data
    if not os.path.exists(JSON_FILE):
        print(f"❌ Could not find {JSON_FILE}. Run the scraper first!")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        reviews_data = json.load(f)
    
    df_reviews = pd.DataFrame(reviews_data)
    print(f"✅ Loaded {len(df_reviews)} reviews into Pandas DataFrame.")

    # 2. TRANSFORM: Add Sentiment Analysis
    print("🧠 Running NLP Sentiment Analysis on review text...")
    df_reviews['sentiment_category'] = df_reviews['review_text'].apply(calculate_sentiment)
    
    # Clean up dates and format them for SQL
    df_reviews['date'] = pd.to_datetime(df_reviews['date'], errors='coerce').dt.date

    # 3. LOAD: Push to SQLite Database
    print(f"💾 Creating SQLite Database at {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    
    # Save the dataframe as a SQL table
    df_reviews.to_sql("customer_reviews", conn, if_exists="replace", index=False)
    
    # Run a quick sanity check query
    cursor = conn.cursor()
    cursor.execute("SELECT sentiment_category, COUNT(*) FROM customer_reviews GROUP BY sentiment_category")
    results = cursor.fetchall()
    
    print("\n📊 Sentiment Breakdown in Database:")
    for row in results:
        print(f"  - {row[0]}: {row[1]} reviews")

    conn.close()
    print("\n🎉 Pipeline complete! Data is ready for analysis.")

if __name__ == "__main__":
    build_database()