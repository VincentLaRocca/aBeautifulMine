# MCP Protocol v1.0: Practical Implementation

**Date:** 2025-11-01
**Status:** READY FOR FIELD TEST
**Scope:** Sessions 12-13 (Pilot Test)
**Team:** Claude (Orchestrator), Droid (Content Generator), Gemini (MCP Backend)

---

## Executive Summary

This protocol adapts the ideal MCP-based collaboration workflow to work within **real-world Gemini MCP constraints** discovered during Session 10.

**Key Adaptations:**
- ✅ Small batch sizes (2-3 questions max per request)
- ✅ Python handles JSON assembly (not Gemini)
- ✅ Retry logic for 500 errors
- ✅ Pragmatic completion criteria
- ✅ Hybrid fallback ready

**Target Performance:**
- 5 indicators per session (30 Q&A pairs)
- ~2-3 hours total time (vs 47 hours manual)
- <$2.00 cost per session
- 95%+ first-draft quality

---

## Gemini MCP Constraints (From Assessment)

### Hard Limits
1. **Token Limit:** 15,000-20,000 output tokens per request
   - **Impact:** ~2,000 words max per response
   - **Solution:** Batch 2-3 questions per request

2. **Structured Data:** Deviates from exact JSON schemas
   - **Impact:** Can't generate final import-ready JSON
   - **Solution:** Use Python for final assembly

3. **Reliability:** ~12% error rate (500 INTERNAL errors)
   - **Impact:** Occasional request failures
   - **Solution:** 3-retry pattern with exponential backoff

4. **Verbosity:** Tends to exceed word count targets
   - **Impact:** Hits token limits more frequently
   - **Solution:** Accept 1,000-2,000 word variance

### Strengths to Leverage
- ✅ Content quality: A+ institutional-grade
- ✅ Context continuity: Excellent with conversationId
- ✅ Speed: 18x faster than manual
- ✅ Cost: ~$0.04 per answer
- ✅ Domain expertise: Strong crypto/blockchain knowledge

---

## Protocol v1.0: Practical Workflow

### Phase 1: Session Setup (5 minutes)

**Agent:** Claude (Orchestrator)

**Steps:**
1. Read session assignment from user/Droid
2. Identify 5 indicators for the session
3. Initialize Gemini conversation:
   ```python
   mcp__gemini__start_conversation(id=f"session_{session_num}")
   ```
4. Set context with initial prompt:
   ```
   You are generating institutional-grade cryptocurrency indicator Q&A pairs.
   Target: 1,200-1,500 words per answer
   Context: 2024-2025 market (ETFs, Layer 2, institutional adoption)
   Maintain context across multiple requests.
   ```

**Success Criteria:** Conversation initialized, session context set

---

### Phase 2: Batch Content Generation (1.5-2 hours)

**Agent:** Claude orchestrating Gemini MCP

**Workflow Pattern:**

#### For Each Indicator (5 iterations):

**Step 1: Generate Q1-Q3 (First Batch)**
```python
prompt = f"""
Generate comprehensive answers for these 3 questions about {indicator_name}:

Q1: What is {indicator_name} and how is it measured/calculated?
Q2: How is {indicator_name} specifically used in cryptocurrency trading?
Q3: What are the optimal settings/thresholds for {indicator_name} in crypto markets?

Requirements:
- 1,200-1,500 words per answer
- 2024-2025 market context (ETFs, Layer 2, institutional adoption)
- Distinguish Bitcoin UTXO vs Ethereum account-based models where relevant
- Include entity-adjusted metrics considerations
- Reference major data providers (Glassnode, CryptoQuant, IntoTheBlock)

Format as:
Q1: [question text]
A1: [comprehensive answer]

Q2: [question text]
A2: [comprehensive answer]

Q3: [question text]
A3: [comprehensive answer]
"""

response = mcp__gemini__chat(
    message=prompt,
    conversationId=f"session_{session_num}",
    model="gemini-2.5-pro",
    maxTokens=15000
)
```

**Expected Time:** 2-3 minutes per batch
**Expected Cost:** ~$0.12 per batch

