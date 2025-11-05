import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check indicators table and their Q&A pairs
cursor.execute('''
    SELECT i.indicator_id, i.indicator_name, i.session_number, i.total_qa_pairs,
           COUNT(q.qa_id) as actual_qa_pairs
    FROM indicators i
    LEFT JOIN qa_pairs q ON i.indicator_id = q.indicator_id
    GROUP BY i.indicator_id, i.indicator_name, i.session_number, i.total_qa_pairs
    ORDER BY i.session_number, i.indicator_name
''')

print("Indicators and their Q&A pairs:")
print("="*80)
total_indicators_with_pairs = 0
total_all_pairs = 0

for row in cursor.fetchall():
    indicator_id, indicator_name, session, expected_pairs, actual_pairs = row
    if actual_pairs > 0:
        total_indicators_with_pairs += 1
        total_all_pairs += actual_pairs
        print(f"Session {session:2d} | {indicator_name:40s} | {actual_pairs:3d} pairs")
    else:
        print(f"Session {session:2d} | {indicator_name:40s} | NO PAIRS")

print("="*80)
print(f"Total indicators with Q&A pairs: {total_indicators_with_pairs}")
print(f"Total Q&A pairs in database: {total_all_pairs}")
print(f"Total indicators in database: {cursor.execute('SELECT COUNT(*) FROM indicators').fetchone()[0]}")

conn.close()
