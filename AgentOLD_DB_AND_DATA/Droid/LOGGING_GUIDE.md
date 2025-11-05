# Crypto Question Generator - Logging Guide

## 📝 Logging Options Available

### Option 1: Enhanced Launcher with Full Logging
**Use:** `run_generator_with_logging.py`

**Features:**
- Creates timestamped log files in `crypto_questions_logs/` directory
- Captures all output (stdout and stderr)
- Records start/end times and duration
- Saved with format: `question_generator_YYYYMMDD_HHMMSS.log`

**Usage:**
```bash
python run_generator_with_logging.py sk-or-v1-your-api-key-here
```

### Option 2: View Existing Logs
**Use:** `view_logs.py`

**Features:**
- Lists all available log files with timestamps
- Shows file sizes and modification times
- Interactive selection to view specific log contents
- Option to monitor running process in real-time

**Usage:**
```bash
# View list of logs and select one to read
python view_logs.py

# Monitor currently running process
python view_logs.py --monitor
```

### Option 3: Basic Console Logging (Default)
**Use:** `run_generator.py` (original)

**Features:**
- No log files created
- All output shown in console only
- Basic error messages

## 📂 Log File Locations

```
crypto_questions_logs/
├── question_generator_20251028_091200.log
├── question_generator_20251028_145630.log
└── question_generator_20251028_210845.log

crypto_questions/
├── Price_Patterns_PP_001_Intermediate.txt
├── Advanced_Patterns_PP_002_Advanced.txt
└── ... (15 total topic files)
```

## 🔍 Log File Contents

Each log file contains:
```
Crypto Question Generator Log
Started: 2025-10-28 09:12:00
Process: python crypto_question_generator_fixed.py
============================================================

Starting question generation at: 09:12:01
Parsing crypto topics document...
Found 15 topics

Processing topic 1/15: Head and shoulders pattern identification and trading
  API attempt 1/3...
+ Generated 15 questions -> crypto_questions/Price_Patterns_PP_001_Intermediate.txt

Processing topic 2/15: Wyckoff accumulation and distribution phases
  API attempt 1/3...
  Rate limited, waiting 2 seconds...
  API attempt 2/3...
+ Generated 15 questions -> crypto_questions/Advanced_Patterns_PP_002_Advanced.txt

[... all topic processing ...]

============================================================
GENERATION COMPLETE
============================================================
Total topics processed: 15
Successfully generated: 15
Failed: 0
Questions per topic: 15
Total questions created: 225
Output directory: C:\users\vlaro\Droid\crypto_questions
Completed at: 09:47:38
Total duration: 0:35:37

Process Summary:
- Topics processed: 15
- Successfully generated: 15
- Failed: 0
- Questions created: 225
- Time per topic: 142.5 seconds

Process completed with exit code: 0
Completed: 2025-10-28 09:47:38
Duration: 0:35:37
```

## 🛠️ Troubleshooting with Logs

**Rate Limiting Issues:**
- Look for "Rate limited, waiting X seconds..." messages
- Check retry attempt counts
- Identify which topics had most issues

**API Errors:**
- Check "API error: 429" or other error codes
- Review error messages from the API
- See which topics failed and why

**Performance Issues:**
- Monitor "Time per topic" calculations
- Identify slow topics or API delays
- Track overall progress

## 💡 Pro Tips

1. **Use enhanced logging for first run** - Helps identify any issues
2. **Monitor during long runs** - Use `python view_logs.py --monitor` 
3. **Keep logs for reference** - They're useful for tracking your question generation history
4. **Check logs immediately** - If the process fails, the log shows exactly where and why

## 🎯 Recommended Workflow

```bash
# First time with logging
python run_generator_with_logging.py sk-or-v1-your-key

# Then review the results
python view_logs.py

# Check your generated questions
ls crypto_questions/
```
