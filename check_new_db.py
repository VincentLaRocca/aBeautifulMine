import sqlite3
db_path = r"C:\Users\vlaro\dreamteam\Droid\Database\crypto_indicators.db"
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessions")
    sessions = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM indicators")
    indicators = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    qa_pairs = cursor.fetchone()[0]
    cursor.execute("SELECT session_number, COUNT(*) FROM indicators GROUP BY session_number")
    session_breakdown = cursor.fetchall()
    
    print(f"=== NEW DREAMTEAM DATABASE ===")
    print(f"Sessions: {sessions}")
    print(f"Indicators: {indicators}")
    print(f"Q&A Pairs: {qa_pairs}")
    print(f"\nSession Breakdown:")
    for session_num, count in session_breakdown:
        print(f"  Session {session_num}: {count} indicators")
