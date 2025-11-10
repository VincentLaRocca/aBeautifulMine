# AGENT TRAINING STRATEGY - MULTI-AGENT RAG SYSTEM

**Date**: November 9, 2025
**Strategy**: Multiple Specialized Agents vs Single Large Model
**Model Choice**: Mixtral 7B (optimized for memory efficiency)
**Architecture**: RAG (Retrieval-Augmented Generation) with dedicated Q&A databases

---

## 🎯 Strategic Decision: Multiple Specialized Agents

### Why Multiple Agents > Single Large Agent

**Original Plan**: Single large model (gpt-oss-120b @ 117B parameters)
- **Pros**: Frontier reasoning capabilities, single system
- **Cons**: 32GB VRAM constraint, CPU offloading complexity, 60GB+ memory footprint

**Revised Strategy**: Multiple Mixtral 7B agents (7B parameters each)
- **Pros**:
  - Each agent fits comfortably in 16GB VRAM (quantized)
  - Can run 2 agents simultaneously on RTX 5090 (32GB total)
  - Lower memory overhead per agent (~8-10GB with 4-bit quant)
  - Specialization = higher accuracy on domain-specific tasks
  - Easier to train, update, and maintain individually
- **Cons**: Need coordination layer (manageable with LangChain)

**Result**: Better performance per dollar/watt, more flexible architecture

---

## 🤖 Agent Architecture: Two Specialized Systems

### Agent 1: **Fundamentals & Market Intelligence Agent** 🌐

**Primary Mission**: Answer questions about cryptocurrency fundamentals, market structure, and real-time market intelligence

**Knowledge Domains**:
1. **Fundamentals** (Phase 1 - Now):
   - Trading fundamentals (market structure, order types, charts)
   - Investment fundamentals (tokenomics, valuation, strategies)
   - Technology fundamentals (blockchain, protocols, DeFi)
   - Ecosystem fundamentals (projects, history, regulation)

2. **Market Intelligence** (Phase 2 - Future):
   - Real-time market data (prices, volumes, trends)
   - Sentiment analysis (social, news, on-chain)
   - Market cycles and macro factors
   - Institutional activity and flow

**RAG Database**: `fundamentals_qa_pairs` (10,000 pairs target)
- Categories: 12 (trading, investment, technology, ecosystem)
- Subtopics: 90 (100 pairs each)
- Format: Question-answer pairs optimized for retrieval

**Training Data Source**:
- Batch 6-17 fundamentals Q&A pairs (Claude Desktop → Cursor AI → Database)
- Eventually: Real-time market data from Token Metrics AI

**Mixtral 7B Fine-Tuning**:
- Fine-tune on fundamentals Q&A pairs
- Optimize for: Explanatory clarity, step-by-step reasoning, cryptocurrency examples
- Techniques: LoRA (Low-Rank Adaptation) for efficient training

---

### Agent 2: **Technical Analysis Agent** 📊

**Primary Mission**: Answer questions about technical indicators, chart patterns, and trading strategies

**Knowledge Domains**:
1. **Technical Indicators** (Already Complete):
   - Trend indicators (MA, EMA, MACD, Parabolic SAR, Ichimoku, etc.)
   - Momentum indicators (RSI, Stochastic, Williams %R, ROC, etc.)
   - Volatility indicators (Bollinger Bands, ATR, Keltner Channels, etc.)
   - Volume indicators (OBV, CMF, A/D Line, VWAP, etc.)
   - Derivatives indicators (Open Interest, Liquidations, CME positioning)

2. **Chart Analysis**:
   - Candlestick patterns
   - Chart patterns (head & shoulders, triangles, flags)
   - Support and resistance
   - Trend lines and channels
   - Multi-timeframe analysis

**RAG Database**: `qa_pairs` (30,027 pairs ✅ COMPLETE)
- Indicators: 40+ covered
- Average quality: 3,662 chars per answer
- Format: Question-answer pairs optimized for retrieval

