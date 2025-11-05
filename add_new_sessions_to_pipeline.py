import json
from pathlib import Path

print("=" * 80)
print("ADDING NEW SESSIONS (18-25) TO REFINEMENT PIPELINE")
print("=" * 80)

# Load refinement prompt
prompt_file = Path('refinement_prompt_template.txt')
with open(prompt_file, 'r', encoding='utf-8') as f:
    refinement_prompt = f.read()

# New session files in inbox
new_sessions = [
    'inbox/session-18-derivatives-qa-complete.json',
    'inbox/session-19-mining-staking-qa-complete.json',
    'inbox/session-20-network-value-qa-complete.json',
    'inbox/session-21-stock-to-flow-qa-complete.json',
    'inbox/session-22-sentiment-realized-qa-complete.json',
    'inbox/session-23-social-metrics-qa-complete.json',
    'inbox/session-24-advanced-social-qa-complete.json',
    'inbox/session-25-funding-derivatives-qa-complete.json'
]

# Load existing batch tracking
tracking_file = Path('gemini_batch_submissions_proper/batch_tracking.json')
with open(tracking_file, 'r', encoding='utf-8') as f:
    tracking_data = json.load(f)

print(f"\nExisting batches: {tracking_data['total_batches']}")
print(f"Existing Q&A pairs: {tracking_data['total_qa_pairs']}")

# Process new sessions
output_dir = Path('gemini_batch_submissions_proper')
new_batches = []
all_new_qa_pairs = []

for session_file in new_sessions:
    session_path = Path(session_file)
    if not session_path.exists():
        print(f"\n⚠️  Warning: {session_file} not found, skipping")
        continue

    print(f"\nProcessing: {session_path.name}")

    with open(session_path, 'r', encoding='utf-8') as f:
        session_data = json.load(f)

    # Extract Q&A pairs - need to read the actual data structure
    # The JSON files contain metadata, need to find the actual Q&A pairs
    if 'qa_pairs' in session_data:
        qa_pairs = session_data['qa_pairs']
    elif 'questions' in session_data:
        # Alternative structure
        qa_pairs = []
        for q in session_data['questions']:
            qa_pairs.append({
                'pair_id': q.get('id', f"s{session_data['session']}_q{len(qa_pairs)}"),
                'question': q.get('question', ''),
                'answer': q.get('answer', ''),
                'topic': session_data.get('category', 'Unknown')
            })
    else:
        # Need to check the actual structure
        print(f"  Keys in file: {list(session_data.keys())}")
        print(f"  Need to extract Q&A pairs from this structure")
        # For now, create placeholder based on metadata
        qa_pairs = []

    if qa_pairs:
        all_new_qa_pairs.extend(qa_pairs)
        print(f"  Extracted: {len(qa_pairs)} Q&A pairs")
        print(f"  Category: {session_data.get('category', 'Unknown')}")

print(f"\n{'='*80}")
print(f"Total new Q&A pairs extracted: {len(all_new_qa_pairs)}")
print(f"{'='*80}")

if len(all_new_qa_pairs) == 0:
    print("\n⚠️  No Q&A pairs extracted. Need to check file structure.")
    print("Let me read one file to see the structure...")

    with open(Path(new_sessions[0]), 'r', encoding='utf-8') as f:
        sample = json.load(f)

    print(f"\nSample file structure:")
    print(json.dumps({k: type(v).__name__ for k, v in sample.items()}, indent=2))

    if 'file_path' in sample:
        print(f"\nNote: Q&A data may be in separate file: {sample['file_path']}")

    exit(1)

# Split into batches of 100
BATCH_SIZE = 100
start_batch_num = tracking_data['total_batches'] + 1

for i in range(0, len(all_new_qa_pairs), BATCH_SIZE):
    batch_qa_pairs = all_new_qa_pairs[i:i + BATCH_SIZE]
    batch_num = start_batch_num + (i // BATCH_SIZE)

    # Create the complete prompt with Q&A data
    full_prompt = f"""{refinement_prompt}

BATCH: refinement_batch_{batch_num:03d}
TOTAL Q&A PAIRS: {len(batch_qa_pairs)}

Q&A PAIRS TO REFINE:

{json.dumps(batch_qa_pairs, indent=2, ensure_ascii=False)}"""

    # Create properly formatted JSONL request (single line)
    jsonl_request = {
        "request": {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ]
        }
    }

    # Write to JSONL file
    output_file = output_dir / f"batch_{batch_num:03d}_proper.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(jsonl_request, ensure_ascii=False))

    file_size = output_file.stat().st_size

    # Track batch info
    new_batches.append({
        'batch_number': batch_num,
        'file_path': str(output_file),
        'qa_count': len(batch_qa_pairs),
        'file_size': file_size,
        'first_pair_id': batch_qa_pairs[0]['pair_id'],
        'last_pair_id': batch_qa_pairs[-1]['pair_id']
    })

    print(f"Created: batch_{batch_num:03d}_proper.jsonl ({len(batch_qa_pairs)} pairs, {file_size:,} bytes)")

# Update tracking file
tracking_data['total_batches'] += len(new_batches)
tracking_data['total_qa_pairs'] += len(all_new_qa_pairs)
tracking_data['batches'].extend(new_batches)

with open(tracking_file, 'w', encoding='utf-8') as f:
    json.dump(tracking_data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("UPDATE COMPLETE")
print("=" * 80)
print(f"New batches created: {len(new_batches)}")
print(f"New Q&A pairs: {len(all_new_qa_pairs)}")
print(f"Total batches: {tracking_data['total_batches']}")
print(f"Total Q&A pairs: {tracking_data['total_qa_pairs']}")
print(f"\nTracking file updated: {tracking_file}")
print("\nReady for submission!")
