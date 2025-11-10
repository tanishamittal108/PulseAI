# dashboard/app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timezone
from utils.helpers import clean_text, truncate, format_datetime, sentiment_color

# ---- Config ----
API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000")
POLL_SECONDS = 8  # dashboard refresh interval

st.set_page_config(page_title="PulseAI — Smart NewsSense", layout="wide")
st.title("🧠 PulseAI — Smart NewsSense Dashboard")
st.markdown("Feel the pulse of the world — summarized and analyzed in real time.")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    topic = st.text_input("Topic / Keyword", value="AI")
    country = st.text_input("Country (2-letter code)", value="us")
    count = st.slider("Articles to fetch", 1, 20, 5)
    auto_refresh = st.checkbox("Auto refresh", value=True)
    st.markdown("---")
    st.markdown("Backend:")
    API_BASE = st.text_input("Backend URL", API_BASE)
    st.code(API_BASE)

# Helper to fetch from backend
def fetch_news(topic, country="us", page_size=5):
    try:
        # 🔥 Increased timeout from 15 → 60 seconds
        resp = requests.get(
            f"{API_BASE}/news",
            params={"topic": topic, "country": country, "page_size": page_size},
            timeout=60
        )
        if resp.ok:
            return resp.json()
        else:
            st.error(f"Backend error: {resp.status_code} {resp.text}")
            return []
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []

placeholder = st.empty()
last_fetched = None

def render(articles):
    # Convert to DataFrame for charts
    rows = []
    for a in articles:
        title = a.get("title") or ""
        summary = a.get("summary") or a.get("description") or ""
        summary = clean_text(summary)
        sentiment = a.get("sentiment", {}).get("label") if isinstance(a.get("sentiment"), dict) else a.get("sentiment")
        score = a.get("sentiment", {}).get("score") if isinstance(a.get("sentiment"), dict) else None
        published = a.get("publishedAt") or a.get("published_at") or ""
        rows.append({
            "title": title,
            "summary": truncate(summary, 350),
            "sentiment_label": sentiment or "UNKNOWN",
            "sentiment_score": score if score is not None else None,
            "publishedAt": format_datetime(published)
        })
    df = pd.DataFrame(rows)
    with placeholder.container():
        col_left, col_right = st.columns([3, 1])
        with col_right:
            st.metric("Articles shown", len(rows))
            if not df.empty and df['sentiment_label'].notnull().any():
                counts = df['sentiment_label'].value_counts().to_dict()
                st.write("Sentiment counts")
                st.write(counts)
        with col_left:
            st.subheader(f"Latest summaries for '{topic}'")
            for idx, row in df.iterrows():
                st.markdown(f"### {row['title']}")
                sent = row['sentiment_label']
                score = row['sentiment_score']
                sent_display = f"{sent}" + (f" ({score:.2f})" if score is not None else "")
                st.markdown(
                    f"**Sentiment:** <span style='color:{sentiment_color(sent)}'>{sent_display}</span>",
                    unsafe_allow_html=True
                )
                st.write(row['summary'])
                st.markdown("---")
        # sentiment trend chart (if scores available)
        if not df.empty and df['sentiment_score'].notnull().any():
            st.subheader("Sentiment Trend")
            df_chart = df.dropna(subset=['sentiment_score']).copy()
            df_chart['t'] = range(len(df_chart))
            st.line_chart(df_chart.set_index('t')['sentiment_score'])

# ---- Main Loop ----
articles = fetch_news(topic, country, page_size=count)
if not articles:
    st.info("No articles returned yet. Try a different topic or check backend logs.")
else:
    render(articles)
    last_fetched = datetime.utcnow()

if auto_refresh:
    while True:
        time.sleep(POLL_SECONDS)
        articles = fetch_news(topic, country, page_size=count)
        render(articles)
        last_fetched = datetime.now(timezone.utc)
        time.sleep(0.001)  # reduce CPU usage
