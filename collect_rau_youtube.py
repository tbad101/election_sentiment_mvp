import os
import time
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from sentiment import analyze_sentiment
from database_rau import init_db, save_posts
from rau_config import MANUAL_YOUTUBE_CHANNELS, RAU_YOUTUBE_SEARCH_QUERIES
from rau_tagging import is_rau_related, build_row

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    if not YOUTUBE_API_KEY or "PASTE" in YOUTUBE_API_KEY:
        raise ValueError("Please add your YOUTUBE_API_KEY in .env")
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def resolve_channel_id(youtube, channel_name):
    try:
        response = youtube.search().list(
            q=channel_name,
            part="snippet",
            type="channel",
            maxResults=1
        ).execute()
        items = response.get("items", [])
        if not items:
            return None, None
        item = items[0]
        return item["snippet"]["channelId"], item["snippet"].get("channelTitle", channel_name)
    except Exception as e:
        print(f"Channel resolve error: {channel_name} | {e}")
        return None, None

def get_uploads_playlist(youtube, channel_id):
    try:
        response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()
        items = response.get("items", [])
        if not items:
            return None
        return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except Exception as e:
        print(f"Upload playlist error: {e}")
        return None

def get_latest_videos_from_channel(youtube, uploads_playlist_id, max_videos=20):
    videos = []
    try:
        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=max_videos
        ).execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            videos.append({
                "video_id": item.get("contentDetails", {}).get("videoId"),
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", "")
            })
    except Exception as e:
        print(f"Latest video error: {e}")

    return videos

def search_videos(youtube, query, max_videos=10):
    videos = []
    try:
        response = youtube.search().list(
            q=query,
            part="id,snippet",
            type="video",
            maxResults=max_videos,
            order="date"
        ).execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            videos.append({
                "video_id": item.get("id", {}).get("videoId"),
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", "")
            })
    except Exception as e:
        print(f"Video search error: {query} | {e}")

    return videos

def get_comments(youtube, video, keyword, max_comments=40):
    rows = []
    video_id = video["video_id"]
    source_name = video.get("channel_title", "YouTube")

    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText",
            order="relevance"
        ).execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            text = comment.get("textDisplay", "")
            created_at = comment.get("publishedAt", "")

            if not text.strip():
                continue

            # Keep a comment if comment itself or parent video context is Rau-linked
            context = text + " " + video.get("title", "") + " " + video.get("description", "") + " " + keyword
            if not is_rau_related(context):
                continue

            sentiment, score = analyze_sentiment(text)

            rows.append(build_row(
                platform="YouTube",
                source_name=source_name,
                text=text,
                keyword=keyword,
                created_at=created_at,
                sentiment=sentiment,
                score=score,
                source_url=f"https://www.youtube.com/watch?v={video_id}"
            ))

    except Exception as e:
        print(f"Could not fetch comments for video {video_id}: {e}")

    return rows

def collect_rau_youtube():
    init_db()
    youtube = get_youtube_client()
    all_rows = []
    seen_videos = set()

    print("1) Collecting via automatic Rau keyword video search")
    for query in RAU_YOUTUBE_SEARCH_QUERIES:
        print(f"Searching: {query}")
        videos = search_videos(youtube, query, max_videos=8)

        for video in videos:
            if not video["video_id"] or video["video_id"] in seen_videos:
                continue
            seen_videos.add(video["video_id"])

            context = video["title"] + " " + video["description"] + " " + query
            if not is_rau_related(context):
                continue

            print(f"Comments: {video['channel_title']} | {video['title'][:80]}")
            all_rows.extend(get_comments(youtube, video, query, max_comments=40))
            time.sleep(0.2)

    print("2) Collecting via manually seeded MP/Indore channels")
    for channel in MANUAL_YOUTUBE_CHANNELS:
        channel_id, channel_title = resolve_channel_id(youtube, channel)
        if not channel_id:
            continue

        uploads = get_uploads_playlist(youtube, channel_id)
        if not uploads:
            continue

        videos = get_latest_videos_from_channel(youtube, uploads, max_videos=20)

        for video in videos:
            if not video["video_id"] or video["video_id"] in seen_videos:
                continue

            context = video["title"] + " " + video["description"]
            if not is_rau_related(context):
                continue

            seen_videos.add(video["video_id"])
            video["channel_title"] = channel_title

            print(f"Channel video comments: {channel_title} | {video['title'][:80]}")
            all_rows.extend(get_comments(youtube, video, video["title"][:120], max_comments=40))
            time.sleep(0.2)

    df = pd.DataFrame(all_rows)
    save_posts(df)
    print(f"Saved {len(df)} Rau YouTube comments")

if __name__ == "__main__":
    collect_rau_youtube()
