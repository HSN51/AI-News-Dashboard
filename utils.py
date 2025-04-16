import streamlit as st
import requests
import json
from config import NEWSAPI_KEY, NEWSAPI_BASE_URL, SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from datetime import datetime
from dateutil import parser  # For parsing date strings

# --- NLTK VADER Download Check ---
# Check if VADER lexicon is downloaded; if not, download it.
# This is important on the first run or in different environments.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except (OSError, LookupError):
    st.info("Downloading VADER lexicon...")
    try:
        nltk.download('vader_lexicon')
        st.success("VADER lexicon downloaded successfully.")
    except Exception as e:
        st.error(f"Failed to download VADER lexicon: {e}")
        # Sentiment analysis won't work without the lexicon; stop the app
        st.stop()
except Exception as e:
    st.warning(f"Unexpected error during NLTK check: {e}")


# --- News Fetching Function ---
# Cache: Store results of requests with the same parameters for 30 minutes
@st.cache_data(ttl=1800, show_spinner="Fetching news from NewsAPI...")
def fetch_news(topic: str, language: str = 'en', page_size: int = 10, sort_by: str = 'relevancy') -> tuple[list, list]:
    """
    Fetches news from NewsAPI based on given topic, language, and settings.
    Returns a tuple of (list of articles, list of errors/warnings).
    """
    if not NEWSAPI_KEY:
        return [], ["❌ Error: NewsAPI key not found. Please check your .env file or set up Streamlit secrets."]

    params = {
        "q": topic,
        "apiKey": NEWSAPI_KEY,
        "pageSize": min(page_size, 100),  # API allows max 100
        "sortBy": sort_by,
        "language": language
    }
    articles = []
    errors = []

    try:
        response = requests.get(NEWSAPI_BASE_URL, params=params, timeout=15)

        # Check for HTTP Errors
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    if not articles:
                        errors.append(f"ℹ️ No news found for topic '{topic}' in language '{language}'.")
                else:
                    errors.append(f"❌ NewsAPI Error: {data.get('code')} - {data.get('message')}")
            except json.JSONDecodeError:
                errors.append(f"❌ Error: Response from NewsAPI is not in valid JSON format.")
        elif response.status_code == 400:
            errors.append(f"❌ API Error (400): Invalid request parameters. Please check your inputs.")
        elif response.status_code == 401:
            errors.append(f"❌ API Error (401): Invalid API key. Please verify your key.")
        elif response.status_code == 429:
            errors.append(f"❌ API Error (429): Too many requests. Please wait and try again (rate limit exceeded).")
        elif response.status_code >= 500:
            errors.append(f"❌ Server Error ({response.status_code}): NewsAPI server may be temporarily unavailable. Please try again later.")
        else:
            errors.append(f"❌ HTTP Error: {response.status_code} - {response.reason}")

    except requests.exceptions.Timeout:
        errors.append("❌ Error: Request to NewsAPI timed out.")
    except requests.exceptions.ConnectionError:
        errors.append("❌ Error: Could not connect to NewsAPI. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        errors.append(f"❌ General Network Error: {e}")
    except Exception as e:
        errors.append(f"❌ Unexpected Error: {e}")

    return articles, errors


# --- Sentiment Analysis Function ---
@st.cache_resource  # Cache the analyzer object
def get_sentiment_analyzer():
    """Loads and returns the VADER Sentiment Analyzer object."""
    return SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text: str) -> tuple[str, float]:
    """
    Returns the sentiment label and compound score of a given text using VADER.
    Output: (Label: 'Positive', 'Negative', or 'Neutral', Compound Score)
    """
    if not isinstance(text, str) or not text.strip():
        return "Neutral", 0.0  # Return neutral for empty/invalid input

    analyzer = get_sentiment_analyzer()
    try:
        vs = analyzer.polarity_scores(text)
        compound_score = vs['compound']

        if compound_score >= SENTIMENT_THRESHOLD_POSITIVE:
            return "Positive", compound_score
        elif compound_score <= SENTIMENT_THRESHOLD_NEGATIVE:
            return "Negative", compound_score
        else:
            return "Neutral", compound_score
    except Exception as e:
        st.warning(f"Error during sentiment analysis: {e}")
        return "Neutral", 0.0


# --- Helper Function: Format Date ---
def format_datetime(date_string: str) -> str:
    """Converts an ISO date string into a more readable format."""
    if not date_string:
        return "No Date"
    try:
        dt_object = parser.isoparse(date_string)
        return dt_object.strftime("%d %B %Y, %H:%M")  # Example: 25 December 2023, 15:30
    except Exception:
        return date_string.split('T')[0]  # Return only the date part if parsing fails
