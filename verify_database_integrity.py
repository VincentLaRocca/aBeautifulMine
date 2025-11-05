#!/usr/bin/env python3
"""
Comprehensive database integrity verification.
"""

import sqlite3

def verify_database(db_path):
    """Run comprehensive integrity checks"""

    print("="*70)
    print("DATABASE INTEGRITY VERIFICATION")
    print("="*70)
    print(f"Database: {db_path}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Overall statistics
    print("OVERALL STATISTICS")
    print("-"*70)

    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]
    print(f"Total Sessions: {total_sessions}")

    cursor.execute("SELECT COUNT(*) FROM indicators")
    total_indicators = cursor.fetchone()[0]
    print(f"Total Indicators: {total_indicators}")

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa = cursor.fetchone()[0]
    print(f"Total Q&A Pairs: {total_qa}")

    # Session-by-session breakdown
    print("\n" + "="*70)
    print("SESSION BREAKDOWN")
    print("="*70)

    cursor.execute("""
        SELECT session_number, COUNT(*) as indicator_count
        FROM indicators
        GROUP BY session_number
        ORDER BY session_number
    """)
    sessions = cursor.fetchall()

    all_correct = True
    for session_num, indicator_count in sessions:
        cursor.execute("""
            SELECT COUNT(*)
            FROM qa_pairs
            WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = ?)
        """, (session_num,))
        qa_count = cursor.fetchone()[0]

        expected_indicators = 5
        expected_qa = 30

        indicator_status = "OK" if indicator_count == expected_indicators else "ERROR"
        qa_status = "OK" if qa_count == expected_qa else "ERROR"

        if indicator_status != "OK" or qa_status != "OK":
            all_correct = False

        print(f"Session {session_num}:")
        print(f"  Indicators: {indicator_count}/5 [{indicator_status}]")
        print(f"  Q&A Pairs:  {qa_count}/30 [{qa_status}]")

    # Check for duplicates
    print("\n" + "="*70)
    print("DUPLICATE CHECK")
    print("="*70)

    cursor.execute("""
        SELECT indicator_name, session_number, COUNT(*) as count
        FROM indicators
        GROUP BY indicator_name, session_number
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()

    if duplicates:
        print("WARNING: Duplicates found!")
        all_correct = False
        for ind_name, session_num, count in duplicates:
            print(f"  Session {session_num} - {ind_name}: {count} occurrences")
    else:
        print("[OK] No duplicates found")

    # Check Q&A distribution
    print("\n" + "="*70)
    print("Q&A PAIR DISTRIBUTION")
    print("="*70)

    cursor.execute("""
        SELECT i.session_number, i.indicator_name, COUNT(q.qa_id) as qa_count
        FROM indicators i
        LEFT JOIN qa_pairs q ON i.indicator_id = q.indicator_id
        GROUP BY i.indicator_id
        HAVING qa_count != 6
        ORDER BY i.session_number, i.indicator_name
    """)
    irregular_qa = cursor.fetchall()

    if irregular_qa:
        print("WARNING: Irregular Q&A counts found!")
        all_correct = False
        for session_num, ind_name, qa_count in irregular_qa:
            print(f"  Session {session_num} - {ind_name}: {qa_count} Q&A pairs (expected 6)")
    else:
        print("[OK] All indicators have exactly 6 Q&A pairs")

    # Final verdict
    print("\n" + "="*70)
    print("FINAL VERDICT")
    print("="*70)

    if all_correct and not duplicates and not irregular_qa:
        print("[SUCCESS] Database integrity verified - ALL CHECKS PASSED")
        verdict = True
    else:
        print("[WARNING] Database has integrity issues - SEE DETAILS ABOVE")
        verdict = False

    conn.close()
    return verdict

def main():
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
    verify_database(db_path)

if __name__ == '__main__':
    main()