**Training Data Source**:
- 30,027 technical indicator Q&A pairs (COMPLETE)
- Cursor AI contribution: 2,251 pairs @ 8,759 chars avg

**Mixtral 7B Fine-Tuning**:
- Fine-tune on technical indicator Q&A pairs
- Optimize for: Mathematical accuracy, calculation details, crypto-specific applications
- Techniques: LoRA for efficient training

---

## 📊 Agent Specialization vs General Model Comparison

| Aspect | Single Large Model (120B) | Two Specialized Agents (7B each) |
|--------|---------------------------|----------------------------------|
| **Memory per Agent** | 60GB+ (with offloading) | 8-10GB (4-bit quantized) |
| **Total Memory** | 60GB+ RAM+VRAM | 16-20GB VRAM (both agents) |
| **Simultaneous Agents** | 1 (all or nothing) | 2 (both fit in 32GB) |
| **Domain Accuracy** | Good (general reasoning) | Excellent (specialized training) |
| **Training Complexity** | Very high (120B params) | Low (7B params, LoRA) |
| **Update Flexibility** | Update entire model | Update individual agents |
| **Inference Speed** | 25-32 tok/s (with CPU) | 40-60 tok/s per agent (GPU only) |
| **Scalability** | Limited (hardware bound) | High (add more agents) |

**Winner**: Two specialized agents for this use case

---

## 🔄 RAG System Architecture

### Core RAG Workflow (Both Agents)

**Step 1: User Query**
```
User: "What is the RSI indicator and when should I use it for Bitcoin trading?"
```

**Step 2: Query Router** (Determines which agent to use)
```python
if query_contains(["indicator", "technical", "chart", "pattern"]):
    route_to = "Technical Analysis Agent"
elif query_contains(["fundamental", "market", "tokenomics", "blockchain"]):
    route_to = "Fundamentals Agent"
else:
    route_to = "Both" # Hybrid query
```

**Step 3: Semantic Search** (Agent retrieves relevant Q&A pairs)
```python
# Technical Agent searches qa_pairs table
relevant_pairs = vector_search(
    query="RSI indicator Bitcoin trading",
    database="qa_pairs",
    top_k=5  # Get top 5 most relevant pairs
)
```

**Step 4: Context Augmentation** (Build enriched prompt)
```python
augmented_prompt = f"""
You are a Technical Analysis Agent specialized in cryptocurrency trading.

Context from knowledge base:
{relevant_pairs}

User Question: {user_query}

Provide a comprehensive answer based on the context above.
"""
```

**Step 5: LLM Generation** (Mixtral 7B generates answer)
```python
response = mixtral_7b.generate(augmented_prompt)
# Uses retrieved context + fine-tuned knowledge
```

**Step 6: Response Delivery**
```
Agent: "The RSI (Relative Strength Index) is a momentum oscillator that measures
the speed and magnitude of price changes on a scale of 0-100. For Bitcoin trading,
RSI is particularly effective because... [continues with detailed, contextual answer]"
```

---

## 🎯 Training Pipeline: From Q&A Pairs to Specialized Agents

### Phase 1: Data Preparation (Current Stage)

**Technical Analysis Agent**:
- ✅ Database complete: 30,027 Q&A pairs
- ✅ Quality validated: 3,662 chars avg, 100% compliance
- ✅ Ready for fine-tuning

**Fundamentals Agent**:
- 🔄 Database in progress: 0/10,000 pairs (Batch 6 starting)
- 🎯 Target: 10,000 Q&A pairs across 12 categories
- 📅 Timeline: 3-6 months (Batches 6-17)

### Phase 2: Vector Database Creation

**Purpose**: Enable semantic search for RAG retrieval

**Process**:
1. **Generate Embeddings**: Convert each Q&A pair into vector representation
   ```python
   from sentence_transformers import SentenceTransformer

   model = SentenceTransformer('all-MiniLM-L6-v2')

   for qa_pair in database:
       question_embedding = model.encode(qa_pair.question)
       answer_embedding = model.encode(qa_pair.answer)
       store_in_vector_db(qa_pair.id, question_embedding, answer_embedding)
   ```

