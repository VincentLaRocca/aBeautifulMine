#!/usr/bin/env python3
"""
Initialize the crypto_indicators_qa.db database with proper schema.
Based on structure from import_session_generic.py
"""

import sqlite3
from pathlib import Path

def init_database(db_path):
    """Initialize database with required tables"""

    print(f"Initializing database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_number INTEGER UNIQUE NOT NULL,
            task TEXT,
            indicator_range TEXT,
            completed_timestamp TEXT,
            research_depth TEXT,
            confidence_level TEXT,
            data_recency TEXT,
            session_status TEXT
        )
    ''')

    # Create indicators table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indicators (
            indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator_name TEXT NOT NULL,
            session_number INTEGER NOT NULL,
            category TEXT,
            subcategory TEXT,
            FOREIGN KEY (session_number) REFERENCES sessions (session_number)
        )
    ''')

    # Create qa_pairs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            question_order INTEGER,
            FOREIGN KEY (indicator_id) REFERENCES indicators (indicator_id)
        )
    ''')

    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_number ON indicators(session_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_indicator_id ON qa_pairs(indicator_id)')

    conn.commit()

    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("\nDatabase initialized successfully!")
    print(f"Tables created: {[t[0] for t in tables]}")

    conn.close()

    return True

if __name__ == '__main__':
    db_path = r'C:\Users\vlaro\dreamteam\claude\crypto_indicators_qa.db'
    init_database(db_path)
