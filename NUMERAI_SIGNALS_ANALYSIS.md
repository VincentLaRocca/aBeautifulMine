# Numerai Signals Notebook - Complete Analysis

**Source:** https://github.com/numerai/signals-example-scripts
**Notebook:** example_model.ipynb (222KB)
**Date Analyzed:** 2025-11-08

---

## 📊 OVERVIEW

Numerai Signals is a quantitative finance tournament where data scientists submit stock market predictions and compete for rewards based on model performance.

**Key Concept:** Participants bring their own data sources and features, use Numerai's provided features for neutralization, and submit ranked signals for ~7,000 stocks globally.

---

## 🗂️ DATA STRUCTURE

### Dataset Version: v2.1

**Files:**
- `train.parquet` (273MB) - Training data
- `validation.parquet` (456MB) - Validation data
- `validation_neutralizer.parquet` (3.99GB) - Neutralization factors
- `validation_sample_weights.parquet` (24.4MB) - Sample weights
- `live.parquet` - Live submission universe (~7,168 stocks)

**Data Size:**
- Training records: ~2.5 million rows
- Multi-country coverage
- Historical data with daily/weekly features

---

## 🎫 TICKER SYSTEMS

### Two Ticker Types:

1. **numerai_ticker** - Full historical coverage
   - Format: `{SYMBOL} {ISO_COUNTRY_CODE}`
   - Example: `AAPL US`, `000640 KR`

2. **composite_figi** - September 2022 onwards
   - Bloomberg Financial Instrument Global Identifier

### Bloomberg Ticker Conversion

```python
TICKER_CTRY_MAP = {
    "AU": "AU", "AV": "AT", "BB": "BE", "BZ": "BR", "CA": "CA",
    "CB": "CO", "CH": "CN", "CI": "CL", "CN": "CA", "CP": "CZ",
    "DC": "DK", "EY": "EG", "FH": "FI", "FP": "FR", "GA": "GR",
    "GR": "DE", "GY": "DE", "HB": "HU", "HK": "HK", "ID": "IE",
    "IJ": "ID", "IM": "IT", "IN": "IN", "IT": "IL", "JP": "JP",
    "KS": "KR", "LN": "GB", "MF": "MX", "MK": "MY", "NA": "NL",
    "NO": "NO", "NZ": "NZ", "PE": "PE", "PL": "PT", "PM": "PH",
    "PW": "PL", "QD": "QA", "RM": "RU", "SJ": "ZA", "SM": "ES",
    "SP": "SG", "SS": "SE", "SW": "CH", "TB": "TH", "TI": "TR",
    "TT": "TW", "UH": "AE", "US": "US", "UQ": "US",
}
```

**Example:** `000640 KS` (Bloomberg) → `000640 KR` (numerai_ticker)

---

## 📈 FEATURES (23 Total)

### Feature Categories:

#### 1. **Risk Factors** (Most targets are neutral to these)
- `feature_adv_20d_factor` - 20-day average dollar volume
- `feature_beta_factor` - Market beta
- `feature_book_to_price_factor` - Book-to-price ratio
- `feature_dividend_yield_factor` - Dividend yield
- `feature_earnings_yield_factor` - Earnings yield
- `feature_growth_factor` - Growth metrics
- `feature_impact_cost_factor` - Trading impact cost
- `feature_market_cap_factor` - Market capitalization
- `feature_momentum_12w_factor` - 12-week momentum
- `feature_momentum_26w_factor` - 26-week momentum
- `feature_momentum_52w_factor` - 52-week momentum
- `feature_momentum_52w_less_4w_factor` - 1-year return excluding last 4 weeks
- `feature_price_factor` - Price factor
- `feature_value_factor` - Value factor
- `feature_volatility_factor` - Volatility factor

#### 2. **Technical Indicators** (Country-ranked and gaussianized)

