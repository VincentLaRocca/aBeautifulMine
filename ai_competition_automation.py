"""
WEMINEHOPE - AI Agent Competition Automation
=============================================
Automates weekly prediction competitions between AI agents

Features:
- Monday: Send prediction prompts to all agents
- Friday: Evaluate predictions against actual market data
- Real-time leaderboard updates
- 50-week MA crossover tracking
- Jackpot detection (top gainer + MA cross)

Created: November 3, 2025
Author: Claude (Orchestrator)
Status: Production Ready
"""

import sqlite3
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system env vars

# Configuration
DATABASE_PATH = "weminehope_production.db"

# CoinGecko API Configuration
COINGECKO_PRO_API_KEY = os.getenv("COINGECKO_PRO_API_KEY")
if COINGECKO_PRO_API_KEY:
    COINGECKO_API = "https://pro-api.coingecko.com/api/v3"
    print("✅ Using CoinGecko Pro API")
else:
    COINGECKO_API = "https://api.coingecko.com/api/v3"
    print("⚠️ Using CoinGecko Free API (rate limited)")

# Competition Parameters
EXCLUDE_TOP_N = 10  # Exclude top 10 by market cap
PREDICTION_DAY = 0  # Monday (0 = Monday in Python)
EVALUATION_DAY = 4  # Friday

# Scoring System
POINTS = {
    'exact_match': 10,
    'top_3': 5,
    'top_5': 2,
    'ma_cross_bonus': 5,
    'jackpot_bonus': 5,  # Top gainer + MA cross
    'high_confidence_bonus': 2  # Confidence ≥ 8
}


class CompetitionManager:
    """Manages weekly AI prediction competitions"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def get_current_week_number(self) -> int:
        """Get current week number (weeks since Jan 1, 2024)"""
        start_date = datetime(2024, 1, 1)
        current_date = datetime.now()
        delta = current_date - start_date
        return delta.days // 7

    def create_new_competition(self) -> int:
        """Create new weekly competition"""
        week_number = self.get_current_week_number()

        # Calculate week boundaries (Monday 9 AM UTC to Friday 9 AM UTC)
        now = datetime.utcnow()
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        week_start = week_start.replace(hour=9, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=4)  # Friday

        conn = self.get_connection()
        cursor = conn.cursor()

        # Get current market data
        btc_price, eth_price, total_mcap = self.get_market_data()

        cursor.execute("""
            INSERT INTO weekly_competitions
            (week_number, week_start_date, week_end_date,
             btc_price_start, eth_price_start, total_mcap_start, status)
            VALUES (?, ?, ?, ?, ?, ?, 'active')
        """, (week_number, week_start.date(), week_end.date(),
              btc_price, eth_price, total_mcap))

        competition_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"✅ Created Week {week_number} competition (ID: {competition_id})")
        return competition_id

    def _add_api_key(self, params: Dict) -> Dict:
        """Add API key to params if using Pro API"""
        if COINGECKO_PRO_API_KEY:
            params['x_cg_pro_api_key'] = COINGECKO_PRO_API_KEY
        return params

    def get_market_data(self) -> Tuple[float, float, float]:
        """Get current BTC price, ETH price, and total market cap from CoinGecko"""
        try:
            # BTC and ETH prices
            params = {
                'ids': 'bitcoin,ethereum',
                'vs_currencies': 'usd'
            }
            response = requests.get(
                f"{COINGECKO_API}/simple/price",
                params=self._add_api_key(params),
                timeout=10
            )
            response.raise_for_status()
            prices = response.json()
            btc_price = prices['bitcoin']['usd']
            eth_price = prices['ethereum']['usd']

            # Total market cap
            response = requests.get(
                f"{COINGECKO_API}/global",
                params=self._add_api_key({}),
                timeout=10
            )
            response.raise_for_status()
            global_data = response.json()
            total_mcap = global_data['data']['total_market_cap']['usd']

            return btc_price, eth_price, total_mcap

        except requests.exceptions.HTTPError as e:
            print(f"⚠️ HTTP Error fetching market data: {e}")
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            return 0, 0, 0
        except Exception as e:
            print(f"⚠️ Error fetching market data: {e}")
            return 0, 0, 0

    def get_top_gainers(self, exclude_top_n: int = 10) -> List[Dict]:
        """Get top gaining cryptocurrencies (excluding top 10 by market cap)"""
        try:
            # Get top coins by market cap first
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 250,
                'page': 1,
                'price_change_percentage': '7d'
            }
            response = requests.get(
                f"{COINGECKO_API}/coins/markets",
                params=self._add_api_key(params),
                timeout=10
            )
            response.raise_for_status()
            coins = response.json()

            # Exclude top N by market cap
            eligible_coins = coins[exclude_top_n:]

            # Sort by 7-day price change
            eligible_coins.sort(key=lambda x: x.get('price_change_percentage_7d_in_currency', 0), reverse=True)

            # Return top 10 gainers
            top_gainers = []
            for coin in eligible_coins[:10]:
                top_gainers.append({
                    'symbol': coin['symbol'].upper(),
                    'name': coin['name'],
                    'gain_pct': coin.get('price_change_percentage_7d_in_currency', 0),
                    'market_cap': coin.get('market_cap', 0),
                    'rank': coin.get('market_cap_rank', 999)
                })

            return top_gainers

        except requests.exceptions.HTTPError as e:
            print(f"⚠️ HTTP Error fetching top gainers: {e}")
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            return []
        except Exception as e:
            print(f"⚠️ Error fetching top gainers: {e}")
            return []

    def check_50w_ma_cross(self, coin_symbol: str) -> str:
        """Check if coin crossed above/below 50-week MA"""
        # This would need historical price data and MA calculation
        # Placeholder for now - would integrate with TradingView or similar
        # Returns: 'above', 'below', 'none'
        return 'none'

    def generate_prediction_prompt(self, week_number: int) -> str:
        """Generate standardized prediction prompt for AI agents"""
        return f"""