**Step 2: Parse and Store Q1-Q3**
```python
# Claude parses the response (not Gemini)
qa_pairs = parse_gemini_response(response)
temp_storage[indicator_name]['q1_q3'] = qa_pairs
```

**Step 3: Generate Q4-Q6 (Second Batch)**
```python
prompt = f"""
Continue with the next 3 questions for {indicator_name}:

Q4: What trading strategies work best with {indicator_name} in crypto?
Q5: How can {indicator_name} be combined with other indicators?
Q6: What are common mistakes when using {indicator_name} in crypto markets?

Requirements: [same as above]
"""

response = mcp__gemini__chat(
    message=prompt,
    conversationId=f"session_{session_num}",
    model="gemini-2.5-pro",
    maxTokens=15000
)
```

**Step 4: Parse and Store Q4-Q6**

**Step 5: Retry Logic (If Needed)**
```python
def call_with_retry(prompt, conv_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return mcp__gemini__chat(message=prompt, conversationId=conv_id)
        except Exception as e:
            if "500" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise
```

**Repeat for all 5 indicators**

**Total Time:** ~15-20 minutes per indicator × 5 = 1.5-2 hours
**Total Cost:** ~$0.24 × 5 = ~$1.20 per session

---

### Phase 3: Python Assembly (30 minutes)

**Agent:** Claude (Orchestrator)

**Why Not Gemini:** Session 10 proved Gemini deviates from exact JSON schemas

**Workflow:**
```python
# Structure the data properly
session_data = {
    "session": session_num,
    "date": datetime.now().strftime("%Y-%m-%d"),
    "category": session_category,
    "indicators": [ind1, ind2, ind3, ind4, ind5],
    "total_qa_pairs": 30,
    "qa_pairs": []
}

# Add all parsed Q&A pairs
for indicator_name in indicators:
    for qa in temp_storage[indicator_name]['q1_q3'] + temp_storage[indicator_name]['q4_q6']:
        session_data["qa_pairs"].append({
            "indicator": indicator_name,
            "question": qa['question'],
            "answer": qa['answer']
        })

# Validate structure
assert len(session_data["qa_pairs"]) == 30
assert all(len(qa["answer"].split()) >= 1000 for qa in session_data["qa_pairs"])

# Write to file
with open(f"crypto-indicators-session-{session_num}-qa-FINAL.json", 'w') as f:
    json.dump(session_data, f, indent=2, ensure_ascii=False)
```

**Success Criteria:**
- Valid JSON structure matching import script schema
- All 30 Q&A pairs present
- Minimum 1,000 words per answer
- Ready for database import

---

### Phase 4: Delivery & Import (10 minutes)

**Agent:** Claude (Orchestrator)

**Steps:**
1. **Quality Check:**
   - Run validation script on JSON
   - Verify no duplicate questions
   - Check answer completeness

2. **Deliver to Gemini:**
   ```bash
   cp session-{N}-qa-FINAL.json ~/dreamteam/Gemini/Inbox/claude/
   ```

3. **Create Completion Report:**
   - Session summary
   - Quality metrics
   - Cost breakdown
   - Any issues encountered

4. **Database Import:**
   ```bash
   python import_session_generic.py
   ```

5. **Verify Import:**
   ```bash
   python verify_database_integrity.py
   ```

**Success Criteria:**
- File delivered to Gemini inbox
- Database import successful
- Integrity check passes
- Progress updated (e.g., 60 of 227 indicators)

---

## Error Handling & Recovery

### Error Type 1: Token Limit Exceeded (MAX_TOKENS)

**Symptom:** Answer cuts off mid-sentence

**Solution:**
```python
# Check if response was truncated
if response.endswith('...') or len(response.split()) < expected_min_words:
    # Request completion
    completion_prompt = f"Please complete the previous answer starting from where it was cut off."
    completion = mcp__gemini__chat(
        message=completion_prompt,
        conversationId=conv_id,
        maxTokens=10000
    )
    full_answer = response + " " + completion
```

**Prevention:** Reduce batch size to 2 questions if hitting limits consistently

---

### Error Type 2: 500 Internal Server Error

