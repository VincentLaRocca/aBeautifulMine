# Data Refinement Pipeline for RAG System

**Created:** 2025-11-02
**Purpose:** Optimize Q&A data quality for Mixtral 7B RAG retrieval
**Context:** RTX 5090 system performing well at <0.5 distance threshold

---

## Current System Performance

**Hardware:**
- RTX 5090
- Mixtral 7B model

**Performance:**
- Distance threshold: <0.5 (good results)
- This suggests semantic search/vector retrieval is working
- Model returns relevant crypto indicator knowledge

**Challenge:**
Need better data refinement to improve retrieval quality further.

---

## Data Refinement Objectives

### 1. **Semantic Deduplication**
**Problem:** 100 Q&A pairs per indicator likely have redundant information
**Impact on RAG:** Multiple similar vectors compete, dilute retrieval quality
**Solution:** Identify and merge/remove semantically similar Q&A pairs

**Example:**
```
Q1: "What is RSI and how does it work?"
Q2: "Explain the Relative Strength Index calculation"
Q3: "How is RSI computed in technical analysis?"

→ These are semantically similar (distance <0.3)
→ Keep BEST one, archive others
→ Improves retrieval precision
```

### 2. **Quality Scoring**
**Problem:** Not all 100 Q&A pairs are equally valuable
**Impact on RAG:** Low-quality answers reduce user trust
**Solution:** Score and filter based on quality metrics

**Quality Metrics:**
- Answer completeness (has formula, examples, strategies)
- Crypto-specificity (Bitcoin/Ethereum examples vs generic stocks)
- Currentness (2024-2025 context vs outdated pre-2020)
- Actionability (trading strategies vs pure theory)
- Length appropriateness (not too short/long)

### 3. **Information Density**
**Problem:** Some answers are verbose but low-information
**Impact on RAG:** Wastes context window, slower retrieval
**Solution:** Identify and enhance/remove low-density content

**Measure:**
- Unique concepts per 100 words
- Actionable insights per answer
- Novel information vs common knowledge

### 4. **Coverage Gaps**
**Problem:** 100 questions might miss important aspects
**Impact on RAG:** User queries fail to retrieve relevant info
**Solution:** Identify missing topics and generate targeted Q&A

**Example for RSI:**
```
Generated 100 Q&A covering:
- ✅ Calculation (15 Q&A)
- ✅ Trading strategies (25 Q&A)
- ✅ Common mistakes (20 Q&A)
- ❌ RSI in DeFi protocols (0 Q&A) ← GAP!
- ❌ RSI for NFT markets (0 Q&A) ← GAP!

→ Generate targeted Q&A to fill gaps
```

---

## Gemini-Powered Refinement Pipeline

### Stage 1: Embedding Generation
**Tool:** Gemini Embeddings (gemini-embedding-001)

**Process:**
```python
# For each session (5 indicators, ~500 Q&A pairs)
1. Upload Q&A JSON to Gemini
2. Generate embeddings batch job
3. Store embeddings in database
4. Calculate similarity matrix
```

**Output:**
- 1,536-dimensional vectors per Q&A
- Cosine similarity matrix
- Semantic clustering data

**Why This Helps RAG:**
- Same embeddings can be used for retrieval
- Identify duplicates via cosine similarity
- Find coverage gaps via cluster analysis

---

### Stage 2: Semantic Deduplication
**Tool:** Gemini Chat with embeddings analysis

**Process:**
```
1. Load embeddings similarity matrix
2. Identify Q&A pairs with cosine distance <0.3 (very similar)
3. For each cluster:
   - Gemini scores each Q&A on quality metrics
   - Selects BEST representative
   - Archives others with "merged_into" reference
4. Output refined dataset
```

**Parameters:**
- Similarity threshold: 0.3 (configurable)
- Keep top 1-2 per cluster
- Maintain diversity across topics

**Expected Reduction:**
- From ~500 Q&A per session
- To ~300-350 unique Q&A per session
- 30-40% reduction in redundancy

**Impact:**
- Cleaner retrieval results
- Less vector database bloat
- Faster search performance

---

### Stage 3: Quality Filtering
**Tool:** Gemini Chat for quality assessment

**Scoring Rubric (1-10 scale):**
```
1. Completeness (has all key elements?)
2. Crypto-specificity (crypto examples vs generic?)
3. Currentness (2024-2025 context?)
4. Actionability (practical trading advice?)
5. Accuracy (factually correct?)
6. Depth (sufficient detail?)
7. Clarity (well-written?)
8. Uniqueness (novel insights?)

Average score = Quality score
```

