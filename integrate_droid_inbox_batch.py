"""
Integrate Droid Inbox Batch - Perpetual Mining Test
====================================================

Integrates new indicator Q&A pairs from Droid's inbox.
Part of first perpetual mining journey.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

def integrate_droid_inbox():
    """Integrate all JSON files from inbox/droid/"""

    # Connect to database
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()

    # Get inbox files
    inbox_path = Path('inbox/droid')
    json_files = list(inbox_path.glob('*.json'))

    print(f"Found {len(json_files)} files to integrate")
    print()

    total_pairs_added = 0
    total_indicators_added = 0
    files_processed = 0

    for json_file in sorted(json_files):
        try:
            # Load data
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if it's the nested format from Droid
            if isinstance(data, dict) and 'qa_pairs' in data:
                indicator_name = data.get('indicator', json_file.stem.replace('_qa_pairs', ''))
                category = data.get('category', 'Technical Indicators')
                pairs_data = data['qa_pairs']
            elif isinstance(data, list):
                # Old format - direct list
                if not data:
                    print(f"Skipping {json_file.name}: empty")
                    continue
                indicator_name = data[0].get('indicator', json_file.stem.replace('_qa_pairs', ''))
                category = data[0].get('category', 'Technical Indicators')
                pairs_data = data
            else:
                print(f"Skipping {json_file.name}: unknown format")
                continue

            if not pairs_data:
                print(f"Skipping {json_file.name}: no pairs")
                continue

            # Check if indicator exists
            c.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
            result = c.fetchone()

            if result:
                indicator_id = result[0]
            else:
                # Create new indicator
                c.execute('''INSERT INTO crypto_indicators (indicator_name, indicator_category, description)
                           VALUES (?, ?, ?)''',
                          (indicator_name, category, f'{indicator_name} technical indicator'))
                indicator_id = c.lastrowid
                total_indicators_added += 1

            # Get max pair_number for this indicator
            c.execute('SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?', (indicator_id,))
            max_pair = c.fetchone()[0]

            # Insert pairs
            pairs_added = 0
            for i, pair in enumerate(pairs_data, start=max_pair + 1):
                question = pair.get('question', '')
                answer = pair.get('answer', '')
                topic = pair.get('topic', indicator_name)

                if not question or not answer:
                    continue

                # Check for duplicate
                c.execute('''SELECT qa_id FROM qa_pairs
                           WHERE indicator_id = ? AND question = ?''',
                          (indicator_id, question))
                if c.fetchone():
                    continue  # Skip duplicate

                # Insert
                c.execute('''INSERT INTO qa_pairs
                           (indicator_id, pair_number, question, answer, topic, created_date,
                            indicator_name, difficulty_level, answer_length,
                            has_formula, has_examples, has_sources, crypto_specific)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (indicator_id, i, question, answer, topic,
                           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           indicator_name,
                           pair.get('difficulty_level', 'intermediate'),
                           len(answer),
                           1 if any(x in answer.lower() for x in ['formula', 'calculation', '=']) else 0,
                           1 if any(x in answer.lower() for x in ['example', 'for instance']) else 0,
                           1 if any(x in answer.lower() for x in ['source', 'according to']) else 0,
                           1 if any(x in answer.lower() for x in ['crypto', 'bitcoin', 'blockchain']) else 0))
                pairs_added += 1

            conn.commit()
            files_processed += 1
            total_pairs_added += pairs_added

            print(f"[{files_processed}/{len(json_files)}] {json_file.name}")
            print(f"    Indicator: {indicator_name}")
            print(f"    Pairs added: {pairs_added}")
            print()

        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            continue

    # Final stats
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    final_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM crypto_indicators')
    indicator_count = c.fetchone()[0]

    conn.close()

    print("="*80)
    print("INTEGRATION COMPLETE")
    print("="*80)
    print(f"Files processed: {files_processed}")
    print(f"New indicators: {total_indicators_added}")
    print(f"New pairs added: {total_pairs_added}")
    print(f"Total pairs in DB: {final_count}")
    print(f"Total indicators: {indicator_count}")
    print("="*80)

    return {
        'files_processed': files_processed,
        'pairs_added': total_pairs_added,
        'indicators_added': total_indicators_added,
        'final_count': final_count
    }

if __name__ == "__main__":
    result = integrate_droid_inbox()
