# Research Agent Guide

## Overview

The multi-agent system now supports **three research modes** for gathering information during Q&A dataset generation:

1. **RAG Mode** - Retrieval from curated knowledge base (ChromaDB or JSONL)
2. **Web Mode** - Real-time web search using search APIs
3. **Hybrid Mode** - Combines both RAG and web search

All three modes are unified in a single agent: `UnifiedResearchAgent`

---

## Quick Start

### Basic Usage

```python
from multi_agent_system import UnifiedResearchAgent

# RAG mode (default) - uses existing knowledge base
agent = UnifiedResearchAgent(research_mode="rag")

# Web search mode - uses real-time web search
agent = UnifiedResearchAgent(research_mode="web")

# Hybrid mode - uses both
agent = UnifiedResearchAgent(research_mode="hybrid")

# Research a question
result = agent.research_question(
    question="What is Bitcoin's halving mechanism?",
    subtopic="Bitcoin Fundamentals"
)

print(result['research_data']['research_notes'])
```

---

## Research Modes

### 1. RAG Mode (Default)

**Best for:**
- Using curated, high-quality knowledge
- Consistent, reliable information
- Privacy (no external API calls)
- Offline operation

**Configuration:**
```python
agent = UnifiedResearchAgent(
    research_mode="rag",
    db_path="chroma_db",                    # ChromaDB directory
    collection_name="qa_dataset",           # Collection name
    knowledge_base_path="path/to/data.jsonl",  # Or JSONL file
    max_context_examples=5                  # Number of examples to retrieve
)
```

**How it works:**
1. Searches ChromaDB or JSONL knowledge base for relevant Q&A pairs
2. Retrieves top N most relevant examples
3. Uses retrieved context to generate research notes

### 2. Web Search Mode

**Best for:**
- Current events and recent information
- Real-time market data
- Breaking news
- Topics not in knowledge base

**Configuration:**
```python
agent = UnifiedResearchAgent(
    research_mode="web",
    search_provider="auto",        # "auto", "brave", "google", "duckduckgo"
    max_search_results=5           # Number of search results
)
```

**Supported Search Providers:**
- **Brave Search API** (recommended) - Fast, privacy-focused
- **Google Custom Search API** - Comprehensive results
- **DuckDuckGo** - No API key required (uses duckduckgo-search package)

**Environment Variables:**
```bash
# .env file
BRAVE_SEARCH_API_KEY=your_brave_api_key
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

**How it works:**
1. Performs web search using configured provider
2. Retrieves top N search results
3. Synthesizes information from multiple sources
4. Cites sources in research notes

### 3. Hybrid Mode

**Best for:**
- Comprehensive research combining both sources
- Maximum information coverage
- Cross-referencing curated and real-time data

**Configuration:**
```python
agent = UnifiedResearchAgent(
    research_mode="hybrid",
    # RAG parameters
    db_path="chroma_db",
    max_context_examples=3,
    # Web parameters
    search_provider="brave",
    max_search_results=3
)
```

**How it works:**
1. Retrieves relevant examples from knowledge base (RAG)
2. Performs web search for current information
3. Combines both sources in a single context
4. Generates research notes synthesizing both

---

## Integration with Multi-Agent Orchestrator

### Update Orchestrator Config

The orchestrator can use the unified research agent:

```python
from multi_agent_system import MultiAgentOrchestrator

# Use RAG mode (default)
orchestrator = MultiAgentOrchestrator(
    config={
        "domain": "cryptocurrency",
        "research_mode": "rag"  # or "web" or "hybrid"
    }
)

# Run pipeline
orchestrator.run_full_pipeline("Bitcoin Technical Analysis")
```

### Override Research Mode Per Run

```python
# Default to RAG, but use web for specific topics
orchestrator = MultiAgentOrchestrator(
    config={"research_mode": "rag"}
)

# This will use RAG
orchestrator.run_full_pipeline("Historical Bitcoin Patterns")

# Override for current events
orchestrator.config["research_mode"] = "web"
orchestrator.run_full_pipeline("2025 Bitcoin Regulations")

