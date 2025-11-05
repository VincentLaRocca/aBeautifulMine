import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "="*50)

# Check crypto_indicators table
cursor.execute('SELECT COUNT(*) FROM crypto_indicators')
total_indicators = cursor.fetchone()[0]
print(f'\nTotal indicators: {total_indicators}')

cursor.execute('''
    SELECT indicator_name, indicator_category, session_number
    FROM crypto_indicators
    ORDER BY session_number, indicator_name
''')
print('\nAll indicators:')
for row in cursor.fetchall():
    print(f'  Session {row[2]}: {row[0]} ({row[1]})')

print("\n" + "="*50)

# Check qa_pairs table
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
total_pairs = cursor.fetchone()[0]
print(f'\nTotal Q&A pairs: {total_pairs}')

cursor.execute('''
    SELECT indicator_name, COUNT(*) as pair_count
    FROM qa_pairs
    GROUP BY indicator_name
    ORDER BY indicator_name
''')
print('\nQ&A pairs by indicator:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]} pairs')

conn.close()
