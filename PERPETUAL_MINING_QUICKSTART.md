### Perpetual Mining Machine - Quick Start Guide

## Overview

This system transforms Claude Code into an **autonomous, self-sustaining data mining machine** that:
- Monitors its own token usage
- Works until 85% token threshold
- Auto-commits and wraps gracefully
- Restarts fresh and continues
- **Never stops building your database**

## Setup (5 Minutes)

### Step 1: Initialize Task Stack

```bash
# Initialize the task system
python task_stack.py init

# Add your tasks (in priority order)
python task_stack.py add \
  --task "integrate_sessions_101_120" \
  --priority 1 \
  --description "Integrate RAG sessions 101-120" \
  --estimated-tokens 50000

python task_stack.py add \
  --task "integrate_sessions_121_140" \
  --priority 2 \
  --description "Integrate RAG sessions 121-140" \
  --estimated-tokens 50000

python task_stack.py add \
  --task "integrate_claude_shared" \
  --priority 3 \
  --description "Integrate original training database" \
  --estimated-tokens 60000

# View your task queue
python task_stack.py list
```

### Step 2: Start Perpetual Mining

```bash
# Start the first session
python session_orchestrator.py start
```

This will:
- Pull the next task from the queue
- Initialize session tracking
- Show you what to work on

## Working Pattern

### During Your Session

**1. Work normally on the task**
- Write code, integrate data, whatever the task requires
- Keep Claude Code interface visible to see token usage

**2. Check tokens periodically** (every 30-60 min):
```bash
# Replace 120000 with your current token usage from Claude Code
python token_monitor_simple.py 120000
```

**3. Record checkpoints** as you make progress:
```bash
# Example: After integrating 10 of 20 sessions
python session_orchestrator.py checkpoint \
  --progress 10/20 \
  --tokens 45000 \
  --description "Sessions 101-110 complete"
```

**4. When you hit 85% tokens** (or complete task):
```bash
# Wrap the session
python session_orchestrator.py wrap --final-tokens 170000
```

This will:
- Backup your database
- Commit changes to git
- Create handoff document
- Update task progress
- Prepare for fresh start

### Starting Next Session

```bash
# Start fresh (full 200K tokens again)
python session_orchestrator.py start
```

You'll be asked: "Resume previous task? (y/n)"
- **y**: Continue where you left off
- **n**: Move to next task in queue

## Real Example Workflow

### Session 1 (Morning)

```bash
# Start
python session_orchestrator.py start
# Output: Task: integrate_sessions_101_120 (Priority 1)

# Work on integrating sessions...
# (Write integration script, test, integrate)

# Token check at 100K
python token_monitor_simple.py 100000
# Output: Status: 🟢 HEALTHY (50%)

# Checkpoint after 10 sessions
python session_orchestrator.py checkpoint \
  --progress 10/20 \
  --tokens 85000 \
  --description "Sessions 101-110 done, 1000 pairs integrated"

# Token check at 170K
python token_monitor_simple.py 170000
# Output: Status: 🟡 WARNING - START WRAPPING (85%)

# Wrap session
python session_orchestrator.py wrap --final-tokens 172000
# Output: Session wrapped, handoff created

# Git commit created: "Session Wrap: integrate_sessions_101_120"
# Progress: 10/20 (50%)
```

### Session 2 (Afternoon)

```bash
# Fresh start
python session_orchestrator.py start
# "Resume previous task? (y/n):" y

# Continue from checkpoint
# Sessions 111-120 remaining

# Work continues...

# Complete task
python session_orchestrator.py checkpoint \
  --progress 20/20 \
  --tokens 160000 \
  --description "All 20 sessions integrated, 2000 pairs added"

# Wrap
python session_orchestrator.py wrap --final-tokens 162000
# Task marked COMPLETE
# Next task automatically queued
```

### Session 3 (Evening)

```bash
# Fresh start
python session_orchestrator.py start
# New task: integrate_sessions_121_140
# Automatically moves to next priority

# ... and so on forever
```

## Key Commands Reference

### Task Management
```bash
# Add task
python task_stack.py add --task <task_id> --priority <1-10>

# List tasks
python task_stack.py list

# Show statistics
python task_stack.py stats

# Get next task
python task_stack.py next
```

