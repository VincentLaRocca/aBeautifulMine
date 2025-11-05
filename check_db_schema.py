import sqlite3

db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Database Schema:")
print("="*60)

for table_name in tables:
    table = table_name[0]
    print(f"\nTable: {table}")
    print("-"*60)

    # Get column information
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()

    for col in columns:
        col_id, name, col_type, not_null, default, pk = col
        pk_str = " [PRIMARY KEY]" if pk else ""
        not_null_str = " NOT NULL" if not_null else ""
        default_str = f" DEFAULT {default}" if default else ""
        print(f"  {name}: {col_type}{not_null_str}{default_str}{pk_str}")

conn.close()
