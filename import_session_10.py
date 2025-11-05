#!/usr/bin/env python3
"""
Import Session 10 Q&A dataset into the crypto indicators database.
"""

import sqlite3
import json
import sys
from pathlib import Path

def import_session_10(db_path, json_file):
    """Import Session 10 data into the database"""

    # Read the JSON file
    print(f"Reading JSON file: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session_number = data['session']
    date = data['date']
    category = data['category']
    indicators = data['indicators']
    qa_pairs = data['qa_pairs']

    print(f"\nSession: {session_number}")
    print(f"Date: {date}")
    print(f"Category: {category}")
    print(f"Indicators: {len(indicators)}")
    print(f"Q&A Pairs: {len(qa_pairs)}")

    # Connect to database
    print(f"\nConnecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if session already exists
    cursor.execute('SELECT COUNT(*) FROM sessions WHERE session_number = ?', (session_number,))
    if cursor.fetchone()[0] > 0:
        print(f"\n⚠️  Session {session_number} already exists in database!")
        response = input("Do you want to delete and re-import? (yes/no): ")
        if response.lower() != 'yes':
            print("Import cancelled.")
            conn.close()
            return

        # Delete existing session data
        print(f"Deleting existing Session {session_number} data...")
        cursor.execute('DELETE FROM qa_pairs WHERE indicator_id IN (SELECT id FROM indicators WHERE session_number = ?)', (session_number,))
        cursor.execute('DELETE FROM indicators WHERE session_number = ?', (session_number,))
        cursor.execute('DELETE FROM sessions WHERE session_number = ?', (session_number,))
        conn.commit()

    # Insert session
    print(f"\nInserting session {session_number}...")
    cursor.execute('''
        INSERT INTO sessions (session_number, task, indicator_range, completed_timestamp,
                            research_depth, confidence_level, data_recency, session_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session_number, category, f"{len(indicators)} indicators", date,
          "Comprehensive", "High", "2024-2025", "Completed"))
    session_id = cursor.lastrowid

    # Insert indicators and Q&A pairs
    print("Inserting indicators and Q&A pairs...")
    for i, indicator_name in enumerate(indicators):
        # Insert indicator
        cursor.execute('''
            INSERT INTO indicators (indicator_name, session_number, category, subcategory)
            VALUES (?, ?, ?, ?)
        ''', (indicator_name, session_number, "On-Chain Indicators", "Network Activity Metrics"))
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

    cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = ?', (session_number,))
    imported_indicators = cursor.fetchone()[0]
    print(f"Indicators imported: {imported_indicators}/{len(indicators)}")

    cursor.execute('''
        SELECT COUNT(*) FROM qa_pairs
        WHERE indicator_id IN (SELECT id FROM indicators WHERE session_number = ?)
    ''', (session_number,))
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
    # Default paths
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
    json_file = 'session_10_transaction_metrics_qa_dataset.json'

    # Check if custom paths provided
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]

    # Verify files exist
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)

    if not Path(json_file).exists():
        print(f"❌ JSON file not found: {json_file}")
        sys.exit(1)

    # Import
    success = import_session_10(db_path, json_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
