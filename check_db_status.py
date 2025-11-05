import sqlite3

conn = sqlite3.connect('AgentOLD_DB_AND_DATA/crypto_indicators.db')
cursor = conn.cursor()

# Total counts
cursor.execute('SELECT COUNT(*) FROM indicators')
print(f'Total indicators: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM qa_pairs')
print(f'Total Q&A pairs: {cursor.fetchone()[0]}')

# Indicators by session
cursor.execute('SELECT session_number, COUNT(*) FROM indicators GROUP BY session_number ORDER BY session_number')
print('\nIndicators by session:')
for row in cursor.fetchall():
    print(f'  Session {row[0]}: {row[1]} indicators')

# Latest session
cursor.execute('SELECT MAX(session_number) FROM sessions')
latest = cursor.fetchone()[0]
print(f'\nLatest session in sessions table: {latest}')

# Session 7 check
cursor.execute('SELECT COUNT(*) FROM indicators WHERE session_number = 7')
session_7_count = cursor.fetchone()[0]
print(f'\nSession 7 indicators: {session_7_count}')

conn.close()
