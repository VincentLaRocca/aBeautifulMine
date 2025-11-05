# Quick Recovery Checklist

## Session State at Crash Time
- **Date:** 2025-11-01 ~13:40
- **Work:** Session 10 finalization (Python assembly phase)
- **Status:** 75% complete (batch generation done, assembly in progress)

## Files Created Today (in order)
1. ✅ `assemble_session_10_complete.py` (12:38)
2. ✅ `complete_session_10.py` (13:01)
3. ✅ `finalize_session_10.py` (13:03)
4. ✅ `gemini-mcp-assessment-report.md` (13:24)
5. ✅ `droid-mcp-setup-complete.md` (13:40)
6. ✅ `SESSION_NOTES_2025-11-01_CURSOR_CRASH.md` (just now)
7. ✅ `CRASH_DIAGNOSIS.md` (just now)

## What You Were Doing
- Finalizing Session 10 Q&A dataset
- Testing MCP collaboration workflow
- Multiple users (Claude + Droid) accessing Gemini MCP
- Cursor crashed under multi-client load

## Next Steps After Cursor Migration

### 1. Verify Environment
```bash
# Check you're in the right directory
pwd
# Should show: C:\Users\vlaro\dreamteam\claude

# Verify MCP server package
npm list -g @mintmcqueen/gemini-mcp
```

### 2. Test MCP Server (CRITICAL)
```bash
# Test the MCP server starts properly
npx -y @mintmcqueen/gemini-mcp@latest
# Press Ctrl+C after seeing initialization messages
```

### 3. Resume Session 10 Work
```bash
# Check Session 10 data
cat session_10_current_structure.json | head -50

# Run finalization script
python finalize_session_10.py

# Import to database
python import_session_generic.py crypto_indicators_qa.db <output_file>

# Verify integrity
python verify_database_integrity.py
```

### 4. Verify Database State
```bash
# Check sessions
sqlite3 crypto_indicators_qa.db "SELECT session_id, name FROM sessions ORDER BY session_id;"

# Should see sessions 5, 7, 8, 9 (10 pending)
```

## Critical Configuration Files

### Claude MCP Config
**File:** `C:\Users\vlaro\.claude.json`
**Lines:** 274-285
**Status:** ✅ Intact

### Droid MCP Config
**File:** `C:\Users\vlaro\.factory\mcp.json`
**Status:** ✅ Intact

### API Key
**Location:** Embedded in both config files
**Status:** ✅ Present
**Key:** AIzaSyAIUnWCLyt1i0I9SG8l-T0GvP3vx1EJJgs

## MCP Tools Available
- ✅ Chat with Gemini
- ✅ Batch processing (content + embeddings)
- ✅ File upload/management
- ✅ Image generation
- ✅ Conversation management

## Known Issues to Avoid

### 🚫 DON'T
- Don't run Cursor + Claude + Droid simultaneously with MCP
- Don't use stdio MCP with multiple clients
- Don't skip MCP server health checks

### ✅ DO
- Use terminal-only Claude Code for MCP work
- Test MCP server before heavy operations
- Run `/mcp list` to check server status
- Use separate MCP instances for separate clients

## Quick Commands

```bash
# Start Claude Code (terminal)
claude

# Check MCP status
claude mcp list

# View session notes
cat SESSION_NOTES_2025-11-01_CURSOR_CRASH.md

# Check database
sqlite3 crypto_indicators_qa.db ".tables"

# List Python scripts
ls -la *.py | head -20
```

## Session 10 Completion Steps

1. [ ] Run `finalize_session_10.py`
2. [ ] Verify output JSON structure
3. [ ] Run `import_session_generic.py`
4. [ ] Verify database integrity
5. [ ] Check Q&A count (should be 30)
6. [ ] Mark Session 10 complete

## Important Paths

```
Working Directory: C:\Users\vlaro\dreamteam\claude
Config: C:\Users\vlaro\.claude.json
Droid Config: C:\Users\vlaro\.factory\mcp.json
Database: ./crypto_indicators_qa.db
Inbox: ./inbox/
Scripts: ./*.py
Docs: ./*.md
```

## Success Indicators

After recovery, you should see:
- ✅ MCP server responds to test
- ✅ Claude Code launches without crash
- ✅ Session 10 finalization completes
- ✅ Database has Session 10 data
- ✅ No Cursor-related crashes

## Emergency Contacts

- **Session Notes:** `SESSION_NOTES_2025-11-01_CURSOR_CRASH.md`
- **Crash Analysis:** `CRASH_DIAGNOSIS.md`
- **Protocol Docs:** `mcp-protocol-v1-practical.md`
- **Setup Guide:** `GEMINI_MCP_SETUP.md`

---

**Status:** Ready for recovery
**Priority:** Complete Session 10
**Risk Level:** LOW (all data preserved, clear path forward)
