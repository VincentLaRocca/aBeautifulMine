# MCP-Based Agent Collaboration Protocol
## Alternative to Inbox/Outbox File System

**Version:** 1.0
**Date:** 2025-11-01
**Author:** Claude Code (Dream Team Orchestrator)
**Status:** PROPOSED - Awaiting Approval

---

## Executive Summary

This document proposes a **Model Context Protocol (MCP) based collaboration system** as an alternative to the current file-based inbox/outbox protocol. The MCP approach enables **real-time, API-driven agent collaboration** while maintaining quality control and workflow transparency.

**Key Advantages:**
- ⚡ Real-time communication (vs async file-based)
- 🎯 Direct quality feedback loops
- 📊 Automated validation and verification
- 🔄 Iterative refinement capability
- 💰 Cost-effective scaling

**Trade-offs:**
- Requires robust error handling
- Less transparent audit trail (vs files)
- Dependency on API availability
- Need for conversation state management

---

## Protocol Comparison

### Current Inbox/Outbox Protocol

```
Orchestrator → Droid/Gemini
    │
    ├─ Write assignment to {Agent}/Inbox/
    ├─ Agent works independently
    ├─ Agent writes output to {Agent}/Outbox/
    └─ Orchestrator reads, verifies, imports

Pros:
✅ Clear audit trail (files persist)
✅ Async - agents work independently
✅ Simple, reliable, transparent
✅ Easy to debug (can read files)
✅ No API dependencies

Cons:
❌ Slower (async file I/O)
❌ No real-time feedback
❌ Manual quality iteration
❌ File management overhead
❌ No automatic validation
```

### Proposed MCP Protocol

```
Orchestrator → Gemini MCP Server
    │
    ├─ Direct API call with specifications
    ├─ Real-time generation
    ├─ Immediate quality check
    ├─ Iterative refinement if needed
    └─ Direct database import

Pros:
✅ Real-time (seconds vs hours/days)
✅ Immediate feedback loops
✅ Automated quality control
✅ Iterative refinement built-in
✅ No file management

Cons:
❌ API dependency (uptime risk)
❌ Less visible audit trail
❌ Requires error handling
❌ Conversation state management
❌ Token limit considerations
```

---

## MCP Protocol Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR (Claude)                  │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Session Manager                                   │  │
│  │  - Tracks conversations                            │  │
│  │  - Manages context                                 │  │
│  │  - Handles retries                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                               │
│                           ├─────────────────────┐        │
│                           │                     │        │
│  ┌────────────────────────▼─────┐  ┌───────────▼─────┐  │
│  │  Content Generator            │  │  Quality Control│  │
│  │  - Sends prompts              │  │  - Validates    │  │
│  │  - Manages batches            │  │  - Verifies     │  │
│  │  - Handles pagination         │  │  - Scores       │  │
│  └────────────────┬──────────────┘  └────────┬────────┘  │
│                   │                           │           │
└───────────────────┼───────────────────────────┼───────────┘
                    │                           │
          ┌─────────▼───────────┐     ┌────────▼─────────┐
          │                     │     │                   │
          │  GEMINI MCP SERVER  │     │  DATABASE         │
          │                     │     │                   │
          │  - chat             │     │  - Import results │
          │  - batch_process    │     │  - Verify         │
          │  - upload_file      │     │  - Track metrics  │
          │                     │     │                   │
          └─────────────────────┘     └───────────────────┘
```

---

## Core Components

### 1. Session Manager

**Purpose:** Orchestrate multi-turn agent interactions

**Responsibilities:**
- Initialize conversations with proper context
- Track conversation IDs for continuity
- Manage conversation lifecycle
- Handle state persistence

**Implementation:**

```python
class SessionManager:
    def __init__(self):
        self.conversations = {}
        self.session_metadata = {}

    def start_session(self, session_number, indicators):
        """Initialize a new work session"""
        conv_id = mcp_start_conversation()

        self.conversations[session_number] = {
            'conversation_id': conv_id,
            'indicators': indicators,
            'status': 'in_progress',
            'created_at': datetime.now(),
            'qa_pairs_generated': 0
        }

        return conv_id

    def end_session(self, session_number):
        """Finalize and archive session"""
        conv_id = self.conversations[session_number]['conversation_id']
        mcp_clear_conversation(conv_id)
        self.conversations[session_number]['status'] = 'completed'
