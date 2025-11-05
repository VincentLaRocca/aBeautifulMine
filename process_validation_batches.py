import json
from pathlib import Path
import time

# Setup
batch_dir = Path('refinement_batches_optimal')
results_dir = Path('refinement_results_validation')
results_dir.mkdir(exist_ok=True)

# Load refinement prompt
with open('refinement_prompt_template.txt', 'r', encoding='utf-8') as f:
    refinement_prompt = f.read()

# Simplified version for better results
simplified_prompt = """You are refining cryptocurrency trading Q&A pairs for a knowledge base.

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

Process ALL pairs in the batch and return the complete JSON array."""

print("="*80)
print("VALIDATION BATCH PROCESSING")
print("="*80)

# Prepare batch information
batches_to_process = []
for i in range(1, 11):  # First 10 batches
    batch_file = batch_dir / f"refinement_batch_{i:03d}.json"
    if batch_file.exists():
        batches_to_process.append({
            'number': i,
            'file': batch_file,
            'id': f"refinement_batch_{i:03d}"
        })

print(f"\nBatches to process: {len(batches_to_process)}")
print(f"Expected Q&A pairs: ~{len(batches_to_process) * 100}")

# Create processing manifest
processing_manifest = {
    'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
    'total_batches': len(batches_to_process),
    'batches': [],
    'summary': {
        'total_qa_pairs': 0,
        'successful_batches': 0,
        'failed_batches': 0,
        'total_processing_time': 0
    }
}

print("\nProcessing batches via Gemini chat API...")
print("Note: This script prepares the data. Use Gemini MCP tools to actually process.\n")

# Generate processing instructions for each batch
for batch_info in batches_to_process:
    with open(batch_info['file'], 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    qa_pairs = batch_data['qa_pairs']

    # Create a compact version for processing
    compact_qa = []
    for qa in qa_pairs:
        compact_qa.append({
            'pair_id': qa['pair_id'],
            'question': qa['question'],
            'answer': qa['answer'],
            'topic': qa['topic']
        })

    # Save processing instructions
    instruction_file = results_dir / f"batch_{batch_info['number']:03d}_instruction.json"
    instruction = {
        'batch_number': batch_info['number'],
        'batch_id': batch_info['id'],
        'qa_count': len(compact_qa),
        'prompt': simplified_prompt,
        'qa_pairs': compact_qa,
        'mcp_command': 'Use mcp__gemini__chat with this prompt and qa_pairs',
        'expected_output': f"batch_{batch_info['number']:03d}_refined.json"
    }

    with open(instruction_file, 'w', encoding='utf-8') as f:
        json.dump(instruction, f, indent=2, ensure_ascii=False)

    processing_manifest['batches'].append({
        'batch_number': batch_info['number'],
        'batch_id': batch_info['id'],
        'qa_count': len(compact_qa),
        'instruction_file': str(instruction_file),
        'status': 'ready_to_process'
    })

    processing_manifest['summary']['total_qa_pairs'] += len(compact_qa)

    print(f"  Prepared batch {batch_info['number']}: {len(compact_qa)} Q&A pairs")

# Save manifest
manifest_file = results_dir / 'processing_manifest.json'
with open(manifest_file, 'w', encoding='utf-8') as f:
    json.dump(processing_manifest, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print("PREPARATION COMPLETE")
print(f"{'='*80}")
print(f"Total batches prepared: {len(batches_to_process)}")
print(f"Total Q&A pairs: {processing_manifest['summary']['total_qa_pairs']}")
print(f"\nInstruction files saved to: {results_dir}/")
print(f"Processing manifest: {manifest_file}")
print(f"\nNext steps:")
print(f"1. Use Gemini MCP chat tool to process each batch")
print(f"2. Save results as batch_XXX_refined.json")
print(f"3. Run quality analysis on results")
print(f"{'='*80}")
