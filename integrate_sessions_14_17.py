import json
import sqlite3
from datetime import datetime
import re

print("="*70)
print("INTEGRATING SESSIONS 14-17")
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

# Process sessions 14-17
for session_num in range(14, 18):
    file_path = f'C:/Users/vlaro/dreamteam/Database/session-{session_num}-qa-complete.json'

    print(f"\n{'='*70}")
    print(f"Processing Session {session_num}")
    print(f"{'='*70}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        session_id = data.get('session', session_num)
        category = data.get('category', 'Unknown')
        qa_pairs = data.get('qa_pairs', [])

        print(f"Session: {session_id}")
        print(f"Category: {category}")
        print(f"Q&A pairs: {len(qa_pairs)}")

        # Get indicators from data
        indicators = data.get('indicators', [])
        if not indicators:
            # If no indicators list, extract from qa_pairs
            indicators_set = set()
            for qa in qa_pairs:
                if 'indicator' in qa:
                    indicators_set.add(qa['indicator'])
                elif 'indicator_name' in qa:
                    indicators_set.add(qa['indicator_name'])
            indicators = list(indicators_set)

        print(f"Indicators: {len(indicators)}")

        # Process each indicator
        for indicator_name in indicators:
            print(f"\n  Processing indicator: {indicator_name}")

            # Check if indicator exists
            cursor.execute('''
                SELECT id FROM crypto_indicators
                WHERE indicator_name = ? AND session_number = ?
            ''', (indicator_name, session_id))

            existing = cursor.fetchone()

            if existing:
                indicator_id = existing[0]
                print(f"    Indicator exists (ID: {indicator_id})")
            else:
                # Insert new indicator
                cursor.execute('''
                    INSERT INTO crypto_indicators (
                        indicator_name, indicator_category, session_number,
                        description, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    indicator_name,
                    category,
                    session_id,
                    f"Indicator from session {session_id}",
                    datetime.now(),
                    datetime.now()
                ))

                indicator_id = cursor.lastrowid
                stats['indicators_added'] += 1
                print(f"    Created indicator (ID: {indicator_id})")

        # Process Q&A pairs
        pair_count = 0
        for idx, qa in enumerate(qa_pairs, 1):
            # Get indicator for this Q&A
            indicator_name = qa.get('indicator') or qa.get('indicator_name')
            if not indicator_name and indicators:
                indicator_name = indicators[0]  # Default to first indicator

            # Get or create indicator ID
            cursor.execute('''
                SELECT id FROM crypto_indicators
                WHERE indicator_name = ? AND session_number = ?
            ''', (indicator_name, session_id))

            result = cursor.fetchone()
            if not result:
                # Create indicator if it doesn't exist
                cursor.execute('''
                    INSERT INTO crypto_indicators (
                        indicator_name, indicator_category, session_number,
                        description, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    indicator_name,
                    category,
                    session_id,
                    f"Indicator from session {session_id}",
                    datetime.now(),
                    datetime.now()
                ))
                indicator_id = cursor.lastrowid
                stats['indicators_added'] += 1
            else:
                indicator_id = result[0]

            # Get Q&A content
            question = qa.get('question', '')
            answer = qa.get('answer', '')

            if not question or not answer:
                stats['errors'].append(f"Session {session_id}, pair {idx}: Missing question or answer")
                continue

            # Check for duplicate
            cursor.execute('''
                SELECT qa_id FROM qa_pairs
                WHERE indicator_id = ? AND pair_number = ?
            ''', (indicator_id, idx))

            if cursor.fetchone():
                continue  # Skip duplicate

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
                indicator_name,
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

    except FileNotFoundError:
        print(f"  ERROR: File not found: {file_path}")
        stats['errors'].append(f"Session {session_num}: File not found")
    except Exception as e:
        print(f"  ERROR: {e}")
        stats['errors'].append(f"Session {session_num}: {str(e)}")

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
    for error in stats['errors'][:10]:
        print(f"  - {error}")

# Verify final state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_pairs = cursor.fetchone()[0]
print(f"\nFinal Q&A pairs in database: {final_pairs:,}")
print(f"Growth: +{final_pairs - starting_pairs:,} pairs ({((final_pairs - starting_pairs) / starting_pairs * 100):.1f}%)")

conn.close()

print("\nSessions 14-17 integration complete!")
