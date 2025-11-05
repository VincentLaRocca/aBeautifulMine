import json
from pathlib import Path

# Load RAG export
rag_file = Path(r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json')

print("Loading RAG export...")
with open(rag_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

sessions = data['sessions']

# Extract first 50 Q&A pairs for testing
test_qa_pairs = []
for session in sessions[:3]:  # First 3 sessions
    for qa in session.get('qa_pairs', [])[:20]:  # Up to 20 from each
        if len(test_qa_pairs) >= 50:
            break
        test_qa_pairs.append({
            'question': qa.get('question', ''),
            'answer': qa.get('answer', ''),
            'topic': session.get('topic', ''),
            'pair_number': qa.get('pair_number', 0)
        })
    if len(test_qa_pairs) >= 50:
        break

print(f"Extracted {len(test_qa_pairs)} Q&A pairs for testing")

# Create simplified refinement prompt
refinement_prompt = """You are refining cryptocurrency trading Q&A pairs for a knowledge base.

For each Q&A pair, analyze and improve:
1. Question clarity
2. Answer completeness and accuracy
3. Crypto-specific examples (2024-2025 context)
4. Technical accuracy

For each pair, return JSON with:
- refined_question: improved question
- refined_answer: enhanced answer with examples
- quality_score: 0-100
- improvements_made: list of changes

Return a JSON array of all refined pairs."""

# Create a single test batch request
test_batch_file = Path('test_refinement_batch.json')

test_request = {
    "prompt": refinement_prompt,
    "qa_pairs": test_qa_pairs[:10]  # Just 10 pairs for initial test
}

with open(test_batch_file, 'w', encoding='utf-8') as f:
    json.dump(test_request, f, indent=2, ensure_ascii=False)

print(f"\nTest batch created: {test_batch_file}")
print(f"Contains {len(test_request['qa_pairs'])} Q&A pairs")
print("\nNext step: Submit this to Gemini to validate the refinement approach")