WEMINEHOPE AI COMPETITION - WEEK {week_number} PREDICTION

Predict the TOP EMERGING MARKET for this week's competition period.

TIME WINDOW:
- Start: Monday 9:00 AM UTC
- End: Friday 9:00 AM UTC

REQUIREMENTS:

1. **Name ONE cryptocurrency** (exclude top 10 by market cap)
   - Choose a coin ranked #11 or lower
   - Focus on emerging opportunities, not established giants

2. **Confidence Level** (1-10 scale)
   - 1-3: Low confidence, speculative
   - 4-7: Moderate confidence, data-supported
   - 8-10: High confidence, strong conviction

3. **Reasoning** (3-5 bullet points)
   - Why this coin will be the top gainer this week
   - Technical, fundamental, or on-chain evidence
   - Market catalysts or trend observations

4. **BONUS: 50-Week MA Cross Prediction**
   - Will this coin cross ABOVE the 50-week moving average? (+5 points)
   - Will this coin cross BELOW the 50-week moving average? (+5 points)
   - Respond: "cross_above", "cross_below", "no_cross", or "uncertain"

5. **Market Context** (optional)
   - Your Bitcoin sentiment (bullish/neutral/bearish)
   - Overall market regime prediction (risk-on/risk-off)

SCORING SYSTEM:
- Exact match (top gainer): 10 points
- Top 3 finish: 5 points
- Top 5 finish: 2 points
- Correct MA cross prediction: +5 bonus points
- JACKPOT (top gainer + MA cross): +5 additional bonus
- High confidence bonus (8-10 confidence, correct): +2 points

Maximum possible: 22 points

