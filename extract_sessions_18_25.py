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
        print(f"⚠️  Missing: Session {session_num}")

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

    # Parse Q&A pairs from the research report format
    # These files typically have "Question:" and "Answer:" markers

    # Split by question markers
    qa_blocks = re.split(r'\n(?:Question|Q):\s*', content, flags=re.IGNORECASE)

    session_pairs = []

    for i, block in enumerate(qa_blocks[1:], 1):  # Skip first empty split
        # Split into question and answer
        parts = re.split(r'\n(?:Answer|A):\s*', block, maxsplit=1, flags=re.IGNORECASE)

        if len(parts) == 2:
            question = parts[0].strip()
            answer = parts[1].strip()

            # Clean up the answer (remove extra markers, formatting)
            # Stop at next question or end markers
            answer = re.split(r'\n(?:Question|Q):', answer, maxsplit=1, flags=re.IGNORECASE)[0]
            answer = answer.strip()

            if question and answer and len(question) > 10 and len(answer) > 50:
                qa_pair = {
                    'pair_id': f"s{session_num}_q{i}",
                    'question': question,
                    'answer': answer,
                    'topic': f"Session {session_num}"
                }
                session_pairs.append(qa_pair)
                all_qa_pairs.append(qa_pair)

    print(f"  Extracted: {len(session_pairs)} Q&A pairs")
    print(f"  Avg question length: {sum(len(p['question']) for p in session_pairs) // len(session_pairs) if session_pairs else 0}")
    print(f"  Avg answer length: {sum(len(p['answer']) for p in session_pairs) // len(session_pairs) if session_pairs else 0}")

print(f"\n{'='*80}")
print(f"EXTRACTION COMPLETE")
print(f"{'='*80}")
print(f"Total Q&A pairs extracted: {len(all_qa_pairs)}")
print(f"Sessions processed: {len(research_files)}")

if len(all_qa_pairs) == 0:
    print("\n⚠️  No Q&A pairs extracted. May need to adjust parsing logic.")
    print("Let me check the file format...")

    if research_files:
        sample_file = research_files[0][1]
        with open(sample_file, 'r', encoding='utf-8', errors='ignore') as f:
            sample_content = f.read(2000)

        print(f"\nFirst 2000 chars of {sample_file.name}:")
        print("="*80)
        print(sample_content)
        print("="*80)

    exit(1)

# Save extracted pairs
output_file = Path('inbox/sessions_18_25_extracted.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'extraction_date': '2025-11-02',
        'sessions': list(range(18, 26)),
        'total_pairs': len(all_qa_pairs),
        'qa_pairs': all_qa_pairs
    }, f, indent=2, ensure_ascii=False)

print(f"\nExtracted data saved to: {output_file}")
print(f"\nReady to add to refinement pipeline!")
