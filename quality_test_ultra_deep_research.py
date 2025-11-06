import json
import re
from collections import Counter
import statistics

print("="*70)
print("ULTRA DEEP RESEARCH DATA - QUALITY TESTING")
print("="*70)

# Load the data
print("\nLoading data...")
with open('C:/Users/vlaro/dreamteam/Gemini/shared/ACTIVE-DATA/ultra_deep_research_ready.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qa_pairs = data['qa_pairs']
metadata = data['metadata']

print(f"Loaded: {len(qa_pairs):,} Q&A pairs")
print(f"Metadata: {metadata}")

# Quality test results
quality_report = {
    'total_pairs': len(qa_pairs),
    'passed': 0,
    'warnings': [],
    'errors': [],
    'statistics': {}
}

print("\n" + "="*70)
print("QUALITY TEST 1: STRUCTURE VALIDATION")
print("="*70)

required_fields = ['question', 'answer', 'topic', 'indicator']
optional_fields = ['pair_number', 'created_date', 'category', 'session', 'source', 'quality_score', 'raw_data']

structure_issues = 0
for idx, pair in enumerate(qa_pairs[:100], 1):  # Test first 100
    missing = [field for field in required_fields if field not in pair or not pair[field]]
    if missing:
        structure_issues += 1
        quality_report['errors'].append(f"Pair {idx}: Missing required fields: {missing}")

if structure_issues == 0:
    print("✅ PASS: All sampled pairs have required fields")
else:
    print(f"❌ FAIL: {structure_issues} pairs missing required fields")

print("\n" + "="*70)
print("QUALITY TEST 2: CONTENT VALIDATION")
print("="*70)

# Test questions
empty_questions = 0
short_questions = 0
question_lengths = []

# Test answers
empty_answers = 0
short_answers = 0
answer_lengths = []

for idx, pair in enumerate(qa_pairs, 1):
    q = pair.get('question', '').strip()
    a = pair.get('answer', '').strip()

    # Question validation
    question_lengths.append(len(q))
    if not q:
        empty_questions += 1
        quality_report['errors'].append(f"Pair {idx}: Empty question")
    elif len(q) < 10:
        short_questions += 1
        quality_report['warnings'].append(f"Pair {idx}: Very short question ({len(q)} chars)")

    # Answer validation
    answer_lengths.append(len(a))
    if not a:
        empty_answers += 1
        quality_report['errors'].append(f"Pair {idx}: Empty answer")
    elif len(a) < 50:
        short_answers += 1
        quality_report['warnings'].append(f"Pair {idx}: Short answer ({len(a)} chars)")

print(f"\nQuestions:")
print(f"  Empty: {empty_questions}")
print(f"  Too short (<10 chars): {short_questions}")
print(f"  Average length: {statistics.mean(question_lengths):.1f} chars")
print(f"  Median length: {statistics.median(question_lengths):.1f} chars")

print(f"\nAnswers:")
print(f"  Empty: {empty_answers}")
print(f"  Too short (<50 chars): {short_answers}")
print(f"  Average length: {statistics.mean(answer_lengths):.1f} chars")
print(f"  Median length: {statistics.median(answer_lengths):.1f} chars")
print(f"  Min length: {min(answer_lengths)} chars")
print(f"  Max length: {max(answer_lengths)} chars")

if empty_questions == 0 and empty_answers == 0:
    print("\n✅ PASS: No empty questions or answers")
else:
    print(f"\n❌ FAIL: {empty_questions} empty questions, {empty_answers} empty answers")

quality_report['statistics']['question_length'] = {
    'average': statistics.mean(question_lengths),
    'median': statistics.median(question_lengths),
    'min': min(question_lengths),
    'max': max(question_lengths)
}

quality_report['statistics']['answer_length'] = {
    'average': statistics.mean(answer_lengths),
    'median': statistics.median(answer_lengths),
    'min': min(answer_lengths),
    'max': max(answer_lengths)
}

print("\n" + "="*70)
print("QUALITY TEST 3: DUPLICATE DETECTION")
print("="*70)

# Check for duplicate questions
questions = [pair.get('question', '').strip().lower() for pair in qa_pairs]
question_counts = Counter(questions)
duplicates = {q: count for q, count in question_counts.items() if count > 1 and q}

print(f"Unique questions: {len([q for q in questions if q]):,}")
print(f"Duplicate questions: {len(duplicates)}")

if len(duplicates) > 0:
    print(f"\nTop 5 duplicates:")
    for q, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  ({count}x) {q[:80]}...")
    quality_report['warnings'].append(f"{len(duplicates)} duplicate questions found")
else:
    print("✅ PASS: No duplicate questions")

print("\n" + "="*70)
print("QUALITY TEST 4: TOPIC/INDICATOR DISTRIBUTION")
print("="*70)

topics = [pair.get('topic', 'Unknown') for pair in qa_pairs]
indicators = [pair.get('indicator', 'Unknown') for pair in qa_pairs]
categories = [pair.get('category', 'Unknown') for pair in qa_pairs]

topic_counts = Counter(topics)
indicator_counts = Counter(indicators)
category_counts = Counter(categories)

print(f"\nUnique topics: {len(topic_counts)}")
print(f"Unique indicators: {len(indicator_counts)}")
print(f"Unique categories: {len(category_counts)}")

print(f"\nTop 10 topics by pair count:")
for topic, count in topic_counts.most_common(10):
    print(f"  {topic}: {count} pairs")

print(f"\nTop 10 indicators by pair count:")
for indicator, count in indicator_counts.most_common(10):
    print(f"  {indicator}: {count} pairs")

quality_report['statistics']['distribution'] = {
    'unique_topics': len(topic_counts),
    'unique_indicators': len(indicator_counts),
    'unique_categories': len(category_counts)
}

print("\n" + "="*70)
print("QUALITY TEST 5: CONTENT QUALITY CHECKS")
print("="*70)

# Check for common quality indicators
has_examples = 0
has_formulas = 0
has_numbers = 0
has_crypto_terms = 0

crypto_terms = ['bitcoin', 'btc', 'ethereum', 'eth', 'blockchain', 'crypto', 'trading', 'market', 'indicator']

for pair in qa_pairs:
    answer = pair.get('answer', '').lower()

    if 'example' in answer or 'for instance' in answer or 'e.g.' in answer:
        has_examples += 1

    if '=' in answer or 'formula' in answer or '×' in answer or '÷' in answer:
        has_formulas += 1

    if re.search(r'\d+', answer):
        has_numbers += 1

    if any(term in answer for term in crypto_terms):
        has_crypto_terms += 1

print(f"\nContent indicators:")
print(f"  Pairs with examples: {has_examples} ({has_examples/len(qa_pairs)*100:.1f}%)")
print(f"  Pairs with formulas: {has_formulas} ({has_formulas/len(qa_pairs)*100:.1f}%)")
print(f"  Pairs with numbers: {has_numbers} ({has_numbers/len(qa_pairs)*100:.1f}%)")
print(f"  Pairs with crypto terms: {has_crypto_terms} ({has_crypto_terms/len(qa_pairs)*100:.1f}%)")

if has_crypto_terms / len(qa_pairs) > 0.8:
    print("\n✅ PASS: High crypto-specific content (>80%)")
else:
    print(f"\n⚠️ WARNING: Lower crypto-specific content ({has_crypto_terms/len(qa_pairs)*100:.1f}%)")

quality_report['statistics']['content_quality'] = {
    'has_examples_pct': has_examples/len(qa_pairs)*100,
    'has_formulas_pct': has_formulas/len(qa_pairs)*100,
    'has_numbers_pct': has_numbers/len(qa_pairs)*100,
    'has_crypto_terms_pct': has_crypto_terms/len(qa_pairs)*100
}

print("\n" + "="*70)
print("QUALITY TEST 6: SESSION/SOURCE VALIDATION")
print("="*70)

sessions = [pair.get('session', 'Unknown') for pair in qa_pairs if pair.get('session')]
sources = [pair.get('source', 'Unknown') for pair in qa_pairs if pair.get('source')]

session_counts = Counter(sessions)
source_counts = Counter(sources)

print(f"\nSessions with data: {len(session_counts)}")
print(f"Sources: {len(source_counts)}")

if len(session_counts) > 0:
    print(f"\nSession distribution:")
    print(f"  Total sessions: {len(session_counts)}")
    print(f"  Avg pairs per session: {len(qa_pairs) / len(session_counts):.1f}")
    print(f"  Min pairs: {min(session_counts.values())}")
    print(f"  Max pairs: {max(session_counts.values())}")

quality_report['statistics']['sessions'] = {
    'total_sessions': len(session_counts),
    'avg_pairs_per_session': len(qa_pairs) / len(session_counts) if session_counts else 0
}

print("\n" + "="*70)
print("QUALITY TEST 7: SAMPLE INSPECTION")
print("="*70)

# Show 3 random samples
import random
samples = random.sample(qa_pairs, min(3, len(qa_pairs)))

for idx, sample in enumerate(samples, 1):
    print(f"\n--- SAMPLE {idx} ---")
    print(f"Topic: {sample.get('topic', 'N/A')}")
    print(f"Indicator: {sample.get('indicator', 'N/A')}")
    print(f"Question: {sample.get('question', 'N/A')[:150]}...")
    print(f"Answer length: {len(sample.get('answer', ''))} chars")
    print(f"Answer preview: {sample.get('answer', 'N/A')[:200]}...")

print("\n" + "="*70)
print("FINAL QUALITY ASSESSMENT")
print("="*70)

# Calculate overall quality score
error_count = len([e for e in quality_report['errors'] if e])
warning_count = len([w for w in quality_report['warnings'] if w])

print(f"\nErrors: {error_count}")
print(f"Warnings: {warning_count}")

# Scoring
score = 100
score -= error_count * 2  # -2 points per error
score -= warning_count * 0.5  # -0.5 points per warning

if empty_questions > 0 or empty_answers > 0:
    score -= 20

if len(duplicates) > 100:
    score -= 10

quality_report['quality_score'] = max(0, score)

print(f"\n{'='*70}")
print(f"OVERALL QUALITY SCORE: {quality_report['quality_score']:.1f}/100")
print(f"{'='*70}")

if quality_report['quality_score'] >= 90:
    print("✅ EXCELLENT: Data ready for production integration")
    integration_ready = True
elif quality_report['quality_score'] >= 75:
    print("✅ GOOD: Data acceptable for integration with minor cleanup")
    integration_ready = True
elif quality_report['quality_score'] >= 60:
    print("⚠️ FAIR: Data needs cleanup before integration")
    integration_ready = False
else:
    print("❌ POOR: Data requires significant cleanup")
    integration_ready = False

# Save quality report
with open('ultra_deep_research_quality_report.json', 'w', encoding='utf-8') as f:
    json.dump(quality_report, f, indent=2, ensure_ascii=False)

print(f"\nQuality report saved to: ultra_deep_research_quality_report.json")
print(f"\nINTEGRATION RECOMMENDATION: {'PROCEED' if integration_ready else 'DO NOT PROCEED - CLEANUP NEEDED'}")

print("\n" + "="*70)
print("QUALITY TESTING COMPLETE")
print("="*70)