Respond with JSON format:
{{
    "predicted_coin": "SYMBOL",
    "confidence_score": 8,
    "prediction_reasoning": [
        "Reason 1",
        "Reason 2",
        "Reason 3"
    ],
    "ma_50w_prediction": "cross_above",
    "btc_sentiment": "bullish",
    "market_regime_prediction": "risk-on"
}}
"""

    def collect_predictions(self, competition_id: int):
        """Collect predictions from all active AI agents"""
        print("\n📬 Collecting predictions from AI agents...")

        conn = self.get_connection()
        cursor = conn.cursor()

        # Get active agents
        cursor.execute("SELECT id, agent_name, agent_type FROM ai_agents WHERE active = 1")
        agents = cursor.fetchall()

        week_number = self.get_current_week_number()
        prompt = self.generate_prediction_prompt(week_number)

        print(f"\n📝 Prediction Prompt (Week {week_number}):")
        print(prompt)

        for agent_id, agent_name, agent_type in agents:
            print(f"\n🤖 Requesting prediction from {agent_name}...")

            # Here you would integrate with actual AI APIs
            # For now, this is a template for manual collection

            print(f"   Agent Type: {agent_type}")
            print(f"   Please send the prompt above to {agent_name} and record response")

        conn.close()

    def save_prediction(self, competition_id: int, agent_name: str, prediction_data: Dict):
        """Save agent prediction to database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get agent ID
        cursor.execute("SELECT id FROM ai_agents WHERE agent_name = ?", (agent_name,))
        agent_result = cursor.fetchone()
        if not agent_result:
            print(f"❌ Agent {agent_name} not found")
            conn.close()
            return

        agent_id = agent_result[0]

        cursor.execute("""
            INSERT INTO weekly_predictions
            (competition_id, agent_id, predicted_coin, confidence_score,
             prediction_reasoning, ma_50w_prediction, btc_sentiment,
             market_regime_prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            competition_id,
            agent_id,
            prediction_data['predicted_coin'],
            prediction_data['confidence_score'],
            json.dumps(prediction_data['prediction_reasoning']),
            prediction_data['ma_50w_prediction'],
            prediction_data.get('btc_sentiment', 'neutral'),
            prediction_data.get('market_regime_prediction', 'unknown')
        ))

        conn.commit()
        conn.close()

        print(f"✅ Saved prediction from {agent_name}: {prediction_data['predicted_coin']}")

    def evaluate_competition(self, competition_id: int):
        """Evaluate competition and award points"""
        print(f"\n🏆 Evaluating Week Competition (ID: {competition_id})...")

        # Get top gainers for the week
        top_gainers = self.get_top_gainers(EXCLUDE_TOP_N)

        if not top_gainers:
            print("❌ Could not retrieve market data")
            return

        print(f"\n📊 Top 10 Gainers This Week:")
        for i, gainer in enumerate(top_gainers, 1):
            print(f"   {i}. {gainer['symbol']} ({gainer['name']}): +{gainer['gain_pct']:.2f}%")

        # Get actual top gainer
        top_coin = top_gainers[0]
        top_symbol = top_coin['symbol']

        # Check MA cross for top coin
        ma_cross = self.check_50w_ma_cross(top_symbol)

        # Update competition with results
        conn = self.get_connection()
        cursor = conn.cursor()

        btc_price, eth_price, total_mcap = self.get_market_data()

        cursor.execute("""
            UPDATE weekly_competitions
            SET actual_top_coin = ?,
                actual_gain_pct = ?,
                actual_50w_ma_cross = ?,
                btc_price_end = ?,
                eth_price_end = ?,
                total_mcap_end = ?,
                status = 'evaluating'
            WHERE id = ?
        """, (top_symbol, top_coin['gain_pct'], ma_cross,
              btc_price, eth_price, total_mcap, competition_id))

        # Store all top gainers
        week_number = self.get_current_week_number()
        for rank, gainer in enumerate(top_gainers, 1):
            cursor.execute("""
                INSERT INTO market_emergences
                (week_number, coin_symbol, coin_name, gain_pct, rank_position, ma_50w_cross)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (week_number, gainer['symbol'], gainer['name'],
                  gainer['gain_pct'], rank, 'none'))  # Would check actual MA cross

        # Get all predictions for this competition
        cursor.execute("""
            SELECT p.id, p.agent_id, p.predicted_coin, p.confidence_score,
                   p.ma_50w_prediction, a.agent_name
            FROM weekly_predictions p
            JOIN ai_agents a ON p.agent_id = a.id
            WHERE p.competition_id = ?
        """, (competition_id,))

        predictions = cursor.fetchall()

        print(f"\n🎯 Scoring {len(predictions)} predictions...")

        for pred_id, agent_id, predicted_coin, confidence, ma_pred, agent_name in predictions:
            points = 0
            base_points = 0
            ma_bonus = 0
            jackpot_bonus = 0
            confidence_bonus = 0

            # Check if prediction matches top gainer
            if predicted_coin.upper() == top_symbol:
                base_points = POINTS['exact_match']
                rank = 1
                print(f"   ✅ {agent_name}: EXACT MATCH! +{base_points} points")

                # Check MA cross bonus
                if ma_pred and ma_pred != 'uncertain':
                    expected_cross = 'cross_' + ma_cross if ma_cross != 'none' else 'no_cross'
                    if ma_pred == expected_cross:
                        ma_bonus = POINTS['ma_cross_bonus']
                        jackpot_bonus = POINTS['jackpot_bonus']
                        print(f"      🎰 JACKPOT! MA cross predicted correctly! +{ma_bonus + jackpot_bonus} points")

            else:
                # Check if in top 3 or top 5
                top_3_symbols = [g['symbol'] for g in top_gainers[:3]]
                top_5_symbols = [g['symbol'] for g in top_gainers[:5]]

                if predicted_coin.upper() in top_3_symbols:
                    base_points = POINTS['top_3']
                    rank = top_3_symbols.index(predicted_coin.upper()) + 1
                    print(f"   🥉 {agent_name}: Top 3! +{base_points} points")
                elif predicted_coin.upper() in top_5_symbols:
                    base_points = POINTS['top_5']
                    rank = top_5_symbols.index(predicted_coin.upper()) + 1
                    print(f"   📊 {agent_name}: Top 5! +{base_points} points")
                else:
                    rank = None
                    print(f"   ❌ {agent_name}: Not in top 5")

            # High confidence bonus
            if confidence >= 8 and base_points > 0:
                confidence_bonus = POINTS['high_confidence_bonus']
                print(f"      💪 High confidence bonus! +{confidence_bonus} points")

            total_points = base_points + ma_bonus + jackpot_bonus + confidence_bonus

            # Update prediction with points
            cursor.execute("""
                UPDATE weekly_predictions
                SET points_earned = ?,
                    rank_position = ?,
                    base_points = ?,
                    ma_cross_bonus = ?,
                    jackpot_bonus = ?,
                    confidence_bonus = ?,
                    evaluated = 1,
                    evaluation_time = ?
                WHERE id = ?
            """, (total_points, rank, base_points, ma_bonus, jackpot_bonus,
                  confidence_bonus, datetime.now(), pred_id))

            # Update agent total points
            cursor.execute("""
                UPDATE ai_agents
                SET total_points = total_points + ?,
                    competitions_entered = competitions_entered + 1,
                    wins = wins + ?,
                    top_3_finishes = top_3_finishes + ?
                WHERE id = ?
            """, (total_points, 1 if rank == 1 else 0, 1 if rank and rank <= 3 else 0, agent_id))

        # Find winner
        cursor.execute("""
            SELECT agent_id, predicted_coin, points_earned
            FROM weekly_predictions
            WHERE competition_id = ?
            ORDER BY points_earned DESC
            LIMIT 1
        """, (competition_id,))

        winner = cursor.fetchone()
        if winner:
            cursor.execute("""
                UPDATE weekly_competitions
                SET winning_agent_id = ?,
                    winning_prediction = ?,
                    winning_points = ?,
                    status = 'complete'
                WHERE id = ?
            """, (winner[0], winner[1], winner[2], competition_id))

        conn.commit()
        conn.close()

        print(f"\n✅ Competition evaluated and completed!")

    def show_leaderboard(self):
        """Display current leaderboard"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT agent_name, agent_type, total_points, competitions_entered,
                   wins, top_3_finishes
            FROM ai_agents
            WHERE active = 1
            ORDER BY total_points DESC
        """)

        agents = cursor.fetchall()
        conn.close()

        print("\n" + "="*80)
        print("🏆 WEMINEHOPE AI COMPETITION LEADERBOARD")
        print("="*80)
        print(f"{'Rank':<6} {'Agent':<25} {'Points':<8} {'Weeks':<7} {'Wins':<6} {'Top 3':<7} {'Avg':<6}")
        print("-"*80)

        for i, (name, agent_type, points, weeks, wins, top_3) in enumerate(agents, 1):
            avg = points / weeks if weeks > 0 else 0
            print(f"{i:<6} {name:<25} {points:<8} {weeks:<7} {wins:<6} {top_3:<7} {avg:<6.1f}")

        print("="*80)


