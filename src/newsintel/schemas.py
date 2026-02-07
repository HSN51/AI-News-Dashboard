"""
Pydantic models for NewsIntel data structures.

This module defines the core data models used throughout the application
for type safety and data validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class SentimentType(str, Enum):
    """Enumeration of possible sentiment classifications."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class NewsSource(BaseModel):
    """Represents a news source configuration.
    
    Attributes:
        name: Display name of the source.
        url: Base URL of the news source.
        api_key: Optional API key for authentication.
        enabled: Whether this source is currently active.
        priority: Source priority for ranking (higher = more important).
    """
    name: str = Field(..., min_length=1, max_length=100)
    url: HttpUrl
    api_key: Optional[str] = Field(default=None, exclude=True)
    enabled: bool = Field(default=True)
    priority: int = Field(default=1, ge=1, le=10)
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "TechCrunch",
                "url": "https://techcrunch.com",
                "enabled": True,
                "priority": 5,
            }
        }


class NewsArticle(BaseModel):
    """Represents a single news article.
    
    Attributes:
        title: Article headline.
        summary: Brief summary or excerpt.
        content: Full article content (if available).
        url: Link to the original article.
        source: Name of the news source.
        author: Article author (if available).
        published_at: Publication timestamp.
        fetched_at: When the article was retrieved.
        image_url: URL to article thumbnail/image.
        tags: List of associated tags or categories.
    """
    title: str = Field(..., min_length=1, max_length=500)
    summary: str = Field(default="", max_length=2000)
    content: Optional[str] = Field(default=None)
    url: Optional[HttpUrl] = Field(default=None)
    source: str = Field(..., min_length=1)
    author: Optional[str] = Field(default=None)
    published_at: datetime = Field(default_factory=datetime.now)
    fetched_at: datetime = Field(default_factory=datetime.now)
    image_url: Optional[HttpUrl] = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "title": "New AI Breakthrough Announced",
                "summary": "Researchers unveil new model capabilities...",
                "source": "TechCrunch",
                "published_at": "2024-01-15T10:30:00Z",
            }
        }


class SentimentResult(BaseModel):
    """Represents sentiment analysis results for an article.
    
    Attributes:
        article_id: Reference to the analyzed article.
        sentiment: Overall sentiment classification.
        score: Sentiment score (-1.0 to 1.0).
        confidence: Confidence level of the analysis.
        keywords: Extracted key phrases.
    """
    article_id: str
    sentiment: SentimentType = Field(default=SentimentType.NEUTRAL)
    score: float = Field(default=0.0, ge=-1.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    keywords: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Aggregated analysis results from the crew.
    
    Attributes:
        article_count: Total number of articles analyzed.
        avg_sentiment: Average sentiment score across articles.
        topics: Identified main topics.
        insights: Key insights extracted from analysis.
        raw_articles: Original articles data.
        created_at: Timestamp of analysis.
    """
    article_count: int = Field(default=0, ge=0)
    avg_sentiment: float = Field(default=0.0, ge=-1.0, le=1.0)
    topics: list[str] = Field(default_factory=list)
    insights: list[str] = Field(default_factory=list)
    raw_articles: list[NewsArticle] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def add_insight(self, insight: str) -> None:
        """Add a new insight to the results.
        
        Args:
            insight: The insight text to add.
        """
        self.insights.append(insight)
    
    def get_summary(self) -> str:
        """Generate a text summary of the analysis.
        
        Returns:
            Formatted summary string.
        """
        return (
            f"Analyzed {self.article_count} articles. "
            f"Average sentiment: {self.avg_sentiment:.2f}. "
            f"Key topics: {', '.join(self.topics[:5])}."
        )


class CrewTaskResult(BaseModel):
    """Result from a single crew task execution.
    
    Attributes:
        task_name: Name of the executed task.
        agent_role: Role of the agent that performed the task.
        output: Raw output from the task.
        success: Whether the task completed successfully.
        execution_time: Time taken to execute (seconds).
        error: Error message if task failed.
    """
    task_name: str
    agent_role: str
    output: str = Field(default="")
    success: bool = Field(default=True)
    execution_time: float = Field(default=0.0, ge=0.0)
    error: Optional[str] = Field(default=None)
