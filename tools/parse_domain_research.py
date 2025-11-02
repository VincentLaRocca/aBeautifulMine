"""
Universal Research Report Parser
Parses research_report_*.txt files for ANY domain

Works for:
- Crypto indicators
- Web development topics
- Database design patterns
- AI agent behaviors
- Any structured knowledge domain
"""

import re
import json
import os
from datetime import datetime
from pathlib import Path


def strip_ansi(text):
    """Remove all ANSI escape codes from text"""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


def parse_research_report(report_file, domain="general", output_dir=None):
    """
    Parse research report for ANY domain

    Args:
        report_file: Path to research_report_*.txt
        domain: Domain identifier (e.g., "crypto_indicators", "web_development")
        output_dir: Where to save parsed JSON (default: parsed_qa_data/)

    Returns:
        dict: Parsed data with topic, Q&A pairs, metadata
    """
    print(f"\n{'='*60}")
    print(f"PARSING: {os.path.basename(report_file)}")
    print(f"DOMAIN: {domain}")
    print(f"{'='*60}\n")

    # Read file
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip ANSI codes
    clean_content = strip_ansi(content)

    # Extract topic name (from filename or content)
    topic_name = extract_topic_name(report_file, clean_content)

    # Extract total Q&A count
    total_pairs = extract_total_pairs(clean_content)

    # Extract Q&A pairs
    qa_pairs = extract_qa_pairs(clean_content, topic_name)

    # Build result structure
    result = {
        'domain': domain,
        'topic': topic_name,
        'topic_slug': slugify(topic_name),
        'source_file': os.path.basename(report_file),
        'total_pairs_reported': total_pairs,
        'pairs_extracted': len(qa_pairs),
        'qa_pairs': qa_pairs,
        'parsed_date': datetime.now().isoformat(),
        'extraction_quality': calculate_quality(total_pairs, len(qa_pairs))
    }

    # Save to JSON
    if output_dir is None:
        output_dir = f"parsed_qa_data/{domain}"

    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{result['topic_slug']}_qa_pairs.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ PARSED: {topic_name}")
    print(f"   Extracted: {len(qa_pairs)} Q&A pairs")
    print(f"   Reported: {total_pairs} Q&A pairs")
    print(f"   Quality: {result['extraction_quality']}")
    print(f"   Saved: {output_file}\n")

    return result


def extract_topic_name(filepath, content):
    """Extract topic name from filename or content"""
    # Try filename first: research_report_topic_name_20241102.txt
    filename = os.path.basename(filepath)
    match = re.search(r'research_report_(.+?)_\d{8}', filename)
    if match:
        topic = match.group(1).replace('_', ' ').title()
        return topic

    # Try content: look for "Research Topic: X" or similar
    topic_match = re.search(r'(?:Research Topic|Topic|Subject):\s*(.+?)(?:\n|$)', content)
    if topic_match:
        return topic_match.group(1).strip()

    # Fallback to filename without extension
    return Path(filepath).stem.replace('_', ' ').title()


def extract_total_pairs(content):
    """Extract total Q&A pair count from report"""
    # Look for "Total Question-Answer Pairs: 123"
    total_match = re.search(r'Total Question-Answer Pairs:.*?(\d{2,})', content)
    if total_match:
        return int(total_match.group(1))

    # Look for "Generated X Q&A pairs"
    gen_match = re.search(r'Generated\s+(\d+)\s+Q&A', content, re.IGNORECASE)
    if gen_match:
        return int(gen_match.group(1))

    return 0


def extract_qa_pairs(content, topic_name):
    """Extract all Q&A pairs from content"""
    qa_pairs = []

    # Split by pair markers: "Pair 1:", "Pair 2:", etc.
    pair_sections = re.split(r'Pair (\d+):', content)

    # Process each pair section
    for i in range(1, len(pair_sections), 2):
        pair_num = int(pair_sections[i])
        pair_content = pair_sections[i+1]

        # Extract question and answer
        question, answer = extract_qa_from_section(pair_content)

        if question and answer:
            qa_pairs.append({
                'pair_number': pair_num,
                'question': question,
                'answer': answer,
                'topic': topic_name,
                'created_date': datetime.now().isoformat()
            })

    return qa_pairs


def extract_qa_from_section(section):
    """Extract question and answer from a pair section"""
    # Look for "Question:" and "Answer:" markers
    q_match = re.search(r'Question:\s*(.*?)(?=Answer:|$)', section, re.DOTALL | re.IGNORECASE)
    a_match = re.search(r'Answer:\s*(.*?)(?=Pair \d+:|$)', section, re.DOTALL | re.IGNORECASE)

    question = q_match.group(1).strip() if q_match else ""
    answer = a_match.group(1).strip() if a_match else ""

    # Clean up extra whitespace
    question = re.sub(r'\s+', ' ', question)
    answer = re.sub(r'\s+', ' ', answer)

    return question, answer


def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    return text


def calculate_quality(reported, extracted):
    """Calculate extraction quality percentage"""
    if reported == 0:
        return "unknown"

    percentage = (extracted / reported) * 100

    if percentage >= 95:
        return "excellent"
    elif percentage >= 85:
        return "good"
    elif percentage >= 70:
        return "acceptable"
    else:
        return "needs_review"


def parse_batch(input_dir, domain="general", pattern="research_report_*.txt"):
    """
    Parse all research reports in a directory

    Args:
        input_dir: Directory containing research_report_*.txt files
        domain: Domain identifier
        pattern: Filename pattern to match

    Returns:
        list: Results for all parsed files
    """
    from glob import glob

    reports = glob(f"{input_dir}/{pattern}")

    print(f"\n{'='*60}")
    print(f"BATCH PARSING: {len(reports)} reports")
    print(f"DOMAIN: {domain}")
    print(f"{'='*60}\n")

    results = []
    for report in reports:
        result = parse_research_report(report, domain)
        results.append(result)

    # Summary
    total_extracted = sum(r['pairs_extracted'] for r in results)
    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE")
    print(f"Files: {len(results)}")
    print(f"Total Q&A: {total_extracted}")
    print(f"Average: {total_extracted / len(results):.1f} per file")
    print(f"{'='*60}\n")

    return results


# CLI Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single file: python parse_domain_research.py <file> [domain]")
        print("  Batch:       python parse_domain_research.py --batch <dir> [domain]")
        print("\nExamples:")
        print("  python parse_domain_research.py research_report_sma_20241102.txt crypto_indicators")
        print("  python parse_domain_research.py --batch inbox/droid web_development")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        input_dir = sys.argv[2]
        domain = sys.argv[3] if len(sys.argv) > 3 else "general"
        parse_batch(input_dir, domain)
    else:
        file_path = sys.argv[1]
        domain = sys.argv[2] if len(sys.argv) > 2 else "general"
        parse_research_report(file_path, domain)