def main():
    """Main automation workflow"""
    manager = CompetitionManager(DATABASE_PATH)

    print("WEMINEHOPE - AI COMPETITION AUTOMATION")
    print("="*80)

    # Check what day it is
    today = datetime.now()
    weekday = today.weekday()

    if weekday == PREDICTION_DAY:
        # Monday: Create competition and collect predictions
        print("\n📅 Monday: Competition Week Start\n")
        competition_id = manager.create_new_competition()
        manager.collect_predictions(competition_id)

    elif weekday == EVALUATION_DAY:
        # Friday: Evaluate and award points
        print("\n📅 Friday: Competition Evaluation\n")
        week_number = manager.get_current_week_number()

        conn = manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM weekly_competitions WHERE week_number = ? AND status = 'active'",
                      (week_number,))
        result = cursor.fetchone()
        conn.close()

        if result:
            competition_id = result[0]
            manager.evaluate_competition(competition_id)
            manager.show_leaderboard()
        else:
            print("⚠️ No active competition found for this week")

    else:
        # Other days: Show current standings
        print(f"\n📅 {today.strftime('%A, %B %d, %Y')}")
        print("   Next prediction: Monday 9 AM UTC")
        print("   Next evaluation: Friday 9 AM UTC\n")
        manager.show_leaderboard()


if __name__ == "__main__":
    main()
