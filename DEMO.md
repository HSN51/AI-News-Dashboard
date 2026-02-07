# 🎬 NewsIntel Demo Guide

> Step-by-step guide for demonstrating NewsIntel capabilities.

## 📋 Pre-Demo Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -e ".[dev]"`)
- [ ] Environment variables configured (`.env` file)
- [ ] Test API keys are valid
- [ ] Sample data available (optional)

## 🚀 Demo Scenarios

### Scenario 1: Basic News Search (3 minutes)

**Goal**: Show the core search and display functionality.

1. **Start the dashboard**
   ```bash
   streamlit run src/newsintel/app.py
   ```

2. **Configure search parameters**
   - Topic: "artificial intelligence"
   - Time Range: "24h"
   - Max Articles: 10

3. **Run analysis**
   - Click "🚀 Run Analysis" button
   - Wait for results to populate

4. **Highlight key features**
   - Real-time sentiment metrics
   - Topic extraction
   - Key insights summary

---

### Scenario 2: Multi-Agent Workflow (5 minutes)

**Goal**: Demonstrate the CrewAI agent orchestration.

1. **Open terminal alongside dashboard**

2. **Run crew directly**
   ```bash
   python -m newsintel.crew
   ```

3. **Explain the agent roles**
   - 🔍 **News Researcher**: Finds relevant articles
   - 📊 **Content Analyst**: Analyzes sentiment and trends
   - 📝 **Report Writer**: Synthesizes findings

4. **Show report output**
   ```bash
   cat reports/latest_report.json
   ```

---

### Scenario 3: Custom Analysis (5 minutes)

**Goal**: Show flexibility and customization.

1. **Using as a Python library**
   ```python
   from newsintel.crew import NewsIntelCrew
   from newsintel.schemas import AnalysisResult
   
   crew = NewsIntelCrew()
   
   # Custom topic analysis
   result = crew.run(
       topic="large language models",
       time_range="7d",
       max_articles=20,
   )
   
   print(f"Analyzed {result.article_count} articles")
   print(f"Average sentiment: {result.avg_sentiment:.2f}")
   
   for insight in result.insights:
       print(f"• {insight}")
   ```

2. **Show schema validation**
   ```python
   from newsintel.schemas import NewsArticle
   
   # Validation in action
   article = NewsArticle(
       title="Demo Article",
       source="Demo Source",
       tags=["ai", "demo"],
   )
   
   print(article.model_dump_json(indent=2))
   ```

---

## 🎯 Key Talking Points

### Architecture Highlights

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Streamlit | Interactive dashboard |
| Agents | CrewAI | Multi-agent orchestration |
| Data Models | Pydantic | Type-safe validation |
| Config | YAML | Flexible source configuration |

### Value Propositions

1. **Time Savings**: Automate news monitoring and analysis
2. **Insights**: Surface trends across multiple sources
3. **Customizable**: Easy to add new sources and agents
4. **Extensible**: Clean architecture for future enhancements

---

## 📸 Screenshots to Capture

1. Dashboard overview with analysis results
2. Sidebar configuration panel
3. Terminal output showing agent execution
4. Generated JSON report

---

## ❓ Anticipated Questions

**Q: How long does analysis take?**
> A: Typically 10-30 seconds depending on article count and API response times.

**Q: Can I add my own news sources?**
> A: Yes! Edit `config/sources.yaml` and implement the corresponding adapter.

**Q: Does it work offline?**
> A: Currently requires internet for news APIs. Offline mode is on the roadmap.

**Q: What LLM does it use?**
> A: Configurable - supports OpenAI, local models via Ollama, and more.

---

## 🔄 Post-Demo Actions

- [ ] Share repository link
- [ ] Provide sample `.env.example`
- [ ] Schedule follow-up for questions
- [ ] Collect feedback

---

## 📞 Support

For demo issues, check:
- Console logs for API errors
- `.env` file for missing keys
- `reports/` folder permissions

Contact: your.email@example.com
