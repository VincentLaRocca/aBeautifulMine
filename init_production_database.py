#!/usr/bin/env python3
"""
Production Database Initialization
Created: 2025-11-02
Purpose: Fresh start with ultra_deep_research methodology

Expected: ~380 Q&A pairs per session (5 indicators × ~76 Q&A each)
"""

import sqlite3
from datetime import datetime

# Database name
DB_NAME = "crypto_indicators_production.db"

def create_production_database():
    """Create fresh production database with optimized schema"""

    print(f"Creating production database: {DB_NAME}")
    print("=" * 60)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table 1: Sessions
    print("\n[*] Creating sessions table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_number INTEGER UNIQUE NOT NULL,
            session_date TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            total_indicators INTEGER DEFAULT 5,
            total_qa_pairs INTEGER,
            executor TEXT,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)

    # Table 2: Indicators
    print("[*] Creating indicators table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator_name TEXT UNIQUE NOT NULL,
            indicator_slug TEXT UNIQUE NOT NULL,
            session_number INTEGER NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            description TEXT,
            total_qa_pairs INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_number) REFERENCES sessions(session_number)
        )
    """)

    # Table 3: Q&A Pairs
    print("[*] Creating qa_pairs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_pairs (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator_id INTEGER NOT NULL,
            pair_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            topic TEXT,
            created_date TEXT,
            FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id),
            UNIQUE(indicator_id, pair_number)
        )
    """)

    # Table 4: Research Metadata
    print("[*] Creating research_metadata table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_metadata (
            meta_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_number INTEGER NOT NULL,
            research_method TEXT DEFAULT 'ultra_deep_research',
            queries_executed INTEGER,
            success_rate REAL,
            generation_date TEXT,
            notes TEXT,
            FOREIGN KEY (session_number) REFERENCES sessions(session_number)
        )
    """)

    # Create indexes for performance
    print("\n[*] Creating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_qa_indicator ON qa_pairs(indicator_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicators_session ON indicators(session_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_indicators_category ON indicators(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status)")

    # Insert project metadata
    print("\n[*] Initializing project metadata...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_info (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    project_meta = [
        ('project_name', 'Crypto Indicators AI Training Dataset'),
        ('methodology', 'ultra_deep_research'),
        ('total_indicators', '227'),
        ('expected_sessions', '46'),
        ('qa_per_session_expected', '380'),
        ('qa_per_indicator_expected', '76'),
        ('created_date', datetime.now().isoformat()),
        ('status', 'production'),
        ('version', '2.0')
    ]

    cursor.executemany("INSERT OR REPLACE INTO project_info VALUES (?, ?)", project_meta)

    conn.commit()

    # Verify schema
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA VERIFICATION")
    print("=" * 60)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()

    print("\nTables created:")
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"\n  {table[0]}:")
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")

    # Summary
    print("\n" + "=" * 60)
    print("PRODUCTION DATABASE READY")
    print("=" * 60)
    print(f"\nDatabase: {DB_NAME}")
    print(f"Tables: {len(tables)}")
    print(f"Expected capacity: ~22,700 Q&A pairs (227 indicators × ~76 avg)")
    print(f"Expected sessions: ~46 (227 indicators ÷ 5 per session)")
    print("\nStatus: READY FOR SESSION 1 IMPORT")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    create_production_database()
