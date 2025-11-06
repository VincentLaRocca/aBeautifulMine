import json
import sqlite3
from datetime import datetime
from collections import defaultdict

print("="*80)
print("CLAUDE_SHARED DATABASE GAP ANALYSIS")
print("="*80)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# PHASE 1: LOAD CLAUDE_SHARED DATA
print("\n" + "="*80)
print("PHASE 1: LOADING CLAUDE_SHARED ORIGINAL DATABASE")
print("="*80)

claude_shared_path = 'C:/users/vlaro/claude_shared/data/qa_harvest/processed/database_qa_export_20251030_012343.json'

print(f"\nLoading: {claude_shared_path}")

try:
    with open(claude_shared_path, 'r', encoding='utf-8') as f:
        claude_shared = json.load(f)
    print("[OK] Successfully loaded claude_shared database")
except FileNotFoundError:
    print("[ERROR] Claude_shared file not found!")
    print("Please verify path and run again.")
    exit(1)

# Extract metadata
metadata = claude_shared.get('export_metadata', claude_shared.get('metadata', {}))
sessions = claude_shared.get('sessions', [])

print(f"\nClaude_Shared Metadata:")
print(f"  Source Database: {metadata.get('source_database', 'crypto_indicators_production.db')}")
print(f"  Export Date: {metadata.get('export_date', 'Unknown')}")
print(f"  Total Sessions: {metadata.get('total_sessions', len(sessions))}")
print(f"  Total Q&A Pairs: {metadata.get('total_qa_pairs', 'Calculating...')}")
print(f"  Total Tokens: {metadata.get('total_tokens', 'N/A'):,}" if metadata.get('total_tokens') else "")

# Build session map
claude_sessions = {}
claude_total_pairs = 0

for session in sessions:
    session_id = session.get('session_id')
    topic = session.get('topic', 'Unknown')
    qa_pairs = session.get('question_answer_pairs', session.get('qa_pairs', []))

    claude_sessions[session_id] = {
        'topic': topic,
        'pairs': qa_pairs,
        'pair_count': len(qa_pairs)
    }
    claude_total_pairs += len(qa_pairs)

print(f"\nClaude_Shared Statistics:")
print(f"  Sessions loaded: {len(claude_sessions)}")
print(f"  Total Q&A pairs: {claude_total_pairs:,}")
print(f"  Average pairs per session: {claude_total_pairs / len(claude_sessions):.1f}")

# PHASE 2: LOAD PRODUCTION DATABASE
print("\n" + "="*80)
print("PHASE 2: LOADING PRODUCTION DATABASE")
print("="*80)

conn = sqlite3.connect('crypto_indicators_production.db')
cursor = conn.cursor()

# Get production statistics
cursor.execute('SELECT COUNT(*) FROM qa_pairs')
prod_total_pairs = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT indicator_id) FROM qa_pairs')
prod_indicators = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(DISTINCT session_number) FROM crypto_indicators WHERE session_number < 900')
prod_sessions_count = cursor.fetchone()[0]

print(f"\nProduction Database Statistics:")
print(f"  Total Q&A pairs: {prod_total_pairs:,}")
print(f"  Unique indicators: {prod_indicators}")
print(f"  Sessions with data: {prod_sessions_count}")

# Build production session map
cursor.execute('''
    SELECT ci.session_number, ci.indicator_name, COUNT(qp.qa_id)
    FROM crypto_indicators ci
    LEFT JOIN qa_pairs qp ON ci.id = qp.indicator_id
    WHERE ci.session_number < 900
    GROUP BY ci.session_number, ci.indicator_name
    ORDER BY ci.session_number
''')

prod_sessions = {}
for row in cursor.fetchall():
    session_num, indicator_name, pair_count = row
    if session_num not in prod_sessions:
        prod_sessions[session_num] = []
    prod_sessions[session_num].append({
        'indicator': indicator_name,
        'pairs': pair_count
    })

# Build production question index for deduplication
print("\nBuilding production question index...")
cursor.execute('SELECT question FROM qa_pairs')
prod_questions = set()
for row in cursor.fetchall():
    prod_questions.add(row[0].strip().lower())

print(f"  Production unique questions: {len(prod_questions):,}")

