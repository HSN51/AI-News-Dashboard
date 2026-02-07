"""
NewsIntel - AI-powered news intelligence dashboard.

This package provides tools for collecting, analyzing, and presenting
AI/ML news using CrewAI agents and a Streamlit interface.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from newsintel.schemas import NewsArticle, AnalysisResult, NewsSource

__all__ = [
    "__version__",
    "NewsArticle",
    "AnalysisResult", 
    "NewsSource",
]
