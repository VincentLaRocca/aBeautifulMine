import json
from collections import defaultdict
from pathlib import Path

# Load the RAG export
rag_file = Path(r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json')

print("Loading RAG export...")
with open(rag_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

metadata = data['metadata']
sessions = data['sessions']

print("="*80)
print("REFINEMENT PIPELINE ANALYSIS")
print("="*80)

print(f"\nMetadata:")
print(f"  Total Sessions: {metadata['total_sessions']}")
print(f"  Total Q&A Pairs: {metadata['total_qa_pairs']}")
print(f"  Average Answer Length: {metadata['average_answer_length']:.1f} chars")

# Analyze sessions
print(f"\n{'='*80}")
print("SESSION BREAKDOWN")
print(f"{'='*80}")

total_qa = 0
session_sizes = []
topics_by_category = defaultdict(list)

for session in sessions:
    qa_count = len(session.get('qa_pairs', []))
    total_qa += qa_count
    session_sizes.append(qa_count)

    topic = session.get('topic', 'Unknown')
    # Try to categorize
    if 'technical' in topic.lower() or 'indicator' in topic.lower():
        category = 'Technical Indicators'
    elif 'derivative' in topic.lower() or 'futures' in topic.lower() or 'options' in topic.lower():
        category = 'Derivatives'
    elif 'on-chain' in topic.lower() or 'blockchain' in topic.lower() or 'mining' in topic.lower():
        category = 'On-Chain Metrics'
    elif 'defi' in topic.lower() or 'liquidity' in topic.lower() or 'yield' in topic.lower():
        category = 'DeFi'
    elif 'sentiment' in topic.lower() or 'psychology' in topic.lower() or 'trading' in topic.lower():
        category = 'Trading Psychology'
    elif 'security' in topic.lower() or 'wallet' in topic.lower() or 'aml' in topic.lower():
        category = 'Security'
    elif 'regulatory' in topic.lower() or 'compliance' in topic.lower() or 'legal' in topic.lower():
        category = 'Regulatory'
    elif 'nft' in topic.lower() or 'metaverse' in topic.lower() or 'gaming' in topic.lower():
        category = 'NFT/Gaming'
    else:
        category = 'Other'

    topics_by_category[category].append((topic, qa_count))

print(f"Total Q&A pairs across all sessions: {total_qa}")
print(f"Average Q&A pairs per session: {sum(session_sizes) / len(session_sizes):.1f}")
print(f"Min session size: {min(session_sizes)} pairs")
print(f"Max session size: {max(session_sizes)} pairs")

print(f"\n{'='*80}")
print("Q&A PAIRS BY CATEGORY")
print(f"{'='*80}")

for category in sorted(topics_by_category.keys()):
    topics = topics_by_category[category]
    total_in_category = sum(count for _, count in topics)
    print(f"\n{category}: {total_in_category} pairs ({len(topics)} sessions)")
    # Show top 5 topics in this category
    sorted_topics = sorted(topics, key=lambda x: x[1], reverse=True)[:5]
    for topic, count in sorted_topics:
        topic_short = topic[:60] + "..." if len(topic) > 60 else topic
        print(f"  {count:4d} - {topic_short}")

# Analyze for batch processing strategy
print(f"\n{'='*80}")
print("BATCH PROCESSING STRATEGY")
print(f"{'='*80}")

# Calculate optimal batch sizes
# Gemini batch API can handle large files, but we want manageable chunks
# Let's aim for batches of ~500-1000 Q&A pairs each

batch_size_target = 500
num_batches = (total_qa + batch_size_target - 1) // batch_size_target

print(f"\nRecommended approach:")
print(f"  Target batch size: {batch_size_target} Q&A pairs")
print(f"  Estimated batches: {num_batches}")
print(f"  Processing strategy: By category or session groups")

# Estimate tokens
# Average answer is ~3228 chars, questions much shorter
# Rough estimate: 1 Q&A pair = ~4000 chars = ~1000 tokens input + output
# So ~500 Q&A pairs = ~500,000 tokens

estimated_tokens_per_batch = batch_size_target * 1000
estimated_total_tokens = total_qa * 1000

print(f"\nEstimated token usage:")
print(f"  Per batch: ~{estimated_tokens_per_batch:,} tokens")
print(f"  Total: ~{estimated_total_tokens:,} tokens")
print(f"  At 50% batch discount: ~{estimated_total_tokens // 2:,} tokens cost")

print(f"\n{'='*80}")
print("REFINEMENT TASKS")
print(f"{'='*80}")
print("""
For each Q&A pair, Gemini will:
1. Analyze for duplicate/similar content
2. Enhance answer quality and clarity
3. Ensure crypto-specific accuracy (2024-2025 context)
4. Standardize formatting
5. Add metadata tags for better RAG retrieval
6. Flag low-quality or outdated content
7. Suggest merged answers for duplicates

Output format:
{
  "original_qa_id": "...",
  "refined_question": "...",
  "refined_answer": "...",
  "quality_score": 0-100,
  "duplicate_of": "qa_id or null",
  "enhancement_notes": "...",
  "rag_tags": ["tag1", "tag2", ...],
  "confidence": 0-100
}
""")

print(f"\n{'='*80}")
print("NEXT STEPS")
print(f"{'='*80}")
print("""
1. Create refinement prompt template
2. Batch sessions into ~40 batches of 500 pairs each
3. Generate JSONL files for Gemini batch API
4. Submit batch jobs (can run concurrently)
5. Monitor progress (~24 hours typical)
6. Download and process refined results
7. Deduplicate based on Gemini's analysis
8. Import to production database
""")

# Save category breakdown for later use
category_summary = {
    cat: {
        'total_pairs': sum(count for _, count in topics),
        'session_count': len(topics),
        'topics': topics
    }
    for cat, topics in topics_by_category.items()
}

with open('refinement_category_summary.json', 'w', encoding='utf-8') as f:
    json.dump(category_summary, f, indent=2, ensure_ascii=False)

print(f"\nCategory summary saved to: refinement_category_summary.json")
print("="*80)
