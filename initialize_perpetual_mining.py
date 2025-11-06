"""
Initialize Perpetual Mining System
===================================

Quick setup script to initialize the perpetual mining system
with your current project tasks.

Usage:
    python initialize_perpetual_mining.py
"""

from task_stack import TaskStack
from session_orchestrator import SessionOrchestrator


def initialize_system():
    """Initialize perpetual mining system with default tasks"""

    print("="*80)
    print("INITIALIZING PERPETUAL MINING SYSTEM")
    print("="*80)
    print()

    # Initialize task stack
    print("[1/3] Initializing task stack...")
    stack = TaskStack()
    print("      Task stack ready")

    # Initialize session orchestrator (creates config)
    print("[2/3] Initializing session orchestrator...")
    orchestrator = SessionOrchestrator()
    print("      Configuration created")

    # Add default tasks for your project
    print("[3/3] Adding default tasks...")

    tasks = [
        {
            "task_id": "integrate_sessions_101_140",
            "priority": 1,
            "description": "Integrate RAG export sessions 101-140 (~4,000 pairs)",
            "estimated_tokens": 100000
        },
        {
            "task_id": "integrate_claude_shared",
            "priority": 2,
            "description": "Integrate original training database (~2,000-7,000 unique pairs)",
            "estimated_tokens": 60000
        },
        {
            "task_id": "integrate_sessions_141_187",
            "priority": 3,
            "description": "Integrate RAG export sessions 141-187 (~4,700 pairs)",
            "estimated_tokens": 120000
        },
        {
            "task_id": "quality_analysis_full_database",
            "priority": 4,
            "description": "Run comprehensive quality analysis on entire database",
            "estimated_tokens": 40000
        },
        {
            "task_id": "embeddings_generation_batch_1",
            "priority": 5,
            "description": "Generate embeddings for first 10,000 pairs",
            "estimated_tokens": 30000
        },
        {
            "task_id": "deduplication_analysis",
            "priority": 6,
            "description": "Identify and remove duplicates via cosine similarity",
            "estimated_tokens": 50000
        }
    ]

    for task in tasks:
        stack.add_task(**task)
        print(f"      Added: {task['task_id']} (Priority {task['priority']})")

    print()
    print("="*80)
    print("INITIALIZATION COMPLETE")
    print("="*80)
    print()

    # Show statistics
    stats = stack.get_statistics()
    print(f"Total tasks added: {stats['pending']}")
    print(f"Estimated total tokens: {stats['estimated_tokens_remaining']:,}")
    print(f"Estimated sessions: {stats['estimated_tokens_remaining'] // 170000} (at 85% per session)")
    print()

    print("Next steps:")
    print("  1. Review tasks: python task_stack.py list")
    print("  2. Customize config: perpetual_mining_config.json")
    print("  3. Start mining: python session_orchestrator.py start")
    print()
    print("="*80)


def show_system_overview():
    """Show overview of the perpetual mining system"""
    print()
    print("="*80)
    print("SYSTEM OVERVIEW")
    print("="*80)
    print()
    print("Files created:")
    print("  [OK] task_stack.json - Your task queue")
    print("  [OK] perpetual_mining_config.json - System configuration")
    print("  [OK] task_stack.py - Task management")
    print("  [OK] session_orchestrator.py - Session lifecycle manager")
    print("  [OK] token_monitor_simple.py - Token usage monitor")
    print()
    print("Directories that will be created:")
    print("  * session_handoffs/ - Handoff documents for each wrap")
    print("  * session_logs/ - Detailed session logs (future)")
    print()
    print("How it works:")
    print("  1. Start session - Pulls next task from queue")
    print("  2. Work on task - Monitor tokens periodically")
    print("  3. Hit 85% tokens - Wrap session (auto-commit)")
    print("  4. Fresh start - Resume or move to next task")
    print("  5. Repeat forever - Never stop building")
    print()
    print("="*80)


if __name__ == "__main__":
    initialize_system()
    show_system_overview()

    print()
    print("[READY] READY TO START PERPETUAL MINING!")
    print()
    print("Run: python session_orchestrator.py start")
    print()
