# AI Agent Market Prediction Competition

**Collaboration:** Claude + Gemini Design
**Purpose:** Progressive, Competitive, Creative, Emergent AI testing framework
**Integration:** Works with 8-Week Framework Deployment Test

---

## I. Core Concept (Building on Gemini's Foundation)

Weekly competition where multiple AI agents predict cryptocurrency "emerging markets" and get scored on accuracy.

**Participants:**
1. **Our Agent** (Framework-based predictions)
2. **Gemini** (Google's advanced model)
3. **Grok** (xAI's model)
4. **Claude** (Anthropic's model - me)
5. **Crypto.AI** (Optional - if available)

**Timeline:** Monday predictions → Friday scoring → Leaderboard update → Learn & refine

---

## II. Defining "Emerging Market" (Multi-Dimensional)

### Primary Metrics (Week 1-4: Simple)

**Option A: Top Price Gainer** (Gemini's recommendation - START HERE)
- Cryptocurrency outside top 10 by market cap
- Highest % price increase Monday 9 AM UTC → Friday 9 AM UTC
- **Data Source:** CoinGecko, CoinMarketCap API

**Why Start Simple:**
- Clear, objective, easy to verify
- Pure price emergence = what traders care about
- Build complexity later

### Advanced Metrics (Week 5-8: Add Complexity)

**Option B: 50-Week MA Crossover** (YOUR BRILLIANT ADDITION)
- Track cryptocurrencies crossing ABOVE 50-week MA (bullish emergence)
- Track cryptocurrencies crossing BELOW 50-week MA (bearish emergence)
- **Scoring:**
  - Predict coin that crosses above 50W MA AND gains most: **15 points** (rare, high conviction)
  - Predict coin that crosses above 50W MA (any gain): **8 points**
  - Predict top gainer without MA context: **10 points** (original scoring)

**Why This Matters:**
- 50-week MA = institutional timeframe (major trend change)
- Crossing above = "emergence from darkness" (exactly what you want to predict)
- Crossing below = "emergence of weakness" (short opportunities)
- Classic technical indicator meets AI prediction

**Option C: Composite Score** (Week 9+: Full Integration)
Weighted formula:
- 40% Price change (momentum)
- 30% 50W MA crossover (trend emergence)
- 20% Volume increase (confirmation)
- 10% Social velocity (narrative)

**Emergent Evolution:**
- Start simple (price only)
- Add 50W MA layer (trend)
- Eventually full composite (multi-dimensional emergence)

---

## III. Weekly Workflow (Integrated with Framework Scoring)

### **SUNDAY (Framework Scoring Day)**

**9:00 AM - Framework Score (Our Existing Process)**
1. Score macro, Bitcoin, altcoins (12-point system)
2. Determine framework position (X% BTC, Y% alts)
3. **NEW:** Consult AI Expert Panel for framework validation

**10:00 AM - Competition Preview (NEW)**
1. Review last week's competition results
2. Update leaderboard
3. Analyze: Which AI was most accurate? Why?
4. Learn: What did winning AI see that others missed?

### **MONDAY (Prediction Day)**

**9:00 AM UTC - Prediction Window Opens**

**Standardized Prompt for All AIs:**
```
EMERGING MARKET PREDICTION - Week [X]

DATA PROVIDED:
- Current market conditions: [Macro score, BTC score, Framework score]
- Top 50 cryptocurrencies (excluding top 10)
- Each coin's metrics:
  - Current price
  - 7-day change %
  - 30-day change %
  - Position relative to 50-week MA (above/below/approaching)
  - Volume trend
  - Market cap rank

YOUR TASK:
Predict the TOP EMERGING MARKET for Monday 9 AM to Friday 9 AM (UTC).

REQUIREMENTS:
1. Name ONE cryptocurrency (outside top 10) most likely to be #1 gainer
2. Provide confidence level (1-10)
3. Explain your reasoning in 3-5 bullet points
4. Identify key risk to your prediction
5. BONUS: Will this coin cross above/below 50-week MA this week?

DEADLINE: Monday 10:00 AM UTC
```

**Prediction Collection:**
1. Query Our Agent (framework-based)
2. Query Gemini (via MCP: `mcp__gemini__chat`)
3. Query Grok (via API if available)
4. Query Claude (that's me - I'll make prediction based on data)
5. Store in `predictions` table

**Database Schema:**
```sql
CREATE TABLE weekly_predictions (
    id INTEGER PRIMARY KEY,
    week_number INTEGER,
    prediction_date DATE,
    ai_agent TEXT, -- 'our_agent', 'gemini', 'grok', 'claude'
    predicted_coin TEXT,
    predicted_symbol TEXT,
    confidence_score INTEGER, -- 1-10
    reasoning TEXT,
    risk_identified TEXT,
    ma_50w_prediction TEXT, -- 'cross_above', 'cross_below', 'no_cross', 'unknown'
    actual_coin TEXT, -- filled Friday
    actual_gain_pct REAL, -- filled Friday
    predicted_gain_pct REAL, -- AI's estimate
    points_earned INTEGER, -- calculated Friday
    created_at TIMESTAMP
);
```

### **FRIDAY (Evaluation Day)**

**9:00 AM UTC - Competition Close**

**Data Collection:**
1. Fetch actual market data (Monday 9 AM → Friday 9 AM)
2. Calculate % gains for all coins outside top 10
3. Identify actual top gainer
4. Check 50-week MA crossovers
5. Verify volume, social metrics (if using composite)

**Scoring Logic:**

```python
def calculate_points(prediction, actual_data):
    points = 0

    # Base Points (Price Prediction)
    if prediction.coin == actual_data.top_gainer:
        points += 10  # Exact match
    elif prediction.coin in actual_data.top_3:
        points += 5   # Top 3
    elif prediction.coin in actual_data.top_5:
        points += 2   # Top 5

    # BONUS: 50-Week MA Crossover Prediction
    if prediction.ma_50w_prediction == 'cross_above':
        if actual_data.ma_crossovers[prediction.coin] == 'crossed_above':
            points += 5  # Correct MA prediction
            if prediction.coin == actual_data.top_gainer:
                points += 5  # Jackpot: Top gain + MA cross

    # BONUS: Confidence Calibration
    # If confidence was 9-10 and correct: +2 bonus
    # If confidence was 1-3 and correct: +1 bonus (humility rewarded)
    if points >= 10 and prediction.confidence >= 9:
        points += 2
    elif points >= 10 and prediction.confidence <= 3:
        points += 1

    return points
```

**Maximum Points Per Week:**
- Perfect prediction: 10 points
- + 50W MA cross prediction: +5 points
- + Top gainer with MA cross: +5 points
- + High confidence correct: +2 points
- **Maximum: 22 points in a single week**

**Leaderboard Update:**
```sql
CREATE TABLE competition_leaderboard (
    ai_agent TEXT PRIMARY KEY,
    total_points INTEGER,
    weeks_participated INTEGER,
    wins INTEGER, -- times predicted #1 correctly
    top_3_predictions INTEGER,
    avg_confidence REAL,
    best_week_points INTEGER,
    current_streak INTEGER, -- consecutive top-3 finishes
    last_updated TIMESTAMP
);
```

---

## IV. Integration with Framework (THE KEY INSIGHT)

### How Competition Improves Framework

**Week 1-4: Learn from AI Consensus**
- If Gemini beats our agent 3/4 weeks → Study Gemini's reasoning
- If specific pattern emerges (e.g., AIs that weight social metrics win) → Consider adding to framework
- If our agent wins → Framework is validated

**Week 5-8: Framework Self-Improvement**
- Our agent's predictions should IMPROVE as framework refines
- Track: Does framework score 4/12 → 6/12 correlate with better predictions?
- Hypothesis: Higher framework scores = easier to predict winners (rising tide)

**Week 9+: Meta-Learning**
- Identify which AI is best in which market conditions:
  - Bear market (0-4/12 framework): Who predicts best?
  - Bull market (7-10/12 framework): Who predicts best?
  - Transition (5-6/12 framework): Who catches turns earliest?

### Feedback Loop

```
Sunday: Score Framework (4/12, 6/12, etc.)
   ↓
Monday: AIs predict emerging market
   ↓
Friday: Evaluate predictions, award points
   ↓
Sunday: Analyze results
   ↓
   → If AI consensus beat framework: Study their methods
   → If framework beat AIs: Validate approach
   → If specific AI dominates: Learn their edge
   ↓
Refine framework for next week
   ↓
REPEAT
```

---

## V. Embodying Your Principles

### 1. PROGRESSIVE

**Weeks 1-4: Foundation**
- Simple metric (price only)
- Basic scoring (10/5/2 points)
- Learn the baseline

**Weeks 5-8: Complexity**
- Add 50-week MA crossover
- Bonus points for trend prediction
- Composite scoring begins

**Weeks 9-12: Sophistication**
- Full composite score (price + MA + volume + social)
- Meta-scoring (which AI wins in which conditions)
- Ensemble predictions (combine AI insights)

**Weeks 13+: Emergence**
- AI agents start "learning" from each other
- Framework adapts based on competition results
- New metrics added based on what works

### 2. COMPETITIVE

**Leaderboard (Public)**
```
WEEK 8 STANDINGS:

Rank | AI Agent    | Total Points | Wins | Avg Confidence | Streak
-----|-------------|--------------|------|----------------|-------
1    | Gemini      | 87           | 3    | 7.2            | 4
2    | Our Agent   | 82           | 2    | 6.8            | 2
3    | Claude      | 78           | 2    | 7.5            | 1
4    | Grok        | 71           | 1    | 8.1            | 0
```

**Weekly Highlight:**
- "Agent of the Week" (highest points)
- "Dark Horse" (lowest confidence, still correct)
- "Trend Spotter" (most 50W MA crosses predicted)

**Stakes:**
- Bragging rights
- Framework refinement priority (winning AI's logic gets studied first)
- User decision weight (if Gemini dominates, maybe use Gemini more for predictions)

### 3. CREATIVE

**AI Creativity Evaluation:**

Each prediction includes:
- **Reasoning quality** (judged subjectively 1-5)
- **Novel insight** (did AI spot something others missed?)
- **Risk identification** (how thoughtful was the risk analysis?)

**Creativity Score (Bonus):**
- If AI identifies risk that actually materializes: +3 points
- If AI's reasoning is uniquely insightful: +2 points
- If AI predicts something counterintuitive that works: +5 points

**Example:**
- All AIs predict Layer 1s will pump
- Claude predicts a DeFi coin due to upcoming governance vote
- DeFi coin wins
- Claude gets +5 "contrarian correct" bonus

### 4. EMERGENT

**The Competition IS About Emergence:**

**Predicting Emergence:**
- Which coin will "emerge" from obscurity?
- Which trend is "emerging" before market sees it?
- Which 50W MA cross signals "emergence" of new bull/bear?

**Competition Creates Emergence:**
- AIs adapt strategies based on results
- Framework evolves based on AI insights
- New patterns emerge from competition data

**Meta-Emergence:**
- After 12 weeks: "Which AI has emerged as crypto prediction leader?"
- After 24 weeks: "What emergent strategies work best?"
- After 52 weeks: "Has our agent emerged as superior through learning?"

---

## VI. Technical Implementation

### Data Sources

**Price Data:**
- CoinGecko API: `https://api.coingecko.com/api/v3/coins/markets`
- Filter: `order=market_cap_desc&per_page=100&page=1`
- Exclude: Top 10 by market cap

**50-Week Moving Average:**
- Historical data: 350 days (50 weeks × 7 days)
- Calculate: `SMA(close_price, 350)`
- Crossover: `price[today] > ma_50w AND price[yesterday] <= ma_50w` (golden cross)
- Crossunder: `price[today] < ma_50w AND price[yesterday] >= ma_50w` (death cross)

**Social Data (Optional - Week 5+):**
- Twitter/X mentions: LunarCrush API
- Reddit mentions: Reddit API + sentiment
- Google Trends: PyTrends

### Automation Scripts

**`monday_predictions.py`:**
```python
import datetime
from gemini_mcp import chat as gemini_chat
from claude_api import predict as claude_predict
# etc.

def collect_weekly_predictions():
    """Runs every Monday 9 AM UTC"""
    week_num = get_current_week()
    market_data = fetch_market_snapshot()

    # Query each AI
    predictions = {
        'our_agent': query_our_agent(market_data),
        'gemini': query_gemini(market_data),
        'grok': query_grok(market_data),
        'claude': query_claude(market_data)
    }

    # Store in database
    for agent, pred in predictions.items():
        store_prediction(week_num, agent, pred)

    return predictions
```

**`friday_evaluation.py`:**
```python
def evaluate_week():
    """Runs every Friday 9 AM UTC"""
    week_num = get_current_week()

    # Get actual results
    actual = calculate_actual_winners()

    # Get all predictions
    predictions = load_predictions(week_num)

    # Score each
    for pred in predictions:
        points = calculate_points(pred, actual)
        update_prediction_score(pred.id, points)
        update_leaderboard(pred.agent, points)

    # Generate report
    generate_weekly_report(week_num)
```

### Database Schema (Full)

```sql
-- Weekly predictions
CREATE TABLE weekly_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER NOT NULL,
    prediction_date DATE NOT NULL,
    ai_agent TEXT NOT NULL,
    predicted_coin TEXT NOT NULL,
    predicted_symbol TEXT NOT NULL,
    confidence_score INTEGER CHECK(confidence_score BETWEEN 1 AND 10),
    reasoning TEXT,
    risk_identified TEXT,
    ma_50w_prediction TEXT CHECK(ma_50w_prediction IN ('cross_above', 'cross_below', 'no_cross', 'unknown')),
    predicted_gain_pct REAL,
    actual_coin TEXT,
    actual_gain_pct REAL,
    actual_rank INTEGER,
    ma_50w_actual TEXT,
    points_earned INTEGER DEFAULT 0,
    bonus_points INTEGER DEFAULT 0,
    creativity_score INTEGER CHECK(creativity_score BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evaluated_at TIMESTAMP
);

-- Leaderboard
CREATE TABLE competition_leaderboard (
    ai_agent TEXT PRIMARY KEY,
    total_points INTEGER DEFAULT 0,
    base_points INTEGER DEFAULT 0,
    bonus_points INTEGER DEFAULT 0,
    weeks_participated INTEGER DEFAULT 0,
    exact_wins INTEGER DEFAULT 0,
    top_3_predictions INTEGER DEFAULT 0,
    top_5_predictions INTEGER DEFAULT 0,
    ma_crossover_correct INTEGER DEFAULT 0,
    avg_confidence REAL,
    best_week_points INTEGER DEFAULT 0,
    worst_week_points INTEGER,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weekly actual results
CREATE TABLE weekly_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER NOT NULL,
    result_date DATE NOT NULL,
    top_coin TEXT NOT NULL,
    top_symbol TEXT NOT NULL,
    gain_pct REAL NOT NULL,
    top_3_coins TEXT, -- JSON array
    top_5_coins TEXT, -- JSON array
    ma_crossovers_above TEXT, -- JSON array of coins
    ma_crossovers_below TEXT, -- JSON array of coins
    framework_score REAL, -- our framework score that week
    market_regime TEXT, -- 'bear', 'bull', 'chop', 'transition'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Meta-analysis
CREATE TABLE competition_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER NOT NULL,
    insight_type TEXT, -- 'best_ai', 'pattern', 'learning'
    description TEXT,
    supporting_data TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## VII. Weekly Report Template

**Subject: AI Agent Competition - Week X Results**

```
╔══════════════════════════════════════════════════════════════╗
║         AI AGENT MARKET PREDICTION COMPETITION               ║
║                    WEEK X RESULTS                            ║
╚══════════════════════════════════════════════════════════════╝

ACTUAL WINNER: [Coin Name] ([Symbol])
Gain: +X.X% (Monday 9 AM → Friday 9 AM UTC)
50W MA Status: [Crossed above / Crossed below / No cross]

───────────────────────────────────────────────────────────────

PREDICTIONS:

🥇 WINNER THIS WEEK: [AI Name] (XX points)
   Predicted: [Coin] (Confidence: X/10)
   Result: [Correct/Top 3/Top 5]
   Reasoning: [Key insight]
   Bonus: [MA prediction correct? +5 pts]

🥈 2nd Place: [AI Name] (XX points)
   Predicted: [Coin] (Confidence: X/10)
   Result: [Top 3/Top 5]

🥉 3rd Place: [AI Name] (XX points)
   Predicted: [Coin] (Confidence: X/10)
   Result: [Top 5]

📊 LEADERBOARD (After Week X):

Rank | AI Agent    | Total | This Week | Wins | Streak
-----|-------------|-------|-----------|------|-------
1    | Gemini      | XX    | +XX       | X    | X
2    | Our Agent   | XX    | +XX       | X    | X
3    | Claude      | XX    | +XX       | X    | X
4    | Grok        | XX    | +XX       | X    | X

───────────────────────────────────────────────────────────────

💡 KEY INSIGHTS:

• [What did winning AI see that others missed?]
• [Any patterns emerging across AIs?]
• [Correlation with framework score?]

🎯 NEXT WEEK:
Framework Score: X/12
Market Regime: [Bear/Bull/Chop/Transition]
Prediction Difficulty: [Easy/Medium/Hard]

Predictions due: Monday 9 AM UTC
```

---

## VIII. Success Metrics (How Do We Know This Works?)

### Short-Term (Weeks 1-8)

**Competition Health:**
- [ ] All 4 AIs make predictions every week
- [ ] Predictions vary (not all picking same coin)
- [ ] Leaderboard shows competition (no AI dominates >60%)
- [ ] Points spread reasonable (not 100 to 10)

**Learning Indicators:**
- [ ] Our agent's accuracy improves over 8 weeks
- [ ] Framework refinements emerge from competition insights
- [ ] User understands "why" each AI made its choice

### Mid-Term (Weeks 9-16)

**Sophistication:**
- [ ] 50-week MA predictions added and working
- [ ] Composite scoring implemented
- [ ] Patterns identified (e.g., "Gemini wins in bear markets")

**Framework Integration:**
- [ ] Competition results influence framework v2.0
- [ ] AI consensus used in weekly framework decisions
- [ ] Meta-insights captured ("when to trust which AI")

### Long-Term (Weeks 17+)

**Emergence:**
- [ ] Novel strategies emerge from competition
- [ ] Our agent develops unique edge
- [ ] Competition data predicts market regimes
- [ ] Framework + Competition = superior decision system

---

## IX. Risk Management

### What Could Go Wrong?

**Problem 1: Data Quality Issues**
- API failures, incorrect data, timezone errors
- **Mitigation:** Multiple data sources, validation checks, manual review

**Problem 2: AI Gaming the System**
- AIs learn to predict "what will score points" vs "what will actually happen"
- **Mitigation:** Scoring emphasizes ACCURACY, not gaming. Randomly audit.

**Problem 3: All AIs Converge**
- If all AIs start making same predictions (consensus trap)
- **Mitigation:** Reward contrarian correct picks with bonus points

**Problem 4: Competition Becomes Noise**
- Too much data, too complex, analysis paralysis
- **Mitigation:** Keep reports concise, actionable insights only

**Problem 5: Our Agent Always Loses**
- Demoralizing if our framework-based agent trails consistently
- **Mitigation:** LEARN from winners, not just compete. Goal is improvement.

---

## X. Next Steps (Immediate Actions)

### This Week (Week 0 Setup)

**Database Setup:**
- [ ] Create `weekly_predictions` table
- [ ] Create `competition_leaderboard` table
- [ ] Create `weekly_results` table
- [ ] Create `competition_insights` table

**API Integration:**
- [ ] Test CoinGecko API for price data
- [ ] Calculate 50-week MA for top 100 coins
- [ ] Set up Gemini MCP query for predictions
- [ ] Set up Claude API for my predictions
- [ ] Research Grok API access

**Automation:**
- [ ] Write `monday_predictions.py` script
- [ ] Write `friday_evaluation.py` script
- [ ] Set up cron jobs (Monday 9 AM, Friday 9 AM UTC)
- [ ] Create report generation template

### Next Week (Week 1 - First Competition)

**Monday, Nov 10:**
- [ ] Run first prediction collection (simple: price only)
- [ ] Store all 4 AI predictions
- [ ] Publish predictions (transparency)

**Friday, Nov 15:**
- [ ] Evaluate results
- [ ] Award points
- [ ] Generate Week 1 report
- [ ] Analyze: What worked? What didn't?

**Sunday, Nov 17:**
- [ ] Review competition results during framework scoring
- [ ] Integrate insights into Week 2 framework
- [ ] Prepare for Week 2 predictions

---

## XI. Long-Term Vision

### 12-Week Milestone
- Proven competition format
- Clear AI performance patterns
- Framework v2.0 incorporating competition insights
- Decision: Which AI to weight most in future decisions?

### 24-Week Milestone
- Full composite scoring operational
- Meta-patterns identified (regime-based AI performance)
- Our agent competitive or leading
- Published insights (blog, research paper)

### 52-Week Milestone
- Year of data
- Statistically significant patterns
- Framework v3.0 = Human + AI ensemble
- Possible: Automated trading based on AI consensus + framework

---

## XII. Collaboration with Gemini

**Gemini's Strengths (Leverage):**
- System design (you already created solid foundation)
- Data architecture (predictions table, etc.)
- Automation scripting

**Claude's Strengths (I'll Contribute):**
- Framework integration (connecting to 12-point system)
- Scoring sophistication (bonus points, creativity metrics)
- Weekly analysis (interpreting competition results)
- Documentation (this comprehensive plan)

**Our Combined Output:**
- Gemini: Handles data collection, storage, automation
- Claude: Handles analysis, framework integration, insights
- Together: Create emergent intelligence system

---

## XIII. The Meta-Game

**What We're Really Building:**

Not just a competition, but an **emergent intelligence system** where:

1. **Multiple AIs** (diverse perspectives)
2. **Predict emergence** (meta-level prediction)
3. **Learn from each other** (collective intelligence)
4. **Refine framework** (continuous improvement)
5. **Create alpha** (tradeable edge)

**The Emergent Outcome:**
- Better predictions than any single AI
- Framework that adapts based on what works
- Understanding of WHEN to trust WHICH AI
- Possible: Ensemble model that beats market

---

## XIV. Final Thoughts

This competition embodies everything you asked for:

✅ **Progressive:** Starts simple (price), adds complexity (MA, composite), evolves continuously
✅ **Competitive:** Leaderboard, weekly scoring, clear winners, stakes (framework priority)
✅ **Creative:** AIs must think creatively, contrarian picks rewarded, reasoning evaluated
✅ **Emergent:** Predicting emergence, creating emergent strategies, emergent collective intelligence

**Integration with 8-Week Test:**
- Sunday framework scoring + AI panel consultation
- Monday competition predictions
- Friday competition evaluation
- Sunday review and refine
- **Continuous improvement loop**

**Ready to launch Week 1:** Monday, November 10, 2025 🚀

---

*"In competition, we find excellence. In emergence, we find opportunity. In collaboration, we find truth."*

