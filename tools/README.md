# Universal Tools Documentation

**aBeautifulMine Framework - Universal Knowledge Base Generation Tools**

These tools enable you to deploy the exponential knowledge base generation system to **ANY domain** - crypto indicators, web development, databases, AI agents, or any structured knowledge area.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Tool Reference](#tool-reference)
4. [Workflow Examples](#workflow-examples)
5. [Configuration Guide](#configuration-guide)

---

## Overview

### The Four Core Tools

```
1. generate_assignments.py     → Create research assignments from domain config
2. parse_domain_research.py   → Parse Droid's research reports into JSON
3. extract_domain_rag.py      → Extract from Droid's RAG database (2.5x faster!)
4. import_domain_batch.py     → Import Q&A pairs into production database
```

### Universal Design

All tools are **domain-agnostic**:
- Work with any knowledge domain
- Use configuration-driven behavior
- Support batch operations
- Generate structured JSON output
- Import to universal database schema

---

## Quick Start

### Deploy a New Domain in 5 Steps

**Example: Web Development Knowledge Base**

```bash
# Step 1: Generate assignments from config
python tools/generate_assignments.py config/web_development_config.json

# Step 2: Give assignments to Droid (manual step)
# → Droid conducts ultra deep research
# → Generates research_report_*.txt files

# Step 3: Parse research reports
python tools/parse_domain_research.py --batch inbox/droid/web_development web_development

# Step 4: (Optional) Extract from RAG database if available
python tools/extract_domain_rag.py --extract \
  qa_pairs_rag_export_20251102.json \
  config/web_dev_topics.json \
  web_development

# Step 5: Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/web_development \
  domains/web_development/web_dev_knowledge.db \
  "Web Development" \
  web_development
```

**Result:** Fully populated knowledge base ready for RAG deployment!

---

## Tool Reference

### 1. generate_assignments.py

**Purpose:** Creates research assignments for Droid from domain configuration

**Usage:**

```bash
# Generate all assignments for a domain
python tools/generate_assignments.py config/web_development_config.json

# Generate with custom output directory
python tools/generate_assignments.py config/ai_agents_config.json inbox/droid/ai_agents

# Show summary without generating
python tools/generate_assignments.py --summary config/database_design_config.json
```

**Input:** Domain configuration JSON (see [Configuration Guide](#configuration-guide))

**Output:**
- Session assignment files: `SESSION_N_DOMAIN.md`
- Structured markdown with topics, focus areas, example questions

**Example Output:**
```
inbox/droid/web_development/
├── SESSION_1_WEB_DEVELOPMENT.md  (5 topics, 500 Q&A target)
├── SESSION_2_WEB_DEVELOPMENT.md  (5 topics, 500 Q&A target)
└── ...
```

---

### 2. parse_domain_research.py

**Purpose:** Parse research reports into structured JSON

**Usage:**

```bash
# Parse single file
python tools/parse_domain_research.py \
  inbox/droid/research_report_react_hooks_20251102.txt \
  web_development

# Parse entire batch
python tools/parse_domain_research.py --batch \
  inbox/droid \
  web_development
```

**Input:**
- `research_report_*.txt` files from Droid
- Domain identifier (e.g., "web_development")

**Output:**
```json
{
  "domain": "web_development",
  "topic": "React Hooks",
  "topic_slug": "react_hooks",
  "total_pairs_reported": 105,
  "pairs_extracted": 103,
  "extraction_quality": "excellent",
  "qa_pairs": [
    {
      "pair_number": 1,
      "question": "What is useState in React?",
      "answer": "useState is a Hook that lets you add state to functional components...",
      "topic": "React Hooks"
    },
    ...
  ]
}
```

**Saved to:** `parsed_qa_data/{domain}/{topic_slug}_qa_pairs.json`

**Features:**
- ANSI code stripping
- Quality validation
- Extraction metrics
- Batch processing

---

### 3. extract_domain_rag.py

**Purpose:** Extract topics from Droid's RAG database (2.5x faster than new generation!)

**Usage:**

```bash
# Analyze what's available
python tools/extract_domain_rag.py --analyze qa_pairs_rag_export_20251102.json

# Find multi-session aggregations
python tools/extract_domain_rag.py --multi qa_pairs_rag_export_20251102.json

# Extract specific topics
python tools/extract_domain_rag.py --extract \
  qa_pairs_rag_export_20251102.json \
  config/web_dev_topics.json \
  web_development
```

**Topics Configuration Format:**
```json
[
  {
    "name": "React Hooks",
    "rag_topics": ["react hooks", "useState", "useEffect"],
    "description": "React Hooks patterns and usage"
  },
  {
    "name": "CSS Grid",
    "rag_topics": ["css grid", "grid layout"],
    "description": "CSS Grid system"
  }
]
```

**Output:** Same JSON format as parse_domain_research.py

**Benefits:**
- 2.5x faster than new generation
- Multi-session aggregation (e.g., 3 sessions → 300 Q&A)
- Zero generation cost
- Leverages existing research

**Example Multi-Session Aggregation:**
```
Topic: Simple Moving Average
Sessions: 3 sessions found
  - Technical Indicators - SMA (2024-10-15): 102 Q&A
  - Moving Averages Deep Dive (2024-10-28): 98 Q&A
  - SMA Advanced Patterns (2024-11-01): 100 Q&A
Total: 300 Q&A pairs (3x the depth!)
```

---

### 4. import_domain_batch.py

**Purpose:** Import parsed Q&A data into universal database

**Usage:**

```bash
# Import single file
python tools/import_domain_batch.py \
  parsed_qa_data/web_development/react_hooks_qa_pairs.json \
  domains/web_development/web_dev_knowledge.db \
  "Web Development" \
  web_development \
  2

# Import entire batch
python tools/import_domain_batch.py --batch \
  parsed_qa_data/web_development \
  domains/web_development/web_dev_knowledge.db \
  "Web Development" \
  web_development
```

**Database Schema:**

```sql
domains (
  domain_id, domain_name, domain_slug, description,
  created_date, updated_date
)

sessions (
  session_id, domain_id, session_number, category, subcategory,
  status, total_topics, total_qa_pairs, created_date, updated_date
)

topics (
  topic_id, domain_id, session_number, topic_name, topic_slug,
  description, total_qa_pairs, source_sessions, created_date, updated_date
)

qa_pairs (
  qa_id, topic_id, pair_number, question, answer, topic_tag,
  source_file, created_date
)
```

**Features:**
- Automatic database creation
- Multi-session aggregation tracking
- Duplicate detection
- Session statistics updating

---

## Workflow Examples

### Example 1: Crypto Indicators (Original Domain)

```bash
# Generate assignments
python tools/generate_assignments.py config/crypto_indicators_config.json

# → Droid generates research reports

# Parse reports
python tools/parse_domain_research.py --batch inbox/droid crypto_indicators

# Extract from RAG
python tools/extract_domain_rag.py --extract \
  qa_pairs_rag_export_20251102.json \
  config/crypto_indicators_topics.json \
  crypto_indicators

# Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/crypto_indicators \
  crypto_indicators_production.db \
  "Crypto Indicators" \
  crypto_indicators
```

**Result:** 227 indicators, ~22,700 Q&A pairs

---

### Example 2: Web Development (New Domain)

```bash
# Generate assignments
python tools/generate_assignments.py config/web_development_config.json

# → Droid generates research for 50 web dev topics

# Parse reports
python tools/parse_domain_research.py --batch \
  inbox/droid/web_development \
  web_development

# Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/web_development \
  domains/web_development/web_dev_knowledge.db \
  "Web Development" \
  web_development
```

**Result:** 50 topics, ~5,000 Q&A pairs

**Timeline:**
- Assignment generation: 5 minutes
- Droid research: 8-10 hours (overnight)
- Parsing: 10 minutes
- Import: 5 minutes
- **Total hands-on time: 20 minutes**

---

### Example 3: Database Design (New Domain)

```bash
# Generate assignments
python tools/generate_assignments.py config/database_design_config.json

# → Droid generates research for 40 database topics

# Parse reports
python tools/parse_domain_research.py --batch \
  inbox/droid/database_design \
  database_design

# Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/database_design \
  domains/database_design/database_knowledge.db \
  "Database Design" \
  database_design
```

**Result:** 40 topics, ~4,000 Q&A pairs

---

### Example 4: RAG-First Workflow

**If Droid already has research in RAG database:**

```bash
# Analyze what's available
python tools/extract_domain_rag.py --analyze qa_pairs_rag_export_20251102.json

# Find multi-session topics
python tools/extract_domain_rag.py --multi qa_pairs_rag_export_20251102.json

# Extract everything available
python tools/extract_domain_rag.py --extract \
  qa_pairs_rag_export_20251102.json \
  config/all_available_topics.json \
  crypto_indicators

# Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/crypto_indicators \
  crypto_indicators_production.db \
  "Crypto Indicators" \
  crypto_indicators

# Generate assignments ONLY for missing topics
python tools/generate_assignments.py config/remaining_topics_config.json
```

**Benefits:**
- Extract 60-70% from RAG (instant)
- Generate only 30-40% new (faster)
- Multi-session aggregation (higher quality)

---

## Configuration Guide

### Domain Configuration Structure

```json
{
  "domain": {
    "name": "Your Domain Name",
    "id": "domain_slug",
    "description": "Description of the domain",
    "target_qa_total": 5000
  },
  "sessions": [
    {
      "session_number": 1,
      "category": "Category Name",
      "subcategory": "Subcategory",
      "target_qa": 100,
      "topics": [
        {
          "name": "Topic Name",
          "description": "Topic description",
          "target_qa": 100,
          "focus_areas": [
            "Focus area 1",
            "Focus area 2"
          ],
          "example_questions": [
            "Example question 1?",
            "Example question 2?"
          ]
        }
      ]
    }
  ]
}
```

### Topic Configuration for RAG Extraction

```json
[
  {
    "name": "Display Name",
    "rag_topics": ["keyword1", "keyword2"],
    "description": "Optional description"
  }
]
```

**Example Configs Available:**
- `config/web_development_config.json` - 50 topics, 5,000 Q&A
- `config/database_design_config.json` - 40 topics, 4,000 Q&A
- `config/ai_agents_config.json` - 60 topics, 6,000 Q&A

---

## Performance Metrics

### Typical Performance

**New Generation:**
- Parsing: 0.5 sec/file
- Import: 0.1 sec/topic
- Total: ~20 minutes for 50 topics

**RAG Extraction:**
- Analysis: 2 sec
- Extraction: 5 sec/topic
- Import: 0.1 sec/topic
- Total: ~10 minutes for 15 topics
- **2.5x faster than generation!**

### Scaling

**Small Domain** (20-30 topics):
- Droid time: 3-5 hours
- Processing time: 10 minutes
- Total: ~5 hours

**Medium Domain** (40-60 topics):
- Droid time: 8-10 hours
- Processing time: 20 minutes
- Total: ~10 hours

**Large Domain** (100+ topics):
- Droid time: 15-20 hours
- Processing time: 30 minutes
- Total: ~20 hours

---

## Best Practices

### 1. Use RAG-First Approach

Always check RAG database before generating new content:
```bash
python tools/extract_domain_rag.py --analyze qa_pairs_rag_export.json
```

### 2. Batch Operations

Process in batches to minimize hands-on time:
```bash
# Generate all assignments at once
python tools/generate_assignments.py config/all_sessions.json

# Parse all reports at once
python tools/parse_domain_research.py --batch inbox/droid domain_name

# Import all data at once
python tools/import_domain_batch.py --batch parsed_qa_data/ database.db
```

### 3. Quality Validation

Check extraction quality after parsing:
```bash
# Look for "extraction_quality" in output
# excellent: 95%+
# good: 85-95%
# acceptable: 70-85%
# needs_review: <70%
```

### 4. Multi-Session Aggregation

Leverage multi-session research for better coverage:
```bash
python tools/extract_domain_rag.py --multi qa_pairs_rag_export.json
# Look for topics with 2-3 sessions → 200-300 Q&A!
```

### 5. Incremental Import

Import can be run multiple times safely:
- Existing topics: Updated with new Q&A
- New topics: Created fresh
- Session stats: Automatically recalculated

---

## Troubleshooting

### Common Issues

**Issue:** "No Q&A pairs found in research report"
```bash
# Check file for ANSI codes
cat research_report_*.txt | head -20

# Solution: Use parse_domain_research.py (ANSI-aware)
```

**Issue:** "Topic not found in RAG database"
```bash
# Analyze available topics
python tools/extract_domain_rag.py --analyze rag_export.json

# Update rag_topics keywords in config
```

**Issue:** "Database locked"
```bash
# Close any open database connections
# Retry import
```

**Issue:** "Low extraction quality"
```bash
# Check research report format
# Verify pair markers ("Pair 1:", "Question:", "Answer:")
# May need to adjust parser regex
```

---

## Next Steps

### For New Domains

1. Copy a config template: `config/web_development_config.json`
2. Customize for your domain
3. Run quick start workflow
4. Deploy to RAG system (see UNIVERSAL_FRAMEWORK.md)

### For Existing Crypto Domain

1. Check RAG first: `extract_domain_rag.py --analyze`
2. Extract available topics
3. Generate assignments for gaps
4. Import everything to database

### For Advanced Usage

- See `UNIVERSAL_FRAMEWORK.md` for complete methodology
- See `THE_SYNTHESIS_PRINCIPLE.md` for strategic insights
- See `SESSION_PROGRESSION_ANALYSIS.md` for growth patterns

---

**These tools turn 20 hours of manual work into 20 minutes.**

**The process has become the product.** 🚀

---

**Created:** 2025-11-02
**Part of:** aBeautifulMine Framework
**Status:** Production-ready
