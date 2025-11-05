import json
from pathlib import Path
from datetime import datetime

# Load RAG export
rag_file = Path(r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json')

print("Loading RAG export...")
with open(rag_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load refinement prompt
with open('refinement_prompt_template.txt', 'r', encoding='utf-8') as f:
    refinement_prompt = f.read()

sessions = data['sessions']
all_qa_pairs = []

# Extract all Q&A pairs with metadata
print("Extracting Q&A pairs...")
for session_idx, session in enumerate(sessions):
    session_id = session.get('session_id', session_idx)
    topic = session.get('topic', 'Unknown')
    qa_pairs = session.get('qa_pairs', [])

    for qa_idx, qa in enumerate(qa_pairs):
        pair_id = f"s{session_id}_q{qa_idx}"
        all_qa_pairs.append({
            'pair_id': pair_id,
            'session_id': session_id,
            'topic': topic,
            'question': qa.get('question', ''),
            'answer': qa.get('answer', ''),
            'original_metadata': {
                'pair_number': qa.get('pair_number'),
                'indicator': qa.get('indicator'),
                'category': qa.get('category'),
                'created_date': qa.get('created_date')
            }
        })

print(f"Total Q&A pairs extracted: {len(all_qa_pairs)}")

# Split into batches
BATCH_SIZE = 500
batches = []
batch_dir = Path('refinement_batches')
batch_dir.mkdir(exist_ok=True)

for i in range(0, len(all_qa_pairs), BATCH_SIZE):
    batch = all_qa_pairs[i:i + BATCH_SIZE]
    batches.append(batch)

print(f"Created {len(batches)} batches of ~{BATCH_SIZE} pairs each")

# Create batch files for Gemini
print("\nGenerating batch request files...")

batch_metadata = []

for batch_idx, batch in enumerate(batches, 1):
    batch_name = f"batch_{batch_idx:03d}"

    # Create a structured request for this batch
    # The batch will include the refinement prompt and the Q&A pairs to process

    batch_request = {
        "batch_id": batch_name,
        "batch_number": batch_idx,
        "total_batches": len(batches),
        "qa_count": len(batch),
        "instruction": refinement_prompt,
        "qa_pairs": batch
    }

    # Save batch as JSON for reference
    batch_json_file = batch_dir / f"{batch_name}_data.json"
    with open(batch_json_file, 'w', encoding='utf-8') as f:
        json.dump(batch_request, f, indent=2, ensure_ascii=False)

    # Create JSONL format for Gemini batch API
    # Each line in JSONL represents one request
    # For refinement, we'll create one request per batch that processes all QA pairs in that batch

    jsonl_file = batch_dir / f"{batch_name}_requests.jsonl"

    # Create the Gemini API request
    gemini_request = {
        "request": batch_name,
        "key": f"refinement_{batch_name}",
        "request": {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"{refinement_prompt}\n\n---\n\nBATCH: {batch_name}\nTOTAL Q&A PAIRS: {len(batch)}\n\n---\n\nQ&A PAIRS TO REFINE:\n\n{json.dumps(batch, indent=2, ensure_ascii=False)}\n\n---\n\nPlease process all {len(batch)} Q&A pairs and return a JSON array with refined versions following the output format specified in the instructions."
                        }
                    ]
                }
            ]
        }
    }

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(gemini_request) + '\n')

    batch_metadata.append({
        'batch_id': batch_name,
        'batch_number': batch_idx,
        'qa_count': len(batch),
        'pair_id_range': f"{batch[0]['pair_id']} to {batch[-1]['pair_id']}",
        'topics_in_batch': list(set(qa['topic'] for qa in batch)),
        'json_file': str(batch_json_file),
        'jsonl_file': str(jsonl_file)
    })

    print(f"  Created {batch_name}: {len(batch)} Q&A pairs")

# Save batch manifest
manifest_file = batch_dir / 'batch_manifest.json'
manifest = {
    'created_at': datetime.now().isoformat(),
    'total_qa_pairs': len(all_qa_pairs),
    'total_batches': len(batches),
    'batch_size': BATCH_SIZE,
    'batches': batch_metadata,
    'refinement_prompt_file': 'refinement_prompt_template.txt',
    'instructions': {
        'next_steps': [
            '1. Review batch files in refinement_batches/ directory',
            '2. Upload JSONL files to Gemini using batch_upload or upload_file',
            '3. Submit batch jobs using batch_create',
            '4. Monitor progress using batch_get_status',
            '5. Download results using batch_download_results',
            '6. Process and deduplicate refined Q&A pairs',
            '7. Import to production database'
        ],
        'estimated_processing_time': '~24 hours per batch',
        'estimated_cost': 'Batch API is 50% cheaper than standard API'
    }
}

with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print("BATCH PREPARATION COMPLETE")
print(f"{'='*80}")
print(f"Total Q&A pairs: {len(all_qa_pairs)}")
print(f"Total batches: {len(batches)}")
print(f"Batch size: ~{BATCH_SIZE} pairs")
print(f"\nFiles created:")
print(f"  - {len(batches)} JSON data files (for reference)")
print(f"  - {len(batches)} JSONL request files (for Gemini API)")
print(f"  - 1 manifest file: {manifest_file}")
print(f"\nAll files saved to: {batch_dir}/")
print(f"{'='*80}")
