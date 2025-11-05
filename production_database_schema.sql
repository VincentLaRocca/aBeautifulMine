-- WEMINEHOPE CRYPTOCURRENCY INTELLIGENCE DATABASE
-- Production Schema v1.0
-- Created: November 3, 2025
-- Purpose: Unified database for Q&A knowledge base, AI competition, and framework tracking

-- ============================================================================
-- KNOWLEDGE BASE TABLES (Cryptocurrency Indicator Q&A Pairs)
-- ============================================================================

CREATE TABLE IF NOT EXISTS crypto_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_name TEXT NOT NULL UNIQUE,
    indicator_category TEXT NOT NULL,
    session_number INTEGER,
    display_name TEXT,
    description TEXT,
    formula TEXT,
    typical_range TEXT,
    bullish_signal TEXT,
    bearish_signal TEXT,
    data_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS qa_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_id INTEGER NOT NULL,
    indicator_name TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    pair_number INTEGER,
    difficulty_level TEXT CHECK(difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    tags TEXT,  -- JSON array of tags
    answer_length INTEGER,
    has_formula BOOLEAN DEFAULT 0,
    has_examples BOOLEAN DEFAULT 0,
    has_sources BOOLEAN DEFAULT 0,
    crypto_specific BOOLEAN DEFAULT 1,
    market_year TEXT,  -- e.g., '2024', '2025' for recency tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (indicator_id) REFERENCES crypto_indicators(id)
);

CREATE TABLE IF NOT EXISTS batch_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_number INTEGER NOT NULL,
    batch_name TEXT,
    session_numbers TEXT,  -- JSON array
    total_indicators INTEGER,
    total_qa_pairs INTEGER,
    quality_score TEXT CHECK(quality_score IN ('A+', 'A', 'B', 'C', 'F')),
    delivery_date DATE,
    delivered_by TEXT,  -- 'Droid', 'Claude', 'Human'
    status TEXT CHECK(status IN ('delivered', 'validated', 'integrated', 'failed')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FRAMEWORK TRACKING TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS framework_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score_date DATE NOT NULL UNIQUE,
    week_number INTEGER,

    -- Macro Points (Outer Circle)
    point_1_fed_policy REAL CHECK(point_1_fed_policy BETWEEN 0 AND 1),
    point_2_money_supply REAL CHECK(point_2_money_supply BETWEEN 0 AND 1),
    point_3_stock_market REAL CHECK(point_3_stock_market BETWEEN 0 AND 1),
    point_4_global_liquidity REAL CHECK(point_4_global_liquidity BETWEEN 0 AND 1),

    -- Bitcoin Points (Middle Circle)
    point_5_cycle_position REAL CHECK(point_5_cycle_position BETWEEN 0 AND 1),
    point_6_onchain_lthoverlap REAL CHECK(point_6_onchain_lthoverlap BETWEEN 0 AND 1),
    point_7_onchain_cycle REAL CHECK(point_7_onchain_cycle BETWEEN 0 AND 1),
    point_8_institutional REAL CHECK(point_8_institutional BETWEEN 0 AND 1),

    -- Altcoin Points (Inner Circle)
    point_9_btc_dominance REAL CHECK(point_9_btc_dominance BETWEEN 0 AND 1),
    point_10_altcoin_season REAL CHECK(point_10_altcoin_season BETWEEN 0 AND 1),
    point_11_defi_metrics REAL CHECK(point_11_defi_metrics BETWEEN 0 AND 1),
    point_12_sector_rotation REAL CHECK(point_12_sector_rotation BETWEEN 0 AND 1),

    -- Calculated Totals
    macro_score REAL,
    bitcoin_score REAL,
    altcoin_score REAL,
    total_score REAL,

    -- Market Context
    btc_price REAL,
    eth_price REAL,
    total_market_cap REAL,
    btc_dominance REAL,

    -- Notes and Analysis
    market_regime TEXT,  -- 'calm', 'volatile', 'crisis'
    key_observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolio_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_date DATE NOT NULL,
    position_type TEXT CHECK(position_type IN ('total', 'core_hodl', 'living_expenses', 'trading')),

    -- Allocations (percentages)
    btc_allocation REAL,
    eth_allocation REAL,
    altcoin_allocation REAL,
    stablecoin_allocation REAL,

    -- Values (USD)
    total_value REAL,
    btc_value REAL,
    eth_value REAL,
    altcoin_value REAL,
    stablecoin_value REAL,

    -- Performance
    daily_change_pct REAL,
    weekly_change_pct REAL,
    since_inception_pct REAL,

    -- Actions Taken
    rebalance_action TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- AI COMPETITION TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL UNIQUE,
    agent_type TEXT,  -- 'claude', 'gemini', 'grok', 'custom'
    model_version TEXT,
    specialization TEXT,
    total_points INTEGER DEFAULT 0,
    competitions_entered INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    top_3_finishes INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weekly_competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER NOT NULL UNIQUE,
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,

    -- Market Context at Start
    btc_price_start REAL,
    eth_price_start REAL,
    total_mcap_start REAL,

    -- Market Context at End
    btc_price_end REAL,
    eth_price_end REAL,
    total_mcap_end REAL,

    -- Winner
    winning_agent_id INTEGER,
    winning_prediction TEXT,
    winning_points INTEGER,

    -- Actual Top Gainer
    actual_top_coin TEXT NOT NULL,
    actual_gain_pct REAL NOT NULL,
    actual_50w_ma_cross TEXT,  -- 'above', 'below', 'none'

    status TEXT CHECK(status IN ('upcoming', 'active', 'evaluating', 'complete')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (winning_agent_id) REFERENCES ai_agents(id)
);

CREATE TABLE IF NOT EXISTS weekly_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER NOT NULL,
    agent_id INTEGER NOT NULL,

    -- Prediction Details
    predicted_coin TEXT NOT NULL,
    confidence_score INTEGER CHECK(confidence_score BETWEEN 1 AND 10),
    prediction_reasoning TEXT,
    ma_50w_prediction TEXT CHECK(ma_50w_prediction IN ('cross_above', 'cross_below', 'no_cross', 'uncertain')),

    -- Prediction Context
    btc_sentiment TEXT,
    market_regime_prediction TEXT,

    -- Scoring
    points_earned INTEGER DEFAULT 0,
    rank_position INTEGER,
    base_points INTEGER DEFAULT 0,
    ma_cross_bonus INTEGER DEFAULT 0,
    jackpot_bonus INTEGER DEFAULT 0,
    confidence_bonus INTEGER DEFAULT 0,

    -- Meta
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evaluated BOOLEAN DEFAULT 0,
    evaluation_time TIMESTAMP,

    FOREIGN KEY (competition_id) REFERENCES weekly_competitions(id),
    FOREIGN KEY (agent_id) REFERENCES ai_agents(id),
    UNIQUE(competition_id, agent_id)
);