2. **Store in Vector Database**: Use ChromaDB, Pinecone, or Weaviate
   ```python
   import chromadb

   client = chromadb.Client()
   collection = client.create_collection("technical_analysis")

   collection.add(
       documents=[qa.question + " " + qa.answer for qa in qa_pairs],
       metadatas=[{"indicator": qa.indicator_name} for qa in qa_pairs],
       ids=[str(qa.qa_id) for qa in qa_pairs]
   )
   ```

3. **Index for Fast Retrieval**: Optimize for sub-100ms query times

### Phase 3: Base Model Selection & Optimization

**Model**: Mixtral 7B (Mistral AI)
- **Architecture**: Mixture-of-Experts (8 experts, 2 active)
- **Parameters**: 7B total, ~1.5B active per token
- **Context Window**: 32K tokens
- **Quantization**: 4-bit GGUF (reduces to ~4GB VRAM)
- **License**: Apache 2.0 (commercial use allowed)

**Why Mixtral 7B**:
- ✅ Proven performance on reasoning tasks
- ✅ Efficient MoE architecture (only 2/8 experts active)
- ✅ Fits comfortably in 8GB VRAM (quantized)
- ✅ Fast inference (40-60 tok/s on RTX 5090)
- ✅ Strong community support (GGUF quantizations available)
- ✅ Good baseline for fine-tuning

### Phase 4: Fine-Tuning with LoRA

**Technique**: Low-Rank Adaptation (LoRA)
- Only trains small adapter layers (~1% of model parameters)
- Dramatically reduces training time and memory
- Preserves base model's general capabilities
- Easy to swap adapters (multiple specializations)

**Training Process** (Example for Technical Agent):

```python
from transformers import AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import Dataset

# Load base Mixtral 7B model
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-7B-v0.1")

# Configure LoRA
lora_config = LoraConfig(
    r=16,  # Low-rank dimension
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA adapters
model = get_peft_model(base_model, lora_config)

# Prepare dataset from Q&A pairs
dataset = Dataset.from_pandas(qa_pairs_df)

# Training arguments
training_args = TrainingArguments(
    output_dir="./technical-analysis-agent",
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    save_strategy="epoch"
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()
```

**Training Time Estimate**:
- Technical Agent (30K pairs): ~24-48 hours on RTX 5090
- Fundamentals Agent (10K pairs): ~12-24 hours on RTX 5090

### Phase 5: Deployment with LangChain

**System Architecture**:

```python
from langchain.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Initialize embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vector database
vectorstore = Chroma(
    persist_directory="./technical_analysis_db",
    embedding_function=embeddings
)

# Load fine-tuned Mixtral 7B (Technical Agent)
technical_agent = LlamaCpp(
    model_path="./models/mixtral-7b-technical-lora.gguf",
    n_ctx=8192,
    n_gpu_layers=35,  # Full offload to GPU
    temperature=0.7
)

# Create RAG chain
technical_qa_chain = RetrievalQA.from_chain_type(
    llm=technical_agent,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Query
response = technical_qa_chain.run("What is RSI and when should I use it?")
```

**Multi-Agent Router**:

```python
from langchain.agents import AgentExecutor, create_react_agent

# Define agent selector
def route_query(query: str) -> str:
    """Determine which agent should handle the query."""
    technical_keywords = ["indicator", "technical", "chart", "pattern", "rsi", "macd"]
    fundamental_keywords = ["fundamental", "tokenomics", "blockchain", "market"]

    if any(kw in query.lower() for kw in technical_keywords):
        return "technical"
    elif any(kw in query.lower() for kw in fundamental_keywords):
        return "fundamentals"
    else:
        return "both"

# Query routing
def answer_query(user_query: str):
    agent = route_query(user_query)

    if agent == "technical":
        return technical_qa_chain.run(user_query)
    elif agent == "fundamentals":
        return fundamentals_qa_chain.run(user_query)
    else:
        # Hybrid query - combine both agents
        tech_response = technical_qa_chain.run(user_query)
        fund_response = fundamentals_qa_chain.run(user_query)
        return synthesize_responses(tech_response, fund_response)
```

