import json
import statistics

# Load the JSON file
with open(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor\dlt_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

answers = data['answers']

print("=== COMPREHENSIVE QUALITY VALIDATION ===\n")

# 1. Length Statistics
lengths = [len(a['answer']) for a in answers]
print("1. ANSWER LENGTH:")
print(f"   Total answers: {len(lengths)}")
print(f"   Average: {statistics.mean(lengths):.0f} chars")
print(f"   Median: {statistics.median(lengths):.0f} chars")
print(f"   Min: {min(lengths)} chars")
print(f"   Max: {max(lengths)} chars")
print(f"   Below 3000: {sum(1 for l in lengths if l < 3000)} ({sum(1 for l in lengths if l < 3000)/len(lengths)*100:.1f}%)")
print(f"   Status: {'PASS' if all(l >= 3000 for l in lengths) else 'FAIL'}\n")

# 2. Crypto-Specific Content
crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency', 'blockchain']
crypto_count = sum(1 for a in answers if any(kw in a['answer'].lower() for kw in crypto_keywords))
print("2. CRYPTO-SPECIFIC CONTENT:")
print(f"   Answers with crypto keywords: {crypto_count}/100 ({crypto_count}%)")
print(f"   Status: {'PASS' if crypto_count >= 95 else 'FAIL'}\n")

# 3. Markdown Structure
with_headings = sum(1 for a in answers if '##' in a['answer'])
with_bullets = sum(1 for a in answers if '- ' in a['answer'] or '* ' in a['answer'])
with_bold = sum(1 for a in answers if '**' in a['answer'])
with_examples = sum(1 for a in answers if 'example' in a['answer'].lower() or 'scenario' in a['answer'].lower())

print("3. MARKDOWN STRUCTURE:")
print(f"   Headings (##): {with_headings}/100 ({with_headings}%)")
print(f"   Bullet points: {with_bullets}/100 ({with_bullets}%)")
print(f"   Bold text (**): {with_bold}/100 ({with_bold}%)")
print(f"   Examples/scenarios: {with_examples}/100 ({with_examples}%)")
print(f"   Status: {'PASS' if all([with_headings >= 95, with_bullets >= 95, with_examples >= 95]) else 'FAIL'}\n")

# 4. Check for FIXED issues (should be GONE now)
print("4. PREVIOUSLY IDENTIFIED ISSUES (should be FIXED):")

# Technical analysis mentions (should be low/gone for DLT)
ta_mentions = sum(1 for a in answers if 'technical analysis' in a['answer'].lower())
print(f"   'Technical analysis' mentions: {ta_mentions}/100")
print(f"   Status: {'PASS - Fixed!' if ta_mentions == 0 else 'WARN - Still present'}")

# Trading signal mentions (should be low/gone for DLT)
trading_signals = sum(1 for a in answers if 'trading signal' in a['answer'].lower())
print(f"   'Trading signal' mentions: {trading_signals}/100")
print(f"   Status: {'PASS - Fixed!' if trading_signals == 0 else 'WARN - Still present'}")

# Calculate mentions (should be gone for DLT)
calculate_mentions = sum(1 for a in answers if 'calculate distributed ledger technology' in a['answer'].lower())
print(f"   'Calculate DLT' mentions: {calculate_mentions}/100")
print(f"   Status: {'PASS - Fixed!' if calculate_mentions == 0 else 'WARN - Still present'}\n")

# 5. Check for appropriate educational framing
education_mentions = sum(1 for a in answers if 'education' in a['answer'].lower() or 'understanding' in a['answer'].lower())
technology_mentions = sum(1 for a in answers if 'technology' in a['answer'].lower() or 'technological' in a['answer'].lower())

print("5. APPROPRIATE FRAMING (DLT as technology/concept):")
print(f"   Educational language: {education_mentions}/100")
print(f"   Technology mentions: {technology_mentions}/100")
print(f"   Status: {'PASS' if technology_mentions >= 80 else 'NEEDS IMPROVEMENT'}\n")

# 6. Schema Validation
print("6. SCHEMA VALIDATION:")
required_root = ['indicator', 'category', 'subcategory', 'total_questions', 'answers']
schema_valid = all(field in data for field in required_root)
print(f"   Root fields: {'PASS' if schema_valid else 'FAIL'}")

answer_fields_valid = all(
    all(field in a for field in ['question_number', 'question', 'answer'])
    for a in answers
)
print(f"   Answer fields: {'PASS' if answer_fields_valid else 'FAIL'}")

question_numbers_valid = all(a['question_number'] == i+1 for i, a in enumerate(answers))
print(f"   Question numbering: {'PASS' if question_numbers_valid else 'FAIL'}\n")

# 7. Sample Answer Quality Check
print("7. SAMPLE ANSWER (Question 1):")
sample = answers[0]['answer']
print(f"   Length: {len(sample)} chars")
print(f"   Has introduction: {'Yes' if '## Introduction' in sample else 'No'}")
print(f"   Has examples: {'Yes' if 'example' in sample.lower() else 'No'}")
print(f"   Crypto-specific: {'Yes' if any(kw in sample.lower() for kw in ['bitcoin', 'ethereum', 'crypto']) else 'No'}")
print(f"\n   First 400 chars:")
print(f"   {sample[:400]}...\n")

# Final Assessment
print("="*60)
print("FINAL ASSESSMENT:")
all_checks = [
    all(l >= 3000 for l in lengths),
    crypto_count >= 95,
    with_headings >= 95,
    with_examples >= 95,
    ta_mentions == 0,
    trading_signals == 0,
    calculate_mentions == 0,
    schema_valid,
    answer_fields_valid
]

if all(all_checks):
    print("STATUS: PASS - Meets all quality standards!")
    print("RECOMMENDATION: APPROVE for integration")
else:
    print("STATUS: NEEDS REVIEW - Some issues remain")
    print("RECOMMENDATION: Review specific issues above")
print("="*60)
