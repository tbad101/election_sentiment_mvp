import streamlit as st
import pandas as pd
import plotly.express as px
from database_rau import init_db, load_posts

st.set_page_config(page_title="Rau Election Intelligence Dashboard", layout="wide")

init_db()
df = load_posts()

st.title("Election Intelligence Dashboard")
st.caption("Phase 1: Madhya Pradesh overview + Rau constituency drill-down")

if df.empty:
    st.warning("No Rau data yet. Run: python collect_rau_news.py and python collect_rau_youtube.py")
    st.stop()

df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["date"] = df["created_at"].dt.date

page = st.sidebar.radio(
    "Navigate",
    ["MP Overview", "Rau Constituency", "Party Analysis", "Candidate Analysis", "Issue Analysis", "Raw Data"]
)

st.sidebar.header("Filters")

platforms = st.sidebar.multiselect(
    "Platform",
    sorted(df["platform"].dropna().unique()),
    default=sorted(df["platform"].dropna().unique())
)

sources = st.sidebar.multiselect(
    "Source",
    sorted(df["source_name"].dropna().unique()),
    default=sorted(df["source_name"].dropna().unique())[:20]
)

sentiments = st.sidebar.multiselect(
    "Sentiment",
    sorted(df["sentiment"].dropna().unique()),
    default=sorted(df["sentiment"].dropna().unique())
)

filtered = df[
    df["platform"].isin(platforms) &
    df["source_name"].isin(sources) &
    df["sentiment"].isin(sentiments)
].copy()

def sentiment_metrics(data):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", len(data))
    c2.metric("Positive", int((data["sentiment"] == "positive").sum()))
    c3.metric("Neutral", int((data["sentiment"] == "neutral").sum()))
    c4.metric("Negative", int((data["sentiment"] == "negative").sum()))

def sentiment_chart(data, title="Sentiment Distribution"):
    counts = data["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    fig = px.bar(counts, x="sentiment", y="count", title=title)
    st.plotly_chart(fig, use_container_width=True)

def trend_chart(data, title="Sentiment Trend"):
    trend = data.dropna(subset=["date"]).groupby(["date", "sentiment"]).size().reset_index(name="count")
    if trend.empty:
        st.info("No date-wise trend available.")
    else:
        fig = px.line(trend, x="date", y="count", color="sentiment", title=title)
        st.plotly_chart(fig, use_container_width=True)

if page == "MP Overview":
    st.header("MP Overview")
    st.info("In Phase 1 this page uses Rau-tagged data only. Later, we will add all 230 constituencies into the same schema.")
    sentiment_metrics(filtered)

    col1, col2 = st.columns(2)
    with col1:
        sentiment_chart(filtered, "Overall Sentiment")
    with col2:
        src = filtered["source_name"].value_counts().head(15).reset_index()
        src.columns = ["source", "count"]
        fig = px.bar(src, x="count", y="source", orientation="h", title="Top Sources")
        st.plotly_chart(fig, use_container_width=True)

    trend_chart(filtered, "Overall Sentiment Trend")

elif page == "Rau Constituency":
    st.header("Rau Constituency View")
    st.caption("Constituency No. 210 | District: Indore | Region: Malwa / Indore")
    sentiment_metrics(filtered)
    trend_chart(filtered, "Rau Sentiment Trend")

    st.subheader("Source-wise Sentiment")
    tmp = filtered.groupby(["source_name", "sentiment"]).size().reset_index(name="count")
    fig = px.bar(tmp, x="source_name", y="count", color="sentiment", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Party Analysis":
    st.header("Party-wise Analysis")
    data = filtered[filtered["entity_type"] == "party"]
    sentiment_metrics(data)

    tmp = data.groupby(["matched_entity", "sentiment"]).size().reset_index(name="count")
    fig = px.bar(tmp, x="matched_entity", y="count", color="sentiment", barmode="group", title="Party-wise Sentiment")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data[["created_at", "source_name", "matched_entity", "sentiment", "text", "source_url"]], use_container_width=True)

elif page == "Candidate Analysis":
    st.header("Candidate / Leader Analysis")
    data = filtered[filtered["entity_type"] == "candidate/leader"]
    sentiment_metrics(data)

    tmp = data.groupby(["matched_entity", "sentiment"]).size().reset_index(name="count")
    fig = px.bar(tmp, x="matched_entity", y="count", color="sentiment", barmode="group", title="Candidate-wise Sentiment")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Negative")
    neg = data[data["sentiment"] == "negative"].sort_values("sentiment_score", ascending=False).head(20)
    st.dataframe(neg[["created_at", "source_name", "matched_entity", "sentiment_score", "text", "source_url"]], use_container_width=True)

    st.subheader("Top Positive")
    pos = data[data["sentiment"] == "positive"].sort_values("sentiment_score", ascending=False).head(20)
    st.dataframe(pos[["created_at", "source_name", "matched_entity", "sentiment_score", "text", "source_url"]], use_container_width=True)

elif page == "Issue Analysis":
    st.header("Issue-wise Analysis")
    data = filtered.copy()
    sentiment_metrics(data)

    tmp = data.groupby(["issue_category", "sentiment"]).size().reset_index(name="count")
    fig = px.bar(tmp, x="issue_category", y="count", color="sentiment", barmode="group", title="Issue-wise Sentiment")
    st.plotly_chart(fig, use_container_width=True)

    issue_count = data["issue_category"].value_counts().head(20).reset_index()
    issue_count.columns = ["issue", "count"]
    fig2 = px.bar(issue_count, x="count", y="issue", orientation="h", title="Top Issues")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Raw Data":
    st.header("Raw Data")
    st.dataframe(
        filtered[[
            "created_at", "constituency", "platform", "source_name", "keyword",
            "matched_entity", "entity_type", "issue_category",
            "sentiment", "sentiment_score", "text", "source_url"
        ]],
        use_container_width=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data", csv, "rau_election_intelligence.csv", "text/csv")

st.subheader("Google Trends Proxy")

try:
    trends = pd.read_csv("rau_google_trends.csv")
    st.caption("Google Trends is MP-level proxy, not assembly constituency-level.")
    st.dataframe(trends, use_container_width=True)

    id_cols = ["date", "constituency", "geo_level", "group"]
    value_cols = [c for c in trends.columns if c not in id_cols]
    long = trends.melt(id_vars=id_cols, value_vars=value_cols, var_name="keyword", value_name="interest")

    fig = px.line(long, x="date", y="interest", color="keyword", line_dash="group", title="Rau-related Google Trends, MP proxy")
    st.plotly_chart(fig, use_container_width=True)

except Exception:
    st.info("No Rau Google Trends file yet. Run: python collect_rau_trends.py")
