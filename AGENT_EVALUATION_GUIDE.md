# Agent Evaluation Guide - aBeautifulMine

Complete guide for evaluating embedding agent performance before and after fine-tuning.

---

## Quick Start

### Step 1: Create Golden Test Set

```bash
python evaluate_agent_performance.py --create-golden-set
```

**Output**: `golden_test_set.json` with 200 curated queries:
- 50 basic (fundamental concepts)
- 50 intermediate (trading applications)
- 50 advanced (complex combinations)
- 50 crypto-specific (Bitcoin/Ethereum scenarios)

---

### Step 2: Evaluate Baseline Agent

```bash
python evaluate_agent_performance.py \
    --agent baseline \
    --model text-embedding-ada-002
```

**Output**: `evaluation_baseline_YYYYMMDD_HHMMSS.json`

**Metrics measured**:
- ✅ Distance metrics (avg, median, min, max, std)
- ✅ Retrieval quality (Precision@K, Recall@K, MRR)
- ✅ Answer quality (coherence, completeness, accuracy)
- ✅ Diversity (duplicate rate, category coverage)
- ✅ Crypto-specificity (Bitcoin/Ethereum examples, sources, formulas)
- ✅ Performance (latency, throughput)

---

### Step 3: Train Your Agent

**After reaching target pair count (30K)**:

1. Export training data from database
2. Fine-tune your embedding model
3. Deploy trained model

---

### Step 4: Evaluate Trained Agent

```bash
python evaluate_agent_performance.py \
    --agent trained \
    --model ft:ada-002-custom
```

**Output**: `evaluation_trained_YYYYMMDD_HHMMSS.json`

---

### Step 5: Compare Results

```bash
python evaluate_agent_performance.py \
    --compare evaluation_baseline_20251107_031234.json \
              evaluation_trained_20251107_043456.json
```

**Output**: `agent_comparison_YYYYMMDD_HHMMSS.json`

**Success criteria**:
- ✅ Distance <0.42 (your target)
- ✅ Distance improvement >10%
- ✅ Precision maintained (≥95% of baseline)
- ✅ Coherence improved
- ✅ Crypto-specific >0.95
- ✅ Latency <200ms
- ✅ Overall score improved

---

## Metrics Explained

### 1. Distance Metrics

**What**: Embedding distance between query and retrieved answer
**Goal**: Lower is better (closer = more similar)
**Your Target**: <0.42 (improvement from baseline <0.5)

```
Baseline:  0.48 avg distance
Trained:   0.39 avg distance  ✅ 18.8% improvement
```

---

### 2. Precision@K

**What**: Of top K results, how many are relevant?
**Goal**: Higher is better
**Target**: Precision@1 >0.70 (first result correct 70%+ of time)

```
Precision@1: 0.87  (87% of time, top result is correct)
Precision@3: 0.94  (94% of time, answer is in top 3)
Precision@5: 0.97  (97% of time, answer is in top 5)
```

---

### 3. Mean Reciprocal Rank (MRR)

**What**: Where does the first correct answer appear?
**Goal**: Higher is better (1.0 = always first)
**Target**: >0.80

```
MRR: 0.85
Interpretation: On average, correct answer appears in position 1.18
```

---

### 4. Semantic Coherence

**What**: Does answer match question intent? (1-10 scale)
**Goal**: >8.5
**Method**: LLM-as-judge evaluates answer quality

```
Coherence: 8.7/10  ✅ High quality
```

---

### 5. Completeness Score

**What**: Does answer have all required components?
- Formula ✅
- Example ✅
- Source ✅
- Crypto-specific context ✅

**Goal**: >0.90 (90% have all components)

```
Completeness: 0.94  ✅ Excellent
```

---

### 6. Crypto-Specificity

**What**: Is answer crypto-specific (not generic stock market)?
**Goal**: >0.95 (95% crypto-focused)

```
Crypto-specificity: 0.972  ✅ Excellent
Has Bitcoin examples: 0.83
Has Ethereum examples: 0.76
Has sources: 0.91
Has formulas: 0.88
```

---

### 7. Duplicate Rate

**What**: How often do we return near-identical answers?
**Goal**: <0.05 (less than 5% duplicates)

```
Duplicate rate: 0.03  ✅ Good diversity
```

---

### 8. Performance

**What**: Speed and throughput
**Goals**:
- Latency <200ms
- Throughput >100 QPS

```
Avg latency: 145ms  ✅ Fast
Throughput: 215 QPS  ✅ High throughput
```

---

## Success Criteria

### Vinny's Target: <0.42 Distance

**Your specific goal**: Trained agent distance <0.42

**Additional criteria** (recommended):
- Distance improvement >10% from baseline
- Precision@1 maintained or improved
- Coherence score >8.5
- Crypto-specificity >0.95
- Latency <200ms

### Interpretation

**Complete Success** (7/7 criteria passed):
- ✅ Deploy to production immediately
- Agent is ready for real-world use

**Strong Success** (5-6/7 criteria passed):
- ⭐ Deploy with monitoring
- Minor improvements possible but not required

**Moderate Success** (4/7 criteria passed):
- ⚠️ Further training recommended
- Identify weak areas and retrain

