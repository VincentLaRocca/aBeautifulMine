#!/usr/bin/env python3
"""
Import Batch 1 Parsed Data to Production Database
Date: 2025-11-02
Purpose: Import 11 indicators (1,089 Q&A pairs) from Droid's Batch 1 output

Sessions covered:
- Session 2 (partial): 2 indicators, 200 Q&A
- Session 4 (partial): 3 indicators, 289 Q&A
- Session 5 (complete): 5 indicators, 500 Q&A
- Session 6 (partial): 1 indicator, 100 Q&A
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_NAME = "crypto_indicators_production.db"
PARSED_DATA_DIR = "parsed_qa_data"

# Mapping of indicators to sessions based on SESSION_INDEX.md
INDICATOR_SESSION_MAP = {
    # Session 2 - Trend Indicators (Moving Averages)
    "exponential_moving_average_ema": {
        "session": 2,
        "name": "Exponential Moving Average (EMA)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators"
    },
    "average_directional_index_adx": {
        "session": 2,
        "name": "Average Directional Index (ADX)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators"
    },

    # Session 4 - Momentum Indicators (Part 1)
    "ichimoku_cloud_chikou_span": {
        "session": 4,
        "name": "Ichimoku Cloud (Chikou Span)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "vortex_indicator": {
        "session": 4,
        "name": "Vortex Indicator",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "stochastic_oscillator_fast": {
        "session": 4,
        "name": "Stochastic Oscillator (Fast)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },

    # Session 5 - Momentum Indicators (Part 2)
    "stochastic_oscillator_slow": {
        "session": 5,
        "name": "Stochastic Oscillator (Slow)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "stochastic_oscillator_full": {
        "session": 5,
        "name": "Stochastic Oscillator (Full)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "rate_of_change_roc": {
        "session": 5,
        "name": "Rate of Change (ROC)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "commodity_channel_index_cci": {
        "session": 5,
        "name": "Commodity Channel Index (CCI)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "williams_r": {
        "session": 5,
        "name": "Williams %R",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },

    # Session 6 - Volatility Indicators
    "momentum_indicator": {
        "session": 6,
        "name": "Momentum Indicator",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators"
    }
}

def slugify(text):
    """Convert indicator name to slug for matching"""
    import re
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '_', slug)
    return slug

def ensure_session_exists(cursor, session_num, category, subcategory):
    """Ensure session metadata exists in database"""
    cursor.execute("SELECT session_id FROM sessions WHERE session_number = ?", (session_num,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("""
            INSERT INTO sessions (session_number, session_date, category, subcategory, executor, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_num, datetime.now().isoformat(), category, subcategory, "Droid", "partial"))
        print(f"  [*] Created session {session_num} metadata")

def import_indicator(cursor, parsed_file, session_info):
    """Import a single indicator with all Q&A pairs"""

    with open(parsed_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    indicator_name = session_info['name']
    indicator_slug = slugify(indicator_name)
    session_num = session_info['session']
    category = session_info['category']
    subcategory = session_info['subcategory']

    print(f"\n  Importing: {indicator_name}")
    print(f"  Session: {session_num} | Category: {subcategory}")
    print(f"  Q&A pairs: {data['total_pairs']}")

    # Ensure session exists
    ensure_session_exists(cursor, session_num, category, subcategory)

    # Check if indicator already exists
    cursor.execute("SELECT indicator_id FROM indicators WHERE indicator_slug = ?", (indicator_slug,))
    existing = cursor.fetchone()

    if existing:
        print(f"  [!] Indicator already exists, skipping...")
        return 0

    # Insert indicator
    cursor.execute("""
        INSERT INTO indicators (
            indicator_name, indicator_slug, session_number,
            category, subcategory, description, total_qa_pairs
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        indicator_name,
        indicator_slug,
        session_num,
        category,
        subcategory,
        f"Research generated via ultra_deep_research on {data.get('generation_date', 'Unknown')}",
        data['total_pairs']
    ))

    indicator_id = cursor.lastrowid

    # Insert all Q&A pairs
    qa_pairs = data.get('qa_pairs', [])
    for qa in qa_pairs:
        cursor.execute("""
            INSERT INTO qa_pairs (
                indicator_id, pair_number, question, answer, topic, created_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            indicator_id,
            qa.get('pair_number', 0),
            qa.get('question', ''),
            qa.get('answer', ''),
            qa.get('topic', indicator_name),
            qa.get('created_date', datetime.now().isoformat())
        ))

    print(f"  [OK] Imported {len(qa_pairs)} Q&A pairs")
    return len(qa_pairs)

def main():
    """Main import process"""

    print("=" * 70)
    print("BATCH 1 IMPORT - Droid Parsed Data to Production Database")
    print("=" * 70)
    print(f"Database: {DB_NAME}")
    print(f"Source: {PARSED_DATA_DIR}/")
    print()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    parsed_dir = Path(PARSED_DATA_DIR)

    imported_count = 0
    total_qa = 0

    # Import each indicator
    for file in sorted(parsed_dir.glob("*_qa_pairs.json")):
        # Extract key parts of filename to match with our mapping
        filename = file.stem.replace('_qa_pairs', '')

        # Try to find matching session info
        session_info = None
        for slug, info in INDICATOR_SESSION_MAP.items():
            if slug in filename:
                session_info = info
                break

        if not session_info:
            print(f"\n  [!] Could not map {file.name} to a session, skipping...")
            continue

        try:
            qa_count = import_indicator(cursor, file, session_info)
            if qa_count > 0:
                imported_count += 1
                total_qa += qa_count
        except Exception as e:
            print(f"  [ERROR] Failed to import {file.name}: {e}")
            conn.rollback()
            continue

    # Commit all changes
    conn.commit()

    # Generate summary report
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)

    # Count by session
    cursor.execute("""
        SELECT s.session_number, s.subcategory,
               COUNT(DISTINCT i.indicator_id) as indicators,
               COUNT(qa.qa_id) as qa_pairs
        FROM sessions s
        LEFT JOIN indicators i ON s.session_number = i.session_number
        LEFT JOIN qa_pairs qa ON i.indicator_id = qa.indicator_id
        GROUP BY s.session_number
        ORDER BY s.session_number
    """)

    print("\nBy Session:")
    for row in cursor.fetchall():
        session_num, subcategory, ind_count, qa_count = row
        print(f"  Session {session_num} ({subcategory}): {ind_count} indicators, {qa_count} Q&A")

    # Overall totals
    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_indicators = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa_db = cursor.fetchone()[0]

    print(f"\nDatabase Totals:")
    print(f"  Total Indicators: {total_indicators}")
    print(f"  Total Q&A Pairs: {total_qa_db}")

    print(f"\nThis Import:")
    print(f"  Indicators Imported: {imported_count}")
    print(f"  Q&A Pairs Imported: {total_qa}")

    print("\n" + "=" * 70)
    print("✓ Import complete!")
    print("=" * 70)

    conn.close()

if __name__ == "__main__":
    main()
