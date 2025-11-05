import sqlite3

db_path = r'C:\Users\vlaro\dreamteam\Gemini\Outbox\claude\crypto_indicators_backup.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("SESSION 7 DETAILED CHECK")
print("="*60)

cursor.execute("""
    SELECT indicator_name, COUNT(*) as occurrences
    FROM indicators
    WHERE session_number = 7
    GROUP BY indicator_name
    ORDER BY indicator_name
""")
session_7_indicators = cursor.fetchall()

print(f"Session 7 has {len(session_7_indicators)} indicators:\n")
for ind_name, count in session_7_indicators:
    cursor.execute("""
        SELECT COUNT(*)
        FROM qa_pairs
        WHERE indicator_id IN (
            SELECT indicator_id FROM indicators
            WHERE session_number = 7 AND indicator_name = ?
        )
    """, (ind_name,))
    qa_count = cursor.fetchone()[0]
    status = "DUPLICATE" if count > 1 else "OK"
    print(f"  - {ind_name}")
    print(f"    Occurrences: {count} [{status}]")
    print(f"    Q&A Pairs: {qa_count}")
    print()

# Total for Session 7
cursor.execute("""
    SELECT COUNT(*)
    FROM qa_pairs
    WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = 7)
""")
total_qa = cursor.fetchone()[0]
print(f"Total Q&A pairs in Session 7: {total_qa}")
print(f"Expected: 30 (5 indicators × 6 questions)")
print(f"Difference: {total_qa - 30}")

conn.close()
