import json
from pathlib import Path

# Read the refinement prompt template
with open('refinement_prompt_template.txt', 'r', encoding='utf-8') as f:
    refinement_prompt = f.read()

# Read the batch manifest
with open('gemini_batch_submissions/batch_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

print("=" * 80)
print("CREATING PROPERLY FORMATTED BATCH JSONL FILES")
print("=" * 80)

output_dir = Path('gemini_batch_submissions_proper')
output_dir.mkdir(exist_ok=True)

for i, batch_info in enumerate(manifest['batches'], 1):
    batch_num = batch_info['batch_number']
    json_file = Path(batch_info['json_file'])

    print(f"\nBatch {batch_num}/{len(manifest['batches'])}: {json_file.name}")

    # Read the Q&A pairs for this batch
    with open(json_file, 'r', encoding='utf-8') as f:
        qa_pairs = json.load(f)

    print(f"  Q&A pairs: {len(qa_pairs)}")

    # Create the complete prompt with Q&A data
    full_prompt = f"""{refinement_prompt}

BATCH: refinement_batch_{batch_num:03d}
TOTAL Q&A PAIRS: {len(qa_pairs)}

Q&A PAIRS TO REFINE:

{json.dumps(qa_pairs, indent=2, ensure_ascii=False)}"""

    # Create the properly formatted JSONL request
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

    # Write to JSONL file (single line)
    output_file = output_dir / f"batch_{batch_num:03d}_proper.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(jsonl_request, ensure_ascii=False))
        # No newline at end - single line file

    print(f"  ✅ Created: {output_file.name}")
    print(f"  File size: {output_file.stat().st_size:,} bytes")

print("\n" + "=" * 80)
print("GENERATION COMPLETE")
print("=" * 80)
print(f"Total batches created: {len(manifest['batches'])}")
print(f"Output directory: {output_dir}")
print("\nNext steps:")
print("1. Verify test batch succeeded")
print("2. Upload these files to Gemini")
print("3. Create batch jobs for all 196 batches")