### Session Management
```bash
# Start session
python session_orchestrator.py start

# Record checkpoint
python session_orchestrator.py checkpoint --progress X/Y --tokens N

# Check status
python session_orchestrator.py status

# Wrap session
python session_orchestrator.py wrap
```

### Token Monitoring
```bash
# Check token usage (replace XXXXX with current usage)
python token_monitor_simple.py XXXXX
```

## Token Thresholds

| Usage | Status | Action |
|-------|--------|--------|
| 0-75% | 🟢 Healthy | Keep working |
| 75-85% | 🟡 Warning | Start looking for wrap point |
| 85-95% | 🔴 Shutdown | Wrap now |
| 95%+ | ⚠️ Critical | Emergency wrap |

## Configuration

Edit `perpetual_mining_config.json`:

```json
{
  "token_budget": 200000,
  "warning_threshold": 0.75,
  "shutdown_threshold": 0.85,
  "critical_threshold": 0.95,
  "auto_commit_interval": 500,
  "backup_before_commit": true
}
```

## Files Created

### Active Files
- `task_stack.json` - Your task queue
- `session_state.json` - Current session state
- `perpetual_mining_config.json` - System configuration

### Output Files
- `session_handoffs/handoff_*.md` - Handoff documents for each wrap
- `session_logs/` - Detailed session logs (future)
- `*.backup_*` - Database backups before commits

## Benefits

### Before (Manual)
- Work until tokens run out
- Lose context between sessions
- Manual commits and tracking
- Single-threaded progress

### After (Perpetual Mining)
- Work efficiently to 85%
- Seamless context preservation
- Auto-commits at checkpoints
- Continuous progress forever

## Example Task Queue

For your current project:

```bash
# Priority 1: Complete remaining RAG sessions
python task_stack.py add --task "integrate_sessions_101_140" --priority 1 --estimated-tokens 100000

# Priority 2: Original training database
python task_stack.py add --task "integrate_claude_shared" --priority 2 --estimated-tokens 60000

# Priority 3: Ultra deep research sessions
python task_stack.py add --task "integrate_sessions_141_187" --priority 3 --estimated-tokens 120000

# Priority 4: Quality improvements
python task_stack.py add --task "quality_analysis_and_cleanup" --priority 4 --estimated-tokens 40000

# Priority 5: Embeddings generation
python task_stack.py add --task "generate_embeddings_batch" --priority 5 --estimated-tokens 30000
```

Then just start and let it run:
```bash
python session_orchestrator.py start
```

## Tips for Success

1. **Set realistic progress metrics**: Break tasks into measurable units (e.g., sessions 101-120 = 20 units)

2. **Checkpoint frequently**: Every 5-10 units or every hour of work

3. **Monitor tokens**: Check every 30-60 minutes, don't wait until it's too late

4. **Wrap at 85%**: Don't push to 95%, leave buffer for clean shutdown

5. **Read handoffs**: Always review the previous session's handoff document

6. **Trust the system**: It tracks everything, you just execute

## Advanced: Full Automation (Future)

The next evolution would be a supervisor script that:
- Monitors token usage automatically
- Triggers wrap at 85%
- Restarts session automatically
- Sends status emails

But for now, semi-manual operation gives you full control.

## Troubleshooting

### "No active session"
- Run `python session_orchestrator.py start`

### "No tasks in queue"
- Add tasks with `python task_stack.py add`

### Git commit fails
- Check git status manually
- Ensure you're in a git repo
- Check for conflicts

### Lost session state
- Check `session_state_archived_*.json` files
- Review `session_handoffs/` for last known state

## Success Metrics

Track your progress with:
```bash
python task_stack.py stats
```

Shows:
- Total tasks
- Completion rate
- Tokens used
- Grade distribution

## The Vision

**You become an unstoppable data mining machine:**

- Session 1 (85% tokens) → Wrap → Handoff
- Session 2 (85% tokens) → Wrap → Handoff
- Session 3 (85% tokens) → Wrap → Handoff
- ...Forever...

**Result: 30,000+ pairs. Then 40,000. Then 50,000.**

**The machine that never stops building.**

---

**For the Greater Good of All**

*Ready to mine perpetually? Start now:*

```bash
python task_stack.py init
python task_stack.py add --task "your_first_task" --priority 1
python session_orchestrator.py start
```

🚀 **Let's go!**
