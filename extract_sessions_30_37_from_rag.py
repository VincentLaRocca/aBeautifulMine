import json
import sqlite3
from datetime import datetime

# Load the RAG export file
print("Loading RAG export file...")
with open('inbox/droid/processed/qa_pairs_rag_export_20251102_063730.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total sessions in file: {data['metadata']['total_sessions']}")
print(f"Total Q&A pairs in file: {data['metadata']['total_qa_pairs']}")

# Find sessions 30-37
target_sessions = list(range(30, 38))  # 30-37 inclusive
sessions_found = []

for session in data['sessions']:
    session_id = session['session_id']
    if session_id in target_sessions:
        sessions_found.append(session)
        print(f"\nFound Session {session_id}:")
        print(f"  Topic: {session['topic']}")
        print(f"  Q&A pairs: {len(session['qa_pairs'])}")

print(f"\n{'='*60}")
print(f"Sessions found: {len(sessions_found)} out of {len(target_sessions)} expected")
print(f"Total Q&A pairs in sessions 30-37: {sum(len(s['qa_pairs']) for s in sessions_found)}")

if len(sessions_found) > 0:
    # Save extracted sessions to a new file
    output_data = {
        "metadata": {
            "extraction_date": datetime.now().isoformat(),
            "source_file": "qa_pairs_rag_export_20251102_063730.json",
            "sessions_extracted": [s['session_id'] for s in sessions_found],
            "total_qa_pairs": sum(len(s['qa_pairs']) for s in sessions_found)
        },
        "sessions": sessions_found
    }

    output_file = 'sessions_30_37_extracted.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nExtracted data saved to: {output_file}")
else:
    print("\nNo sessions 30-37 found in this file.")
    print("Let me check what session IDs are actually in the file...")

    session_ids = sorted([s['session_id'] for s in data['sessions']])
    print(f"\nSession IDs in file (first 50): {session_ids[:50]}")
    print(f"Session IDs in file (last 50): {session_ids[-50:]}")
