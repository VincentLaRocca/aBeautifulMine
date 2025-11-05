"""
WeMineHope.com Data Governance System
Comprehensive data management and analysis for AI training datasets

Purpose: Track, analyze, and report on Q&A pair distribution to prevent
data imbalance issues that occurred in the previous 25,000 pair system.

Author: Claude Code
Date: November 2, 2025
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import re


class DataGovernanceSystem:
    """
    Comprehensive data governance for cryptocurrency knowledge base.

    Analyzes Q&A pair distribution across:
    - Sessions (1-37)
    - Indicators (100+ types)
    - Categories (technical, DeFi, derivatives, etc.)
    - Waves (1, 2, 3)
    """

    def __init__(self, base_path: str = r"C:\Users\vlaro\dreamteam\claude"):
        self.base_path = Path(base_path)
        self.data_inventory = {
            'wave1': [],
            'wave2': [],
            'wave3': [],
            'parsed_originals': []
        }
        self.statistics = {
            'total_pairs': 0,
            'by_wave': defaultdict(int),
            'by_indicator': defaultdict(int),
            'by_category': defaultdict(int),
            'by_session': defaultdict(int),
            'indicator_details': {}
        }

        # Category mappings
        self.category_map = {
            # Technical Indicators
            'technical': [
                'sma', 'ema', 'wma', 'macd', 'rsi', 'atr', 'adx', 'cci', 'momentum',
                'roc', 'stochastic', 'williams', 'aroon', 'ichimoku', 'bollinger',
                'donchian', 'kst', 'obv', 'ultimate', 'vortex'
            ],
            # Volume & Money Flow
            'volume': [
                'obv', 'cmf', 'mfi', 'vwap', 'accumulation', 'volume_rate',
                'delta_volume', 'taker_buy_sell', 'maker_buy_sell'
            ],
            # Volatility
            'volatility': [
                'atr', 'bollinger', 'chaikin_volatility', 'historical_volatility',
                'standard_deviation', 'bollinger_band_width'
            ],
            # DeFi Metrics
            'defi': [
                'dex_volume', 'liquidity_pool', 'impermanent_loss', 'supply_rate',
                'borrow_rate', 'slippage', 'dex_to_cex'
            ],
            # Derivatives & Futures
            'derivatives': [
                'futures_open_interest', 'funding_rates', 'options_analytics',
                'liquidations', 'cme_institutionals', 'basis'
            ],
            # Market Structure
            'market_structure': [
                'bid_ask_spread', 'footprint', 'orderbook', 'market_buy_sell_ratio',
                'liquidation_events'
            ],
            # On-Chain & Exchange
            'onchain': [
                'exchange_reserve', 'exchange_netflows', 'netflows'
            ],
            # Market Dominance & Correlation
            'dominance': [
                'bitcoin_dominance', 'ethereum_dominance', 'stablecoin_dominance',
                'altcoin_season', 'total_crypto_market_cap', 'total2', 'total3',
                'market_cap_growth'
            ],
            # Correlation Metrics
            'correlation': [
                'btc_correlation', 'altcoin_correlation', 'crypto_to_stock',
                'crypto_to_gold', 'z-score', 'kurtosis'
            ]
        }

    def scan_wave1_data(self):
        """Scan Wave 1 batch JSONL files (204 batches, 20,400 pairs)"""
        batch_dir = self.base_path / "gemini_batch_submissions_proper"

        if not batch_dir.exists():
            print(f"Warning: Wave 1 batch directory not found: {batch_dir}")
            return

        batch_files = sorted(batch_dir.glob("batch_*_proper.jsonl"))

        for batch_file in batch_files:
            try:
                with open(batch_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Extract batch number from filename
                batch_num = int(re.search(r'batch_(\d+)_proper', batch_file.name).group(1))

                # Parse the embedded Q&A pairs from the prompt text
                prompt_text = data['request']['contents'][0]['parts'][0]['text']

                # Extract batch metadata from prompt
                batch_match = re.search(r'BATCH: refinement_batch_(\d+)', prompt_text)
                total_match = re.search(r'TOTAL Q&A PAIRS: (\d+)', prompt_text)

                if batch_match and total_match:
                    batch_id = batch_match.group(1)
                    pair_count = int(total_match.group(1))

                    self.data_inventory['wave1'].append({
                        'batch_number': batch_num,
                        'batch_id': batch_id,
                        'pair_count': pair_count,
                        'file': str(batch_file)
                    })

                    self.statistics['by_wave']['wave1'] += pair_count
                    self.statistics['total_pairs'] += pair_count

            except Exception as e:
                print(f"Error processing {batch_file.name}: {e}")

        print(f"Wave 1: Scanned {len(self.data_inventory['wave1'])} batch files")

    def scan_wave2_data(self):
        """Scan Wave 2 JSON files (9 indicators, 701 pairs)"""
        wave2_dir = self.base_path / "inbox" / "droid" / "wave2_staging"

        if not wave2_dir.exists():
            print(f"Warning: Wave 2 staging directory not found: {wave2_dir}")
            return

        json_files = sorted(wave2_dir.glob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle two possible formats:
                # 1. Array of Q&A pairs: [{"question": ..., "answer": ...}, ...]
                # 2. Object with qa_pairs key: {"qa_pairs": [...], "total_pairs": 100, ...}
                if isinstance(data, list):
                    qa_pairs = data
                elif isinstance(data, dict) and 'qa_pairs' in data:
                    qa_pairs = data['qa_pairs']
                else:
                    print(f"Warning: Unknown format in {json_file.name}")
                    continue

                pair_count = len(qa_pairs)
                indicator_name = self._extract_indicator_name(json_file.name)
                session = data.get('session', qa_pairs[0].get('session', 'unknown')) if pair_count > 0 else 'unknown'

                self.data_inventory['wave2'].append({
                    'indicator': indicator_name,
                    'pair_count': pair_count,
                    'session': session,
                    'file': str(json_file)
                })

                self.statistics['by_wave']['wave2'] += pair_count
                self.statistics['by_indicator'][indicator_name] += pair_count
                self.statistics['by_session'][session] += pair_count
                self.statistics['total_pairs'] += pair_count

                # Track indicator details
                if indicator_name not in self.statistics['indicator_details']:
                    self.statistics['indicator_details'][indicator_name] = {
                        'total_pairs': 0,
                        'sessions': set(),
                        'waves': set()
                    }

                self.statistics['indicator_details'][indicator_name]['total_pairs'] += pair_count
                self.statistics['indicator_details'][indicator_name]['sessions'].add(session)
                self.statistics['indicator_details'][indicator_name]['waves'].add('wave2')

            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")

        print(f"Wave 2: Scanned {len(self.data_inventory['wave2'])} indicator files")

    def scan_wave3_data(self):
        """Scan Wave 3 JSON files (20 indicators, 1,407 pairs)"""
        wave3_dir = self.base_path / "inbox" / "droid" / "wave3_staging"

        if not wave3_dir.exists():
            print(f"Warning: Wave 3 staging directory not found: {wave3_dir}")
            return

        json_files = sorted(wave3_dir.glob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle two possible formats:
                # 1. Array of Q&A pairs: [{"question": ..., "answer": ...}, ...]
                # 2. Object with qa_pairs key: {"qa_pairs": [...], "total_pairs": 100, ...}
                if isinstance(data, list):
                    qa_pairs = data
                elif isinstance(data, dict) and 'qa_pairs' in data:
                    qa_pairs = data['qa_pairs']
                else:
                    print(f"Warning: Unknown format in {json_file.name}")
                    continue

                pair_count = len(qa_pairs)
                indicator_name = self._extract_indicator_name(json_file.name)
                session = data.get('session', qa_pairs[0].get('session', 'unknown')) if pair_count > 0 else 'unknown'

                self.data_inventory['wave3'].append({
                    'indicator': indicator_name,
                    'pair_count': pair_count,
                    'session': session,
                    'file': str(json_file)
                })

                self.statistics['by_wave']['wave3'] += pair_count
                self.statistics['by_indicator'][indicator_name] += pair_count
                self.statistics['by_session'][session] += pair_count
                self.statistics['total_pairs'] += pair_count

                # Track indicator details
                if indicator_name not in self.statistics['indicator_details']:
                    self.statistics['indicator_details'][indicator_name] = {
                        'total_pairs': 0,
                        'sessions': set(),
                        'waves': set()
                    }

                self.statistics['indicator_details'][indicator_name]['total_pairs'] += pair_count
                self.statistics['indicator_details'][indicator_name]['sessions'].add(session)
                self.statistics['indicator_details'][indicator_name]['waves'].add('wave3')

            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")

        print(f"Wave 3: Scanned {len(self.data_inventory['wave3'])} indicator files")

    def scan_parsed_originals(self):
        """Scan original parsed Q&A data (technical indicators)"""
        parsed_dir = self.base_path / "parsed_qa_data"

        if not parsed_dir.exists():
            print(f"Warning: Parsed data directory not found: {parsed_dir}")
            return

        json_files = sorted(parsed_dir.glob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle two possible formats
                if isinstance(data, list):
                    qa_pairs = data
                elif isinstance(data, dict) and 'qa_pairs' in data:
                    qa_pairs = data['qa_pairs']
                else:
                    print(f"Warning: Unknown format in {json_file.name}")
                    continue

                pair_count = len(qa_pairs)
                indicator_name = self._extract_indicator_name(json_file.name)

                self.data_inventory['parsed_originals'].append({
                    'indicator': indicator_name,
                    'pair_count': pair_count,
                    'file': str(json_file)
                })

                # Note: These are likely already in Wave 1 batches
                # So we track them separately for reference

            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")

        print(f"Original Parsed: Scanned {len(self.data_inventory['parsed_originals'])} indicator files")

    def _extract_indicator_name(self, filename: str) -> str:
        """Extract clean indicator name from filename"""
        # Remove _qa_pairs.json suffix
        name = filename.replace('_qa_pairs.json', '')
        # Remove leading underscores
        name = name.lstrip('_')
        # Replace underscores with spaces for readability
        name = name.replace('_', ' ')
        return name

    def categorize_indicators(self):
        """Categorize all indicators by type"""
        for indicator, details in self.statistics['indicator_details'].items():
            indicator_lower = indicator.lower()

            # Find matching category
            matched = False
            for category, keywords in self.category_map.items():
                for keyword in keywords:
                    if keyword in indicator_lower:
                        self.statistics['by_category'][category] += details['total_pairs']
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                self.statistics['by_category']['other'] += details['total_pairs']

    def calculate_balance_metrics(self) -> Dict:
        """Calculate data balance and identify imbalances"""
        total = self.statistics['total_pairs']

        balance_metrics = {
            'total_pairs': total,
            'over_represented': [],  # >5% of total
            'well_represented': [],  # 1-5% of total
            'under_represented': [],  # 0.1-1% of total
            'critically_low': [],  # <0.1% of total
            'missing': []  # 0 pairs
        }

        for indicator, details in self.statistics['indicator_details'].items():
            count = details['total_pairs']
            percentage = (count / total * 100) if total > 0 else 0

            entry = {
                'indicator': indicator,
                'count': count,
                'percentage': percentage
            }

            if count == 0:
                balance_metrics['missing'].append(entry)
            elif percentage >= 5.0:
                balance_metrics['over_represented'].append(entry)
            elif percentage >= 1.0:
                balance_metrics['well_represented'].append(entry)
            elif percentage >= 0.1:
                balance_metrics['under_represented'].append(entry)
            else:
                balance_metrics['critically_low'].append(entry)

        return balance_metrics

    def generate_report(self, output_file: str = "DATA_GOVERNANCE_REPORT.md"):
        """Generate comprehensive governance report"""
        balance = self.calculate_balance_metrics()

        report = []
        report.append("# WeMineHope.com Data Governance Report\n")
        report.append(f"**Generated:** November 2, 2025\n")
        report.append(f"**Total Q&A Pairs:** {self.statistics['total_pairs']:,}\n")
        report.append("\n---\n\n")

        # Executive Summary
        report.append("## Executive Summary\n\n")
        report.append("This report provides comprehensive tracking and analysis of Q&A pair distribution ")
        report.append("to prevent the data imbalance issues that affected the previous 25,000 pair system.\n\n")

        # Wave Distribution
        report.append("### Distribution by Wave\n\n")
        report.append("| Wave | Q&A Pairs | Percentage | Status |\n")
        report.append("|------|-----------|------------|--------|\n")
        for wave in ['wave1', 'wave2', 'wave3']:
            count = self.statistics['by_wave'][wave]
            pct = (count / self.statistics['total_pairs'] * 100) if self.statistics['total_pairs'] > 0 else 0
            status = "Processing" if wave == 'wave1' else "Staged"
            report.append(f"| {wave.upper()} | {count:,} | {pct:.1f}% | {status} |\n")
        report.append(f"| **TOTAL** | **{self.statistics['total_pairs']:,}** | **100%** | - |\n\n")

        # Category Distribution
        report.append("### Distribution by Category\n\n")
        report.append("| Category | Q&A Pairs | Percentage |\n")
        report.append("|----------|-----------|------------|\n")

        sorted_categories = sorted(
            self.statistics['by_category'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, count in sorted_categories:
            pct = (count / self.statistics['total_pairs'] * 100) if self.statistics['total_pairs'] > 0 else 0
            report.append(f"| {category.title()} | {count:,} | {pct:.1f}% |\n")
        report.append("\n")

        # Balance Analysis
        report.append("## Balance Analysis\n\n")

        report.append("### Over-Represented Topics (>5%)\n\n")
        if balance['over_represented']:
            report.append("| Indicator | Count | Percentage |\n")
            report.append("|-----------|-------|------------|\n")
            for item in sorted(balance['over_represented'], key=lambda x: x['percentage'], reverse=True):
                report.append(f"| {item['indicator']} | {item['count']:,} | {item['percentage']:.2f}% |\n")
        else:
            report.append("No over-represented topics detected.\n")
        report.append("\n")

        report.append("### Well-Represented Topics (1-5%)\n\n")
        if balance['well_represented']:
            report.append(f"**Total:** {len(balance['well_represented'])} indicators\n\n")
        else:
            report.append("No topics in this range.\n\n")

        report.append("### Under-Represented Topics (0.1-1%)\n\n")
        if balance['under_represented']:
            report.append("| Indicator | Count | Percentage |\n")
            report.append("|-----------|-------|------------|\n")
            for item in sorted(balance['under_represented'], key=lambda x: x['percentage'], reverse=True):
                report.append(f"| {item['indicator']} | {item['count']:,} | {item['percentage']:.2f}% |\n")
        else:
            report.append("No under-represented topics.\n")
        report.append("\n")

        report.append("### Critically Low (<0.1%)\n\n")
        if balance['critically_low']:
            report.append("| Indicator | Count | Percentage |\n")
            report.append("|-----------|-------|------------|\n")
            for item in sorted(balance['critically_low'], key=lambda x: x['count']):
                report.append(f"| {item['indicator']} | {item['count']} | {item['percentage']:.3f}% |\n")
        else:
            report.append("No critically low topics.\n")
        report.append("\n")

        report.append("### Missing Indicators (0 pairs)\n\n")
        if balance['missing']:
            for item in balance['missing']:
                report.append(f"- {item['indicator']}\n")
        else:
            report.append("All indicators have data.\n")
        report.append("\n")

        # Recommendations
        report.append("## Recommendations\n\n")

        if balance['over_represented']:
            report.append("### Address Over-Representation\n\n")
            report.append("The following topics comprise >5% of the dataset each:\n\n")
            for item in balance['over_represented'][:5]:
                report.append(f"- **{item['indicator']}** ({item['percentage']:.1f}%)\n")
            report.append("\nConsider: Reducing future generation or ensuring other topics catch up.\n\n")

        if balance['critically_low'] or balance['missing']:
            report.append("### Fill Critical Gaps\n\n")
            report.append("Priority indicators for additional Q&A generation:\n\n")

            combined = balance['critically_low'] + balance['missing']
            for item in sorted(combined, key=lambda x: x['count'])[:10]:
                report.append(f"- **{item['indicator']}** ({item['count']} pairs)\n")
            report.append("\n")

        report.append("### Maintain Balanced Growth\n\n")
        report.append("- Target 100 pairs per indicator for consistency\n")
        report.append("- Monitor distribution after each wave\n")
        report.append("- Use this report to guide future generation priorities\n\n")

        # Detailed Indicator List
        report.append("## Complete Indicator Inventory\n\n")
        report.append("| Indicator | Total Pairs | Sessions | Waves | Status |\n")
        report.append("|-----------|-------------|----------|-------|--------|\n")

        sorted_indicators = sorted(
            self.statistics['indicator_details'].items(),
            key=lambda x: x[1]['total_pairs'],
            reverse=True
        )

        for indicator, details in sorted_indicators:
            count = details['total_pairs']
            sessions = ', '.join(str(s) for s in sorted(details['sessions'])) if details['sessions'] else 'N/A'
            waves = ', '.join(sorted(details['waves'])) if details['waves'] else 'N/A'

            if count >= 100:
                status = "Complete"
            elif count >= 50:
                status = "Good"
            elif count >= 10:
                status = "Low"
            elif count > 0:
                status = "Critical"
            else:
                status = "Missing"

            report.append(f"| {indicator} | {count} | {sessions} | {waves} | {status} |\n")

        report.append("\n---\n\n")
        report.append("**Report End**\n")

        # Write report
        output_path = self.base_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(report)

        print(f"\nReport generated: {output_path}")
        return output_path

    def export_statistics(self, output_file: str = "data_statistics.json"):
        """Export statistics to JSON for programmatic access"""
        # Convert sets to lists for JSON serialization
        export_stats = dict(self.statistics)
        export_stats['indicator_details'] = {
            k: {
                'total_pairs': v['total_pairs'],
                'sessions': list(v['sessions']),
                'waves': list(v['waves'])
            }
            for k, v in self.statistics['indicator_details'].items()
        }

        output_path = self.base_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_stats, f, indent=2)

        print(f"Statistics exported: {output_path}")
        return output_path

    def run_full_analysis(self):
        """Run complete data governance analysis"""
        print("=" * 70)
        print("WeMineHope.com Data Governance System")
        print("=" * 70)
        print()

        print("Scanning data sources...")
        self.scan_wave1_data()
        self.scan_wave2_data()
        self.scan_wave3_data()
        self.scan_parsed_originals()

        print("\nCategorizing indicators...")
        self.categorize_indicators()

        print("\nGenerating reports...")
        self.generate_report()
        self.export_statistics()

        print("\n" + "=" * 70)
        print("Analysis Complete")
        print("=" * 70)
        print(f"\nTotal Q&A Pairs Analyzed: {self.statistics['total_pairs']:,}")
        print(f"Unique Indicators: {len(self.statistics['indicator_details'])}")
        print(f"Categories: {len(self.statistics['by_category'])}")
        print(f"Sessions: {len(self.statistics['by_session'])}")
        print()


if __name__ == "__main__":
    system = DataGovernanceSystem()
    system.run_full_analysis()
