# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# NewsAPI Configuration
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"  # Or use the 'top-headlines' endpoint

# Default Search Parameters
DEFAULT_TOPIC = "artificial intelligence"
DEFAULT_LANGUAGE = "en"  # Try 'tr' for Turkish news, though API support may be limited
DEFAULT_PAGE_SIZE = 10
AVAILABLE_LANGUAGES = {
    "English": "en",
    "Turkish": "tr",
    "German": "de",
    "French": "fr"
}
SORT_BY_OPTIONS = ["relevancy", "popularity", "publishedAt"]

# Sentiment Analysis Configuration (for VADER)
# Threshold values based on compound score
SENTIMENT_THRESHOLD_POSITIVE = 0.05
SENTIMENT_THRESHOLD_NEGATIVE = -0.05

# UI Configuration
MAX_ARTICLES_TO_DISPLAY = 50  # Maximum number of articles to display
