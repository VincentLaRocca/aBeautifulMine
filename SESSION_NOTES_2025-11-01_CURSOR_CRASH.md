# Session Notes - Cursor Crash Incident
**Date:** 2025-11-01
**Time:** ~13:40 (based on file timestamps)
**Location:** C:\Users\vlaro\dreamteam\claude

## Crash Context

### What Crashed
- **Primary Issue:** Cursor IDE crashes
- **Trigger:** Claude orchestrating MCP server with two other people
- **Suspected Root Cause:** Multi-user collaboration via MCP causing Cursor instability

### User Actions
- User is moving away from Cursor due to crash issues
- Session notes captured before making changes

---

## Current MCP Configuration

### Gemini MCP Server
**Configuration File:** `C:\Users\vlaro\.claude.json` (lines 274-285)

```json
"mcpServers": {
  "gemini": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@mintmcqueen/gemini-mcp@latest"],
    "env": {
      "GEMINI_API_KEY": "AIzaSyAIUnWCLyt1i0I9SG8l-T0GvP3vx1EJJgs"
    }
  }
}
```

**Package:** `@mintmcqueen/gemini-mcp@0.3.3`
**Install Location:** `C:\Users\vlaro\AppData\Roaming\npm\node_modules\@mintmcqueen\gemini-mcp`
**Transport:** stdio (standard input/output)

### Droid (Factory AI) Configuration
**Configuration File:** `C:\Users\vlaro\.factory\mcp.json`
- Same Gemini MCP configuration
- Status: `disabled: false` (active)

---

## Work In Progress

### Session 10 Finalization
**Last Activity:** Session 10 completion and database import

**Recent Files Modified (Nov 1, 2025):**
1. `droid-mcp-setup-complete.md` - 13:40 (12KB)
2. `gemini-mcp-assessment-report.md` - 13:24 (17KB)
3. `finalize_session_10.py` - 13:03 (2.7KB)
4. `complete_session_10.py` - 13:01 (3.1KB)
5. `assemble_session_10_complete.py` - 12:38 (2.3KB)

### Current Workflow State
**Protocol:** MCP-based Collaboration Protocol v1.0
**Document:** `mcp-protocol-v1-practical.md`

**4-Phase Workflow:**
1. ✅ Session Setup (5 min)
2. ✅ Batch Content Generation (1.5-2 hours)
3. ⚠️ Python Assembly (30 min) - IN PROGRESS
4. ⏳ Delivery & Import (10 min) - PENDING

### Key Scripts
- `import_session_generic.py` - Generic session importer (5.2KB)
- `verify_database_integrity.py` - DB validation (3.9KB)
- Database: `crypto_indicators_qa.db` (SQLite)

---

## Collaborative Setup

### Multi-User MCP Architecture

```
┌──────────────────┐       ┌──────────────────┐
│   Claude Code    │       │  Droid (Joy)     │
│  (Orchestrator)  │       │  (Factory AI)    │
└────────┬─────────┘       └────────┬─────────┘
         │                          │
         │ ~/.claude.json           │ ~/.factory/mcp.json
         │                          │
         └──────────┬───────────────┘
                    │
                    ▼
          ┌──────────────────────┐
          │   Gemini MCP Server  │
          │ @mintmcqueen/gemini  │
          │      v0.3.3          │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   Google Gemini API  │
          │  gemini-2.5-pro      │
          └──────────────────────┘
```

**Issue:** Multiple clients (Claude + Droid + Cursor?) connecting to same MCP server causing stdio transport conflicts

---

## Technical Debt & Known Issues

### From Assessment Report
1. **Token Limits:** 15K-20K output tokens per request (~2K words max)
2. **Error Rate:** ~12% (500 INTERNAL errors)
3. **Structured Data:** Deviates from exact JSON schemas
4. **Verbosity:** Exceeds word count targets (1K-2K variance)

### Cursor-Specific Issues
- **Crash Pattern:** Occurs during MCP orchestration with multiple users
- **Suspected Cause:** stdio transport not designed for multi-client access
- **IDE Impact:** Cursor IDE becomes unstable/crashes

---

## Database State

### Location
- Primary: `crypto_indicators_qa.db`
- Backups: Various backup DBs exist

### Recent Sessions
- Session 5: ✅ Complete
- Session 7: ✅ Cleaned up
- Session 8: ✅ Cleaned up
- Session 9: ✅ Verified
- Session 10: ⚠️ IN PROGRESS (assembly phase)

### Structure
- Sessions table
- Indicators table (5 per session)
- Q&A pairs table (30 per session, 6 per indicator)

---

## Critical Files for Recovery

### Configuration
1. `.claude.json` - Claude Code config + MCP server
2. `.factory/mcp.json` - Droid MCP config
3. `.claude/settings.json` - Project settings

### Documentation
1. `mcp-protocol-v1-practical.md` - Workflow protocol
2. `gemini-mcp-assessment-report.md` - Performance analysis
3. `droid-mcp-setup-complete.md` - Setup guide
4. `GEMINI_MCP_SETUP.md` - Original setup docs

### Active Scripts
1. `import_session_generic.py` - DB import
2. `finalize_session_10.py` - Current session finalization
3. `verify_database_integrity.py` - Validation

---

## Recommendations for Recovery

### Immediate Actions
1. **Stop Cursor IDE** - Prevent further crashes
2. **Move MCP orchestration** - Consider terminal-only workflow
3. **Test MCP Server** - Run `npx -y @mintmcqueen/gemini-mcp@latest` manually
4. **Check stdio conflicts** - Verify only one client connects at a time

### Alternative IDE Options
1. **VS Code** - More stable with Claude Code
2. **Terminal only** - Pure CLI workflow (most stable)
3. **Separate terminals** - Claude and Droid in separate processes

### MCP Transport Alternatives
- Consider SSE (Server-Sent Events) instead of stdio for multi-client support
- Or: Use HTTP transport for better client isolation

---

## Environment Details

**Working Directory:** `C:\Users\vlaro\dreamteam\claude`
**Platform:** Windows (win32)
**Git Repo:** No
**Date:** 2025-11-01

**User:** vlaroc@gmail.com (Vinny)
**Organization:** vlaroc@gmail.com's Organization
**Claude Code Version:** 2.0.31

---

## Next Steps After Cursor Migration

1. Verify MCP server still accessible
2. Complete Session 10 assembly
3. Run database import
4. Validate integrity
5. Document new IDE setup
6. Test multi-user workflow in new environment

---

## Appendix: Available MCP Tools

### Communication
- `mcp__gemini__chat`
- `mcp__gemini__start_conversation`
- `mcp__gemini__clear_conversation`

### Batch Processing (50% cost savings)
- `mcp__gemini__batch_process`
- `mcp__gemini__batch_create`
- `mcp__gemini__batch_get_status`
- `mcp__gemini__batch_download_results`
- `mcp__gemini__batch_ingest_content`

### Embeddings
- `mcp__gemini__batch_process_embeddings`
- `mcp__gemini__batch_ingest_embeddings`

### File Management
- `mcp__gemini__upload_file`
- `mcp__gemini__upload_multiple_files`
- `mcp__gemini__list_files`
- `mcp__gemini__delete_file`

### Image Generation
- `mcp__gemini__generate_images`

---

**End of Session Notes**
**Status:** Preserved before Cursor migration
**Recovery:** All critical information captured
