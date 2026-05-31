# Rau Constituency Phase 1

Copy these files into your existing `election_sentiment_mvp` folder:

- database_rau.py
- rau_config.py
- rau_tagging.py
- collect_rau_news.py
- collect_rau_youtube.py
- collect_rau_trends.py
- app_rau.py

Your existing files are reused:

- `.env`
- `sentiment.py`
- `requirements.txt`

## Run in VS Code terminal

Activate your virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Then run:

```bash
python collect_rau_news.py
python collect_rau_youtube.py
python collect_rau_trends.py
streamlit run app_rau.py
```

## Edit later

Open `rau_config.py` and modify:

- location terms
- local areas
- party aliases
- candidate aliases
- issue keywords
- YouTube channels
- search queries

## Important limitation

Free sources cannot reliably provide booth-level or voter-level sentiment. Google Trends does not provide assembly constituency-level geography, so `collect_rau_trends.py` uses MP-level Trends as a proxy.
