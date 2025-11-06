"""
Task Stack Management System
============================

Manages priority queue of tasks for perpetual mining operation.

Usage:
    # Initialize
    python task_stack.py init

    # Add task
    python task_stack.py add --task "integrate_sessions_101_120" --priority 1

    # Get next task
    python task_stack.py next

    # Update progress
    python task_stack.py update integrate_sessions_101_120 --progress 15/20

    # Complete task
    python task_stack.py complete integrate_sessions_101_120 --grade A

    # List all tasks
    python task_stack.py list
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class TaskStack:
    """
    Priority-based task queue for perpetual mining operation.
    """

    def __init__(self, storage_path: str = "task_stack.json"):
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not self.storage_path.exists():
            self._write_storage({
                "tasks": {},
                "completed": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            })

    def _read_storage(self) -> Dict:
        """Read storage file"""
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def _write_storage(self, data: Dict):
        """Write to storage file"""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_task(self, task_id: str, priority: int = 5,
                 description: str = "", estimated_tokens: int = 50000,
                 dependencies: List[str] = None, metadata: Dict = None):
        """
        Add a new task to the stack.

        Args:
            task_id: Unique identifier for the task
            priority: Priority level (1=highest, 10=lowest)
            description: Human-readable description
            estimated_tokens: Estimated token budget needed
            dependencies: List of task_ids that must complete first
            metadata: Additional task metadata
        """
        data = self._read_storage()

        task = {
            "task_id": task_id,
            "priority": priority,
            "description": description,
            "status": "pending",
            "estimated_tokens": estimated_tokens,
            "actual_tokens": 0,
            "dependencies": dependencies or [],
            "progress": {
                "current": 0,
                "total": 0,
                "percentage": 0
            },
            "checkpoints": [],
            "assigned_to": None,
            "created": datetime.now().isoformat(),
            "started": None,
            "completed": None,
            "grade": None,
            "metadata": metadata or {}
        }

        data["tasks"][task_id] = task
        self._write_storage(data)
        print(f"[SUCCESS] Task '{task_id}' added with priority {priority}")

    def get_next_task(self) -> Optional[Dict]:
        """
        Get the next task to execute based on priority and dependencies.

        Returns:
            Task dict or None if no tasks available
        """
        data = self._read_storage()

        # Filter to pending tasks
        pending_tasks = [
            (tid, task) for tid, task in data["tasks"].items()
            if task["status"] == "pending"
        ]

        if not pending_tasks:
            print("[INFO] No pending tasks in queue")
            return None

        # Filter out tasks with unmet dependencies
        available_tasks = []
        for tid, task in pending_tasks:
            # Check if all dependencies are completed
            deps_met = all(
                data["completed"].get(dep_id) is not None
                for dep_id in task["dependencies"]
            )
            if deps_met:
                available_tasks.append((tid, task))

        if not available_tasks:
            print("[INFO] No tasks with met dependencies")
            return None

        # Sort by priority (lower number = higher priority)
        available_tasks.sort(key=lambda x: x[1]["priority"])

        next_task_id, next_task = available_tasks[0]
        print(f"[SUCCESS] Next task: {next_task_id} (Priority {next_task['priority']})")
        return next_task

    def start_task(self, task_id: str, assigned_to: str = "claude_code"):
        """Mark a task as in progress"""
        data = self._read_storage()

        if task_id not in data["tasks"]:
            print(f"[ERROR] Task '{task_id}' not found")
            return False

        data["tasks"][task_id]["status"] = "in_progress"
        data["tasks"][task_id]["started"] = datetime.now().isoformat()
        data["tasks"][task_id]["assigned_to"] = assigned_to

        self._write_storage(data)
        print(f"[SUCCESS] Task '{task_id}' started by {assigned_to}")
        return True

    def update_progress(self, task_id: str, current: int, total: int,
                       tokens_used: int = 0, checkpoint: str = None):
        """
        Update task progress.

        Args:
            task_id: Task identifier
            current: Current units completed
            total: Total units to complete
            tokens_used: Tokens used so far
            checkpoint: Optional checkpoint description
        """
        data = self._read_storage()

        if task_id not in data["tasks"]:
            print(f"[ERROR] Task '{task_id}' not found")
            return False

        task = data["tasks"][task_id]
        task["progress"]["current"] = current
        task["progress"]["total"] = total
        task["progress"]["percentage"] = (current / total * 100) if total > 0 else 0
        task["actual_tokens"] += tokens_used

        if checkpoint:
            task["checkpoints"].append({
                "checkpoint": checkpoint,
                "timestamp": datetime.now().isoformat(),
                "progress": current,
                "tokens": task["actual_tokens"]
            })

        self._write_storage(data)
        print(f"[SUCCESS] Progress updated: {current}/{total} ({task['progress']['percentage']:.1f}%)")
        return True

    def complete_task(self, task_id: str, grade: str = "N/A",
                     final_tokens: int = 0, report: Dict = None):
        """
        Mark a task as completed.

        Args:
            task_id: Task identifier
            grade: Performance grade (A-F)
            final_tokens: Total tokens used
            report: Completion report data
        """
        data = self._read_storage()

        if task_id not in data["tasks"]:
            print(f"[ERROR] Task '{task_id}' not found")
            return False

        task = data["tasks"][task_id]
        task["status"] = "completed"
        task["completed"] = datetime.now().isoformat()
        task["grade"] = grade
        task["actual_tokens"] = final_tokens
        task["progress"]["current"] = task["progress"]["total"]
        task["progress"]["percentage"] = 100

        if report:
            task["completion_report"] = report

        # Move to completed tasks
        data["completed"][task_id] = task
        del data["tasks"][task_id]

        self._write_storage(data)
        print(f"[SUCCESS] Task '{task_id}' completed with grade {grade}")
        return True

    def list_tasks(self, status: str = "all") -> List[Dict]:
        """
        List tasks filtered by status.

        Args:
            status: Filter by status (all, pending, in_progress, completed)

        Returns:
            List of task dictionaries
        """
        data = self._read_storage()

        if status == "all":
            active = list(data["tasks"].values())
            completed = list(data["completed"].values())
            tasks = active + completed
        elif status == "completed":
            tasks = list(data["completed"].values())
        else:
            tasks = [
                task for task in data["tasks"].values()
                if task["status"] == status
            ]

        return tasks

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        data = self._read_storage()

        if task_id in data["tasks"]:
            return data["tasks"][task_id]
        elif task_id in data["completed"]:
            return data["completed"][task_id]
        else:
            return None

    def get_statistics(self) -> Dict:
        """Get task statistics"""
        data = self._read_storage()

        pending = [t for t in data["tasks"].values() if t["status"] == "pending"]
        in_progress = [t for t in data["tasks"].values() if t["status"] == "in_progress"]
        completed = list(data["completed"].values())

        total_estimated_tokens = sum(t["estimated_tokens"] for t in pending + in_progress)
        total_actual_tokens = sum(t["actual_tokens"] for t in completed)

        grade_distribution = {}
        for task in completed:
            grade = task.get("grade", "N/A")
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

        return {
            "total_tasks": len(pending) + len(in_progress) + len(completed),
            "pending": len(pending),
            "in_progress": len(in_progress),
            "completed": len(completed),
            "estimated_tokens_remaining": total_estimated_tokens,
            "actual_tokens_used": total_actual_tokens,
            "grade_distribution": grade_distribution,
            "completion_rate": len(completed) / (len(completed) + len(pending) + len(in_progress)) * 100
            if (len(completed) + len(pending) + len(in_progress)) > 0 else 0
        }


# CLI Interface
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Task Stack Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init
    subparsers.add_parser("init", help="Initialize task stack")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--task", required=True, help="Task ID")
    add_parser.add_argument("--priority", type=int, default=5, help="Priority (1-10)")
    add_parser.add_argument("--description", default="", help="Task description")
    add_parser.add_argument("--estimated-tokens", type=int, default=50000, help="Estimated tokens")

    # Get next
    subparsers.add_parser("next", help="Get next task")

    # Start task
    start_parser = subparsers.add_parser("start", help="Start a task")
    start_parser.add_argument("task_id", help="Task ID")

    # Update progress
    update_parser = subparsers.add_parser("update", help="Update task progress")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--progress", required=True, help="Progress (e.g., 15/20)")
    update_parser.add_argument("--tokens", type=int, default=0, help="Tokens used")
    update_parser.add_argument("--checkpoint", help="Checkpoint description")

    # Complete task
    complete_parser = subparsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("task_id", help="Task ID")
    complete_parser.add_argument("--grade", default="N/A", help="Grade (A-F)")
    complete_parser.add_argument("--tokens", type=int, default=0, help="Total tokens used")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", default="all",
                           choices=["all", "pending", "in_progress", "completed"],
                           help="Filter by status")

    # Statistics
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    stack = TaskStack()

    if args.command == "init":
        print("[SUCCESS] Task stack initialized")

    elif args.command == "add":
        stack.add_task(
            task_id=args.task,
            priority=args.priority,
            description=args.description,
            estimated_tokens=args.estimated_tokens
        )

    elif args.command == "next":
        task = stack.get_next_task()
        if task:
            print(f"\nTask ID: {task['task_id']}")
            print(f"Description: {task['description']}")
            print(f"Priority: {task['priority']}")
            print(f"Estimated tokens: {task['estimated_tokens']:,}")

    elif args.command == "start":
        stack.start_task(args.task_id)

    elif args.command == "update":
        current, total = map(int, args.progress.split("/"))
        stack.update_progress(
            task_id=args.task_id,
            current=current,
            total=total,
            tokens_used=args.tokens,
            checkpoint=args.checkpoint
        )

    elif args.command == "complete":
        stack.complete_task(
            task_id=args.task_id,
            grade=args.grade,
            final_tokens=args.tokens
        )

    elif args.command == "list":
        tasks = stack.list_tasks(status=args.status)
        if not tasks:
            print(f"[INFO] No {args.status} tasks")
        else:
            print(f"\n{'='*80}")
            print(f"{args.status.upper()} TASKS ({len(tasks)})")
            print(f"{'='*80}\n")
            for task in sorted(tasks, key=lambda t: t.get("priority", 99)):
                status_symbol = {
                    "pending": "[PENDING]",
                    "in_progress": "[ACTIVE]",
                    "completed": "[DONE]"
                }.get(task["status"], "[?]")
                print(f"{status_symbol} [{task['priority']}] {task['task_id']}")
                print(f"   {task['description']}")
                if task['progress']['total'] > 0:
                    print(f"   Progress: {task['progress']['current']}/{task['progress']['total']} ({task['progress']['percentage']:.1f}%)")
                if task.get("grade"):
                    print(f"   Grade: {task['grade']}")
                print()

    elif args.command == "stats":
        stats = stack.get_statistics()
        print(f"\n{'='*60}")
        print(f"TASK STACK STATISTICS")
        print(f"{'='*60}")
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Pending: {stats['pending']}")
        print(f"In Progress: {stats['in_progress']}")
        print(f"Completed: {stats['completed']}")
        print(f"Completion Rate: {stats['completion_rate']:.1f}%")
        print(f"\nEstimated Tokens Remaining: {stats['estimated_tokens_remaining']:,}")
        print(f"Actual Tokens Used: {stats['actual_tokens_used']:,}")
        print(f"\nGrade Distribution:")
        for grade, count in sorted(stats['grade_distribution'].items()):
            print(f"  {grade}: {count}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
