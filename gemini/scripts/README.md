# GitHub Scripts - Gemini Shared Area

**Location**: `gemini/scripts/`
**Purpose**: Shared scripts for Gemini workflow coordination

---

## 📜 Available Scripts

### 1. **auto_push_to_github.sh**
Automatically commits and pushes Gemini output to GitHub.

**Usage**:
```bash
cd ../..  # Go to repo root
./gemini/scripts/auto_push_to_github.sh "Your commit message"

# OR auto-generate message
./gemini/scripts/auto_push_to_github.sh
```

### 2. **quick_push.sh**
Quick shorthand for pushing Gemini deliveries.

**Usage**:
```bash
cd ../..
./gemini/scripts/quick_push.sh "Gemini Deep Research: Batch 4 complete"
```

### 3. **scheduled_push.sh**
Continuously monitors and auto-pushes changes on interval.

**Usage**:
```bash
cd ../..
# Push every 30 minutes
./gemini/scripts/scheduled_push.sh 30
```

### 4. **auto_sync_team_commits.sh**
Monitors GitHub for commits from other team members and auto-pulls.

**Usage**:
```bash
cd ../..
# Start monitoring (checks every 2 minutes)
./gemini/scripts/auto_sync_team_commits.sh
```

---

## 🎯 Gemini Workflow Integration

### After Receiving Gemini Output
```bash
# Navigate to repo root
cd C:\Users\vlaro\dreamteam\claude

# Push Gemini results
./gemini/scripts/quick_push.sh "Gemini output: 100 Ichimoku Tenkan-sen answers"
```

### Shared Question Sets
When Claude Desktop pushes new question sets:
```bash
# Sync monitor will auto-pull new questions
./gemini/scripts/auto_sync_team_commits.sh
```

### After Processing Gemini Results
```bash
# After parsing/formatting Gemini output
./gemini/scripts/auto_push_to_github.sh "Formatted Gemini Batch 4 output for integration"
```

---

## 📁 Directory Structure

```
gemini/
├── scripts/          # <- You are here
│   ├── auto_push_to_github.sh
│   ├── quick_push.sh
│   ├── scheduled_push.sh
│   └── auto_sync_team_commits.sh
├── shared/           # Question sets & coordination
│   ├── question_sets/
│   └── BATCH_4_ACTIVATION_NOV08.md
└── outbox/           # Gemini output for Claude Code
    └── claude/
```

---

## 🔄 Team Odd Couple Integration

**The Flow**:
1. Claude Desktop generates questions → pushes to `gemini/shared/`
2. Sync monitor alerts Vinny → submits to Gemini
3. Gemini produces answers → saved to `gemini/outbox/claude/`
4. Push to GitHub → Claude Code's sync monitor auto-pulls
5. Claude Code integrates → everyone synced!

---

**For the Greater Good of All** ✨