# PHASE 3: SESSION COMPARISON
print("\n" + "="*80)
print("PHASE 3: SESSION-LEVEL COMPARISON")
print("="*80)

comparison = {
    'in_both': [],
    'claude_only': [],
    'production_only': [],
    'details': []
}

# Get all session IDs
all_session_ids = set(list(claude_sessions.keys()) + list(prod_sessions.keys()))

print(f"\nComparing {len(all_session_ids)} unique session IDs...")

for session_id in sorted(all_session_ids):
    in_claude = session_id in claude_sessions
    in_prod = session_id in prod_sessions

    if in_claude and in_prod:
        claude_pairs = claude_sessions[session_id]['pair_count']
        prod_pairs = sum(ind['pairs'] for ind in prod_sessions[session_id])

        comparison['in_both'].append(session_id)
        comparison['details'].append({
            'session': session_id,
            'status': 'BOTH',
            'claude_topic': claude_sessions[session_id]['topic'],
            'claude_pairs': claude_pairs,
            'prod_indicators': len(prod_sessions[session_id]),
            'prod_pairs': prod_pairs
        })

    elif in_claude:
        comparison['claude_only'].append(session_id)
        comparison['details'].append({
            'session': session_id,
            'status': 'CLAUDE_ONLY',
            'claude_topic': claude_sessions[session_id]['topic'],
            'claude_pairs': claude_sessions[session_id]['pair_count']
        })

    else:
        prod_pairs = sum(ind['pairs'] for ind in prod_sessions[session_id])
        comparison['production_only'].append(session_id)
        comparison['details'].append({
            'session': session_id,
            'status': 'PROD_ONLY',
            'prod_indicators': len(prod_sessions[session_id]),
            'prod_pairs': prod_pairs
        })

print(f"\nSession Distribution:")
print(f"  In BOTH databases: {len(comparison['in_both'])} sessions")
print(f"  ONLY in claude_shared: {len(comparison['claude_only'])} sessions")
print(f"  ONLY in production: {len(comparison['production_only'])} sessions")

# PHASE 4: QUESTION-LEVEL DEDUPLICATION
print("\n" + "="*80)
print("PHASE 4: QUESTION-LEVEL ANALYSIS")
print("="*80)

print("\nAnalyzing question overlap...")

unique_pairs = []
duplicate_pairs = []
session_stats = defaultdict(lambda: {'unique': 0, 'duplicates': 0})

for session_id, session_data in claude_sessions.items():
    for qa in session_data['pairs']:
        question = qa.get('question', '').strip()
        answer = qa.get('answer', '').strip()

        if not question or not answer:
            continue

        question_lower = question.lower()

        if question_lower not in prod_questions:
            unique_pairs.append({
                'session': session_id,
                'topic': session_data['topic'],
                'question': question,
                'answer': answer,
                'answer_length': len(answer)
            })
            session_stats[session_id]['unique'] += 1
        else:
            duplicate_pairs.append({
                'session': session_id,
                'question': question[:100]
            })
            session_stats[session_id]['duplicates'] += 1

print(f"\nDeduplication Results:")
print(f"  Unique questions (NEW): {len(unique_pairs):,}")
print(f"  Duplicate questions (SKIP): {len(duplicate_pairs):,}")
print(f"  Duplicate rate: {(len(duplicate_pairs) / claude_total_pairs * 100):.1f}%")
print(f"  Unique rate: {(len(unique_pairs) / claude_total_pairs * 100):.1f}%")

# PHASE 5: CONTENT QUALITY ANALYSIS
print("\n" + "="*80)
print("PHASE 5: CONTENT QUALITY METRICS")
print("="*80)

# Analyze unique pairs quality
if unique_pairs:
    total_length = sum(p['answer_length'] for p in unique_pairs)
    avg_length = total_length / len(unique_pairs)

    print(f"\nUnique Pairs Quality:")
    print(f"  Total unique pairs: {len(unique_pairs):,}")
    print(f"  Average answer length: {avg_length:.0f} characters")
    print(f"  Total content volume: {total_length:,} characters")

    # Length distribution
    short = len([p for p in unique_pairs if p['answer_length'] < 1000])
    medium = len([p for p in unique_pairs if 1000 <= p['answer_length'] < 3000])
    long_ans = len([p for p in unique_pairs if p['answer_length'] >= 3000])

    print(f"\n  Length Distribution:")
    print(f"    Short (<1000 chars): {short:,} pairs ({short/len(unique_pairs)*100:.1f}%)")
    print(f"    Medium (1000-3000): {medium:,} pairs ({medium/len(unique_pairs)*100:.1f}%)")
    print(f"    Long (3000+): {long_ans:,} pairs ({long_ans/len(unique_pairs)*100:.1f}%)")

