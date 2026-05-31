import pandas as pd
from pytrends.request import TrendReq

def collect_google_trends():
    pytrend = TrendReq(hl="en-IN", tz=330)

    keywords = [
        "Narendra Modi",
        "Rahul Gandhi",
        "BJP",
        "Congress",
        "India election"
    ]

    pytrend.build_payload(
        keywords,
        cat=0,
        timeframe="today 12-m",
        geo="IN",
        gprop=""
    )

    df = pytrend.interest_over_time()

    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    df.to_csv("google_trends.csv")
    print("Saved Google Trends data to google_trends.csv")

if __name__ == "__main__":
    collect_google_trends()
