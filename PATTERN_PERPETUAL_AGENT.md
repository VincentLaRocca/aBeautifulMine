# PATTERN: Perpetual Agent Operation

## The Pattern

**Name**: Perpetual Agent with Resource Monitoring and Graceful Continuation

**Problem**: AI agents have resource limits (tokens, memory, time) that force interruptions, losing context and momentum.

**Solution**: Build self-monitoring agents that:
1. Track their own resource consumption
2. Gracefully shutdown before limits
3. Persist state and context
4. Resume seamlessly in fresh instance
5. Continue until work is complete

## Pattern Structure

```
┌─────────────────────────────────────────────────────────┐
│                  PERPETUAL AGENT PATTERN                 │
└─────────────────────────────────────────────────────────┘

Components:
  1. Task Queue (what to do)
  2. Resource Monitor (how much left)
  3. State Persistence (where we are)
  4. Graceful Shutdown (clean exit)
  5. Resume Mechanism (pick up where left off)
  6. Orchestrator (manage lifecycle)

Flow:
  Instance 1: Work → Monitor → Threshold → Save State → Shutdown
  Instance 2: Load State → Resume → Work → Monitor → Threshold → Save State → Shutdown
  Instance 3: Load State → Resume → Work → Complete → Done
```

## Core Elements

### 1. Resource Monitor
```python
class ResourceMonitor:
    """Monitors agent resource usage"""

    def __init__(self, budget, threshold=0.85):
        self.budget = budget
        self.threshold = threshold
        self.current = 0

    def check_status(self):
        percentage = self.current / self.budget
        if percentage >= self.threshold:
            return "WRAP_NOW"
        elif percentage >= 0.75:
            return "WARNING"
        else:
            return "HEALTHY"
```

### 2. State Persistence
```python
class StatePersistence:
    """Saves/loads agent state between instances"""

    def save_state(self, state):
        # Save:
        # - Current task
        # - Progress
        # - Context
        # - Next action
        # - Checkpoints

    def load_state(self):
        # Restore everything needed to continue
```

### 3. Graceful Shutdown
```python
class GracefulShutdown:
    """Handles clean agent shutdown"""

    def shutdown(self):
        # 1. Complete current unit
        # 2. Save state
        # 3. Backup data
        # 4. Commit changes
        # 5. Create handoff
        # 6. Exit cleanly
```

### 4. Task Queue
```python
class TaskQueue:
    """Priority queue of work to complete"""

    def get_next_task(self):
        # Returns next task based on:
        # - Priority
        # - Dependencies
        # - Estimated resources
```

### 5. Resume Mechanism
```python
class ResumeMechanism:
    """Resumes from saved state"""

    def resume(self, state):
        # 1. Load state
        # 2. Restore context
        # 3. Validate integrity
        # 4. Continue from checkpoint
```

## Implementation Template

```python
# Minimal perpetual agent implementation

class PerpetualAgent:
    def __init__(self, resource_budget, threshold=0.85):
        self.resource_budget = resource_budget
        self.threshold = threshold
        self.task_queue = TaskQueue()
        self.state_manager = StateManager()

    def run_session(self):
        """Run one session of work"""

        # 1. Load state or get next task
        state = self.state_manager.load() or self.get_next_task()

        # 2. Work loop
        while self.has_resources() and not self.task_complete():
            self.do_work()
            self.update_state()

            # 3. Check resources
            if self.resource_usage() >= self.threshold:
                self.graceful_shutdown()
                break

        # 4. If task complete, move to next
        if self.task_complete():
            self.task_queue.mark_complete()
            self.state_manager.clear()

    def has_resources(self):
        return self.resource_usage() < self.threshold

    def resource_usage(self):
        return self.current_usage / self.resource_budget

    def graceful_shutdown(self):
        # Save state
        self.state_manager.save({
            'task': self.current_task,
            'progress': self.progress,
            'context': self.context,
            'next_action': self.next_action
        })

        # Commit work
        self.commit_changes()

        # Create handoff
        self.create_handoff_doc()

# Usage
agent = PerpetualAgent(resource_budget=200000, threshold=0.85)

# Session 1
agent.run_session()  # Works to 85%, saves state, exits

# Session 2 (fresh instance, full resources)
agent.run_session()  # Loads state, continues, works to 85%, saves state

# Session 3
agent.run_session()  # Completes task, moves to next

# Forever...
```

## Real-World Applications

### 1. Token-Limited AI Agents (Our Use Case)
- **Resource**: Token budget (200K)
- **Threshold**: 85% (170K tokens)
- **Persistence**: JSON state files
- **Handoff**: Markdown documents
- **Use**: Claude Code data mining

