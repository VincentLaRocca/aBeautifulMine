#!/usr/bin/env python3
"""
Clean up duplicate Session 9 data from the database.
"""

import sqlite3

def cleanup_session_9(db_path):
    """Remove all Session 9 data"""

    print("="*60)
    print("DATABASE CLEANUP: Removing Session 9")
    print("="*60)
    print(f"Database: {db_path}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check current state
    print("BEFORE CLEANUP:")
    print("-"*60)

    cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = 9')
    indicator_count = cursor.fetchone()[0]

    cursor.execute('''
        SELECT COUNT(*) FROM qa_pairs
        WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = 9)
    ''')
    qa_count = cursor.fetchone()[0]

    print(f"Session 9: {indicator_count} indicators, {qa_count} Q&A pairs")
    print(f"Expected: 5 indicators, 30 Q&A pairs")
    print(f"Issue: Duplicated (imported twice)")

    # Delete Session 9 data
    print("\nDeleting Session 9 data...")

    # Delete Q&A pairs first (foreign key constraint)
    cursor.execute('''
        DELETE FROM qa_pairs
        WHERE indicator_id IN (
            SELECT indicator_id FROM indicators WHERE session_number = 9
        )
    ''')
    qa_deleted = cursor.rowcount
    print(f"  - Deleted {qa_deleted} Q&A pairs")

    # Delete indicators
    cursor.execute('DELETE FROM indicators WHERE session_number = 9')
    indicators_deleted = cursor.rowcount
    print(f"  - Deleted {indicators_deleted} indicators")

    # Delete session metadata
    cursor.execute('DELETE FROM sessions WHERE session_number = 9')
    sessions_deleted = cursor.rowcount
    print(f"  - Deleted {sessions_deleted} session records")

    # Commit changes
    conn.commit()

    # Verify deletion
    print("\n" + "="*60)
    print("AFTER CLEANUP:")
    print("-"*60)

    cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = 9')
    indicator_count = cursor.fetchone()[0]
    print(f"Session 9: {indicator_count} indicators (should be 0)")

    conn.close()

    print("\n[SUCCESS] CLEANUP COMPLETE")
    return True

def main():
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
    cleanup_session_9(db_path)

if __name__ == '__main__':
    main()
