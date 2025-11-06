import json
import sqlite3
from datetime import datetime
import re

print("="*70)
print("PHASE 2 BATCH 2: INTEGRATING SESSIONS 61-80")
print("="*70)

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Check starting state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
starting_pairs = cursor.fetchone()[0]
print(f"\nStarting Q&A pairs in database: {starting_pairs:,}")

# Load RAG export
print("\nLoading RAG export...")
with open('C:/Users/vlaro/dreamteam/claude/inbox/droid/processed/qa_pairs_rag_export_20251102_063730.json', 'r', encoding='utf-8') as f:
    rag_export = json.load(f)

sessions_data = rag_export.get('sessions', [])
print(f"RAG export loaded: {len(sessions_data)} sessions")

# Integration stats
stats = {
    'sessions_processed': 0,
    'indicators_created': 0,
    'indicators_existing': 0,
    'qa_pairs_added': 0,
    'qa_pairs_skipped': 0,
    'errors': []
}

# Target sessions (61-80)
target_sessions = list(range(61, 81))
print(f"\nTarget sessions: {target_sessions[0]}-{target_sessions[-1]} ({len(target_sessions)} sessions)")

for target_session in target_sessions:
    print(f"\n{'='*70}")
    print(f"Processing Session {target_session}")
    print(f"{'='*70}")

    # Find session in RAG data
    session_found = None
    for session in sessions_data:
        if session.get('session_id') == target_session:
            session_found = session
            break

    if not session_found:
        print(f"  WARNING: Session {target_session} not found in RAG export")
        stats['errors'].append(f"Session {target_session} not found")
        continue

    topic = session_found.get('topic', 'Unknown')
    qa_pairs = session_found.get('qa_pairs', [])

    print(f"Session topic: {topic[:80]}...")
    print(f"Q&A pairs available: {len(qa_pairs)}")

    # Use topic as indicator name
    indicator_name = topic

    # Categorize based on topic keywords
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ['price', 'moving average', 'macd', 'rsi', 'oscillator', 'momentum']):
        category = 'Price-Based Technical Indicators'
    elif any(word in topic_lower for word in ['volume', 'obv', 'mfi', 'vwap']):
        category = 'Volume-Based Indicators'
    elif any(word in topic_lower for word in ['blockchain', 'network', 'hash', 'difficulty', 'mining']):
        category = 'Blockchain Metrics'
    elif any(word in topic_lower for word in ['exchange', 'flow', 'whale', 'holder']):
        category = 'Exchange & Holder Metrics'
    elif any(word in topic_lower for word in ['sentiment', 'social', 'fear', 'greed']):
        category = 'Market Sentiment'
    elif any(word in topic_lower for word in ['defi', 'dex', 'tvl', 'liquidity']):
        category = 'DeFi Metrics'
    elif any(word in topic_lower for word in ['regulation', 'legal', 'compliance', 'tax']):
        category = 'Regulatory & Legal'
    else:
        category = 'Advanced Indicators'

    # Check if indicator exists
    cursor.execute('''
        SELECT id FROM crypto_indicators
        WHERE indicator_name = ?
    ''', (indicator_name,))

    result = cursor.fetchone()

    if result:
        indicator_id = result[0]
        stats['indicators_existing'] += 1
    else:
        # Create indicator
        cursor.execute('''
            INSERT INTO crypto_indicators (
                indicator_name, indicator_category, session_number,
                description, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            indicator_name,
            category,
            target_session,
            f"{indicator_name} - Session {target_session}",
            datetime.now(),
            datetime.now()
        ))

        indicator_id = cursor.lastrowid
        stats['indicators_created'] += 1
        print(f"  Created indicator (ID: {indicator_id})")

    # Process Q&A pairs
    pairs_added = 0
    for idx, qa in enumerate(qa_pairs, 1):
        # Extract question and answer
        question = qa.get('question', '')
        answer = qa.get('answer', '')

        if not question or not answer:
            # Try alternate structure
            content = qa.get('content', '')
            if 'Question:' in content and 'Answer:' in content:
                parts = content.split('Answer:', 1)
                if len(parts) == 2:
                    question = parts[0].replace('Question:', '').strip()
                    answer = parts[1].strip()

        if not question or not answer:
            stats['errors'].append(f"Session {target_session}, pair {idx}: Missing content")
            continue

        # Check for duplicate
        cursor.execute('''
            SELECT qa_id FROM qa_pairs
            WHERE indicator_id = ? AND question = ?
        ''', (indicator_id, question))

        if cursor.fetchone():
            stats['qa_pairs_skipped'] += 1
            continue

        # Get next pair_number
        cursor.execute('''
            SELECT COALESCE(MAX(pair_number), 0) + 1
            FROM qa_pairs
            WHERE indicator_id = ?
        ''', (indicator_id,))
        next_pair_number = cursor.fetchone()[0]

        # Analyze answer
        answer_length = len(answer)
        has_formula = bool(re.search(r'[=×÷\+\-]|\bformula\b', answer, re.IGNORECASE))
        has_examples = bool(re.search(r'\bexample\b|\bfor instance\b|\be\.g\.\b', answer, re.IGNORECASE))
        has_sources = bool(re.search(r'\bsource\b|\baccording to\b|\bresearch\b', answer, re.IGNORECASE))

        # Insert Q&A pair
        cursor.execute('''
            INSERT INTO qa_pairs (
                indicator_id, indicator_name, pair_number,
                question, answer,
                difficulty_level, answer_length,
                has_formula, has_examples, has_sources,
                crypto_specific, created_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            indicator_id,
            indicator_name,
            next_pair_number,
            question,
            answer,
            'intermediate',
            answer_length,
            has_formula,
            has_examples,
            has_sources,
            True,
            datetime.now().strftime('%Y-%m-%d')
        ))

        pairs_added += 1
        stats['qa_pairs_added'] += 1

    print(f"  Inserted {pairs_added} Q&A pairs")
    stats['sessions_processed'] += 1

    # Commit every 5 sessions
    if stats['sessions_processed'] % 5 == 0:
        conn.commit()
        print(f"  [Checkpoint] Committed after {stats['sessions_processed']} sessions")

