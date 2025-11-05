import json

# Load the RAG export file
print("Checking RAG export for Batch 7 sessions...")
with open('inbox/droid/processed/qa_pairs_rag_export_20251102_063730.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total sessions in file: {data['metadata']['total_sessions']}")

# Check for sessions 26-29, 38-44
target_sessions = [26, 27, 28, 29, 38, 39, 40, 41, 42, 43, 44]
sessions_found = {}

for session in data['sessions']:
    session_id = session['session_id']
    if session_id in target_sessions:
        sessions_found[session_id] = {
            'topic': session['topic'],
            'qa_count': len(session['qa_pairs']),
            'tokens_used': session.get('tokens_used', 0)
        }

print(f"\n{'='*70}")
print("BATCH 7 SESSIONS IN RAG EXPORT:")
print(f"{'='*70}")

for session_num in sorted(target_sessions):
    if session_num in sessions_found:
        info = sessions_found[session_num]
        print(f"\n[YES] Session {session_num}: {info['topic']}")
        print(f"   Q&A Pairs: {info['qa_count']}")
        print(f"   Tokens: {info['tokens_used']:,}")
    else:
        print(f"\n[NO] Session {session_num}: NOT FOUND in RAG export")

print(f"\n{'='*70}")
print(f"SUMMARY:")
print(f"{'='*70}")
print(f"Found: {len(sessions_found)}/{len(target_sessions)} sessions")
print(f"Total Q&A pairs in found sessions: {sum(s['qa_count'] for s in sessions_found.values())}")

if len(sessions_found) > 0:
    print(f"\nThese sessions CAN be extracted from the RAG export!")
    print(f"Just like we did for Sessions 30-37.")
