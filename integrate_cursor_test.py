"""
Integrate Cursor AI Q&A Pair - Test Integration
===============================================

Tests integration of a single Cursor AI generated Q&A pair.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

def integrate_cursor_test():
    """Integrate single Cursor Q&A pair for testing"""

    # Connect to database
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()

    # Target file
    test_file = Path('inbox/droid/cursor_test_ichimoku_tenkan_sen_qa_003.json')

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        return

    print("=" * 70)
    print("CURSOR AI INTEGRATION TEST")
    print("=" * 70)
    print()

    # Load the Cursor data
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract fields
    indicator_name = data.get('indicator', 'Ichimoku Tenkan-Sen')
    category = data.get('category', 'Ichimoku')
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    difficulty_level = data.get('difficulty_level', 'expert')
    tags = ','.join(data.get('tags', []))
    answer_char_count = data.get('answer_char_count', len(answer))
    quality_score = data.get('quality_score', 90)

    print(f"File: {test_file.name}")
    print(f"Indicator: {indicator_name}")
    print(f"Category: {category}")
    print(f"Difficulty: {difficulty_level}")
    print(f"Answer Length: {answer_char_count:,} characters")
    print(f"Quality Score: {quality_score}/100")
    print(f"Question: {question[:100]}...")
    print()

    # Check if indicator exists
    c.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
    result = c.fetchone()

    if result:
        indicator_id = result[0]
        print(f"Found existing indicator: {indicator_name} (ID: {indicator_id})")
    else:
        # Create new indicator
        c.execute('''INSERT INTO crypto_indicators (indicator_name, indicator_category, description)
                   VALUES (?, ?, ?)''',
                  (indicator_name, category, f'{indicator_name} - {category}'))
        indicator_id = c.lastrowid
        print(f"Created new indicator: {indicator_name} (ID: {indicator_id})")

    print()

    # Check for duplicate question
    c.execute('''SELECT qa_id, answer_length FROM qa_pairs
               WHERE indicator_id = ? AND question = ?''',
              (indicator_id, question))
    duplicate = c.fetchone()

    if duplicate:
        print("DUPLICATE DETECTED!")
        print(f"  Existing QA ID: {duplicate[0]}")
        print(f"  Existing Length: {duplicate[1]:,} chars")
        print(f"  New Length: {answer_char_count:,} chars")
        print()
        print("Skipping insertion - duplicate protection working correctly!")
        print("=" * 70)
        conn.close()
        return

    # Get next pair_number
    c.execute('SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?', (indicator_id,))
    next_pair_number = c.fetchone()[0] + 1

    # Insert the Q&A pair
    c.execute('''INSERT INTO qa_pairs
               (indicator_id, pair_number, question, answer, topic, created_date,
                indicator_name, difficulty_level, answer_length,
                has_formula, has_examples, has_sources, crypto_specific)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (indicator_id,
               next_pair_number,
               question,
               answer,
               indicator_name,
               datetime.now().strftime('%Y-%m-%d'),
               indicator_name,
               difficulty_level,
               answer_char_count,
               1,  # has_formula
               1,  # has_examples
               1,  # has_sources
               1)) # crypto_specific

    qa_id = c.lastrowid
    conn.commit()

    print("SUCCESSFULLY INSERTED!")
    print(f"  QA Pair ID: {qa_id}")
    print(f"  Pair Number: {next_pair_number}")
    print(f"  Indicator ID: {indicator_id}")
    print(f"  Answer Length: {answer_char_count:,} characters")
    print(f"  Difficulty: {difficulty_level}")
    print(f"  Source: Cursor AI")
    print()

    # Get updated database stats
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    total_pairs = c.fetchone()[0]

    c.execute('SELECT COUNT(DISTINCT indicator_id) FROM qa_pairs')
    total_indicators = c.fetchone()[0]

    print("=" * 70)
    print("DATABASE STATUS AFTER INTEGRATION")
    print("=" * 70)
    print(f"Total Q&A Pairs: {total_pairs:,}")
    print(f"Total Indicators: {total_indicators}")
    print(f"Progress to 30K: {(total_pairs/30000)*100:.2f}%")
    print(f"Remaining: {30000-total_pairs:,} pairs")
    print("=" * 70)

    conn.close()

    # Move file to processed
    processed_dir = Path('inbox/droid/processed')
    processed_dir.mkdir(exist_ok=True)
    processed_file = processed_dir / test_file.name
    test_file.rename(processed_file)
    print(f"\nMoved to: {processed_file}")
    print()

if __name__ == '__main__':
    integrate_cursor_test()
