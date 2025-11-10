#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Integration Batch Validator for Gemini
Validates Q&A batches before they enter the database
"""

import json
import statistics
import sys
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class BatchValidator:
    """Validates Q&A batches before database integration"""

    def __init__(self, json_file, db_type):
        self.json_file = json_file
        self.db_type = db_type.lower()  # 'technical' or 'fundamentals'
        self.data = None
        self.answers = []
        self.issues = []
        self.warnings = []
        self.passes = []

        # Quality thresholds
        self.MIN_LENGTH = 3000
        self.MIN_CRYPTO_PCT = 95.0
        self.MIN_EXAMPLES_PCT = 95.0
        self.MIN_MARKDOWN_PCT = 95.0

    def load_data(self):
        """Load JSON data"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.answers = self.data.get('answers', [])
            return True
        except Exception as e:
            self.issues.append(f"Failed to load JSON: {e}")
            return False

    def check_data_integrity(self):
        """Check for data integrity issues"""
        print("\n1. DATA INTEGRITY")
        print("-" * 70)

        declared = self.data.get('total_questions', 0)
        actual = len(self.answers)

        print(f"   Declared: {declared} questions")
        print(f"   Actual: {actual} answers")

        if declared != actual:
            self.issues.append(f"Data mismatch: {declared} declared, {actual} actual")
            print(f"   Status: FAIL - Missing {declared - actual} answer(s)")

            # Find missing numbers
            expected = set(range(1, declared + 1))
            actual_nums = {a['question_number'] for a in self.answers}
            missing = expected - actual_nums
            if missing:
                print(f"   Missing: {sorted(missing)}")
        else:
            self.passes.append("Data integrity: counts match")
            print(f"   Status: PASS")

        # Check for duplicates
        question_numbers = [a['question_number'] for a in self.answers]
        duplicates = [num for num in set(question_numbers) if question_numbers.count(num) > 1]
        if duplicates:
            self.issues.append(f"Duplicate question numbers: {duplicates}")
            print(f"   Duplicates: {duplicates} - FAIL")
        else:
            print(f"   Duplicates: None - PASS")

    def check_answer_lengths(self):
        """Check answer lengths"""
        print("\n2. ANSWER LENGTH")
        print("-" * 70)

        if not self.answers:
            self.issues.append("No answers to validate")
            return

        lengths = [len(a['answer']) for a in self.answers]
        avg = statistics.mean(lengths)
        min_len = min(lengths)
        max_len = max(lengths)
        below_min = sum(1 for l in lengths if l < self.MIN_LENGTH)

        print(f"   Average: {avg:.0f} chars")
        print(f"   Min: {min_len} chars")
        print(f"   Max: {max_len} chars")
        print(f"   Below {self.MIN_LENGTH}: {below_min} ({below_min/len(lengths)*100:.1f}%)")

        if below_min > 0:
            self.issues.append(f"{below_min} answers below {self.MIN_LENGTH} character minimum")
            print(f"   Status: FAIL")
        else:
            self.passes.append(f"All answers ≥ {self.MIN_LENGTH} characters")
            print(f"   Status: PASS")

    def check_crypto_specific(self):
        """Check crypto-specific content"""
        print("\n3. CRYPTO-SPECIFIC CONTENT")
        print("-" * 70)

        crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency', 'blockchain']
        crypto_count = sum(1 for a in self.answers if any(kw in a['answer'].lower() for kw in crypto_keywords))
        crypto_pct = (crypto_count / len(self.answers) * 100) if self.answers else 0

        print(f"   Crypto-specific: {crypto_count}/{len(self.answers)} ({crypto_pct:.1f}%)")

        if crypto_pct < self.MIN_CRYPTO_PCT:
            self.warnings.append(f"Low crypto-specificity: {crypto_pct:.1f}%")
            print(f"   Status: WARN - Below {self.MIN_CRYPTO_PCT}%")
        else:
            self.passes.append("Crypto-specificity sufficient")
            print(f"   Status: PASS")

    def check_markdown_structure(self):
        """Check markdown formatting"""
        print("\n4. MARKDOWN STRUCTURE")
        print("-" * 70)

        with_headings = sum(1 for a in self.answers if '##' in a['answer'])
        with_bullets = sum(1 for a in self.answers if '- ' in a['answer'] or '* ' in a['answer'])
        with_examples = sum(1 for a in self.answers if 'example' in a['answer'].lower())

        heading_pct = (with_headings / len(self.answers) * 100) if self.answers else 0
        example_pct = (with_examples / len(self.answers) * 100) if self.answers else 0

        print(f"   Headings: {with_headings}/{len(self.answers)} ({heading_pct:.1f}%)")
        print(f"   Bullets: {with_bullets}/{len(self.answers)}")
        print(f"   Examples: {with_examples}/{len(self.answers)} ({example_pct:.1f}%)")

        if heading_pct < self.MIN_MARKDOWN_PCT:
            self.warnings.append(f"Low markdown usage: {heading_pct:.1f}%")
            print(f"   Status: WARN")
        elif example_pct < self.MIN_EXAMPLES_PCT:
            self.warnings.append(f"Low example coverage: {example_pct:.1f}%")
            print(f"   Status: WARN")
        else:
            self.passes.append("Markdown structure good")
            print(f"   Status: PASS")

    def check_framing(self):
        """Check appropriate framing based on database type"""
        print("\n5. CONTENT FRAMING")
        print("-" * 70)

        ta_mentions = sum(1 for a in self.answers if 'technical analysis' in a['answer'].lower())
        trading_signals = sum(1 for a in self.answers if 'trading signal' in a['answer'].lower())
        education_mentions = sum(1 for a in self.answers if 'education' in a['answer'].lower())

        print(f"   Database type: {self.db_type.upper()}")

        if self.db_type == 'technical':
            # Should have technical analysis framing
            print(f"   Technical analysis mentions: {ta_mentions}/{len(self.answers)}")
            if ta_mentions < len(self.answers) * 0.5:
                self.warnings.append("Low technical analysis framing for technical DB")
                print(f"   Status: WARN - Expected more technical framing")
            else:
                self.passes.append("Technical analysis framing appropriate")
                print(f"   Status: PASS")

        elif self.db_type == 'fundamentals':
            # Should NOT have technical analysis framing
            print(f"   Technical analysis mentions: {ta_mentions}/{len(self.answers)}")
            print(f"   Trading signals mentions: {trading_signals}/{len(self.answers)}")
            print(f"   Educational mentions: {education_mentions}/{len(self.answers)}")

            if ta_mentions > 0:
                self.issues.append(f"Wrong framing: {ta_mentions} 'technical analysis' mentions in fundamentals batch")
                print(f"   Status: FAIL - Wrong framing for fundamentals")
            elif trading_signals > len(self.answers) * 0.1:
                self.issues.append(f"Wrong framing: {trading_signals} 'trading signal' mentions in fundamentals batch")
                print(f"   Status: FAIL - Too many trading signals for fundamentals")
            else:
                self.passes.append("Fundamentals framing appropriate")
                print(f"   Status: PASS")

    def check_schema(self):
        """Check schema compliance"""
        print("\n6. SCHEMA VALIDATION")
        print("-" * 70)

        required_root = ['indicator', 'category', 'subcategory', 'total_questions', 'answers']
        has_root = all(field in self.data for field in required_root)

        print(f"   Root fields: {'PASS' if has_root else 'FAIL'}")

        if not has_root:
            missing = [f for f in required_root if f not in self.data]
            self.issues.append(f"Missing root fields: {missing}")

        if self.answers:
            required_answer = ['question_number', 'question', 'answer']
            has_answer_fields = all(
                all(field in a for field in required_answer)
                for a in self.answers
            )
            print(f"   Answer fields: {'PASS' if has_answer_fields else 'FAIL'}")

            if not has_answer_fields:
                self.issues.append("Some answers missing required fields")
        else:
            print(f"   Answer fields: Cannot validate (no answers)")

    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)

        print(f"\nFile: {self.json_file}")
        print(f"Database Type: {self.db_type.upper()}")
        print(f"Topic: {self.data.get('indicator', 'Unknown')}")
        print(f"Category: {self.data.get('category', 'Unknown')} > {self.data.get('subcategory', 'Unknown')}")

        print(f"\nCRITICAL ISSUES: {len(self.issues)}")
        if self.issues:
            for issue in self.issues:
                print(f"   X {issue}")
        else:
            print(f"   None")

        print(f"\nWARNINGS: {len(self.warnings)}")
        if self.warnings:
            for warning in self.warnings:
                print(f"   ! {warning}")
        else:
            print(f"   None")

        print(f"\nPASSES: {len(self.passes)}")
        for p in self.passes:
            print(f"   + {p}")

        print("\n" + "="*70)

        # Decision
        if not self.issues and not self.warnings:
            decision = "APPROVE"
            print("DECISION: APPROVE FOR INTEGRATION")
        elif not self.issues:
            decision = "APPROVE_WITH_WARNINGS"
            print("DECISION: APPROVE WITH WARNINGS")
        else:
            decision = "REJECT"
            print("DECISION: REJECT - NEEDS FIXES")

        print("="*70)

        return decision

    def save_report(self, decision):
        """Save validation report to file"""
        report_file = f"validation_report_{Path(self.json_file).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"BATCH VALIDATION REPORT\n")
            f.write(f"=" * 70 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"File: {self.json_file}\n")
            f.write(f"Database Type: {self.db_type.upper()}\n")
            f.write(f"Topic: {self.data.get('indicator', 'Unknown')}\n")
            f.write(f"Category: {self.data.get('category', 'Unknown')} > {self.data.get('subcategory', 'Unknown')}\n\n")

            f.write(f"DECISION: {decision}\n\n")

            f.write(f"CRITICAL ISSUES: {len(self.issues)}\n")
            for issue in self.issues:
                f.write(f"  X {issue}\n")
            f.write("\n")

            f.write(f"WARNINGS: {len(self.warnings)}\n")
            for warning in self.warnings:
                f.write(f"  ! {warning}\n")
            f.write("\n")

            f.write(f"PASSES: {len(self.passes)}\n")
            for p in self.passes:
                f.write(f"  + {p}\n")

        print(f"\nReport saved to: {report_file}")

    def validate(self):
        """Run complete validation"""
        print("="*70)
        print("PRE-INTEGRATION BATCH VALIDATION")
        print("="*70)

        if not self.load_data():
            return "ERROR"

        self.check_data_integrity()
        self.check_answer_lengths()
        self.check_crypto_specific()
        self.check_markdown_structure()
        self.check_framing()
        self.check_schema()

        decision = self.generate_report()
        self.save_report(decision)

        return decision

def main():
    """Main execution"""
    if len(sys.argv) != 3:
        print("Usage: python validate_batch_preintegration.py <json_file> <db_type>")
        print("  db_type: 'technical' or 'fundamentals'")
        sys.exit(1)

    json_file = sys.argv[1]
    db_type = sys.argv[2]

    if db_type.lower() not in ['technical', 'fundamentals']:
        print("Error: db_type must be 'technical' or 'fundamentals'")
        sys.exit(1)

    validator = BatchValidator(json_file, db_type)
    decision = validator.validate()

    # Exit codes for automation
    if decision == "APPROVE":
        sys.exit(0)
    elif decision == "APPROVE_WITH_WARNINGS":
        sys.exit(1)
    else:  # REJECT or ERROR
        sys.exit(2)

if __name__ == '__main__':
    main()
