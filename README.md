# Election Sentiment MVP

This is a simple MVP for election sentiment analysis using:

- YouTube Data API
- NewsAPI
- Hugging Face sentiment model
- SQLite database
- Streamlit dashboard

## 1. Create virtual environment

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Create `.env`

Copy `.env.example` to `.env`.

### Linux / Mac

```bash
cp .env.example .env
nano .env
```

### Windows

```bash
copy .env.example .env
notepad .env
```

Paste your actual API keys.

## 4. Collect news data

```bash
python collect_news.py
```

## 5. Collect YouTube comments

```bash
python collect_youtube.py
```

## 6. Run dashboard

```bash
streamlit run app.py
```

Open the local URL shown in terminal, usually:

```text
http://localhost:8501
```

## Notes

- First run may take time because the sentiment model downloads.
- Data is stored in `election_sentiment.db`.
- For MVP, SQLite is used. Later you can upgrade to PostgreSQL.
