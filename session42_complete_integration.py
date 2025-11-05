"""
Complete Session 42 Integration - Clean slate approach
Removes ALL data and does fresh integration
"""

import sqlite3
import re
import json

DB_PATH = r"C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db"
SOURCE_FILE = r"C:\Users\vlaro\dreamteam\session42_nft_metrics_part1_complete.txt"
SESSION_NUMBER = 42

INDICATOR_DEFS = {
    'NFT Sales Volume': 'NFT Sales Volume (24h/7d/30d) - Total dollar value of NFT transactions',
    'Floor Price': 'NFT Floor Price - Lowest listed price in a collection',
    'Unique Buyers': 'Unique Buyers Count - Distinct wallet addresses purchasing NFTs',
    'NFT Market Cap': 'NFT Market Capitalization - Total valuation of NFT collection',
    'Blue Chip NFT Index': 'Blue Chip NFT Index - Performance tracker for top-tier collections'
}

print("="*80)
print("SESSION 42 COMPLETE INTEGRATION")
print("="*80)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# STEP 1: Complete cleanup
print("\n[1/5] Cleaning database...")
cursor.execute("DELETE FROM qa_pairs WHERE indicator_id IN (SELECT id FROM crypto_indicators WHERE session_number = 42)")
deleted_qa = cursor.rowcount
cursor.execute("DELETE FROM crypto_indicators WHERE session_number = 42")
deleted_ind = cursor.rowcount
conn.commit()
print(f"  Deleted: {deleted_ind} indicators, {deleted_qa} Q&A pairs")

# STEP 2: Parse file
print("\n[2/5] Parsing source file...")

with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Find sections by indicator names
indicator_qa = {}

for ind_name in INDICATOR_DEFS.keys():
    # Find the section  for this indicator
    # Look for patterns like: "NFT SALES VOLUME (100 Q&A Pairs)"
    pattern = rf'{re.escape(ind_name.upper())}\s*\(\d+\s+Q&A\s+Pairs\)[^\n]*\n=+(.*?)(?=\n=+\s*\n\d+|$)'

    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        section_text = match.group(1)

        # Extract Q&A pairs
        qa_pattern = r'Q(\d+):\s*(.*?)\s*\nA\1:\s*(.*?)(?=\n\s*Q\d+:|\Z)'
        pairs = []

        for qa_match in re.finditer(qa_pattern, section_text, re.DOTALL):
            pair_num = int(qa_match.group(1))
            question = ' '.join(qa_match.group(2).strip().split())
            answer = ' '.join(qa_match.group(3).strip().split())

            if question and answer and len(answer) > 30:
                pairs.append({
                    'number': pair_num,
                    'question': question,
                    'answer': answer
                })

        indicator_qa[ind_name] = pairs
        print(f"  {ind_name}: {len(pairs)} pairs")
    else:
        print(f"  WARNING: Could not find {ind_name}")

total_pairs = sum(len(pairs) for pairs in indicator_qa.values())
print(f"\n  Total extracted: {total_pairs} Q&A pairs")

# STEP 3: Create indicators
print("\n[3/5] Creating indicators...")

indicator_ids = {}
for ind_name, desc in INDICATOR_DEFS.items():
    cursor.execute("""
        INSERT INTO crypto_indicators (indicator_name, indicator_category, session_number, description)
        VALUES (?, ?, ?, ?)
    """, (ind_name, 'NFT Metrics', SESSION_NUMBER, desc))

    indicator_ids[ind_name] = cursor.lastrowid
    print(f"  Created ID {cursor.lastrowid}: {ind_name}")

conn.commit()

# STEP 4: Insert Q&A pairs
print("\n[4/5] Inserting Q&A pairs...")

def get_difficulty(answer):
    a = answer.lower()
    if any(w in a for w in ['formula', 'calculate', 'algorithm']):
        return 'advanced'
    elif any(w in a for w in ['strategy', 'interpretation', 'analysis']):
        return 'intermediate'
    return 'beginner'

def get_tags(text):
    t = text.lower()
    tags = []
    if 'nft' in t:
        tags.append('nft')
    if 'volume' in t:
        tags.append('volume')
    if 'price' in t or 'floor' in t:
        tags.append('price')
    if 'buyer' in t or 'seller' in t:
        tags.append('trading')
    if 'collection' in t:
        tags.append('collection')
    if 'marketplace' in t:
        tags.append('marketplace')
    if 'blue chip' in t:
        tags.append('blue-chip')
    return json.dumps(tags) if tags else None

total_inserted = 0

for ind_name, pairs in indicator_qa.items():
    ind_id = indicator_ids[ind_name]

    # Renumber pairs sequentially starting from 1 for each indicator
    for idx, pair in enumerate(pairs, 1):
        cursor.execute("""
            INSERT INTO qa_pairs (
                indicator_id, indicator_name, question, answer,
                pair_number, difficulty_level, tags, answer_length,
                crypto_specific, market_year
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ind_id,
            ind_name,
            pair['question'],
            pair['answer'],
            idx,  # Use sequential numbering: 1, 2, 3, ...
            get_difficulty(pair['answer']),
            get_tags(pair['question'] + ' ' + pair['answer']),
            len(pair['answer']),
            1,
            '2024-2025'
        ))

        total_inserted += 1

    print(f"  {ind_name}: {len(pairs)} pairs inserted")

conn.commit()
print(f"\n  Total inserted: {total_inserted}")

# STEP 5: Verify
print("\n[5/5] Verification...")

cursor.execute("SELECT COUNT(*) FROM crypto_indicators WHERE session_number = 42")
n_ind = cursor.fetchone()[0]

cursor.execute("""
    SELECT i.indicator_name, COUNT(q.qa_id)
    FROM crypto_indicators i
    LEFT JOIN qa_pairs q ON i.id = q.indicator_id
    WHERE i.session_number = 42
    GROUP BY i.id
""")

results = cursor.fetchall()
n_qa = sum(r[1] for r in results)

print(f"\n  Indicators: {n_ind}/5")
print(f"  Q&A pairs: {n_qa}/{total_pairs}")
print("\n  Breakdown:")
for name, count in results:
    print(f"    {name}: {count} pairs")

# Sample
print("\n  Sample Q&A:")
cursor.execute("""
    SELECT i.indicator_name, q.pair_number, q.question
    FROM qa_pairs q
    JOIN crypto_indicators i ON q.indicator_id = i.id
    WHERE i.session_number = 42
    ORDER BY i.id, q.pair_number
    LIMIT 3
""")

for row in cursor.fetchall():
    print(f"    {row[0]} Q{row[1]}: {row[2][:50]}...")

print("\n" + "="*80)
if n_ind == 5 and n_qa == total_pairs:
    print("SUCCESS: Integration complete!")
else:
    print(f"WARNING: Expected 5 indicators and {total_pairs} pairs")
print("="*80)

conn.close()
