#!/usr/bin/env python3
"""
Add UNIQUE constraint to qa_pairs table: (indicator_id, question)
This prevents duplicate questions for the same indicator.
"""

import sqlite3
import sys

def add_unique_constraint(db_path):
    """Add unique constraint to qa_pairs table"""

    print("="*70)
    print("ADDING UNIQUE CONSTRAINT TO QA_PAIRS TABLE")
    print("="*70)
    print(f"Database: {db_path}\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check current table structure
    print("Current qa_pairs table structure:")
    print("-"*70)
    cursor.execute("PRAGMA table_info(qa_pairs)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]}: {col[2]}")

    # Check for existing data
    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_qa = cursor.fetchone()[0]
    print(f"\nTotal Q&A pairs in table: {total_qa}")

    # Check if constraint already exists by examining schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='qa_pairs'")
    current_schema = cursor.fetchone()[0]

    if 'UNIQUE' in current_schema and 'indicator_id' in current_schema and 'question' in current_schema:
        print("\n[INFO] Unique constraint appears to already exist!")
        print("Current schema:")
        print(current_schema)
        conn.close()
        return True

    print("\n" + "="*70)
    print("IMPLEMENTING UNIQUE CONSTRAINT")
    print("="*70)

    # SQLite doesn't support ALTER TABLE ADD CONSTRAINT
    # We need to recreate the table with the constraint

    print("\nStep 1: Creating new table with unique constraint...")

    cursor.execute('''
        CREATE TABLE qa_pairs_new (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            question_order INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id),
            UNIQUE(indicator_id, question)
        )
    ''')

    print("[OK] New table created with unique constraint")

    print("\nStep 2: Copying data from old table to new table...")

    cursor.execute('''
        INSERT INTO qa_pairs_new (qa_id, indicator_id, question, answer, question_order, created_at)
        SELECT qa_id, indicator_id, question, answer, question_order, created_at
        FROM qa_pairs
    ''')

    rows_copied = cursor.rowcount
    print(f"[OK] Copied {rows_copied} rows")

    print("\nStep 3: Dropping old table...")
    cursor.execute('DROP TABLE qa_pairs')
    print("[OK] Old table dropped")

    print("\nStep 4: Renaming new table...")
    cursor.execute('ALTER TABLE qa_pairs_new RENAME TO qa_pairs')
    print("[OK] Table renamed")

    # Commit changes
    conn.commit()

    # Verify new structure
    print("\n" + "="*70)
    print("VERIFICATION")
    print("="*70)

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='qa_pairs'")
    new_schema = cursor.fetchone()[0]
    print("\nNew table schema:")
    print(new_schema)

    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    final_count = cursor.fetchone()[0]
    print(f"\nFinal Q&A count: {final_count}")

    if final_count == total_qa:
        print("[SUCCESS] All data preserved")
    else:
        print(f"[WARNING] Data count mismatch! Before: {total_qa}, After: {final_count}")

    conn.close()

    print("\n" + "="*70)
    print("[SUCCESS] UNIQUE CONSTRAINT ADDED")
    print("="*70)
    print("\nConstraint: UNIQUE(indicator_id, question)")
    print("Effect: Prevents duplicate questions for the same indicator")

    return True

def test_constraint(db_path):
    """Test the unique constraint by attempting to insert a duplicate"""

    print("\n" + "="*70)
    print("TESTING UNIQUE CONSTRAINT")
    print("="*70)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get a sample indicator_id and question
    cursor.execute('''
        SELECT indicator_id, question
        FROM qa_pairs
        LIMIT 1
    ''')
    result = cursor.fetchone()

    if not result:
        print("No data to test with")
        conn.close()
        return

    test_indicator_id, test_question = result

    print(f"\nAttempting to insert duplicate:")
    print(f"  Indicator ID: {test_indicator_id}")
    print(f"  Question: {test_question[:50]}...")

    try:
        cursor.execute('''
            INSERT INTO qa_pairs (indicator_id, question, answer, question_order)
            VALUES (?, ?, ?, ?)
        ''', (test_indicator_id, test_question, "Test answer", 999))

        print("\n[FAILED] Duplicate was inserted! Constraint not working!")
        conn.rollback()
        conn.close()
        return False

    except sqlite3.IntegrityError as e:
        print(f"\n[SUCCESS] Duplicate rejected as expected!")
        print(f"Error message: {e}")
        conn.rollback()
        conn.close()
        return True

def main():
    db_path = r'C:\Users\vlaro\dreamteam\Gemini\Database\crypto_indicators.db'

    if len(sys.argv) > 1:
        db_path = sys.argv[1]

    # Add constraint
    success = add_unique_constraint(db_path)

    if success:
        # Test constraint
        test_constraint(db_path)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
