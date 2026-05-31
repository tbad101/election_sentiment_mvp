import pandas as pd
from pytrends.request import TrendReq
from rau_config import TREND_GROUPS

def collect_rau_trends():
    pytrend = TrendReq(hl="hi-IN", tz=330)
    frames = []

    for group in TREND_GROUPS:
        try:
            print(f"Fetching trends for: {group}")
            # Google Trends does not provide Assembly Constituency-level geography.
            # IN-MP is the closest free geographic level.
            pytrend.build_payload(group, cat=0, timeframe="today 12-m", geo="IN-MP", gprop="")
            df = pytrend.interest_over_time()

            if df.empty:
                continue

            if "isPartial" in df.columns:
                df = df.drop(columns=["isPartial"])

            df = df.reset_index()
            df["constituency"] = "Rau"
            df["geo_level"] = "Madhya Pradesh proxy"
            df["group"] = ", ".join(group)
            frames.append(df)

        except Exception as e:
            print(f"Trend error: {group} | {e}")

    if frames:
        final = pd.concat(frames, ignore_index=True)
        final.to_csv("rau_google_trends.csv", index=False)
        print("Saved rau_google_trends.csv")
    else:
        print("No trends collected")

if __name__ == "__main__":
    collect_rau_trends()
