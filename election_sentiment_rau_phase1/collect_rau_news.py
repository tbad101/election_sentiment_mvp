import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sentiment import analyze_sentiment
from database_rau import init_db, save_posts
from rau_config import NEWS_QUERIES
from rau_tagging import is_rau_related, build_row

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def collect_rau_news():
    init_db()

    if not NEWS_API_KEY or "PASTE" in NEWS_API_KEY:
        raise ValueError("Please add your NEWS_API_KEY in .env")

    rows = []

    for query in NEWS_QUERIES:
        print(f"Fetching Rau news for: {query}")

        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50,
            "apiKey": NEWS_API_KEY
        }

        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=30)
        except Exception as e:
            print(f"Request failed: {e}")
            continue

        if response.status_code != 200:
            print("News API error:", response.status_code, response.text)
            continue

        for article in response.json().get("articles", []):
            title = article.get("title") or ""
            description = article.get("description") or ""
            source_name = article.get("source", {}).get("name", "News")
            text = f"{title} {description}".strip()

            if not text:
                continue

            # Since query itself is Rau-specific, allow query to assist tagging
            if not is_rau_related(text + " " + query):
                continue

            sentiment, score = analyze_sentiment(text)

            rows.append(build_row(
                platform="News",
                source_name=source_name,
                text=text,
                keyword=query,
                created_at=article.get("publishedAt", ""),
                sentiment=sentiment,
                score=score,
                source_url=article.get("url", "")
            ))

    df = pd.DataFrame(rows)
    save_posts(df)
    print(f"Saved {len(df)} Rau news records")

if __name__ == "__main__":
    collect_rau_news()
