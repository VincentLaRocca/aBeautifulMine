#!/usr/bin/env python3
"""
Import Batch 3 - RAG Export Extracted Indicators
Date: 2025-11-02
Purpose: Import 15 NEW indicators (2,083 Q&A pairs) from Droid's RAG export

This batch will COMPLETE multiple sessions:
- Session 2: 5/5 (100%) - adds SMA, WMA, MACD
- Session 4: 5/5 (100%) - adds Aroon, RSI
- Session 6: 5/5 (100%) - adds ATR, Ultimate Oscillator
- Session 7: 4/5 (80%) - adds Chaikin Vol, Historical Vol, Std Dev
- Session 8: 6/5 (120%) - adds CMF, MFI, VWAP, A/D Line, Vol ROC
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_NAME = "crypto_indicators_production.db"
PARSED_DATA_DIR = "parsed_qa_data"

# Mapping of 15 new indicators to sessions
NEW_INDICATORS_MAP = {
    # Session 2 - Trend Indicators (COMPLETES SESSION)
    "simple_moving_average_sma": {
        "session": 2,
        "name": "Simple Moving Average (SMA)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators"
    },
    "weighted_moving_average_wma": {
        "session": 2,
        "name": "Weighted Moving Average (WMA)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators"
    },
    "moving_average_convergence_divergence_macd": {
        "session": 2,
        "name": "Moving Average Convergence Divergence (MACD)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators"
    },

    # Session 4 - Momentum Indicators Part 1 (COMPLETES SESSION)
    "aroon_indicator": {
        "session": 4,
        "name": "Aroon Indicator",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },
    "relative_strength_index_rsi": {
        "session": 4,
        "name": "Relative Strength Index (RSI)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators"
    },

    # Session 6 - Volatility Indicators (COMPLETES SESSION)
    "average_true_range_atr": {
        "session": 6,
        "name": "Average True Range (ATR)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators"
    },
    "ultimate_oscillator": {
        "session": 6,
        "name": "Ultimate Oscillator",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators"
    },

    # Session 7 - Volume Indicators Part 1
    "chaikin_volatility": {
        "session": 7,
        "name": "Chaikin Volatility",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "historical_volatility": {
        "session": 7,
        "name": "Historical Volatility",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "standard_deviation": {
        "session": 7,
        "name": "Standard Deviation",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },

    # Session 8 - Volume Indicators Part 2
    "chaikin_money_flow_cmf": {
        "session": 8,
        "name": "Chaikin Money Flow (CMF)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "money_flow_index_mfi": {
        "session": 8,
        "name": "Money Flow Index (MFI)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "volume_weighted_average_price_vwap": {
        "session": 8,
        "name": "Volume Weighted Average Price (VWAP)",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "accumulationdistribution_line": {
        "session": 8,
        "name": "Accumulation/Distribution Line",
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators"
    },
    "volume_rate_of_change": {
        "session": 8,
        "name": "Volume Rate of Change",
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
        f"Extracted from RAG export on {data.get('generation_date', 'Unknown')}",
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

def update_session_status(cursor, session_num, total_indicators):
    """Update session status to 'complete' if all indicators present"""
    cursor.execute("""
        SELECT COUNT(*) FROM indicators WHERE session_number = ?
    """, (session_num,))

    count = cursor.fetchone()[0]

    if count >= total_indicators:
        cursor.execute("""
            UPDATE sessions SET status = 'complete' WHERE session_number = ?
        """, (session_num,))
        return True
    return False

def main():
    """Main import process"""

    print("=" * 70)
    print("BATCH 3 IMPORT - RAG Export Extracted Indicators")
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
        for slug, info in NEW_INDICATORS_MAP.items():
            if slug in filename:
                session_info = info
                break

        if not session_info:
            # Not one of the 15 new indicators, skip
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

    # Update session completion status
    print("\n" + "=" * 70)
    print("UPDATING SESSION STATUS")
    print("=" * 70)

    sessions_to_check = {
        2: 5,  # Session 2 should have 5 indicators
        4: 5,  # Session 4 should have 5 indicators
        6: 5,  # Session 6 should have 5 indicators
        7: 5,  # Session 7 should have 5 indicators
        8: 5   # Session 8 should have 5 indicators
    }

    for session_num, expected_count in sessions_to_check.items():
        completed = update_session_status(cursor, session_num, expected_count)
        if completed:
            print(f"  [OK] Session {session_num} marked as COMPLETE")

    # Commit all changes
    conn.commit()

    # Generate summary report
    print("\n" + "=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)

    # Count by session
    cursor.execute("""
        SELECT s.session_number, s.subcategory, s.status,
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
        session_num, subcategory, status, ind_count, qa_count = row
        status_icon = "[OK]" if status == 'complete' else "[ ]"
        print(f"  {status_icon} Session {session_num} ({subcategory}): {ind_count} indicators, {qa_count} Q&A - {status}")

    # Overall totals
    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_indicators = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa_db = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sessions WHERE status = 'complete'")
    complete_sessions = cursor.fetchone()[0]

    print(f"\nDatabase Totals:")
    print(f"  Total Indicators: {total_indicators}")
    print(f"  Total Q&A Pairs: {total_qa_db}")
    print(f"  Complete Sessions: {complete_sessions}")

    print(f"\nThis Import:")
    print(f"  Indicators Imported: {imported_count}")
    print(f"  Q&A Pairs Imported: {total_qa}")

    print("\n" + "=" * 70)
    print("[OK] Import complete!")
    print("=" * 70)

    conn.close()

if __name__ == "__main__":
    main()
