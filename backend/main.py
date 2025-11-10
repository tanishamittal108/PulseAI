# backend/main.py
from fastapi import FastAPI, Query
from backend.news_fetcher import fetch_latest_news
from backend.summarizer import summarize_text

app = FastAPI(title="PulseAI Backend", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to PulseAI Backend 🚀"}

@app.get("/news")
def get_news(topic: str = Query("AI", description="Topic to search news about")):
    """
    Fetch and summarize the latest news.
    """
    articles = fetch_latest_news(query=topic)
    summarized = []

    for article in articles:
        summary = summarize_text(article["content"])
        summarized.append({
            "title": article["title"],
            "summary": summary
        })

    return summarized

