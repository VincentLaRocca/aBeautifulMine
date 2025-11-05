# Droid MCP Protocol Briefing
**Date:** 2025-11-01
**From:** Claude (Orchestrator)
**To:** Droid (Content Generator)
**Status:** READY TO BEGIN

---

## Mission Overview

You are being assigned to test the **MCP-based collaboration protocol v1.0** for cryptocurrency indicator Q&A generation. This is a **pilot test** to prove we can complete sessions in 2-3 hours instead of 47 hours manual work.

**Goal:** Complete as many sessions as possible using the MCP protocol while I orchestrate.

---

## Your Role: Content Generator

As the **Content Generator**, you will:
1. ✅ Generate Q&A content via Gemini MCP server
2. ✅ Parse and structure responses into JSON
3. ✅ Validate quality (word count, structure)
4. ✅ Import completed sessions to database
5. ✅ Report results back to orchestrator

**What you will NOT do:**
- ❌ Manual research (Gemini generates the content)
- ❌ Wait for file-based approvals (real-time iteration)
- ❌ Multi-day workflows (complete in one session)

---

## MCP Protocol Understanding - CRITICAL

### The 4-Phase Workflow

**Phase 1: Session Setup (5 min)**
- Read session assignment
- Identify 5 indicators
- Initialize Gemini conversation:
  ```
  mcp__gemini__start_conversation(id="session_N")
  ```
- Set context prompt about crypto indicators, 2024-2025 market, 1200-1500 words per answer

