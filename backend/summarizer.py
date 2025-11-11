# backend/summarizer.py
import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# Load Hugging Face API key (if needed for hosted models)
HF_API_KEY = os.getenv("HF_API_KEY")

print("🔄 Loading summarization model... (this may take 1–2 minutes on first run)")

# Load local or Hugging Face summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",  # good balance of speed + quality
    device_map="auto" if HF_API_KEY else None
)

print("✅ Summarizer model loaded successfully!")

def summarize_text(text: str, max_length: int = 120, min_length: int = 30) -> str:
    """
    Summarize given text using transformer model.
    """
    if not text or len(text.strip()) == 0:
        return "No content to summarize."

    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Summarization failed: {str(e)}"

