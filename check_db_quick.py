import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Total Q&A pairs
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
total = cursor.fetchone()[0]
print(f'Total Q&A pairs in production: {total}')

# Pairs by session
cursor.execute('''
    SELECT session_number, COUNT(*)
    FROM crypto_indicators
    GROUP BY session_number
    ORDER BY session_number
''')
print('\nIndicators by session:')
for row in cursor.fetchall():
    print(f'  Session {row[0]}: {row[1]} indicators')

# Total indicators
cursor.execute('SELECT COUNT(*) FROM crypto_indicators')
total_indicators = cursor.fetchone()[0]
print(f'\nTotal indicators: {total_indicators}')

conn.close()