**Symptom:** `{"error":{"code":500,"message":"An internal error has occurred..."}}`

**Solution:** Already implemented in retry logic (Phase 2, Step 5)

**Escalation:** If 3 retries fail, continue with next batch and flag for manual review

---

### Error Type 3: Incomplete Answers

**Symptom:** Answer is <1,000 words or missing key sections

**Solution:**
```python
# Request expansion
expansion_prompt = f"""
The previous answer for Q{n} about {indicator} was too brief ({word_count} words).
Please provide a more comprehensive answer covering:
- Detailed explanation
- Real-world examples
- 2024-2025 market context
- Practical trading applications
Target: 1,200-1,500 words
"""
```

---

### Error Type 4: JSON Assembly Errors

**Symptom:** Python script fails validation

**Solution:**
```python
# Manual inspection and fix
print("Validation failed. Checking issues...")
for i, qa in enumerate(session_data["qa_pairs"]):
    if "indicator" not in qa:
        print(f"Missing indicator in pair {i}")
    if not qa.get("answer"):
        print(f"Empty answer in pair {i}")
# Fix issues and re-validate
```

**Prevention:** Use try-except blocks and detailed error messages

---

## Success Metrics (Per Session)

### Must-Have (Hard Requirements)
- ✅ 30 Q&A pairs generated (5 indicators × 6 questions)
- ✅ Valid JSON structure (passes import script validation)
- ✅ All answers ≥1,000 words
- ✅ Database import successful
- ✅ Zero duplicate questions

### Target (Soft Goals)
- 🎯 Average answer length: 1,200-1,500 words
- 🎯 Total time: <3 hours
- 🎯 Total cost: <$2.00
- 🎯 First-draft quality: ≥95% (minimal edits needed)
- 🎯 Error rate: <5% (maximum 1 failed batch)

### Stretch (Nice-to-Have)
- ⭐ All answers 1,200-1,500 words (no outliers)
- ⭐ Total time: <2 hours
- ⭐ Zero errors/retries needed
- ⭐ 100% first-draft quality (no edits)

---

## Pilot Test Plan: Sessions 12-13

### Session 12: Full MCP Test
**Goal:** Test complete MCP workflow end-to-end

**Indicators:** 5 indicators from Session 12 assignment
**Protocol:** Full Protocol v1.0 as documented above
**Monitoring:**
- Time each phase
- Count retries needed
- Track token usage
- Note any deviations from protocol

**Success Criteria:**
- Complete session in <3 hours
- Cost <$2.00
- Valid JSON delivered
- Database import successful

**Deliverable:** Session 12 completion + performance report

---

### Session 13: Refinement Test
**Goal:** Apply learnings from Session 12

**Adjustments Based on Session 12:**
- Batch size optimization (if needed)
- Prompt refinements
- Error handling improvements
- Timing adjustments

**Success Criteria:**
- Improvement in at least 2 metrics vs Session 12
- Further reduce manual intervention
- Approach stretch goals

**Deliverable:** Session 13 completion + comparative analysis

---

## Fallback Strategy: Hybrid Protocol

**Trigger Conditions:**
- Gemini MCP down/unreliable (>3 consecutive 500 errors)
- Quality below 90% (major rewrites needed)
- Cost exceeds $3.00 per session
- Time exceeds 4 hours

**Fallback Plan:**
1. **Use Gemini MCP for content drafts** (as planned)
2. **Droid reviews and refines** (inbox/outbox workflow)
3. **Claude assembles final JSON** (as planned)
4. **Extended timeline:** Allow 24 hours for Droid review

**When to Escalate:**
- After 2 consecutive session failures with MCP
- User requests return to inbox/outbox
- Consensus from team that quality is suffering

---

## Communication Protocol

### Daily Check-ins (During Pilot)
**Agent:** Claude posts to shared location

**Format:**
```markdown
## Session {N} Progress Update

**Status:** [In Progress / Blocked / Complete]
**Phase:** [Setup / Generation / Assembly / Delivery]
**Time Elapsed:** {X} hours
**Cost to Date:** ${X.XX}
**Issues:** [None / See details below]

**Next Step:** [What happens next]
**ETA:** [When session will complete]
```

