"""
Clean and Re-integrate Session 42 - NFT Metrics Part 1
Removes incorrect data and properly integrates the 500 Q&A pairs
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

print("="*80)
print("SESSION 42 CLEAN AND RE-INTEGRATION")
print("="*80)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Step 1: Delete existing Session 42 data
print("\nStep 1: Cleaning existing Session 42 data...")
cursor.execute("SELECT id FROM crypto_indicators WHERE session_number = 42")
indicator_ids = [row[0] for row in cursor.fetchall()]

if indicator_ids:
    print(f"  Found {len(indicator_ids)} existing indicators: {indicator_ids}")

    # Delete Q&A pairs
    cursor.execute(f"DELETE FROM qa_pairs WHERE indicator_id IN ({','.join(map(str, indicator_ids))})")
    deleted_qa = cursor.rowcount
    print(f"  Deleted {deleted_qa} Q&A pairs")

    # Delete indicators
    cursor.execute("DELETE FROM crypto_indicators WHERE session_number = 42")
    deleted_indicators = cursor.rowcount
    print(f"  Deleted {deleted_indicators} indicators")

    conn.commit()
    print("  Database cleaned!")
else:
    print("  No existing Session 42 data found")

# Step 2: Parse source file MORE CAREFULLY
print("\nStep 2: Parsing source file...")

with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all Q&A pairs using a more flexible pattern
def extract_all_qa_pairs(text, indicator_name):
    """Extract Q&A pairs more carefully"""
    pairs = []

    # Split by sections if present
    sections = ['FUNDAMENTALS', 'INTERPRETATION', 'ADVANCED', 'TRADING APPLICATIONS', 'MARKET ANALYSIS']

    # Pattern that handles multi-line answers
    pattern = r'Q(\d+):\s*(.*?)\n+A\1:\s*(.*?)(?=\n+Q\d+:|$)'

    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        pair_num = int(match.group(1))
        question = match.group(2).strip()
        answer = match.group(3).strip()

        # Clean up whitespace
        question = ' '.join(question.split())
        answer = ' '.join(answer.split())

        if question and answer and len(answer) > 50:  # Filter out incomplete data
            pairs.append({
                'pair_number': pair_num,
                'question': question,
                'answer': answer
            })

    return pairs

# Define indicators
INDICATORS = [
    "NFT SALES VOLUME",
    "FLOOR PRICE",
    "UNIQUE BUYERS",
    "NFT MARKET CAP",
    "BLUE CHIP NFT INDEX"
]

indicator_data = {}

# Split content by indicator sections
for indicator in INDICATORS:
    # Find the section for this indicator
    pattern = rf'={70,}\s*\n\d+[️⃣]+\s+{re.escape(indicator)}\s*\([^\)]+\)\s*\n={70,}(.*?)(?=\n={70,}\s*\n\d+[️⃣]+|\Z)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        section_content = match.group(1)
        pairs = extract_all_qa_pairs(section_content, indicator)

        # Normalize indicator name
        normalized_name = indicator.title().replace('Nft', 'NFT')
        indicator_data[normalized_name] = pairs

        print(f"  {normalized_name}: {len(pairs)} Q&A pairs extracted")
    else:
        print(f"  WARNING: Could not find section for {indicator}")

total_extracted = sum(len(pairs) for pairs in indicator_data.values())
print(f"\n  Total Q&A pairs extracted: {total_extracted}")

if total_extracted < 400:
    print("\n  ERROR: Not enough Q&A pairs extracted!")
    print("  Please check the source file format.")
    conn.close()
    exit(1)

# Step 3: Create indicator records
print("\nStep 3: Creating indicator records...")

indicator_map = {}
INDICATOR_DEFINITIONS = {
    'Nft Sales Volume': {
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
    'Nft Market Cap': {
        'display_name': 'NFT Market Capitalization',
        'description': 'Total valuation of an NFT collection (floor price x total supply)'
    },
    'Blue Chip Nft Index': {
        'display_name': 'Blue Chip NFT Index',
        'description': 'Composite index tracking performance of top-tier NFT collections'
    }
}

for indicator_name in indicator_data.keys():
    defn = INDICATOR_DEFINITIONS.get(indicator_name, {})

    cursor.execute("""
        INSERT INTO crypto_indicators (
            indicator_name, indicator_category, session_number,
            display_name, description
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        indicator_name,
        CATEGORY,
        SESSION_NUMBER,
        defn.get('display_name', indicator_name),
        defn.get('description', '')
    ))

    indicator_id = cursor.lastrowid
    indicator_map[indicator_name] = indicator_id
    print(f"  Created: {indicator_name} (ID: {indicator_id})")

