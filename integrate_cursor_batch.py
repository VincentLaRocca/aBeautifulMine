"""
Integrate Cursor AI Batch - Complete Integration
================================================

Integrates all remaining Cursor AI generated Q&A pairs.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

def integrate_cursor_batch():
    """Integrate all Cursor Q&A pairs"""

    # Connect to database
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()

    # Source directory
    source_dir = Path("C:/Users/vlaro/dreamteam/gemini/shared/jsonpairs")
    files = sorted(source_dir.glob("ichimoku_tenkan_sen_qa_*.json"))

    # Exclude already integrated file
    files = [f for f in files if f.name != "ichimoku_tenkan_sen_qa_003.json"]

    print("=" * 70)
    print("CURSOR AI BATCH INTEGRATION")
    print("=" * 70)
    print(f"\nFiles to integrate: {len(files)}")
    print()

    # Get current stats
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    initial_count = c.fetchone()[0]

    integrated_count = 0
    duplicate_count = 0
    error_count = 0

    for file_path in files:
        try:
            # Load data
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract fields
            indicator_name = data.get('indicator', 'Ichimoku Tenkan-Sen')
            category = data.get('category', 'Ichimoku')
            question = data.get('question', '').strip()
            answer = data.get('answer', '').strip()
            difficulty_level = data.get('difficulty_level', 'expert')
            answer_char_count = data.get('answer_char_count', len(answer))

            # Check if indicator exists
            c.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?',
                     (indicator_name,))
            result = c.fetchone()

            if result:
                indicator_id = result[0]
            else:
                # Create new indicator
                c.execute('''INSERT INTO crypto_indicators
                           (indicator_name, indicator_category, description)
                           VALUES (?, ?, ?)''',
                         (indicator_name, category, f'{indicator_name} - {category}'))
                indicator_id = c.lastrowid

            # Check for duplicate
            c.execute('''SELECT qa_id FROM qa_pairs
                       WHERE indicator_id = ? AND question = ?''',
                     (indicator_id, question))

            if c.fetchone():
                duplicate_count += 1
                print(f"SKIP (duplicate): {file_path.name}")
                continue

            # Get next pair_number
            c.execute('''SELECT COALESCE(MAX(pair_number), 0)
                       FROM qa_pairs WHERE indicator_id = ?''',
                     (indicator_id,))
            next_pair_number = c.fetchone()[0] + 1

            # Insert the Q&A pair
            c.execute('''INSERT INTO qa_pairs
                       (indicator_id, pair_number, question, answer, topic,
                        created_date, indicator_name, difficulty_level,
                        answer_length, has_formula, has_examples,
                        has_sources, crypto_specific)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (indicator_id, next_pair_number, question, answer,
                      indicator_name, datetime.now().strftime('%Y-%m-%d'),
                      indicator_name, difficulty_level, answer_char_count,
                      1, 1, 1, 1))

            integrated_count += 1
            print(f"[OK] INTEGRATED: {file_path.name} ({answer_char_count:,} chars)")

        except Exception as e:
            error_count += 1
            print(f"[ERROR] {file_path.name} - {str(e)}")

    # Commit all changes
    conn.commit()

    # Get final stats
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    final_count = c.fetchone()[0]

    c.execute('SELECT COUNT(DISTINCT indicator_id) FROM qa_pairs')
    total_indicators = c.fetchone()[0]

    print()
    print("=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)
    print(f"\nSuccessfully Integrated: {integrated_count}")
    print(f"Duplicates Skipped: {duplicate_count}")
    print(f"Errors: {error_count}")
    print()
    print("DATABASE STATUS:")
    print(f"  Before: {initial_count:,} pairs")
    print(f"  After: {final_count:,} pairs")
    print(f"  Added: +{final_count - initial_count} pairs")
    print(f"  Total Indicators: {total_indicators}")
    print()
    print(f"Progress to 30K: {(final_count/30000)*100:.2f}%")
    print(f"Remaining: {30000 - final_count:,} pairs")
    print("=" * 70)

    conn.close()

if __name__ == '__main__':
    integrate_cursor_batch()