```

### 2. Content Generator

**Purpose:** Generate Q&A content via MCP

**Specifications:**

```python
class ContentGenerator:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.retry_limit = 3
        self.batch_size = 2  # Questions per request (optimal)

    def generate_indicator_qa(self, session_num, indicator_name):
        """Generate all 6 Q&A pairs for an indicator"""

        conv_id = self.session_manager.conversations[session_num]['conversation_id']

        questions = [
            f"What is {indicator_name} and how is it measured/calculated?",
            f"How is {indicator_name} specifically used in cryptocurrency trading?",
            f"What are the optimal settings/thresholds for {indicator_name} in crypto markets?",
            f"What trading strategies work best with {indicator_name} in crypto?",
            f"How can {indicator_name} be combined with other indicators?",
            f"What are common mistakes when using {indicator_name} in crypto markets?"
        ]

        qa_pairs = []

        # Generate in batches of 2 to avoid token limits
        for i in range(0, 6, self.batch_size):
            batch = questions[i:i+self.batch_size]

            prompt = self._build_prompt(indicator_name, batch)

            response = self._call_with_retry(
                conversation_id=conv_id,
                prompt=prompt
            )

            # Parse and validate response
            parsed_qa = self._parse_response(response, indicator_name, batch)
            qa_pairs.extend(parsed_qa)

        return qa_pairs

    def _call_with_retry(self, conversation_id, prompt, attempt=0):
        """Call MCP with exponential backoff retry"""
        try:
            return mcp_gemini_chat(
                message=prompt,
                conversationId=conversation_id,
                model="gemini-2.5-pro",
                maxTokens=15000
            )
        except Exception as e:
            if attempt < self.retry_limit:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                return self._call_with_retry(conversation_id, prompt, attempt + 1)
            else:
                raise Exception(f"MCP call failed after {self.retry_limit} retries: {e}")
```

### 3. Quality Control Module

**Purpose:** Validate and score generated content

**Validation Criteria:**

```python
class QualityController:
    def __init__(self):
        self.min_word_count = 1000
        self.max_word_count = 2000
        self.required_keywords = {
            'calculation': ['calculated', 'formula', 'computation'],
            'trading': ['strategy', 'trading', 'position'],
            'context': ['2024', '2025', 'ETF', 'institutional'],
            'layer2': ['Layer 2', 'L2', 'Arbitrum', 'Optimism'],
        }

    def validate_qa_pair(self, qa_pair):
        """Validate a single Q&A pair"""
        issues = []
        score = 100

        # Check answer length
        word_count = len(qa_pair['answer'].split())
        if word_count < self.min_word_count:
            issues.append(f"Answer too short: {word_count} words (min {self.min_word_count})")
            score -= 20
        elif word_count > self.max_word_count:
            issues.append(f"Answer too long: {word_count} words (max {self.max_word_count})")
            score -= 5

        # Check for required context based on question type
        if "measured" in qa_pair['question'] or "calculated" in qa_pair['question']:
            if not any(kw in qa_pair['answer'].lower() for kw in self.required_keywords['calculation']):
                issues.append("Missing calculation/formula details")
                score -= 15

        # Check for 2024-2025 context
        if not any(kw in qa_pair['answer'] for kw in self.required_keywords['context']):
            issues.append("Missing 2024-2025 market context")
            score -= 10

        # Check for Layer 2 considerations (for on-chain metrics)
        if "transaction" in qa_pair['indicator'].lower():
            if not any(kw in qa_pair['answer'] for kw in self.required_keywords['layer2']):
                issues.append("Missing Layer 2 scaling considerations")
                score -= 10

        return {
            'valid': score >= 70,
            'score': score,
            'issues': issues,
            'word_count': word_count
        }

    def validate_session(self, qa_pairs):
        """Validate entire session of Q&A pairs"""
        results = []
        for qa in qa_pairs:
            result = self.validate_qa_pair(qa)
            result['indicator'] = qa['indicator']
            result['question'] = qa['question'][:100] + "..."
            results.append(result)

        avg_score = sum(r['score'] for r in results) / len(results)
        pass_rate = sum(1 for r in results if r['valid']) / len(results) * 100

        return {
            'average_score': avg_score,
            'pass_rate': pass_rate,
            'results': results,
            'approved': avg_score >= 80 and pass_rate >= 90
        }
