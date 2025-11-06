"""
Integrate Crypto Unified Training Dataset
Integrates 419 Q&A pairs from C:/users/vlaro/crypto/compiled_datasets

Date: November 5, 2025
Source: Unified training data from crypto project
"""

import json
import sqlite3
from datetime import datetime

print("="*80)
print("CRYPTO UNIFIED DATASET INTEGRATION")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Load unified training data
data_path = 'C:/users/vlaro/crypto/compiled_datasets/unified_training_data_20251025_145038.json'

print(f"\nLoading: {data_path}")
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[OK] Loaded {len(data)} conversation pairs")

# Connect to database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Get current stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
initial_count = cursor.fetchone()[0]
print(f"\nProduction DB before integration: {initial_count:,} pairs")

# Build question index for deduplication
print("\nBuilding question index...")
cursor.execute('SELECT question FROM qa_pairs')
existing_questions = set()
for row in cursor.fetchall():
    existing_questions.add(row[0].strip().lower())

print(f"  Existing questions: {len(existing_questions):,}")

# Extract Q&A pairs from OpenAI chat format
qa_pairs = []
for item in data:
    messages = item.get('messages', [])

    # Extract user message (question) and assistant message (answer)
    question = None
    answer = None

    for msg in messages:
        if msg.get('role') == 'user':
            question = msg.get('content', '').strip()
        elif msg.get('role') == 'assistant':
            answer = msg.get('content', '').strip()

    if question and answer:
        qa_pairs.append({
            'question': question,
            'answer': answer
        })

print(f"\n[EXTRACTED] {len(qa_pairs)} Q&A pairs from chat format")

# Deduplicate
unique_pairs = []
duplicate_count = 0

for pair in qa_pairs:
    question = pair['question']
    if question.lower() not in existing_questions:
        unique_pairs.append(pair)
        existing_questions.add(question.lower())
    else:
        duplicate_count += 1

print(f"\n[DEDUPLICATION]")
print(f"  Total pairs: {len(qa_pairs):,}")
print(f"  Unique pairs (NEW): {len(unique_pairs):,}")
print(f"  Duplicates (SKIP): {duplicate_count:,}")
print(f"  Duplicate rate: {(duplicate_count/len(qa_pairs)*100):.1f}%")

if not unique_pairs:
    print("\n[INFO] All pairs are duplicates, no integration needed")
    exit(0)

# Create indicator for this dataset
indicator_name = 'DeFi and Cryptocurrency Fundamentals'
category = 'Educational Content'
session = 204

print(f"\n[CREATING INDICATOR]")
cursor.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
result = cursor.fetchone()

if result:
    indicator_id = result[0]
    print(f"  Using existing indicator ID: {indicator_id}")
else:
    cursor.execute('''
        INSERT INTO crypto_indicators
        (indicator_name, indicator_category, display_name, description, session_number, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        indicator_name,
        category,
        indicator_name,
        'Comprehensive DeFi yield farming, cryptocurrency fundamentals, and technical analysis training data from unified dataset',
        session,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    indicator_id = cursor.lastrowid
    print(f"  Created new indicator ID: {indicator_id}")

# Get next pair_number
cursor.execute('''
    SELECT COALESCE(MAX(pair_number), 0) + 1
    FROM qa_pairs WHERE indicator_id = ?
''', (indicator_id,))
next_pair_number = cursor.fetchone()[0]

# Integration statistics
stats = {
    'pairs_added': 0,
    'errors': 0
}

# Add Q&A pairs
print(f"\n[INTEGRATING]")
print(f"  Starting at pair_number: {next_pair_number}")

for i, pair in enumerate(unique_pairs, 1):
    question = pair['question']
    answer = pair['answer']

    answer_length = len(answer)
    topic = 'DeFi and Cryptocurrency Fundamentals'

    try:
        cursor.execute('''
            INSERT INTO qa_pairs
            (indicator_id, pair_number, question, answer, answer_length, topic)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            indicator_id,
            next_pair_number,
            question,
            answer,
            answer_length,
            topic
        ))

        next_pair_number += 1
        stats['pairs_added'] += 1

        if i % 100 == 0:
            print(f"  Progress: {i}/{len(unique_pairs)} pairs added")

    except Exception as e:
        print(f"  [ERROR] Could not add pair {i}: {e}")
        stats['errors'] += 1

# Final commit
conn.commit()
print(f"\n[FINAL COMMIT] All changes saved")

# Get final stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT indicator_id) FROM qa_pairs')
total_indicators = cursor.fetchone()[0]

# Close connection
conn.close()

# Print summary
print("\n" + "="*80)
print("INTEGRATION COMPLETE")
print("="*80)

print(f"\n[RESULTS]")
print(f"  Pairs added: {stats['pairs_added']:,}")
print(f"  Errors: {stats['errors']}")

print(f"\n[DATABASE GROWTH]")
print(f"  Before: {initial_count:,} pairs")
print(f"  After: {final_count:,} pairs")
print(f"  Added: {final_count - initial_count:,} pairs")
print(f"  Total indicators: {total_indicators}")

print(f"\n[PROGRESS TO GOAL]")
goal = 30000
progress = (final_count / goal * 100)
remaining = goal - final_count
print(f"  Current: {final_count:,} / {goal:,} pairs")
print(f"  Progress: {progress:.1f}%")
print(f"  Remaining: {remaining:,} pairs")

if final_count >= goal:
    print(f"\n  *** GOAL ACHIEVED! ***")
    print(f"  Exceeded by: {final_count - goal:,} pairs!")
else:
    print(f"\n  Gap to goal: {remaining:,} pairs")

# Save integration report
report = {
    'integration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'source': 'crypto_unified_training_dataset',
    'source_path': data_path,
    'statistics': stats,
    'database': {
        'before': initial_count,
        'after': final_count,
        'added': final_count - initial_count
    },
    'progress': {
        'current': final_count,
        'goal': goal,
        'progress_pct': progress,
        'remaining': remaining,
        'goal_achieved': final_count >= goal
    }
}

with open('crypto_unified_integration_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\n[OK] Integration report saved: crypto_unified_integration_report.json")

print("\n" + "="*80)
print("For the Greater Good of All")
print("="*80)
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
