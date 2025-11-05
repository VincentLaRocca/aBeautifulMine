# ✅ Session Wrap Checklist

**Use this when token usage hits 85% or at natural session end**

---

## 🎯 WRAP TRIGGER CONDITIONS:

- [ ] Token usage ≥ 85% (run `python token_monitor_simple.py [current_tokens]`)
- [ ] Natural stopping point reached (task completed)
- [ ] Major milestone achieved
- [ ] User requests session wrap

---

## 📋 PRE-WRAP CHECKLIST:

### **1. Complete Current Work**
- [ ] Finish current task (don't leave half-done)
- [ ] Test any code written
- [ ] Verify database integrity if modified
- [ ] Close any open logical loops

### **2. Document Session State**
- [ ] Note what was accomplished
- [ ] List in-progress work
- [ ] Identify next priorities
- [ ] Record any blocking issues

### **3. Check Async Work Streams**
- [ ] Check `inbox_from_code/` for new deliverables
- [ ] Check `inbox_from_gemini/` for updates
- [ ] Note status of active missions
- [ ] Document pending responses

---

## 💾 COMMIT SEQUENCE:

### **Step 1: Stage Changes**
```bash
cd /c/Users/vlaro/dreamteam/claude
git status  # Review what's changed
git add .   # Or add specific files
```

### **Step 2: Commit with Template**
```bash
git commit -m "$(cat <<'EOF'
Session Wrap: [Brief description of main work]

Token usage: [X]% of 200K budget
Session duration: [X] hours

COMPLETED:
- [Achievement 1]
- [Achievement 2]
- [Achievement 3]

IN PROGRESS:
- [Ongoing work 1]
- [Ongoing work 2]

NEXT SESSION PRIORITIES:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

ACTIVE MISSIONS:
- ClaudeCodeNet: [List pending deliverables]
- Gemini: [List pending tasks]
- Droid: [List status]

DATABASE STATUS:
- [X] pairs ([X]% of goal)

BLOCKING ISSUES:
[None / List any blockers]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### **Step 3: Push to GitHub (if applicable)**
```bash
git push origin main
```

---

## 📄 HANDOFF DOCUMENT:

Create: `SESSION_HANDOFF_[YYYYMMDD_HHMM].md`

```markdown
# Session Handoff: [Date/Time]

## Session Statistics:
- **Tokens Used:** [X] / 200,000 ([X]%)
- **Duration:** [X] hours
- **Status:** Clean wrap at [X]% threshold

## Accomplishments This Session:
1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

## Current System State:

### Database:
- Total pairs: [X] ([X]% of 30,000 goal)
- Last integration: [Source name]

### Git Status:
- Branch: main
- Last commit: [Hash] - [Message]
- Status: Clean / [X uncommitted files]

### Active Missions:

**ClaudeCodeNet (Internet Research):**
- Mission 1: [Status - Pending/In Progress/Delivered]
- Mission 2: [Status]
- Expected deliverables in: inbox_from_code/

**Gemini (Batch Processing):**
- Mission 1: [Status]
- Expected deliverables in: inbox_from_gemini/

**Droid:**
- Status: [Current state]

### Inbox Status:
- inbox_from_code: [X] new files
- inbox_from_gemini: [X] new files
- inbox_from_droid: [X] new files

## In-Progress Work:
1. [Task 1 - X% complete]
2. [Task 2 - X% complete]

## Next Session Priorities:
1. [Priority 1 - Why important]
2. [Priority 2 - Why important]
3. [Priority 3 - Why important]

## Blocking Issues:
[None / List any]

## Context Notes:
[Any important context for next session - decisions made,
 discoveries, things to remember]

## Quick Resume Commands:
```bash
# Check for new deliverables
ls inbox_from_code/
ls inbox_from_gemini/

# Check database status
python check_db_status.py

# Resume work on [specific task]
[Command or note]
```

---

**Handoff created:** [Timestamp]
**Next session start:** Fresh 200K token budget ✅
```

---

## 🧹 CLEANUP CHECKLIST:

- [ ] All work committed to git
- [ ] Handoff document created
- [ ] Session summary updated (if applicable)
- [ ] Inbox status documented
- [ ] No hanging processes
- [ ] Ready for fresh start

---

## 🚀 EXIT CLEANLY:

**You're done when:**
- ✅ All changes committed
- ✅ Handoff document complete
- ✅ Next priorities clear
- ✅ No blocking issues undocumented
- ✅ System in clean state

**Then:**
- Exit current session
- Start fresh session with full 200K token budget
- Read handoff document
- Check inboxes
- Continue momentum

---

## 💡 WRAP TIPS:

**Good wrap points:**
- Just completed a major task
- Database integration finished
- Documentation set complete
- Before starting large new task

**Bad wrap points:**
- Middle of complex operation
- Database in inconsistent state
- Uncommitted code changes
- Mid-debugging session

**Pro tip:** Start looking for wrap opportunities at 70-75% token usage. By the time you find a good stopping point, you'll be at 85%.

---

## 📊 EFFICIENCY TRACKING:

Track these over time to optimize:
- Average tokens per session
- Sessions per day
- Token efficiency (work completed per token)
- Time to wrap (should be < 15 minutes)

**Goal:** Maximize work completed while staying under 90% token usage.

---

**For the Greater Good of All** 🌟

**WRAP CLEAN. START FRESH. NEVER STOP PROGRESSING.** ⚡