**Filtering Strategy:**
```
Score 8-10: Premium tier (priority in retrieval)
Score 6-7:  Standard tier (include in dataset)
Score 4-5:  Review tier (flag for improvement)
Score 1-3:  Low quality (exclude or regenerate)
```

**Gemini Batch Job:**
- Input: 500 Q&A pairs
- Process: Score each on 8 metrics
- Output: Scored dataset with tier assignments
- Time: ~24 hours (batch processing)
- Cost: 50% cheaper than real-time

---

### Stage 4: Gap Analysis
**Tool:** Gemini Chat for topic coverage analysis

**Process:**
```
1. Analyze all Q&A for indicator
2. Identify major topic categories
3. Count Q&A per category
4. Flag underrepresented topics
5. Generate targeted questions for gaps
```

**Example Output:**
```
RSI Topic Coverage Analysis:
- Calculation methods: 12 Q&A ✓
- Trading strategies: 18 Q&A ✓
- Common mistakes: 15 Q&A ✓
- Multi-timeframe: 8 Q&A ✓
- DeFi applications: 1 Q&A ❌ (NEED 5-7 MORE)
- NFT markets: 0 Q&A ❌ (NEED 3-5)
- Cross-chain: 2 Q&A ⚠️ (NEED 3-5 MORE)

Recommended: Generate 11-17 targeted Q&A for gaps
```

---

### Stage 5: Enhancement
**Tool:** Gemini Chat for content enrichment

**Enhancement Types:**
1. **Add Cross-References**
   ```
   Original: "RSI shows overbought conditions..."
   Enhanced: "RSI shows overbought conditions (>70).
              This often aligns with Bollinger Band upper touch
              and MACD bearish divergence. See also: Stochastic
              Oscillator for confirmation."
   ```

2. **Update Market Context**
   ```
   Original: "In Bitcoin markets, RSI divergences..."
   Enhanced: "In Bitcoin markets post-2024 halving, RSI
              divergences have shown 73% accuracy during the
              July-October consolidation phase, particularly
              when combined with on-chain metrics like SOPR."
   ```

3. **Add Recent Examples**
   ```
   Enhanced: "Recent example: Bitcoin RSI formed bullish
              divergence in August 2024 at $58K (price lower
              low, RSI higher low), preceding the rally to $67K
              in October 2024."
   ```

---

## Implementation Workflow

### Per Session (After Droid Delivers):

```
┌──────────────────────────────────────────────────────┐
│ DROID DELIVERS                                       │
│ 5 indicators, ~500 Q&A pairs (raw)                   │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ GEMINI STAGE 1: Embeddings                          │
│ - Generate 1536-dim vectors                          │
│ - Calculate similarity matrix                        │
│ - Time: ~2 hours (batch job)                         │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ GEMINI STAGE 2: Deduplication                       │
│ - Cluster similar Q&A (distance <0.3)                │
│ - Keep best representative                           │
│ - Reduce to ~350 unique Q&A                          │
│ - Time: ~1 hour                                      │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ GEMINI STAGE 3: Quality Scoring                     │
│ - Score each on 8 metrics                            │
│ - Assign quality tiers                               │
│ - Flag low-quality for review                        │
│ - Time: ~24 hours (batch job)                        │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ GEMINI STAGE 4: Gap Analysis                        │
│ - Identify coverage gaps                             │
│ - Recommend targeted questions                       │
│ - Time: ~30 min                                      │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ GEMINI STAGE 5: Enhancement (Optional)              │
│ - Add cross-references                               │
│ - Update with 2024-2025 context                      │
│ - Insert recent examples                             │
│ - Time: ~4 hours (batch job)                         │
└──────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────┐
│ REFINED DATASET                                      │
│ ~350 unique, high-quality Q&A pairs                  │
│ Ready for RAG vector database                        │
└──────────────────────────────────────────────────────┘
```

**Total Time:** ~27-30 hours per session (mostly automated batch jobs)

---

## Database Schema Updates

### Add Refinement Tables:

