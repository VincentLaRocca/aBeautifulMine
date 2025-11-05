"""
Final Session 42 Integration Script - NFT Metrics Part 1
Simple, robust integration of 500 Q&A pairs
"""

import sqlite3
import re
import json
from datetime import datetime

# Configuration
DB_PATH = r"C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db"
SOURCE_FILE = r"C:\Users\vlaro\dreamteam\session42_nft_metrics_part1_complete.txt"
SESSION_NUMBER = 42
CATEGORY = "NFT Metrics"
MARKET_YEAR = "2024-2025"

INDICATOR_DEFINITIONS = {
    'NFT Sales Volume': {
        'display_name': 'NFT Sales Volume (24h/7d/30d)',
        'description': 'Total dollar value of NFT transactions over specific time periods across major marketplaces'
    },
    'Floor Price': {
        'display_name': 'NFT Floor Price',
        'description': 'Lowest listed price for an NFT in a collection, indicating entry-level valuation'
    },
    'Unique Buyers': {
        'display_name': 'Unique Buyers Count',
        'description': 'Number of distinct wallet addresses purchasing NFTs in a given period'
    },
    'NFT Market Cap': {
        'display_name': 'NFT Market Capitalization',
        'description': 'Total valuation of an NFT collection (floor price x total supply)'
    },
    'Blue Chip NFT Index': {
        'display_name': 'Blue Chip NFT Index',
        'description': 'Composite index tracking performance of top-tier NFT collections'
    }
}

print("="*80)
print("SESSION 42 INTEGRATION - NFT Metrics Part 1")
print("="*80)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Read file
with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse by looking for major section headers
def parse_file_simple(content):
    """Simple parser that splits by indicator sections"""
    indicator_data = {}

    # Split content into lines
    lines = content.split('\n')

    current_indicator = None
    current_qa_buffer = []

    for i, line in enumerate(lines):
        # Check if this is an indicator section header (contains =====)
        if '=====' in line and i+1 < len(lines):
            next_line = lines[i+1].strip()

            # Check if next line is an indicator name
            for ind_name in INDICATOR_DEFINITIONS.keys():
                if ind_name.upper() in next_line.upper() and 'Q&A' in next_line.upper():
                    # Save previous indicator data
                    if current_indicator and current_qa_buffer:
                        indicator_data[current_indicator] = '\n'.join(current_qa_buffer)
                        current_qa_buffer = []

                    # Start new indicator
                    current_indicator = ind_name
                    print(f"  Found section: {ind_name}")
                    break
        elif current_indicator:
            # Collect lines for current indicator
            current_qa_buffer.append(line)

    # Save last indicator
    if current_indicator and current_qa_buffer:
        indicator_data[current_indicator] = '\n'.join(current_qa_buffer)

    return indicator_data

print("\nStep 1: Parsing source file...")
indicator_sections = parse_file_simple(content)
print(f"  Found {len(indicator_sections)} indicator sections")

# Extract Q&A pairs from each section
def extract_qa_pairs(text):
    """Extract Q&A pairs using regex"""
    pairs = []

    # Pattern: Q<number>: <question>\nA<number>: <answer>
    pattern = r'Q(\d+):\s*(.*?)\s*\nA\1:\s*(.*?)(?=\n\s*Q\d+:|\Z)'

    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        pair_num = int(match.group(1))
        question = ' '.join(match.group(2).strip().split())
        answer = ' '.join(match.group(3).strip().split())

        if question and answer and len(answer) > 30:
            pairs.append({
                'pair_number': pair_num,
                'question': question,
                'answer': answer
            })

    return pairs

print("\nStep 2: Extracting Q&A pairs...")
all_qa_data = {}
total_pairs = 0

for indicator_name, section_text in indicator_sections.items():
    pairs = extract_qa_pairs(section_text)
    all_qa_data[indicator_name] = pairs
    total_pairs += len(pairs)
    print(f"  {indicator_name}: {len(pairs)} pairs")

print(f"\nTotal pairs extracted: {total_pairs}")

if total_pairs < 100:
    print("ERROR: Too few Q&A pairs extracted!")
    conn.close()
    exit(1)

# Create indicators
print("\nStep 3: Creating indicators...")
indicator_map = {}