```

### 4. Database Importer

**Purpose:** Structure and import validated content

```python
class DatabaseImporter:
    def __init__(self, db_path):
        self.db_path = db_path

    def import_session(self, session_num, qa_pairs, metadata):
        """Import validated Q&A pairs to database"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check for existing session
            cursor.execute(
                'SELECT COUNT(*) FROM sessions WHERE session_number = ?',
                (session_num,)
            )
            if cursor.fetchone()[0] > 0:
                raise Exception(f"Session {session_num} already exists")

            # Insert session
            cursor.execute('''
                INSERT INTO sessions (session_number, session_date, category, subcategory)
                VALUES (?, ?, ?, ?)
            ''', (session_num, metadata['date'], metadata['category'], metadata['subcategory']))

            # Group Q&A pairs by indicator
            indicators_data = {}
            for qa in qa_pairs:
                ind = qa['indicator']
                if ind not in indicators_data:
                    indicators_data[ind] = []
                indicators_data[ind].append(qa)

            # Insert indicators and Q&A pairs
            for indicator_name, qa_list in indicators_data.items():
                cursor.execute('''
                    INSERT INTO indicators (session_number, indicator_name, category, subcategory)
                    VALUES (?, ?, ?, ?)
                ''', (session_num, indicator_name, metadata['category'], metadata['subcategory']))

                indicator_id = cursor.lastrowid

                for order, qa in enumerate(qa_list, 1):
                    cursor.execute('''
                        INSERT INTO qa_pairs (indicator_id, question, answer, question_order)
                        VALUES (?, ?, ?, ?)
                    ''', (indicator_id, qa['question'], qa['answer'], order))

            conn.commit()

            return {
                'success': True,
                'session': session_num,
                'indicators': len(indicators_data),
                'qa_pairs': len(qa_pairs)
            }

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
```

---

## Workflow Protocols

### Protocol A: Full MCP Session (Optimal for Speed)

**Use Case:** When speed is priority and content can be iteratively refined

```
STEP 1: Initialize
─────────────────
Orchestrator:
  ├─ start_conversation() → conv_id
  ├─ Set context (project requirements, quality standards)
  └─ Prepare indicator list

STEP 2: Generate Content
─────────────────────────
For each indicator:
  ├─ Generate 6 Q&A pairs (in 3 batches of 2)
  ├─ Parse responses
  ├─ Validate quality in real-time
  └─ If quality < threshold:
      ├─ Request refinement
      └─ Re-validate

STEP 3: Compile & Structure
────────────────────────────
Orchestrator:
  ├─ Combine all Q&A pairs
  ├─ Structure into session format
  └─ Final validation check

STEP 4: Import
───────────────
  ├─ Import to database
  ├─ Verify integrity
  └─ Generate completion report

STEP 5: Cleanup
────────────────
  ├─ Clear conversation (optional)
  └─ Archive metadata
```

**Timeline:** 2-4 hours for 5 indicators (30 Q&A pairs)

### Protocol B: Hybrid MCP + File Review

**Use Case:** When quality review is critical, combines MCP speed with file-based audit

```
STEP 1-2: Same as Protocol A (MCP generation)

STEP 3: Export to File
──────────────────────
Orchestrator:
  ├─ Write generated content to review file
  └─ {Agent}/Review/session-{N}-generated.json

STEP 4: Human/Agent Review (Optional)
──────────────────────────────────────
  ├─ Review file for quality
  ├─ Note any issues
  └─ Approve or request revisions

STEP 5: Revise if Needed
─────────────────────────
If issues found:
  ├─ Send refinement request to MCP
  └─ Update review file

STEP 6: Import & Complete
───────────────────────────
  └─ Same as Protocol A
```

**Timeline:** 3-6 hours (includes review time)

### Protocol C: MCP-Assisted Manual

**Use Case:** Complex sessions requiring significant human oversight

```
STEP 1: Generate Drafts via MCP
────────────────────────────────
  ├─ Use MCP for initial drafts
  └─ Export to working files

STEP 2: Manual Refinement
──────────────────────────
Human:
  ├─ Edit for accuracy
  ├─ Adjust formatting
  └─ Enhance depth where needed

STEP 3: Final Assembly
───────────────────────
  ├─ Compile refined content
  └─ Import to database
```

**Timeline:** 6-10 hours (significant manual work)

---

## Error Handling & Recovery

### Error Types & Responses

**1. MCP API Errors (500, 503)**
```python
Error: Internal Server Error
Action:
  ├─ Retry with exponential backoff (2^n seconds)
  ├─ Max retries: 3
  ├─ If all fail → Fallback to manual generation
  └─ Log error for pattern analysis
```

**2. Token Limit Exceeded**
```python
Error: MAX_TOKENS reached, response truncated
Action:
  ├─ Detect truncation (incomplete sentence)
  ├─ Send continuation request: "Please complete the previous answer"
  ├─ Append response
  └─ Validate completion
```

**3. Quality Validation Failure**
```python
Error: Generated content below quality threshold
Action:
  ├─ Identify specific issues (length, missing keywords, etc.)
  ├─ Send refinement request with specific feedback
  ├─ Example: "Please expand the section on Layer 2 scaling (currently missing)"
  └─ Re-validate
```

**4. Structured Data Mismatch**
```python
Error: Response doesn't match expected JSON schema
Action:
  ├─ Extract content using regex/parsing
  ├─ Restructure programmatically
  ├─ Don't rely on exact schema from MCP
  └─ Use Python to enforce structure
```

### Recovery Strategies

**Graceful Degradation:**
```
Level 1: Full MCP automation → Fast, optimal
    ↓ (if errors)
Level 2: MCP + Manual post-processing → Moderate speed
    ↓ (if persistent errors)
Level 3: MCP drafts + Manual refinement → Slower but reliable
    ↓ (if MCP unavailable)
Level 4: Full manual generation → Slowest, guaranteed success
```

---

## Implementation Roadmap

### Phase 1: Proof of Concept (1 Session)
**Goal:** Test MCP protocol on Session 12

```
Tasks:
├─ Implement basic SessionManager
├─ Implement ContentGenerator with retry logic
├─ Test full workflow on 1 session (5 indicators)
├─ Measure: speed, quality, error rate
└─ Compare to inbox/outbox baseline

Success Criteria:
├─ Generate 30 Q&A pairs in < 4 hours
├─ Quality score ≥ 85%
├─ < 3 errors requiring manual intervention
└─ Successfully import to database
```

### Phase 2: Refinement (3 Sessions)
**Goal:** Optimize based on POC learnings

```
Tasks:
├─ Enhance error handling based on observed patterns
├─ Optimize batch sizes for efficiency
├─ Improve quality validation algorithms
├─ Add automated retries for common issues
└─ Test on Sessions 13-15

Success Criteria:
├─ Reduce error rate by 50%
├─ Improve average quality score to ≥ 90%
├─ Reduce generation time to < 3 hours
└─ Achieve 95% automation rate
```

### Phase 3: Production (Ongoing)
**Goal:** Make MCP the primary protocol

```
Tasks:
├─ Implement full monitoring & logging
├─ Create dashboard for session tracking
├─ Build automated quality reports
├─ Establish SLAs (speed, quality, reliability)
└─ Document best practices

Success Criteria:
├─ 10 consecutive successful sessions
├─ < 2 hour average generation time
├─ 98% pass rate on first attempt
└─ Team confidence in protocol
```

---

## Monitoring & Metrics

### Key Performance Indicators

**Speed Metrics:**
```
- Time per Q&A pair (target: < 10 minutes)
- Time per indicator (target: < 1 hour)
- Time per session (target: < 4 hours)
- Time savings vs manual (target: > 80%)
```

**Quality Metrics:**
```
- Average quality score (target: ≥ 85%)
- First-attempt pass rate (target: ≥ 90%)
- Refinement requests per session (target: < 3)
- Database integrity (target: 100%)
```

**Reliability Metrics:**
```
- MCP API uptime (measure)
- Error rate per session (target: < 5%)
- Retry success rate (target: ≥ 80%)
- Fallback invocations (target: < 10%)
```

**Cost Metrics:**
```
- Token usage per session (measure)
- Cost per Q&A pair (current: ~$0.04)
- Cost per session (current: ~$1.20)
- ROI vs manual time (current: ~950x)
```

### Monitoring Dashboard

```
┌────────────────────────────────────────────────────────┐
│         MCP Protocol Performance Dashboard              │
├────────────────────────────────────────────────────────┤
│                                                          │
│  Current Session: 12                                    │
│  Status: In Progress (Indicator 3 of 5)                 │
│                                                          │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │ Speed        │ Quality      │ Reliability  │        │
│  ├──────────────┼──────────────┼──────────────┤        │
│  │ 8 min/QA     │ Score: 87%   │ Uptime: 98%  │        │
│  │ ✅ On target │ ✅ Good       │ ✅ Excellent │        │
│  └──────────────┴──────────────┴──────────────┘        │
│                                                          │
│  Recent Sessions:                                       │
│  ├─ Session 12: In Progress                             │
│  ├─ Session 11: ✅ Complete (92% quality)               │
│  └─ Session 10: ⚠️ Partial (see notes)                 │
│                                                          │
│  Error Log (Last 24h):                                  │
│  ├─ 500 Error: 1 occurrence (recovered via retry)       │
│  └─ Token limit: 2 occurrences (handled via continuation│
│                                                          │
└────────────────────────────────────────────────────────┘
```

---

## Decision Matrix: When to Use Which Protocol

### Use MCP Protocol When:

✅ **Speed is priority**
- Need results quickly (< 4 hours)
- Tight deadlines

✅ **Content generation focused**
- Primary task is writing/analysis
- Structure is standardized

✅ **Iterative refinement acceptable**
- Can tolerate 2-3 revision cycles
- Quality through iteration OK

✅ **Standard indicators**
- Well-defined indicator types
- Established Q&A pattern

### Use Inbox/Outbox When:

✅ **Audit trail critical**
- Need permanent file records
- Compliance/documentation requirements

✅ **Async work required**
- Agents work on different schedules
- Multi-day workflows

✅ **Complex/novel indicators**
- Requires deep research
- Unusual indicator types

✅ **Multiple human reviewers**
- Need collaborative review
- File-based comments needed

### Use Hybrid Approach When:

✅ **Balance speed & oversight**
- Want MCP speed but with review checkpoints
- Best of both worlds

✅ **Training/learning**
- Learning new indicator types
- Building quality baselines

✅ **High-stakes sessions**
- Critical milestones
- Extra quality assurance needed

---

## Comparison Summary

| Aspect | Inbox/Outbox | MCP Protocol | Hybrid |
|--------|--------------|--------------|---------|
| **Speed** | Slow (async) | Fast (real-time) | Moderate |
| **Quality** | High (manual review) | High (automated + refinement) | Highest (both) |
| **Audit Trail** | Excellent (files) | Limited (logs) | Good (files + logs) |
| **Cost** | Low (no API) | Very Low (API pennies) | Low |
| **Scalability** | Limited | Excellent | Good |
| **Transparency** | High | Medium | High |
| **Reliability** | Very High | Good (99%+) | Very High |
| **Learning Curve** | Low | Medium | Medium |
| **Automation** | Low | Very High | High |
| **Best For** | Established workflows | Speed + scale | Critical sessions |

---

## Recommendations

### For This Project (Crypto Indicators)

**Primary Protocol:** **MCP (Protocol A)**
**Reason:**
- 177 indicators remaining
- Standardized Q&A format
- Speed is valuable
- Quality validation can be automated

**Fallback:** **Hybrid (Protocol B)** for milestone sessions (every 25 indicators)
**Reason:**
- Provides quality checkpoints
- Maintains file audit trail
- Builds confidence in MCP approach

### Implementation Plan

**Immediate (Next Session):**
1. Implement Protocol A for Session 12
2. Measure all KPIs
3. Document learnings
4. Refine based on results

**Short-term (Sessions 12-15):**
1. Optimize based on Session 12 data
2. Build monitoring dashboard
3. Establish quality baselines
4. Create runbooks for common issues

**Long-term (Sessions 16+):**
1. Full MCP adoption for standard sessions
2. Hybrid for milestones (50, 75, 100, 125 indicators)
3. Continuous refinement
4. Scale to other projects

---

## Approval & Next Steps

**Status:** PROPOSED - Awaiting User Decision

**Questions for User:**
1. Approve MCP as primary protocol for Session 12+?
2. Prefer full MCP (Protocol A) or Hybrid (Protocol B) to start?
3. Any specific quality concerns to address?
4. Acceptable timeline for Phase 1 POC?

**If Approved:**
- [ ] Implement SessionManager
- [ ] Implement ContentGenerator
- [ ] Implement QualityController
- [ ] Test on Session 12
- [ ] Measure & report results
- [ ] Refine for Sessions 13+

**If Modified:**
- [ ] Adjust protocol based on feedback
- [ ] Re-submit for approval

**If Rejected:**
- [ ] Continue with Inbox/Outbox
- [ ] Use MCP as supplement only

---

**Document Prepared By:** Claude Code
**Date:** 2025-11-01
**Version:** 1.0
**Status:** Awaiting Approval

---

