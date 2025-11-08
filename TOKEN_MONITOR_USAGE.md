# Token Monitor Usage Guide

## Overview

`token_monitor_simple.py` has been enhanced to track both **session-level** and **weekly usage** of Claude Desktop tokens.

## Features

### Session Tracking
- Monitors current session token usage
- Alerts at 85% (warning) and 95% (critical) thresholds
- Shows remaining tokens in current session

### Weekly Tracking
- Tracks total tokens used across all sessions in the current week
- Week starts on Monday and resets automatically
- Stores usage data in `~/.claude_usage_tracker.json`
- Provides statistics:
  - Total tokens used this week
  - Number of sessions
  - Average tokens per session
  - Estimated sessions remaining
  - Days left in the week

## Usage

### Basic Usage
```bash
python token_monitor_simple.py <current_token_count>
```

### Example
```bash
python token_monitor_simple.py 32000
```

### Exit Codes
- `0` - Healthy (both session and weekly below warning threshold)
- `1` - Warning (session or weekly at 85%+)
- `2` - Critical (session or weekly at 95%+)
- `3` - Error (invalid input)

## Configuration

Edit the constants in the script to adjust limits:

```python
TOKEN_BUDGET = 200000       # Session budget
WEEKLY_BUDGET = 1000000     # Weekly budget (adjust for your plan)
WARNING_THRESHOLD = 0.85    # 85%
CRITICAL_THRESHOLD = 0.95   # 95%
```

## Data Storage

Usage data is stored in `~/.claude_usage_tracker.json` with the format:

```json
{
  "sessions": [
    {
      "timestamp": "2025-11-07T19:00:17.123456",
      "tokens": 32000
    }
  ],
  "week_start": "2025-11-04T00:00:00"
}
```

The data automatically resets when a new week (Monday) begins.

## Sample Output

```
============================================================
                    TOKEN USAGE MONITOR
============================================================
Status: 🟢 HEALTHY
============================================================

📊 CURRENT SESSION:
Current Usage:         32,000 tokens
Budget:               200,000 tokens
Remaining:            168,000 tokens
Percentage Used:         16.0%

📅 WEEKLY USAGE:
Week: Nov 07 - Nov 14, 2025
Status:            🟢 HEALTHY
Total Used:            96,000 tokens
Weekly Budget:      1,000,000 tokens
Remaining:            904,000 tokens
Percentage Used:          9.6%
Sessions Count:             3
Days Left:                  6
Avg Per Session:       32,000 tokens
Est. Sessions Left:        28

============================================================
Time: 2025-11-07 19:00:17
============================================================

✅ Session healthy. ~138,000 tokens until session warning threshold.
✅ Weekly usage healthy. ~754,000 tokens until weekly warning threshold.
```

## Integration Tips

1. **Manual Check**: Run the script periodically with your current token count
2. **Shell Alias**: Add to your `.bashrc` or `.zshrc`:
   ```bash
   alias tmon='python /path/to/token_monitor_simple.py'
   ```
3. **Pre-commit Hook**: Add to `.git/hooks/pre-commit` to check before commits

## Notes

- Weekly budget of 1M tokens is approximate for Claude Pro
- Adjust `WEEKLY_BUDGET` based on your actual plan limits
- The tracker persists data across terminal sessions
- Data is stored locally and not shared
