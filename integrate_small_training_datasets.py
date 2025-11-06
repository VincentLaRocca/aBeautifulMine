"""
Integrate Small Training Datasets
Integrates high-quality training data: Bitcoin, Rollups, Stablecoins, QA Harvest

Date: November 5, 2025
Target: +110 pairs
"""

import json
import sqlite3
from datetime import datetime

print("="*80)
print("SMALL TRAINING DATASETS INTEGRATION")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Define datasets to integrate
datasets = [
    {
        'path': 'C:/users/vlaro/claude_shared/data/qa_harvest/processed/bitcoin_digital_gold_training.json',
        'indicator_name': 'Bitcoin Digital Gold Narrative',
        'category': 'Fundamental Analysis',
        'session': 200
    },
    {
        'path': 'C:/users/vlaro/claude_shared/data/qa_harvest/processed/rollups_training_data.json',
        'indicator_name': 'Layer 2 Rollups Technology',
        'category': 'Technical Infrastructure',
        'session': 201
    },
    {
        'path': 'C:/users/vlaro/claude_shared/data/qa_harvest/processed/stablecoins_training_data.json',
        'indicator_name': 'Stablecoin Mechanisms',
        'category': 'DeFi Metrics',
        'session': 202
    },
    {
        'path': 'C:/users/vlaro/claude_shared/data/qa_harvest/processed/qa_harvest_latest.json',
        'indicator_name': 'General Cryptocurrency Concepts',
        'category': 'Educational Content',
        'session': 203
    }
]

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

# Integration statistics
stats = {
    'datasets_processed': 0,
    'pairs_added': 0,
    'duplicates_skipped': 0,
    'indicators_created': 0,
    'errors': 0,
    'dataset_breakdown': []
}

# Process each dataset
print("\n" + "="*80)
print("STARTING INTEGRATION")
print("="*80)

for dataset_info in datasets:
    path = dataset_info['path']
    indicator_name = dataset_info['indicator_name']
    category = dataset_info['category']
    session = dataset_info['session']

    print(f"\n[Dataset: {indicator_name}]")
    print(f"  File: {path.split('/')[-1]}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract Q&A pairs
        qa_pairs = data.get('qa_pairs', [])
        print(f"  Total pairs in file: {len(qa_pairs)}")

        if not qa_pairs:
            print(f"  [WARNING] No Q&A pairs found")
            continue

        # Deduplicate
        unique_pairs = []
        for pair in qa_pairs:
            question = pair.get('question', '').strip()
            if question.lower() not in existing_questions:
                unique_pairs.append(pair)
                existing_questions.add(question.lower())
            else:
                stats['duplicates_skipped'] += 1

        print(f"  Unique pairs to add: {len(unique_pairs)}")

        if not unique_pairs:
            print(f"  [INFO] All pairs are duplicates, skipping")
            continue

        # Check if indicator exists
        cursor.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
        result = cursor.fetchone()

        if result:
            indicator_id = result[0]
            print(f"  Using existing indicator ID: {indicator_id}")
        else:
            # Create new indicator
            cursor.execute('''
                INSERT INTO crypto_indicators
                (indicator_name, indicator_category, display_name, description, session_number, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_name,
                category,
                indicator_name,
                data.get('topic', indicator_name),
                session,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            indicator_id = cursor.lastrowid
            stats['indicators_created'] += 1
            print(f"  Created new indicator ID: {indicator_id}")

        # Get next pair_number
        cursor.execute('''
            SELECT COALESCE(MAX(pair_number), 0) + 1
            FROM qa_pairs WHERE indicator_id = ?
        ''', (indicator_id,))
        next_pair_number = cursor.fetchone()[0]

        # Add pairs
        pairs_added_this_dataset = 0

        for pair in unique_pairs:
            question = pair.get('question', '').strip()
            answer = pair.get('answer', '').strip()

            if not question or not answer:
                continue

            answer_length = len(answer)
            topic = data.get('topic', indicator_name)

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
                pairs_added_this_dataset += 1
                stats['pairs_added'] += 1

            except Exception as e:
                print(f"  [ERROR] Could not add pair: {e}")
                stats['errors'] += 1

        print(f"  Added: {pairs_added_this_dataset} pairs")

        stats['dataset_breakdown'].append({
            'dataset': indicator_name,
            'file': path.split('/')[-1],
            'total_pairs': len(qa_pairs),
            'unique_pairs': len(unique_pairs),
            'added': pairs_added_this_dataset,
            'duplicates': len(qa_pairs) - len(unique_pairs)
        })

        stats['datasets_processed'] += 1

    except FileNotFoundError:
        print(f"  [ERROR] File not found: {path}")
        stats['errors'] += 1
        continue
    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON decode error: {e}")
        stats['errors'] += 1
        continue
    except Exception as e:
        print(f"  [ERROR] Unexpected error: {e}")
        stats['errors'] += 1
        continue

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
print(f"  Datasets processed: {stats['datasets_processed']}")
print(f"  Pairs added: {stats['pairs_added']:,}")
print(f"  Duplicates skipped: {stats['duplicates_skipped']}")
print(f"  Indicators created: {stats['indicators_created']}")
print(f"  Errors: {stats['errors']}")

print(f"\n[DATASET BREAKDOWN]")
for dataset in stats['dataset_breakdown']:
    print(f"  {dataset['dataset']}:")
    print(f"    Total: {dataset['total_pairs']}, Unique: {dataset['unique_pairs']}, Added: {dataset['added']}")

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
    'source': 'small_training_datasets',
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

with open('small_datasets_integration_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\n[OK] Integration report saved: small_datasets_integration_report.json")

print("\n" + "="*80)
print("For the Greater Good of All")
print("="*80)
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