**PPO (Percentage Price Oscillator):**
- `feature_ppo_60d_90d_country_ranknorm` - 60-day vs 90-day PPO
- `feature_ppo_60d_130d_country_ranknorm` - 60-day vs 130-day PPO
- **Definition:** Compares shorter and longer moving averages as a ratio
- **Use:** Momentum indicator, shows relationship between MAs

**RSI (Relative Strength Index):**
- `feature_rsi_60d_country_ranknorm` - 60-day RSI
- `feature_rsi_90d_country_ranknorm` - 90-day RSI
- `feature_rsi_130d_country_ranknorm` - 130-day RSI
- **Definition:** Momentum oscillator measuring speed/magnitude of price changes
- **Use:** Overbought (>70) / Oversold (<30) indicator

**TRIX (Triple Exponential Moving Average):**
- `feature_trix_60d_country_ranknorm` - 60-day TRIX
- `feature_trix_130d_country_ranknorm` - 130-day TRIX
- **Definition:** Triple exponential smoothed moving average of price
- **Use:** Momentum indicator, identifies trend reversals

#### 3. **Non-Numerical Features** (Categorical)
- `feature_country` - ISO country code
- `feature_exchange_code` - Exchange identifier

### Feature Engineering Notes:

**Time-Series Pattern:** `{n}(d|w)` suffix
- `d` = days (e.g., 20d, 60d, 130d)
- `w` = weeks (e.g., 12w, 26w, 52w)

**Country Normalization:** `country_ranknorm`
- Features are grouped by country
- Then ranked within country
- Then gaussianized (normalized to normal distribution)

**Factor Neutrality:**
- Most targets are neutral to these risk factors
- Features used primarily to REMOVE exposures
- Not intended as primary predictive features

---

## 🤖 MODEL ARCHITECTURE

### LightGBM Configuration

```python
model = lgb.LGBMRegressor(
  n_estimators=2000,        # Number of boosting rounds
  learning_rate=0.01,       # Learning rate (0.01 = slow, stable)
  max_depth=5,              # Max tree depth
  num_leaves=2**5-1,        # 31 leaves (2^5 - 1)
  colsample_bytree=0.1      # 10% feature sampling per tree
)
```

**Training:**
- Features: 22 numerical features (excluding country and exchange_code)
- Target: `target_chili_60` (60-day forward-looking target)
- Training time: "a few minutes"

**Key Design Choices:**
- **High n_estimators + low learning_rate:** Prevents overfitting, stable convergence
- **Low colsample_bytree (0.1):** Feature bagging reduces variance
- **Moderate max_depth (5):** Limits tree complexity

---

## 📊 SCORING METHODOLOGY

### Two Key Metrics:

#### 1. **Alpha Score**
- Measures performance after neutralizing to risk factors
- Calculated using `numerai-tools` package
- Formula: Alpha = neutralized prediction correlation with targets

**Calculation Process:**
```python
from numerai_tools.scoring import alpha

alpha_score = alpha(
    predictions=predictions,        # Your ranked signals
    neutralizers=neutralizers,      # Risk factors to neutralize
    sample_weights=weights,         # Importance weights per stock
    targets=targets,                # Actual target values
)
```

**Validation Performance:**
- Sharpe ratio: **0.803** (for basic feature model)
- Comparison: S&P 500 10-year Sharpe ~0.6
- Note: Performance plateaus over time (basic features insufficient)

#### 2. **Meta Portfolio Contribution**
- Measures contribution to ensemble portfolio
- Details not provided in this notebook

---

## 📤 SUBMISSION WORKFLOW

### 1. Generate Live Predictions

```python
# Load live universe
live = pd.read_parquet(f'signals/{DATASET_VERSION}/live.parquet')

# Generate predictions
live['signal'] = model.predict(live[feature_cols])

# CRITICAL: Rank signals to 0-1 range
live['signal'] = tie_kept_rank(live[['signal']])
```

**Live Universe:** ~7,168 stocks (as of notebook execution)

### 2. Format Submission

