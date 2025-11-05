import json
import re
from pathlib import Path

print("=" * 80)
print("EXTRACTING Q&A PAIRS FROM SESSIONS 18-25")
print("=" * 80)

# Find all research report files for sessions 18-25
inbox_droid = Path('inbox/droid')
research_files = []

for session_num in range(18, 26):  # 18-25 inclusive
    pattern = f"research_report_session-{session_num}-*.txt"
    matches = list(inbox_droid.glob(pattern))

    if matches:
        # Take the most recent if multiple exist
        research_file = sorted(matches)[-1]
        research_files.append((session_num, research_file))
        print(f"Found: Session {session_num} -> {research_file.name}")
    else:
        print(f"Warning: Missing: Session {session_num}")

print(f"\n{'='*80}")
print(f"Total research files found: {len(research_files)}")
print(f"{'='*80}\n")

if len(research_files) == 0:
    print("No research files found. Exiting.")
    exit(1)

# Extract Q&A pairs from each file
all_qa_pairs = []

for session_num, file_path in research_files:
    print(f"\nProcessing Session {session_num}: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remove ANSI color codes
    content = re.sub(r'\x1b\[[0-9;]+m', '', content)

    # Find all Pair blocks using simpler pattern
    # Pattern: Pair X: followed by question: and answer:
    pair_pattern = r'Pair\s+(\d+):\s*\n\s*question:\s*(.+?)\s*\n\s*question characters:\s*\d+\s*\n\s*answer:\s*(.+?)(?=\s*\n\s*answer characters:|\s*\n\s*Pair\s+\d+:|\Z)'

    matches = re.findall(pair_pattern, content, re.DOTALL | re.IGNORECASE)

    session_pairs = []

    for match in matches:
        pair_num, question, answer = match

        # Clean up
        question = question.strip().strip('"\'')
        answer = answer.strip()

        if question and answer and len(question) > 10 and len(answer) > 50:
            qa_pair = {
                'pair_id': f"s{session_num}_q{pair_num}",
                'question': question,
                'answer': answer,
                'topic': f"Session {session_num}"
            }
            session_pairs.append(qa_pair)
            all_qa_pairs.append(qa_pair)

    print(f"  Extracted: {len(session_pairs)} Q&A pairs")
    if session_pairs:
        print(f"  Avg question length: {sum(len(p['question']) for p in session_pairs) // len(session_pairs)}")
        print(f"  Avg answer length: {sum(len(p['answer']) for p in session_pairs) // len(session_pairs)}")

print(f"\n{'='*80}")
print(f"EXTRACTION COMPLETE")
print(f"{'='*80}")
print(f"Total Q&A pairs extracted: {len(all_qa_pairs)}")
print(f"Sessions processed: {len(research_files)}")
if research_files:
    print(f"Average pairs per session: {len(all_qa_pairs) // len(research_files)}")

if len(all_qa_pairs) == 0:
    print("\nERROR: No Q&A pairs extracted.")
    print("Checking first file for debugging...")

    if research_files:
        with open(research_files[0][1], 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Remove ANSI codes
        content = re.sub(r'\x1b\[[0-9;]+m', '', content)
        # Find first few Pair markers
        pair_markers = re.findall(r'(Pair\s+\d+:.*?question:.*?answer:.*?answer characters:\s*\d+)', content, re.DOTALL)
        if pair_markers:
            print(f"\nFound {len(pair_markers)} pair markers. Showing first one:")
            print(pair_markers[0][:500])
    exit(1)

# Save extracted pairs
output_file = Path('inbox/sessions_18_25_extracted.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'extraction_date': '2025-11-02',
        'sessions': [s for s, _ in research_files],
        'total_pairs': len(all_qa_pairs),
        'qa_pairs': all_qa_pairs
    }, f, indent=2, ensure_ascii=False)

print(f"\nExtracted data saved to: {output_file}")
print(f"Ready to add to refinement pipeline!")
