import sqlite3

db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("SESSION 9 IN DATABASE")
print("="*60)

# Get Session 9 indicators
cursor.execute('''
    SELECT indicator_name
    FROM indicators
    WHERE session_number = 9
    ORDER BY indicator_id
''')
indicators = cursor.fetchall()

print(f"\nTotal indicators: {len(indicators)}")
print("\nIndicators:")
for i, (name,) in enumerate(indicators, 1):
    # Get Q&A count for this indicator
    cursor.execute('''
        SELECT COUNT(*)
        FROM qa_pairs
        WHERE indicator_id IN (
            SELECT indicator_id FROM indicators
            WHERE session_number = 9 AND indicator_name = ?
        )
    ''', (name,))
    qa_count = cursor.fetchone()[0]
    print(f"  {i}. {name}: {qa_count} Q&A pairs")

# Get total Q&A for Session 9
cursor.execute('''
    SELECT COUNT(*)
    FROM qa_pairs
    WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = 9)
''')
total_qa = cursor.fetchone()[0]
print(f"\nTotal Q&A pairs in Session 9: {total_qa}")

conn.close()
