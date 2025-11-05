import json
from datetime import datetime

# Load the RAG export file
print("Loading RAG export file...")
with open('inbox/droid/processed/qa_pairs_rag_export_20251102_063730.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total sessions in file: {data['metadata']['total_sessions']}")

# Target Batch 7 sessions
target_sessions = [26, 27, 28, 29, 38, 39, 40, 41, 42, 43, 44]
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
print(f"Total Q&A pairs: {sum(len(s['qa_pairs']) for s in sessions_found)}")

# Save extracted sessions
output_data = {
    "metadata": {
        "extraction_date": datetime.now().isoformat(),
        "source_file": "qa_pairs_rag_export_20251102_063730.json",
        "batch": "Batch 7",
        "sessions_extracted": sorted([s['session_id'] for s in sessions_found]),
        "total_qa_pairs": sum(len(s['qa_pairs']) for s in sessions_found)
    },
    "sessions": sessions_found
}

output_file = 'batch7_sessions_26-44_extracted.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"\nExtracted data saved to: {output_file}")
print("Ready for integration!")
