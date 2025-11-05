import json
from pathlib import Path

# Load batch 1
batch_file = Path('refinement_results_validation/batch_001_instruction.json')
with open(batch_file, 'r', encoding='utf-8') as f:
    batch_data = json.load(f)

# Extract first 20 pairs
chunk_1 = batch_data['qa_pairs'][:20]

# Create request for Gemini
request_data = {
    'batch': 'batch_001_chunk_1',
    'pairs': chunk_1,
    'pair_count': len(chunk_1)
}

# Save for reference
with open('refinement_results_validation/batch_001_chunk_1_request.json', 'w', encoding='utf-8') as f:
    json.dump(request_data, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(chunk_1)} pairs for Batch 1 Chunk 1")
print(f"Pair IDs: {chunk_1[0]['pair_id']} to {chunk_1[-1]['pair_id']}")
print(f"Ready to send to Gemini")
