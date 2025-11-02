"""
Universal Domain Batch Importer
Imports parsed Q&A data into database for ANY domain

Works with the universal database schema
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path


def create_universal_database(db_path, domain_name):
    """
    Create universal database schema for any domain

    Tables:
    - domains: Domain metadata
    - sessions: Research sessions
    - topics: Knowledge topics (replaces "indicators")
    - qa_pairs: Question-answer pairs
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Domains table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_name TEXT NOT NULL UNIQUE,
            domain_slug TEXT NOT NULL UNIQUE,
            description TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL
        )
    ''')

    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_id INTEGER NOT NULL,
            session_number INTEGER NOT NULL,
            category TEXT,
            subcategory TEXT,
            status TEXT DEFAULT 'pending',
            total_topics INTEGER DEFAULT 0,
            total_qa_pairs INTEGER DEFAULT 0,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            FOREIGN KEY (domain_id) REFERENCES domains (domain_id),
            UNIQUE (domain_id, session_number)
        )
    ''')

    # Topics table (universal replacement for "indicators")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_id INTEGER NOT NULL,
            session_number INTEGER,
            topic_name TEXT NOT NULL,
            topic_slug TEXT NOT NULL,
            description TEXT,
            total_qa_pairs INTEGER DEFAULT 0,
            source_sessions TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            FOREIGN KEY (domain_id) REFERENCES domains (domain_id),
            UNIQUE (domain_id, topic_slug)
        )
    ''')

    # Q&A Pairs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            pair_number INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            topic_tag TEXT,
            source_file TEXT,
            created_date TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id)
        )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_topics_domain ON topics(domain_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_topics_session ON topics(session_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_qa_topic ON qa_pairs(topic_id)')

    conn.commit()
    conn.close()

    print(f"✅ Database created: {db_path}")


def import_parsed_data(parsed_json_file, db_path, domain_name, domain_id=None, session_number=None):
    """
    Import parsed Q&A data into universal database

    Args:
        parsed_json_file: Path to parsed JSON from parse_domain_research.py
        db_path: Database file path
        domain_name: Domain name
        domain_id: Domain slug/ID (optional, extracted from JSON)
        session_number: Session number (optional)

    Returns:
        dict: Import statistics
    """
    # Load parsed data
    with open(parsed_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract metadata
    if domain_id is None:
        domain_id = data.get('domain', 'general')

    topic_name = data['topic']
    topic_slug = data['topic_slug']
    qa_pairs = data['qa_pairs']

    print(f"\n{'='*60}")
    print(f"IMPORTING: {topic_name}")
    print(f"Domain: {domain_name} ({domain_id})")
    print(f"Q&A Pairs: {len(qa_pairs)}")
    print(f"{'='*60}\n")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Ensure domain exists
        domain_pk = ensure_domain_exists(cursor, domain_name, domain_id)

        # Ensure session exists (if session number provided)
        if session_number:
            ensure_session_exists(cursor, domain_pk, session_number)

        # Check if topic already exists
        cursor.execute('''
            SELECT topic_id, total_qa_pairs, source_sessions
            FROM topics
            WHERE domain_id = ? AND topic_slug = ?
        ''', (domain_pk, topic_slug))

        existing = cursor.fetchone()

        if existing:
            # Update existing topic
            topic_id = existing[0]
            current_qa = existing[1]
            source_sessions = existing[2] or ""

            # Add session to source_sessions if not already there
            if session_number and str(session_number) not in source_sessions:
                source_sessions = f"{source_sessions},{session_number}".strip(',')

            cursor.execute('''
                UPDATE topics
                SET total_qa_pairs = total_qa_pairs + ?,
                    source_sessions = ?,
                    updated_date = ?
                WHERE topic_id = ?
            ''', (len(qa_pairs), source_sessions, datetime.now().isoformat(), topic_id))

            print(f"📝 Updated existing topic: {topic_name}")
            print(f"   Previous Q&A: {current_qa}")
            print(f"   Adding: {len(qa_pairs)}")
            print(f"   New Total: {current_qa + len(qa_pairs)}")

        else:
            # Insert new topic
            source_sessions = str(session_number) if session_number else ""

            cursor.execute('''
                INSERT INTO topics (
                    domain_id, session_number, topic_name, topic_slug,
                    total_qa_pairs, source_sessions, created_date, updated_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                domain_pk, session_number, topic_name, topic_slug,
                len(qa_pairs), source_sessions,
                datetime.now().isoformat(), datetime.now().isoformat()
            ))

            topic_id = cursor.lastrowid
            print(f"✅ Created new topic: {topic_name} (ID: {topic_id})")

        # Import Q&A pairs
        for qa in qa_pairs:
            cursor.execute('''
                INSERT INTO qa_pairs (
                    topic_id, pair_number, question, answer, topic_tag,
                    source_file, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                topic_id,
                qa.get('pair_number'),
                qa['question'],
                qa['answer'],
                qa.get('topic', topic_name),
                data.get('source_file', ''),
                qa.get('created_date', datetime.now().isoformat())
            ))

        # Update session stats if applicable
        if session_number:
            update_session_stats(cursor, domain_pk, session_number)

        # Update domain stats
        update_domain_stats(cursor, domain_pk)

        conn.commit()

        print(f"\n✅ IMPORT COMPLETE: {topic_name}")
        print(f"   Imported: {len(qa_pairs)} Q&A pairs")
        print(f"   Topic ID: {topic_id}\n")

        return {
            'topic_name': topic_name,
            'topic_id': topic_id,
            'qa_imported': len(qa_pairs),
            'success': True
        }

    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERROR importing {topic_name}: {str(e)}\n")
        return {
            'topic_name': topic_name,
            'qa_imported': 0,
            'success': False,
            'error': str(e)
        }

    finally:
        conn.close()


def ensure_domain_exists(cursor, domain_name, domain_slug):
    """Ensure domain record exists, return domain_id"""
    cursor.execute('SELECT domain_id FROM domains WHERE domain_slug = ?', (domain_slug,))
    result = cursor.fetchone()

    if result:
        return result[0]

    # Create new domain
    cursor.execute('''
        INSERT INTO domains (domain_name, domain_slug, created_date, updated_date)
        VALUES (?, ?, ?, ?)
    ''', (domain_name, domain_slug, datetime.now().isoformat(), datetime.now().isoformat()))

    return cursor.lastrowid


def ensure_session_exists(cursor, domain_id, session_number, category=None, subcategory=None):
    """Ensure session record exists"""
    cursor.execute('''
        SELECT session_id FROM sessions
        WHERE domain_id = ? AND session_number = ?
    ''', (domain_id, session_number))

    result = cursor.fetchone()
    if not result:
        cursor.execute('''
            INSERT INTO sessions (
                domain_id, session_number, category, subcategory,
                status, created_date, updated_date
            ) VALUES (?, ?, ?, ?, 'active', ?, ?)
        ''', (
            domain_id, session_number, category, subcategory,
            datetime.now().isoformat(), datetime.now().isoformat()
        ))


def update_session_stats(cursor, domain_id, session_number):
    """Update session statistics"""
    # Count topics and Q&A pairs for this session
    cursor.execute('''
        SELECT COUNT(DISTINCT topic_id), SUM(total_qa_pairs)
        FROM topics
        WHERE domain_id = ? AND (
            session_number = ? OR
            source_sessions LIKE '%' || ? || '%'
        )
    ''', (domain_id, session_number, session_number))

    stats = cursor.fetchone()
    topic_count = stats[0] or 0
    qa_count = stats[1] or 0

    cursor.execute('''
        UPDATE sessions
        SET total_topics = ?,
            total_qa_pairs = ?,
            updated_date = ?
        WHERE domain_id = ? AND session_number = ?
    ''', (topic_count, qa_count, datetime.now().isoformat(), domain_id, session_number))


def update_domain_stats(cursor, domain_id):
    """Update domain-level statistics"""
    cursor.execute('''
        UPDATE domains
        SET updated_date = ?
        WHERE domain_id = ?
    ''', (datetime.now().isoformat(), domain_id))


def import_batch(parsed_data_dir, db_path, domain_name, domain_id, session_number=None):
    """
    Import all parsed JSON files from a directory

    Args:
        parsed_data_dir: Directory containing *_qa_pairs.json files
        db_path: Database path
        domain_name: Domain name
        domain_id: Domain slug/ID
        session_number: Optional session number

    Returns:
        dict: Import summary
    """
    from glob import glob

    json_files = glob(f"{parsed_data_dir}/*_qa_pairs.json")

    print(f"\n{'='*60}")
    print(f"BATCH IMPORT: {len(json_files)} files")
    print(f"Domain: {domain_name}")
    print(f"Database: {db_path}")
    print(f"{'='*60}\n")

    results = []
    for json_file in json_files:
        result = import_parsed_data(
            json_file,
            db_path,
            domain_name,
            domain_id,
            session_number
        )
        results.append(result)

    # Summary
    successful = [r for r in results if r['success']]
    total_qa = sum(r['qa_imported'] for r in successful)

    print(f"\n{'='*60}")
    print(f"BATCH IMPORT COMPLETE")
    print(f"Files Processed: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(results) - len(successful)}")
    print(f"Total Q&A Imported: {total_qa}")
    print(f"{'='*60}\n")

    return {
        'files_processed': len(results),
        'successful': len(successful),
        'failed': len(results) - len(successful),
        'total_qa_imported': total_qa,
        'results': results
    }


# CLI Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage:")
        print("  Single file: python import_domain_batch.py <json_file> <db_path> <domain_name> [domain_id] [session]")
        print("  Batch:       python import_domain_batch.py --batch <dir> <db_path> <domain_name> <domain_id> [session]")
        print("\nExamples:")
        print("  python import_domain_batch.py sma_qa_pairs.json database.db 'Crypto Indicators' crypto_indicators 1")
        print("  python import_domain_batch.py --batch parsed_qa_data/ database.db 'Web Dev' web_development")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        data_dir = sys.argv[2]
        db_path = sys.argv[3]
        domain_name = sys.argv[4]
        domain_id = sys.argv[5] if len(sys.argv) > 5 else 'general'
        session = int(sys.argv[6]) if len(sys.argv) > 6 else None

        # Create database if it doesn't exist
        if not os.path.exists(db_path):
            create_universal_database(db_path, domain_name)

        import_batch(data_dir, db_path, domain_name, domain_id, session)
    else:
        json_file = sys.argv[1]
        db_path = sys.argv[2]
        domain_name = sys.argv[3]
        domain_id = sys.argv[4] if len(sys.argv) > 4 else 'general'
        session = int(sys.argv[5]) if len(sys.argv) > 5 else None

        # Create database if it doesn't exist
        if not os.path.exists(db_path):
            create_universal_database(db_path, domain_name)

        import_parsed_data(json_file, db_path, domain_name, domain_id, session)
