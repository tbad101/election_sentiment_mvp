import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sentiment import analyze_sentiment
from database import init_db, save_posts

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def collect_news_data():
    init_db()

    if not NEWS_API_KEY or NEWS_API_KEY == "PASTE_YOUR_NEWS_API_KEY_HERE":
        raise ValueError("Please add your NEWS_API_KEY in the .env file")

    keywords = [
        "BJP election",
        "Congress election",
        "Narendra Modi",
        "Rahul Gandhi",
        "India election",
        "unemployment India election",
        "inflation India election"
    ]

    rows = []

    for keyword in keywords:
        print(f"Fetching news for: {keyword}")

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": keyword,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            print("News API error:", response.status_code, response.text)
            continue

        articles = response.json().get("articles", [])

        for article in articles:
            title = article.get("title") or ""
            description = article.get("description") or ""
            text = title + " " + description

            if not text.strip():
                continue

            sentiment, score = analyze_sentiment(text)

            rows.append({
                "platform": "News",
                "text": text,
                "keyword": keyword,
                "created_at": article.get("publishedAt", ""),
                "sentiment": sentiment,
                "sentiment_score": score,
                "source_url": article.get("url", "")
            })

    df = pd.DataFrame(rows)
    save_posts(df)

    print(f"Saved {len(df)} news records")

if __name__ == "__main__":
    collect_news_data()
