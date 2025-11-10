import json
import os
from pathlib import Path

inbox_path = Path(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor')

# Expected indicators
expected_files = {
    'ema_100_questions_answers.json': ('EMA', 'Exponential Moving Average'),
    'williams_r_100_questions_answers.json': ('Williams %R', 'Williams'),
    'atr_100_questions_answers.json': ('ATR', 'Average True Range'),
    'cci_100_questions_answers.json': ('CCI', 'Commodity Channel Index'),
    'momentum_100_questions_answers.json': ('Momentum', 'Momentum Indicator'),
    'vortex_100_questions_answers.json': ('Vortex', 'VI+', 'VI-')
}

print("=" * 80)
print("BATCH 6 VALIDATION REPORT - November 9, 2025")
print("=" * 80)
print()

total_pairs = 0
total_chars = 0
compliance_count = 0
all_lengths = []
issues = []

for filename, keywords in expected_files.items():
    filepath = inbox_path / filename

    if not filepath.exists():
        issues.append(f"MISSING: {filename}")
        continue

    print(f"\n{'=' * 60}")
    print(f"File: {filename}")
    print(f"{'=' * 60}")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)

    # Basic counts
    pair_count = len(data.get('answers', []))
    total_pairs += pair_count

    # Check for wrong content
    wrong_indicators = ['Kijun-sen', 'Tenkan-sen', 'Ichimoku']
    wrong_count = sum(content.count(wrong) for wrong in wrong_indicators)

    # Get indicator name from data
    indicator_name = data.get('indicator', 'Unknown')

    # Calculate stats
    answer_lengths = []
    for entry in data.get('answers', []):
        answer = entry.get('answer', '')
        answer_length = len(answer)
        answer_lengths.append(answer_length)
        all_lengths.append(answer_length)
        total_chars += answer_length
        if answer_length >= 3000:
            compliance_count += 1

    avg_length = sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0
    min_length = min(answer_lengths) if answer_lengths else 0
    max_length = max(answer_lengths) if answer_lengths else 0
    compliant = sum(1 for l in answer_lengths if l >= 3000)
    compliance_rate = (compliant / len(answer_lengths) * 100) if answer_lengths else 0

    # Content validation
    keyword_found = False
    for keyword in keywords:
        if keyword.lower() in content.lower():
            keyword_found = True
            break

    # Report
    print(f"Indicator: {indicator_name}")
    print(f"Pairs: {pair_count}")
    print(f"Average length: {avg_length:,.0f} chars")
    print(f"Min length: {min_length:,} chars")
    print(f"Max length: {max_length:,} chars")
    print(f"Compliance (>=3000): {compliant}/{pair_count} ({compliance_rate:.1f}%)")
    print(f"Wrong indicators: {wrong_count}")
    print(f"Keyword validation: {'PASS' if keyword_found else 'FAIL - keywords not found'}")

    # Check for issues
    if wrong_count > 0:
        issues.append(f"{filename}: Contains {wrong_count} wrong indicator references")
    if not keyword_found:
        issues.append(f"{filename}: Missing expected keywords ({', '.join(keywords)})")
    if compliance_rate < 100:
        issues.append(f"{filename}: Only {compliance_rate:.1f}% compliant (some answers <3000 chars)")

    # Sample content check (first answer snippet)
    if data.get('answers'):
        first_answer = data['answers'][0].get('answer', '')[:500]
        print(f"\nFirst answer preview:")
        print(first_answer[:200] + "...")

print()
print("=" * 80)
print("BATCH 6 SUMMARY")
print("=" * 80)

if total_pairs > 0:
    overall_avg = total_chars / total_pairs
    overall_compliance = (compliance_count / total_pairs * 100)

    print(f"Total pairs: {total_pairs}")
    print(f"Overall average: {overall_avg:,.0f} chars")
    print(f"Overall compliance: {compliance_count}/{total_pairs} ({overall_compliance:.1f}%)")
    print(f"Total characters: {total_chars:,}")

print()
print("=" * 80)
print("ISSUES DETECTED")
print("=" * 80)

if issues:
    for issue in issues:
        print(f"- {issue}")
    print()
    print("VERDICT: REJECTION REQUIRED")
else:
    print("No issues detected")
    print()
    print("VERDICT: APPROVED FOR INTEGRATION")

print("=" * 80)
