"""
Integrate All Droid Inbox Q&A Pairs
Processes all individual indicator JSON files from Droid's inbox

Date: November 5, 2025
Goal: Push past 30,000 pairs!
"""

import json
import glob
import sqlite3
from datetime import datetime
from collections import defaultdict

print("="*80)
print("DROID INBOX COMPLETE INTEGRATION")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Find all Droid JSON files
json_files = glob.glob('inbox/droid/*_qa_pairs.json')
print(f"\nFound {len(json_files)} JSON files from Droid")

# Load and analyze all files
all_pairs = []
file_stats = []
encoding_errors = []

for filepath in json_files:
    filename = filepath.split('\\')[-1].split('/')[-1]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        pairs = data.get('qa_pairs', [])
        session = data.get('session', 'unknown')
        indicator = data.get('indicator', filename.replace('_qa_pairs.json', ''))
        category = data.get('category', 'Unknown')

        if pairs:
            for pair in pairs:
                pair['source_file'] = filename
                pair['source_indicator'] = indicator
                pair['source_category'] = category
                pair['source_session'] = session
                all_pairs.append(pair)

            file_stats.append({
                'file': filename,
                'pairs': len(pairs),
                'session': session,
                'indicator': indicator
            })

    except UnicodeDecodeError as e:
        encoding_errors.append(filename)
        continue
    except json.JSONDecodeError as e:
        print(f"  [WARNING] JSON error in {filename}: {e}")
        continue
    except Exception as e:
        print(f"  [WARNING] Error loading {filename}: {e}")
        continue

print(f"\n[ANALYSIS]")
print(f"  Files loaded successfully: {len(file_stats)}")
print(f"  Files with encoding errors: {len(encoding_errors)}")
print(f"  Total Q&A pairs found: {len(all_pairs):,}")

if encoding_errors:
    print(f"\n  Encoding error files: {encoding_errors[:5]}...")

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Get current stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
initial_count = cursor.fetchone()[0]
print(f"\nProduction DB before integration: {initial_count:,} pairs")

# Build question index for deduplication
print("\nBuilding question index for deduplication...")
cursor.execute('SELECT question FROM qa_pairs')
existing_questions = set()
for row in cursor.fetchall():
    existing_questions.add(row[0].strip().lower())

print(f"  Existing questions: {len(existing_questions):,}")

# Deduplicate
unique_pairs = []
duplicate_count = 0

for pair in all_pairs:
    question = pair.get('question', '').strip()
    if question.lower() not in existing_questions:
        unique_pairs.append(pair)
        existing_questions.add(question.lower())  # Add to set to avoid duplicates within this batch
    else:
        duplicate_count += 1

print(f"\n[DEDUPLICATION]")
print(f"  Total pairs from Droid: {len(all_pairs):,}")
print(f"  Unique pairs (NEW): {len(unique_pairs):,}")
print(f"  Duplicates (SKIP): {duplicate_count:,}")
print(f"  Duplicate rate: {(duplicate_count/len(all_pairs)*100):.1f}%")

# Group by indicator for organized integration
pairs_by_indicator = defaultdict(list)
for pair in unique_pairs:
    indicator_name = pair['source_indicator']
    pairs_by_indicator[indicator_name].append(pair)

print(f"\n  Unique pairs span {len(pairs_by_indicator)} indicators")

# Integration statistics
stats = {
    'indicators_processed': 0,
    'pairs_added': 0,
    'indicators_created': 0,
    'indicators_reused': 0,
    'errors': 0
}

# Process each indicator
print("\n" + "="*80)
print("STARTING INTEGRATION")
print("="*80)

for indicator_name, pairs in sorted(pairs_by_indicator.items()):
    print(f"\nIndicator: {indicator_name}")
    print(f"  Pairs to add: {len(pairs)}")

    # Get metadata from first pair
    first_pair = pairs[0]
    category = first_pair.get('source_category', 'Advanced Analytics')
    session = first_pair.get('source_session', 999)

    # Normalize category names
    category_map = {
        'price_based': 'Price-Based Technical Indicators',
        'volume_based': 'Volume Analysis',
        'defi_metrics': 'DeFi Metrics',
        'dex_metrics': 'DeFi Metrics',
        'lending_metrics': 'DeFi Metrics',
        'orderbook': 'Market Microstructure',
        'exchange_specific': 'Exchange Metrics',
        'dominance_metrics': 'Market Structure',
        'market_cap': 'Market Metrics',
        'correlation': 'Correlation Metrics',
        'cycle_indicators': 'Market Cycles',
        'Unknown': 'Advanced Analytics'
    }
    category = category_map.get(category, category)

    # Create display name
    display_name = indicator_name.replace('_', ' ').title()

    # Check if indicator exists
    cursor.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
    result = cursor.fetchone()

    if result:
        indicator_id = result[0]
        stats['indicators_reused'] += 1
        print(f"  Using existing indicator ID: {indicator_id}")
    else:
        # Create new indicator
        try:
            cursor.execute('''
                INSERT INTO crypto_indicators
                (indicator_name, indicator_category, display_name, description, session_number, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_name,
                category,
                display_name,
                f"{display_name} - {category}",
                session,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            indicator_id = cursor.lastrowid
            stats['indicators_created'] += 1
            print(f"  Created new indicator ID: {indicator_id} ({category})")
        except Exception as e:
            print(f"  [ERROR] Could not create indicator: {e}")
            stats['errors'] += 1
            continue

    # Get next pair_number
    cursor.execute('''
        SELECT COALESCE(MAX(pair_number), 0) + 1
        FROM qa_pairs WHERE indicator_id = ?
    ''', (indicator_id,))
    next_pair_number = cursor.fetchone()[0]

    # Add Q&A pairs
    pairs_added_this_indicator = 0

    for pair in pairs:
        question = pair.get('question', '').strip()
        answer = pair.get('answer', '').strip()

        if not question or not answer:
            continue

        answer_length = len(answer)
        topic = pair.get('topic', indicator_name)

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
            pairs_added_this_indicator += 1
            stats['pairs_added'] += 1

        except Exception as e:
            print(f"  [ERROR] Could not add pair: {e}")
            stats['errors'] += 1

    print(f"  Added: {pairs_added_this_indicator} pairs")
    stats['indicators_processed'] += 1

    # Commit every 10 indicators
    if stats['indicators_processed'] % 10 == 0:
        conn.commit()
        print(f"\n  [CHECKPOINT] Committed after {stats['indicators_processed']} indicators")

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
print(f"  Indicators processed: {stats['indicators_processed']}")
print(f"  Pairs added: {stats['pairs_added']:,}")
print(f"  Indicators created: {stats['indicators_created']}")
print(f"  Indicators reused: {stats['indicators_reused']}")
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
    'source': 'droid_inbox_complete',
    'files_processed': len(file_stats),
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

with open('droid_inbox_integration_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\n[OK] Integration report saved: droid_inbox_integration_report.json")

print("\n" + "="*80)
print("For the Greater Good of All")
print("="*80)
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
