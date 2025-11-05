#!/usr/bin/env python3
"""
Clean up duplicate Session 7 & 8 data from the database.
"""

import sqlite3
import sys

def cleanup_database(db_path):
    """Remove all Session 7 and 8 data"""

    print("="*60)
    print("DATABASE CLEANUP: Removing Sessions 7 & 8")
    print("="*60)
    print(f"Database: {db_path}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check current state
    print("BEFORE CLEANUP:")
    print("-"*60)

    for session_num in [7, 8]:
        cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = ?', (session_num,))
        indicator_count = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) FROM qa_pairs
            WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = ?)
        ''', (session_num,))
        qa_count = cursor.fetchone()[0]

        print(f"Session {session_num}: {indicator_count} indicators, {qa_count} Q&A pairs")

    cursor.execute('SELECT COUNT(*) FROM indicators')
    total_indicators_before = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM qa_pairs')
    total_qa_before = cursor.fetchone()[0]

    print(f"\nTotal before: {total_indicators_before} indicators, {total_qa_before} Q&A pairs")

    # Confirm deletion
    print("\n" + "="*60)
    response = input("Proceed with deletion? (yes/no): ")
    if response.lower() != 'yes':
        print("Cleanup cancelled.")
        conn.close()
        return False

    # Delete Session 7 and 8 data
    print("\nDeleting Session 7 & 8 data...")

    # Delete Q&A pairs first (foreign key constraint)
    cursor.execute('''
        DELETE FROM qa_pairs
        WHERE indicator_id IN (
            SELECT indicator_id FROM indicators WHERE session_number IN (7, 8)
        )
    ''')
    qa_deleted = cursor.rowcount
    print(f"  - Deleted {qa_deleted} Q&A pairs")

    # Delete indicators
    cursor.execute('DELETE FROM indicators WHERE session_number IN (7, 8)')
    indicators_deleted = cursor.rowcount
    print(f"  - Deleted {indicators_deleted} indicators")

    # Delete session metadata
    cursor.execute('DELETE FROM sessions WHERE session_number IN (7, 8)')
    sessions_deleted = cursor.rowcount
    print(f"  - Deleted {sessions_deleted} session records")

    # Commit changes
    conn.commit()

    # Verify deletion
    print("\n" + "="*60)
    print("AFTER CLEANUP:")
    print("-"*60)

    for session_num in [7, 8]:
        cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = ?', (session_num,))
        indicator_count = cursor.fetchone()[0]
        print(f"Session {session_num}: {indicator_count} indicators (should be 0)")

    cursor.execute('SELECT COUNT(*) FROM indicators')
    total_indicators_after = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM qa_pairs')
    total_qa_after = cursor.fetchone()[0]

    print(f"\nTotal after: {total_indicators_after} indicators, {total_qa_after} Q&A pairs")
    print(f"Removed: {total_indicators_before - total_indicators_after} indicators, {total_qa_before - total_qa_after} Q&A pairs")

    conn.close()

    print("\n" + "="*60)
    print("✓ CLEANUP COMPLETE")
    print("="*60)

    return True

def main():
    # Main database path
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'

    if len(sys.argv) > 1:
        db_path = sys.argv[1]

    success = cleanup_database(db_path)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
