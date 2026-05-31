from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///election_sentiment.db")

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            text TEXT,
            keyword TEXT,
            created_at TEXT,
            sentiment TEXT,
            sentiment_score REAL,
            source_url TEXT
        )
        """))

def save_posts(df):
    if df is not None and not df.empty:
        df.to_sql("posts", engine, if_exists="append", index=False)

def load_posts():
    try:
        return pd.read_sql("SELECT * FROM posts", engine)
    except Exception:
        return pd.DataFrame()
