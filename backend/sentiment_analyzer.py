from transformers import pipeline

# Initialize sentiment analysis model
sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> dict:
    """
    Perform sentiment analysis on given text using Hugging Face pipeline.
    Returns a dictionary with label and score.
    """
    if not text or len(text.strip()) < 5:
        return {"label": "NEUTRAL", "score": 0.0}

    try:
        result = sentiment_model(text[:512])[0]  # truncate long text
        return {
            "label": result["label"].upper(),
            "score": round(result["score"], 3)
        }
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"label": "ERROR", "score": 0.0}
