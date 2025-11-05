import sqlite3

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Get schema for indicators table
cursor.execute("PRAGMA table_info(indicators)")
print("Schema for 'indicators' table:")
for row in cursor.fetchall():
    print(f"  {row[1]} ({row[2]})")

print("\n" + "="*50 + "\n")

# Get schema for crypto_indicators table
cursor.execute("PRAGMA table_info(crypto_indicators)")
print("Schema for 'crypto_indicators' table:")
for row in cursor.fetchall():
    print(f"  {row[1]} ({row[2]})")

print("\n" + "="*50 + "\n")

# Get schema for qa_pairs table
cursor.execute("PRAGMA table_info(qa_pairs)")
print("Schema for 'qa_pairs' table:")
for row in cursor.fetchall():
    print(f"  {row[1]} ({row[2]})")

print("\n" + "="*50 + "\n")

# Count Q&A pairs linked to each table
cursor.execute('''
    SELECT COUNT(DISTINCT indicator_name) as unique_indicators, COUNT(*) as total_pairs
    FROM qa_pairs
''')
result = cursor.fetchone()
print(f"Q&A pairs table summary:")
print(f"  Unique indicators: {result[0]}")
print(f"  Total pairs: {result[1]}")

# Check which indicators have Q&A pairs
cursor.execute('''
    SELECT DISTINCT indicator_name
    FROM qa_pairs
    ORDER BY indicator_name
''')
print("\nIndicators with Q&A pairs:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

conn.close()
