"""
Pipeline Status Checker
Check progress of your multi-agent pipeline without interrupting it
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def check_pipeline_status():
    """Check the current status of the pipeline"""
    output_dir = Path("multi_agent_output")
    
    print("="*80)
    print("PIPELINE STATUS CHECK")
    print("="*80)
    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Find latest task list
    task_list_dir = output_dir / "task_lists"
    if not task_list_dir.exists():
        print("[INFO] No task lists found. Pipeline hasn't started.")
        return
    
    task_lists = list(task_list_dir.glob("*_task_list_*.json"))
    if not task_lists:
        print("[INFO] No task lists found.")
        return
    
    latest_task_list = max(task_lists, key=lambda p: p.stat().st_mtime)
    
    with open(latest_task_list, 'r', encoding='utf-8') as f:
        task_data = json.load(f)
    
    topic = task_data.get("topic", "Unknown")
    subtopics = task_data.get("subtopics", [])
    total_subtopics = len(subtopics)
    
    print(f"[TOPIC] {topic}")
    print(f"[TOTAL SUBTOPICS] {total_subtopics}")
    print()
    
    # Check each stage
    questions_dir = output_dir / "questions"
    research_dir = output_dir / "research"
    answers_dir = output_dir / "answers"
    
    # Count files per subtopic
    questions_by_subtopic = defaultdict(int)
    research_by_subtopic = defaultdict(int)
    answers_by_subtopic = defaultdict(int)
    
    if questions_dir.exists():
        for q_file in questions_dir.glob("*_questions_*.json"):
            try:
                with open(q_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    idx = data.get("subtopic_index", -1)
                    if idx >= 0:
                        questions_by_subtopic[idx] = data.get("total_questions", 0)
            except:
                pass
    
    if research_dir.exists():
        for r_file in research_dir.glob("*_research_*.json"):
            try:
                with open(r_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Try to match by subtopic name
                    subtopic_name = data.get("subtopic", "")
                    for idx, st in enumerate(subtopics):
                        if subtopic_name in st or st in subtopic_name:
                            research_by_subtopic[idx] = len(data.get("research_results", {}))
                            break
            except:
                pass
    
    if answers_dir.exists():
        for a_file in answers_dir.glob("*_qa_pairs_*.json"):
            try:
                with open(a_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    subtopic_name = data.get("subtopic", "")
                    for idx, st in enumerate(subtopics):
                        if subtopic_name in st or st in subtopic_name:
                            answers_by_subtopic[idx] = data.get("total_pairs", 0)
                            break
            except:
                pass
    
    # Summary statistics
    print("="*80)
    print("PROGRESS SUMMARY")
    print("="*80)
    
    completed_subtopics = []
    in_progress_subtopics = []
    pending_subtopics = []
    
    for idx, subtopic in enumerate(subtopics):
        has_questions = idx in questions_by_subtopic
        has_research = idx in research_by_subtopic
        has_answers = idx in answers_by_subtopic
        
        if has_answers:
            completed_subtopics.append(idx)
        elif has_research or has_questions:
            in_progress_subtopics.append(idx)
        else:
            pending_subtopics.append(idx)
    
    print(f"\n[COMPLETED] {len(completed_subtopics)} subtopics")
    print(f"[IN PROGRESS] {len(in_progress_subtopics)} subtopics")
    print(f"[PENDING] {len(pending_subtopics)} subtopics")
    print()
    
    # Show detailed progress
    print("="*80)
    print("DETAILED PROGRESS")
    print("="*80)
    
    for idx, subtopic in enumerate(subtopics):
        q_count = questions_by_subtopic.get(idx, 0)
        r_count = research_by_subtopic.get(idx, 0)
        a_count = answers_by_subtopic.get(idx, 0)
        
        if a_count > 0:
            status = "[COMPLETE]"
        elif r_count > 0:
            status = "[RESEARCHING]"
        elif q_count > 0:
            status = "[QUESTIONS]"
        else:
            status = "[PENDING]"
        
        print(f"{status} [{idx:2d}] {subtopic[:60]}...")
        if q_count > 0 or r_count > 0 or a_count > 0:
            print(f"         Questions: {q_count}, Research: {r_count}, Answers: {a_count}")
    
    print()
    print("="*80)
    
    # Calculate completion percentage
    if total_subtopics > 0:
        completion_pct = (len(completed_subtopics) / total_subtopics) * 100
        print(f"\n[OVERALL PROGRESS] {completion_pct:.1f}% complete")
        print(f"  {len(completed_subtopics)}/{total_subtopics} subtopics finished")
    
    # Estimate time remaining (very rough)
    if completed_subtopics:
        print(f"\n[ESTIMATE] ~{len(pending_subtopics) + len(in_progress_subtopics)} subtopics remaining")
        print(f"          (Each subtopic takes ~2-3 hours with 100 questions)")
    
    print()
    print("="*80)
    
    # Resume command
    if pending_subtopics or in_progress_subtopics:
        next_idx = min(pending_subtopics + in_progress_subtopics)
        print(f"\n[RESUME] To continue from subtopic {next_idx}:")
        print(f'python run_multi_agent.py "{topic}" {next_idx}')
        print(f'\nOr use auto-resume:')
        print(f'python run_multi_agent.py "{topic}" --continue')

if __name__ == "__main__":
    check_pipeline_status()