# Use hybrid for comprehensive coverage
orchestrator.config["research_mode"] = "hybrid"
orchestrator.run_full_pipeline("Bitcoin Market Cycles")
```

---

## Advanced Usage

### Dynamic Mode Switching

```python
agent = UnifiedResearchAgent(research_mode="rag")

# Use RAG for most questions
result1 = agent.research_question("What is proof of work?")

# Override to web for current events
result2 = agent.research_question(
    "Latest Bitcoin ETF developments",
    override_mode="web"
)

# Use hybrid for comprehensive analysis
result3 = agent.research_question(
    "Bitcoin's role in institutional portfolios",
    override_mode="hybrid"
)
```

### Access Research Metadata

```python
result = agent.research_question("What is DeFi?")

if result['success']:
    data = result['research_data']

    print(f"Research method: {data['research_method']}")
    print(f"Research length: {data['research_length']} chars")
    print(f"Key concepts: {data['key_concepts']}")

    # RAG-specific
    if 'rag_examples_count' in data:
        print(f"RAG examples used: {data['rag_examples_count']}")

    # Web-specific
    if 'sources_count' in data:
        print(f"Web sources: {data['sources_count']}")
        for source in data.get('sources', []):
            print(f"  - {source['title']}: {source['url']}")
```

---

## Setting Up Web Search

### Option 1: Brave Search API (Recommended)

1. Sign up at https://brave.com/search/api/
2. Get API key
3. Add to `.env`:
   ```bash
   BRAVE_SEARCH_API_KEY=your_api_key_here
   ```

**Pros:**
- Fast and privacy-focused
- Good cryptocurrency coverage
- Reasonable rate limits

### Option 2: Google Custom Search

1. Create project at https://console.cloud.google.com/
2. Enable Custom Search API
3. Create custom search engine at https://programmablesearchengine.google.com/
4. Add to `.env`:
   ```bash
   GOOGLE_SEARCH_API_KEY=your_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
   ```

**Pros:**
- Comprehensive results
- Excellent for general queries

### Option 3: DuckDuckGo (No API Key)

1. Install package:
   ```bash
   pip install duckduckgo-search
   ```

2. No API key needed!

**Pros:**
- No API key required
- Privacy-focused
- Free

**Cons:**
- May have rate limiting
- Less cryptocurrency-specific results

---

## Best Practices

### When to Use Each Mode

| Use Case | Recommended Mode | Reason |
|----------|------------------|--------|
| Fundamental concepts | RAG | Curated, high-quality knowledge |
| Historical analysis | RAG | Consistent information |
| Current events | Web | Real-time information |
| Breaking news | Web | Latest updates |
| Regulatory changes | Web | Recent developments |
| Comprehensive research | Hybrid | Best of both worlds |
| Privacy-sensitive topics | RAG | No external API calls |
| Offline operation | RAG | No internet required |

### Performance Considerations

**RAG Mode:**
- Fast (local retrieval)
- No API rate limits
- Consistent performance

**Web Mode:**
- Slower (network latency)
- API rate limits apply
- Variable response time

**Hybrid Mode:**
- Slowest (both RAG + web)
- Most comprehensive
- Best for quality over speed

### Cost Considerations

**RAG Mode:**
- ✅ Free (local resources only)
- ✅ No API costs

**Web Mode:**
- 💰 Brave: $5/month for 1000 queries
- 💰 Google: $5/1000 queries
- ✅ DuckDuckGo: Free (rate limited)

**Hybrid Mode:**
- 💰 Combined costs of web search
- ✅ RAG portion is free

---

## Troubleshooting

### RAG Mode Issues

**Problem:** "No knowledge base found"
```bash
# Solution: Ensure you have either ChromaDB or JSONL data
ls chroma_db/  # Should contain ChromaDB files
# or
ls compiled_datasets/*.jsonl  # Should contain training data
```

**Problem:** "No relevant context found"
```bash
# Solution: Knowledge base might not cover the topic
# Use web mode or hybrid mode instead
agent = UnifiedResearchAgent(research_mode="web")
```

### Web Mode Issues

**Problem:** "Web search not available"
```bash
# Solution 1: Install web_search module
# Check: multi_agent_system/web_search.py exists

# Solution 2: Configure API keys in .env
echo "BRAVE_SEARCH_API_KEY=your_key" >> .env

# Solution 3: Install DuckDuckGo package
pip install duckduckgo-search
```

**Problem:** "All providers failed"
```bash
# Check API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('BRAVE_SEARCH_API_KEY'))"

# Test web search directly
python multi_agent_system/web_search.py
```

### Hybrid Mode Issues

**Problem:** Using only one source
```bash
# Check both RAG and web are available
agent = UnifiedResearchAgent(research_mode="hybrid")
print(f"RAG available: {agent.rag_available}")
print(f"Web available: {agent.web_search_available}")
```

---

## Example: Complete Workflow

```python
from multi_agent_system import MultiAgentOrchestrator

# Configure orchestrator with hybrid research
config = {
    "domain": "cryptocurrency",
    "research_mode": "hybrid",      # Use both RAG and web
    "questions_per_topic": 100,
    "max_context_examples": 3,      # RAG: 3 examples
    "max_search_results": 3,        # Web: 3 results
    "search_provider": "brave"      # Use Brave Search
}

orchestrator = MultiAgentOrchestrator(config=config)

# Generate comprehensive dataset with both sources
orchestrator.run_full_pipeline("DeFi Lending Protocols")

# Result:
# - 1000+ Q&A pairs
# - Research uses both curated knowledge + real-time web data
# - Comprehensive, up-to-date answers
```

---

## Migration Guide

### From Old ResearchAgent

**Before:**
```python
from multi_agent_system import ResearchAgent

agent = ResearchAgent()
result = agent.research_question("What is Bitcoin?")
```

**After:**
```python
from multi_agent_system import UnifiedResearchAgent

# Same behavior as before (RAG is default)
agent = UnifiedResearchAgent(research_mode="rag")
result = agent.research_question("What is Bitcoin?")

# Or explicitly use the old ResearchAgent (still available)
from multi_agent_system import ResearchAgent
agent = ResearchAgent()  # No changes needed
```

**Compatibility:**
- Old `ResearchAgent` still works
- New `UnifiedResearchAgent` provides more flexibility
- Can use both in same codebase

---

## API Reference

### UnifiedResearchAgent

```python
class UnifiedResearchAgent:
    def __init__(
        self,
        model_url: Optional[str] = None,
        domain_config: Optional[Dict] = None,
        research_mode: Literal["rag", "web", "hybrid"] = "rag",
        # RAG parameters
        knowledge_base_path: Optional[str] = None,
        db_path: str = "chroma_db",
        collection_name: str = "qa_dataset",
        max_context_examples: int = 5,
        # Web parameters
        search_provider: str = "auto",
        max_search_results: int = 5
    )

    def research_question(
        self,
        question: str,
        subtopic: Optional[str] = None,
        override_mode: Optional[Literal["rag", "web", "hybrid"]] = None
    ) -> Dict[str, Any]
```

### Research Result Structure

```python
{
    "success": True,
    "research_data": {
        "question": "What is Bitcoin?",
        "research_notes": "Comprehensive research notes...",
        "key_concepts": ["blockchain", "proof of work", ...],
        "research_length": 1234,
        "research_method": "rag" | "web" | "hybrid" | "llm_only",
        # RAG-specific
        "rag_examples_count": 5,
        # Web-specific
        "sources_count": 3,
        "sources": [
            {"title": "...", "url": "..."},
            ...
        ]
    }
}
```

---

## Summary

✅ **Single unified agent** with three research modes
✅ **Flexible configuration** via parameters
✅ **Runtime mode switching** with override_mode
✅ **Backward compatible** with existing ResearchAgent
✅ **Automatic fallback** when sources unavailable
✅ **Comprehensive metadata** in research results

Choose the mode that best fits your use case, or use hybrid for maximum coverage!
