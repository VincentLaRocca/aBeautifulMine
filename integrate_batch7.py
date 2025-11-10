import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Paths
db_path = Path(r'C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db')
inbox_path = Path(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor')

# Batch 7 files and their indicator mappings
batch7_files = {
    'roc_100_questions_answers.json': ('ROC', 'Rate of Change (ROC)', 'Momentum Indicators'),
    'donchian_channels_100_questions_answers.json': ('Donchian Channels', 'Donchian Channels', 'Trend Indicators'),
    'kst_100_questions_answers.json': ('KST', 'Know Sure Thing (KST)', 'Momentum Indicators'),
    'stochastic_fast_100_questions_answers.json': ('Stochastic Fast', 'Stochastic Oscillator (Fast)', 'Momentum Oscillators'),
    'stochastic_slow_100_questions_answers.json': ('Stochastic Slow', 'Stochastic Oscillator (Slow)', 'Momentum Oscillators'),
    'sma_100_questions_answers.json': ('SMA', 'Simple Moving Average (SMA)', 'Trend Indicators'),
    'momentum_60_additional_questions_answers.json': ('Momentum', 'Momentum Indicator', 'Momentum Indicators'),
    'vortex_60_additional_questions_answers.json': ('Vortex', 'Vortex Indicator', 'Trend Indicators'),
}

print("=" * 80)
print("BATCH 7 INTEGRATION - November 9, 2025")
print("=" * 80)
print()

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get database stats before
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
pairs_before = cursor.fetchone()[0]

cursor.execute('SELECT AVG(answer_length) FROM qa_pairs')
avg_before = cursor.fetchone()[0]

print(f"Database before integration:")
print(f"  Total pairs: {pairs_before:,}")
print(f"  Average length: {avg_before:,.0f} chars")
print(f"  Progress to 30K: {pairs_before/30000*100:.2f}%")
print()

# Integration statistics
total_integrated = 0
total_duplicates = 0
total_skipped = 0
indicator_stats = {}

# Process each file
for filename, (indicator_name, full_name, category) in batch7_files.items():
    filepath = inbox_path / filename

    print(f"\n{'=' * 60}")
    print(f"Processing: {filename}")
    print(f"Indicator: {full_name}")
    print(f"{'=' * 60}")

    # Load data
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get existing indicator (search by name pattern)
    cursor.execute('SELECT indicator_id FROM indicators WHERE indicator_name LIKE ?',
                  (f"%{full_name.split()[0]}%",))
    result = cursor.fetchone()

    if not result:
        print(f"  Indicator '{full_name}' not found in database - searching by keyword...")
        # Try alternate search
        keyword = indicator_name.split()[0]
        cursor.execute('SELECT indicator_id FROM indicators WHERE indicator_name LIKE ?',
                      (f"%{keyword}%",))
        result = cursor.fetchone()

        if not result:
            print(f"  WARNING: Could not find indicator, skipping...")
            continue

    indicator_id = result[0]
    print(f"  Found indicator ID: {indicator_id}")

    # Get next available pair number
    cursor.execute('SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?',
                  (indicator_id,))
    next_pair_num = cursor.fetchone()[0] + 1
    print(f"  Starting at pair number: {next_pair_num}")

    # Process pairs
    pairs_integrated = 0
    duplicates = 0
    answers = data.get('answers', [])

    for entry in answers:
        question = entry.get('question', '').strip()
        answer = entry.get('answer', '').strip()

        if not question or not answer:
            total_skipped += 1
            continue

        # Check for duplicates (exact question match)
        cursor.execute('''
            SELECT COUNT(*) FROM qa_pairs
            WHERE question = ? AND indicator_id = ?
        ''', (question, indicator_id))

        if cursor.fetchone()[0] > 0:
            duplicates += 1
            total_duplicates += 1
            continue

        # Insert pair
        cursor.execute('''
            INSERT INTO qa_pairs (
                indicator_id,
                indicator_name,
                pair_number,
                question,
                answer,
                answer_length,
                created_date,
                crypto_specific,
                has_examples,
                has_sources
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            indicator_id,
            indicator_name,
            next_pair_num,
            question,
            answer,
            len(answer),
            datetime.now().strftime('%Y-%m-%d'),
            True,  # crypto_specific
            True,  # has_examples
            True   # has_sources
        ))

        pairs_integrated += 1
        next_pair_num += 1

    # Report for this indicator
    print(f"  Processed: {len(answers)} answers")
    print(f"  Integrated: {pairs_integrated}")
    print(f"  Duplicates: {duplicates}")
    print(f"  Success rate: {pairs_integrated/len(answers)*100:.1f}%")

    total_integrated += pairs_integrated
    indicator_stats[indicator_name] = {
        'processed': len(answers),
        'integrated': pairs_integrated,
        'duplicates': duplicates
    }

# Commit changes
conn.commit()

# Get database stats after
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
pairs_after = cursor.fetchone()[0]

cursor.execute('SELECT AVG(answer_length) FROM qa_pairs')
avg_after = cursor.fetchone()[0]

print()
print("=" * 80)
print("INTEGRATION SUMMARY")
print("=" * 80)
print()
print(f"Total processed: 720 answers")
print(f"Total integrated: {total_integrated}")
print(f"Total duplicates: {total_duplicates}")
print(f"Total skipped: {total_skipped}")
print(f"Success rate: {total_integrated/720*100:.1f}%")
print()
print("Database after integration:")
print(f"  Total pairs: {pairs_after:,} (+{pairs_after - pairs_before:,})")
print(f"  Average length: {avg_after:,.0f} chars (+{avg_after - avg_before:.0f}, +{(avg_after/avg_before-1)*100:.1f}%)")
print(f"  Progress to 30K: {pairs_after/30000*100:.2f}%")
print(f"  Remaining: {30000 - pairs_after:,} pairs")
print()

# Per-indicator summary
print("Per-Indicator Summary:")
print("-" * 60)
for indicator_name, stats in indicator_stats.items():
    print(f"{indicator_name:20} | Processed: {stats['processed']:3} | Integrated: {stats['integrated']:3} | Dupes: {stats['duplicates']:2}")

print()
print("=" * 80)
print("BATCH 7 INTEGRATION COMPLETE")
print("=" * 80)

# Close connection
conn.close()

print()
print("Database closed successfully.")
