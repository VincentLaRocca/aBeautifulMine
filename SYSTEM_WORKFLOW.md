# Multi-Agent Data Collection System Workflow

**Version:** 2.0
**Date:** 2025-11-02
**Project:** Cryptocurrency Indicators Training Dataset (22,700 Q&A pairs)

---

## System Overview

A multi-agent pipeline for generating institutional-grade cryptocurrency indicator knowledge base optimized for RAG retrieval with Mixtral 7B on RTX 5090.

### Agents & Roles

1. **Droid** - Raw data generation (speed over perfection)
2. **Claude** - Parsing, orchestration, quality control, gap analysis
3. **Gemini** - Batch refinement and enhancement
4. **Mixtral 7B RAG** - Final deployment target (<0.5 distance threshold)

---

## Phase 1: Assignment & Generation

### Claude's Role: Assignment Creation
- Generate detailed session assignments from master indicator list
- Stack assignments in `inbox/droid/`
- Create execution plan (MASTER_EXECUTION_PLAN.md)
- Define success criteria per session

### Droid's Role: Lightning-Fast Research
**Method:** Ultra Deep Research
- Execute 100 concurrent search queries per indicator
- Generate raw research reports (research_report_*.txt)
- ANSI color codes, unstructured format
- **Speed is priority** - gaps and misses are expected and acceptable
- Output: Raw .txt files with Q&A data embedded

**Expected Output Per Session:**
- 5 indicators (Session 44 has 1)
- ~380-500 Q&A pairs total
- 80-100% search success rate
- Raw research_report_*.txt files

**Droid's Known Behavior:**
- Fast but messy
- Inevitably misses questions
- Quality varies
- This is EXPECTED and part of the workflow

---

## Phase 2: Parsing & Gap Analysis

### Claude's Role: Parse Droid's Output

**Tool:** `parse_droid_research.py`

**Input:** Droid's raw research_report_*.txt files
- ANSI color codes
- Unstructured text format
- Embedded Q&A pairs

**Parsing Process:**
1. Read research_report_*.txt files from `inbox/droid/processed/`
2. Extract metadata (topic, date, queries executed, success rate)
3. Use regex to find Q&A pairs section
4. Extract individual Q&A pairs:
   - Clean questions (remove quotes, formatting)
   - Clean answers (strip ANSI codes, normalize whitespace)
   - Preserve crypto-specific context
5. Structure into JSON format
6. Validate data integrity

**Output:** Structured JSON files
```json
{
  "research_topic": "Indicator Name",
  "total_pairs": 89,
  "research_method": "ultra_deep_research",
  "queries_executed": 100,
  "success_rate": "89%",
  "generation_date": "2025-11-02",
  "qa_pairs": [
    {
      "pair_number": 1,
      "question": "What is...",
      "answer": "The indicator...",
      "topic": "Indicator Name",
      "created_date": "2025-11-02"
    }
  ]
}
```

### Gap Analysis

**Claude analyzes parsed data:**
1. **Completion Rate:** Did we get 80-100 Q&A per indicator?
2. **Quality Assessment:** Are answers crypto-specific and detailed?
3. **Coverage Gaps:** What topics/questions are missing?
4. **Success Rate:** What was Droid's search success rate?

**Gap Report Format:**
```markdown
Session X Gap Analysis:

Indicator 1: 89/100 Q&A (89%) - Missing questions on: [topics]
Indicator 2: 76/100 Q&A (76%) - Needs batch 2 assignment
Indicator 3: 100/100 Q&A (100%) - Complete ✓
Indicator 4: 92/100 Q&A (92%) - Minor gaps
Indicator 5: 85/100 Q&A (85%) - Missing questions on: [topics]

Total: 442/500 Q&A (88.4%)
Recommendation: Create Batch 2 assignment for Indicator 2
```

---

## Phase 3: Database Import

### Claude's Role: Import to Production

**Database:** `crypto_indicators_production.db`

**Schema:**
- `sessions` - Session metadata
- `indicators` - Indicator details
- `qa_pairs` - Question-answer pairs (supports 100+ per indicator)
- `research_metadata` - Research execution data

**Import Process:**
1. Validate parsed JSON structure
2. Insert session metadata
3. Insert indicators (with proper slugs)
4. Insert all Q&A pairs
5. Verify foreign key integrity
6. Run validation queries
7. Report cumulative totals

**Validation Checks:**
- No orphaned records
- All indicators have Q&A pairs
- Total counts match expectations
- Database integrity maintained

---

## Phase 4: RAG Export Extraction (NEW!)

**DISCOVERY:** Droid maintains an internal RAG database of all research!

