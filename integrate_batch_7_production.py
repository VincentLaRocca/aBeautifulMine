"""
WEMINEHOPE - Batch 7 Production Integration
============================================
Integrates Droid's Batch 7 delivery into production database
Handles quality validation and statistical reporting

Created: November 3, 2025
Author: Claude (Orchestrator)
Status: Production Ready
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict

# Configuration
DATABASE_PATH = "weminehope_production.db"
INBOX_PATH = Path("inbox/droid")
SCHEMA_PATH = "production_database_schema.sql"

# Quality Thresholds
MIN_ANSWER_LENGTH = 800  # words
MIN_PAIRS_PER_INDICATOR = 80
TARGET_PAIRS_PER_INDICATOR = 100

# Category Mapping (Session → Category)
CATEGORY_MAP = {
    31: "dex_metrics",
    32: "lending_protocol_metrics",
    33: "orderbook_indicators",
    34: "exchange_specific",
    35: "dominance_metrics",
    36: "market_cap_metrics",
    37: "correlation_metrics",
    26: "derivatives_metrics",
    27: "funding_metrics",
    28: "institutional_metrics",
    29: "protocol_metrics",
    38: "statistical_indicators",
    39: "cycle_indicators",
    40: "network_growth",
    41: "stablecoin_metrics",
    42: "nft_metrics",
    43: "nft_metrics_advanced",
    44: "token_specific"
}

# Session Mapping (Indicator Name → Session Number)
SESSION_MAP = {
    # Session 31: DEX Metrics
    "impermanent_loss": 31,
    "dex_volume_24h": 31,
    "dex_volume_7d": 31,
    "dex_volume_30d": 31,
    "dex_to_cex_volume_ratio": 31,
    "liquidity_pool_depth": 31,

    # Session 32: Lending Protocol
    "supply_rate": 32,
    "borrow_rate": 32,

    # Session 33: Orderbook
    "bid_ask_spread": 33,
    "delta_volume": 33,
    "market_buy_sell_ratio": 33,
    "maker_buy_sell_volume": 33,
    "taker_buy_sell_volume": 33,
    "footprint_charts": 33,

    # Session 34: Exchange Specific
    "exchange_netflows": 34,
    "exchange_reserve": 34,

    # Session 35: Dominance
    "bitcoin_dominance_btc.d": 35,
    "ethereum_dominance_eth.d": 35,
    "stablecoin_dominance": 35,

    # Session 36: Market Cap
    "total_crypto_market_cap": 36,
    "market_cap_growth_rate": 36,
    "total3_total_market_cap___bitcoin___ethereum": 36,

    # Session 37: Correlation
    "crypto_to_gold_correlation": 37,
    "crypto_to_stock_market_correlation": 37,
    "altcoin_correlation_to_btc": 37,
    "bollinger_band_width": 37,

    # Session 28: Institutional
    "grayscale_holdings": 28,

    # Session 34: Exchange Events
    "liquidation_events": 34,

    # Session 35: Market Structure
    "altcoin_season_index": 35,
}


class BatchIntegrator:
    """Handles integration of Batch 7 Q&A pairs into production database"""

    def __init__(self, db_path: str, inbox_path: Path, schema_path: str):
        self.db_path = db_path
        self.inbox_path = inbox_path
        self.schema_path = schema_path
        self.stats = defaultdict(int)
        self.quality_issues = []

    def initialize_database(self):
        """Create database and tables from schema"""
        print("🔧 Initializing production database...")

        with open(self.schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        conn = sqlite3.connect(self.db_path)
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

        print(f"✅ Database initialized: {self.db_path}")

    def get_json_files(self) -> List[Path]:
        """Get all JSON Q&A pair files from inbox"""
        json_files = list(self.inbox_path.glob("*_qa_pairs.json"))
        print(f"\n📁 Found {len(json_files)} JSON files in {self.inbox_path}")
        return sorted(json_files)

    def categorize_file_by_size(self, file_path: Path) -> str:
        """Categorize file as excellent, acceptable, or failed based on size"""
        size_kb = file_path.stat().st_size / 1024

        if size_kb >= 100:
            return "excellent"  # Likely 100 pairs with good content
        elif size_kb >= 50:
            return "acceptable"  # Maybe 50-80 pairs
        elif size_kb >= 10:
            return "needs_review"  # Suspiciously small
        else:
            return "failed"  # Almost certainly incomplete

    def parse_indicator_name(self, file_path: Path) -> str:
        """Extract clean indicator name from filename"""
        filename = file_path.stem
        # Remove _qa_pairs suffix
        indicator_name = filename.replace('_qa_pairs', '')
        return indicator_name

    def load_json_file(self, file_path: Path) -> Dict:
        """Load and parse JSON file with error handling"""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except UnicodeDecodeError:
            # Try UTF-16 if UTF-8 fails (handles grayscale_holdings issue)
            try:
                with open(file_path, 'r', encoding='utf-16') as f:
                    data = json.load(f)
                self.quality_issues.append(f"⚠️ {file_path.name}: UTF-16 encoding (should be UTF-8)")
                return data
            except Exception as e:
                self.quality_issues.append(f"❌ {file_path.name}: Failed to load - {e}")
                return None
        except json.JSONDecodeError as e:
            self.quality_issues.append(f"❌ {file_path.name}: Invalid JSON - {e}")
            return None
        except Exception as e:
            self.quality_issues.append(f"❌ {file_path.name}: Unknown error - {e}")
            return None

    def analyze_answer_quality(self, answer: str) -> Dict:
        """Analyze answer for quality metrics"""
        word_count = len(answer.split())

        # Check for formulas (mathematical expressions)
        has_formula = bool(re.search(r'[=×÷\+\-\*/]|\b(formula|calculation|equation)\b', answer.lower()))

        # Check for examples (2024, 2025, specific coins/protocols)
        has_examples = bool(re.search(r'(2024|2025|bitcoin|ethereum|uniswap|aave|example)', answer.lower()))

        # Check for sources (citations, references)
        has_sources = bool(re.search(r'(source|according to|cited|reference|binance|coinbase|coingecko|messari)', answer.lower()))

        # Check crypto-specific terms
        crypto_terms = ['bitcoin', 'ethereum', 'blockchain', 'cryptocurrency', 'defi', 'dex', 'protocol', 'wallet', 'hash']
        has_crypto_context = any(term in answer.lower() for term in crypto_terms)

        return {
            'word_count': word_count,
            'has_formula': has_formula,
            'has_examples': has_examples,
            'has_sources': has_sources,
            'crypto_specific': has_crypto_context
        }

    def determine_session(self, indicator_name: str) -> int:
        """Determine session number from indicator name"""
        return SESSION_MAP.get(indicator_name, 0)  # 0 = unknown

    def determine_category(self, indicator_name: str) -> str:
        """Determine category from indicator name and session"""
        session = self.determine_session(indicator_name)
        return CATEGORY_MAP.get(session, "uncategorized")

    def insert_indicator(self, conn: sqlite3.Connection, indicator_name: str, data: Dict) -> int:
        """Insert indicator into crypto_indicators table"""
        session = self.determine_session(indicator_name)
        category = self.determine_category(indicator_name)

        # Clean display name
        display_name = indicator_name.replace('_', ' ').title()

        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO crypto_indicators
            (indicator_name, indicator_category, session_number, display_name, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (indicator_name, category, session, display_name, datetime.now()))

        conn.commit()

        # Get the ID
        cursor.execute("SELECT id FROM crypto_indicators WHERE indicator_name = ?", (indicator_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def insert_qa_pairs(self, conn: sqlite3.Connection, indicator_id: int, indicator_name: str, qa_pairs: List[Dict]) -> int:
        """Insert Q&A pairs into qa_pairs table"""
        inserted = 0

        cursor = conn.cursor()

        for qa in qa_pairs:
            question = qa.get('question', '')
            answer = qa.get('answer', '')
            pair_number = qa.get('pair_number', 0)

            if not question or not answer:
                continue

            # Analyze quality
            quality = self.analyze_answer_quality(answer)

            # Determine difficulty (heuristic based on answer length and complexity)
            if quality['word_count'] < 500:
                difficulty = 'beginner'
            elif quality['word_count'] < 1000:
                difficulty = 'intermediate'
            else:
                difficulty = 'advanced'

            # Extract market year mentions
            market_year = '2025' if '2025' in answer else ('2024' if '2024' in answer else None)

            cursor.execute("""
                INSERT INTO qa_pairs
                (indicator_id, indicator_name, question, answer, pair_number,
                 difficulty_level, answer_length, has_formula, has_examples,
                 has_sources, crypto_specific, market_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                indicator_id, indicator_name, question, answer, pair_number,
                difficulty, quality['word_count'], quality['has_formula'],
                quality['has_examples'], quality['has_sources'],
                quality['crypto_specific'], market_year
            ))

            inserted += 1

        conn.commit()
        return inserted

    def process_file(self, conn: sqlite3.Connection, file_path: Path) -> Tuple[str, int, Dict]:
        """Process single JSON file and insert into database"""
        indicator_name = self.parse_indicator_name(file_path)
        size_category = self.categorize_file_by_size(file_path)

        # Load JSON
        data = self.load_json_file(file_path)
        if not data:
            return indicator_name, 0, {'status': 'failed', 'reason': 'load_error'}

        # Extract Q&A pairs
        qa_pairs = data.get('qa_pairs', [])
        total_pairs = len(qa_pairs)

        if total_pairs == 0:
            return indicator_name, 0, {'status': 'failed', 'reason': 'no_pairs'}

        # Insert indicator
        indicator_id = self.insert_indicator(conn, indicator_name, data)
        if not indicator_id:
            return indicator_name, 0, {'status': 'failed', 'reason': 'insert_error'}

        # Insert Q&A pairs
        inserted = self.insert_qa_pairs(conn, indicator_id, indicator_name, qa_pairs)

        # Determine quality status
        if inserted >= TARGET_PAIRS_PER_INDICATOR and size_category == 'excellent':
            status = 'excellent'
        elif inserted >= MIN_PAIRS_PER_INDICATOR:
            status = 'acceptable'
        elif inserted >= 10:
            status = 'needs_review'
        else:
            status = 'failed'

        return indicator_name, inserted, {
            'status': status,
            'size_category': size_category,
            'total_in_file': total_pairs,
            'session': self.determine_session(indicator_name),
            'category': self.determine_category(indicator_name)
        }

    def integrate_all_files(self):
        """Main integration process"""
        print("\n🚀 Starting Batch 7 Integration...")

        json_files = self.get_json_files()

        if not json_files:
            print("❌ No JSON files found in inbox!")
            return

        conn = sqlite3.connect(self.db_path)

        results = {
            'excellent': [],
            'acceptable': [],
            'needs_review': [],
            'failed': []
        }

        print("\n📊 Processing files...\n")

        for file_path in json_files:
            indicator_name, inserted, metadata = self.process_file(conn, file_path)
            status = metadata['status']

            results[status].append({
                'name': indicator_name,
                'pairs': inserted,
                'file': file_path.name,
                **metadata
            })

            # Status emoji
            emoji = {
                'excellent': '✅',
                'acceptable': '⚠️',
                'needs_review': '🔍',
                'failed': '❌'
            }[status]

            print(f"{emoji} {indicator_name}: {inserted} pairs ({status})")

            self.stats['total_files'] += 1
            self.stats['total_pairs'] += inserted
            self.stats[f'{status}_count'] += 1

        conn.close()

        return results

    def generate_report(self, results: Dict):
        """Generate comprehensive integration report"""
        print("\n" + "="*80)
        print("BATCH 7 INTEGRATION REPORT")
        print("="*80)

        print(f"\n📦 DELIVERY SUMMARY:")
        print(f"   Total Files Processed: {self.stats['total_files']}")
        print(f"   Total Q&A Pairs Imported: {self.stats['total_pairs']:,}")

        print(f"\n🎯 QUALITY BREAKDOWN:")
        print(f"   ✅ Excellent (100+ pairs):  {self.stats['excellent_count']} indicators")
        print(f"   ⚠️  Acceptable (80-99):     {self.stats['acceptable_count']} indicators")
        print(f"   🔍 Needs Review (10-79):   {self.stats['needs_review_count']} indicators")
        print(f"   ❌ Failed (<10 pairs):     {self.stats['failed_count']} indicators")

        if results['excellent']:
            print(f"\n✅ EXCELLENT INDICATORS ({len(results['excellent'])}):")
            for item in sorted(results['excellent'], key=lambda x: x['pairs'], reverse=True)[:10]:
                print(f"   • {item['name']}: {item['pairs']} pairs (Session {item['session']})")
            if len(results['excellent']) > 10:
                print(f"   ... and {len(results['excellent']) - 10} more")

        if results['failed']:
            print(f"\n❌ FAILED INDICATORS ({len(results['failed'])}):")
            for item in results['failed']:
                print(f"   • {item['name']}: {item['pairs']} pairs - {item.get('reason', 'unknown')}")

        if self.quality_issues:
            print(f"\n⚠️  QUALITY ISSUES ({len(self.quality_issues)}):")
            for issue in self.quality_issues[:10]:
                print(f"   {issue}")

        print(f"\n📈 DATABASE STATUS:")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM crypto_indicators")
        total_indicators = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM qa_pairs")
        total_pairs_db = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(answer_length) FROM qa_pairs")
        avg_length = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM qa_pairs WHERE has_sources = 1")
        with_sources = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM qa_pairs WHERE crypto_specific = 1")
        crypto_specific = cursor.fetchone()[0]

        conn.close()

        print(f"   Total Indicators: {total_indicators}")
        print(f"   Total Q&A Pairs: {total_pairs_db:,}")
        print(f"   Average Answer Length: {int(avg_length)} words")
        print(f"   With Sources: {with_sources:,} ({with_sources/total_pairs_db*100:.1f}%)")
        print(f"   Crypto-Specific: {crypto_specific:,} ({crypto_specific/total_pairs_db*100:.1f}%)")

        print("\n" + "="*80)
        print("INTEGRATION COMPLETE ✅")
        print("="*80)


def main():
    """Main execution"""
    print("="*80)
    print("WEMINEHOPE - BATCH 7 PRODUCTION INTEGRATION")
    print("="*80)

    integrator = BatchIntegrator(DATABASE_PATH, INBOX_PATH, SCHEMA_PATH)

    # Step 1: Initialize database
    integrator.initialize_database()

    # Step 2: Integrate all files
    results = integrator.integrate_all_files()

    if results:
        # Step 3: Generate report
        integrator.generate_report(results)

        # Step 4: Save detailed results to JSON
        output_file = f"integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'stats': dict(integrator.stats),
                'results': results,
                'quality_issues': integrator.quality_issues
            }, f, indent=2)

        print(f"\n📄 Detailed report saved: {output_file}")
    else:
        print("\n❌ Integration failed - no results to report")


if __name__ == "__main__":
    main()