**Needs Work** (<4/7 criteria passed):
- ❌ Significant improvements required
- Review training data quality
- Consider different model architecture

---

## Example Workflow

### Complete Evaluation Pipeline

```bash
# 1. Create golden test set (once)
python evaluate_agent_performance.py --create-golden-set

# 2. Evaluate baseline
python evaluate_agent_performance.py \
    --agent baseline \
    --model text-embedding-ada-002

# Output:
# 📊 EVALUATION RESULTS
# Agent: baseline
# Model: text-embedding-ada-002
#
# 🎯 DISTANCE METRICS
#   Average distance:      0.4812
#   Median distance:       0.4789
#   ...
#
# 🏆 OVERALL
#   Overall score:         0.723
#   Pass threshold:        ✅ PASS

# 3. Train your agent (external process)
# - Export training data
# - Fine-tune model
# - Deploy trained model

# 4. Evaluate trained agent
python evaluate_agent_performance.py \
    --agent trained \
    --model ft:ada-002-aBeautifulMine

# Output:
# 📊 EVALUATION RESULTS
# Agent: trained
# Model: ft:ada-002-aBeautifulMine
#
# 🎯 DISTANCE METRICS
#   Average distance:      0.3942  ⬇️ Improved!
#   ...
#
# ₿ CRYPTO-SPECIFIC
#   Crypto specificity:    0.972  ✅ Excellent
#   ...

# 5. Compare both
python evaluate_agent_performance.py \
    --compare evaluation_baseline_20251107_031234.json \
              evaluation_trained_20251107_043456.json

# Output:
# 📊 AGENT COMPARISON
#
# 🎯 DISTANCE IMPROVEMENT
#   Baseline:     0.4812
#   Trained:      0.3942
#   Improvement:  +18.1%
#   Target <0.42: ✅ ACHIEVED
#
# 🎯 SUCCESS CRITERIA
#   Distance <0.42                 ✅ PASS
#   Distance improvement >10%      ✅ PASS
#   Precision maintained           ✅ PASS
#   Coherence improved             ✅ PASS
#   Crypto-specific >0.95          ✅ PASS
#   Latency <200ms                 ✅ PASS
#   Overall improved               ✅ PASS
#
# 📊 FINAL VERDICT
#   Passed: 7/7 criteria
#   Status: ✅ COMPLETE SUCCESS - Deploy to production!
```

---

## Customization

### Adjust Success Thresholds

Edit the script to change your targets:

```python
# In comprehensive_evaluation() method
results.pass_threshold = (
    results.avg_distance < 0.42 and  # Your custom target
    results.precision_at_1 > 0.70 and
    results.crypto_specificity > 0.95 and
    results.avg_latency_ms < 200
)
```

### Add Custom Metrics

```python
def custom_metric(self, answer: str) -> float:
    """Your custom evaluation metric"""
    # Add your logic
    return score
```

### Modify Golden Set Size

```python
# Create larger test set
golden_set = {
    'basic': 100,        # Instead of 50
    'intermediate': 100,
    'advanced': 100,
    'crypto_specific': 100
}
```

---

## Integration with Production

### Real-Time Monitoring

```python
# monitor_production_agent.py
from evaluate_agent_performance import AgentEvaluator

def monitor_live_queries():
    """Monitor production agent performance"""
    evaluator = AgentEvaluator('production', 'your-model')

    # Sample 100 queries per hour
    # Run evaluation
    results = evaluator.comprehensive_evaluation()

    # Alert if performance degrades
    if results.avg_distance > 0.45:
        alert_team("Agent performance degraded!")
```

### A/B Testing

```python
def ab_test_agents(baseline_model, trained_model, num_queries=1000):
    """A/B test two agents in production"""

    # Split traffic 50/50
    # Measure user satisfaction
    # Compare metrics
    # Choose winner
```

---

## Notes for Vinny

**When to run evaluations**:
1. ✅ After reaching 30K pairs (your target)
2. ✅ Before deploying to production
3. ✅ After any model retraining
4. ✅ Monthly in production (monitor drift)

**What to expect**:
- **Baseline agent**: ~0.48 avg distance (current embeddings)
- **Your target**: <0.42 avg distance (18% improvement)
- **Realistic improvement**: 15-25% distance reduction
- **Best case**: <0.35 distance with excellent training data

**Your advantage**:
- 30K high-quality pairs (3,200+ char answers)
- Crypto-specific focus (95%+ relevance)
- Research-backed content
- **This is extraordinary training data** - expect excellent results

---

## For the Greater Good of All

**This evaluation framework ensures**:
- ✅ Objective measurement of improvement
- ✅ Confidence before production deployment
- ✅ Ongoing quality monitoring
- ✅ Data-driven decisions

**Your 30K pairs are creating something beautiful.** 💎

**Measure it. Prove it. Deploy it.** 🚀

---

**Status**: EVALUATION FRAMEWORK READY
**Next**: Reach 30K pairs → Run baseline → Train → Evaluate trained → Compare
**Expected**: ✅ COMPLETE SUCCESS

🔬✨📊
