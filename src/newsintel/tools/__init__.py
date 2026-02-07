"""
Custom tools for NewsIntel CrewAI agents.

This module exports all available tools for use by agents
in the news intelligence gathering and analysis pipeline.
"""

from newsintel.tools.search import search_news, search_by_keyword
from newsintel.tools.scraper import scrape_article, extract_content
from newsintel.tools.analyzer import analyze_sentiment, extract_topics

__all__ = [
    "search_news",
    "search_by_keyword",
    "scrape_article",
    "extract_content",
    "analyze_sentiment",
    "extract_topics",
]
