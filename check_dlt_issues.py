import json

# Load the JSON file
with open(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor\dlt_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

answers = data['answers']

# Check for generic repetitive patterns that might indicate templating issues
print("=== QUALITY ISSUES CHECK ===\n")

issues_found = []

# Issue 1: Check if answers are too similar (repetitive structure)
first_answer = answers[0]['answer']
if "What is Distributed Ledger Technology (DLT), and what is its fundamental purpose? is a fundamental question" in first_answer:
    issues_found.append("ISSUE: Repetitive question embedding in answer detected")
    issues_found.append("   First answer contains the question repeated in the introduction.")

# Issue 2: Check for generic technical analysis mentions when topic is DLT
dlt_specific = data.get('indicator', '')
if 'DLT' in dlt_specific or 'Distributed Ledger' in dlt_specific:
    ta_mentions = sum(1 for a in answers if 'technical analysis' in a['answer'].lower())
    if ta_mentions > 50:
        issues_found.append(f"ISSUE: DLT topic but {ta_mentions}/100 answers mention 'technical analysis'")
        issues_found.append("   DLT is not a technical analysis indicator, it's a blockchain concept.")

# Issue 3: Check for inappropriate trading signal mentions
trading_signals = sum(1 for a in answers if 'trading signal' in a['answer'].lower() or 'execute trades' in a['answer'].lower())
if trading_signals > 50 and 'DLT' in dlt_specific:
    issues_found.append(f"ISSUE: {trading_signals}/100 answers mention trading signals for DLT concept")
    issues_found.append("   DLT is a technology concept, not a trading indicator.")

# Issue 4: Check for "calculate DLT" mentions (DLT is not calculated)
calculate_mentions = sum(1 for a in answers if 'calculate distributed ledger technology' in a['answer'].lower())
if calculate_mentions > 0:
    issues_found.append(f"ISSUE: {calculate_mentions}/100 answers mention 'calculating DLT'")
    issues_found.append("   DLT is a technology concept, not a calculated indicator.")

if issues_found:
    for issue in issues_found:
        print(issue)
    print()
else:
    print("No major quality issues detected.\n")

# Issue 5: Sample a random answer to check for context appropriateness
print("=== SAMPLE ANSWER CHECK ===\n")
sample_idx = 5
sample = answers[sample_idx]
print(f"Question {sample['question_number']}: {sample['question']}\n")
print(f"Answer preview (first 500 chars):")
print(sample['answer'][:500])
print("...\n")

# Issue 6: Check required schema fields
print("=== SCHEMA VALIDATION ===\n")
required_fields = ['indicator', 'category', 'subcategory', 'total_questions', 'answers']
schema_valid = all(field in data for field in required_fields)
print(f"Required root fields present: {schema_valid}")
print(f"  indicator: {data.get('indicator', 'MISSING')}")
print(f"  category: {data.get('category', 'MISSING')}")
print(f"  subcategory: {data.get('subcategory', 'MISSING')}")
print(f"  total_questions: {data.get('total_questions', 'MISSING')}")
print(f"  answers count: {len(data.get('answers', []))}")

answer_fields_valid = all(
    all(field in a for field in ['question_number', 'question', 'answer'])
    for a in answers
)
print(f"\nAll answers have required fields: {answer_fields_valid}")
print(f"  (question_number, question, answer)")
