# Perpetual Mining Machine - Architecture

## Vision

Create an autonomous Claude Code system that continuously mines and integrates data without human intervention, managing its own token budget, making commits, and seamlessly continuing across sessions.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PERPETUAL MINING SYSTEM                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │      Task Stack (Priority Queue)       │
        │  ┌──────────────────────────────────┐  │
        │  │ 1. Integrate Sessions 101-120    │  │
        │  │ 2. Integrate Sessions 121-140    │  │
        │  │ 3. Integrate Claude_Shared       │  │
        │  │ 4. Quality analysis & cleanup    │  │
        │  │ 5. Generate embeddings (batch)   │  │
        │  └──────────────────────────────────┘  │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │        Session Orchestrator            │
        │  - Reads next task from stack          │
        │  - Instantiates Claude Code session    │
        │  - Loads context & state               │
        │  - Monitors token usage                │
        │  - Triggers graceful shutdown at 85%   │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │      Claude Code Session Instance      │
        │  ┌──────────────────────────────────┐  │
        │  │ Token Budget: 200,000            │  │
        │  │ Current Usage: ████░░░░░ 85%     │  │
        │  │                                  │  │
        │  │ Working on: Integrate 101-120   │  │
        │  │ Progress: 15/20 sessions done   │  │
        │  │                                  │  │
        │  │ [Token Monitor Active]           │  │
        │  └──────────────────────────────────┘  │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │      Graceful Shutdown (85% tokens)    │
        │  1. Complete current sub-task          │
        │  2. Write session state to disk        │
        │  3. Backup database                    │
        │  4. Commit changes to git              │
        │  5. Generate handoff document          │
        │  6. Update task stack with progress    │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │          Re-instantiation              │
        │  1. New Claude Code session starts     │
        │  2. Load session state from disk       │
        │  3. Read handoff document              │
        │  4. Continue from checkpoint           │
        │  5. Monitor tokens again...            │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │      Task Completion & Grading         │
        │  1. Task finishes completely           │
        │  2. Run validation & quality checks    │
        │  3. Grade performance (A-F)            │
        │  4. Generate completion report         │
        │  5. Remove from task stack             │
        │  6. Move to next task                  │
        └────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │      Task Assignment (ClaudePrompt)    │
        │  - Reviews completed tasks             │
        │  - Analyzes performance grades         │
        │  - Assigns new tasks to stack          │
        │  - Prioritizes based on goals          │
        └────────────────────────────────────────┘
```

## Core Components

### 1. Task Stack Manager (`task_stack.py`)

**Purpose**: Manages queue of tasks to be executed

**Features**:
- Priority-based queue
- Task dependencies
- Progress tracking
- State persistence

**Schema**:
```python
{
  "task_id": "integrate_sessions_101_120",
  "priority": 1,
  "status": "in_progress",
  "assigned_to": "claude_code_session_3",
  "progress": {
    "current": 15,
    "total": 20,
    "percentage": 75
  },
  "estimated_tokens": 50000,
  "actual_tokens": 38500,
  "checkpoints": [
    {"session": 105, "timestamp": "2025-11-06T10:30:00"},
    {"session": 110, "timestamp": "2025-11-06T11:15:00"}
  ]
}
```

### 2. Session Orchestrator (`session_orchestrator.py`)

**Purpose**: Manages Claude Code session lifecycle

**Responsibilities**:
- Instantiate new sessions
- Load task from stack
- Inject initial prompt with context
- Monitor token usage
- Trigger shutdown at threshold
- Handle re-instantiation

**Key Methods**:
```python
def start_session(task):
    """Start new Claude Code session with task"""

def monitor_tokens():
    """Track token usage in real-time"""

def trigger_shutdown(threshold=0.85):
    """Gracefully end session at token limit"""

def create_handoff():
    """Generate handoff doc for next session"""
