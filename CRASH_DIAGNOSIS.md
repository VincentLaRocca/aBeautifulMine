# Cursor MCP Crash - Quick Diagnosis

## Problem Summary
**Cursor IDE crashes when Claude orchestrates MCP server with multiple users**

## Root Cause Analysis

### stdio Transport Limitation
- **Transport Type:** stdio (standard input/output)
- **Design:** Single-process, single-client communication
- **Problem:** stdio cannot handle multiple clients simultaneously
- **Impact:** When Claude (via Cursor), Droid, and possibly other processes try to access the same MCP server, stdio connections conflict

### Architecture Issue
```
❌ PROBLEMATIC SETUP:
Cursor → Claude → ┐
                  ├─→ Gemini MCP (stdio) → CRASH!
Droid (Joy) ──────┘
```

## Why Cursor Crashes Specifically

1. **IDE Integration:** Cursor has tighter integration with Claude Code
2. **Process Management:** Cursor may spawn additional processes
3. **stdio Blocking:** When MCP server is busy with one client, others block/crash
4. **Resource Contention:** Multiple IDE features trying to access MCP simultaneously

## Immediate Fix Options

### Option 1: Separate MCP Servers (RECOMMENDED)
Each client gets their own MCP server instance:
```
Claude → Gemini MCP Instance 1 (stdio on port/pipe 1)
Droid  → Gemini MCP Instance 2 (stdio on port/pipe 2)
```

### Option 2: Switch to SSE Transport
SSE supports multiple clients:
```json
{
  "mcpServers": {
    "gemini": {
      "type": "sse",
      "url": "http://localhost:3000/sse",
      "env": {
        "GEMINI_API_KEY": "your-key"
      }
    }
  }
}
```

### Option 3: Use Terminal Only (NO IDE)
- Run Claude Code in pure terminal mode
- No Cursor integration
- Most stable for multi-client MCP setups

### Option 4: Sequential Access (Coordination)
- Only one client uses MCP at a time
- Requires manual coordination
- Not practical for real collaboration

## Migration Steps

### Step 1: Stop All Processes
```bash
# Kill any running MCP servers
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *gemini-mcp*"

# Close Cursor
# Close any Claude Code terminals
```

### Step 2: Choose Your Path

**Path A: Terminal Only (Safest)**
```bash
# Run Claude Code from terminal only
claude
```

**Path B: VS Code (More Stable)**
- Install VS Code
- Install Claude Code extension for VS Code
- Configure MCP in VS Code settings

**Path C: Multiple MCP Instances**
- Create separate config files:
  - `.claude.json` - for Claude
  - `.factory/mcp.json` - for Droid
- Ensure different ports/pipes if using SSE/HTTP

### Step 3: Verify MCP Works
```bash
# Test MCP server manually
npx -y @mintmcqueen/gemini-mcp@latest
```

### Step 4: Resume Work
- Complete Session 10 finalization
- Run `import_session_generic.py`
- Verify database integrity

## Prevention Checklist

- [ ] Only one client connects to stdio MCP servers
- [ ] Use SSE/HTTP for multi-client scenarios
- [ ] Monitor MCP server health in `/mcp`
- [ ] Keep Cursor closed during heavy MCP operations
- [ ] Consider dedicated MCP orchestration terminal

## Recovery Commands

```bash
# Check MCP server status
claude mcp list

# Test MCP connection
npx -y @mintmcqueen/gemini-mcp@latest

# Verify files are intact
ls -la *.py
ls -la *.md
ls -la *.json

# Check database
sqlite3 crypto_indicators_qa.db "SELECT COUNT(*) FROM sessions;"
```

## Files to Monitor

- `.claude.json` - Claude MCP config
- `.factory/mcp.json` - Droid MCP config
- Session notes: `SESSION_NOTES_2025-11-01_CURSOR_CRASH.md`
- Current work: `finalize_session_10.py`

## Contact Points

- Claude Code Docs: https://docs.claude.com/en/docs/claude-code
- MCP Protocol: https://modelcontextprotocol.io
- Gemini MCP: https://github.com/mintmcqueen/gemini-mcp

---

**Status:** Crash documented, ready for migration
**Next:** Choose IDE alternative and resume Session 10 work
