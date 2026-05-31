import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from sentiment import analyze_sentiment
from database import init_db, save_posts

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "PASTE_YOUR_YOUTUBE_API_KEY_HERE":
        raise ValueError("Please add your YOUTUBE_API_KEY in the .env file")
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_videos(youtube, keyword, max_results=5):
    request = youtube.search().list(
        q=keyword,
        part="id,snippet",
        type="video",
        maxResults=max_results,
        order="relevance"
    )
    response = request.execute()

    video_ids = []

    for item in response.get("items", []):
        video_ids.append(item["id"]["videoId"])

    return video_ids

def get_comments(youtube, video_id, keyword, max_results=50):
    rows = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )

        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            text = comment.get("textDisplay", "")
            created_at = comment.get("publishedAt", "")

            if not text.strip():
                continue

            sentiment, score = analyze_sentiment(text)

            rows.append({
                "platform": "YouTube",
                "text": text,
                "keyword": keyword,
                "created_at": created_at,
                "sentiment": sentiment,
                "sentiment_score": score,
                "source_url": f"https://www.youtube.com/watch?v={video_id}"
            })

    except Exception as e:
        print(f"Could not fetch comments for video {video_id}: {e}")

    return rows

def collect_youtube_data():
    init_db()
    youtube = get_youtube_client()

    keywords = [
        "BJP election",
        "Congress election",
        "Narendra Modi election",
        "Rahul Gandhi election",
        "India election unemployment",
        "India election inflation",
        "Lok Sabha election",
        "assembly election India"
    ]

    all_rows = []

    for keyword in keywords:
        print(f"Searching YouTube for: {keyword}")
        video_ids = search_videos(youtube, keyword, max_results=5)

        for video_id in video_ids:
            print(f"Fetching comments from: {video_id}")
            rows = get_comments(youtube, video_id, keyword, max_results=50)
            all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    save_posts(df)

    print(f"Saved {len(df)} YouTube comments")

if __name__ == "__main__":
    collect_youtube_data()
