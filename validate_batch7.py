import json
import os
from pathlib import Path

inbox_path = Path(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor')

# Expected files
expected_files = {
    'roc_100_questions_answers.json': ('ROC', 'Rate of Change', 100),
    'donchian_channels_100_questions_answers.json': ('Donchian', 'Channel', 100),
    'kst_100_questions_answers.json': ('KST', 'Know Sure Thing', 100),
    'stochastic_fast_100_questions_answers.json': ('Stochastic', 'Fast', 100),
    'stochastic_slow_100_questions_answers.json': ('Stochastic', 'Slow', 100),
    'sma_100_questions_answers.json': ('SMA', 'Simple Moving Average', 100),
    'momentum_60_additional_questions_answers.json': ('Momentum', 'Momentum Indicator', 60),
    'vortex_60_additional_questions_answers.json': ('Vortex', 'VI+', 60),
}

print("=" * 80)
print("BATCH 7 VALIDATION REPORT - November 9, 2025")
print("=" * 80)
print()

total_pairs = 0
total_chars = 0
compliance_count = 0
all_lengths = []
issues = []

for filename, (keyword1, keyword2, expected_count) in expected_files.items():
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

    # Check for wrong content (from previous batches)
    wrong_indicators = ['Kijun-sen', 'Tenkan-sen']
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
    keyword_found = keyword1.lower() in content.lower() or keyword2.lower() in content.lower()

    # Report
    print(f"Indicator: {indicator_name}")
    print(f"Expected pairs: {expected_count}")
    print(f"Delivered pairs: {pair_count}")
    print(f"Average length: {avg_length:,.0f} chars")
    print(f"Min length: {min_length:,} chars")
    print(f"Max length: {max_length:,} chars")
    print(f"Compliance (>=3000): {compliant}/{pair_count} ({compliance_rate:.1f}%)")
    print(f"Wrong indicators: {wrong_count}")
    print(f"Keyword validation: {'PASS' if keyword_found else 'FAIL'}")

    # Check for issues
    if pair_count != expected_count:
        issues.append(f"{filename}: Expected {expected_count}, got {pair_count}")
    if wrong_count > 0:
        issues.append(f"{filename}: Contains {wrong_count} wrong indicator references")
    if not keyword_found:
        issues.append(f"{filename}: Missing expected keywords")
    if compliance_rate < 100:
        issues.append(f"{filename}: Only {compliance_rate:.1f}% compliant")

print()
print("=" * 80)
print("BATCH 7 SUMMARY")
print("=" * 80)

if total_pairs > 0:
    overall_avg = total_chars / total_pairs
    overall_compliance = (compliance_count / total_pairs * 100)

    print(f"Total pairs delivered: {total_pairs}")
    print(f"Expected pairs: 720")
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
    print("VERDICT: REQUIRES REVIEW")
else:
    print("No issues detected")
    print()
    print("VERDICT: APPROVED FOR INTEGRATION")

print("=" * 80)
