from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///election_sentiment_rau.db")

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS constituency_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            constituency_no INTEGER,
            constituency TEXT,
            district TEXT,
            region TEXT,
            platform TEXT,
            source_name TEXT,
            text TEXT,
            keyword TEXT,
            matched_entity TEXT,
            entity_type TEXT,
            issue_category TEXT,
            created_at TEXT,
            sentiment TEXT,
            sentiment_score REAL,
            source_url TEXT
        )
        """))

def save_posts(df):
    if df is not None and not df.empty:
        df.to_sql("constituency_posts", engine, if_exists="append", index=False)

def load_posts():
    try:
        return pd.read_sql("SELECT * FROM constituency_posts", engine)
    except Exception:
        return pd.DataFrame()
