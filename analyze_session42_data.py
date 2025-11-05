import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

print("="*80)
print("SESSION 42 DATA ANALYSIS")
print("="*80)

# Check for duplicate Q&A pairs
print("\n1. Checking for duplicate pair_numbers per indicator:")
cursor.execute('''
    SELECT indicator_id, pair_number, COUNT(*) as cnt
    FROM qa_pairs
    WHERE indicator_id IN (SELECT id FROM crypto_indicators WHERE session_number = 42)
    GROUP BY indicator_id, pair_number
    HAVING cnt > 1
    ORDER BY indicator_id, pair_number
    LIMIT 20
''')

duplicates = cursor.fetchall()
if duplicates:
    print(f"  Found {len(duplicates)} duplicate pair_numbers:")
    for row in duplicates[:10]:
        print(f"    Indicator {row[0]}, Pair {row[1]}: {row[2]} copies")
else:
    print("  No duplicate pair_numbers found")

# Check pair_number distribution
print("\n2. Pair number ranges by indicator:")
cursor.execute('''
    SELECT i.indicator_name, MIN(q.pair_number), MAX(q.pair_number), COUNT(DISTINCT q.pair_number), COUNT(*)
    FROM crypto_indicators i
    JOIN qa_pairs q ON i.id = q.indicator_id
    WHERE i.session_number = 42
    GROUP BY i.id
''')

for row in cursor.fetchall():
    print(f"  {row[0]}:")
    print(f"    Range: {row[1]} - {row[2]}")
    print(f"    Unique pair_numbers: {row[3]}")
    print(f"    Total rows: {row[4]}")

# Sample some data
print("\n3. Sample Q&A pairs from Floor Price (ID=2):")
cursor.execute('''
    SELECT pair_number, question, LENGTH(answer) as ans_len
    FROM qa_pairs
    WHERE indicator_id = 2
    ORDER BY pair_number
    LIMIT 5
''')

for row in cursor.fetchall():
    print(f"  Pair {row[0]}: {row[1][:60]}... ({row[2]} chars)")

# Check if there's data without pair_number
print("\n4. Checking for NULL pair_numbers:")
cursor.execute('''
    SELECT COUNT(*)
    FROM qa_pairs
    WHERE indicator_id IN (SELECT id FROM crypto_indicators WHERE session_number = 42)
    AND pair_number IS NULL
''')
print(f"  Rows with NULL pair_number: {cursor.fetchone()[0]}")

conn.close()
