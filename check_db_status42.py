import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

print("="*80)
print("DATABASE STATUS CHECK")
print("="*80)

# Check indicators
cursor.execute('SELECT id, indicator_name, session_number FROM crypto_indicators ORDER BY id')
indicators = cursor.fetchall()
print(f"\nTotal indicators: {len(indicators)}")
print("\nExisting indicators:")
for row in indicators:
    print(f"  ID {row[0]}: {row[1]} (Session {row[2]})")

# Check by session
cursor.execute('SELECT session_number, COUNT(*) FROM crypto_indicators GROUP BY session_number ORDER BY session_number')
print("\nIndicators by session:")
for row in cursor.fetchall():
    print(f"  Session {row[0]}: {row[1]} indicators")

# Check Q&A pairs
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
print(f"\nTotal Q&A pairs: {cursor.fetchone()[0]}")

# Check Session 42 specifically
cursor.execute('''
    SELECT i.id, i.indicator_name, COUNT(q.qa_id)
    FROM crypto_indicators i
    LEFT JOIN qa_pairs q ON i.id = q.indicator_id
    WHERE i.session_number = 42
    GROUP BY i.id
''')
session42 = cursor.fetchall()
if session42:
    print("\nSession 42 indicators and Q&A counts:")
    for row in session42:
        print(f"  ID {row[0]}: {row[1]} - {row[2]} Q&A pairs")
else:
    print("\nSession 42: NOT FOUND in database")

conn.close()