# Final commit
conn.commit()

# Final report
print(f"\n{'='*70}")
print("PHASE 2 BATCH 2 INTEGRATION COMPLETE")
print(f"{'='*70}")
print(f"Sessions processed: {stats['sessions_processed']}")
print(f"Indicators created: {stats['indicators_created']}")
print(f"Indicators existing: {stats['indicators_existing']}")
print(f"Q&A pairs added: {stats['qa_pairs_added']}")
print(f"Q&A pairs skipped (duplicates): {stats['qa_pairs_skipped']}")

if stats['errors']:
    print(f"\nWarnings/Errors: {len(stats['errors'])}")
    for error in stats['errors'][:10]:
        print(f"  - {error}")

# Verify final state
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_pairs = cursor.fetchone()[0]
growth = final_pairs - starting_pairs

print(f"\nDatabase Status:")
print(f"  Starting pairs: {starting_pairs:,}")
print(f"  Final pairs: {final_pairs:,}")
print(f"  Growth: +{growth:,} pairs (+{(growth / starting_pairs * 100):.1f}%)")

# Session coverage
cursor.execute('SELECT COUNT(DISTINCT session_number) FROM crypto_indicators WHERE session_number < 900')
total_sessions = cursor.fetchone()[0]
print(f"  Total sessions in DB: {total_sessions}")

# Coverage through 80
cursor.execute('SELECT COUNT(DISTINCT session_number) FROM crypto_indicators WHERE session_number BETWEEN 1 AND 80')
sessions_1_80 = cursor.fetchone()[0]
print(f"  Sessions 1-80 coverage: {sessions_1_80}/80 ({(sessions_1_80/80*100):.1f}%)")

conn.close()

print("\n" + "="*70)
print("PHASE 2 BATCH 2 SUCCESS - READY FOR BATCH 3")
print("="*70)
