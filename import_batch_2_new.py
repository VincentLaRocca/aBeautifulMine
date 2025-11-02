#!/usr/bin/env python3
"""
Import Batch 2 New Data - Additional Indicators from Droid
Date: 2025-11-02
Purpose: Import 4 new indicators (400 Q&A pairs)

New indicators:
- Bollinger Bands (Session 6)
- Know Sure Thing/KST (Session 6)
- Donchian Channels (Session 7)
- On-Balance Volume/OBV (Session 8)
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_NAME = "crypto_indicators_production.db"
PARSED_DATA_DIR = "parsed_qa_data"

# New indicators mapping
NEW_INDICATORS = {
    "bollinger_bands": {
        "session": 6,
        "name": "Bollinger Bands",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators"
    },
    "know_sure_thing_kst": {
        "session": 6,
        "name": "Know Sure Thing (KST)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators"
    },
    "donchian_channels": {
        "session": 7,
        "name": "Donchian Channels",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "on-balance_volume_obv": {
        "session": 8,
        "name": "On-Balance Volume (OBV)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    }
}

def slugify(text):
    """Convert indicator name to slug"""
    import re
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '_', slug)
    return slug

def ensure_session_exists(cursor, session_num, category, subcategory):
    """Ensure session exists"""
    cursor.execute("SELECT session_id FROM sessions WHERE session_number = ?", (session_num,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("""
            INSERT INTO sessions (session_number, session_date, category, subcategory, executor, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_num, datetime.now().isoformat(), category, subcategory, "Droid", "partial"))
        print(f"  [*] Created session {session_num} metadata")

def import_indicator(cursor, parsed_file, session_info):
    """Import indicator with Q&A pairs"""

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

    ensure_session_exists(cursor, session_num, category, subcategory)

    # Check if already exists
    cursor.execute("SELECT indicator_id FROM indicators WHERE indicator_slug = ?", (indicator_slug,))
    existing = cursor.fetchone()

    if existing:
        print(f"  [!] Already exists, skipping...")
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

    # Insert Q&A pairs
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
    print("=" * 70)
    print("BATCH 2 IMPORT - New Indicators from Droid")
    print("=" * 70)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    parsed_dir = Path(PARSED_DATA_DIR)

    imported_count = 0
    total_qa = 0

    # Import each new indicator
    for file in sorted(parsed_dir.glob("*_qa_pairs.json")):
        filename = file.stem.replace('_qa_pairs', '')

        # Find matching session info
        session_info = None
        for slug, info in NEW_INDICATORS.items():
            if slug in filename:
                session_info = info
                break

        if not session_info:
            continue

        try:
            qa_count = import_indicator(cursor, file, session_info)
            if qa_count > 0:
                imported_count += 1
                total_qa += qa_count
        except Exception as e:
            print(f"  [ERROR] Failed: {e}")
            conn.rollback()
            continue

    conn.commit()

    # Summary
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)

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

    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_indicators = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa_db = cursor.fetchone()[0]

    print(f"\nDatabase Totals:")
    print(f"  Total Indicators: {total_indicators}")
    print(f"  Total Q&A Pairs: {total_qa_db}")

    print(f"\nThis Import:")
    print(f"  New Indicators: {imported_count}")
    print(f"  New Q&A Pairs: {total_qa}")

    print("\n" + "=" * 70)
    print("[OK] Import complete!")
    print("=" * 70)

    conn.close()

if __name__ == "__main__":
    main()
