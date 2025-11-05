# Batch Submission Agent - Usage Guide

## Overview

The Batch Submission Agent is a repeatable, resumable process for submitting all 204 batches to the Gemini Batch API with automatic rate limit handling.

## Files Created

### 1. `batch_submission_agent.py`
**Purpose**: Standalone Python script that can be run independently
**Features**:
- Progress tracking with JSON state file
- Automatic rate limit detection and retry
- Resumable from any point
- Detailed logging

**Usage**:
```bash
# Submit all remaining batches
python batch_submission_agent.py

# Submit specific range
python batch_submission_agent.py 81 204

# Resume from specific batch
python batch_submission_agent.py 170 204
```

### 2. `batch_submission_agent_mcp.py`
**Purpose**: MCP-integrated version for Claude Code execution
**Features**:
- Direct integration with Gemini MCP tools
- Full automation with error handling
- State persistence across runs
- JSONL event logging

**Usage via Claude Code**:
```
"Use the batch submission agent to complete all remaining batches"
```

### 3. `batch_submission_state.json`
**Purpose**: Persistent state tracking
**Contains**:
- Last completed batch number
- All submitted job names
- Failed batches list
- Upload file URIs
- Timestamps

### 4. `batch_submission_log.jsonl`
**Purpose**: Detailed event log
**Format**: One JSON object per line with:
- Timestamp
- Event type (upload_success, batch_created, error)
- Batch number
- Event data

## How It Works

### State Management
1. **Load State**: Reads `batch_submission_state.json` on startup
2. **Track Progress**: Updates state after each batch
3. **Save State**: Persists state after each successful submission
4. **Resume**: Automatically continues from last completed batch

### Rate Limit Handling
1. **Detection**: Catches 429 RESOURCE_EXHAUSTED errors
2. **Wait**: Pauses for 180 seconds (3 minutes)
3. **Retry**: Attempts submission again
4. **Persistence**: Continues until success or max retries

### Batch Processing Flow
```
For each batch:
  1. Check if already submitted (skip if yes)
  2. Upload JSONL file → Get file URI
  3. Create batch job → Get job name
  4. Save state
  5. Log event
  6. Continue to next batch
```

## Current Progress (as of last run)

- **Total Batches**: 204
- **Successfully Submitted**: ~169 (check state file for exact count)
- **Remaining**: ~35 batches
- **Status**: Ready to complete final batches

## Running the Agent

### Method 1: Via Claude Code (Recommended)
Simply ask Claude Code:
```
"Run the batch submission agent to finish all remaining batches"
```

Claude Code will:
1. Load the agent class
2. Check remaining batches
3. Submit in groups with rate limit handling
4. Generate final completion report

### Method 2: Manual Execution
If you have Python and MCP client configured:
```bash
cd c:\Users\VLARO\dreamteam\claude
python batch_submission_agent.py
```

### Method 3: Check Progress Only
```python
import json
with open('batch_submission_state.json') as f:
    state = json.load(f)
print(f"Submitted: {len(state['submitted_jobs'])}/204")
print(f"Last batch: {state['last_completed_batch']}")
```

## Monitoring Submitted Batches

After submission, monitor batch job status:
```
Use mcp__gemini__batch_get_status with any job name from state file
```

Download results when complete:
```
Use mcp__gemini__batch_download_results
  batchName: <from state file>
  outputLocation: c:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper
```

## Error Recovery

### If Agent Stops Mid-Run
The agent saves state after each batch, so you can simply restart it:
```
python batch_submission_agent.py
```
It will automatically resume from where it left off.

### If Rate Limits Persist
The agent automatically handles rate limits, but if you need to:
1. Wait 10-15 minutes
2. Check quota at: https://ai.dev/usage?tab=rate-limit
3. Restart agent - it will continue automatically

### If Batches Fail
Failed batches are tracked in `state['failed_batches']`. To retry:
```python
python batch_submission_agent.py
# Or manually submit failed batches via Claude Code
```

## Files Generated

- `batch_submission_state.json` - Current state and progress
- `batch_submission_log.jsonl` - Detailed event log
- `batch_submission_final_report.json` - Completion report

## Next Steps After Completion

Once all 204 batches are submitted:

1. **Monitor Processing**
   - Batches typically complete in 10-30 minutes
   - Check status periodically

2. **Download Results**
   - Use `mcp__gemini__batch_download_results` for each completed batch
   - Results saved to `gemini_batch_results_proper/`

3. **Process Refined Data**
   - Parse refined Q&A pairs from results
   - Identify and remove duplicates
   - Generate embeddings

4. **Import to Database**
   - Load refined pairs into `crypto_indicators_production.db`
   - Update metadata and statistics

## Support

For issues or questions:
- Check `batch_submission_log.jsonl` for detailed error messages
- Review `batch_submission_state.json` for current progress
- Ask Claude Code to analyze the logs and state files
