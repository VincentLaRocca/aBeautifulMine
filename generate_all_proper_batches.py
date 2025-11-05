import json
from pathlib import Path

print("=" * 80)
print("GENERATING PROPERLY FORMATTED BATCH JSONL FILES")
print("=" * 80)

# Read the RAG export
rag_export_path = Path('inbox/droid/qa_pairs_rag_export_20251102_075728.json')
print(f"\nReading RAG export: {rag_export_path}")

with open(rag_export_path, 'r', encoding='utf-8') as f:
    rag_data = json.load(f)

# Extract all Q&A pairs
all_qa_pairs = []
for session in rag_data['sessions']:
    for qa in session['qa_pairs']:
        all_qa_pairs.append({
            'pair_id': qa['id'],  # Field is 'id' not 'pair_id'
            'question': qa['question'],
            'answer': qa['answer'],
            'topic': qa['metadata'].get('topic', session.get('topic', 'Unknown'))
        })

print(f"Total Q&A pairs: {len(all_qa_pairs)}")

# Read the refinement prompt
prompt_file = Path('refinement_prompt_template.txt')
with open(prompt_file, 'r', encoding='utf-8') as f:
    refinement_prompt = f.read()

print(f"Refinement prompt loaded: {len(refinement_prompt)} chars")

# Create output directory
output_dir = Path('gemini_batch_submissions_proper')
output_dir.mkdir(exist_ok=True)

# Split into batches of 100
BATCH_SIZE = 100
batches = []
for i in range(0, len(all_qa_pairs), BATCH_SIZE):
    batch_qa_pairs = all_qa_pairs[i:i + BATCH_SIZE]
    batches.append(batch_qa_pairs)

print(f"\nTotal batches: {len(batches)}")
print(f"Batch size: {BATCH_SIZE} Q&A pairs")
print(f"Last batch size: {len(batches[-1])} Q&A pairs")

# Generate properly formatted JSONL files
batch_tracking = []

for batch_num, batch_qa_pairs in enumerate(batches, 1):
    # Create the complete prompt with Q&A data
    full_prompt = f"""{refinement_prompt}

BATCH: refinement_batch_{batch_num:03d}
TOTAL Q&A PAIRS: {len(batch_qa_pairs)}

Q&A PAIRS TO REFINE:

{json.dumps(batch_qa_pairs, indent=2, ensure_ascii=False)}"""

    # Create the properly formatted JSONL request (SINGLE LINE!)
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

    # Write to JSONL file (single line, no newline)
    output_file = output_dir / f"batch_{batch_num:03d}_proper.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(jsonl_request, ensure_ascii=False))

    file_size = output_file.stat().st_size

    # Track batch info
    batch_tracking.append({
        'batch_number': batch_num,
        'file_path': str(output_file),
        'qa_count': len(batch_qa_pairs),
        'file_size': file_size,
        'first_pair_id': batch_qa_pairs[0]['pair_id'],
        'last_pair_id': batch_qa_pairs[-1]['pair_id']
    })

    if batch_num % 20 == 0 or batch_num == len(batches):
        print(f"  Batch {batch_num:03d}: {len(batch_qa_pairs)} pairs, {file_size:,} bytes")

# Save batch tracking data
tracking_file = output_dir / 'batch_tracking.json'
with open(tracking_file, 'w', encoding='utf-8') as f:
    json.dump({
        'total_batches': len(batches),
        'total_qa_pairs': len(all_qa_pairs),
        'batch_size': BATCH_SIZE,
        'batches': batch_tracking,
        'format': 'Single JSONL request per file',
        'ready_for_upload': True
    }, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("GENERATION COMPLETE")
print("=" * 80)
print(f"✅ Generated: {len(batches)} properly formatted JSONL files")
print(f"✅ Total Q&A pairs: {len(all_qa_pairs)}")
print(f"✅ Output directory: {output_dir}")
print(f"✅ Tracking file: {tracking_file}")
print("\nFile format:")
print("  - Single line per file")
print("  - One request containing full prompt + all Q&A pairs")
print("  - Ready for Gemini Batch API upload")
print("\nNext steps:")
print("  1. Upload files using upload_file tool")
print("  2. Create batch jobs using batch_create")
print("  3. Monitor with batch_get_status")
