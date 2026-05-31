import streamlit as st
import plotly.express as px
import pandas as pd
from database import init_db, load_posts

st.set_page_config(
    page_title="Election Sentiment MVP",
    layout="wide"
)

init_db()

st.title("Election Sentiment Analysis MVP")

df = load_posts()

if df.empty:
    st.warning("No data found. First run: python collect_news.py and python collect_youtube.py")
    st.stop()

st.sidebar.header("Filters")

platforms = st.sidebar.multiselect(
    "Platform",
    options=sorted(df["platform"].dropna().unique()),
    default=sorted(df["platform"].dropna().unique())
)

keywords = st.sidebar.multiselect(
    "Keyword",
    options=sorted(df["keyword"].dropna().unique()),
    default=sorted(df["keyword"].dropna().unique())
)

filtered = df[
    (df["platform"].isin(platforms)) &
    (df["keyword"].isin(keywords))
]

st.metric("Total Records", len(filtered))

col1, col2 = st.columns(2)

with col1:
    sentiment_count = filtered["sentiment"].value_counts().reset_index()
    sentiment_count.columns = ["sentiment", "count"]

    fig = px.bar(
        sentiment_count,
        x="sentiment",
        y="count",
        title="Overall Sentiment Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    platform_count = filtered["platform"].value_counts().reset_index()
    platform_count.columns = ["platform", "count"]

    fig = px.pie(
        platform_count,
        names="platform",
        values="count",
        title="Data Source Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("Keyword-wise Sentiment")

keyword_sentiment = filtered.groupby(
    ["keyword", "sentiment"]
).size().reset_index(name="count")

fig2 = px.bar(
    keyword_sentiment,
    x="keyword",
    y="count",
    color="sentiment",
    barmode="group",
    title="Sentiment by Keyword"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Collected Data")

st.dataframe(
    filtered[["platform", "keyword", "sentiment", "sentiment_score", "text", "source_url"]],
    use_container_width=True
)

st.subheader("Google Trends Data")

try:
    trends = pd.read_csv("google_trends.csv")
    st.dataframe(trends, use_container_width=True)

    trend_long = trends.melt(id_vars=["date"], var_name="keyword", value_name="interest")

    fig3 = px.line(
        trend_long,
        x="date",
        y="interest",
        color="keyword",
        title="Google Trends Interest Over Time"
    )

    st.plotly_chart(fig3, use_container_width=True)

except Exception:
    st.info("Google Trends data not found. Run: python collect_trends.py")