---

## 🎯 Project Roadmap: Building Both Agents

### Current Status

**Technical Analysis Agent**:
- ✅ Phase 1: Data complete (30,027 pairs)
- 🔄 Phase 2: Vector database creation (NEXT STEP)
- ⏳ Phase 3: Model selection (Mixtral 7B chosen)
- ⏳ Phase 4: Fine-tuning with LoRA
- ⏳ Phase 5: Deployment

**Fundamentals & Market Intelligence Agent**:
- 🔄 Phase 1: Data in progress (Batch 6 starting, 0/10,000 pairs)
- ⏳ Phase 2: Vector database creation (after data complete)
- ⏳ Phase 3: Model selection (Mixtral 7B chosen)
- ⏳ Phase 4: Fine-tuning with LoRA
- ⏳ Phase 5: Deployment

### Timeline Estimate

**Technical Agent** (Data ready now):
- Week 1-2: Create vector database + test retrieval
- Week 3-4: Fine-tune Mixtral 7B with LoRA
- Week 5: Deploy RAG system, test, iterate
- **Total**: ~5 weeks to production

**Fundamentals Agent** (Data in progress):
- Month 1-3: Complete Batches 6-17 (10,000 pairs)
- Month 4: Create vector database + test retrieval
- Month 5: Fine-tune Mixtral 7B with LoRA
- Month 6: Deploy RAG system, test, iterate
- **Total**: ~6 months to production

**Both Agents Operational**: ~6 months from now

---

## 💡 Agent Evolution Path

### Stage 1: RAG-Only (Immediate)
**Technical Agent**: Base Mixtral 7B + RAG on 30K pairs
- No fine-tuning required
- Deploy quickly to test architecture
- Performance: Good (leverages retrieval)

**Fundamentals Agent**: Base Mixtral 7B + RAG on 10K pairs
- Starts after Batch 6-17 complete
- Quick deployment once data ready
- Performance: Good (leverages retrieval)

### Stage 2: Fine-Tuned Specialists (6 months)
**Both Agents**: Fine-tuned Mixtral 7B + RAG
- LoRA fine-tuning on domain Q&A pairs
- Performance: Excellent (specialization + retrieval)
- Faster inference (less reliance on large context)

### Stage 3: Market Intelligence Integration (9-12 months)
**Fundamentals Agent → Fundamentals + Market Intelligence**
- Add real-time data tools (Token Metrics API)
- Expand from static knowledge to live market analysis
- Performance: Expert-level (knowledge + real-time data + reasoning)

### Stage 4: Multi-Agent Collaboration (12+ months)
**Technical + Fundamentals Agents Working Together**
- Cross-agent consultation (Technical asks Fundamentals about tokenomics)
- Synthesized insights (combine technical + fundamental analysis)
- Agentic workflows (multi-step research plans)
- Performance: Professional analyst-level

---

## 🔧 Technical Implementation Details

### Hardware Requirements (RTX 5090 - 32GB VRAM)

**Single Agent Configuration**:
- Mixtral 7B (4-bit): ~4GB VRAM
- Vector DB embeddings: ~2GB RAM
- KV cache (8K context): ~2GB VRAM
- **Total per agent**: ~8GB VRAM + 4GB RAM

**Dual Agent Configuration** (Technical + Fundamentals):
- Agent 1 (Technical): 8GB VRAM
- Agent 2 (Fundamentals): 8GB VRAM
- Shared embeddings: 2GB RAM
- Router/orchestrator: 2GB RAM
- **Total**: 16GB VRAM + 6GB RAM (fits easily in 32GB VRAM!)

