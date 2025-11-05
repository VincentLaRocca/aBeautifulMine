#!/usr/bin/env python3
"""
Import Session 5 Q&A dataset into the crypto indicators database.
"""

import sqlite3
import json
import sys
from pathlib import Path

def import_session(db_path, json_file, session_number):
    """Import session data into the database"""

    # Read the JSON file
    print(f"Reading JSON file: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session_num = data.get('session', session_number)
    date = data.get('date', '2025-11-01')
    indicators = data['indicators']
    qa_pairs = data['qa_pairs']

    print(f"\nSession: {session_num}")
    print(f"Date: {date}")
    print(f"Indicators: {len(indicators)}")
    print(f"Q&A Pairs: {len(qa_pairs)}")

    # Connect to database
    print(f"\nConnecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if session already exists
    cursor.execute('SELECT COUNT(*) FROM sessions WHERE session_number = ?', (session_num,))
    if cursor.fetchone()[0] > 0:
        print(f"\n⚠️  Session {session_num} already exists in database!")
        response = input("Do you want to delete and re-import? (yes/no): ")
        if response.lower() != 'yes':
            print("Import cancelled.")
            conn.close()
            return False

        # Delete existing session data
        print(f"Deleting existing Session {session_num} data...")
        cursor.execute('DELETE FROM qa_pairs WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = ?)', (session_num,))
        cursor.execute('DELETE FROM indicators WHERE session_number = ?', (session_num,))
        cursor.execute('DELETE FROM sessions WHERE session_number = ?', (session_num,))
        conn.commit()

    # Determine category and subcategory
    if session_num <= 3:
        category = "Price-Based Technical Indicators"
        subcategory = "Trend Indicators"
    elif session_num == 4:
        category = "Price-Based Technical Indicators"
        subcategory = "Momentum Indicators"
    elif session_num == 5:
        category = "Price-Based Technical Indicators"
        subcategory = "Momentum & Volatility Indicators"
    elif session_num in [7, 8]:
        category = "Volume Indicators"
        subcategory = "Volume Analysis"
    else:
        category = "Technical Indicators"
        subcategory = "Mixed"

    # Insert session
    print(f"\nInserting session {session_num}...")
    cursor.execute('''
        INSERT INTO sessions (session_number, task, indicator_range, completed_timestamp,
                            research_depth, confidence_level, data_recency, session_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session_num, 'Cryptocurrency Technical Indicators Analysis',
          f"{(session_num-1)*5+1}-{session_num*5} of 227", date,
          "Comprehensive", "High", "2024-2025", "Completed"))
    session_id = cursor.lastrowid

    # Insert indicators and Q&A pairs
    print("Inserting indicators and Q&A pairs...")
    for indicator_name in indicators:
        # Insert indicator
        cursor.execute('''
            INSERT INTO indicators (indicator_name, session_number, category, subcategory)
            VALUES (?, ?, ?, ?)
        ''', (indicator_name, session_num, category, subcategory))
        indicator_id = cursor.lastrowid

        # Find all Q&A pairs for this indicator
        indicator_qa_pairs = [qa for qa in qa_pairs if qa['indicator'] == indicator_name]

        print(f"  - {indicator_name}: {len(indicator_qa_pairs)} Q&A pairs")

        # Insert Q&A pairs
        for j, qa in enumerate(indicator_qa_pairs):
            cursor.execute('''
                INSERT INTO qa_pairs (indicator_id, question, answer, question_order)
                VALUES (?, ?, ?, ?)
            ''', (indicator_id, qa['question'], qa['answer'], j + 1))

    # Commit changes
    conn.commit()

    # Verify import
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)

    cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = ?', (session_num,))
    imported_indicators = cursor.fetchone()[0]
    print(f"Indicators imported: {imported_indicators}/{len(indicators)}")

    cursor.execute('''
        SELECT COUNT(*) FROM qa_pairs
        WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = ?)
    ''', (session_num,))
    imported_qa_pairs = cursor.fetchone()[0]
    print(f"Q&A pairs imported: {imported_qa_pairs}/{len(qa_pairs)}")

    # Show database totals
    cursor.execute('SELECT COUNT(*) FROM sessions')
    total_sessions = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM indicators')
    total_indicators = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM qa_pairs')
    total_qa_pairs = cursor.fetchone()[0]

    print(f"\nDatabase totals:")
    print(f"  Total sessions: {total_sessions}")
    print(f"  Total indicators: {total_indicators}")
    print(f"  Total Q&A pairs: {total_qa_pairs}")

    conn.close()

    if imported_indicators == len(indicators) and imported_qa_pairs == len(qa_pairs):
        print("\n✅ Import successful!")
        return True
    else:
        print("\n❌ Import verification failed!")
        return False

def main():
    # Paths
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
    json_file = r'C:\Users\vlaro\dreamteam\Gemini\Outbox\claude\crypto-indicators-session-05-qa-FULL.json'
    session_number = 5

    # Check if custom paths provided
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]
    if len(sys.argv) > 3:
        session_number = int(sys.argv[3])

    # Verify files exist
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)

    if not Path(json_file).exists():
        print(f"❌ JSON file not found: {json_file}")
        sys.exit(1)

    # Import
    success = import_session(db_path, json_file, session_number)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