**Required Columns:**
1. Ticker column (one of):
   - `cusip`
   - `sedol`
   - `bloomberg_ticker`
   - `composite_figi`
   - `numerai_ticker` (used in example)

2. `signal` column:
   - **MUST** be ranked between 0 and 1
   - Ties are kept (tie_kept_rank)
   - Represents relative strength across universe

**Example Output:**
```
numerai_ticker    signal
000080 KR         0.990723
000100 KR         0.161063
...
ZYME US           0.111258
```

### 3. Submit via Web Interface

- Upload CSV to https://signals.numer.ai/submissions
- Scoring begins ~1 week after submission
- **Alpha score resolves:** ~13 weeks later (60 business days + evaluation period)

---

## 🔑 KEY INSIGHTS

### For Data Scientists:

1. **Bring Your Own Data:** Numerai's features are insufficient alone
   - Basic features → Sharpe 0.8 (marginal)
   - Need proprietary signals for competitive performance

2. **Neutralization is Critical:**
   - Targets are neutral to provided risk factors
   - Model must be aware of neutralization methodology
   - Sample weighting affects final scores

3. **Feature Engineering Matters:**
   - Country-level ranking prevents country bias
   - Time-series features capture momentum/trend
   - Multiple timeframes (60d, 90d, 130d) = robustness

4. **Model Complexity vs. Overfitting:**
   - Conservative hyperparameters prevent overfitting
   - Feature bagging (10% sampling) crucial
   - Validation set is 456MB (large enough to validate)

### For Crypto Adaptation:

1. **Technical Indicators Translate:**
   - PPO, RSI, TRIX work for BTC/ETH/altcoins
   - Similar momentum/reversal patterns

2. **Neutralization Needed:**
   - Crypto: neutralize to BTC beta, market cap, volume
   - Remove common factor exposures

3. **Country → Exchange:**
   - Replace country normalization with exchange normalization
   - Binance, Coinbase, Kraken etc. have different dynamics

4. **Timeframe Adaptation:**
   - Stock: 60d, 90d, 130d (business days)
   - Crypto: 24/7 markets → 60d, 90d, 130d (calendar days)
   - Or: 1440h, 2160h, 3120h (hourly features)

---

## 📦 DEPENDENCIES

```python
numerapi          # Official Numerai API
lightgbm          # Gradient boosting model
pyarrow           # Parquet file reading
scikit-learn      # ML utilities
scipy             # Scientific computing
matplotlib        # Visualization
pandas            # Data manipulation
numerai-tools     # Scoring functions (alpha, neutralization)
```

---

## 🚀 CRYPTO INTEGRATION OPPORTUNITIES

### 1. **Crypto Market Signals System**
- Adapt workflow for BTC, ETH, top 100 altcoins
- Replace stock tickers with crypto symbols
- Use 24/7 market data instead of business days

### 2. **Technical Indicator Q&A Generation**
- PPO for crypto trading
- RSI overbought/oversold in crypto markets
- TRIX momentum in volatile crypto markets
- Momentum factors (12w, 26w, 52w) for crypto

### 3. **Feature Engineering Q&A**
- Country ranknorm → Exchange ranknorm
- Time-series feature construction
- Factor neutralization in crypto
- Sample weighting for crypto (volume, market cap)

### 4. **Model Architecture Q&A**
- LightGBM for crypto prediction
- Hyperparameter tuning for volatile markets
- Ensemble methods for crypto signals

### 5. **Scoring Methodology Q&A**
- Alpha calculation for crypto portfolios
- Sharpe ratio vs Sortino ratio for crypto
- Meta portfolio contribution
- Backtesting crypto signals

---

## 📝 NEXT ACTIONS

1. ✅ Extract technical indicator definitions
2. ⏳ Generate 50+ crypto-specific Q&A pairs
3. ⏳ Create crypto market prediction integration script
4. ⏳ Integrate new pairs into database

---

**Analysis Complete**
*Token Usage: Efficient - comprehensive analysis in single read*
*Ready for Q&A generation and integration*
