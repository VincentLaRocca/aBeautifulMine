import sqlite3

db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Session 8 Details:")
print("="*60)

# Get Session 8 indicators
cursor.execute('''
    SELECT indicator_name, category, subcategory
    FROM indicators
    WHERE session_number = 8
    ORDER BY indicator_id
''')

indicators = cursor.fetchall()
print(f"\nTotal indicators in Session 8: {len(indicators)}")
print("\nIndicator list:")
for i, (name, category, subcategory) in enumerate(indicators, 1):
    print(f"  {i}. {name}")
    print(f"     Category: {category}")
    print(f"     Subcategory: {subcategory}")

# Get Q&A count for Session 8
cursor.execute('''
    SELECT COUNT(*)
    FROM qa_pairs
    WHERE indicator_id IN (SELECT indicator_id FROM indicators WHERE session_number = 8)
''')
qa_count = cursor.fetchone()[0]
print(f"\nTotal Q&A pairs in Session 8: {qa_count}")

conn.close()
