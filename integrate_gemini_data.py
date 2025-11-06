import json
import sqlite3
from datetime import datetime
import re

print("="*70)
print("INTEGRATING GEMINI DATABASE DATA")
print("="*70)

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check starting state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
starting_pairs = cursor.fetchone()[0]
print(f"\nStarting Q&A pairs in database: {starting_pairs:,}")

# Load Gemini's extracted data
with open('gemini_data_extracted.json', 'r', encoding='utf-8') as f:
    gemini_data = json.load(f)

print(f"\nGemini data loaded:")
print(f"  Total pairs: {gemini_data['total_pairs']}")
print(f"  Sessions: {len(gemini_data['sessions'])}")

# Integration stats
stats = {
    'sessions_processed': 0,
    'indicators_created': 0,
    'indicators_existing': 0,
    'qa_pairs_added': 0,
    'qa_pairs_skipped': 0,
    'errors': []
}

# Process each session
for session_data in gemini_data['sessions']:
    session_num = session_data['session']
    qa_pairs = session_data['qa_pairs']

    print(f"\n{'='*70}")
    print(f"Processing Session {session_num}")
    print(f"{'='*70}")
    print(f"Q&A pairs: {len(qa_pairs)}")

    # Process each Q&A pair
    for qa in qa_pairs:
        indicator_name = qa['indicator']
        category = qa.get('category', 'Unknown')
        question = qa['question']
        answer = qa['answer']
        pair_number = qa['pair_number']

        # Check if indicator exists in production (by name only - UNIQUE constraint)
        cursor.execute('''
            SELECT id FROM crypto_indicators
            WHERE indicator_name = ?
        ''', (indicator_name,))

        result = cursor.fetchone()

        if result:
            indicator_id = result[0]
            stats['indicators_existing'] += 1
        else:
            # Create indicator (first occurrence)
            cursor.execute('''
                INSERT INTO crypto_indicators (
                    indicator_name, indicator_category, session_number,
                    description, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_name,
                category,
                session_num,
                f"{indicator_name} from Gemini database",
                datetime.now(),
                datetime.now()
            ))

            indicator_id = cursor.lastrowid
            stats['indicators_created'] += 1
            print(f"  Created indicator: {indicator_name} (ID: {indicator_id})")

        # Check for duplicate Q&A (by question text to be thorough)
        cursor.execute('''
            SELECT qa_id FROM qa_pairs
            WHERE indicator_id = ? AND question = ?
        ''', (indicator_id, question))

        if cursor.fetchone():
            stats['qa_pairs_skipped'] += 1
            continue

        # Get next available pair_number for this indicator
        cursor.execute('''
            SELECT COALESCE(MAX(pair_number), 0) + 1
            FROM qa_pairs
            WHERE indicator_id = ?
        ''', (indicator_id,))
        next_pair_number = cursor.fetchone()[0]

        # Analyze answer content
        answer_length = len(answer)
        has_formula = bool(re.search(r'[=×÷\+\-]|\bformula\b', answer, re.IGNORECASE))
        has_examples = bool(re.search(r'\bexample\b|\bfor instance\b|\be\.g\.\b', answer, re.IGNORECASE))
        has_sources = bool(re.search(r'\bsource\b|\baccording to\b|\bresearch\b', answer, re.IGNORECASE))

        # Insert Q&A pair with dynamic pair_number
        cursor.execute('''
            INSERT INTO qa_pairs (
                indicator_id, indicator_name, pair_number,
                question, answer,
                difficulty_level, answer_length,
                has_formula, has_examples, has_sources,
                crypto_specific, created_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            indicator_id,
            indicator_name,
            next_pair_number,
            question,
            answer,
            'intermediate',
            answer_length,
            has_formula,
            has_examples,
            has_sources,
            True,
            datetime.now().strftime('%Y-%m-%d')
        ))

        stats['qa_pairs_added'] += 1

    stats['sessions_processed'] += 1
    print(f"  Processed: {len(qa_pairs)} pairs")

# Commit changes
conn.commit()

# Final report
print(f"\n{'='*70}")
print("INTEGRATION COMPLETE")
print(f"{'='*70}")
print(f"Sessions processed: {stats['sessions_processed']}")
print(f"Indicators created: {stats['indicators_created']}")
print(f"Indicators existing: {stats['indicators_existing']}")
print(f"Q&A pairs added: {stats['qa_pairs_added']}")
print(f"Q&A pairs skipped (duplicates): {stats['qa_pairs_skipped']}")

if stats['errors']:
    print(f"\nErrors: {len(stats['errors'])}")
    for error in stats['errors']:
        print(f"  - {error}")

# Verify final state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_pairs = cursor.fetchone()[0]
growth = final_pairs - starting_pairs

print(f"\nDatabase Status:")
print(f"  Starting pairs: {starting_pairs:,}")
print(f"  Final pairs: {final_pairs:,}")
print(f"  Growth: +{growth:,} pairs (+{(growth / starting_pairs * 100):.1f}%)")

# Session coverage check
cursor.execute('SELECT COUNT(DISTINCT session_number) FROM crypto_indicators')
total_sessions = cursor.fetchone()[0]
print(f"  Total sessions in DB: {total_sessions}")

conn.close()

print("\n" + "="*70)
print("GEMINI DATA INTEGRATION SUCCESS")
print("="*70)
