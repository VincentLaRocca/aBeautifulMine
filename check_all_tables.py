import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check indicators table (not crypto_indicators)
cursor.execute('SELECT COUNT(*) FROM indicators')
total_indicators = cursor.fetchone()[0]
print(f'Total indicators in "indicators" table: {total_indicators}')

if total_indicators > 0:
    cursor.execute('''
        SELECT session_number, COUNT(*) as indicator_count
        FROM indicators
        GROUP BY session_number
        ORDER BY session_number
    ''')
    print('\nIndicators by session (from "indicators" table):')
    for row in cursor.fetchall():
        if row[0]:
            print(f'  Session {row[0]}: {row[1]} indicators')
        else:
            print(f'  Session NULL: {row[1]} indicators')

# Check if there are Q&A pairs linked to the indicators table
cursor.execute('''
    SELECT COUNT(*)
    FROM qa_pairs
    WHERE indicator_id IN (SELECT id FROM indicators)
''')
pairs_from_indicators = cursor.fetchone()[0]
print(f'\nQ&A pairs linked to "indicators" table: {pairs_from_indicators}')

# Check sessions table
cursor.execute('SELECT COUNT(*) FROM sessions')
total_sessions = cursor.fetchone()[0]
print(f'\nTotal sessions in database: {total_sessions}')

if total_sessions > 0:
    cursor.execute('''
        SELECT session_number, status, indicators_count, qa_pairs_count
        FROM sessions
        ORDER BY session_number
    ''')
    print('\nSessions summary:')
    for row in cursor.fetchall():
        print(f'  Session {row[0]}: {row[1]} - {row[2]} indicators, {row[3]} Q&A pairs')

conn.close()