```

### 3. Token Monitor (`token_monitor.py`)

**Purpose**: Track token usage and trigger actions

**Features**:
- Real-time token counting
- Configurable thresholds
- Warning alerts (75%, 85%, 90%)
- Automatic shutdown trigger
- Token usage analytics

**Thresholds**:
- **75%**: Warning - start preparing for wrap-up
- **85%**: Shutdown trigger - complete current unit, commit
- **90%**: Hard stop - emergency commit and exit
- **95%**: Panic mode - force commit, may be incomplete

### 4. State Manager (`state_manager.py`)

**Purpose**: Persist session state across restarts

**Saves**:
- Current task details
- Progress checkpoints
- Variables and context
- Database state
- Files modified
- Next action to take

**Schema**:
```python
{
  "session_id": "claude_code_session_3",
  "task_id": "integrate_sessions_101_120",
  "timestamp": "2025-11-06T11:45:00",
  "token_usage": 170000,
  "token_budget": 200000,
  "progress": {
    "sessions_completed": [101, 102, ..., 115],
    "sessions_remaining": [116, 117, 118, 119, 120],
    "next_session": 116,
    "pairs_integrated": 1500,
    "errors_encountered": 0
  },
  "context": {
    "database_path": "crypto_indicators_production.db",
    "source_file": "rag_export_data.json",
    "integration_method": "batch_insert",
    "last_checkpoint": "session_115_complete"
  },
  "next_action": "Continue integration from session 116"
}
```

### 5. Commit Manager (`commit_manager.py`)

**Purpose**: Automatic git commits at checkpoints

**Features**:
- Auto-commit every N items
- Descriptive commit messages
- Include progress stats
- Tag important milestones
- Push to remote (optional)

**Commit Strategy**:
- Every 500 pairs integrated
- Every 10 sessions completed
- At 85% token threshold
- On task completion
- On error recovery

### 6. Grading System (`task_grader.py`)

**Purpose**: Evaluate task completion quality

**Metrics**:
- Success rate (errors vs successes)
- Speed (tokens per item)
- Quality (validation checks)
- Completeness (% of task done)
- Efficiency (token usage vs estimate)

**Grade Calculation**:
```python
Grade = (
    0.3 * success_rate +
    0.2 * speed_score +
    0.3 * quality_score +
    0.2 * efficiency_score
)
```

### 7. Task Assigner (`task_assigner.py`)

**Purpose**: ClaudePrompt-style task generation

**Functions**:
- Review completed tasks
- Analyze performance trends
- Generate new tasks based on goals
- Prioritize task queue
- Estimate token requirements

## Workflow Example

### Initial Setup (Human)

```bash
# 1. Initialize task stack
python task_stack.py init

# 2. Add tasks
python task_stack.py add \
  --task "integrate_sessions_101_120" \
  --priority 1 \
  --estimated-tokens 50000

python task_stack.py add \
  --task "integrate_sessions_121_140" \
  --priority 2 \
  --estimated-tokens 50000

# 3. Start perpetual mining
python perpetual_miner.py start
```

### Session 1 (Automatic)

```
[Session Start]
Budget: 200,000 tokens
Task: integrate_sessions_101_120

[Token: 50,000] Progress: Sessions 101-105 complete (5/20)
[Token: 100,000] Progress: Sessions 106-110 complete (10/20)
[Token: 150,000] Progress: Sessions 111-115 complete (15/20)
[Token: 170,000] ⚠️  Warning: 85% tokens used
[Token: 170,500] Completing session 115...
[Token: 171,000] Writing state to disk...
[Token: 171,500] Backing up database...
[Token: 172,000] Committing changes...
[Token: 172,500] Creating handoff document...

Git commit: "Session 1: Integrated sessions 101-115 (1500 pairs, 15/20 complete)"

[Session End] State saved. Ready for re-instantiation.
```

### Session 2 (Automatic)

```
[Session Start]
Budget: 200,000 tokens
Loading state from: session_1_handoff.json

Resuming task: integrate_sessions_101_120
Progress: 15/20 complete
Next action: Continue from session 116

[Token: 20,000] Progress: Session 116 complete (16/20)
[Token: 40,000] Progress: Session 117 complete (17/20)
[Token: 60,000] Progress: Session 118 complete (18/20)
[Token: 80,000] Progress: Session 119 complete (19/20)
[Token: 100,000] Progress: Session 120 complete (20/20)

