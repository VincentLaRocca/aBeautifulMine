import json
from pathlib import Path
from datetime import datetime

# Directories
batch_dir = Path('refinement_batches_optimal')
output_dir = Path('gemini_batch_submissions')
output_dir.mkdir(exist_ok=True)

# Refined prompt based on successful test
refinement_prompt = """You are refining cryptocurrency trading Q&A pairs for a knowledge base.

For each Q&A pair, analyze and improve:
1. Question clarity and specificity
2. Answer completeness and technical accuracy
3. Add crypto-specific 2024-2025 examples where relevant
4. Ensure comprehensive answers (2000-4000 chars for complex topics)

Return a JSON array where each object has:
{
  "pair_id": "original pair ID",
  "refined_question": "improved question text",
  "refined_answer": "enhanced answer with 2024-2025 examples and formulas",
  "quality_score": 85,
  "improvements_made": ["list of specific improvements"]
}

Process ALL Q&A pairs in this batch and return the complete JSON array."""

print("="*80)
print("PREPARING BATCHES FOR GEMINI BATCH API")
print("="*80)

# Track all batches
batch_submissions = []
total_qa_pairs = 0

# Process each batch file
for batch_num in range(1, 197):  # 196 batches
    batch_file = batch_dir / f"refinement_batch_{batch_num:03d}.json"

    if not batch_file.exists():
        print(f"Warning: {batch_file} not found, skipping")
        continue

    # Load batch data
    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    qa_pairs = batch_data['qa_pairs']
    total_qa_pairs += len(qa_pairs)

    # Create the content for this batch
    batch_content = f"{refinement_prompt}\n\n"
    batch_content += f"BATCH: refinement_batch_{batch_num:03d}\n"
    batch_content += f"TOTAL Q&A PAIRS: {len(qa_pairs)}\n\n"
    batch_content += "Q&A PAIRS TO REFINE:\n\n"
    batch_content += json.dumps(qa_pairs, indent=2, ensure_ascii=False)
    batch_content += f"\n\nReturn ONLY the JSON array with all {len(qa_pairs)} refined pairs."

    # Save content file for this batch
    content_file = output_dir / f"batch_{batch_num:03d}_content.txt"
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(batch_content)

    # Create metadata for tracking
    batch_submissions.append({
        'batch_number': batch_num,
        'batch_id': f"refinement_batch_{batch_num:03d}",
        'qa_count': len(qa_pairs),
        'content_file': str(content_file),
        'status': 'ready_for_submission',
        'estimated_tokens': len(qa_pairs) * 1200  # ~1200 tokens per Q&A pair
    })

    if batch_num % 20 == 0:
        print(f"  Prepared {batch_num}/196 batches...")

print(f"  Prepared all 196 batches")

# Create submission manifest
manifest = {
    'created_at': datetime.now().isoformat(),
    'total_batches': len(batch_submissions),
    'total_qa_pairs': total_qa_pairs,
    'batches': batch_submissions,
    'submission_strategy': {
        'method': 'Gemini Batch API via MCP tools',
        'model': 'gemini-2.5-flash',
        'estimated_total_tokens': sum(b['estimated_tokens'] for b in batch_submissions),
        'estimated_cost_with_discount': '$65-90 (50% batch discount)',
        'expected_completion': '24-48 hours'
    },
    'next_steps': [
        '1. Use mcp__gemini__batch_ingest_content for each batch',
        '2. Submit batches using mcp__gemini__batch_create',
        '3. Monitor with mcp__gemini__batch_get_status',
        '4. Download results with mcp__gemini__batch_download_results'
    ]
}

manifest_file = output_dir / 'submission_manifest.json'
with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Create submission script guide
guide_file = output_dir / 'SUBMISSION_GUIDE.md'
with open(guide_file, 'w', encoding='utf-8') as f:
    f.write(f"""# Gemini Batch API Submission Guide

## Summary
- **Total Batches:** {len(batch_submissions)}
- **Total Q&A Pairs:** {total_qa_pairs:,}
- **Estimated Tokens:** ~{sum(b['estimated_tokens'] for b in batch_submissions):,}
- **Estimated Cost:** $65-90 (with 50% batch discount)
- **Expected Time:** 24-48 hours

## Submission Strategy

We'll submit batches in groups of 10-20 for easier monitoring.

### Method 1: Using batch_ingest_content + batch_create

For each batch:
```python
# 1. Ingest content (converts to proper JSONL format)
result = mcp__gemini__batch_ingest_content(
    inputFile='gemini_batch_submissions/batch_001_content.txt'
)

# 2. Create batch job
batch_job = mcp__gemini__batch_create(
    inputFileUri=result['outputFile'],  # From step 1
    model='gemini-2.5-flash',
    displayName='refinement_batch_001'
)
```

### Method 2: Using batch_process (All-in-one)

This handles everything automatically:
```python
result = mcp__gemini__batch_process(
    inputFile='gemini_batch_submissions/batch_001_content.txt',
    model='gemini-2.5-flash',
    pollIntervalSeconds=60
)
```

## Recommended Approach

**Submit in groups of 20 batches** to monitor progress:

### Group 1: Batches 1-20 (2,000 Q&A pairs)
### Group 2: Batches 21-40 (2,000 Q&A pairs)
### Group 3: Batches 41-60 (2,000 Q&A pairs)
...and so on

This allows us to:
- Monitor initial batch quality
- Adjust if needed
- Track progress systematically

## Monitoring

After submission, track each batch:
```python
status = mcp__gemini__batch_get_status(
    batchName='batch_job_name_from_create',
    autoPoll=True,
    pollIntervalSeconds=300  # Check every 5 minutes
)
```

## File Structure

Each batch has:
- `batch_XXX_content.txt` - Ready for submission
- Content includes:
  - Refinement prompt
  - 100 Q&A pairs to refine
  - Instructions for output format

## Next Actions

1. Review this guide
2. Start with first 20 batches
3. Monitor progress
4. Submit remaining batches once confident
5. Download results as they complete

---

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Ready for Submission:** All 196 batches prepared
""")

print(f"\n{'='*80}")
print("PREPARATION COMPLETE")
print(f"{'='*80}")
print(f"Total batches prepared: {len(batch_submissions)}")
print(f"Total Q&A pairs: {total_qa_pairs:,}")
print(f"Estimated tokens: ~{sum(b['estimated_tokens'] for b in batch_submissions):,}")
print(f"Estimated cost: $65-90 (with 50% batch discount)")
print(f"\nFiles created:")
print(f"  - {len(batch_submissions)} content files")
print(f"  - 1 submission manifest")
print(f"  - 1 submission guide")
print(f"\nAll files in: {output_dir}/")
print(f"\nNext: Use Gemini MCP tools to submit batches")
print(f"{'='*80}")
