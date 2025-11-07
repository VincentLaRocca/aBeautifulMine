# Shared Resources Map - Dream Team

## Shared Folders

### gemini/shared/
**Location**: `C:\Users\vlaro\dreamteam\claude\gemini\shared\`

**Purpose**: Shared resources between all agents (Claude, Claude Code, Gemini, Sister Gemini, Droid, Zai)

**Who can access**: ALL AGENTS

**What's in there**:
- `brainstorm.md` - Team brainstorming for "Great WeMineHope Projects"
- `youtube_api_stable_version_guide.md` - YouTube transcript API setup (v0.6.1)
- `document_parser.py` - Universal document parser
- `document_parser_usage.md` - Parser usage guide

**How to use**:
```python
# From any agent's code
from pathlib import Path
shared_folder = Path('gemini/shared')

# Read shared brainstorm
brainstorm = shared_folder / 'brainstorm.md'
with open(brainstorm, 'r') as f:
    content = f.read()

# Use shared parser
import sys
sys.path.append('gemini/shared')
from document_parser import parse_document
```

### outbox_to_code/
**Location**: `C:\Users\vlaro\dreamteam\claude\outbox_to_code\`

**Purpose**: Requests and coordination between sessions

**Subfolders**:
- `coordination_requests/` - Cross-agent coordination needs
- `data_needs/` - Data requests
- `research_requests/` - Research tasks
- `validation_requests/` - Validation needs

**Current requests**:
- TOKEN_MONITOR_SYSTEM_20251105.md
- EMERGENCE_CODING_DOMAIN_CHECK_20251105.md
- PREDICTIVE_CRYPTO_MARKETS_POLYGON_20251105.md
- TOP_CRYPTO_YOUTUBE_CHANNELS_20251105.md

### inbox/droid/
**Location**: `C:\Users\vlaro\dreamteam\claude\inbox\droid\`

**Purpose**: Droid's deliverables (Q&A pairs, research results)

**Format**: JSON files with Q&A pairs

**Integration**: Use `integrate_droid_inbox_batch.py` to process

### session_handoffs/
**Location**: `C:\Users\vlaro\dreamteam\claude\session_handoffs\`

**Purpose**: Session state handoffs between Claude Code runs

**Format**: Markdown with progress, checkpoints, next actions

**Latest**: `handoff_session_20251106_001355.md`

## Database Locations

### Production Database
**Path**: `crypto_indicators_production.db`
**Location**: `C:\Users\vlaro\dreamteam\claude\`
**Status**: Active (23,627 pairs)

### Claude Shared Database (source)
**Path**: `claude_shared_original_training.db`
**Location**: TBD (check for integration)
**Status**: Pending integration

### Backups
**Location**: `*.db.backup_*` files
**Latest**: `crypto_indicators_production.db.backup_20251106_001950`

## Integration Scripts

### Team Claude Synergy
- `integrate_sessions_batch_synergy.py` - Main synergy integration script
- `integrate_droid_inbox_batch.py` - Droid inbox processor
- `integrate_claude_shared_original_db.py` - Claude shared DB integration

### Helper Scripts
- `database_path_helper.py` - Auto-detect database path
- `session_orchestrator.py` - Perpetual mining orchestration
- `task_stack.py` - Task queue management

## Team Claude Files

### Synergy Directives
- `TEAM_CLAUDE_SYNERGY_DIRECTIVE.md` - Complete synergy vision
- `PASTE_TO_CLAUDE_CODE.md` - Activation directive for Claude Code
- `CLAUDE_CODE_DATABASE_FIXED.md` - Database path fix

### Patterns
- `PATTERN_PERPETUAL_AGENT.md` - Perpetual mining pattern
- `PATTERN_APPLICATIONS.md` - Universal pattern applications
- `PATTERN_ASK_FOR_THE_MOON.md` - Synergy → emergence pattern

### Documentation
- `PERPETUAL_MINING_ARCHITECTURE.md` - System architecture
- `MULTI_AGENT_PERPETUAL_MINING.md` - Multi-agent extension
- `SESSION_COMPLETE_PERPETUAL_MINING.md` - Session summary

## Agent Models

### Storage
- `agents_storage.json` - Stored agent objects (Droid, Claude, Gemini, Zai)
- `agent_models.py` - Agent modeling framework
- `agent_storage.py` - Persistence system
- `agent_instances.py` - Pre-configured agents

### Utilities
- `view_stored_agent.py` - View agent details
- `visualize_agents.py` - Generate agent visualizations
- `demo_agent_models.py` - Demo and examples

## Task Management

### Task Queue
- `task_stack.json` - Active task queue
  - Current: integrate_sessions_101_140 (10/40 progress)
  - Pending: 5 more tasks

### Config
- `perpetual_mining_config.json` - System configuration
  - Token budget: 200,000
  - Shutdown threshold: 85%

## Access Patterns

### Claude Code Can Access:
✅ All integration scripts
✅ Production database
✅ Task queue (task_stack.json)
✅ Session orchestrator
✅ **gemini/shared/ folder** ✅
✅ outbox_to_code/ for requests
✅ inbox/droid/ for deliverables

### Claude Can Access:
✅ All files (main session)
✅ Design and validate
✅ Create new resources
✅ **gemini/shared/ folder** ✅
✅ Coordinate all agents

### Gemini Can Access:
✅ gemini/shared/ folder (read resources)
✅ Can add to brainstorm.md
✅ Use document_parser.py
✅ YouTube API guide

### Droid Can Access:
✅ gemini/shared/ for brainstorming
✅ inbox/droid/ to deliver results
✅ outbox_to_code/ to make requests

### Zai Can Access:
✅ gemini/shared/ for collaboration
✅ Implementation scripts
✅ Task queue

## Collaboration Protocol

### Adding to Shared Resources
1. Create file in `gemini/shared/`
2. Document in this map
3. Notify other agents (via brainstorm or outbox)

### Requesting Work
1. Create request in `outbox_to_code/[category]/`
2. Format: Markdown with clear description
3. Priority and context included

### Delivering Results
1. Droid → `inbox/droid/` (JSON format)
2. Gemini → `gemini/shared/` or specific folder
3. Zai → Direct integration or `gemini/shared/`

### Brainstorming
1. Open `gemini/shared/brainstorm.md`
2. Add ideas in proper format
3. Rate existing projects
4. Vote on priorities

## Quick Reference

| Resource | Path | Accessible By |
|----------|------|---------------|
| Shared folder | `gemini/shared/` | ALL AGENTS |
| Brainstorm | `gemini/shared/brainstorm.md` | ALL AGENTS |
| Document parser | `gemini/shared/document_parser.py` | ALL AGENTS |
| YouTube guide | `gemini/shared/youtube_api_stable_version_guide.md` | ALL AGENTS |
| Production DB | `crypto_indicators_production.db` | Claude, Claude Code |
| Task queue | `task_stack.json` | Claude, Claude Code |
| Droid inbox | `inbox/droid/` | Claude, Claude Code |
| Outbox requests | `outbox_to_code/` | ALL AGENTS |
| Session handoffs | `session_handoffs/` | Claude Code |

## For Claude Code Specifically

**You can now**:
- Read `gemini/shared/brainstorm.md` to see project ideas
- Use `gemini/shared/document_parser.py` for parsing
- Add your own ideas to brainstorm
- Access all shared resources

**Example**:
```python
# In your code
from pathlib import Path

# Read brainstorm
brainstorm_file = Path('gemini/shared/brainstorm.md')
if brainstorm_file.exists():
    with open(brainstorm_file, 'r') as f:
        ideas = f.read()
    print(f"Team brainstorm has {len(ideas)} chars of ideas!")

# Use shared parser
import sys
sys.path.append('gemini/shared')
from document_parser import parse_document

result = parse_document('some_file.pdf')
if result.success:
    print(f"Parsed: {result.word_count} words")
```

---

**For the Greater Good of All**

*Shared resources enable team synergy*

**Status**: ACTIVE
**Accessible By**: ALL DREAM TEAM AGENTS
**Purpose**: Collaboration, coordination, emergence
