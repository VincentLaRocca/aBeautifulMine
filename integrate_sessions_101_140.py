"""
Integrate Sessions 101-140 from RAG Export
===========================================

Extracts and integrates sessions 101-140 from Droid's RAG export file.
Target: ~4,000 Q&A pairs from sessions 101-140.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

def integrate_sessions_101_140():
    """Extract sessions 101-140 from RAG export and integrate into production DB"""

    # Load RAG export
    rag_file = Path('inbox/droid/processed/qa_pairs_rag_export_20251102_075728.json')
    print(f"Loading RAG export from {rag_file}")

    with open(rag_file, 'r', encoding='utf-8') as f:
        rag_data = json.load(f)

    # Filter sessions 101-140
    target_sessions = []
    for session in rag_data['sessions']:
        if 101 <= session['session_id'] <= 140:
            target_sessions.append(session)

    print(f"Found {len(target_sessions)} sessions in range 101-140")

    # Connect to database
    conn = sqlite3.connect('crypto_indicators_production.db')
    c = conn.cursor()

    # Get current count
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    start_count = c.fetchone()[0]
    print(f"Current database pairs: {start_count}")
    print()

    total_pairs_added = 0
    total_indicators_added = 0
    session_stats = []

    for session in sorted(target_sessions, key=lambda x: x['session_id']):
        session_id = session['session_id']
        topic = session['topic']
        qa_pairs = session['qa_pairs']

        print(f"Session {session_id}: {topic}")
        print(f"  Total pairs in session: {len(qa_pairs)}")

        # Determine indicator name from topic
        indicator_name = topic.split()[0] if topic else f"session_{session_id}"
        category = "Technical Indicators"

        # Check if indicator exists
        c.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
        result = c.fetchone()

        if result:
            indicator_id = result[0]
        else:
            # Create new indicator
            c.execute('''INSERT INTO crypto_indicators (indicator_name, indicator_category, description)
                       VALUES (?, ?, ?)''',
                      (indicator_name, category, topic))
            indicator_id = c.lastrowid
            total_indicators_added += 1

        # Get max pair_number for this indicator
        c.execute('SELECT COALESCE(MAX(pair_number), 0) FROM qa_pairs WHERE indicator_id = ?', (indicator_id,))
        max_pair = c.fetchone()[0]

        # Insert pairs
        pairs_added = 0
        pairs_skipped = 0

        for pair_data in qa_pairs:
            question = pair_data.get('question', '')
            answer = pair_data.get('answer', '')

            if not question or not answer:
                pairs_skipped += 1
                continue

            # Check for duplicate by question
            c.execute('''SELECT qa_id FROM qa_pairs
                       WHERE indicator_id = ? AND question = ?''',
                      (indicator_id, question))
            if c.fetchone():
                pairs_skipped += 1
                continue  # Skip duplicate

            # Insert
            pair_number = max_pair + pairs_added + 1
            c.execute('''INSERT INTO qa_pairs
                       (indicator_id, pair_number, question, answer, topic, created_date,
                        indicator_name, difficulty_level, answer_length,
                        has_formula, has_examples, has_sources, crypto_specific)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (indicator_id, pair_number, question, answer, topic,
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       indicator_name,
                       'intermediate',
                       len(answer),
                       1 if any(x in answer.lower() for x in ['formula', 'calculation', '=']) else 0,
                       1 if any(x in answer.lower() for x in ['example', 'for instance']) else 0,
                       1 if any(x in answer.lower() for x in ['source', 'according to']) else 0,
                       1 if any(x in answer.lower() for x in ['crypto', 'bitcoin', 'blockchain']) else 0))
            pairs_added += 1

        conn.commit()
        total_pairs_added += pairs_added

        print(f"  Pairs added: {pairs_added}")
        print(f"  Pairs skipped (duplicates): {pairs_skipped}")
        print()

        session_stats.append({
            'session_id': session_id,
            'topic': topic,
            'pairs_added': pairs_added,
            'pairs_skipped': pairs_skipped
        })

    # Final stats
    c.execute('SELECT COUNT(*) FROM qa_pairs')
    final_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM crypto_indicators')
    indicator_count = c.fetchone()[0]

    conn.close()

    print("="*80)
    print("INTEGRATION COMPLETE - SESSIONS 101-140")
    print("="*80)
    print(f"Sessions processed: {len(target_sessions)}")
    print(f"New indicators created: {total_indicators_added}")
    print(f"New pairs added: {total_pairs_added}")
    print(f"Database before: {start_count}")
    print(f"Database after: {final_count}")
    print(f"Net increase: {final_count - start_count}")
    print(f"Total indicators: {indicator_count}")
    print("="*80)

    return {
        'sessions_processed': len(target_sessions),
        'pairs_added': total_pairs_added,
        'indicators_added': total_indicators_added,
        'start_count': start_count,
        'final_count': final_count,
        'session_stats': session_stats
    }

if __name__ == "__main__":
    result = integrate_sessions_101_140()

    # Save results for handoff
    with open('session_101_140_integration_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("\nResults saved to session_101_140_integration_results.json")