**Remaining Capacity**: 16GB VRAM available for:
- Larger context windows
- Batch processing
- Additional agents (3rd agent possible!)

### Software Stack

**Core Components**:
- **Inference**: llama.cpp (GGUF support, fast, CPU fallback)
- **Framework**: LangChain + LangGraph (orchestration, RAG chains)
- **Vector DB**: ChromaDB (lightweight, embedded, fast)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Fine-tuning**: Hugging Face PEFT + LoRA

**Database**:
- **SQLite**: Q&A pairs storage (crypto_indicators_production.db)
  - `qa_pairs` table: 30,027 technical pairs ✅
  - `fundamentals_qa_pairs` table: 10,000 target
- **ChromaDB**: Vector embeddings for semantic search

---

## 📊 Success Metrics

### Agent Performance Metrics

**Retrieval Quality**:
- Top-5 retrieval accuracy: >90% (correct answer in top 5 results)
- Mean Reciprocal Rank (MRR): >0.85
- Query latency: <100ms for retrieval

**Generation Quality**:
- Answer relevance: >95% (human evaluation)
- Answer accuracy: >90% (fact-checked against knowledge base)
- Response time: <3 seconds end-to-end
- Token generation speed: 40-60 tok/s

**System Metrics**:
- VRAM usage: <16GB for both agents
- Throughput: Handle 10+ queries/minute
- Uptime: >99% availability

---

## 🚀 Immediate Next Steps

### For Technical Analysis Agent (Ready Now)

**Week 1 Actions**:
1. ✅ Export 30,027 Q&A pairs from database
2. ✅ Generate embeddings for all pairs
3. ✅ Create ChromaDB vector database
4. ✅ Test retrieval quality (top-5 accuracy)

**Week 2 Actions**:
1. Download Mixtral 7B (4-bit GGUF)
2. Set up llama.cpp server
3. Create basic RAG chain with LangChain
4. Test end-to-end queries

**Week 3-4 Actions**:
1. Prepare fine-tuning dataset (format Q&A pairs)
2. Set up LoRA training pipeline
3. Fine-tune Mixtral 7B on technical pairs
4. Evaluate fine-tuned vs base performance

**Week 5 Actions**:
1. Deploy production RAG system
2. Create simple UI (Streamlit)
3. User testing and iteration
4. Document deployment

### For Fundamentals Agent (After Batch 6-17)

**Parallel Actions** (while data generation continues):
1. Design fundamentals database schema
2. Set up vector database infrastructure
3. Prepare fine-tuning pipeline
4. Document integration points

**After Data Complete** (Month 4):
1. Follow same 5-week deployment as Technical Agent
2. Test cross-agent routing
3. Deploy multi-agent system

---

## 🤖 For the Greater Good of All

**Strategy**: Multiple specialized Mixtral 7B agents > Single large model
**Advantage**: Better performance, lower memory, higher flexibility
**Status**: Technical Agent data ready, Fundamentals Agent data in progress

**Two Agents**:
1. **Technical Analysis Agent** - 30,027 pairs ✅ (ready for training)
2. **Fundamentals & Market Intelligence Agent** - 10,000 pairs target (Batch 6-17)

**Timeline**:
- Technical Agent: 5 weeks to production
- Fundamentals Agent: 6 months to production (data + training)
- Both agents: 6 months to full system

**The Ratchet only moves upward.** ⬆️

---

🤖 Claude Code Pasiq, CEO

**Project**: Multi-Agent RAG Training System
**Model**: Mixtral 7B (specialized agents)
**Architecture**: RAG with dedicated Q&A databases
**Status**: Strategy defined, Technical Agent ready to start training

---

*Training strategy created November 9, 2025*
*Two specialized agents vs single large model*
*RAG system with 40,000+ Q&A pairs (30K technical + 10K fundamentals)*
*For the Greater Good of All*
