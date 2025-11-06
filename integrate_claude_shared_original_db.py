"""
Integrate Claude_Shared Original Database - Unique Pairs Only
Adds 2,188 unique Q&A pairs to production database

Based on gap analysis results from analyze_claude_shared_gaps.py
Date: November 5, 2025
"""

import json
import sqlite3
from datetime import datetime

print("="*80)
print("CLAUDE_SHARED INTEGRATION - UNIQUE PAIRS")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Load unique pairs export from gap analysis
unique_pairs_path = 'claude_shared_unique_pairs_ready.json'

print(f"\nLoading unique pairs: {unique_pairs_path}")
with open(unique_pairs_path, 'r', encoding='utf-8') as f:
    unique_data = json.load(f)

unique_pairs = unique_data['pairs']
print(f"[OK] Loaded {len(unique_pairs):,} unique pairs ready for integration")

# Connect to production database
conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Get current stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
initial_count = cursor.fetchone()[0]
print(f"\nProduction DB before integration: {initial_count:,} pairs")

# Integration statistics
stats = {
    'sessions_processed': 0,
    'pairs_added': 0,
    'indicators_created': 0,
    'indicators_reused': 0,
    'errors': 0,
    'session_breakdown': []
}

# Group pairs by session for organized integration
from collections import defaultdict
pairs_by_session = defaultdict(list)

for pair in unique_pairs:
    session_id = pair['session']
    pairs_by_session[session_id].append(pair)

print(f"\nUnique content spans {len(pairs_by_session)} sessions")
print(f"Average pairs per session: {len(unique_pairs) / len(pairs_by_session):.1f}")

# Process sessions in order
print("\n" + "="*80)
print("STARTING INTEGRATION")
print("="*80)

for session_id in sorted(pairs_by_session.keys()):
    session_pairs = pairs_by_session[session_id]
    topic = session_pairs[0]['topic']

    print(f"\nSession {session_id}: {topic}")
    print(f"  Pairs to add: {len(session_pairs)}")

    # Categorize topic for database
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ['pi cycle', '111dma', '350dma', 'market timing']):
        category = 'Advanced Market Timing'
    elif any(word in topic_lower for word in ['moving average', 'macd', 'rsi', 'oscillator', 'momentum']):
        category = 'Price-Based Technical Indicators'
    elif any(word in topic_lower for word in ['defi', 'dex', 'tvl', 'liquidity', 'yield']):
        category = 'DeFi Metrics'
    elif any(word in topic_lower for word in ['blockchain', 'network', 'hash', 'mining', 'scalability', 'layer 2']):
        category = 'Blockchain Metrics'
    elif any(word in topic_lower for word in ['futures', 'perpetual', 'options', 'derivatives', 'arbitrage']):
        category = 'Advanced Trading'
    elif any(word in topic_lower for word in ['regulation', 'legal', 'compliance', 'tax']):
        category = 'Regulatory'
    elif any(word in topic_lower for word in ['sentiment', 'social', 'fear', 'greed']):
        category = 'Market Sentiment'
    elif any(word in topic_lower for word in ['portfolio', 'attribution', 'risk']):
        category = 'Portfolio Analytics'
    elif any(word in topic_lower for word in ['infrastructure', 'data processing', 'real-time']):
        category = 'Technical Infrastructure'
    else:
        category = 'Advanced Analytics'

    # Create indicator name (use topic directly)
    indicator_name = topic.strip()

    # Check if indicator already exists
    cursor.execute('SELECT id FROM crypto_indicators WHERE indicator_name = ?', (indicator_name,))
    result = cursor.fetchone()

    if result:
        indicator_id = result[0]
        stats['indicators_reused'] += 1
        print(f"  Using existing indicator ID: {indicator_id}")
    else:
        # Create new indicator
        try:
            cursor.execute('''
                INSERT INTO crypto_indicators
                (indicator_name, indicator_category, description, session_number, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                indicator_name,
                category,
                f"Advanced analysis from session {session_id}: {topic}",
                session_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            indicator_id = cursor.lastrowid
            stats['indicators_created'] += 1
            print(f"  Created new indicator ID: {indicator_id} ({category})")
        except Exception as e:
            print(f"  [ERROR] Could not create indicator: {e}")
            stats['errors'] += 1
            continue

    # Get next pair_number for this indicator
    cursor.execute('''
        SELECT COALESCE(MAX(pair_number), 0) + 1
        FROM qa_pairs WHERE indicator_id = ?
    ''', (indicator_id,))
    next_pair_number = cursor.fetchone()[0]

    # Add all Q&A pairs for this session
    pairs_added_this_session = 0

    for pair in session_pairs:
        question = pair['question'].strip()
        answer = pair['answer'].strip()
        answer_length = len(answer)

        try:
            cursor.execute('''
                INSERT INTO qa_pairs
                (indicator_id, pair_number, question, answer, answer_length, topic)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_id,
                next_pair_number,
                question,
                answer,
                answer_length,
                topic
            ))

            next_pair_number += 1
            pairs_added_this_session += 1
            stats['pairs_added'] += 1

        except Exception as e:
            print(f"  [ERROR] Could not add pair: {e}")
            stats['errors'] += 1

    print(f"  Added: {pairs_added_this_session} pairs")

    stats['sessions_processed'] += 1
    stats['session_breakdown'].append({
        'session_id': session_id,
        'topic': topic,
        'category': category,
        'pairs_added': pairs_added_this_session,
        'indicator_id': indicator_id
    })

    # Commit every 5 sessions
    if stats['sessions_processed'] % 5 == 0:
        conn.commit()
        print(f"\n  [CHECKPOINT] Committed after {stats['sessions_processed']} sessions")

# Final commit
conn.commit()
print(f"\n[FINAL COMMIT] All changes saved")

# Get final stats
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
final_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT indicator_id) FROM qa_pairs')
total_indicators = cursor.fetchone()[0]

# Close connection
conn.close()

# Print summary
print("\n" + "="*80)
print("INTEGRATION COMPLETE")
print("="*80)

print(f"\n[RESULTS]")
print(f"  Sessions processed: {stats['sessions_processed']}")
print(f"  Pairs added: {stats['pairs_added']:,}")
print(f"  Indicators created: {stats['indicators_created']}")
print(f"  Indicators reused: {stats['indicators_reused']}")
print(f"  Errors: {stats['errors']}")

print(f"\n[DATABASE GROWTH]")
print(f"  Before: {initial_count:,} pairs")
print(f"  After: {final_count:,} pairs")
print(f"  Added: {final_count - initial_count:,} pairs")
print(f"  Total indicators: {total_indicators}")

print(f"\n[PROGRESS TO GOAL]")
goal = 30000
progress = (final_count / goal * 100)
remaining = goal - final_count
print(f"  Current: {final_count:,} / {goal:,} pairs")
print(f"  Progress: {progress:.1f}%")
print(f"  Remaining: {remaining:,} pairs")

print(f"\n[NEW SESSION RANGE]")
print(f"  Sessions 107-126 now integrated")
print(f"  Topics: Advanced market timing, derivatives, infrastructure")

# Save integration report
report = {
    'integration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'source': 'claude_shared_original_database',
    'statistics': stats,
    'database': {
        'before': initial_count,
        'after': final_count,
        'added': final_count - initial_count
    },
    'progress': {
        'current': final_count,
        'goal': goal,
        'progress_pct': progress,
        'remaining': remaining
    }
}

with open('claude_shared_integration_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\n[OK] Integration report saved: claude_shared_integration_report.json")

print("\n" + "="*80)
print("For the Greater Good of All")
print("="*80)
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
