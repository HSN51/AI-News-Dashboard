"""
Streamlit application entrypoint for NewsIntel dashboard.

Run with: streamlit run src/newsintel/app.py
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional
from enum import Enum

import streamlit as st


# ============================================================================
# Configuration & Constants
# ============================================================================

class RunMode(str, Enum):
    """Available run modes for the application."""
    CLASSIC = "Classic"
    AGENT = "Agent (CrewAI)"


SUPPORTED_LANGUAGES = {
    "en": "🇺🇸 English",
    "tr": "🇹🇷 Türkçe",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
}

SAMPLE_TOPICS = [
    "artificial intelligence",
    "machine learning",
    "large language models",
    "robotics",
    "autonomous vehicles",
    "quantum computing",
]


# ============================================================================
# Custom CSS for Professional Styling
# ============================================================================

def inject_custom_css() -> None:
    """Inject custom CSS for enhanced visual appearance."""
    st.markdown("""
    <style>
        /* ═══════════════════════════════════════════════════════════════
           GLOBAL STYLES
           ═══════════════════════════════════════════════════════════════ */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* ═══════════════════════════════════════════════════════════════
           SIDEBAR STYLING
           ═══════════════════════════════════════════════════════════════ */
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #0f172a 100%);
            border-right: 1px solid rgba(99, 102, 241, 0.2);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }
        
        /* Sidebar ALL text white */
        [data-testid="stSidebar"] h1 {
            color: #c7d2fe !important;
            font-weight: 700;
        }
        
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #e0e7ff !important;
            font-weight: 600;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] em {
            color: #e0e7ff !important;
        }
        
        /* Sidebar inputs */
        [data-testid="stSidebar"] .stTextInput > div > div {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 8px;
        }
        
        [data-testid="stSidebar"] .stTextInput input {
            color: #ffffff !important;
        }
        
        /* Sidebar selectbox */
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 8px;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox span {
            color: #ffffff !important;
        }
        
        /* Sidebar slider */
        [data-testid="stSidebar"] .stSlider > div > div > div {
            background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        }
        
        [data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] .stSlider p {
            color: #ffffff !important;
        }
        
        /* Sidebar radio buttons */
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stRadio p,
        [data-testid="stSidebar"] .stRadio span {
            color: #ffffff !important;
        }

        /* Sidebar checkbox */
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stCheckbox p,
        [data-testid="stSidebar"] .stCheckbox span {
            color: #ffffff !important;
        }
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.5);
            border-radius: 6px;
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.5) 0%, rgba(139, 92, 246, 0.5) 100%);
            border-color: #a5b4fc;
            transform: translateY(-1px);
        }
        
        /* Primary button */
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: none;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }
        
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
            transform: translateY(-2px);
        }
        
        /* Sidebar divider */
        [data-testid="stSidebar"] hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.4), transparent);
            margin: 1.5rem 0;
        }
        
        /* Sidebar expander */
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 8px;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] .streamlit-expanderHeader p {
            color: #ffffff !important;
        }
        
        /* ═══════════════════════════════════════════════════════════════
           MAIN CONTENT AREA
           ═══════════════════════════════════════════════════════════════ */
        
        .main {
            background: linear-gradient(180deg, #0a0a0f 0%, #111827 100%);
        }
        
        /* ALL main area text white */
        .main p, .main span, .main label, .main li {
            color: #f1f5f9 !important;
        }
        
        .main h1, .main h2, .main h3, .main h4 {
            color: #ffffff !important;
        }
        
        /* Custom header */
        .main-header {
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            color: #e2e8f0 !important;
            font-size: 1.15rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        [data-testid="stMetricLabel"] {
            color: #ffffff !important;
            font-weight: 500;
        }
        
        [data-testid="stMetricLabel"] p {
            color: #ffffff !important;
        }
        
        [data-testid="stMetricDelta"] {
            color: #4ade80 !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(30, 41, 59, 0.6);
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #e2e8f0 !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        
        .stTabs [data-baseweb="tab"] span {
            color: #e2e8f0 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        }
        
        .stTabs [aria-selected="true"] span {
            color: white !important;
        }
        
        /* Expander styling - Articles & Insights */
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 10px;
            color: #ffffff !important;
        }
        
        .streamlit-expanderHeader p,
        .streamlit-expanderHeader span {
            color: #ffffff !important;
            font-weight: 500;
        }
        
        .streamlit-expanderContent {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-top: none;
            border-radius: 0 0 10px 10px;
            padding: 1rem;
        }
        
        .streamlit-expanderContent p,
        .streamlit-expanderContent span,
        .streamlit-expanderContent strong {
            color: #f1f5f9 !important;
        }
        
        /* Success/Info/Warning messages */
        .stSuccess {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
            border: 1px solid rgba(34, 197, 94, 0.4);
            border-radius: 10px;
        }
        
        .stSuccess p {
            color: #4ade80 !important;
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 10px;
        }
        
        .stInfo p {
            color: #a5b4fc !important;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(245, 158, 11, 0.15) 100%);
            border: 1px solid rgba(251, 191, 36, 0.4);
            border-radius: 10px;
        }
        
        .stWarning p {
            color: #fcd34d !important;
        }
        
        /* Link buttons */
        .stLinkButton > a {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            text-decoration: none;
        }
        
        /* Markdown content */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffffff !important;
        }
        
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #f1f5f9 !important;
        }
        
        .stMarkdown strong {
            color: #ffffff !important;
        }
        
        .stMarkdown a {
            color: #a5b4fc !important;
        }
        
        /* Dividers */
        .main hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.4), transparent);
            margin: 2rem 0;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        }
        
        /* Code blocks */
        code {
            color: #c084fc !important;
            background: rgba(99, 102, 241, 0.2) !important;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# Page Configuration
# ============================================================================

def setup_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="NewsIntel - AI News Dashboard",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()


# ============================================================================
# Sidebar Components
# ============================================================================

def render_sidebar() -> dict:
    """Render sidebar with configuration options.
    
    Returns:
        Dictionary containing user configuration selections.
    """
    with st.sidebar:
        # Logo & Title
        st.markdown("# 📰 NewsIntel")
        st.markdown("*AI-Powered News Intelligence*")
        st.divider()
        
        # ── Configuration Section ──
        st.markdown("### ⚙️ Configuration")
        
        # Topic Input
        topic = st.text_input(
            "🔍 Topic",
            value="artificial intelligence",
            help="Enter the news topic to analyze",
            placeholder="e.g., machine learning, robotics..."
        )
        
        # Quick topic suggestions
        st.markdown("**Quick Topics:**")
        cols = st.columns(3)
        for i, sample_topic in enumerate(SAMPLE_TOPICS[:6]):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(sample_topic.split()[0].capitalize(), key=f"topic_{i}", use_container_width=True):
                    st.session_state["selected_topic"] = sample_topic
        
        # Use selected topic if clicked
        if "selected_topic" in st.session_state:
            topic = st.session_state["selected_topic"]
        
        st.divider()
        
        # Language Selection
        language = st.selectbox(
            "🌐 Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            help="Select output language"
        )
        
        # Max Articles
        max_articles = st.slider(
            "📊 Max Articles",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="Maximum number of articles to analyze"
        )
        
        # Run Mode
        mode = st.radio(
            "🤖 Run Mode",
            options=[RunMode.CLASSIC.value, RunMode.AGENT.value],
            help="Classic: Fast mock analysis\nAgent: Full CrewAI pipeline"
        )
        
        st.divider()
        
        # ── Advanced Settings ──
        with st.expander("🔧 Advanced Settings"):
            time_range = st.selectbox(
                "Time Range",
                options=["24h", "7d", "30d"],
                help="Search time range for articles"
            )
            
            include_sentiment = st.checkbox(
                "Include Sentiment Analysis",
                value=True
            )
            
            include_topics = st.checkbox(
                "Extract Key Topics",
                value=True
            )
        
        st.divider()
        
        # ── Run Button ──
        run_clicked = st.button(
            "🚀 Run Analysis",
            type="primary",
            use_container_width=True
        )
        
        # Footer
        st.divider()
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.8rem;'>
                <p>NewsIntel v0.1.0</p>
                <p>Powered by CrewAI + Streamlit</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        return {
            "topic": topic,
            "language": language,
            "max_articles": max_articles,
            "mode": mode,
            "time_range": time_range if 'time_range' in dir() else "24h",
            "include_sentiment": include_sentiment if 'include_sentiment' in dir() else True,
            "include_topics": include_topics if 'include_topics' in dir() else True,
            "run_clicked": run_clicked,
        }


# ============================================================================
# Main Panel Components
# ============================================================================

def render_header() -> None:
    """Render the main header section."""
    st.markdown('<h1 class="main-header">NewsIntel Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">AI-powered news intelligence — Collect, analyze, and summarize the latest news using CrewAI agents.</p>',
        unsafe_allow_html=True
    )


def render_status_bar(status: str, details: Optional[str] = None) -> None:
    """Render a status notification bar.
    
    Args:
        status: Current status message.
        details: Optional additional details.
    """
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.metric("Status", status)
    with col2:
        if details:
            st.info(details)
    with col3:
        st.metric("Last Run", datetime.now().strftime("%H:%M:%S"))


def render_metrics(result: dict) -> None:
    """Render analysis metrics in cards.
    
    Args:
        result: Analysis result dictionary.
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📰 Articles Analyzed",
            result.get("article_count", 0),
            delta=None
        )
    
    with col2:
        sentiment = result.get("avg_sentiment", 0)
        sentiment_label = "Positive" if sentiment > 0.3 else "Negative" if sentiment < -0.3 else "Neutral"
        st.metric(
            "😊 Sentiment",
            sentiment_label,
            delta=f"{sentiment:.2f}"
        )
    
    with col3:
        st.metric(
            "🏷️ Topics Found",
            len(result.get("topics", []))
        )
    
    with col4:
        st.metric(
            "💡 Insights",
            len(result.get("insights", []))
        )


def render_output(result: dict) -> None:
    """Render the analysis output in markdown format.
    
    Args:
        result: Analysis result dictionary.
    """
    st.markdown("## 📊 Analysis Results")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 Summary", "📰 Articles", "📈 Insights"])
    
    with tab1:
        st.markdown("### Executive Summary")
        st.markdown(result.get("summary", "No summary available."))
        
        if result.get("topics"):
            st.markdown("### 🏷️ Key Topics")
            topic_cols = st.columns(len(result["topics"][:5]))
            for i, topic in enumerate(result["topics"][:5]):
                with topic_cols[i]:
                    st.markdown(f"<span style='background: linear-gradient(90deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem;'>{topic}</span>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📰 Analyzed Articles")
        if result.get("articles"):
            for i, article in enumerate(result["articles"][:5], 1):
                with st.expander(f"{i}. {article['title']}", expanded=i==1):
                    st.markdown(f"**Source:** {article['source']}")
                    st.markdown(f"**Published:** {article['published_at']}")
                    st.markdown(article['summary'])
                    if article.get('url'):
                        st.link_button("Read Full Article →", article['url'])
        else:
            st.info("No articles to display. Run an analysis to see results.")
    
    with tab3:
        st.markdown("### 💡 Key Insights")
        if result.get("insights"):
            for insight in result["insights"]:
                st.markdown(f"- {insight}")
        else:
            st.info("No insights available yet.")


# ============================================================================
# Mock Data & Analysis Functions
# ============================================================================

def run_mock_analysis(config: dict) -> dict:
    """Run a mock analysis (placeholder for real implementation).
    
    Args:
        config: Configuration dictionary.
        
    Returns:
        Mock analysis results.
    """
    topic = config["topic"]
    max_articles = config["max_articles"]
    
    # Simulate processing time
    progress_bar = st.progress(0, text="Initializing analysis...")
    
    steps = [
        (20, "🔍 Searching news sources..."),
        (40, "📥 Fetching articles..."),
        (60, "🧠 Analyzing content..."),
        (80, "📊 Generating insights..."),
        (100, "✅ Completing analysis..."),
    ]
    
    for progress, text in steps:
        time.sleep(0.3)  # Simulate work
        progress_bar.progress(progress, text=text)
    
    progress_bar.empty()
    
    # Return mock data
    return {
        "article_count": max_articles,
        "avg_sentiment": 0.65,
        "topics": [topic.title(), "Technology", "Innovation", "Future", "Research"],
        "insights": [
            f"🚀 Strong momentum in {topic} sector with 15% growth in coverage",
            "📈 Positive sentiment dominates (65%) across analyzed sources",
            "🔬 Research and development focus increasing in enterprise applications",
            "🌍 Global adoption accelerating, especially in Asia-Pacific region",
            "💼 Major tech companies announcing significant investments",
        ],
        "summary": f"""
## {topic.title()} - Market Intelligence Report

Based on analysis of **{max_articles} articles** from the past 24 hours, here are the key findings:

### Market Overview
The {topic} sector continues to show strong growth momentum, with increased media coverage 
and positive sentiment across major news outlets. Enterprise adoption is accelerating, 
particularly in automation and efficiency optimization use cases.

### Key Trends
1. **Increased Investment** - Major players announcing multi-billion dollar commitments
2. **Regulatory Attention** - Governments worldwide developing frameworks
3. **Talent Demand** - 40% year-over-year increase in job postings
4. **Open Source Growth** - Community-driven projects gaining significant traction

### Outlook
The sector is expected to maintain its growth trajectory, with particular emphasis on 
responsible development and deployment practices.
        """,
        "articles": [
            {
                "title": f"Breaking: Major Advances in {topic.title()}",
                "source": "TechCrunch",
                "published_at": "2 hours ago",
                "summary": f"New developments in {topic} are reshaping the industry landscape...",
                "url": "https://techcrunch.com"
            },
            {
                "title": f"How {topic.title()} is Transforming Business",
                "source": "Forbes",
                "published_at": "5 hours ago", 
                "summary": f"Enterprise adoption of {topic} solutions continues to accelerate...",
                "url": "https://forbes.com"
            },
            {
                "title": f"The Future of {topic.title()}: Expert Analysis",
                "source": "Wired",
                "published_at": "8 hours ago",
                "summary": f"Industry experts weigh in on the trajectory of {topic} development...",
                "url": "https://wired.com"
            },
        ]
    }


def run_agent_analysis(config: dict) -> dict:
    """Run CrewAI agent-based analysis.
    
    Args:
        config: Configuration dictionary.
        
    Returns:
        Analysis results from CrewAI agents.
    """
    # TODO: Integrate with actual CrewAI crew
    # from newsintel.crew import NewsIntelCrew, run_demo
    # crew = NewsIntelCrew()
    # result = crew.run(topic=config["topic"], max_articles=config["max_articles"])
    
    st.warning("🤖 Agent mode will use CrewAI. Using mock data for now.")
    return run_mock_analysis(config)


# ============================================================================
# Main Application
# ============================================================================

def main() -> None:
    """Main application entrypoint."""
    setup_page_config()
    
    # Initialize session state
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "analysis_status" not in st.session_state:
        st.session_state["analysis_status"] = "Ready"
    
    # Render sidebar and get config
    config = render_sidebar()
    
    # Main content area
    render_header()
    
    # Status section
    st.markdown("---")
    
    # Handle Run button
    if config["run_clicked"]:
        st.session_state["analysis_status"] = "Running"
        
        with st.spinner(""):
            if config["mode"] == RunMode.AGENT.value:
                result = run_agent_analysis(config)
            else:
                result = run_mock_analysis(config)
            
            st.session_state["analysis_result"] = result
            st.session_state["analysis_status"] = "Complete"
        
        st.success("✅ Analysis completed successfully!")
    
    # Display results
    if st.session_state["analysis_result"]:
        render_metrics(st.session_state["analysis_result"])
        st.markdown("---")
        render_output(st.session_state["analysis_result"])
    else:
        # Welcome state
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 20px; margin: 2rem 0; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);'>
                    <h2 style='background: linear-gradient(135deg, #818cf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem; font-size: 1.8rem;'>👋 Welcome to NewsIntel</h2>
                    <p style='color: #9ca3af; font-size: 1.1rem; margin-bottom: 1.5rem; line-height: 1.6;'>
                        Configure your analysis parameters in the sidebar and click 
                        <strong style='background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Run Analysis</strong> to get started.
                    </p>
                    <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2.5rem;'>
                        <div style='text-align: center; padding: 1rem;'>
                            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📰</div>
                            <p style='color: #a5b4fc; margin: 0; font-weight: 500;'>Multi-Source</p>
                            <p style='color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;'>News Aggregation</p>
                        </div>
                        <div style='text-align: center; padding: 1rem;'>
                            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🤖</div>
                            <p style='color: #a5b4fc; margin: 0; font-weight: 500;'>AI-Powered</p>
                            <p style='color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;'>CrewAI Agents</p>
                        </div>
                        <div style='text-align: center; padding: 1rem;'>
                            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊</div>
                            <p style='color: #a5b4fc; margin: 0; font-weight: 500;'>Deep Insights</p>
                            <p style='color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;'>Sentiment & Topics</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