# Compare with production
cursor.execute('SELECT AVG(answer_length) FROM qa_pairs')
prod_avg_length = cursor.fetchone()[0]

print(f"\n  Comparison with Production:")
print(f"    Claude_shared avg: {avg_length:.0f} chars")
print(f"    Production avg: {prod_avg_length:.0f} chars")
print(f"    Difference: {avg_length - prod_avg_length:+.0f} chars")

# PHASE 6: CATEGORY ANALYSIS
print("\n" + "="*80)
print("PHASE 6: TOPIC CATEGORY ANALYSIS")
print("="*80)

# Categorize unique pairs
category_stats = defaultdict(lambda: {'sessions': set(), 'pairs': 0})

for pair in unique_pairs:
    topic = pair['topic'].lower()
    session = pair['session']

    # Simple categorization
    if any(word in topic for word in ['moving average', 'macd', 'rsi', 'oscillator', 'momentum']):
        category = 'Technical Indicators'
    elif any(word in topic for word in ['defi', 'dex', 'tvl', 'liquidity', 'yield']):
        category = 'DeFi & Protocols'
    elif any(word in topic for word in ['blockchain', 'network', 'hash', 'mining']):
        category = 'Blockchain Metrics'
    elif any(word in topic for word in ['market making', 'derivatives', 'futures', 'options']):
        category = 'Advanced Trading'
    elif any(word in topic for word in ['regulation', 'legal', 'compliance', 'tax']):
        category = 'Regulatory'
    elif any(word in topic for word in ['sentiment', 'social', 'fear', 'greed']):
        category = 'Market Sentiment'
    else:
        category = 'Other'

    category_stats[category]['sessions'].add(session)
    category_stats[category]['pairs'] += 1

print(f"\nUnique Pairs by Category:")
for category in sorted(category_stats.keys()):
    stats = category_stats[category]
    print(f"  {category}:")
    print(f"    Sessions: {len(stats['sessions'])}")
    print(f"    Pairs: {stats['pairs']:,}")

# PHASE 7: INTEGRATION IMPACT PROJECTION
print("\n" + "="*80)
print("PHASE 7: INTEGRATION IMPACT PROJECTION")
print("="*80)

projected_total = prod_total_pairs + len(unique_pairs)
goal = 30000
progress = (projected_total / goal * 100)

print(f"\nCurrent Status:")
print(f"  Production DB: {prod_total_pairs:,} pairs")
print(f"  Goal: {goal:,} pairs")
print(f"  Current progress: {(prod_total_pairs/goal*100):.1f}%")

print(f"\nAfter Claude_Shared Integration:")
print(f"  Unique pairs to add: {len(unique_pairs):,}")
print(f"  Projected total: {projected_total:,} pairs")
print(f"  Projected progress: {progress:.1f}%")
print(f"  Remaining to goal: {goal - projected_total:,} pairs")

if projected_total >= goal:
    print(f"  [SUCCESS] GOAL EXCEEDED by {projected_total - goal:,} pairs!")
else:
    print(f"  Gap to goal: {goal - projected_total:,} pairs ({((goal-projected_total)/goal*100):.1f}%)")

# PHASE 8: SESSION-BY-SESSION BREAKDOWN
print("\n" + "="*80)
print("PHASE 8: DETAILED SESSION BREAKDOWN")
print("="*80)

print("\nSessions with Unique Content (Top 20 by pair count):")
print(f"{'Session':<10} {'Unique':<8} {'Dups':<8} {'Topic':<50}")
print("-" * 80)

sorted_sessions = sorted(
    [(sid, stats['unique'], stats['duplicates'], claude_sessions[sid]['topic'])
     for sid, stats in session_stats.items() if stats['unique'] > 0],
    key=lambda x: x[1],
    reverse=True
)