Task COMPLETE! Running validation...
Validation passed ✓
Generating completion report...
Grading performance...

Task Grade: A
- Success rate: 100%
- Speed: Excellent (1.5 pairs/token)
- Quality: Perfect (0 errors)
- Efficiency: 95% (used 270k of 400k budget)

Git commit: "Task Complete: Integrated sessions 101-120 (2000 pairs, Grade A)"

Moving to next task: integrate_sessions_121_140
```

### Session 3+ (Perpetual)

System continues automatically:
- Loads next task
- Executes with token monitoring
- Commits at checkpoints
- Gracefully shuts down at 85%
- Re-instantiates and continues
- Grades completed tasks
- Moves to next task

## Key Files

### Configuration
- `perpetual_mining_config.json` - System settings
- `task_stack.json` - Active task queue
- `session_state.json` - Current session state

### Scripts
- `perpetual_miner.py` - Main orchestrator
- `task_stack.py` - Task queue manager
- `session_orchestrator.py` - Session lifecycle
- `token_monitor.py` - Token tracking
- `state_manager.py` - State persistence
- `commit_manager.py` - Auto-commits
- `task_grader.py` - Performance grading
- `task_assigner.py` - New task generation

### Output
- `session_handoffs/` - Handoff documents
- `session_logs/` - Detailed logs
- `task_reports/` - Completion reports
- `performance_metrics/` - Analytics

## Token Budget Management

### Session Budget: 200,000 tokens

**Allocation Strategy**:
- **Work**: 170,000 tokens (85%)
- **Shutdown**: 20,000 tokens (10%)
- **Buffer**: 10,000 tokens (5%)

**Shutdown Process (20k tokens)**:
1. Complete current unit (2k)
2. Write state file (2k)
3. Backup database (1k)
4. Git commit (3k)
5. Generate handoff (5k)
6. Update task stack (2k)
7. Validation (3k)
8. Buffer (2k)

## Error Handling

### Token Overrun (>90%)
- Emergency commit
- Save incomplete state
- Flag task as "needs review"
- Human notification

### Integration Error
- Rollback to last checkpoint
- Log error details
- Retry with adjusted parameters
- If fails 3x, flag for human review

### Database Locked
- Wait and retry (3 attempts)
- Save state and exit gracefully
- Resume after lock clears

## Benefits

✅ **Autonomous**: Runs without human intervention
✅ **Resilient**: Graceful handling of token limits
✅ **Persistent**: State preserved across sessions
✅ **Trackable**: Git commits at every checkpoint
✅ **Measurable**: Performance grading on all tasks
✅ **Scalable**: Handle unlimited task queue
✅ **Safe**: Automatic backups before operations
✅ **Efficient**: Optimal token usage per task

## Human Oversight Points

**Setup** (One-time):
- Define initial task stack
- Set priorities
- Configure token thresholds

**Monitoring** (Passive):
- Review completion reports
- Check git commits
- Monitor performance grades

**Intervention** (As-needed):
- Add new tasks to stack
- Adjust priorities
- Review flagged errors
- Unblock dependencies

**Grading** (Periodic):
- Review task grades
- Adjust task assignments
- Optimize strategies

## Success Metrics

- **Uptime**: % of time system is working
- **Throughput**: Pairs integrated per hour
- **Efficiency**: Tokens used per pair
- **Quality**: Error rate and grade distribution
- **Autonomy**: Hours without human intervention

## Next Steps

1. Build core components (task_stack, orchestrator, token_monitor)
2. Create session state management
3. Implement graceful shutdown logic
4. Add auto-commit system
5. Build grading and reporting
6. Test with pilot task
7. Deploy perpetual mining

## Vision Realized

**Before**: Human-driven, session-by-session work
**After**: Autonomous, perpetual data mining machine

Claude Code becomes a self-sustaining worker that:
- Knows when to stop (85% tokens)
- Commits its work automatically
- Hands off to next session seamlessly
- Grades its own performance
- Works toward goal completion 24/7

**The perpetual mining machine that never stops building your database.**
