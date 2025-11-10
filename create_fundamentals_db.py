#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create crypto_fundamentals_production.db and integrate DLT Q&A pairs
"""

import sqlite3
import json
import sys
from datetime import datetime

# Ensure proper encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def create_fundamentals_database():
    """Create the crypto fundamentals database with appropriate schema"""

    conn = sqlite3.connect('crypto_fundamentals_production.db')
    cursor = conn.cursor()

    print("Creating crypto_fundamentals_production.db...\n")

    # Create sessions table (adapted for fundamentals)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_number INTEGER UNIQUE NOT NULL,
            session_date TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            total_topics INTEGER DEFAULT 1,
            total_qa_pairs INTEGER,
            executor TEXT,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    print("✓ Created sessions table")

    # Create topics table (equivalent to indicators, but for concepts/projects)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT UNIQUE NOT NULL,
            topic_slug TEXT UNIQUE NOT NULL,
            session_number INTEGER NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            description TEXT,
            total_qa_pairs INTEGER,
            priority TEXT DEFAULT 'medium',
            topic_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_number) REFERENCES sessions(session_number)
        )
    ''')
    print("✓ Created topics table")

    # Create qa_pairs table (adapted for fundamentals)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            pair_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            subtopic TEXT,
            created_date TEXT,
            topic_name TEXT,
            difficulty_level TEXT,
            tags TEXT,
            answer_length INTEGER,
            has_examples BOOLEAN DEFAULT 0,
            has_sources BOOLEAN DEFAULT 0,
            crypto_specific BOOLEAN DEFAULT 1,
            technology_focus BOOLEAN DEFAULT 1,
            FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
            UNIQUE(topic_id, pair_number)
        )
    ''')
    print("✓ Created qa_pairs table")

    # Create metadata tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_info (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created project_info table")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batch_metadata (
            batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_name TEXT NOT NULL,
            category TEXT,
            subcategory TEXT,
            total_topics INTEGER,
            total_qa_pairs INTEGER,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            integrated_at TIMESTAMP
        )
    ''')
    print("✓ Created batch_metadata table")

    # Insert project info
    cursor.execute('''
        INSERT INTO project_info (key, value) VALUES
        ('database_name', 'Cryptocurrency Fundamentals Knowledge Base'),
        ('database_type', 'fundamentals'),
        ('created_date', ?),
        ('version', '1.0.0'),
        ('purpose', 'AI Agent training dataset for blockchain technology and cryptocurrency fundamentals')
    ''', (datetime.now().isoformat(),))
    print("✓ Inserted project info")

    conn.commit()
    print("\n✅ Database schema created successfully!")
    return conn, cursor

def integrate_dlt_data(cursor, conn):
    """Integrate DLT Q&A pairs from the JSON file"""

    print("\n" + "="*60)
    print("INTEGRATING DLT DATA")
    print("="*60 + "\n")

    # Load DLT JSON
    with open(r'inbox\cursor\dlt_questions_answers.json', 'r', encoding='utf-8') as f:
        dlt_data = json.load(f)

    print(f"Loaded DLT data: {dlt_data['total_questions']} Q&A pairs")

    # Create session for DLT
    session_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO sessions (
            session_number, session_date, category, subcategory,
            total_topics, total_qa_pairs, executor, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        1,  # First session
        session_date,
        dlt_data['category'],
        dlt_data['subcategory'],
        1,  # 1 topic (DLT)
        dlt_data['total_questions'],
        'Cursor AI',
        'completed',
        'First fundamentals batch - Distributed Ledger Technology basics'
    ))
    print(f"✓ Created Session 1: {dlt_data['category']} - {dlt_data['subcategory']}")

    # Create topic for DLT
    cursor.execute('''
        INSERT INTO topics (
            topic_name, topic_slug, session_number, category, subcategory,
            description, total_qa_pairs, priority, topic_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dlt_data['indicator'],
        'distributed_ledger_technology',
        1,
        dlt_data['category'],
        dlt_data['subcategory'],
        'Fundamental blockchain technology concept explaining distributed ledger systems',
        dlt_data['total_questions'],
        'high',
        'technology_concept'
    ))
    topic_id = cursor.lastrowid
    print(f"✓ Created Topic: {dlt_data['indicator']} (ID: {topic_id})")

    # Insert Q&A pairs
    print(f"\nInserting {len(dlt_data['answers'])} Q&A pairs...")
    inserted_count = 0

    for answer_obj in dlt_data['answers']:
        question_num = answer_obj['question_number']
        question = answer_obj['question']
        answer = answer_obj['answer']
        answer_length = len(answer)

        # Check for examples and sources
        has_examples = 1 if 'example' in answer.lower() or 'scenario' in answer.lower() else 0
        has_sources = 1 if 'source' in answer.lower() or 'according to' in answer.lower() else 0

        cursor.execute('''
            INSERT INTO qa_pairs (
                topic_id, pair_number, question, answer, subtopic,
                created_date, topic_name, answer_length, has_examples,
                has_sources, crypto_specific, technology_focus
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            topic_id,
            question_num,
            question,
            answer,
            dlt_data['subcategory'],
            session_date,
            dlt_data['indicator'],
            answer_length,
            has_examples,
            has_sources,
            1,  # crypto_specific
            1   # technology_focus
        ))

        inserted_count += 1
        if inserted_count % 20 == 0:
            print(f"  Inserted {inserted_count}/{len(dlt_data['answers'])} pairs...")

    print(f"✓ Inserted all {inserted_count} Q&A pairs")

    # Insert batch metadata
    cursor.execute('''
        INSERT INTO batch_metadata (
            batch_name, category, subcategory, total_topics,
            total_qa_pairs, source, integrated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Batch 1 - DLT Fundamentals',
        dlt_data['category'],
        dlt_data['subcategory'],
        1,
        dlt_data['total_questions'],
        'inbox/cursor/dlt_questions_answers.json',
        datetime.now().isoformat()
    ))
    print("✓ Created batch metadata")

    conn.commit()
    print("\n✅ DLT data integrated successfully!")

def generate_summary_report(cursor):
    """Generate summary report of the database"""

    print("\n" + "="*60)
    print("DATABASE SUMMARY REPORT")
    print("="*60 + "\n")

    # Get database info
    cursor.execute("SELECT value FROM project_info WHERE key = 'database_name'")
    db_name = cursor.fetchone()[0]
    print(f"Database: {db_name}\n")

    # Get session info
    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]
    print(f"Total Sessions: {total_sessions}")

    # Get topic info
    cursor.execute("SELECT COUNT(*) FROM topics")
    total_topics = cursor.fetchone()[0]
    print(f"Total Topics: {total_topics}")

    # Get Q&A info
    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    total_pairs = cursor.fetchone()[0]
    print(f"Total Q&A Pairs: {total_pairs}")

    # Get answer length stats
    cursor.execute('''
        SELECT
            AVG(answer_length) as avg_length,
            MIN(answer_length) as min_length,
            MAX(answer_length) as max_length
        FROM qa_pairs
    ''')
    avg_len, min_len, max_len = cursor.fetchone()
    print(f"\nAnswer Length Statistics:")
    print(f"  Average: {avg_len:.0f} characters")
    print(f"  Minimum: {min_len} characters")
    print(f"  Maximum: {max_len} characters")

    # Get quality metrics
    cursor.execute('''
        SELECT
            SUM(has_examples) as with_examples,
            SUM(crypto_specific) as crypto_specific,
            SUM(technology_focus) as tech_focus
        FROM qa_pairs
    ''')
    examples, crypto, tech = cursor.fetchone()
    print(f"\nQuality Metrics:")
    print(f"  With Examples: {examples}/{total_pairs} ({examples/total_pairs*100:.1f}%)")
    print(f"  Crypto-Specific: {crypto}/{total_pairs} ({crypto/total_pairs*100:.1f}%)")
    print(f"  Technology Focus: {tech}/{total_pairs} ({tech/total_pairs*100:.1f}%)")

    # List topics
    cursor.execute('''
        SELECT topic_name, category, subcategory, total_qa_pairs, priority
        FROM topics
    ''')
    topics = cursor.fetchall()
    print(f"\nTopics in Database:")
    for topic in topics:
        print(f"  • {topic[0]}")
        print(f"    Category: {topic[1]} > {topic[2]}")
        print(f"    Q&A Pairs: {topic[3]}")
        print(f"    Priority: {topic[4]}")

    print("\n" + "="*60)
    print("✅ CRYPTO_FUNDAMENTALS_PRODUCTION.DB READY!")
    print("="*60)

def main():
    """Main execution function"""

    print("\n" + "="*60)
    print("CRYPTO FUNDAMENTALS DATABASE CREATION")
    print("="*60 + "\n")

    # Create database
    conn, cursor = create_fundamentals_database()

    # Integrate DLT data
    integrate_dlt_data(cursor, conn)

    # Generate summary report
    generate_summary_report(cursor)

    # Close connection
    conn.close()

    print("\n✅ All operations completed successfully!")
    print(f"Database location: crypto_fundamentals_production.db")

if __name__ == '__main__':
    main()