for i, (session_id, unique, dups, topic) in enumerate(sorted_sessions[:20], 1):
    topic_short = topic[:47] + "..." if len(topic) > 50 else topic
    print(f"{session_id:<10} {unique:<8} {dups:<8} {topic_short}")

if len(sorted_sessions) > 20:
    print(f"\n... and {len(sorted_sessions) - 20} more sessions with unique content")

# PHASE 9: GENERATE SUMMARY REPORT
print("\n" + "="*80)
print("PHASE 9: GENERATING SUMMARY REPORT")
print("="*80)

summary = {
    'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'claude_shared': {
        'total_sessions': len(claude_sessions),
        'total_pairs': claude_total_pairs,
        'avg_pairs_per_session': claude_total_pairs / len(claude_sessions)
    },
    'production': {
        'total_pairs': prod_total_pairs,
        'total_sessions': prod_sessions_count,
        'unique_questions': len(prod_questions)
    },
    'comparison': {
        'sessions_in_both': len(comparison['in_both']),
        'sessions_claude_only': len(comparison['claude_only']),
        'sessions_prod_only': len(comparison['production_only'])
    },
    'deduplication': {
        'unique_pairs': len(unique_pairs),
        'duplicate_pairs': len(duplicate_pairs),
        'duplicate_rate': len(duplicate_pairs) / claude_total_pairs * 100,
        'unique_rate': len(unique_pairs) / claude_total_pairs * 100
    },
    'quality': {
        'avg_answer_length_unique': avg_length if unique_pairs else 0,
        'avg_answer_length_production': prod_avg_length
    },
    'projection': {
        'current_total': prod_total_pairs,
        'pairs_to_add': len(unique_pairs),
        'projected_total': projected_total,
        'goal': goal,
        'projected_progress_pct': progress,
        'remaining_to_goal': goal - projected_total
    }
}

# Save summary to JSON
with open('claude_shared_gap_analysis_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

print("[OK] Summary saved to: claude_shared_gap_analysis_summary.json")

# Save detailed session breakdown
session_breakdown = []
for session_id in sorted(claude_sessions.keys()):
    stats = session_stats[session_id]
    session_breakdown.append({
        'session_id': session_id,
        'topic': claude_sessions[session_id]['topic'],
        'claude_total_pairs': claude_sessions[session_id]['pair_count'],
        'unique_pairs': stats['unique'],
        'duplicate_pairs': stats['duplicates'],
        'in_production': session_id in prod_sessions,
        'prod_pair_count': sum(ind['pairs'] for ind in prod_sessions.get(session_id, []))
    })

with open('claude_shared_session_breakdown.json', 'w', encoding='utf-8') as f:
    json.dump(session_breakdown, f, indent=2)

print("[OK] Session breakdown saved to: claude_shared_session_breakdown.json")

# Save unique pairs for integration
unique_pairs_export = {
    'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_unique_pairs': len(unique_pairs),
    'pairs': unique_pairs
}

with open('claude_shared_unique_pairs_ready.json', 'w', encoding='utf-8') as f:
    json.dump(unique_pairs_export, f, indent=2)

print("[OK] Unique pairs export saved to: claude_shared_unique_pairs_ready.json")

# Close database
conn.close()

# FINAL SUMMARY
print("\n" + "="*80)
print("GAP ANALYSIS COMPLETE")
print("="*80)

print(f"\n[KEY FINDINGS]")
print(f"   - Claude_shared contains {claude_total_pairs:,} total pairs across {len(claude_sessions)} sessions")
print(f"   - Production currently has {prod_total_pairs:,} pairs across {prod_sessions_count} sessions")
print(f"   - Found {len(unique_pairs):,} UNIQUE pairs ready to integrate")
print(f"   - Integration would bring total to {projected_total:,} pairs ({progress:.1f}% of goal)")

print(f"\n[OUTPUT FILES]")
print(f"   1. claude_shared_gap_analysis_summary.json - High-level metrics")
print(f"   2. claude_shared_session_breakdown.json - Session-by-session details")
print(f"   3. claude_shared_unique_pairs_ready.json - Unique pairs for integration")

print(f"\n[NEXT STEP]")
print(f"   Run: python integrate_claude_shared_original_db.py")
print(f"   This will integrate the {len(unique_pairs):,} unique pairs into production")

print("\n" + "="*80)
print("For the Greater Good of All")
print("="*80)