### 2. Memory-Limited Processes
- **Resource**: RAM usage
- **Threshold**: 80% of available
- **Persistence**: Database snapshots
- **Handoff**: Process checkpoints
- **Use**: Large-scale data processing

### 3. Time-Limited Jobs
- **Resource**: Execution time
- **Threshold**: 90% of time limit
- **Persistence**: Job state files
- **Handoff**: Job continuation metadata
- **Use**: Cloud function chains

### 4. Rate-Limited API Workers
- **Resource**: API quota
- **Threshold**: 85% of daily limit
- **Persistence**: Request queue state
- **Handoff**: Pending requests list
- **Use**: Social media scrapers

### 5. Cost-Limited Cloud Tasks
- **Resource**: Budget dollars
- **Threshold**: 80% of budget
- **Persistence**: Work progress logs
- **Handoff**: Cost accounting + remaining work
- **Use**: AWS batch processing

## Pattern Benefits

### Efficiency
- **Maximize resource usage**: Work to 85-90% instead of arbitrary stops
- **No wasted startup**: Resume exactly where left off
- **Optimal batching**: Natural work unit boundaries

### Resilience
- **Crash recovery**: State saved at checkpoints
- **No context loss**: Complete state preservation
- **Graceful degradation**: Clean shutdown even on errors

### Scalability
- **Unlimited work**: Task queue can grow infinitely
- **Parallel instances**: Multiple agents on separate tasks
- **Resource pooling**: Share resources across instances

### Maintainability
- **Clear boundaries**: Session = one instance lifecycle
- **Auditable**: Handoff docs show all transitions
- **Debuggable**: State files show exact progress

## Pattern Variations

### Variation 1: Multi-Resource Monitoring
Monitor multiple resources (tokens + time + memory):
```python
def should_shutdown(self):
    return (
        self.token_usage() >= 0.85 or
        self.time_usage() >= 0.90 or
        self.memory_usage() >= 0.80
    )
```

### Variation 2: Adaptive Thresholds
Adjust threshold based on task complexity:
```python
def get_threshold(self):
    if self.task_complexity == "simple":
        return 0.90  # Can push higher
    elif self.task_complexity == "complex":
        return 0.80  # Need buffer for shutdown
    else:
        return 0.85  # Default
```

### Variation 3: Predictive Shutdown
Predict when to shutdown based on work rate:
```python
def should_shutdown_predictive(self):
    work_remaining = self.estimate_remaining_work()
    resources_remaining = self.budget - self.current_usage
    estimated_cost = work_remaining * self.avg_cost_per_unit

    return estimated_cost > resources_remaining * 0.95
```

### Variation 4: Multi-Agent Orchestration
Multiple perpetual agents working in parallel:
```python
orchestrator = MultiAgentOrchestrator()
orchestrator.add_agent("miner_1", task_subset_1)
orchestrator.add_agent("miner_2", task_subset_2)
orchestrator.run()  # Both work perpetually in parallel
```

## Anti-Patterns to Avoid

### ❌ Hard Limits Without Shutdown Buffer
```python
# BAD: Work until you crash
while True:
    work()  # No monitoring, no graceful shutdown
```

### ❌ No State Persistence
```python
# BAD: Lose everything on restart
def work():
    progress = 0
    # If interrupted, progress lost
```

### ❌ Manual Resource Tracking
```python
# BAD: Human has to watch and intervene
print("Check tokens manually and stop me when needed")
```

### ❌ All-or-Nothing Tasks
```python
# BAD: Can't resume partial work
def process_all_data():
    # Either completes all or nothing saved
```

## Pattern Evolution

### Level 1: Basic (Manual)
- Human monitors resources
- Human triggers shutdown
- Manual resume

### Level 2: Semi-Automated (Our Implementation)
- Agent monitors resources
- Agent triggers shutdown
- Automated state save
- Manual resume (human starts next session)

### Level 3: Fully Automated
- Agent monitors resources
- Agent triggers shutdown
- Automated state save
- **Automated resume** (agent spawns next instance)
- No human intervention

### Level 4: Self-Optimizing
- Agent monitors resources
- Agent predicts optimal shutdown
- Agent optimizes resource allocation
- Agent spawns parallel instances
- Agent adjusts strategies based on performance

## When to Use This Pattern

### ✅ Use When:
- Resource limits are known and measurable
- Work can be broken into checkpointable units
- Context can be serialized
- Resume cost is low
- Work is long-running
- Graceful completion matters