### When to Use RAG Export Extraction

**Triggers:**
- Gap analysis shows missing indicators
- Before requesting new generation from Droid
- Periodic checks for newly added content

### Droid's RAG Export Format

**File:** `qa_pairs_rag_export_YYYYMMDD_HHMMSS.json`

**Structure:**
```json
{
  "metadata": {
    "export_timestamp": "2025-11-02T06:11:44",
    "total_sessions": 180,
    "total_qa_pairs": 17656
  },
  "sessions": [
    {
      "topic": "Indicator name cryptocurrency trading",
      "qa_pairs": [
        {
          "question": "...",
          "answer": "..."
        }
      ]
    }
  ]
}
```

### Claude's Extraction Process

**Tool:** `extract_rag_indicators.py`

**Steps:**
1. Load RAG export JSON file
2. Map desired indicators to RAG session topics
3. Search for matching sessions (fuzzy matching)
4. Extract Q&A pairs for each indicator
5. Combine multiple sessions if available (e.g., SMA had 3 sessions!)
6. Save as structured JSON (same format as parsed data)
7. Import to production database

**Benefits:**
- 2.5x faster than new generation
- Multi-session aggregation (more comprehensive coverage)
- No new Droid processing needed
- Leverages existing research

**Example Result:**
- Batch 3: Extracted 15 indicators with 2,083 Q&A in 40 minutes
- Some indicators had 200-300 Q&A from multiple sessions
- Zero generation cost, pure extraction

### Multi-Session Aggregation

Some indicators appear in multiple RAG sessions:
- **SMA:** 3 sessions → 300 Q&A total
- **WMA:** 3 sessions → 286 Q&A total
- **RSI:** 2 sessions → 200 Q&A total
- **MACD:** 2 sessions → 197 Q&A total

This provides **multiple perspectives** on the same indicator!

---

## Phase 5: Iterative Refinement (Batch 2+)

### When Batch 2 is Needed

**Triggers:**
- Indicator has <80 Q&A pairs (below acceptable threshold)
- Critical questions missing
- Low quality answers detected
- Success rate <60%
- **Indicator NOT found in RAG export**

### Priority Check: RAG Export First!

**NEW WORKFLOW:**
```
Gap Detected
    ↓
Check RAG Export
    ↓
┌───────────────────┐
│ Found in RAG?     │
└───────┬───────────┘
        │
    ┌───┴───┐
   YES      NO
    │        │
    ▼        ▼
Extract    Create
from RAG   Batch 2
Export     Assignment
    │        │
    └───┬────┘
        ▼
    Import to
    Database
```

### Claude Creates Batch 2 Assignment

**Format:**
```markdown
Session X - Batch 2 Assignment

Target Indicators:
- Indicator 2: Need 24 more Q&A (currently 76/100)
  - Focus on: [specific missing topics]
- Indicator 5: NOT FOUND in RAG export (need 100 Q&A)

Specific Questions to Research:
1. [Question Droid missed]
2. [Question Droid missed]
...

Expected Output: 124+ additional Q&A pairs
```

### Droid Executes Batch 2
- Targeted research on specific gaps
- Same ultra_deep_research methodology
- Focused queries on missing topics
- May add to RAG database for future extraction

### Claude Parses Batch 2
- Same parsing process (research_report_*.txt files)
- Merge with Batch 1 data
- Update database
- Re-analyze for Batch 3 if needed

**Iterate until session meets quality threshold**

---

## Phase 6: Batch Refinement with Gemini

**ONLY after all sessions are complete and iterated**

### Stage 1: Embeddings Generation
- Export all Q&A pairs to JSONL
- Upload to Gemini File API
- Create embeddings batch job
- Task type: RETRIEVAL_DOCUMENT
- Output: 1,536-dimensional vectors

**Duration:** ~24 hours
**Cost:** ~$30-40 (batch pricing 50% off)

### Stage 2: Semantic Deduplication
- Calculate cosine similarity between all Q&A pairs
- Identify duplicates (distance <0.3)
- Cluster similar questions
- Keep highest quality version
- Remove redundant pairs

**Duration:** ~4 hours
**Cost:** ~$10-20

### Stage 3: Quality Scoring
- 8-metric quality assessment:
  1. Answer completeness
  2. Crypto-specific context
  3. Technical accuracy
  4. Clarity and structure
  5. Practical examples
  6. 2024-2025 relevance
  7. Length appropriateness
  8. Question-answer alignment

**Quality Tiers:**
- Premium (90-100)
- Standard (70-89)
- Review (50-69)
- Low (<50)

