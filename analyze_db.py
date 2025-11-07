import sqlite3
conn = sqlite3.connect('crypto_indicators_production.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM qa_pairs')
total = cur.fetchone()[0]
cur.execute('SELECT source, COUNT(*) FROM qa_pairs GROUP BY source')
sources = cur.fetchall()
print(f'Total: {total:,} pairs\n')
print('By Source:')
for src, cnt in sources:
    print(f'  {src}: {cnt:,}')
conn.close()
