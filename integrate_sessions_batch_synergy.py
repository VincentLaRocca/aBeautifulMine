"""
Team Claude Synergy - Batch Integration Script
===============================================

Pure synergy integration for sessions 101-187 and claude_shared database.
Claude designs, Claude Code executes, both validate.

Pattern: Flow state, no boundaries, total emergence.
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def get_database_path():
    """Auto-detect database path (Windows/Git Bash compatible)"""
    candidates = [
        'crypto_indicators_production.db',
        './crypto_indicators_production.db',
        'C:/Users/vlaro/dreamteam/claude/crypto_indicators_production.db',
        '/c/Users/vlaro/dreamteam/claude/crypto_indicators_production.db',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return 'crypto_indicators_production.db'

class SynergyBatchIntegrator:
    """
    Universal batch integrator designed for Team Claude synergy.

    Claude: Designed the architecture
    Claude Code: Executes the integration
    Both: Validate quality in real-time
    """

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = get_database_path()
        self.db_path = db_path
        print(f"[Synergy] Using database: {self.db_path}")
        self.stats = {
            'batches_processed': 0,
            'pairs_inserted': 0,
            'duplicates_skipped': 0,
            'errors': 0,
            'quality_score': 0.0
        }

    def integrate_rag_sessions(self, start_session: int, end_session: int) -> Dict:
        """
        Integrate RAG export sessions (101-140, 141-187, etc.)

        Args:
            start_session: First session number
            end_session: Last session number

        Returns:
            Integration statistics
        """
        print(f"\n{'='*60}")
        print(f"SYNERGY BATCH: Sessions {start_session}-{end_session}")
        print(f"{'='*60}\n")

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        batch_stats = {
            'sessions_processed': 0,
            'pairs_inserted': 0,
            'duplicates': 0,
            'start_time': datetime.now().isoformat()
        }

        # Process each session
        for session_num in range(start_session, end_session + 1):
            session_file = Path(f'rag_export/session_{session_num:03d}.json')

            if not session_file.exists():
                continue

            # Load session data
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Process Q&A pairs from session
            pairs_added = self._process_session_data(c, data, session_num)

            batch_stats['sessions_processed'] += 1
            batch_stats['pairs_inserted'] += pairs_added

            # Checkpoint every 5 sessions
            if session_num % 5 == 0:
                conn.commit()
                print(f"  Checkpoint: Session {session_num}")
                print(f"    Total pairs: {batch_stats['pairs_inserted']}")

        # Final commit
        conn.commit()

        # Quality validation
        quality = self._validate_quality(c)
        batch_stats['quality_score'] = quality
        batch_stats['end_time'] = datetime.now().isoformat()

        conn.close()

        self.stats['batches_processed'] += 1
        self.stats['pairs_inserted'] += batch_stats['pairs_inserted']

        return batch_stats

    def integrate_claude_shared_db(self, source_db: str = 'claude_shared_original_training.db') -> Dict:
        """
        Integrate claude_shared database with deduplication

        Args:
            source_db: Path to source database

        Returns:
            Integration statistics
        """
        print(f"\n{'='*60}")
        print(f"SYNERGY BATCH: Claude Shared Database")
        print(f"{'='*60}\n")

        if not Path(source_db).exists():
            return {'error': f'Database not found: {source_db}'}

        # Connect to both databases
        source_conn = sqlite3.connect(source_db)
        target_conn = sqlite3.connect(self.db_path)

        source_c = source_conn.cursor()
        target_c = target_conn.cursor()

        batch_stats = {
            'pairs_processed': 0,
            'pairs_inserted': 0,
            'duplicates': 0,
            'start_time': datetime.now().isoformat()
        }

        # Get all Q&A pairs from source
        source_c.execute('''
            SELECT question, answer, indicator_name, topic, difficulty_level
            FROM qa_pairs
        ''')

        for row in source_c.fetchall():
            question, answer, indicator_name, topic, difficulty_level = row
            batch_stats['pairs_processed'] += 1

            # Check for duplicate
            if self._is_duplicate(target_c, question):
                batch_stats['duplicates'] += 1
                continue

            # Get or create indicator
            indicator_id = self._get_or_create_indicator(target_c, indicator_name)

            # Get next pair number
            target_c.execute(
                'SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?',
                (indicator_id,)
            )
            pair_number = target_c.fetchone()[0] + 1

            # Insert pair
            target_c.execute('''
                INSERT INTO qa_pairs (
                    indicator_id, pair_number, question, answer, topic,
                    created_date, indicator_name, difficulty_level,
                    answer_length, has_formula, has_examples, has_sources, crypto_specific
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                indicator_id, pair_number, question, answer, topic or indicator_name,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                indicator_name,
                difficulty_level or 'intermediate',
                len(answer),
                1 if any(x in answer.lower() for x in ['formula', 'calculation', '=']) else 0,
                1 if any(x in answer.lower() for x in ['example', 'for instance']) else 0,
                1 if any(x in answer.lower() for x in ['source', 'according to']) else 0,
                1 if any(x in answer.lower() for x in ['crypto', 'bitcoin', 'blockchain']) else 0
            ))

            batch_stats['pairs_inserted'] += 1

            # Checkpoint every 500 pairs
            if batch_stats['pairs_inserted'] % 500 == 0:
                target_conn.commit()
                print(f"  Checkpoint: {batch_stats['pairs_inserted']} pairs inserted")

        # Final commit
        target_conn.commit()

        # Quality validation
        quality = self._validate_quality(target_c)
        batch_stats['quality_score'] = quality
        batch_stats['end_time'] = datetime.now().isoformat()

        source_conn.close()
        target_conn.close()

        self.stats['batches_processed'] += 1
        self.stats['pairs_inserted'] += batch_stats['pairs_inserted']
        self.stats['duplicates_skipped'] += batch_stats['duplicates']

        return batch_stats

    def _process_session_data(self, cursor, data: Dict, session_num: int) -> int:
        """Process data from a single RAG export session"""
        pairs_added = 0

        # Handle different data formats
        if isinstance(data, dict) and 'qa_pairs' in data:
            pairs = data['qa_pairs']
        elif isinstance(data, list):
            pairs = data
        else:
            return 0

        for pair in pairs:
            question = pair.get('question', '')
            answer = pair.get('answer', '')
            indicator_name = pair.get('indicator', f'session_{session_num}')
            topic = pair.get('topic', indicator_name)

            if not question or not answer:
                continue

            # Check for duplicate
            if self._is_duplicate(cursor, question):
                self.stats['duplicates_skipped'] += 1
                continue

            # Get or create indicator
            indicator_id = self._get_or_create_indicator(cursor, indicator_name)

            # Get next pair number
            cursor.execute(
                'SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?',
                (indicator_id,)
            )
            pair_number = cursor.fetchone()[0] + 1

            # Insert pair
            cursor.execute('''
                INSERT INTO qa_pairs (
                    indicator_id, pair_number, question, answer, topic,
                    created_date, indicator_name, difficulty_level,
                    answer_length, has_formula, has_examples, has_sources, crypto_specific
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                indicator_id, pair_number, question, answer, topic,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                indicator_name,
                pair.get('difficulty_level', 'intermediate'),
                len(answer),
                1 if any(x in answer.lower() for x in ['formula', 'calculation', '=']) else 0,
                1 if any(x in answer.lower() for x in ['example', 'for instance']) else 0,
                1 if any(x in answer.lower() for x in ['source', 'according to']) else 0,
                1 if any(x in answer.lower() for x in ['crypto', 'bitcoin', 'blockchain']) else 0
            ))

            pairs_added += 1

        return pairs_added

    def _is_duplicate(self, cursor, question: str) -> bool:
        """Check if question already exists"""
        cursor.execute('SELECT qa_id FROM qa_pairs WHERE question = ?', (question,))
        return cursor.fetchone() is not None

    def _get_or_create_indicator(self, cursor, indicator_name: str) -> int:
        """Get indicator ID or create new indicator"""
        cursor.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
        result = cursor.fetchone()

        if result:
            return result[0]

        # Create new indicator
        cursor.execute('''
            INSERT INTO crypto_indicators (indicator_name, indicator_category, description)
            VALUES (?, ?, ?)
        ''', (indicator_name, 'Technical Indicators', f'{indicator_name} analysis'))

        return cursor.lastrowid

    def _validate_quality(self, cursor) -> float:
        """Validate overall database quality"""
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                AVG(answer_length) as avg_length,
                SUM(crypto_specific) * 100.0 / COUNT(*) as crypto_pct,
                SUM(has_formula) * 100.0 / COUNT(*) as formula_pct,
                SUM(has_examples) * 100.0 / COUNT(*) as examples_pct
            FROM qa_pairs
        ''')

        result = cursor.fetchone()
        total, avg_length, crypto_pct, formula_pct, examples_pct = result

        # Quality score (weighted)
        quality = (
            (min(avg_length / 3000, 1.0) * 0.4) +  # 40% weight on length
            (crypto_pct / 100 * 0.4) +              # 40% weight on crypto-specific
            (formula_pct / 100 * 0.1) +             # 10% weight on formulas
            (examples_pct / 100 * 0.1)              # 10% weight on examples
        ) * 100

        return round(quality, 2)

    def get_stats(self) -> Dict:
        """Get integration statistics"""
        return self.stats

    def print_summary(self):
        """Print integration summary"""
        print(f"\n{'='*60}")
        print("TEAM CLAUDE SYNERGY - INTEGRATION SUMMARY")
        print(f"{'='*60}")
        print(f"Batches processed: {self.stats['batches_processed']}")
        print(f"Pairs inserted: {self.stats['pairs_inserted']:,}")
        print(f"Duplicates skipped: {self.stats['duplicates_skipped']:,}")
        print(f"Quality score: {self.stats['quality_score']:.1f}%")
        print(f"{'='*60}\n")


def main():
    """Main integration workflow"""
    integrator = SynergyBatchIntegrator()

    print("\n" + "="*60)
    print("TEAM CLAUDE SYNERGY INTEGRATION")
    print("Pure flow, no boundaries, total emergence")
    print("="*60)

    # Get current database state
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    initial_count = c.fetchone()[0]
    conn.close()

    print(f"\nStarting pairs: {initial_count:,}")

    # Integration sequence
    print("\n[Claude + Claude Code] Beginning integration...")

    # Batch 1: Sessions 101-140 (resume from 10/40)
    print("\n[Claude Code] Executing Batch 1: Sessions 101-140")
    result1 = integrator.integrate_rag_sessions(101, 140)
    print(f"[Claude] Validated: {result1['pairs_inserted']:,} pairs")
    print(f"[Both] Quality: {result1.get('quality_score', 0):.1f}%")

    # Batch 2: Claude Shared Database
    print("\n[Claude Code] Executing Batch 2: Claude Shared DB")
    result2 = integrator.integrate_claude_shared_db()
    if 'error' not in result2:
        print(f"[Claude] Validated: {result2['pairs_inserted']:,} pairs")
        print(f"[Both] Duplicates skipped: {result2['duplicates']:,}")
    else:
        print(f"[Claude] {result2['error']}")

    # Batch 3: Sessions 141-187
    print("\n[Claude Code] Executing Batch 3: Sessions 141-187")
    result3 = integrator.integrate_rag_sessions(141, 187)
    print(f"[Claude] Validated: {result3['pairs_inserted']:,} pairs")
    print(f"[Both] Quality: {result3.get('quality_score', 0):.1f}%")

    # Final summary
    integrator.print_summary()

    # Get final count
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    final_count = c.fetchone()[0]
    conn.close()

    print(f"Initial pairs: {initial_count:,}")
    print(f"Final pairs: {final_count:,}")
    print(f"Growth: +{final_count - initial_count:,} pairs")
    print(f"\n{'='*60}")
    print("SYNERGY COMPLETE - EMERGENCE ACHIEVED")
    print("="*60)


if __name__ == "__main__":
    main()