conn.commit()

# Step 4: Insert Q&A pairs
print("\nStep 4: Inserting Q&A pairs...")

def analyze_answer(answer):
    """Analyze answer content"""
    answer_lower = answer.lower()

    # Determine difficulty
    difficulty = 'beginner'
    if any(kw in answer_lower for kw in ['formula', 'calculate', 'equation', 'algorithm']):
        difficulty = 'advanced'
    elif any(kw in answer_lower for kw in ['strategy', 'interpretation', 'divergence', 'advanced']):
        difficulty = 'intermediate'

    # Detect features
    has_formula = bool(re.search(r'[=×÷\+\-\*/]\s*\w+|formula|equation|calculate', answer_lower))
    has_examples = bool(re.search(r'example|for instance|e\.g\.|such as|\$[\d,]+|bored ape|cryptopunks|azuki', answer_lower))
    has_sources = bool(re.search(r'source|opensea|blur|looksrare|nftgo|dune|research|study', answer_lower))

    # Generate tags
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
    if 'liquidity' in answer_lower:
        tags.append('liquidity')
    if 'market cap' in answer_lower or 'valuation' in answer_lower:
        tags.append('valuation')
    if 'blue chip' in answer_lower or 'bayc' in answer_lower or 'cryptopunks' in answer_lower:
        tags.append('blue-chip')

    return {
        'difficulty_level': difficulty,
        'has_formula': has_formula,
        'has_examples': has_examples,
        'has_sources': has_sources,
        'answer_length': len(answer),
        'tags': json.dumps(tags) if tags else None
    }

total_inserted = 0
for indicator_name, pairs in indicator_data.items():
    indicator_id = indicator_map[indicator_name]
    print(f"\n  Processing: {indicator_name} ({len(pairs)} pairs)")

    for pair in pairs:
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

        total_inserted += 1

    print(f"    Inserted {len(pairs)} pairs")

conn.commit()
print(f"\n  Total Q&A pairs inserted: {total_inserted}")

# Step 5: Verification
print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM crypto_indicators WHERE session_number = 42")
ind_count = cursor.fetchone()[0]
print(f"\nIndicators: {ind_count} (expected: 5)")

cursor.execute("""
    SELECT i.indicator_name, COUNT(q.qa_id)
    FROM crypto_indicators i
    LEFT JOIN qa_pairs q ON i.id = q.indicator_id
    WHERE i.session_number = 42
    GROUP BY i.id
    ORDER BY i.indicator_name
""")

print("\nQ&A Pairs by Indicator:")
total_qa = 0
for row in cursor.fetchall():
    total_qa += row[1]
    print(f"  {row[0]}: {row[1]} pairs")

print(f"\nTotal Q&A pairs: {total_qa}")
print(f"Expected: ~500 (actual file had {total_extracted})")

# Check metadata
cursor.execute("""
    SELECT difficulty_level, COUNT(*) as cnt
    FROM qa_pairs q
    JOIN crypto_indicators i ON q.indicator_id = i.id
    WHERE i.session_number = 42
    GROUP BY difficulty_level
""")

print("\nDifficulty distribution:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} pairs")

# Sample check
print("\nSample Q&A pairs:")
cursor.execute("""
    SELECT i.indicator_name, q.pair_number, q.question, LENGTH(q.answer)
    FROM qa_pairs q
    JOIN crypto_indicators i ON q.indicator_id = i.id
    WHERE i.session_number = 42
    ORDER BY i.id, q.pair_number
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"  {row[0]} Q{row[1]}: {row[2][:50]}... ({row[3]} chars)")

print("\n" + "="*80)
print(f"INTEGRATION COMPLETE!")
print("="*80)

conn.close()
