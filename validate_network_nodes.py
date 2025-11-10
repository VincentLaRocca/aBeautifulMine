#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate network_nodes_questions_answers.json against quality standards
"""

import json
import statistics
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load the JSON file
with open(r'inbox\cursor\network_nodes_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

answers = data.get('answers', [])

print("="*70)
print("COMPREHENSIVE QUALITY VALIDATION: NETWORK NODES")
print("="*70 + "\n")

# 1. Data Integrity Check
print("1. DATA INTEGRITY CHECK")
print("-" * 70)
declared_count = data.get('total_questions', 0)
actual_count = len(answers)
print(f"   Declared questions: {declared_count}")
print(f"   Actual answers: {actual_count}")
if declared_count != actual_count:
    print(f"   WARNING: Mismatch! Missing {declared_count - actual_count} answer(s)")
    missing_nums = set(range(1, declared_count + 1)) - {a['question_number'] for a in answers}
    if missing_nums:
        print(f"   Missing question numbers: {sorted(missing_nums)}")
else:
    print(f"   Status: PASS")

# Check for duplicate question numbers
question_numbers = [a['question_number'] for a in answers]
duplicates = [num for num in set(question_numbers) if question_numbers.count(num) > 1]
if duplicates:
    print(f"   WARNING: Duplicate question numbers found: {duplicates}")
else:
    print(f"   No duplicate question numbers: PASS")

print()

# 2. Answer Length Statistics
print("2. ANSWER LENGTH")
print("-" * 70)
if answers:
    lengths = [len(a['answer']) for a in answers]
    print(f"   Total answers: {len(lengths)}")
    print(f"   Average: {statistics.mean(lengths):.0f} chars")
    print(f"   Median: {statistics.median(lengths):.0f} chars")
    print(f"   Min: {min(lengths)} chars")
    print(f"   Max: {max(lengths)} chars")
    print(f"   Below 3000: {sum(1 for l in lengths if l < 3000)} ({sum(1 for l in lengths if l < 3000)/len(lengths)*100:.1f}%)")
    print(f"   Status: {'PASS' if all(l >= 3000 for l in lengths) else 'FAIL - Some below minimum'}")
else:
    print(f"   ERROR: No answers found")

print()

# 3. Crypto-Specific Content
print("3. CRYPTO-SPECIFIC CONTENT")
print("-" * 70)
crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency', 'blockchain']
crypto_count = sum(1 for a in answers if any(kw in a['answer'].lower() for kw in crypto_keywords))
print(f"   Answers with crypto keywords: {crypto_count}/{len(answers)} ({crypto_count/len(answers)*100:.1f}%)")
print(f"   Status: {'PASS' if crypto_count >= len(answers)*0.95 else 'WARN - Low crypto specificity'}")

print(f"\n   Keyword frequency:")
for kw in crypto_keywords:
    count = sum(1 for a in answers if kw in a['answer'].lower())
    print(f"     {kw}: {count} answers ({count/len(answers)*100:.1f}%)")

print()

# 4. Markdown Structure
print("4. MARKDOWN STRUCTURE")
print("-" * 70)
with_headings = sum(1 for a in answers if '##' in a['answer'])
with_bullets = sum(1 for a in answers if '- ' in a['answer'] or '* ' in a['answer'])
with_bold = sum(1 for a in answers if '**' in a['answer'])
with_examples = sum(1 for a in answers if 'example' in a['answer'].lower() or 'scenario' in a['answer'].lower())

print(f"   Headings (##): {with_headings}/{len(answers)} ({with_headings/len(answers)*100:.1f}%)")
print(f"   Bullet points: {with_bullets}/{len(answers)} ({with_bullets/len(answers)*100:.1f}%)")
print(f"   Bold text (**): {with_bold}/{len(answers)} ({with_bold/len(answers)*100:.1f}%)")
print(f"   Examples/scenarios: {with_examples}/{len(answers)} ({with_examples/len(answers)*100:.1f}%)")
print(f"   Status: {'PASS' if all([with_headings >= len(answers)*0.95, with_examples >= len(answers)*0.95]) else 'NEEDS IMPROVEMENT'}")

print()

# 5. Appropriate Framing Check
print("5. APPROPRIATE FRAMING (Should be fundamentals, NOT technical analysis)")
print("-" * 70)

# Check for WRONG framing (technical analysis)
ta_mentions = sum(1 for a in answers if 'technical analysis' in a['answer'].lower())
trading_signals = sum(1 for a in answers if 'trading signal' in a['answer'].lower())
calculate_mentions = sum(1 for a in answers if 'calculate' in a['answer'].lower() and 'indicator' in a['answer'].lower())

print(f"   'Technical analysis' mentions: {ta_mentions}/{len(answers)}")
print(f"   Status: {'PASS' if ta_mentions == 0 else 'FAIL - Wrong framing!'}")

print(f"\n   'Trading signal' mentions: {trading_signals}/{len(answers)}")
print(f"   Status: {'PASS' if trading_signals == 0 else 'FAIL - Wrong framing!'}")

print(f"\n   'Calculate indicator' mentions: {calculate_mentions}/{len(answers)}")
print(f"   Status: {'PASS' if calculate_mentions == 0 else 'WARN - Inappropriate for fundamentals'}")

# Check for CORRECT framing (educational/technology)
education_mentions = sum(1 for a in answers if 'education' in a['answer'].lower() or 'understanding' in a['answer'].lower())
technology_mentions = sum(1 for a in answers if 'technology' in a['answer'].lower() or 'technological' in a['answer'].lower())
network_mentions = sum(1 for a in answers if 'network' in a['answer'].lower())

print(f"\n   Educational language: {education_mentions}/{len(answers)}")
print(f"   Technology mentions: {technology_mentions}/{len(answers)}")
print(f"   Network mentions: {network_mentions}/{len(answers)}")
print(f"   Status: {'PASS' if network_mentions >= len(answers)*0.8 else 'NEEDS IMPROVEMENT'}")

print()

# 6. Topic Appropriateness
print("6. TOPIC APPROPRIATENESS (Network Nodes)")
print("-" * 70)
topic_name = data.get('indicator', '')
print(f"   Topic: {topic_name}")
print(f"   Category: {data.get('category', 'N/A')} > {data.get('subcategory', 'N/A')}")

# Check if content is about nodes/network
node_terms = ['node', 'full node', 'light node', 'peer', 'network', 'blockchain', 'synchronization']
node_relevance = sum(1 for a in answers if any(term in a['answer'].lower() for term in node_terms))
print(f"   Answers with node-related terms: {node_relevance}/{len(answers)} ({node_relevance/len(answers)*100:.1f}%)")
print(f"   Status: {'PASS' if node_relevance >= len(answers)*0.9 else 'WARN - Low topic relevance'}")

print()

# 7. Sample Answer Preview
print("7. SAMPLE ANSWER PREVIEW")
print("-" * 70)
if answers:
    sample = answers[0]
    print(f"   Question {sample['question_number']}: {sample['question'][:80]}...")
    print(f"   Answer length: {len(sample['answer'])} chars")
    print(f"\n   First 500 chars:")
    print(f"   {sample['answer'][:500]}...")

print()

# 8. Schema Validation
print("8. SCHEMA VALIDATION")
print("-" * 70)
required_root = ['indicator', 'category', 'subcategory', 'total_questions', 'answers']
schema_valid = all(field in data for field in required_root)
print(f"   Root fields present: {'PASS' if schema_valid else 'FAIL'}")

if answers:
    answer_fields_valid = all(
        all(field in a for field in ['question_number', 'question', 'answer'])
        for a in answers
    )
    print(f"   Answer fields present: {'PASS' if answer_fields_valid else 'FAIL'}")
else:
    print(f"   Answer fields: Cannot validate (no answers)")

print()

# Final Assessment
print("="*70)
print("FINAL ASSESSMENT")
print("="*70)

issues = []
warnings = []
passes = []

# Critical issues
if declared_count != actual_count:
    issues.append(f"Data mismatch: {declared_count} declared, {actual_count} actual")
if answers and any(len(a['answer']) < 3000 for a in answers):
    issues.append("Some answers below 3,000 character minimum")
if ta_mentions > 0:
    issues.append(f"Wrong framing: {ta_mentions} mentions of 'technical analysis'")
if trading_signals > 0:
    issues.append(f"Wrong framing: {trading_signals} mentions of 'trading signals'")

# Warnings
if crypto_count < len(answers) * 0.95:
    warnings.append(f"Low crypto-specificity: {crypto_count/len(answers)*100:.1f}%")
if with_examples < len(answers) * 0.95:
    warnings.append(f"Low example coverage: {with_examples/len(answers)*100:.1f}%")
if node_relevance < len(answers) * 0.9:
    warnings.append(f"Low topic relevance: {node_relevance/len(answers)*100:.1f}%")

# Passes
if not issues:
    passes.append("All critical checks passed")
if crypto_count >= len(answers) * 0.95:
    passes.append("Crypto-specific content: PASS")
if all(len(a['answer']) >= 3000 for a in answers):
    passes.append("Answer length: PASS")

print("\nCRITICAL ISSUES:")
if issues:
    for issue in issues:
        print(f"   X {issue}")
else:
    print(f"   None - All critical checks passed!")

print("\nWARNINGS:")
if warnings:
    for warning in warnings:
        print(f"   ! {warning}")
else:
    print(f"   None")

print("\nPASSES:")
for p in passes:
    print(f"   + {p}")

print("\n" + "="*70)
if not issues and not warnings:
    print("RECOMMENDATION: APPROVE FOR INTEGRATION")
    print("="*70)
elif not issues:
    print("RECOMMENDATION: APPROVE WITH MINOR WARNINGS")
    print("="*70)
else:
    print("RECOMMENDATION: NEEDS FIXES BEFORE INTEGRATION")
    print("="*70)
