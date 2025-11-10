# utils/helpers.py
import re
from datetime import datetime

def clean_text(text: str) -> str:
    """
    Remove URLs and weird characters; keep text readable.
    """
    if not text:
        return ""
    text = re.sub(r"http\S+", "", text)          # remove urls
    text = re.sub(r"\s+", " ", text).strip()     # collapse whitespace
    # optionally remove non-printable characters
    text = ''.join(ch for ch in text if ord(ch) >= 32)
    return text

def truncate(text: str, limit: int = 200) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit].rsplit(' ', 1)[0] + "..."

def format_datetime(dt_str: str) -> str:
    """
    Format ISO dates into readable form. If parsing fails, return original.
    """
    if not dt_str:
        return ""
    try:
        # handle common formats
        dt = None
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except Exception:
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                return dt_str
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return dt_str

def sentiment_color(label: str) -> str:
    """
    Map sentiment label to a display color.
    Accepts common labels: POSITIVE, NEGATIVE, NEUTRAL (case-insensitive).
    """
    if not label:
        return "#888888"
    lbl = label.strip().upper()
    if "POS" in lbl or "POSITIVE" in lbl:
        return "#2ecc71"  # green
    if "NEG" in lbl or "NEGATIVE" in lbl:
        return "#e74c3c"  # red
    if "NEUT" in lbl or "NEUTRAL" in lbl:
        return "#f1c40f"  # yellow
    return "#95a5a6"      # gray default
