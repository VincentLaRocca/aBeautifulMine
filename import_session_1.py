#!/usr/bin/env python3
"""
Session 1 Import - Derivatives Indicators
Created: 2025-11-02
Purpose: Import Droid's ultra_deep_research output into production database

Session 1: Derivatives Indicators
- Futures Open Interest
- Funding Rates
- Options Analytics
- Liquidations/Positioning
- CME Institutionals
"""

import sqlite3
import json
from datetime import datetime
import os

# Database
DB_NAME = "crypto_indicators_production.db"

# Source files
SOURCE_FILES = [
    {
        "file": "inbox/droid/futures_open_interest_qa_pairs.json",
        "indicator_name": "Futures Open Interest",
        "indicator_slug": "futures_open_interest",
        "description": "Total number of outstanding futures contracts"
    },
    {
        "file": "inbox/droid/funding_rates_qa_pairs.json",
        "indicator_name": "Funding Rates",
        "indicator_slug": "funding_rates",
        "description": "Periodic payments between long and short perpetual futures holders"
    },
    {
        "file": "inbox/droid/options_analytics_qa_pairs.json",
        "indicator_name": "Options Analytics",
        "indicator_slug": "options_analytics",
        "description": "Options market metrics including put/call ratios and volatility"
    },
    {
        "file": "inbox/droid/liquidations_positioning_qa_pairs.json",
        "indicator_name": "Liquidations & Positioning",
        "indicator_slug": "liquidations_positioning",
        "description": "Forced liquidation events and trader positioning metrics"
    },
    {
        "file": "inbox/droid/cme_institutionals_qa_pairs.json",
        "indicator_name": "CME Institutional Positioning",
        "indicator_slug": "cme_institutionals",
        "description": "CME futures positioning data from institutional traders"
    }
]

def import_session_1():
    """Import Session 1 data into production database"""

    print("=" * 70)
    print("SESSION 1 IMPORT - DERIVATIVES INDICATORS")
    print("=" * 70)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create Session 1
    print("\n[1] Creating Session 1 record...")
    session_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO sessions (session_number, session_date, category, subcategory,
                             total_indicators, executor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (1, session_date, "Derivatives Indicators", "Market Structure", 5, "Droid", "importing"))

    session_id = cursor.lastrowid
    print(f"    Session ID: {session_id}")

    total_qa_imported = 0
    indicators_imported = 0

    # Import each indicator
    for idx, source in enumerate(SOURCE_FILES, 1):
        print(f"\n[{idx+1}] Processing: {source['indicator_name']}")
        print(f"    File: {source['file']}")

        # Check file exists
        if not os.path.exists(source['file']):
            print(f"    ERROR: File not found!")
            continue

        # Load JSON
        with open(source['file'], 'r', encoding='utf-8') as f:
            data = json.load(f)

        qa_pairs = data.get('qa_pairs', [])
        queries_executed = data.get('queries_executed', 100)
        success_rate = data.get('success_rate', '0%').replace('%', '')

        print(f"    Q&A pairs in file: {len(qa_pairs)}")
        print(f"    Queries executed: {queries_executed}")
        print(f"    Success rate: {success_rate}%")

        # Insert indicator
        cursor.execute("""
            INSERT INTO indicators (indicator_name, indicator_slug, session_number,
                                   category, subcategory, description, total_qa_pairs)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (source['indicator_name'], source['indicator_slug'], 1,
              "Derivatives", "Market Structure", source['description'], len(qa_pairs)))

        indicator_id = cursor.lastrowid
        print(f"    Indicator ID: {indicator_id}")

        # Insert Q&A pairs
        qa_imported = 0
        for qa in qa_pairs:
            try:
                cursor.execute("""
                    INSERT INTO qa_pairs (indicator_id, pair_number, question, answer, topic, created_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    indicator_id,
                    qa.get('pair_number', 0),
                    qa.get('question', '').strip('"'),
                    qa.get('answer', ''),
                    qa.get('topic', ''),
                    qa.get('created_date', session_date)
                ))
                qa_imported += 1
            except sqlite3.IntegrityError as e:
                print(f"    Warning: Skipped duplicate Q&A pair {qa.get('pair_number')}")
            except Exception as e:
                print(f"    Error importing Q&A pair {qa.get('pair_number')}: {e}")

        print(f"    Imported: {qa_imported} Q&A pairs")
        total_qa_imported += qa_imported
        indicators_imported += 1

        # Insert research metadata
        try:
            success_rate_float = float(success_rate)
        except:
            success_rate_float = 0.0

        cursor.execute("""
            INSERT INTO research_metadata (session_number, research_method, queries_executed,
                                          success_rate, generation_date)
            VALUES (?, ?, ?, ?, ?)
        """, (1, 'ultra_deep_research', queries_executed, success_rate_float, session_date))

    # Update session with totals
    print(f"\n[7] Updating session totals...")
    cursor.execute("""
        UPDATE sessions
        SET total_qa_pairs = ?, status = 'completed', completed_at = ?
        WHERE session_number = 1
    """, (total_qa_imported, datetime.now().isoformat()))

    conn.commit()

    # Verification
    print("\n" + "=" * 70)
    print("IMPORT VERIFICATION")
    print("=" * 70)

    cursor.execute("SELECT COUNT(*) FROM indicators WHERE session_number = 1")
    ind_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM qa_pairs WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = 1)")
    qa_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT indicator_name, total_qa_pairs
        FROM indicators
        WHERE session_number = 1
        ORDER BY indicator_id
    """)

    print("\nSession 1 Contents:")
    print(f"  Indicators: {ind_count}/5")
    print(f"  Total Q&A pairs: {qa_count}")
    print("\nPer Indicator:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]} Q&A pairs")

    # Database totals
    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_indicators = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa = cursor.fetchone()[0]

    print("\n" + "=" * 70)
    print("DATABASE TOTALS")
    print("=" * 70)
    print(f"Total Sessions: {total_sessions}")
    print(f"Total Indicators: {total_indicators}")
    print(f"Total Q&A Pairs: {total_qa}")
    print(f"\nProgress: {total_indicators}/227 indicators ({total_indicators/227*100:.1f}%)")
    print(f"Remaining: {227 - total_indicators} indicators")
    print(f"Remaining Sessions: ~{(227 - total_indicators) // 5}")

    print("\n" + "=" * 70)
    print("SESSION 1 IMPORT COMPLETE")
    print("=" * 70)

    conn.close()

if __name__ == "__main__":
    import_session_1()
