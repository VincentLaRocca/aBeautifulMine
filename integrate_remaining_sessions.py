import json
import sqlite3
from datetime import datetime
import re
import os
import glob

print("="*70)
print("INTEGRATING REMAINING SESSIONS (1-13)")
print("="*70)

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check starting state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
starting_pairs = cursor.fetchone()[0]
print(f"\nStarting Q&A pairs in database: {starting_pairs:,}")

# Integration stats
stats = {
    'sessions_processed': 0,
    'indicators_added': 0,
    'qa_pairs_added': 0,
    'errors': []
}

# Session 10-13 from archive
archive_sessions = {
    10: 'archive/rd_phase/session_10_transaction_metrics_qa_dataset.json',
    11: 'archive/rd_phase/session-11-qa-complete.json',
    13: 'archive/rd_phase/session-13-qa-complete-corrected.json'
}

# Sessions 1-9 from inbox
inbox_sessions = list(range(1, 10))

def process_session(session_num, file_path):
    """Process a single session file"""
    print(f"\n{'='*70}")
    print(f"Processing Session {session_num}")
    print(f"{'='*70}")

    try:
        if not os.path.exists(file_path):
            print(f"  SKIPPED: File not found")
            return False

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different file structures
        qa_pairs = data.get('qa_pairs', [])
        if isinstance(data, list):
            qa_pairs = data

        if not qa_pairs:
            print(f"  SKIPPED: No Q&A pairs found")
            return False

        # Get topic/category
        topic = data.get('topic') or data.get('category') or data.get('indicator_name') or f"Session {session_num}"

        print(f"Topic: {topic}")
        print(f"Q&A pairs: {len(qa_pairs)}")

        # Check if indicator exists
        cursor.execute('''
            SELECT id FROM crypto_indicators
            WHERE indicator_name = ? AND session_number = ?
        ''', (topic, session_num))

        existing = cursor.fetchone()

        if existing:
            indicator_id = existing[0]
            print(f"  Indicator exists (ID: {indicator_id})")
        else:
            # Insert new indicator
            cursor.execute('''
                INSERT INTO crypto_indicators (
                    indicator_name, indicator_category, session_number,
                    description, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                topic,
                "Research Topics",
                session_num,
                f"Topic from session {session_num}",
                datetime.now(),
                datetime.now()
            ))

            indicator_id = cursor.lastrowid
            stats['indicators_added'] += 1
            print(f"  Created indicator (ID: {indicator_id})")

        # Process Q&A pairs
        pair_count = 0
        for idx, qa in enumerate(qa_pairs, 1):
            question = qa.get('question', '')
            answer = qa.get('answer', '')

            if not question or not answer:
                continue

            # Check for duplicate
            cursor.execute('''
                SELECT qa_id FROM qa_pairs
                WHERE indicator_id = ? AND pair_number = ?
            ''', (indicator_id, idx))

            if cursor.fetchone():
                continue

            # Analyze answer
            answer_length = len(answer)
            has_formula = bool(re.search(r'[=×÷\\+\\-]|\\bformula\\b', answer, re.IGNORECASE))
            has_examples = bool(re.search(r'\\bexample\\b|\\bfor instance\\b|\\be\\.g\\.\\b', answer, re.IGNORECASE))
            has_sources = bool(re.search(r'\\bsource\\b|\\baccording to\\b|\\bresearch\\b', answer, re.IGNORECASE))

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
                topic,
                idx,
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

            pair_count += 1
            stats['qa_pairs_added'] += 1

        print(f"  Inserted {pair_count} Q&A pairs")
        stats['sessions_processed'] += 1
        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        stats['errors'].append(f"Session {session_num}: {str(e)}")
        return False

# Process archive sessions (10-13)
print("\n" + "="*70)
print("ARCHIVE SESSIONS (10-13)")
print("="*70)

for session_num, rel_path in archive_sessions.items():
    file_path = f'C:/Users/vlaro/dreamteam/claude/{rel_path}'
    process_session(session_num, file_path)

# Process inbox sessions (1-9)
print("\n" + "="*70)
print("INBOX SESSIONS (1-9)")
print("="*70)

for session_num in inbox_sessions:
    file_path = f'C:/Users/vlaro/dreamteam/claude/inbox/crypto-indicators-session-{session_num:02d}-qa.json'
    process_session(session_num, file_path)

# Commit changes
conn.commit()

# Final report
print(f"\n{'='*70}")
print("INTEGRATION COMPLETE")
print(f"{'='*70}")
print(f"Sessions processed: {stats['sessions_processed']}")
print(f"Indicators added: {stats['indicators_added']}")
print(f"Q&A pairs added: {stats['qa_pairs_added']}")

if stats['errors']:
    print(f"\nErrors encountered: {len(stats['errors'])}")
    for error in stats['errors']:
        print(f"  - {error}")

# Verify final state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_pairs = cursor.fetchone()[0]
print(f"\nFinal Q&A pairs in database: {final_pairs:,}")
print(f"Growth: +{final_pairs - starting_pairs:,} pairs")

conn.close()

print("\nRemaining sessions integration complete!")
