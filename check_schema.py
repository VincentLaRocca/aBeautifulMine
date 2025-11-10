import sqlite3
from pathlib import Path

db_path = Path(r'C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("QA_PAIRS SCHEMA:")
print("=" * 60)
cursor.execute("PRAGMA table_info(qa_pairs)")
for row in cursor.fetchall():
    print(f"{row[1]:20} {row[2]:15} PK:{row[5]}")

print()
print("INDICATORS SCHEMA:")
print("=" * 60)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='indicators'")
if cursor.fetchone():
    cursor.execute("PRAGMA table_info(indicators)")
    for row in cursor.fetchall():
        print(f"{row[1]:20} {row[2]:15} PK:{row[5]}")
else:
    print("No indicators table exists")

conn.close()
