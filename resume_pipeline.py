"""
Resume Pipeline Helper
Automatically detects where to resume from based on output files
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def find_latest_task_list(output_dir: Path):
    """Find the most recent task list file"""
    task_list_dir = output_dir / "task_lists"
    if not task_list_dir.exists():
        return None
    
    task_lists = list(task_list_dir.glob("*_task_list_*.json"))
    if not task_lists:
        return None
    
    # Sort by modification time, get most recent
    latest = max(task_lists, key=lambda p: p.stat().st_mtime)
    return latest

def find_completed_subtopics(output_dir: Path, topic: str):
    """Find which subtopics have completed Q&A pairs"""
    answers_dir = output_dir / "answers"
    if not answers_dir.exists():
        return []
    
    completed = []
    answer_files = list(answers_dir.glob("*_qa_pairs_*.json"))
    
    for answer_file in answer_files:
        try:
            with open(answer_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get("topic") == topic or topic.lower() in data.get("topic", "").lower():
                    subtopic = data.get("subtopic", "")
                    subtopic_index = data.get("subtopic_index", -1)
                    if subtopic_index >= 0:
                        completed.append(subtopic_index)
        except:
            continue
    
    return sorted(set(completed))

def get_subtopics_from_task_list(task_list_path: Path):
    """Load subtopics from task list"""
    with open(task_list_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("subtopics", []), data.get("topic", "")

def main():
    output_dir = Path("multi_agent_output")
    
    print("="*80)
    print("PIPELINE RESUME HELPER")
    print("="*80)
    print()
    
    # Find latest task list
    task_list_path = find_latest_task_list(output_dir)
    if not task_list_path:
        print("[ERROR] No task list found. Run the pipeline from the beginning.")
        print("Usage: python run_multi_agent.py \"Your Topic\"")
        sys.exit(1)
    
    print(f"[FOUND] Task list: {task_list_path.name}")
    
    # Load subtopics
    subtopics, topic = get_subtopics_from_task_list(task_list_path)
    print(f"[TOPIC] {topic}")
    print(f"[SUBTOPICS] {len(subtopics)} total")
    print()
    
    # Find completed subtopics
    completed = find_completed_subtopics(output_dir, topic)
    
    if completed:
        print(f"[COMPLETED] Subtopics: {completed}")
        print(f"[LAST COMPLETED] Subtopic index: {max(completed)}")
        next_index = max(completed) + 1
    else:
        print("[COMPLETED] No subtopics completed yet")
        next_index = 0
    
    print()
    print("="*80)
    print("RESUME COMMAND")
    print("="*80)
    print()
    
    if next_index >= len(subtopics):
        print("[INFO] All subtopics completed!")
        print(f"[INFO] Processed {len(subtopics)} subtopics")
    else:
        print(f"To resume from subtopic {next_index} ({subtopics[next_index][:60]}...):")
        print()
        print(f'python run_multi_agent.py "{topic}" {next_index}')
        print()
        print("Or to start from the beginning:")
        print(f'python run_multi_agent.py "{topic}"')
    
    print()
    print("="*80)
    
    # Show subtopic list
    print("\nSubtopics:")
    for idx, subtopic in enumerate(subtopics):
        status = "[OK]" if idx in completed else "[PENDING]"
        print(f"  {status} [{idx}] {subtopic[:70]}...")

if __name__ == "__main__":
    main()

