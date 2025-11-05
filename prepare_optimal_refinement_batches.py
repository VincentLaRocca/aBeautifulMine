import json
from pathlib import Path
from datetime import datetime

# Load RAG export
rag_file = Path(r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json')

print("Loading RAG export...")
with open(rag_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

sessions = data['sessions']
all_qa_pairs = []

# Extract all Q&A pairs with minimal metadata
print("Extracting Q&A pairs...")
for session_idx, session in enumerate(sessions):
    session_id = session.get('session_id', session_idx)
    topic = session.get('topic', 'Unknown')
    qa_pairs = session.get('qa_pairs', [])

    for qa_idx, qa in enumerate(qa_pairs):
        pair_id = f"s{session_id}_q{qa_idx}"
        all_qa_pairs.append({
            'pair_id': pair_id,
            'question': qa.get('question', ''),
            'answer': qa.get('answer', ''),
            'topic': topic
        })

print(f"Total Q&A pairs extracted: {len(all_qa_pairs)}")

# Optimized batch size for quality refinement
BATCH_SIZE = 100  # Sweet spot for Gemini quality
batches = []
batch_dir = Path('refinement_batches_optimal')
batch_dir.mkdir(exist_ok=True)

for i in range(0, len(all_qa_pairs), BATCH_SIZE):
    batch = all_qa_pairs[i:i + BATCH_SIZE]
    batches.append(batch)

print(f"Created {len(batches)} batches of ~{BATCH_SIZE} pairs each")

# Simplified refinement prompt for batch processing
refinement_prompt = """Refine these cryptocurrency Q&A pairs for a knowledge base.

For each pair:
1. Improve question clarity
2. Enhance answer completeness and technical accuracy
3. Add crypto-specific 2024-2025 examples where relevant
4. Ensure answers are comprehensive (2000-4000 chars for complex topics)

Return JSON array with:
- pair_id: original ID
- refined_question: improved question
- refined_answer: enhanced answer with examples
- quality_score: 0-100
- improvements_made: list of changes"""

# Create batch files
print("\nGenerating batch files...")

batch_metadata = []

for batch_idx, batch in enumerate(batches, 1):
    batch_name = f"refinement_batch_{batch_idx:03d}"

    # Create the content for Gemini
    batch_content = {
        "batch_id": batch_name,
        "instruction": refinement_prompt,
        "qa_pairs": batch
    }

    # Save as JSON for reference
    batch_json_file = batch_dir / f"{batch_name}.json"
    with open(batch_json_file, 'w', encoding='utf-8') as f:
        json.dump(batch_content, f, indent=2, ensure_ascii=False)

    # Create simplified content file for batch ingestion
    content_file = batch_dir / f"{batch_name}_content.txt"
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(f"{refinement_prompt}\n\n")
        f.write(f"BATCH: {batch_name}\n")
        f.write(f"Q&A PAIRS: {len(batch)}\n\n")
        f.write("---\n\n")
        for qa in batch:
            f.write(f"Pair ID: {qa['pair_id']}\n")
            f.write(f"Topic: {qa['topic']}\n")
            f.write(f"Question: {qa['question']}\n")
            f.write(f"Answer: {qa['answer']}\n")
            f.write("\n---\n\n")

    batch_metadata.append({
        'batch_id': batch_name,
        'batch_number': batch_idx,
        'qa_count': len(batch),
        'pair_id_range': f"{batch[0]['pair_id']} to {batch[-1]['pair_id']}",
        'json_file': str(batch_json_file),
        'content_file': str(content_file)
    })

    if batch_idx % 20 == 0:
        print(f"  Created {batch_idx} batches...")

print(f"  Created all {len(batches)} batches")

# Save manifest
manifest_file = batch_dir / 'batch_manifest.json'
manifest = {
    'created_at': datetime.now().isoformat(),
    'total_qa_pairs': len(all_qa_pairs),
    'total_batches': len(batches),
    'batch_size': BATCH_SIZE,
    'batches': batch_metadata,
    'strategy': {
        'batch_size_rationale': 'Optimized for quality: ~100 pairs per batch based on successful test',
        'expected_tokens_per_batch': '~120,000 tokens',
        'estimated_total_cost': 'Batch API 50% discount applies'
    },
    'next_steps': [
        '1. Use Gemini batch API to submit batches',
        '2. Monitor progress',
        '3. Download refined results',
        '4. Consolidate and deduplicate',
        '5. Import to production database'
    ]
}

with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Create a summary script for submission
submission_script = batch_dir / 'submit_batches_guide.md'
with open(submission_script, 'w', encoding='utf-8') as f:
    f.write(f"""# Refinement Batch Submission Guide

## Summary
- **Total Q&A Pairs:** {len(all_qa_pairs):,}
- **Total Batches:** {len(batches)}
- **Batch Size:** ~{BATCH_SIZE} pairs
- **Estimated Tokens:** ~{len(batches) * 120000:,} tokens (~{len(batches) * 60000:,} with 50% discount)

## Batch Processing Strategy

Given the test success (3 pairs → quality scores 92-96), we're using:
- **100 pairs per batch** for optimal quality
- **{len(batches)} total batches** for full dataset
- **Gemini 2.5 Flash** for cost-effective refinement

## Options for Submission

### Option A: Gemini Batch API (Recommended for Scale)
Use the Gemini batch processing MCP tools to submit all batches:
- Lower cost (50% discount)
- Automated processing (~24 hours)
- Best for processing all {len(batches)} batches

### Option B: Sequential Chat API (For Testing)
Process a few batches first to validate:
- Use `mcp__gemini__chat` for first 5-10 batches
- Validate results quality
- Then switch to batch API for remainder

### Option C: Hybrid Approach (Recommended)
1. Process first 10 batches via chat API (validate quality)
2. If quality is good, submit remaining {len(batches) - 10} via batch API
3. Monitor and adjust as needed

## File Structure
Each batch has:
- `refinement_batch_XXX.json` - Structured data
- `refinement_batch_XXX_content.txt` - Human-readable version

## Estimated Timeline
- **Batch API:** ~24 hours for all batches
- **Chat API:** ~2-3 hours per 10 batches (if done sequentially)
- **Recommended:** Mix of both (~2-3 days total)

## Next Command
```python
# For chat API test (process first 5 batches):
# Use mcp__gemini__chat with content from refinement_batch_001.json

# For batch API (full processing):
# Use mcp__gemini__batch_create with prepared content files
```
""")

print(f"\n{'='*80}")
print("OPTIMAL BATCH PREPARATION COMPLETE")
print(f"{'='*80}")
print(f"Total Q&A pairs: {len(all_qa_pairs):,}")
print(f"Total batches: {len(batches)}")
print(f"Batch size: ~{BATCH_SIZE} pairs (optimized for quality)")
print(f"\nEstimated tokens:")
print(f"  Per batch: ~120,000 tokens")
print(f"  Total: ~{len(batches) * 120000:,} tokens")
print(f"  With 50% batch discount: ~{len(batches) * 60000:,} tokens")
print(f"\nFiles created:")
print(f"  - {len(batches)} JSON batch files")
print(f"  - {len(batches)} content text files")
print(f"  - 1 manifest file")
print(f"  - 1 submission guide")
print(f"\nAll files saved to: {batch_dir}/")
print(f"{'='*80}")
