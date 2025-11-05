#!/usr/bin/env python3
"""
Droid Research Report Parser
Created: 2025-11-02
Purpose: Parse Droid's ultra_deep_research reports into structured Q&A JSON

Input: Research report .txt files from Droid
Output: Structured JSON files ready for database import

This is Claude's parsing skill - transforming Droid's research faucet into refined content!
"""

import re
import json
from pathlib import Path
from datetime import datetime

def parse_research_report(report_file):
    """Parse a Droid research report and extract Q&A pairs"""

    print(f"\nParsing: {report_file}")
    print("=" * 70)

    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from header
    topic_match = re.search(r'Topic:\s*(.+)', content)
    date_match = re.search(r'Research Completed:\s*(.+)', content)
    queries_match = re.search(r'Search Queries Executed:\s*(\d+)', content)
    success_match = re.search(r'Success Rate:\s*([\d.]+)%', content)

    topic = topic_match.group(1).strip() if topic_match else "Unknown"
    research_date = date_match.group(1).strip() if date_match else datetime.now().isoformat()
    queries_executed = int(queries_match.group(1)) if queries_match else 100
    success_rate = success_match.group(1) if success_match else "0.0"

    # Find the Q&A pairs section (accounting for ANSI color codes)
    qa_section_match = re.search(
        r'QUESTION-ANSWER PAIRS WITH CHARACTER COUNTS.*?\[33mTotal Question-Answer Pairs:\[0m\s*(\d+)',
        content,
        re.DOTALL
    )

    if not qa_section_match:
        print("  [!] Could not find Q&A pairs section")
        return None

    total_pairs = int(qa_section_match.group(1))
    print(f"  Total Q&A pairs found: {total_pairs}")

    # Extract individual Q&A pairs
    # Pattern: Pair X: question: "..." answer: ...
    pair_pattern = r'\[32mPair (\d+):\[0m\s*\[33mquestion:\[0m\s*(.+?)\[36mquestion characters:\[0m\s*\d+\s*\[33manswer:\[0m\s*(.+?)\[36manswer characters:\[0m\s*\d+'

    qa_pairs = []
    matches = re.finditer(pair_pattern, content, re.DOTALL)

    for match in matches:
        pair_num = int(match.group(1))
        question = match.group(2).strip()
        answer = match.group(3).strip()

        # Clean up question (remove quotes and formatting)
        question = re.sub(r'^["\']+|["\']+$', '', question)
        question = question.replace(' AND ', ' ')
        question = question.strip()

        # Clean up answer (remove ANSI color codes, extra whitespace)
        answer = re.sub(r'\[[\d;]+m', '', answer)
        answer = re.sub(r'\n\s*\n', '\n\n', answer)
        answer = answer.strip()

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

    for report_file in report_files:
        try:
            # Parse the report
            data = parse_research_report(report_file)

            if data:
                # Generate output filename
                # Extract indicator name from filename or topic
                base_name = report_file.stem.replace("research_report_", "")
                output_file = output_path / f"{base_name}_qa_pairs.json"

                # Save to JSON
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"  ✓ Saved: {output_file}")
                parsed_count += 1

        except Exception as e:
            print(f"  ✗ Error parsing {report_file.name}: {e}")

    print("\n" + "=" * 70)
    print(f"Parsing complete: {parsed_count}/{len(report_files)} reports processed")
    print("=" * 70)

if __name__ == "__main__":
    # Test with processed reports
    input_directory = "inbox/droid/processed"
    output_directory = "parsed_qa_data"

    parse_all_reports(input_directory, output_directory)
