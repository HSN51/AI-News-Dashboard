# app.py
import streamlit as st

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Google News Current News Fetcher",
    page_icon="📰",
    layout="wide",
)

# Other imports
import pandas as pd  # For statistics or tables
from config import (
    DEFAULT_TOPIC, DEFAULT_LANGUAGE, DEFAULT_PAGE_SIZE, AVAILABLE_LANGUAGES,
    SORT_BY_OPTIONS, MAX_ARTICLES_TO_DISPLAY
)
from utils import fetch_news, analyze_sentiment_vader, format_datetime
import os  # For API Key check

# --- Sidebar ---
with st.sidebar:
    st.header("🧠 Smart News Feed")
    st.markdown("Fetch current news using NewsAPI and view sentiment analysis.")
    st.divider()

    # API Key Check (Informational only)
    if not os.getenv("NEWSAPI_KEY"):
        st.error("NewsAPI Key not found!")
        st.caption("Please add it to the `.env` file or Streamlit Secrets.")

    st.header("📰 Search Settings")
    # Topic Input
    topic = st.text_input("News Topic:", value=DEFAULT_TOPIC)
    # Language Selection
    lang_label = st.selectbox("News Language:", options=list(AVAILABLE_LANGUAGES.keys()), index=0)
    language = AVAILABLE_LANGUAGES[lang_label]  # Get language code from selected label
    # Number of News Articles
    page_size = st.slider("Maximum Number of News Articles:", min_value=5, max_value=MAX_ARTICLES_TO_DISPLAY, value=DEFAULT_PAGE_SIZE, step=5)
    # Sorting Criteria
    sort_by = st.selectbox("Sorting Criteria:", options=SORT_BY_OPTIONS, index=0)
    st.divider()

    # Search Button
    search_button = st.button("🔍 Fetch News")


# --- Main Content Area ---
st.title("🧠 Smart News Feed")

# If the search button is clicked and a topic is entered, fetch the news
if search_button and topic:
    # Call the function to fetch news
    articles, errors = fetch_news(topic, language, page_size, sort_by)

    # Display errors first (if any)
    if errors:
        for error in errors:
            st.error(error)

    # If news articles are found, process them
    if articles:
        st.success(f"Found {len(articles)} news articles on '{topic}'.")
        st.divider()

        # Lists to collect sentiment analysis results
        sentiments = []
        sentiment_scores = []

        # Process and display each news article
        for article in articles:
            col1, col2 = st.columns([1, 3])  # Small column for image, large column for text

            with col1:
                # Display image if available (with error handling)
                if article.get('urlToImage'):
                    try:
                        st.image(article['urlToImage'], use_column_width=True)
                    except Exception as img_err:
                        st.caption(f"Image could not be loaded: {img_err}")
                else:
                     st.caption("No Image")

            with col2:
                # Title
                st.subheader(article.get('title', 'No Title'))
                # Source and Date
                source_name = article.get('source', {}).get('name', 'No Source')
                published_at = format_datetime(article.get('publishedAt'))
                st.caption(f"Source: {source_name} | Published: {published_at}")

                # Description (if available)
                description = article.get('description')
                if description:
                    st.write(description)

                    # --- Sentiment Analysis ---
                    sentiment_label, sentiment_score = analyze_sentiment_vader(description)
                    sentiments.append(sentiment_label)
                    sentiment_scores.append(sentiment_score)

                    # Display sentiment label and score
                    emoji = "🙂" if sentiment_label == "Positive" else ("😠" if sentiment_label == "Negative" else "😐")
                    st.markdown(f"**Sentiment:** {emoji} {sentiment_label} (Score: {sentiment_score:.2f})")
                    # --- End of Sentiment Analysis ---

                # Link to the full news article
                if article.get('url'):
                    st.markdown(f"[🔗 Read Full Article]({article['url']})", unsafe_allow_html=True)

            st.divider()  # Separator between articles

        # --- Overall Sentiment Summary ---
        if sentiments:
             st.subheader("📊 Overall Sentiment Distribution")
             sentiment_counts = pd.Series(sentiments).value_counts()
             # Define colors
             colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'grey'}
             try:
                st.bar_chart(sentiment_counts, color=[colors.get(x, '#888888') for x in sentiment_counts.index])
             except Exception as chart_err:
                 st.warning(f"Error while drawing chart: {chart_err}")
                 st.write(sentiment_counts)  # If chart cannot be drawn, display the data


    # If no news articles are found (and no API errors)
    elif not errors:
         st.info(f"No news articles found for '{topic}' in {language} language.")

# If no topic is entered or the button is not clicked, display a starting message
elif not topic:
    st.info("Please enter a topic to search.")