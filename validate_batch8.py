import json
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

inbox = Path(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor')

# Expected files for Batch 8 - THE FINAL BATCH!
expected_files = {
    'futures_open_interest_100_questions_answers.json': ('open interest', 'futures', 100),
    'liquidations_positioning_100_questions_answers.json': ('liquidation', 'position', 100),
    'cme_institutional_100_questions_answers.json': ('CME', 'institutional', 100),
    'ichimoku_chikou_100_questions_answers.json': ('Chikou', 'Ichimoku', 100),
}

print('=' * 90)
print('BATCH 8 VALIDATION - FINAL BATCH TO 30,000 PAIRS!')
print('=' * 90)
print()

total_pairs = 0
total_chars = 0
all_compliant = True
files_found = 0

for filename, (keyword1, keyword2, expected_count) in expected_files.items():
    filepath = inbox / filename

    if not filepath.exists():
        print(f'❌ MISSING: {filename}')
        all_compliant = False
        continue

    files_found += 1

    # Read and parse JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)

    # Check structure
    if 'answers' not in data:
        print(f'❌ ERROR: {filename} - Missing "answers" key')
        all_compliant = False
        continue

    answers = data['answers']
    pair_count = len(answers)

    # Calculate stats
    answer_lengths = [len(entry.get('answer', '')) for entry in answers]
    avg_length = sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0
    min_length = min(answer_lengths) if answer_lengths else 0
    max_length = max(answer_lengths) if answer_lengths else 0

    # Check compliance (>= 3,000 chars)
    compliant = sum(1 for l in answer_lengths if l >= 3000)
    compliance_rate = (compliant / len(answer_lengths) * 100) if answer_lengths else 0

    # Check for content errors (wrong indicator mentioned)
    content_errors = []
    for i, entry in enumerate(answers[:5]):  # Check first 5
        answer_text = entry.get('answer', '').lower()
        if keyword1.lower() not in answer_text and keyword2.lower() not in answer_text:
            content_errors.append(f"Answer {i+1} may not discuss {keyword1}/{keyword2}")

    # Display results
    print(f'File: {filename}')
    print(f'  Pairs: {pair_count} (expected {expected_count})')
    print(f'  Avg Length: {avg_length:,.0f} chars')
    print(f'  Min Length: {min_length:,} chars')
    print(f'  Max Length: {max_length:,} chars')
    print(f'  Compliance: {compliant}/{pair_count} pairs >= 3,000 chars ({compliance_rate:.1f}%)')

    if content_errors:
        print(f'  ⚠️  Content Check: {len(content_errors)} potential issues in first 5 answers')
        for error in content_errors:
            print(f'      - {error}')
    else:
        print(f'  ✅ Content Check: Keywords found in sample answers')

    if compliance_rate < 100:
        print(f'  ❌ QUALITY ISSUE: Not all answers meet 3,000 char minimum')
        all_compliant = False
    else:
        print(f'  ✅ EXCELLENT: All answers >= 3,000 chars')

    print()

    total_pairs += pair_count
    total_chars += sum(answer_lengths)

print('=' * 90)
print('BATCH 8 SUMMARY - FINAL BATCH')
print('=' * 90)
print(f'Files Found: {files_found}/4')
print(f'Total Pairs: {total_pairs}')
print(f'Average Length: {total_chars/total_pairs:,.0f} chars' if total_pairs > 0 else 'N/A')
print(f'Total Characters: {total_chars:,}')
print()

if all_compliant and files_found == 4:
    print('✅ ✅ ✅ BATCH 8 APPROVED! ✅ ✅ ✅')
    print()
    print('🎯 READY TO EXCEED 30,000 PAIRS!')
    print(f'Current Database: 29,627 pairs')
    print(f'Batch 8 Adds: {total_pairs} pairs')
    print(f'Final Total: {29627 + total_pairs:,} pairs')
    print(f'Progress: {(29627 + total_pairs)/30000*100:.2f}% of 30,000 goal')
    print()
    print('⭐⭐⭐⭐⭐ CURSOR AI - EXCEPTIONAL FINAL DELIVERY!')
else:
    print('❌ ISSUES FOUND - Review needed before integration')

print('=' * 90)