**Duration:** ~24 hours
**Cost:** ~$50-70

### Stage 4: Gap Analysis (Cross-Dataset)
- Identify missing topics across ALL indicators
- Find under-represented concepts
- Detect coverage imbalances
- Generate recommendations

**Duration:** ~2 hours
**Cost:** ~$10-20

### Stage 5: Enhancement (Optional)
- Enhance Review/Low tier Q&A pairs
- Add missing context
- Improve clarity
- Add practical examples

**Duration:** ~24 hours
**Cost:** ~$50-80

**Total Refinement Cost:** ~$150-200
**Total Duration:** ~3-4 days (mostly automated)

---

## Phase 7: RAG System Deployment

### Final Output
- Refined dataset: ~17,000-22,000 Q&A pairs
- Quality distribution: 80%+ Premium/Standard tier
- Embeddings generated
- Optimized for semantic search

### Deployment to Mixtral 7B
- Load refined dataset
- Configure retrieval parameters
- Test distance threshold performance
- Validate <0.5 distance accuracy

---

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ CLAUDE: Generate Session Assignments (44 sessions)      │
│ Output: inbox/droid/session-XX-assignment.md            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ DROID: Execute Ultra Deep Research (Batch 1)            │
│ - 100 queries per indicator                             │
│ - Fast, messy output                                     │
│ - Stores in internal RAG database                       │
│ Output: research_report_*.txt files                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ CLAUDE: Parse Raw Research Reports                      │
│ Tool: parse_droid_research.py                           │
│ - Extract Q&A pairs                                      │
│ - Clean formatting                                       │
│ Output: Structured JSON                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ CLAUDE: Gap Analysis                                    │
│ - Count Q&A per indicator                               │
│ - Identify missing questions                            │
│ - Assess quality                                         │
│ Output: Gap report                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
                ┌────┴────┐
                │ Gaps?   │
                └────┬────┘
                     │
        ┌────────────┼────────────┐
        │ YES                     │ NO
        ▼                         ▼
┌───────────────────┐    ┌────────────────────┐
│ CLAUDE: Check     │    │ CLAUDE: Import to  │
│ Droid RAG Export  │    │ Production DB      │
└────────┬──────────┘    └────────┬───────────┘
         │                        │
    ┌────┴────┐                   │
    │ Found?  │                   │
    └────┬────┘                   │
         │                        │
    ┌────┴────┐                   │
   YES        NO                  │
    │          │                  │
    ▼          ▼                  │
┌────────┐ ┌────────────────┐    │
│Extract │ │CLAUDE: Create  │    │
│from RAG│ │Batch 2         │    │
│Export  │ │Assignment      │    │
└───┬────┘ └───────┬────────┘    │
    │              │              │
    │              ▼              │
    │       ┌──────────────┐      │
    │       │DROID: Execute│      │
    │       │Batch 2       │      │
    │       └──────┬───────┘      │
    │              │              │
    └──────────────┴──────────────┘
                   │
                   └────► (Loop back to Parse)
                   │
                   ▼
        ┌─────────────────────────┐
        │ All 44 Sessions         │
        │ Complete?               │
        └────────┬────────────────┘
                 │ YES
                 ▼
┌─────────────────────────────────────┐
│ GEMINI: Batch Refinement (5 Stages) │
│ - Embeddings                         │
│ - Deduplication                      │
│ - Quality Scoring                    │
│ - Gap Analysis                       │
│ - Enhancement                        │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ MIXTRAL 7B RAG: Deploy Dataset      │
│ - Test retrieval                     │
│ - Validate performance               │
└─────────────────────────────────────┘
```

---

## File Locations & Organization

### Claude's Working Directory
```
C:\Users\vlaro\dreamteam\claude\
├── crypto_indicators_production.db      # Production database
├── parse_droid_research_v2.py           # Parsing script (ANSI-aware)
├── extract_rag_indicators.py            # RAG export extraction tool
├── import_batch_*.py                    # Import scripts
├── SYSTEM_WORKFLOW.md                   # This document
├── SESSION_INDEX.md                     # Session status tracking
├── PROGRESS_UPDATE_*.md                 # Progress reports
├── gemini_refinement/                   # Gemini batch jobs
│   ├── session_X_embeddings_batch.jsonl
│   └── session_X_for_embeddings.json
├── inbox/droid/                         # Assignments for Droid
│   ├── MASTER_EXECUTION_PLAN.md
│   ├── SESSION_INDEX.md
│   ├── BATCH_X_*.md                     # Batch assignments
│   ├── session-XX-assignment.md
│   ├── research_report_*.txt            # Raw research from Droid
│   └── qa_pairs_rag_export_*.json       # RAG database exports
└── parsed_qa_data/                      # Parsed output
    └── indicator_slug_qa_pairs.json
