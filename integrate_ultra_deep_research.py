import json
import sqlite3
from datetime import datetime
import re

print("="*70)
print("ULTRA DEEP RESEARCH INTEGRATION")
print("="*70)

# Load the data
print("\nLoading Ultra Deep Research data...")
with open('C:/Users/vlaro/dreamteam/Gemini/shared/ACTIVE-DATA/ultra_deep_research_ready.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qa_pairs = data['qa_pairs']
metadata = data['metadata']

print(f"Loaded: {len(qa_pairs):,} Q&A pairs")
print(f"Source: {metadata.get('source_database', 'Unknown')}")
print(f"Extraction date: {metadata.get('extraction_date', 'Unknown')}")

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check starting state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
starting_pairs = cursor.fetchone()[0]
print(f"\nStarting Q&A pairs in database: {starting_pairs:,}")

# Integration stats
stats = {
    'pairs_processed': 0,
    'pairs_added': 0,
    'pairs_skipped': 0,
    'indicators_added': 0,
    'errors': []
}

print("\n" + "="*70)
print("CREATING ULTRA DEEP RESEARCH INDICATOR")
print("="*70)

# Create a single indicator for all Ultra Deep Research data
indicator_name = "Ultra Deep Research Collection"
session_number = 999  # Special session number for this collection

# Check if indicator already exists
cursor.execute('''
    SELECT id FROM crypto_indicators
    WHERE indicator_name = ? AND session_number = ?
''', (indicator_name, session_number))

existing = cursor.fetchone()

if existing:
    indicator_id = existing[0]
    print(f"Indicator already exists (ID: {indicator_id})")
    print("WARNING: This may create duplicates!")
else:
    # Insert new indicator
    cursor.execute('''
        INSERT INTO crypto_indicators (
            indicator_name, indicator_category, session_number,
            description, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        indicator_name,
        "Research Topics",
        session_number,
        "Comprehensive ultra deep research collection - 9,999 Q&A pairs",
        datetime.now(),
        datetime.now()
    ))

    indicator_id = cursor.lastrowid
    stats['indicators_added'] += 1
    print(f"Created indicator (ID: {indicator_id})")

print("\n" + "="*70)
print("INTEGRATING Q&A PAIRS")
print("="*70)
print("This will take a few minutes...")

# Process all Q&A pairs
batch_size = 500
total_batches = (len(qa_pairs) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(qa_pairs))
    batch = qa_pairs[start_idx:end_idx]

    print(f"\nProcessing batch {batch_num + 1}/{total_batches} (pairs {start_idx + 1}-{end_idx})...")

    for pair in batch:
        pair_number = pair.get('pair_number', stats['pairs_processed'] + 1)
        question = pair.get('question', '').strip()
        answer = pair.get('answer', '').strip()
        topic = pair.get('topic', 'Unknown')

        stats['pairs_processed'] += 1

        if not question or not answer:
            stats['errors'].append(f"Pair {pair_number}: Missing question or answer")
            stats['pairs_skipped'] += 1
            continue

        # Check for duplicate by pair number
        cursor.execute('''
            SELECT qa_id FROM qa_pairs
            WHERE indicator_id = ? AND pair_number = ?
        ''', (indicator_id, pair_number))

        if cursor.fetchone():
            stats['pairs_skipped'] += 1
            continue  # Skip duplicate

        # Analyze answer for metadata
        answer_length = len(answer)
        has_formula = bool(re.search(r'[=×÷\\+\\-]|\\bformula\\b', answer, re.IGNORECASE))
        has_examples = bool(re.search(r'\\bexample\\b|\\bfor instance\\b|\\be\\.g\\.\\b', answer, re.IGNORECASE))
        has_sources = bool(re.search(r'\\bsource\\b|\\baccording to\\b|\\bresearch\\b', answer, re.IGNORECASE))

        # Insert Q&A pair
        try:
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
                pair_number,
                question,
                answer,
                'advanced',  # Ultra Deep Research is advanced content
                answer_length,
                has_formula,
                has_examples,
                has_sources,
                True,
                datetime.now().strftime('%Y-%m-%d')
            ))

            stats['pairs_added'] += 1

        except sqlite3.IntegrityError as e:
            stats['errors'].append(f"Pair {pair_number}: Integrity error - {str(e)}")
            stats['pairs_skipped'] += 1
        except Exception as e:
            stats['errors'].append(f"Pair {pair_number}: {str(e)}")
            stats['pairs_skipped'] += 1

    # Commit after each batch
    conn.commit()
    print(f"  Batch committed. Total added so far: {stats['pairs_added']:,}")

# Final commit
conn.commit()

# Final report
print("\n" + "="*70)
print("INTEGRATION COMPLETE")
print("="*70)
print(f"Pairs processed: {stats['pairs_processed']:,}")
print(f"Pairs added: {stats['pairs_added']:,}")
print(f"Pairs skipped: {stats['pairs_skipped']:,}")
print(f"Indicators added: {stats['indicators_added']}")

if stats['errors']:
    print(f"\nErrors encountered: {len(stats['errors'])}")
    for error in stats['errors'][:10]:
        print(f"  - {error}")
    if len(stats['errors']) > 10:
        print(f"  ... and {len(stats['errors']) - 10} more errors")

# Verify final state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_pairs = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM crypto_indicators')
total_indicators = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT session_number) FROM crypto_indicators WHERE session_number IS NOT NULL')
total_sessions = cursor.fetchone()[0]

print("\n" + "="*70)
print("DATABASE STATUS")
print("="*70)
print(f"Starting pairs: {starting_pairs:,}")
print(f"Final pairs: {final_pairs:,}")
print(f"Growth: +{final_pairs - starting_pairs:,} pairs ({((final_pairs - starting_pairs) / starting_pairs * 100):.1f}%)")
print(f"\nTotal indicators: {total_indicators}")
print(f"Total sessions: {total_sessions}")

# Calculate statistics for Ultra Deep Research data
cursor.execute('''
    SELECT
        COUNT(*) as total_pairs,
        AVG(answer_length) as avg_answer_length,
        MIN(answer_length) as min_answer_length,
        MAX(answer_length) as max_answer_length,
        SUM(CASE WHEN has_examples = 1 THEN 1 ELSE 0 END) as pairs_with_examples,
        SUM(CASE WHEN has_formula = 1 THEN 1 ELSE 0 END) as pairs_with_formulas
    FROM qa_pairs
    WHERE indicator_id = ?
''', (indicator_id,))

udr_stats = cursor.fetchone()

print("\n" + "="*70)
print("ULTRA DEEP RESEARCH STATISTICS")
print("="*70)
print(f"Total pairs: {udr_stats[0]:,}")
print(f"Average answer length: {udr_stats[1]:.1f} chars")
print(f"Answer length range: {udr_stats[2]}-{udr_stats[3]} chars")
print(f"Pairs with examples: {udr_stats[4]:,} ({udr_stats[4]/udr_stats[0]*100:.1f}%)")
print(f"Pairs with formulas: {udr_stats[5]:,} ({udr_stats[5]/udr_stats[0]*100:.1f}%)")

conn.close()

print("\n" + "="*70)
print("SUCCESS!")
print("="*70)
print(f"Ultra Deep Research integration complete!")
print(f"Database now contains {final_pairs:,} Q&A pairs")
print(f"Ready for use!")