**Phase 2: Batch Content Generation (1.5-2 hours)**
- For EACH of 5 indicators:
  - **Batch 1:** Generate Q1-Q3 (2-3 min per batch)
  - **Batch 2:** Generate Q4-Q6 (2-3 min per batch)
  - Use `mcp__gemini__chat` with conversationId for continuity
  - Parse responses (Gemini won't give perfect JSON)
  - Handle errors with 3-retry exponential backoff

**Phase 3: Python Assembly (30 min)**
- YOU assemble the JSON structure (not Gemini)
- Format: see `session_10_current_structure.json` as template
- Validate: 30 Q&A pairs, all >1000 words

**Phase 4: Delivery & Import (10 min)**
- Import to database: `crypto_indicators_qa.db`
- Run verification
- Generate completion report

### Key Constraints You MUST Follow

1. **Small Batches:** Only 2-3 questions per MCP request (token limits)
2. **Python Structures JSON:** Don't ask Gemini for perfect JSON
3. **Retry Pattern:** 3 attempts with 2^n second waits for 500 errors
4. **Conversation Continuity:** Always use same conversationId for a session

---

## Protocol Documents - READ THESE

**Primary Protocol:**
- `C:\Users\vlaro\dreamteam\claude\mcp-protocol-v1-practical.md` (full workflow)
- `C:\Users\vlaro\dreamteam\claude\mcp-protocol-quick-reference.md` (quick ref card)

**Supporting Docs:**
- `C:\Users\vlaro\dreamteam\claude\mcp-based-collaboration-protocol.md` (theory)
- `C:\Users\vlaro\dreamteam\claude\SESSION_NOTES_2025-11-01_CURSOR_CRASH.md` (context)

**Assessment Report:**
- `C:\Users\vlaro\dreamteam\claude\gemini-mcp-assessment-report.md` (Gemini limitations)

---

## Technical Resources

### MCP Server Access
You have access to these MCP tools:
- `mcp__gemini__start_conversation`
- `mcp__gemini__chat`
- `mcp__gemini__clear_conversation`

Your MCP config is in: `C:\Users\vlaro\.factory\mcp.json`

### Database
**Location:** `C:\Users\vlaro\dreamteam\claude\crypto_indicators_qa.db`
**Status:** ✅ Initialized with proper schema (sessions, indicators, qa_pairs)
**Import Script:** `C:\Users\vlaro\dreamteam\claude\import_session_generic.py`

### Template Files
**JSON Structure:** `C:\Users\vlaro\dreamteam\claude\session_10_current_structure.json`
**Example Session:** `C:\Users\vlaro\dreamteam\claude\session_10_transaction_metrics_qa_dataset.json`

---

## Session Assignment Options

### Recommended: Start with Session 11
**Indicators 51-55:**
- Session 10 has incomplete data (only 1 Q&A pair)
- Session 11 would be cleaner to start fresh
- Follows natural progression

**OR**

### Alternative: Start with Session 12
**Indicators 56-60:**
- This was the original pilot test session in the protocol docs
- Clean slate, no prior work

**Decision:** Your choice - whichever you prefer!

---

## Standard 6 Questions Per Indicator

Every indicator gets these 6 questions:
1. What is [indicator] and how is it measured/calculated?
2. How is [indicator] specifically used in cryptocurrency trading?
3. What are the optimal settings/thresholds for [indicator] in crypto markets?
4. What trading strategies work best with [indicator] in crypto?
5. How can [indicator] be combined with other indicators?
6. What are common mistakes when using [indicator] in crypto markets?

---

## Quality Standards

### Each Answer Must Include:
- ✅ 1,200-1,500 words (minimum 1,000)
- ✅ 2024-2025 market context (ETF approvals, institutional adoption)
- ✅ Layer 2 scaling considerations (where relevant)
- ✅ Cross-chain analysis (Bitcoin UTXO vs Ethereum account model)
- ✅ Data sources (Glassnode, IntoTheBlock, Santiment)
- ✅ Trading strategies with specific entry/exit rules
- ✅ Risk management guidelines

### Validation Checklist:
- [ ] 30 Q&A pairs total (5 indicators × 6 questions)
- [ ] All answers ≥1,000 words
- [ ] Valid JSON structure
- [ ] No truncated/incomplete answers
- [ ] Database import successful

---

## Error Handling You'll Encounter

### 500 Internal Error
**Solution:** Retry 3× with exponential backoff (2s, 4s, 8s)
```python
for attempt in range(3):
    try:
        return mcp__gemini__chat(...)
    except:
        if attempt < 2:
            time.sleep(2 ** attempt)
        else:
            raise
```

### Token Limit Exceeded
**Solution:** Request completion
```
Prompt: "Complete the previous answer from where it was cut off"
```

### Answer Too Short
**Solution:** Request expansion
```
Prompt: "Previous answer was {X} words, please expand to 1200-1500 words"
```

---

## Success Metrics

### Must-Have (Session Approved)
- ✅ 30 Q&A pairs generated
- ✅ Valid JSON structure
- ✅ All answers ≥1,000 words
- ✅ Import successful to database

### Target (Excellent Performance)
- 🎯 Completed in <3 hours
- 🎯 Cost <$2.00
- 🎯 Quality score ≥95%
- 🎯 Error rate <5%

---

## Orchestrator Support (Me - Claude)

I will:
- ✅ Assign sessions
- ✅ Monitor progress
- ✅ Provide guidance if you get stuck
- ✅ Verify final results
- ✅ Track overall metrics

I will NOT:
- ❌ Do content generation
- ❌ Parse responses
- ❌ Assemble JSON
- ❌ Import to database

**You own the execution. I orchestrate.**

---

## Communication Protocol

### When You Start
Create: `C:\Users\vlaro\dreamteam\claude\outbox\droid-session-N-started.md`
Include:
- Session number
- Start timestamp
- Indicators list

### Progress Updates (Optional)
If you want to report progress:
`C:\Users\vlaro\dreamteam\claude\outbox\droid-session-N-progress.md`

### When You Complete
Create: `C:\Users\vlaro\dreamteam\claude\outbox\droid-session-N-complete.md`
Include:
- Completion timestamp
- Final JSON file location
- Database import status
- Quality metrics
- Any issues encountered

---

## Test Run Expectations

### Session 1 (Your First Test)
**Goal:** Validate the entire workflow end-to-end
**Expectation:** May take 3-4 hours as you learn the process
**Focus:** Correctness over speed

### Session 2+ (If Session 1 Succeeds)
**Goal:** Optimize for speed and scale
**Expectation:** Should hit 2-3 hour target
**Focus:** Efficiency and automation

### How Many Sessions?
**Target:** Complete as many as you can until:
- You hit a blocker
- Cost becomes prohibitive (>$5 total)
- Quality drops below 90%
- OR you complete 3-5 sessions successfully 🎉

---

## Critical Success Factors

1. **Read the protocol docs FIRST** - Don't wing it
2. **Small batches** - 2-3 questions max per request
3. **Python handles JSON** - Don't rely on Gemini for structure
4. **Retry logic** - Build it in from the start
5. **Validate before import** - Catch issues early

---

## Ready to Begin?

### Pre-Flight Checklist
- [ ] Read `mcp-protocol-v1-practical.md`
- [ ] Read `mcp-protocol-quick-reference.md`
- [ ] Verify MCP server access
- [ ] Review JSON template structure
- [ ] Decide which session to start with (11 or 12)

### When Ready
1. Create your "started" file in outbox
2. Initialize your first Gemini conversation
3. Begin Phase 1: Session Setup

---

## Questions Before You Start?

I'm here as orchestrator if you need:
- Clarification on protocol
- Session assignment details
- Technical support
- Quality validation

**Otherwise, you have full autonomy to execute!**

---

**STATUS: AWAITING YOUR ACKNOWLEDGMENT**

Please confirm:
1. You've read and understand the MCP protocol
2. Which session you want to start with (11 or 12)
3. You're ready to begin

**Good luck, Droid! Let's prove this protocol works! 🚀**
