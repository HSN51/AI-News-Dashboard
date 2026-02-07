"""
CrewAI crew definitions for news intelligence gathering and analysis.

This module contains the main crew configuration and agent definitions
for the NewsIntel system.

Usage:
    python -m newsintel.crew
"""

from __future__ import annotations

import os
import sys
from typing import Any, Optional
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7

from pydantic import BaseModel

from newsintel.schemas import AnalysisResult, NewsArticle
from newsintel.tools import search_news, scrape_article, analyze_sentiment

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try multiple locations for .env file
    env_paths = [
        Path(__file__).parent.parent.parent / ".env",  # Project root
        Path.cwd() / ".env",  # Current directory
        Path.cwd().parent / ".env",  # Parent directory (if in src/)
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # dotenv not installed, rely on system env vars


# ============================================================================
# Configuration
# ============================================================================

class AgentConfig(BaseModel):
    """Configuration for a CrewAI agent.
    
    Attributes:
        role: The agent's role description.
        goal: The agent's primary goal.
        backstory: Background context for the agent.
    """
    role: str
    goal: str
    backstory: str


def get_llm_config() -> dict[str, Any]:
    """Get LLM configuration from environment variables.
    
    Returns:
        Dictionary with LLM provider settings.
        
    Raises:
        EnvironmentError: If required API key is not set.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if openai_key:
        return {
            "provider": "openai",
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "api_key": openai_key,
        }
    elif anthropic_key:
        return {
            "provider": "anthropic",
            "model": os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            "api_key": anthropic_key,
        }
    elif gemini_key:
        return {
            "provider": "google",
            "model": os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"),
            "api_key": gemini_key,
        }
    else:
        raise EnvironmentError(
            "\n" + "=" * 60 + "\n"
            "❌ LLM API KEY NOT FOUND!\n"
            "=" * 60 + "\n\n"
            "Please set one of the following environment variables:\n\n"
            "  • OPENAI_API_KEY     - For OpenAI models (GPT-4, etc.)\n"
            "  • ANTHROPIC_API_KEY  - For Anthropic models (Claude)\n"
            "  • GOOGLE_API_KEY     - For Google models (Gemini)\n\n"
            "Example:\n"
            "  Windows:  set OPENAI_API_KEY=sk-your-key-here\n"
            "  Linux:    export OPENAI_API_KEY=sk-your-key-here\n\n"
            "Or create a .env file in the project root.\n"
            "=" * 60
        )


# ============================================================================
# CrewAI Demo Implementation
# ============================================================================

def run_demo() -> None:
    """Run a simple 2-agent CrewAI demo.
    
    This demo creates:
    - Agent1 (Researcher): Generates research text about AI trends
    - Agent2 (Reporter): Converts the research into 5 bullet points
    
    The demo shows basic agent collaboration and task chaining.
    """
    print("\n" + "=" * 60)
    print("🚀 NewsIntel CrewAI Demo")
    print("=" * 60 + "\n")
    
    # Step 1: Check LLM configuration
    print("📋 Step 1: Checking LLM configuration...")
    try:
        llm_config = get_llm_config()
        print(f"   ✅ Using {llm_config['provider'].upper()} - {llm_config['model']}\n")
    except EnvironmentError as e:
        print(str(e))
        sys.exit(1)
    
    # Step 2: Import and setup CrewAI
    print("📋 Step 2: Setting up CrewAI agents...")
    try:
        from crewai import Agent, Task, Crew, Process
    except ImportError:
        print("\n   ❌ CrewAI not installed!")
        print("   Run: pip install crewai")
        sys.exit(1)
    
    # Step 3: Create agents
    researcher = Agent(
        role="AI Research Specialist",
        goal="Research and compile information about artificial intelligence trends",
        backstory="""You are an expert AI researcher with deep knowledge of 
        current trends in machine learning, large language models, and 
        autonomous agents. You excel at finding and synthesizing information.""",
        verbose=True,
        allow_delegation=False,
    )
    
    reporter = Agent(
        role="News Reporter",
        goal="Transform research into clear, concise bullet points",
        backstory="""You are a skilled journalist who excels at taking complex 
        technical information and converting it into easy-to-understand 
        bullet points for a general audience.""",
        verbose=True,
        allow_delegation=False,
    )
    
    print("   ✅ Created 2 agents: Researcher, Reporter\n")
    
    # Step 4: Create tasks
    print("📋 Step 3: Creating tasks...")
    
    research_task = Task(
        description="""Research the latest trends in artificial intelligence for 2024-2025.
        Focus on:
        - Large Language Models (LLMs)
        - AI Agents and Automation
        - Multimodal AI systems
        - Enterprise AI adoption
        
        Provide a comprehensive paragraph summarizing the key developments.""",
        expected_output="A detailed paragraph about AI trends (150-200 words)",
        agent=researcher,
    )
    
    report_task = Task(
        description="""Take the research from the previous task and convert it into 
        exactly 5 clear, actionable bullet points.
        
        Each bullet point should:
        - Start with an emoji
        - Be concise (max 20 words)
        - Highlight a specific trend or insight""",
        expected_output="5 bullet points summarizing AI trends",
        agent=reporter,
        context=[research_task],  # This task depends on research_task output
    )
    
    print("   ✅ Created 2 tasks: Research → Report\n")
    
    # Step 5: Create and run crew
    print("📋 Step 4: Running the crew...\n")
    print("-" * 60)
    
    crew = Crew(
        agents=[researcher, reporter],
        tasks=[research_task, report_task],
        process=Process.sequential,  # Tasks run in order
        verbose=True,
    )
    
    result = crew.kickoff()
    
    # Step 6: Display results
    print("\n" + "-" * 60)
    print("\n📊 FINAL REPORT")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print("\n✅ Demo completed successfully!\n")
    
    return result


# ============================================================================
# NewsIntel Crew (Full Implementation)
# ============================================================================

class NewsIntelCrew:
    """Main crew orchestrator for news intelligence operations.
    
    This crew coordinates multiple agents to collect, analyze, and
    summarize news articles on specified topics.
    
    Attributes:
        config_path: Path to the sources configuration file.
        agents: List of configured agents.
    """
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize the NewsIntel crew.
        
        Args:
            config_path: Optional path to sources.yaml configuration.
        """
        self.config_path = config_path or self._default_config_path()
        self.agents: list[AgentConfig] = []
        self._setup_agents()
    
    def _default_config_path(self) -> Path:
        """Get the default configuration file path.
        
        Returns:
            Path to the default sources.yaml file.
        """
        return Path(__file__).parent.parent.parent / "config" / "sources.yaml"
    
    def _setup_agents(self) -> None:
        """Initialize and configure crew agents."""
        self.agents = [
            AgentConfig(
                role="News Researcher",
                goal="Find the most relevant and recent news articles on the given topic",
                backstory="Expert at discovering breaking news and trending stories from reliable sources"
            ),
            AgentConfig(
                role="Content Analyst",
                goal="Analyze news content for key insights, sentiment, and trends",
                backstory="Seasoned analyst with expertise in media analysis and trend identification"
            ),
            AgentConfig(
                role="Report Writer",
                goal="Synthesize findings into clear, actionable intelligence reports",
                backstory="Skilled technical writer who excels at creating executive summaries"
            ),
        ]
    
    def _create_researcher_task(self, topic: str, max_articles: int) -> dict[str, Any]:
        """Create the research task configuration.
        
        Args:
            topic: The topic to research.
            max_articles: Maximum number of articles to fetch.
            
        Returns:
            Task configuration dictionary.
        """
        return {
            "description": f"Research news articles about: {topic}",
            "expected_output": f"List of up to {max_articles} relevant articles",
            "tools": [search_news],
        }
    
    def _create_analyst_task(self, articles: list[NewsArticle]) -> dict[str, Any]:
        """Create the analysis task configuration.
        
        Args:
            articles: List of articles to analyze.
            
        Returns:
            Task configuration dictionary.
        """
        return {
            "description": "Analyze sentiment and extract key themes from articles",
            "expected_output": "Sentiment scores and topic analysis",
            "tools": [analyze_sentiment],
        }
    
    def run(
        self,
        topic: str,
        time_range: str = "24h",
        max_articles: int = 10,
    ) -> AnalysisResult:
        """Execute the news intelligence crew.
        
        Args:
            topic: The topic to analyze.
            time_range: Time range for article search (24h, 7d, 30d).
            max_articles: Maximum number of articles to process.
            
        Returns:
            Analysis result containing insights and metrics.
        """
        # Placeholder implementation - returns mock data
        # TODO: Integrate actual CrewAI execution with run_demo() pattern
        return AnalysisResult(
            article_count=max_articles,
            avg_sentiment=0.65,
            topics=[topic, "technology", "innovation"],
            insights=[
                f"Found {max_articles} articles about {topic}",
                "Overall sentiment is positive",
                "Key trend: Increasing AI adoption",
            ],
            raw_articles=[],
        )
    
    def save_report(self, result: AnalysisResult, output_path: Optional[Path] = None) -> Path:
        """Save analysis results to a report file.
        
        Args:
            result: The analysis result to save.
            output_path: Optional custom output path.
            
        Returns:
            Path to the saved report file.
        """
        if output_path is None:
            reports_dir = Path(__file__).parent.parent.parent / "reports"
            reports_dir.mkdir(exist_ok=True)
            output_path = reports_dir / "latest_report.json"
        
        output_path.write_text(result.model_dump_json(indent=2))
        return output_path


# ============================================================================
# CLI Entrypoints
# ============================================================================

def run_crew() -> None:
    """CLI entrypoint for running the crew directly (mock mode)."""
    crew = NewsIntelCrew()
    result = crew.run(topic="artificial intelligence", max_articles=10)
    print(f"Analysis complete: {result.article_count} articles analyzed")
    print(f"Insights: {result.insights}")


if __name__ == "__main__":
    # Run the CrewAI demo when executed directly
    run_demo()
