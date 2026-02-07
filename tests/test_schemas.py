"""
Tests for NewsIntel Pydantic schemas.
"""

from datetime import datetime

import pytest

from newsintel.schemas import (
    NewsArticle,
    NewsSource,
    AnalysisResult,
    SentimentResult,
    SentimentType,
)


class TestNewsArticle:
    """Tests for NewsArticle model."""

    def test_create_minimal_article(self) -> None:
        """Test creating article with minimal required fields."""
        article = NewsArticle(
            title="Test Article",
            source="Test Source",
        )
        assert article.title == "Test Article"
        assert article.source == "Test Source"
        assert article.summary == ""
        assert article.tags == []

    def test_create_full_article(self) -> None:
        """Test creating article with all fields."""
        article = NewsArticle(
            title="Full Test Article",
            summary="This is a test summary",
            content="Full content here",
            url="https://example.com/article",
            source="Test Source",
            author="Test Author",
            tags=["ai", "tech"],
        )
        assert article.title == "Full Test Article"
        assert article.author == "Test Author"
        assert len(article.tags) == 2


class TestAnalysisResult:
    """Tests for AnalysisResult model."""

    def test_create_empty_result(self) -> None:
        """Test creating empty analysis result."""
        result = AnalysisResult()
        assert result.article_count == 0
        assert result.avg_sentiment == 0.0
        assert result.topics == []

    def test_add_insight(self) -> None:
        """Test adding insights to result."""
        result = AnalysisResult()
        result.add_insight("Test insight")
        assert len(result.insights) == 1
        assert "Test insight" in result.insights

    def test_get_summary(self) -> None:
        """Test summary generation."""
        result = AnalysisResult(
            article_count=10,
            avg_sentiment=0.5,
            topics=["ai", "tech"],
        )
        summary = result.get_summary()
        assert "10 articles" in summary
        assert "0.50" in summary