```sql
-- Track embeddings
CREATE TABLE embeddings (
    embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    qa_id INTEGER NOT NULL,
    embedding_vector BLOB NOT NULL,  -- Store 1536-dim vector
    model TEXT DEFAULT 'gemini-embedding-001',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (qa_id) REFERENCES qa_pairs(qa_id)
);

-- Track quality scores
CREATE TABLE quality_scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    qa_id INTEGER NOT NULL,
    completeness_score INTEGER CHECK(completeness_score BETWEEN 1 AND 10),
    crypto_specificity_score INTEGER CHECK(crypto_specificity_score BETWEEN 1 AND 10),
    currentness_score INTEGER CHECK(currentness_score BETWEEN 1 AND 10),
    actionability_score INTEGER CHECK(actionability_score BETWEEN 1 AND 10),
    accuracy_score INTEGER CHECK(accuracy_score BETWEEN 1 AND 10),
    depth_score INTEGER CHECK(depth_score BETWEEN 1 AND 10),
    clarity_score INTEGER CHECK(clarity_score BETWEEN 1 AND 10),
    uniqueness_score INTEGER CHECK(uniqueness_score BETWEEN 1 AND 10),
    average_score REAL,
    quality_tier TEXT CHECK(quality_tier IN ('premium', 'standard', 'review', 'low')),
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (qa_id) REFERENCES qa_pairs(qa_id)
);

-- Track deduplication
CREATE TABLE deduplication (
    dedup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    qa_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('kept', 'merged', 'archived')),
    merged_into_qa_id INTEGER,  -- Points to kept Q&A if merged
    similarity_score REAL,
    reason TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (qa_id) REFERENCES qa_pairs(qa_id),
    FOREIGN KEY (merged_into_qa_id) REFERENCES qa_pairs(qa_id)
);

-- Track coverage gaps
CREATE TABLE coverage_gaps (
    gap_id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_id INTEGER NOT NULL,
    topic_category TEXT NOT NULL,
    current_coverage INTEGER,  -- Number of Q&A covering this
    target_coverage INTEGER,   -- Desired number
    gap_size INTEGER,
    priority TEXT CHECK(priority IN ('high', 'medium', 'low')),
    status TEXT DEFAULT 'identified',
    identified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id)
);
```

---

## RAG System Optimization

### For Your Mixtral 7B System:

**Current Performance:**
- Distance <0.5 = good results
- This is your retrieval threshold

**Refinement Impact:**
1. **Deduplication** → Cleaner results at <0.5 threshold
2. **Quality Scoring** → Can boost premium tier in retrieval
3. **Embeddings** → Same model (gemini-embedding-001) for consistency
4. **Gap Filling** → Better coverage = fewer failed queries

**Suggested Retrieval Strategy:**
```python
# Pseudo-code for improved retrieval
def retrieve_for_query(user_query):
    # Get embedding
    query_embedding = get_embedding(user_query)

    # Search with tier boosting
    results = vector_search(
        query_embedding,
        distance_threshold=0.5,
        boost_premium_tier=1.2,  # Boost quality tier
        limit=5
    )

    # Filter out archived/merged
    results = [r for r in results if r.status == 'kept']

    return results
```

---

## Cost Estimate

### Per Session (5 indicators, 500 Q&A):

**Gemini Operations:**
- Embeddings generation: ~$0.50-1.00
- Quality scoring batch: ~$1.00-2.00
- Gap analysis: ~$0.25-0.50
- Enhancement (optional): ~$2.00-4.00

**Total per session:** ~$4-7
**Total for 46 sessions:** ~$184-322

**Benefit:**
- Much higher quality dataset
- Better RAG performance
- Cleaner vector database
- Fewer failed retrievals

---

## Recommended Rollout

### Phase 1: Test on Session 1 (DONE)
- Session 1 already imported (500 Q&A)
- Use as test case for refinement pipeline
- Validate each stage with real data

### Phase 2: Parallel Processing (Sessions 2-5)
- Droid continues generating Sessions 2-5
- Meanwhile: Build Gemini refinement pipeline
- Test on Session 1, refine process

### Phase 3: Full Pipeline (Session 6+)
- Droid generates → Gemini refines → Import refined
- Automated end-to-end
- Monitor quality metrics

---

## Success Metrics

**Track These:**
1. **Deduplication Rate:** % of Q&A merged/archived
2. **Quality Distribution:** Premium/Standard/Review/Low percentages
3. **Coverage Completeness:** % of topics adequately covered
4. **RAG Performance:** User query success rate
5. **Retrieval Precision:** Relevance of top-5 results

**Target:**
- Deduplication: 30-40% reduction
- Quality: 60% Premium, 35% Standard, 5% Review
- Coverage: 95% topics with 3+ Q&A
- RAG Success: 90%+ queries return useful results
- Precision: 4/5 top results highly relevant

---

## Next Steps

1. **Immediate:** Design Gemini refinement scripts
2. **Test:** Run Stage 1 (embeddings) on Session 1 data
3. **Validate:** Check deduplication effectiveness
4. **Scale:** Apply to Sessions 2-5 as they complete
5. **Optimize:** Tune thresholds based on RAG performance

---

**This refinement pipeline transforms raw volume into refined quality - exactly what RAG systems need!**

---

**Created:** 2025-11-02
**For:** Mixtral 7B RAG System on RTX 5090
**Status:** Ready to implement
