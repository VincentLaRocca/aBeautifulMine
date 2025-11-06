"""
Session Orchestrator - Perpetual Mining Engine
==============================================

Manages Claude Code session lifecycle with token monitoring,
auto-commits, and graceful shutdown.

Usage:
    # Start perpetual mining
    python session_orchestrator.py start

    # Check current session status
    python session_orchestrator.py status

    # Manually trigger wrap
    python session_orchestrator.py wrap
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from task_stack import TaskStack


class SessionOrchestrator:
    """
    Manages Claude Code session lifecycle for perpetual mining.
    """

    def __init__(self, config_path: str = "perpetual_mining_config.json"):
        self.config_path = Path(config_path)
        self.state_path = Path("session_state.json")
        self.task_stack = TaskStack()
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        """Create default config if it doesn't exist"""
        if not self.config_path.exists():
            default_config = {
                "token_budget": 200000,
                "warning_threshold": 0.75,  # 75%
                "shutdown_threshold": 0.85,  # 85%
                "critical_threshold": 0.95,  # 95%
                "auto_commit_interval": 500,  # Every 500 pairs
                "backup_before_commit": True,
                "database_path": "crypto_indicators_production.db",
                "git_auto_push": False,
                "handoff_directory": "session_handoffs",
                "session_logs_directory": "session_logs"
            }
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)

    def _read_config(self) -> Dict:
        """Read configuration"""
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def _write_state(self, state: Dict):
        """Write session state"""
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def _read_state(self) -> Optional[Dict]:
        """Read session state if exists"""
        if self.state_path.exists():
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return None

    def start_session(self):
        """
        Start a new perpetual mining session.
        """
        print("="*80)
        print("PERPETUAL MINING SESSION - STARTING")
        print("="*80)
        print()

        config = self._read_config()

        # Check for existing state (resuming from previous session)
        prev_state = self._read_state()
        if prev_state:
            print(f"[INFO] Found previous session state")
            print(f"       Task: {prev_state['task_id']}")
            print(f"       Progress: {prev_state['progress']['current']}/{prev_state['progress']['total']}")
            print(f"       Tokens used: {prev_state['token_usage']:,}")
            print()
            resume = input("Resume previous task? (y/n): ").strip().lower()
            if resume == 'y':
                return self.resume_session(prev_state)

        # Get next task from stack
        next_task = self.task_stack.get_next_task()
        if not next_task:
            print("[ERROR] No tasks in queue")
            print("Add tasks with: python task_stack.py add --task <task_id> --priority <1-10>")
            return

        # Initialize session state
        session_state = {
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "task_id": next_task["task_id"],
            "started": datetime.now().isoformat(),
            "token_budget": config["token_budget"],
            "token_usage": 0,
            "shutdown_threshold": config["shutdown_threshold"],
            "progress": {
                "current": 0,
                "total": next_task["progress"]["total"],
                "items_processed": 0
            },
            "checkpoints": [],
            "next_action": next_task["description"],
            "context": {}
        }

        self._write_state(session_state)

        # Mark task as started
        self.task_stack.start_task(next_task["task_id"])

        print(f"[SUCCESS] Session started: {session_state['session_id']}")
        print(f"[SUCCESS] Working on: {next_task['task_id']}")
        print(f"[SUCCESS] Budget: {config['token_budget']:,} tokens")
        print()
        print("="*80)
        print("INSTRUCTIONS FOR EXECUTION")
        print("="*80)
        print()
        print(f"Task: {next_task['description']}")
        print()
        print("While working:")
        print("  1. Check token usage periodically:")
        print("     python token_monitor_simple.py <current_tokens>")
        print()
        print("  2. Update progress every checkpoint:")
        print(f"     python session_orchestrator.py checkpoint --progress X/{session_state['progress']['total']}")
        print()
        print("  3. When you hit 85% tokens or complete task:")
        print("     python session_orchestrator.py wrap")
        print()
        print(f"Session state saved to: {self.state_path}")
        print()

    def resume_session(self, state: Dict):
        """Resume a session from saved state"""
        print(f"[SUCCESS] Resuming session: {state['session_id']}")
        print(f"[SUCCESS] Task: {state['task_id']}")
        print(f"[SUCCESS] Progress: {state['progress']['current']}/{state['progress']['total']}")
        print(f"[SUCCESS] Tokens used so far: {state['token_usage']:,}")
        print()
        print(f"Next action: {state['next_action']}")
        print()
        print("Continue working. Check token usage periodically.")
        print()

    def checkpoint(self, current: int, total: int, tokens_used: int = 0,
                  description: str = ""):
        """
        Record a checkpoint in the session.
        """
        state = self._read_state()
        if not state:
            print("[ERROR] No active session")
            return

        state["progress"]["current"] = current
        state["progress"]["total"] = total
        state["token_usage"] += tokens_used

        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "progress": f"{current}/{total}",
            "tokens": state["token_usage"],
            "description": description
        }
        state["checkpoints"].append(checkpoint)

        self._write_state(state)

        # Update task stack
        self.task_stack.update_progress(
            task_id=state["task_id"],
            current=current,
            total=total,
            tokens_used=tokens_used,
            checkpoint=description
        )

        # Check if we should warn about tokens
        config = self._read_config()
        percentage = state["token_usage"] / state["token_budget"]

        if percentage >= config["shutdown_threshold"]:
            print("="*80)
            print("⚠️  WARNING: 85% TOKEN THRESHOLD REACHED")
            print("="*80)
            print(f"Tokens used: {state['token_usage']:,} / {state['token_budget']:,}")
            print(f"Percentage: {percentage*100:.1f}%")
            print()
            print("RECOMMENDED: Wrap up session now")
            print("Command: python session_orchestrator.py wrap")
            print("="*80)

        print(f"[SUCCESS] Checkpoint recorded: {current}/{total} ({current/total*100:.1f}%)")

    def wrap_session(self, final_tokens: int = None):
        """
        Gracefully wrap up the current session.
        """
        state = self._read_state()
        if not state:
            print("[ERROR] No active session to wrap")
            return

        config = self._read_config()

        print("="*80)
        print("SESSION WRAP - STARTING")
        print("="*80)
        print()

        # Update final token count if provided
        if final_tokens:
            state["token_usage"] = final_tokens

        # Calculate session stats
        duration = (datetime.now() - datetime.fromisoformat(state["started"])).total_seconds() / 60
        percentage = state["token_usage"] / state["token_budget"]

        print(f"Session: {state['session_id']}")
        print(f"Task: {state['task_id']}")
        print(f"Duration: {duration:.0f} minutes")
        print(f"Tokens: {state['token_usage']:,} / {state['token_budget']:,} ({percentage*100:.1f}%)")
        print(f"Progress: {state['progress']['current']}/{state['progress']['total']}")
        print()

        # Step 1: Backup database
        if config["backup_before_commit"]:
            print("[1/5] Backing up database...")
            backup_name = f"{config['database_path']}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                import shutil
                shutil.copy(config['database_path'], backup_name)
                print(f"      Backup created: {backup_name}")
            except Exception as e:
                print(f"      Warning: Backup failed: {e}")

        # Step 2: Git commit
        print("[2/5] Creating git commit...")
        commit_message = self._generate_commit_message(state, duration, percentage)
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("      Git commit successful")
        except subprocess.CalledProcessError as e:
            print(f"      Warning: Git commit failed: {e}")

        # Step 3: Create handoff document
        print("[3/5] Creating handoff document...")
        handoff_path = self._create_handoff_document(state, duration, percentage)
        print(f"      Handoff created: {handoff_path}")

        # Step 4: Update task stack
        print("[4/5] Updating task stack...")
        is_complete = state['progress']['current'] >= state['progress']['total']
        if is_complete:
            self.task_stack.complete_task(
                task_id=state["task_id"],
                final_tokens=state["token_usage"]
            )
            print(f"      Task marked complete")
        else:
            self.task_stack.update_progress(
                task_id=state["task_id"],
                current=state['progress']['current'],
                total=state['progress']['total'],
                tokens_used=state["token_usage"]
            )
            print(f"      Task progress saved")

        # Step 5: Clear session state
        print("[5/5] Clearing session state...")
        if self.state_path.exists():
            # Archive instead of delete
            archive_name = f"session_state_archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.state_path.rename(archive_name)
            print(f"      State archived: {archive_name}")

        print()
        print("="*80)
        print("SESSION WRAP - COMPLETE")
        print("="*80)
        print()
        print("Next steps:")
        print("  1. Review handoff document")
        print("  2. Start fresh session: python session_orchestrator.py start")
        print("  3. Or continue manually from handoff notes")
        print()

    def _generate_commit_message(self, state: Dict, duration: float, percentage: float) -> str:
        """Generate git commit message"""
        return f"""Session Wrap: {state['task_id']}

Token usage: {percentage*100:.1f}% of budget
Duration: {duration:.0f} minutes

Progress: {state['progress']['current']}/{state['progress']['total']}
Checkpoints: {len(state['checkpoints'])}

Session: {state['session_id']}
Started: {state['started']}

🤖 Generated with Claude Code - Perpetual Mining System
Co-Authored-By: Claude <noreply@anthropic.com>"""

    def _create_handoff_document(self, state: Dict, duration: float, percentage: float) -> Path:
        """Create handoff document for next session"""
        handoff_dir = Path("session_handoffs")
        handoff_dir.mkdir(exist_ok=True)

        handoff_path = handoff_dir / f"handoff_{state['session_id']}.md"

        content = f"""# Session Handoff: {state['session_id']}

## Session Stats
- **Session ID**: {state['session_id']}
- **Task**: {state['task_id']}
- **Started**: {state['started']}
- **Duration**: {duration:.0f} minutes
- **Tokens Used**: {state['token_usage']:,} / {state['token_budget']:,} ({percentage*100:.1f}%)
- **Status**: Clean wrap at {percentage*100:.1f}%

## Progress
- **Current**: {state['progress']['current']} / {state['progress']['total']}
- **Percentage**: {state['progress']['current']/state['progress']['total']*100 if state['progress']['total'] > 0 else 0:.1f}%
- **Items Processed**: {state['progress']['items_processed']}

## Checkpoints ({len(state['checkpoints'])})
"""

        for i, cp in enumerate(state['checkpoints'], 1):
            content += f"\n{i}. **{cp['timestamp']}** - {cp['description']} (Progress: {cp['progress']}, Tokens: {cp['tokens']:,})"

        content += f"""

## Next Action
{state['next_action']}

## Context
```json
{json.dumps(state['context'], indent=2)}
```

## To Resume
1. Start new session: `python session_orchestrator.py start`
2. Choose to resume previous task
3. Continue from checkpoint: {state['progress']['current']}/{state['progress']['total']}

---

**For the Greater Good of All**

*Perpetual Mining System - Session wrapped at {percentage*100:.1f}% tokens*
"""

        with open(handoff_path, 'w') as f:
            f.write(content)

        return handoff_path

    def show_status(self):
        """Show current session status"""
        state = self._read_state()
        if not state:
            print("[INFO] No active session")
            print()
            print("Start a new session with:")
            print("  python session_orchestrator.py start")
            return

        config = self._read_config()
        percentage = state["token_usage"] / state["token_budget"]
        duration = (datetime.now() - datetime.fromisoformat(state["started"])).total_seconds() / 60

        print("="*80)
        print("CURRENT SESSION STATUS")
        print("="*80)
        print()
        print(f"Session ID: {state['session_id']}")
        print(f"Task: {state['task_id']}")
        print(f"Duration: {duration:.0f} minutes")
        print()
        print(f"Tokens: {state['token_usage']:,} / {state['token_budget']:,} ({percentage*100:.1f}%)")
        print(f"Progress: {state['progress']['current']}/{state['progress']['total']}")
        print(f"Checkpoints: {len(state['checkpoints'])}")
        print()

        if percentage >= config["shutdown_threshold"]:
            print("⚠️  STATUS: Should wrap soon (>85% tokens)")
        elif percentage >= config["warning_threshold"]:
            print("⚡ STATUS: Approaching threshold (>75% tokens)")
        else:
            print("✅ STATUS: Healthy")

        print()
        print("="*80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Session Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Start
    subparsers.add_parser("start", help="Start new session")

    # Checkpoint
    checkpoint_parser = subparsers.add_parser("checkpoint", help="Record checkpoint")
    checkpoint_parser.add_argument("--progress", required=True, help="Progress (e.g., 15/20)")
    checkpoint_parser.add_argument("--tokens", type=int, default=0, help="Tokens used since last checkpoint")
    checkpoint_parser.add_argument("--description", default="", help="Checkpoint description")

    # Wrap
    wrap_parser = subparsers.add_parser("wrap", help="Wrap session")
    wrap_parser.add_argument("--final-tokens", type=int, help="Final token count")

    # Status
    subparsers.add_parser("status", help="Show session status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    orchestrator = SessionOrchestrator()

    if args.command == "start":
        orchestrator.start_session()

    elif args.command == "checkpoint":
        current, total = map(int, args.progress.split("/"))
        orchestrator.checkpoint(
            current=current,
            total=total,
            tokens_used=args.tokens,
            description=args.description
        )

    elif args.command == "wrap":
        orchestrator.wrap_session(final_tokens=args.final_tokens)

    elif args.command == "status":
        orchestrator.show_status()


if __name__ == "__main__":
    main()
