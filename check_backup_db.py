import sqlite3
import os

db_path = r'C:\Users\vlaro\dreamteam\Gemini\Outbox\claude\crypto_indicators_backup.db'

if not os.path.exists(db_path):
    print(f"Database not found: {db_path}")
    exit(1)

print("BACKUP DATABASE ASSESSMENT")
print("="*60)
print(f"Database: {db_path}")
print(f"Size: {os.path.getsize(db_path) / 1024:.2f} KB")
print()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Basic statistics
cursor.execute("SELECT COUNT(*) FROM sessions")
total_sessions = cursor.fetchone()[0]
print(f"Total Sessions: {total_sessions}")

cursor.execute("SELECT COUNT(*) FROM indicators")
total_indicators = cursor.fetchone()[0]
print(f"Total Indicators: {total_indicators}")

cursor.execute("SELECT COUNT(*) FROM qa_pairs")
total_qa = cursor.fetchone()[0]
print(f"Total Q&A Pairs: {total_qa}")

# Session breakdown
print("\n" + "="*60)
print("SESSION BREAKDOWN")
print("="*60)

cursor.execute("""
    SELECT session_number, COUNT(*) as indicator_count
    FROM indicators
    GROUP BY session_number
    ORDER BY session_number
""")
sessions = cursor.fetchall()
for session_num, count in sessions:
    cursor.execute("""
        SELECT COUNT(*)
        FROM qa_pairs
        WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = ?)
    """, (session_num,))
    qa_count = cursor.fetchone()[0]
    print(f"Session {session_num}: {count} indicators, {qa_count} Q&A pairs")

# Check for duplicates
print("\n" + "="*60)
print("DUPLICATE CHECK")
print("="*60)

cursor.execute("""
    SELECT indicator_name, session_number, COUNT(*) as count
    FROM indicators
    GROUP BY indicator_name, session_number
    HAVING COUNT(*) > 1
""")
duplicates = cursor.fetchall()

if duplicates:
    print("WARNING: Duplicates found!")
    for ind_name, session_num, count in duplicates:
        print(f"  Session {session_num} - {ind_name}: {count} occurrences")
else:
    print("✓ No duplicates found - Database is CLEAN")

# Session 8 specific check
print("\n" + "="*60)
print("SESSION 8 SPECIFIC CHECK")
print("="*60)

cursor.execute("""
    SELECT indicator_name, COUNT(*) as occurrences
    FROM indicators
    WHERE session_number = 8
    GROUP BY indicator_name
    ORDER BY indicator_name
""")
session_8_indicators = cursor.fetchall()

if session_8_indicators:
    print(f"Session 8 has {len(session_8_indicators)} unique indicators:")
    for ind_name, count in session_8_indicators:
        cursor.execute("""
            SELECT COUNT(*)
            FROM qa_pairs
            WHERE indicator_id IN (
                SELECT indicator_id FROM indicators
                WHERE session_number = 8 AND indicator_name = ?
            )
        """, (ind_name,))
        qa_count = cursor.fetchone()[0]
        status = "DUPLICATE" if count > 1 else "OK"
        print(f"  - {ind_name}: {count} occurrence(s), {qa_count} Q&A pairs [{status}]")
else:
    print("Session 8 not found in backup database")

conn.close()

print("\n" + "="*60)
print("ASSESSMENT COMPLETE")
print("="*60)
