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
    content = re.sub(r'\[[0-9;]+m', '', content)

    # Find the Q&A pairs section
    qa_section_match = re.search(r'QUESTION-ANSWER PAIRS WITH CHARACTER COUNTS.*?(?=\n\n\n|\Z)', content, re.DOTALL)

    if not qa_section_match:
        print(f"  ERROR: Could not find Q&A section")
        continue

    qa_section = qa_section_match.group()

    # Split into individual pairs
    pair_blocks = re.split(r'Pair \d+:', qa_section)

    session_pairs = []

    for pair_block in pair_blocks[1:]:  # Skip first empty split
        # Extract question
        question_match = re.search(r'question:\s*(.+?)(?:\nquestion characters:|\nanswer:)', pair_block, re.DOTALL)
        # Extract answer
        answer_match = re.search(r'answer:\s*(.+?)(?:\nanswer characters:|\nPair \d+:|\Z)', pair_block, re.DOTALL)

        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()

            # Clean up
            question = question.strip('"\'')
            answer = answer.strip()

            if question and answer and len(question) > 10 and len(answer) > 50:
                qa_pair = {
                    'pair_id': f"s{session_num}_q{len(session_pairs)+1}",
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
print(f"Average pairs per session: {len(all_qa_pairs) // len(research_files) if research_files else 0}")

if len(all_qa_pairs) == 0:
    print("\nERROR: No Q&A pairs extracted.")
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
