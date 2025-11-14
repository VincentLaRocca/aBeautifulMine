# Research Agent - How It Works

## Current Implementation

The `ResearchAgent` in your multi-agent system performs **LLM-based research** - it uses your Mixtral model to synthesize research notes based on the question.

### How It Works (Step by Step)

1. **Receives a Question**
   - The orchestrator passes a question from Step 2 (question generation)

2. **LLM Research Prompt**
   - Sends the question to Mixtral with a research-focused system prompt
   - Asks the LLM to act as an expert researcher
   - Temperature: 0.3 (lower = more factual, less creative)

3. **Research Synthesis**
   - LLM generates structured research notes covering:
     - Key concepts and terminology
     - Main points from authoritative sources
     - Practical examples (crypto-specific)
     - Different perspectives
     - Risks and limitations
     - Areas needing deeper investigation

4. **Extract Key Concepts**
   - Parses the research notes to extract key concepts
   - Uses regex patterns to find:
     - Terms in quotes
     - Concepts after "concept:" or "term:"
     - Capitalized technical terms

5. **Returns Research Data**
   ```python
   {
       "question": "What is RSI?",
       "research_notes": "...structured research notes...",
       "key_concepts": ["RSI", "Relative Strength Index", "momentum", ...],
       "research_length": 1234
   }
   ```

6. **Passes to Answer Generator**
   - Research data is passed to Step 4 (answer generation)
   - Answer generator uses research context to create comprehensive answers

## Current Limitations

⚠️ **Important**: The current implementation does **NOT** perform actual web searches. It relies on:
- LLM's training data (Mixtral's knowledge)
- LLM's ability to synthesize information
- LLM's understanding of authoritative sources

### Why This Works (But Could Be Better)

**Works because:**
- Mixtral has extensive training data on crypto/trading topics
- LLM can synthesize information logically
- Provides structured context for answer generation

**Could be better with:**
- Actual web search integration
- Real-time data fetching
- Multiple source verification

## Enhanced Version (With Web Search)

I noticed you have a `research_answer_agent.py` that includes web search capabilities. Here's how you could enhance the research agent:

### Option 1: Add DuckDuckGo Search

```python
import requests

def search_web(self, query: str, num_results: int = 5):
    """Search web using DuckDuckGo API"""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    results = []
    if data.get("Abstract"):
        results.append({
            "title": data.get("Heading", ""),
            "snippet": data.get("Abstract", ""),
            "url": data.get("AbstractURL", "")
        })
    
    return results
```

### Option 2: Use Your Existing Research Tools

You have `research_answer_agent.py` with web search. You could:
1. Integrate it into the multi-agent system
2. Use it to fetch real web results
3. Combine web results with LLM synthesis

## How Research Data Flows

```
Question Generator (Step 2)
    ↓
    [100 questions]
    ↓
Research Agent (Step 3)
    ↓
    For each question:
    - Generate research notes (LLM)
    - Extract key concepts
    - Return research_data
    ↓
    [Research results dictionary]
    ↓
Answer Generator (Step 4)
    ↓
    Uses research_context to:
    - Enhance answer quality
    - Add specific examples
    - Include key concepts
    ↓
    [Comprehensive answers]
```

## Research Agent Code Flow

```python
# 1. Initialize
research_agent = ResearchAgent(model_url="http://localhost:8080/v1")

# 2. Research a question
result = research_agent.research_question("What is RSI?")

# 3. Returns:
{
    "success": True,
    "research_data": {
        "question": "What is RSI?",
        "research_notes": "RSI (Relative Strength Index) is a momentum oscillator...",
        "key_concepts": ["RSI", "momentum", "oscillator", ...],
        "research_length": 1500
    }
}

# 4. Used by answer generator
answer_agent.generate_answer(
    question="What is RSI?",
    research_context=result["research_data"]
)
```

## Configuration

The research agent uses:
- **Model**: Mixtral (via your llama.cpp server)
- **Temperature**: 0.3 (factual, deterministic)
- **Max Tokens**: 2048 (research notes length)
- **System Prompt**: Expert researcher persona
- **User Prompt**: Structured research request

## Enhancing the Research Agent

### Quick Enhancement: Add Web Search

You could modify `research_agent.py` to:

1. **Generate search queries** from the question
2. **Perform web searches** (DuckDuckGo, Google, etc.)
3. **Synthesize web results** with LLM
4. **Combine** web data + LLM knowledge

### Example Enhancement

```python
def research_question(self, question: str) -> Dict[str, Any]:
    # 1. Generate search queries
    search_queries = self._generate_search_queries(question)
    
    # 2. Perform web searches
    web_results = []
    for query in search_queries:
        results = self._search_web(query)
        web_results.extend(results)
    
    # 3. Synthesize with LLM
    research_prompt = f"""
    Question: {question}
    
    Web Search Results:
    {self._format_web_results(web_results)}
    
    Synthesize this information into structured research notes...
    """
    
    # 4. Continue with LLM synthesis...
```

## Current vs Enhanced

| Feature | Current | Enhanced (Possible) |
|---------|---------|---------------------|
| **Web Search** | ❌ No | ✅ Yes (DuckDuckGo/Google) |
| **Real-time Data** | ❌ No | ✅ Yes |
| **Source Verification** | ❌ LLM only | ✅ Multiple sources |
| **Speed** | ✅ Fast | ⚠️ Slower (API calls) |
| **Cost** | ✅ Free (local) | ⚠️ May need API keys |
| **Reliability** | ✅ Always works | ⚠️ Depends on APIs |

## Recommendation

**For now**: The current LLM-based research works well because:
- Mixtral has good crypto/trading knowledge
- Fast and reliable
- No external dependencies
- Good enough for training data generation

**For production**: Consider adding web search if you need:
- Real-time data
- Latest developments
- Multiple source verification
- Higher accuracy requirements

## Summary

The research agent:
1. ✅ Uses LLM to synthesize research notes
2. ✅ Extracts key concepts automatically
3. ✅ Provides structured context for answer generation
4. ⚠️ Relies on LLM training data (no web search currently)
5. ✅ Works well for your use case (training data generation)

The research data enhances answer quality by providing:
- Structured context
- Key concepts to emphasize
- Research notes for the answer generator to reference