for indicator_name, defn in INDICATOR_DEFINITIONS.items():
    try:
        cursor.execute("""
            INSERT INTO crypto_indicators (
                indicator_name, indicator_category, session_number,
                display_name, description
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            indicator_name,
            CATEGORY,
            SESSION_NUMBER,
            defn['display_name'],
            defn['description']
        ))

        indicator_id = cursor.lastrowid
        indicator_map[indicator_name] = indicator_id
        print(f"  Created: {indicator_name} (ID: {indicator_id})")

    except sqlite3.IntegrityError:
        # Indicator exists, get its ID
        cursor.execute("SELECT id FROM crypto_indicators WHERE indicator_name = ?", (indicator_name,))
        indicator_id = cursor.fetchone()[0]
        indicator_map[indicator_name] = indicator_id
        print(f"  Exists: {indicator_name} (ID: {indicator_id})")

conn.commit()

# Insert Q&A pairs
print("\nStep 4: Inserting Q&A pairs...")

def analyze_answer(answer):
    """Quick answer analysis"""
    answer_lower = answer.lower()

    # Difficulty
    if any(kw in answer_lower for kw in ['formula', 'calculate', 'algorithm', 'equation']):
        difficulty = 'advanced'
    elif any(kw in answer_lower for kw in ['strategy', 'interpretation', 'analysis', 'divergence']):
        difficulty = 'intermediate'
    else:
        difficulty = 'beginner'

    # Features
    has_formula = bool(re.search(r'[=×÷\+\-]/|formula|equation', answer_lower))
    has_examples = bool(re.search(r'example|for instance|e\.g\.|bored ape|cryptopunks|azuki|\$[\d,]+', answer_lower))
    has_sources = bool(re.search(r'opensea|blur|looksrare|nftgo|dune analytics', answer_lower))

    # Tags
    tags = []
    if 'nft' in answer_lower:
        tags.append('nft')
    if 'volume' in answer_lower:
        tags.append('volume')
    if 'floor' in answer_lower or 'price' in answer_lower:
        tags.append('price')
    if 'buyer' in answer_lower or 'seller' in answer_lower:
        tags.append('trading')
    if 'collection' in answer_lower:
        tags.append('collection')
    if 'marketplace' in answer_lower:
        tags.append('marketplace')
    if 'blue chip' in answer_lower:
        tags.append('blue-chip')

    return {
        'difficulty_level': difficulty,
        'has_formula': has_formula,
        'has_examples': has_examples,
        'has_sources': has_sources,
        'answer_length': len(answer),
        'tags': json.dumps(tags) if tags else None
    }

inserted_count = 0
error_count = 0

for indicator_name, pairs in all_qa_data.items():
    if indicator_name not in indicator_map:
        print(f"  WARNING: No ID for {indicator_name}, skipping")
        continue

    indicator_id = indicator_map[indicator_name]
    print(f"\n  Processing: {indicator_name}")

    for pair in pairs:
        try:
            metadata = analyze_answer(pair['answer'])

            cursor.execute("""
                INSERT INTO qa_pairs (
                    indicator_id, indicator_name, question, answer,
                    pair_number, difficulty_level, tags, answer_length,
                    has_formula, has_examples, has_sources,
                    crypto_specific, market_year
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                indicator_id,
                indicator_name,
                pair['question'],
                pair['answer'],
                pair['pair_number'],
                metadata['difficulty_level'],
                metadata['tags'],
                metadata['answer_length'],
                metadata['has_formula'],
                metadata['has_examples'],
                metadata['has_sources'],
                1,
                MARKET_YEAR
            ))

            inserted_count += 1

        except sqlite3.Error as e:
            error_count += 1
            if error_count <= 5:
                print(f"    Error on Q{pair['pair_number']}: {e}")

    print(f"    Inserted: {len(pairs)} pairs")

conn.commit()
print(f"\nTotal inserted: {inserted_count}")
print(f"Errors: {error_count}")

# Verification
print("\n" + "="*80)
print("VERIFICATION REPORT")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM crypto_indicators WHERE session_number = 42")
ind_count = cursor.fetchone()[0]
print(f"\n1. Indicators: {ind_count}/5")

cursor.execute("""
    SELECT i.indicator_name, COUNT(q.qa_id)
    FROM crypto_indicators i
    LEFT JOIN qa_pairs q ON i.id = q.indicator_id
    WHERE i.session_number = 42
    GROUP BY i.id
    ORDER BY i.indicator_name
""")

print("\n2. Q&A Pairs by Indicator:")
total_qa = 0
for row in cursor.fetchall():
    total_qa += row[1]
    status = "[OK]" if row[1] >= 80 else "[LOW]"
    print(f"  {status} {row[0]}: {row[1]} pairs")

print(f"\n3. Total Q&A pairs: {total_qa}")

# Metadata stats
cursor.execute("""
    SELECT
        difficulty_level,
        COUNT(*) as cnt,
        AVG(answer_length) as avg_len
    FROM qa_pairs q
    JOIN crypto_indicators i ON q.indicator_id = i.id
    WHERE i.session_number = 42
    GROUP BY difficulty_level
""")

print("\n4. Difficulty Distribution:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} pairs (avg {int(row[2])} chars)")

# Sample data
print("\n5. Sample Q&A pairs:")
cursor.execute("""
    SELECT i.indicator_name, q.pair_number, q.question
    FROM qa_pairs q
    JOIN crypto_indicators i ON q.indicator_id = i.id
    WHERE i.session_number = 42
    ORDER BY i.id, q.pair_number
    LIMIT 5
""")

for row in cursor.fetchall():
    print(f"  {row[0]} Q{row[1]}: {row[2][:60]}...")

print("\n" + "="*80)
print("INTEGRATION COMPLETE!")
print("="*80)
print(f"\nDatabase: {DB_PATH}")
print(f"Session: {SESSION_NUMBER}")
print(f"Indicators: {ind_count}")
print(f"Q&A Pairs: {total_qa}")
print(f"Status: {'SUCCESS' if total_qa >= 400 else 'PARTIAL'}")
print("="*80)

conn.close()
