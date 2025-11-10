# backend/news_fetcher.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_latest_news(query="AI", language="en", page_size=5):
    """
    Fetch latest news headlines using NewsAPI.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch news from NewsAPI")

    data = response.json()
    articles = data.get("articles", [])

    # Extract title + description for summarization
    cleaned_articles = [
        {
            "title": article["title"],
            "content": article.get("description") or article.get("content") or "",
        }
        for article in articles if article.get("title")
    ]

    return cleaned_articles