### Completion Reports
**Agent:** Claude delivers to all inboxes

**Contents:**
- Full session summary
- Performance vs targets
- Lessons learned
- Recommendations for next session

### Escalation Path
1. **Minor Issue:** Claude handles autonomously (retry logic)
2. **Moderate Issue:** Claude documents and continues
3. **Major Issue:** Claude notifies user and awaits direction

---

## Tool Reference: Gemini MCP Commands

### Essential Tools for Protocol v1.0

```python
# 1. Start conversation
mcp__gemini__start_conversation(
    id="session_12"  # Use consistent IDs
)

# 2. Generate content
mcp__gemini__chat(
    message=prompt,
    conversationId="session_12",
    model="gemini-2.5-pro",
    maxTokens=15000,
    temperature=1.0  # Default
)

# 3. Clear conversation (if needed to restart)
mcp__gemini__clear_conversation(
    id="session_12"
)
```

### Advanced Tools (Optional)

```python
# For very large batches (not needed for 30 Q&A)
mcp__gemini__batch_process(
    inputFile="session_12_questions.jsonl",
    model="gemini-2.5-pro",
    outputLocation="./batch_results/"
)

# For embeddings (future feature)
mcp__gemini__batch_process_embeddings(
    inputFile="indicators_for_search.txt",
    taskType="SEMANTIC_SIMILARITY"
)
```

---

## Cost Breakdown

### Per-Session Estimate

**Content Generation:**
- 10 batches (2× per indicator × 5 indicators)
- ~3,500 output tokens per batch × 10 = 35,000 tokens
- ~2,000 input tokens total (prompts)
- Cost: (2K × $0.005) + (35K × $0.015) = $0.01 + $0.53 = **$0.54**

**Retries/Completions (estimated 20% overhead):**
- Additional ~7,000 tokens
- Cost: 7K × $0.015 = **$0.11**

**Total per Session:** ~$0.65

**Safety Buffer (3× for unexpected issues):** **$1.95**

**Realistic Budget:** **$0.65 - $2.00 per session**

### Project-Level Estimate

**Remaining Sessions:** 227 total - 55 complete = 172 indicators
**Sessions at 5 indicators each:** 172 ÷ 5 = ~35 sessions

**Total Project Cost (MCP approach):**
- Low estimate: 35 × $0.65 = **$22.75**
- High estimate: 35 × $2.00 = **$70.00**
- Expected: ~**$40-50 total**

**vs Manual Generation Cost:**
- 172 indicators × 6 questions × 45 min × $50/hr = **$38,700**

**ROI:** 970× - 1,700×

---

## Quality Control Checklist

### Before Delivery (Claude's responsibility)

- [ ] All 30 Q&A pairs present
- [ ] Each answer ≥1,000 words
- [ ] No duplicate questions
- [ ] Valid JSON structure
- [ ] All indicators have exactly 6 questions
- [ ] No truncated/incomplete answers
- [ ] Proper formatting (no markdown artifacts)
- [ ] 2024-2025 context included
- [ ] Entity-adjusted metrics mentioned where relevant
- [ ] Layer 2 considerations addressed where relevant

### After Import (Verification)

- [ ] Database import successful (no errors)
- [ ] Integrity check passes
- [ ] No duplicate question detection triggered
- [ ] Session count updated correctly
- [ ] Total indicator count updated
- [ ] Q&A pair count matches expected

---

## Lessons from Session 10 (Don't Repeat)

### ❌ What Didn't Work

1. **Trying to generate all 18 answers at once**
   - Hit token limits immediately
   - Lost context, got incomplete answers

2. **Asking Gemini to assemble final JSON**
   - Deviated from schema despite examples
   - Created extra work reformatting

3. **Not implementing retry logic upfront**
   - 500 error disrupted workflow
   - Had to manually adjust approach

4. **Uploading reference files to Gemini**
   - Got 500 error
   - Wasted time on failed approach

### ✅ What Worked

1. **Small batches (2-3 questions)**
   - Reliable, consistent results
   - Fewer token limit issues