```

### Droid's Working Directory
```
C:\Users\vlaro\dreamteam\Droid\
├── inbox/                               # Receives assignments
│   └── processed/                       # Raw research reports
│       ├── research_report_*.txt
│       └── crypto-indicators-session-XX-qa.json
├── outbox/                              # Completion signals
│   └── session-X-completion-report.md
├── research_qa.db                       # Internal RAG database (SQLite)
└── ultra_deep_research/
    └── research_reports/                # Archived research
        ├── compiled_research_*.json
        ├── archive_summary_*.txt
        └── qa_pairs_rag_export_*.json   # RAG exports for Claude
```

---

## Success Criteria

### Per Session (Minimum Acceptable)
- ✅ All 5 indicators researched (Session 44: 1 indicator)
- ✅ 60%+ success rate average
- ✅ 300+ total Q&A pairs
- ✅ Valid JSON structure
- ✅ Crypto-specific content

### Per Session (Target)
- 🎯 All 5 indicators researched
- 🎯 80%+ success rate average
- 🎯  380-500 total Q&A pairs
- 🎯 Rich, detailed answers
- 🎯 2024-2025 examples included

### Complete Project (Minimum)
- ✅ All 227 indicators covered
- ✅ 12,000+ Q&A pairs
- ✅ Database import successful
- ✅ Valid for RAG deployment

### Complete Project (Target)
- 🎯 All 227 indicators covered
- 🎯 17,000+ Q&A pairs
- 🎯 80%+ Premium/Standard quality tier
- 🎯 <0.5 distance retrieval performance

---

## Key Principles

1. **Speed Over Perfection (Batch 1)**
   Droid moves fast, gaps are expected and acceptable

2. **Quality Through Iteration**
   Multiple batches refine coverage, not single perfect pass

3. **Parse Everything**
   Claude transforms Droid's messy output into structured data

4. **Gap-Driven Assignments**
   Batch 2+ assignments target specific identified gaps

5. **Batch Refinement at End**
   Gemini processes complete dataset, not per-session

6. **Validate at Every Step**
   Database integrity, Q&A counts, quality checks

7. **Document Everything**
   Gap reports, import logs, completion summaries

---

## Troubleshooting

### Droid Output is Missing
**Problem:** Can't find research_report_*.txt files
**Solution:** Check `Droid/inbox/processed/` and `Droid/ultra_deep_research/research_reports/`

### Parsing Fails
**Problem:** Regex doesn't match Q&A pairs
**Solution:** Examine raw .txt file format, adjust regex pattern in parse_droid_research.py

### Low Q&A Count
**Problem:** Indicator has <60 Q&A pairs
**Solution:** Create Batch 2 assignment, don't re-run entire session

### Database Import Error
**Problem:** Foreign key constraint violation
**Solution:** Verify session exists before inserting indicators

### Gemini Batch Job Stuck
**Problem:** Batch job in PENDING for >2 hours
**Solution:** Check quota limits, verify file processing state

---

## Version History

**v3.0 (2025-11-02)** - MAJOR UPDATE
- **Added Phase 4:** RAG Export Extraction methodology
- **Discovery:** Droid's internal RAG database (17,656 Q&A pairs)
- **Multi-session aggregation:** Combine multiple research sessions per indicator
- **Updated workflow:** Check RAG export before requesting new generation
- **Performance metrics:** 2.5x faster via extraction vs new generation
- **Batch 3 results:** 15 indicators, 2,083 Q&A in 40 minutes
- **Updated diagram:** Includes RAG export check in gap workflow
- **File organization:** Added extract_rag_indicators.py and RAG export files
- **Current status:** 35 indicators, 4,072 Q&A pairs, 6 complete sessions

**v2.0 (2025-11-02)**
- Clarified iterative batch approach
- Defined Claude's parsing role
- Documented Droid's expected gaps
- Added gap analysis workflow
- Established quality thresholds

**v1.0 (2025-11-01)**
- Initial system design
- Database schema created
- Session assignments generated
- Batch processing framework

---

**Last Updated:** 2025-11-02 (v3.0 - After Batch 3 Breakthrough)
**Maintained By:** Claude (Orchestrator)
**Project Status:** Active - 6 Complete Sessions (1,2,4,5,6,8), 1 Partial (7), 1 Missing (3)
**Progress:** 35/227 indicators (15.4%), 4,072 Q&A pairs (17.9% of target)
