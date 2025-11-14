# Resume Guide - Picking Up Where You Left Off

## Quick Resume Commands

### Option 1: Auto-Detect Resume Point (Easiest)
```bash
python run_multi_agent.py "Your Topic" --continue
```

### Option 2: Manual Resume
```bash
python run_multi_agent.py "Your Topic" 5  # Resume from subtopic index 5
```

### Option 3: Check Status First
```bash
python check_pipeline_status.py  # See what's done
python run_multi_agent.py "Your Topic" --continue  # Then resume
```

## How Resume Works

The system automatically:
1. ✅ **Saves checkpoints** after each subtopic
2. ✅ **Tracks completed subtopics** via output files
3. ✅ **Skips completed work** when resuming
4. ✅ **Continues from next subtopic** automatically

## Checking Progress

### Quick Status Check
```bash
python check_pipeline_status.py
```

This shows:
- How many subtopics are completed
- Which subtopics are in progress
- Estimated time remaining
- Resume command

### Manual Check
Check the output directories:
- `multi_agent_output/questions/` - Generated questions
- `multi_agent_output/research/` - Research results
- `multi_agent_output/answers/` - Q&A pairs
- `multi_agent_output/checkpoints/` - Saved checkpoints

## Resume Scenarios

### Scenario 1: Pipeline Stopped Mid-Subtopic
**What happens:** The current subtopic will restart from the beginning
**Action:** Resume from the same subtopic index

### Scenario 2: Pipeline Stopped Between Subtopics
**What happens:** Next subtopic starts automatically
**Action:** Use `--continue` to auto-detect

### Scenario 3: Computer Crashed/Rebooted
**What happens:** Checkpoints are saved, can resume
**Action:** 
1. Check status: `python check_pipeline_status.py`
2. Resume: `python run_multi_agent.py "Topic" --continue`

### Scenario 4: Want to Skip a Subtopic
**What happens:** You can manually specify a higher index
**Action:** `python run_multi_agent.py "Topic" 10` (skips to subtopic 10)

## Best Practices

1. **Let it run overnight** - The pipeline saves checkpoints automatically
2. **Check status periodically** - Use `check_pipeline_status.py`
3. **Don't delete output files** - They're used to detect completed work
4. **Use --continue** - It's smarter than manual index guessing

## Time Estimates

- **Per Question**: ~1-2 minutes (research + answer)
- **100 Questions**: ~2-3 hours per subtopic
- **10 Subtopics**: ~20-30 hours total
- **29 Subtopics**: ~60-90 hours total

**Tip:** Let it run continuously. Checkpoints ensure you can always resume!

## Troubleshooting

### "No previous run found"
→ Make sure you're using the exact same topic name
→ Check `multi_agent_output/task_lists/` for your task list

### Resume starts from wrong subtopic
→ Check status first: `python check_pipeline_status.py`
→ Manually specify index: `python run_multi_agent.py "Topic" X`

### Checkpoints not saving
→ Check write permissions in `multi_agent_output/checkpoints/`
→ Checkpoints are optional - resume still works via output files

## Example Workflow

```bash
# Start pipeline
python run_multi_agent.py "Cryptocurrency Technical Analysis"

# ... hours later, check progress ...
python check_pipeline_status.py

# ... if stopped, resume ...
python run_multi_agent.py "Cryptocurrency Technical Analysis" --continue

# ... repeat as needed ...
```

## Files Created for Resume

- **Task Lists**: `multi_agent_output/task_lists/*.json`
- **Questions**: `multi_agent_output/questions/*.json`
- **Research**: `multi_agent_output/research/*.json`
- **Answers**: `multi_agent_output/answers/*.json`
- **Checkpoints**: `multi_agent_output/checkpoints/*.json`

All of these help the system know where you left off!