### ❌ Don't Use When:
- Resources are unlimited
- Work completes quickly (< 10% of resource budget)
- State cannot be saved
- Resume cost is prohibitive
- Atomic operations required

## Related Patterns

- **Checkpoint/Restart**: Similar but focused on failure recovery
- **Saga Pattern**: Distributed transactions with compensation
- **Circuit Breaker**: Prevents resource exhaustion
- **Bulkhead**: Resource isolation
- **Backpressure**: Flow control under load

## Success Metrics

Track pattern effectiveness:

```python
metrics = {
    "resource_efficiency": tokens_used / tokens_budgeted,  # Target: >0.85
    "resume_overhead": resume_time / total_time,  # Target: <0.05
    "context_preservation": restored_state / total_state,  # Target: 1.0
    "graceful_shutdowns": clean_exits / total_exits,  # Target: 1.0
    "work_completion_rate": tasks_done / tasks_started  # Target: 1.0
}
```

## Example: Our Implementation

```python
# task_stack.py - Task queue
stack = TaskStack()
stack.add_task("integrate_data", priority=1)

# session_orchestrator.py - Orchestrator
orchestrator = SessionOrchestrator()

# Session 1
orchestrator.start_session()  # Gets task from stack
# Work happens...
orchestrator.checkpoint(progress="10/20", tokens=85000)
# Work continues...
orchestrator.wrap_session(final_tokens=170000)  # 85% reached
# State saved, git committed, handoff created

# Session 2 (fresh instance)
orchestrator.start_session()  # Loads saved state
# "Resume previous task? y"
# Work continues from 10/20...
orchestrator.checkpoint(progress="20/20", tokens=160000)
orchestrator.wrap_session()  # Task complete
# Moves to next task in stack

# Pattern continues forever
```

## The Pattern in One Sentence

**"Build agents that know when to stop, save where they are, and seamlessly continue in a fresh instance."**

## Why This Pattern Matters

### Before (Traditional)
- Work until crash or arbitrary limit
- Lose context between runs
- Waste resources at boundaries
- Manual intervention required

### After (Perpetual Pattern)
- Work to optimal threshold
- Preserve complete context
- Maximize resource efficiency
- Autonomous operation

### Result
**Agents that work like humans**: Take breaks when tired, remember everything, continue tomorrow, complete the job.

---

## Pattern Template (Copy-Paste Ready)

```python
"""
Perpetual Agent Pattern Template
=================================
Use this template for any resource-limited autonomous agent.
"""

class PerpetualAgentTemplate:
    def __init__(self, resource_budget, shutdown_threshold=0.85):
        self.resource_budget = resource_budget
        self.shutdown_threshold = shutdown_threshold

        # Components
        self.task_queue = self._init_task_queue()
        self.resource_monitor = self._init_resource_monitor()
        self.state_manager = self._init_state_manager()

    def run(self):
        """Main execution loop"""

        # Try to resume from previous state
        state = self.state_manager.load_state()

        if state:
            self._resume_from_state(state)
        else:
            task = self.task_queue.get_next()
            self._start_new_task(task)

        # Work loop with resource monitoring
        while self._should_continue():
            self._do_work_unit()
            self._update_state()

            if self._should_shutdown():
                self._graceful_shutdown()
                break

        # Check if task complete
        if self._task_complete():
            self._finalize_task()

    def _should_continue(self):
        return (
            not self._task_complete() and
            self.resource_monitor.has_budget()
        )

    def _should_shutdown(self):
        return self.resource_monitor.at_threshold(
            self.shutdown_threshold
        )

    def _graceful_shutdown(self):
        # 1. Complete current unit
        self._finish_current_unit()

        # 2. Save state
        self.state_manager.save_state(self._get_state())

        # 3. Commit work
        self._commit_changes()

        # 4. Create handoff
        self._create_handoff_document()

        # 5. Cleanup
        self._cleanup()

    def _get_state(self):
        return {
            'task_id': self.current_task_id,
            'progress': self.progress,
            'context': self.context,
            'resources_used': self.resource_monitor.current_usage,
            'next_action': self.next_action,
            'checkpoints': self.checkpoints
        }

    # Implement these methods for your specific use case
    def _do_work_unit(self): raise NotImplementedError
    def _finish_current_unit(self): raise NotImplementedError
    def _commit_changes(self): raise NotImplementedError
    def _create_handoff_document(self): raise NotImplementedError
```

---

**This is a universal pattern for building unstoppable autonomous agents.**

Use it everywhere:
- AI agents with token limits
- Cloud functions with time limits
- API workers with rate limits
- Batch jobs with cost limits
- Any long-running process with constraints

**The pattern that never stops working.**
