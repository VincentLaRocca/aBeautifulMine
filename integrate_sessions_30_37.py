import json
import sqlite3
from datetime import datetime
import re

# Load extracted sessions
print("Loading sessions 30-37...")
with open('sessions_30_37_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Sessions to integrate: {len(data['sessions'])}")
print(f"Total Q&A pairs: {data['metadata']['total_qa_pairs']}")

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Track integration stats
stats = {
    'sessions_processed': 0,
    'indicators_added': 0,
    'qa_pairs_added': 0,
    'errors': []
}

# Process each session
for session in data['sessions']:
    session_id = session['session_id']
    topic = session['topic']
    qa_pairs = session['qa_pairs']

    print(f"\n{'='*60}")
    print(f"Processing Session {session_id}: {topic}")
    print(f"Q&A pairs: {len(qa_pairs)}")

    # For these research sessions, the topic itself is the "indicator"
    # Create a single indicator entry for each session
    indicator_name = topic
    indicator_category = "Research Topics"  # These appear to be research-based, not traditional indicators

    # Check if indicator already exists
    cursor.execute('''
        SELECT id FROM crypto_indicators
        WHERE indicator_name = ?
    ''', (indicator_name,))

    existing = cursor.fetchone()

    if existing:
        indicator_id = existing[0]
        print(f"  Indicator already exists (ID: {indicator_id})")
    else:
        # Insert new indicator
        cursor.execute('''
            INSERT INTO crypto_indicators (
                indicator_name, indicator_category, session_number,
                description, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            indicator_name,
            indicator_category,
            session_id,
            f"Research topic from session {session_id}",
            datetime.now(),
            datetime.now()
        ))

        indicator_id = cursor.lastrowid
        stats['indicators_added'] += 1
        print(f"  Created indicator (ID: {indicator_id})")

    # Now insert Q&A pairs
    pair_count = 0
    for idx, qa in enumerate(qa_pairs, 1):
        question = qa.get('question', '')
        answer = qa.get('answer', '')

        if not question or not answer:
            stats['errors'].append(f"Session {session_id}, pair {idx}: Missing question or answer")
            continue

        # Check if this Q&A pair already exists
        cursor.execute('''
            SELECT qa_id FROM qa_pairs
            WHERE indicator_id = ? AND pair_number = ?
        ''', (indicator_id, idx))

        if cursor.fetchone():
            continue  # Skip duplicates

        # Analyze answer for metadata
        answer_length = len(answer)
        has_formula = bool(re.search(r'[=×÷\+\-]|\bformula\b', answer, re.IGNORECASE))
        has_examples = bool(re.search(r'\bexample\b|\bfor instance\b|\be\.g\.\b', answer, re.IGNORECASE))
        has_sources = bool(re.search(r'\bsource\b|\baccording to\b|\bresearch\b', answer, re.IGNORECASE))

        # Insert Q&A pair
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
            idx,
            question,
            answer,
            'intermediate',  # Default difficulty
            answer_length,
            has_formula,
            has_examples,
            has_sources,
            True,  # All crypto-related
            datetime.now().strftime('%Y-%m-%d')
        ))

        pair_count += 1
        stats['qa_pairs_added'] += 1

    print(f"  Inserted {pair_count} Q&A pairs")
    stats['sessions_processed'] += 1

# Commit changes
conn.commit()

# Print final stats
print(f"\n{'='*60}")
print("INTEGRATION COMPLETE")
print(f"{'='*60}")
print(f"Sessions processed: {stats['sessions_processed']}")
print(f"Indicators added: {stats['indicators_added']}")
print(f"Q&A pairs added: {stats['qa_pairs_added']}")

if stats['errors']:
    print(f"\nErrors encountered: {len(stats['errors'])}")
    for error in stats['errors'][:10]:  # Show first 10 errors
        print(f"  - {error}")

# Verify final database state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
total_pairs = cursor.fetchone()[0]
print(f"\nTotal Q&A pairs in database: {total_pairs}")

cursor.execute('SELECT COUNT(*) FROM crypto_indicators')
total_indicators = cursor.fetchone()[0]
print(f"Total indicators in database: {total_indicators}")

# Show sessions in database
cursor.execute('''
    SELECT session_number, COUNT(*) as indicator_count
    FROM crypto_indicators
    GROUP BY session_number
    ORDER BY session_number
''')
print("\nIndicators by session:")
for row in cursor.fetchall():
    if row[0]:
        print(f"  Session {row[0]}: {row[1]} indicators")

conn.close()

print("\nIntegration complete!")