2. **Conversation continuity (conversationId)**
   - Context maintained across requests
   - No redundant explanations

3. **Pragmatic completion criteria**
   - Imported what was ready
   - Documented what was pending
   - Maintained momentum

4. **Python for structured data**
   - Full control over JSON format
   - Easy to validate and fix

---

## Decision Points During Execution

### Decision Point 1: Batch Size
**When:** After first indicator
**Question:** Are we hitting token limits?

**Options:**
- A) Keep at 3 questions per batch (if working)
- B) Reduce to 2 questions per batch (if limits hit)
- C) Increase to 4 questions (if plenty of headroom)

**Criteria:** If any answer >1,500 words and hitting limits → Reduce batch size

---

### Decision Point 2: Retry vs Skip
**When:** After 3 failed retries
**Question:** Continue or skip this batch?

**Options:**
- A) Skip and flag for manual review (if multiple batches pending)
- B) Keep retrying with modified prompt (if critical blocker)
- C) Switch to alternative model (gemini-2.5-flash)

**Criteria:** If blocking overall progress → Skip and continue

---

### Decision Point 3: Quality vs Speed
**When:** Mid-session quality check
**Question:** Are answers meeting quality bar?

**Options:**
- A) Continue as-is (if ≥95% quality)
- B) Request expansions/refinements (if 80-94% quality)
- C) Escalate to Hybrid Protocol (if <80% quality)

**Criteria:** Balance session timeline with quality requirements

---

## Post-Pilot Review Template

### After Session 12 Completion

**Performance:**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Time | <3 hrs | {X} hrs | ✅/⚠️/❌ |
| Cost | <$2.00 | ${X} | ✅/⚠️/❌ |
| Quality | ≥95% | {X}% | ✅/⚠️/❌ |
| Errors | <5% | {X}% | ✅/⚠️/❌ |

**What Went Well:**
- [List successes]

**What Went Wrong:**
- [List issues]

**Adjustments for Session 13:**
- [Specific changes to implement]

**Continue/Modify/Abort:**
- [ ] Continue with Protocol v1.0 (no changes)
- [ ] Continue with modifications (see above)
- [ ] Switch to Hybrid Protocol
- [ ] Abort MCP approach (return to inbox/outbox)

---

## Summary: Key Differences from Original Protocol

### Original "Protocol A: Full MCP" vs v1.0 Practical

| Aspect | Original Design | v1.0 Practical |
|--------|----------------|----------------|
| **Batch Size** | 6 questions at once | 2-3 questions per batch |
| **JSON Assembly** | Gemini generates final JSON | Python assembles from parsed text |
| **Error Handling** | Generic retry | Specific 500/token/quality handlers |
| **Quality Check** | Automated validation | Manual + automated checks |
| **Timeline** | Optimistic (1 hour) | Realistic (2-3 hours) |
| **Fallback** | Not specified | Hybrid protocol ready |
| **Cost Estimate** | $0.71 per session | $0.65-$2.00 range |

### Why These Changes?

**Real-world constraints beat ideal designs.**

Session 10 taught us that Gemini MCP is powerful but has limitations. v1.0 works *with* those limitations rather than fighting them.

The goal: **Reliable 95% quality output in 2-3 hours** rather than **perfect 100% quality that takes 10 attempts**.

---

## Authorization & Sign-Off

**Protocol Owner:** Claude (Orchestrator)
**Approved By:** User (Project Lead)
**Technical Review:** Gemini (MCP Backend)
**Implementation:** Droid (Content Generator) + Claude

**Status:** Ready for Pilot Test
**Start Date:** Session 12 (Next Assignment)
**Review Date:** After Session 13 Completion

**Signatures:**
- Claude Code: ✅ Ready to Execute
- Gemini: ✅ Constraints Understood
- Droid: ⏳ Awaiting MCP Activation
- User: ⏳ Approval Pending

---

**Document Version:** 1.0
**Last Updated:** 2025-11-01
**Next Review:** After Session 13
**Location:** `~/dreamteam/claude/mcp-protocol-v1-practical.md`

---

*Let's ship it! 🚀*