CREATE TABLE IF NOT EXISTS market_emergences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER NOT NULL,
    coin_symbol TEXT NOT NULL,
    coin_name TEXT,

    -- Performance
    gain_pct REAL NOT NULL,
    rank_position INTEGER,  -- 1 = top gainer, 2 = second, etc.

    -- Technical Analysis
    ma_50w_cross TEXT,  -- 'above', 'below', 'none'
    volume_change_pct REAL,

    -- Context
    market_cap_usd REAL,
    sector TEXT,  -- 'defi', 'gaming', 'ai', 'infrastructure', etc.

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(week_number, coin_symbol)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Knowledge Base Indexes
CREATE INDEX IF NOT EXISTS idx_qa_indicator ON qa_pairs(indicator_name);
CREATE INDEX IF NOT EXISTS idx_qa_difficulty ON qa_pairs(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_qa_length ON qa_pairs(answer_length);
CREATE INDEX IF NOT EXISTS idx_indicator_category ON crypto_indicators(indicator_category);
CREATE INDEX IF NOT EXISTS idx_indicator_session ON crypto_indicators(session_number);

-- Framework Indexes
CREATE INDEX IF NOT EXISTS idx_framework_date ON framework_scores(score_date);
CREATE INDEX IF NOT EXISTS idx_framework_week ON framework_scores(week_number);
CREATE INDEX IF NOT EXISTS idx_portfolio_date ON portfolio_positions(position_date);
CREATE INDEX IF NOT EXISTS idx_portfolio_type ON portfolio_positions(position_type);

-- Competition Indexes
CREATE INDEX IF NOT EXISTS idx_competition_week ON weekly_competitions(week_number);
CREATE INDEX IF NOT EXISTS idx_competition_status ON weekly_competitions(status);
CREATE INDEX IF NOT EXISTS idx_prediction_competition ON weekly_predictions(competition_id);
CREATE INDEX IF NOT EXISTS idx_prediction_agent ON weekly_predictions(agent_id);
CREATE INDEX IF NOT EXISTS idx_emergence_week ON market_emergences(week_number);
CREATE INDEX IF NOT EXISTS idx_emergence_rank ON market_emergences(rank_position);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Indicator Quality Summary
CREATE VIEW IF NOT EXISTS v_indicator_quality AS
SELECT
    i.indicator_name,
    i.indicator_category,
    i.session_number,
    COUNT(q.id) as total_pairs,
    AVG(q.answer_length) as avg_answer_length,
    SUM(CASE WHEN q.has_formula THEN 1 ELSE 0 END) as pairs_with_formulas,
    SUM(CASE WHEN q.has_examples THEN 1 ELSE 0 END) as pairs_with_examples,
    SUM(CASE WHEN q.has_sources THEN 1 ELSE 0 END) as pairs_with_sources,
    i.created_at
FROM crypto_indicators i
LEFT JOIN qa_pairs q ON i.id = q.indicator_id
GROUP BY i.id;

-- Agent Leaderboard
CREATE VIEW IF NOT EXISTS v_agent_leaderboard AS
SELECT
    a.agent_name,
    a.agent_type,
    a.total_points,
    a.competitions_entered,
    a.wins,
    a.top_3_finishes,
    ROUND(CAST(a.wins AS REAL) / NULLIF(a.competitions_entered, 0) * 100, 1) as win_rate_pct,
    ROUND(CAST(a.total_points AS REAL) / NULLIF(a.competitions_entered, 0), 1) as avg_points_per_week
FROM ai_agents a
WHERE a.active = 1
ORDER BY a.total_points DESC;

-- Framework Performance Over Time
CREATE VIEW IF NOT EXISTS v_framework_performance AS
SELECT
    f.score_date,
    f.week_number,
    f.total_score,
    f.btc_price,
    p.btc_allocation,
    p.total_value,
    LAG(p.total_value) OVER (ORDER BY f.score_date) as prev_week_value,
    ROUND((p.total_value - LAG(p.total_value) OVER (ORDER BY f.score_date)) /
          NULLIF(LAG(p.total_value) OVER (ORDER BY f.score_date), 0) * 100, 2) as weekly_change_pct
FROM framework_scores f
LEFT JOIN portfolio_positions p ON f.score_date = p.position_date AND p.position_type = 'total'
ORDER BY f.score_date DESC;

-- ============================================================================
-- INITIAL DATA SETUP
-- ============================================================================

-- Insert Initial AI Agents
INSERT OR IGNORE INTO ai_agents (agent_name, agent_type, model_version, specialization) VALUES
    ('Claude Sonnet 4.5', 'claude', 'claude-sonnet-4-5-20250929', 'Framework integration, systematic analysis'),
    ('Gemini 2.5 Pro', 'gemini', 'gemini-2.5-pro', 'Deep research, data generation'),
    ('Gemini 2.5 Flash', 'gemini', 'gemini-2.5-flash', 'Speed, pattern recognition'),
    ('Grok 2', 'grok', 'grok-2', 'Real-time data, social sentiment');

-- Insert Batch Metadata Placeholder (will be updated during import)
INSERT OR IGNORE INTO batch_metadata (batch_number, batch_name, session_numbers, delivered_by, status) VALUES
    (7, 'Droid Batch 7 - Extended Indicators', '["26-29", "38-44"]', 'Droid (Gemini)', 'delivered');

-- ============================================================================
-- DATABASE STATISTICS QUERY
-- ============================================================================

-- Run this to get database overview:
-- SELECT
--     'Total Indicators' as metric, COUNT(*) as value FROM crypto_indicators
-- UNION ALL SELECT 'Total Q&A Pairs', COUNT(*) FROM qa_pairs
-- UNION ALL SELECT 'Active Agents', COUNT(*) FROM ai_agents WHERE active = 1
-- UNION ALL SELECT 'Completed Competitions', COUNT(*) FROM weekly_competitions WHERE status = 'complete';
