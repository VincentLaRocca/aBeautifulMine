import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Paths
inbox = Path(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor')
db_path = r'C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db'

# Files to integrate - BATCH 8 - THE FINAL BATCH!
batch8_files = {
    'futures_open_interest_100_questions_answers.json': 'Futures Open Interest',
    'liquidations_positioning_100_questions_answers.json': 'Liquidations & Positioning',
    'cme_institutional_100_questions_answers.json': 'CME Institutional Positioning',
    'ichimoku_chikou_100_questions_answers.json': 'Ichimoku Cloud (Chikou Span)',
}

print('=' * 90)
print('BATCH 8 INTEGRATION - FINAL PUSH TO 30,000 PAIRS!')
print('=' * 90)
print()

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get initial stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
initial_count = cursor.fetchone()[0]

cursor.execute('SELECT AVG(answer_length) FROM qa_pairs')
initial_avg = cursor.fetchone()[0]

print(f'Initial Database Status:')
print(f'  Total Pairs: {initial_count:,}')
print(f'  Average Length: {initial_avg:,.0f} chars')
print(f'  Progress: {initial_count/30000*100:.2f}% to 30K')
print()
print('=' * 90)
print()

total_integrated = 0
total_duplicates = 0
file_stats = []

for filename, full_name in batch8_files.items():
    filepath = inbox / filename

    print(f'Processing: {filename}')
    print(f'  Indicator: {full_name}')

    # Read JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    answers = data.get('answers', [])
    print(f'  Pairs in file: {len(answers)}')

    # Get or create indicator
    cursor.execute('SELECT indicator_id FROM indicators WHERE indicator_name = ?', (full_name,))
    result = cursor.fetchone()

    if result:
        indicator_id = result[0]
        print(f'  Found indicator ID: {indicator_id}')
    else:
        # Try flexible matching
        search_term = full_name.split()[0]
        cursor.execute('SELECT indicator_id, indicator_name FROM indicators WHERE indicator_name LIKE ?',
                      (f'%{search_term}%',))
        result = cursor.fetchone()

        if result:
            indicator_id, db_name = result
            print(f'  Found indicator ID {indicator_id} via search: {db_name}')
        else:
            print(f'  ⚠️  Indicator not found, creating new: {full_name}')
            cursor.execute('''
                INSERT INTO indicators (indicator_name, indicator_category, created_date)
                VALUES (?, ?, ?)
            ''', (full_name, 'Derivatives', datetime.now().isoformat()))
            indicator_id = cursor.lastrowid
            print(f'  Created new indicator ID: {indicator_id}')

    # Get next pair number
    cursor.execute('SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?',
                  (indicator_id,))
    next_pair_num = cursor.fetchone()[0] + 1
    print(f'  Starting at pair number: {next_pair_num}')

    # Insert pairs
    integrated = 0
    duplicates = 0

    for entry in answers:
        question = entry.get('question', '').strip()
        answer = entry.get('answer', '').strip()

        if not question or not answer:
            continue

        # Check for duplicate question
        cursor.execute('''
            SELECT COUNT(*) FROM qa_pairs
            WHERE question = ? AND indicator_id = ?
        ''', (question, indicator_id))

        if cursor.fetchone()[0] > 0:
            duplicates += 1
            continue

        # Insert new pair
        answer_length = len(answer)

        cursor.execute('''
            INSERT INTO qa_pairs (
                indicator_id, pair_number, question, answer,
                answer_length, created_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            indicator_id, next_pair_num, question, answer,
            answer_length, datetime.now().isoformat()
        ))

        integrated += 1
        next_pair_num += 1

    print(f'  ✅ Integrated: {integrated} pairs')
    if duplicates > 0:
        print(f'  ⚠️  Duplicates: {duplicates} pairs')
    print()

    total_integrated += integrated
    total_duplicates += duplicates
    file_stats.append({
        'name': full_name,
        'integrated': integrated,
        'duplicates': duplicates
    })

# Commit changes
conn.commit()

# Get final stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_count = cursor.fetchone()[0]

cursor.execute('SELECT AVG(answer_length) FROM qa_pairs')
final_avg = cursor.fetchone()[0]

print('=' * 90)
print('BATCH 8 INTEGRATION COMPLETE!')
print('=' * 90)
print()

for stat in file_stats:
    print(f"{stat['name']}:")
    print(f"  Integrated: {stat['integrated']}")
    if stat['duplicates'] > 0:
        print(f"  Duplicates: {stat['duplicates']}")

print()
print('=' * 90)
print('DATABASE IMPACT')
print('=' * 90)
print(f'Initial: {initial_count:,} pairs @ {initial_avg:,.0f} chars avg')
print(f'Final:   {final_count:,} pairs @ {final_avg:,.0f} chars avg')
print(f'Added:   +{final_count - initial_count:,} pairs')
print(f'Quality: +{final_avg - initial_avg:,.0f} chars avg ({(final_avg/initial_avg - 1)*100:+.1f}%)')
print()
print(f'Progress: {initial_count/30000*100:.2f}% → {final_count/30000*100:.2f}%')
print()

if final_count >= 30000:
    print('🎯 🎯 🎯 30,000-PAIR GOAL ACHIEVED! 🎯 🎯 🎯')
    print()
    print(f'FINAL DATABASE: {final_count:,} pairs ({final_count/30000*100:.2f}%)')
    print(f'OVER GOAL: +{final_count - 30000:,} pairs')
    print()
    print('⭐⭐⭐⭐⭐ PROJECT MILESTONE COMPLETE! ⭐⭐⭐⭐⭐')
else:
    print(f'Remaining to 30K: {30000 - final_count:,} pairs')

print('=' * 90)

conn.close()

print()
print('✅ Integration complete! Database updated successfully.')
