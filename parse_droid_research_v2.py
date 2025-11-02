#!/usr/bin/env python3
"""
Droid Research Report Parser v2
Created: 2025-11-02
Purpose: Parse Droid's ultra_deep_research reports with proper ANSI code handling

Handles \x1b[XXm ANSI escape sequences properly
"""

import re
import json
from pathlib import Path
from datetime import datetime

def strip_ansi(text):
    """Remove all ANSI escape codes from text"""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def parse_research_report(report_file):
    """Parse a Droid research report and extract Q&A pairs"""

    print(f"\nParsing: {report_file}")
    print("=" * 70)

    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from header (strip ANSI codes first for easier parsing)
    topic_match = re.search(r'Topic:\s*(.+)', content)
    date_match = re.search(r'Research Completed:\s*(.+)', content)
    queries_match = re.search(r'Search Queries Executed:\s*(\d+)', content)
    success_match = re.search(r'Success Rate:\s*([\d.]+)%', content)

    topic = strip_ansi(topic_match.group(1).strip()) if topic_match else "Unknown"
    research_date = strip_ansi(date_match.group(1).strip()) if date_match else datetime.now().isoformat()
    queries_executed = int(queries_match.group(1)) if queries_match else 100
    success_rate = success_match.group(1) if success_match else "0.0"

    # Find the Q&A pairs section
    qa_section_match = re.search(
        r'QUESTION-ANSWER PAIRS WITH CHARACTER COUNTS',
        content,
        re.IGNORECASE
    )

    if not qa_section_match:
        print("  [!] Could not find Q&A pairs section")
        return None

    # Extract total pairs count (skip ANSI codes - look for 2+ digits to avoid matching digits in ANSI codes)
    total_match = re.search(r'Total Question-Answer Pairs:.*?(\d{2,})', content)
    total_pairs = int(total_match.group(1)) if total_match else 0

    if total_pairs == 0:
        print("  [!] No Q&A pairs found")
        return None

    print(f"  Total Q&A pairs found: {total_pairs}")

    # Extract individual Q&A pairs
    # Look for pattern: Pair X: ... question: ... answer: ...
    # Split by "Pair X:" markers
    pair_sections = re.split(r'Pair (\d+):', content)

    qa_pairs = []

    # Skip first element (everything before first "Pair 1:")
    for i in range(1, len(pair_sections), 2):
        if i+1 >= len(pair_sections):
            break

        pair_num = int(pair_sections[i])
        pair_content = pair_sections[i+1]

        # Extract question
        question_match = re.search(r'question:\s*(.+?)question characters:', pair_content, re.DOTALL)
        if not question_match:
            continue

        question = strip_ansi(question_match.group(1).strip())
        question = re.sub(r'^["\']+|["\']+$', '', question)  # Remove quotes
        question = question.strip()

        # Extract answer
        answer_match = re.search(r'answer:\s*(.+?)answer characters:', pair_content, re.DOTALL)
        if not answer_match:
            continue

        answer = strip_ansi(answer_match.group(1).strip())
        answer = re.sub(r'\n\s*\n\s*\n+', '\n\n', answer)  # Normalize multiple newlines
        answer = answer.strip()

        # Skip if empty
        if not question or not answer:
            continue

        qa_pairs.append({
            "pair_number": pair_num,
            "question": question,
            "answer": answer,
            "topic": topic,
            "created_date": research_date
        })

    print(f"  Extracted {len(qa_pairs)} Q&A pairs")

    # Build structured output
    output = {
        "research_topic": topic,
        "total_pairs": len(qa_pairs),
        "research_method": "ultra_deep_research",
        "queries_executed": queries_executed,
        "success_rate": f"{success_rate}%",
        "generation_date": research_date,
        "source_file": str(report_file),
        "qa_pairs": qa_pairs
    }

    return output

def parse_all_reports(input_dir, output_dir):
    """Parse all research reports in a directory"""

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Find all research report text files
    report_files = list(input_path.glob("research_report_*.txt"))

    print(f"\nFound {len(report_files)} research reports to parse")
    print("=" * 70)

    parsed_count = 0
    total_qa = 0

    for report_file in report_files:
        try:
            # Parse the report
            data = parse_research_report(report_file)

            if data:
                # Generate output filename from topic
                topic_slug = data['research_topic'].lower()
                topic_slug = re.sub(r'[^\w\s-]', '', topic_slug)
                topic_slug = re.sub(r'[\s_]+', '_', topic_slug)
                topic_slug = topic_slug[:80]  # Limit length

                output_file = output_path / f"{topic_slug}_qa_pairs.json"

                # Save to JSON
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"  [OK] Saved: {output_file}")
                parsed_count += 1
                total_qa += data['total_pairs']

        except Exception as e:
            print(f"  [ERROR] Error parsing {report_file.name}: {e}")

    print("\n" + "=" * 70)
    print(f"Parsing complete: {parsed_count}/{len(report_files)} reports processed")
    print(f"Total Q&A pairs extracted: {total_qa}")
    print("=" * 70)

if __name__ == "__main__":
    # Parse from inbox/droid directory
    input_directory = "inbox/droid"
    output_directory = "parsed_qa_data"

    parse_all_reports(input_directory, output_directory)
