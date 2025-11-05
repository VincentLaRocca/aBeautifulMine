import sqlite3
import os

databases = [
    ('Gemini', r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'),
    ('Droid', r'C:\Users\vlaro\dreamteam\Droid\Database\crypto_indicators.db'),
    ('Claude OLD', r'C:\Users\vlaro\dreamteam\claude\AgentOLD_DB_AND_DATA\crypto_indicators.db')
]

for name, db_path in databases:
    print(f'\n{"="*50}')
    print(f'{name} Database: {db_path}')
    print(f'{"="*50}')

    if not os.path.exists(db_path):
        print('Database file does not exist!')
        continue

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f'Tables: {[t[0] for t in tables]}')

        if not tables:
            print('No tables in database')
            conn.close()
            continue

        # Total counts
        try:
            cursor.execute('SELECT COUNT(*) FROM indicators')
            print(f'Total indicators: {cursor.fetchone()[0]}')
        except:
            print('No indicators table')

        try:
            cursor.execute('SELECT COUNT(*) FROM qa_pairs')
            print(f'Total Q&A pairs: {cursor.fetchone()[0]}')
        except:
            print('No qa_pairs table')

        try:
            cursor.execute('SELECT MAX(session_number) FROM sessions')
            latest = cursor.fetchone()[0]
            print(f'Latest session: {latest}')
        except:
            print('No sessions table')

        # Indicators by session
        try:
            cursor.execute('SELECT session_number, COUNT(*) FROM indicators GROUP BY session_number ORDER BY session_number')
            print('\nIndicators by session:')
            for row in cursor.fetchall():
                print(f'  Session {row[0]}: {row[1]} indicators')
        except:
            pass

        conn.close()
    except Exception as e:
        print(f'Error: {e}')
