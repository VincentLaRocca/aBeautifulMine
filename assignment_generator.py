#!/usr/bin/env python3
"""
Assignment Generator Agent
Created: 2025-11-02
Purpose: Auto-generate all session assignments from master indicator list

Process:
1. Parse crypto-technical-indicators.txt
2. Group indicators into sessions (5 per session)
3. Generate detailed .md assignment files for each session
4. Place in assignments/ directory for Droid
"""

import os
from datetime import datetime

INDICATORS_FILE = "crypto-technical-indicators.txt"
ASSIGNMENTS_DIR = "assignments"
INDICATORS_PER_SESSION = 5

# Assignment template
ASSIGNMENT_TEMPLATE = """# Session {session_num} Assignment - {category_name}

**Date:** {date}
**Assigned to:** Droid
**Session:** {session_num} of ~46
**Status:** READY TO START

---

## 🎯 Mission

Generate comprehensive Q&A datasets for {category_name} using **ultra_deep_research** methodology.

---

## 📊 Session {session_num} Indicators

**Category:** {main_category}
**Subcategory:** {subcategory}

### The {count} Indicators:

{indicator_list}

---

## 🔬 Methodology

**Use your proven ultra_deep_research system:**

- 100 diverse search queries per indicator
- Concurrent API execution via OpenRouter
- AI-powered synthesis with advanced reasoning
- Question-answer pairs extraction
- JSON output with metadata

**Expected Output per Indicator:**
- ~76-100 Q&A pairs
- Success rate: 76-100%
- Total session output: ~380-500 Q&A pairs

---

## 📁 Deliverable Format

For each indicator, create a JSON file:

```
{file_list}
```

### Required JSON Structure:

```json
{{
  "research_topic": "CRYPTO INDICATOR [Indicator Name]",
  "total_pairs": 100,
  "session": {session_num},
  "indicator": "indicator_slug",
  "category": "{category_slug}",
  "research_method": "ultra_deep_research",
  "queries_executed": 100,
  "success_rate": "100.0%",
  "generation_date": "{date}",
  "source_database": "ultra_deep_research_db",
  "qa_pairs": [
    {{
      "pair_number": 1,
      "question": "your question here",
      "answer": "comprehensive answer here",
      "topic": "CRYPTO INDICATOR [Name]",
      "created_date": "{date} HH:MM:SS",
      "indicator": "indicator_slug",
      "category": "{category_slug}",
      "session": {session_num}
    }}
  ]
}}
```

---

## 🎯 Research Focus Areas

For each indicator, ensure ultra_deep_research covers:

### Core Understanding
- Mathematical formula and calculation
- Historical development and creator
- Theoretical basis and assumptions
- Default parameters and optimization

### Cryptocurrency Application
- Crypto-specific adaptations (24/7 markets, high volatility)
- Bitcoin, Ethereum, altcoin differences
- DeFi protocol integration
- NFT market applications
- Cross-chain considerations

### Trading Strategies
- Entry/exit signals
- Trend confirmation techniques
- Divergence patterns
- Multi-timeframe analysis
- Combination with other indicators
- Risk management

### Advanced Concepts
- Optimization for crypto markets
- Backtesting results (2020-2024)
- Common mistakes and pitfalls
- False signal filtering
- Market regime considerations

### Current Market Context (2024-2025)
- Post-halving dynamics (Bitcoin April 2024)
- ETF impact on volatility and trends
- Institutional vs retail usage patterns
- AI/algorithm trading effects
- Regulatory developments impact

---

## 📌 Indicator-Specific Guidance

{indicator_guidance}

---

## ✅ Quality Standards

**Each Answer Should Include:**
- 200-800 words (varies by question complexity)
- Clear, professional language
- Specific cryptocurrency examples
- Current data (2023-2024 examples)
- Actionable insights
- Credible sources

**Avoid:**
- Generic stock market advice
- Outdated pre-2020 examples
- Unverified claims
- Overly promotional language
- Missing cryptocurrency context

---

## 🚀 Execution Timeline

**Estimated: 3-5 hours total**

{time_estimates}

---

## 📤 Delivery Instructions

1. **Generate all {count} JSON files** using ultra_deep_research
2. **Place files in:** `inbox/droid/`
3. **Create completion report:** Brief markdown summary
4. **Notify:** Place "session-{session_num}-complete.txt" flag file

**That's it!** Import and refinement will be handled by orchestrator.

---

## 🎓 Context: Why These {count} Together?

{context_explanation}

---

## 📊 Progress Tracking

**Project Status After Session {session_num}:**
- Sessions Complete: {session_num}/{total_sessions}
- Indicators Complete: {total_indicators}/227 ({progress_pct}%)
- Q&A Pairs: ~{estimated_qa} total
- Categories: {categories_complete}

---

## 💡 Success Criteria

**Minimum (Approved):**
- {count} JSON files created
- ~300+ total Q&A pairs
- All indicators covered
- Valid JSON structure

**Target (Excellent):**
- {count} JSON files created
- ~380-450 total Q&A pairs
- 80%+ success rate per indicator
- Rich, detailed answers

**Outstanding (Exceptional):**
- {count} JSON files created
- ~450-500 total Q&A pairs
- 95%+ success rate per indicator
- Crypto-specific insights throughout

---

## 🔄 After Completion

**You'll receive:**
- Import confirmation
- Refinement results from Gemini
- Session {next_session} assignment (next {count} indicators)
- Progress update

**Session {next_session} Preview:** {next_preview}

---

## ❓ Questions?

If you encounter issues:
- API rate limits: adjust concurrent search limits
- Low success rates: refine query generation
- Quality concerns: add more specific crypto context
- Technical issues: check .env configuration

---

**Ready to execute, Droid!** 🚀

This is the production methodology that works. Session 1 achieved 100% success rate.

**Onwards to Session {session_num}!**

---

**Assignment Created:** {date}
**Orchestrator:** Claude (Assignment Generator Agent)
**Production Database:** crypto_indicators_production.db
**Method:** Ultra Deep Research v2.0
"""

def slugify(text):
    """Convert text to slug format"""
    return text.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('-', '_')

def parse_indicators():
    """Parse the master indicator list"""
    indicators = []

    with open(INDICATORS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[1:]:  # Skip header
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) >= 3:
            indicators.append({
                'category': parts[0],
                'subcategory': parts[1],
                'name': parts[2]
            })

    return indicators

def group_into_sessions(indicators):
    """Group indicators into sessions of 5"""
    sessions = []
    current_session = []

    for idx, indicator in enumerate(indicators, 1):
        current_session.append(indicator)

        if len(current_session) == INDICATORS_PER_SESSION:
            sessions.append(current_session)
            current_session = []

    # Add remaining indicators as final session
    if current_session:
        sessions.append(current_session)

    return sessions

def generate_indicator_guidance(indicators):
    """Generate specific guidance for each indicator"""
    guidance = []

    for idx, ind in enumerate(indicators, 1):
        slug = slugify(ind['name'])
        guidance.append(f"### {idx}. {ind['name']}")
        guidance.append(f"- Focus on: [Key characteristics and use cases]")
        guidance.append(f"- Cover: [Important parameters and settings]")
        guidance.append(f"- Highlight: [Crypto-specific applications]")
        guidance.append("")

    return "\n".join(guidance)

def generate_time_estimates(count):
    """Generate time estimates"""
    estimates = []
    time_per = 45 if count <= 3 else 50

    for i in range(1, count + 1):
        estimates.append(f"- Indicator {i}: ~{time_per} min")

    estimates.append("- Review & QA: ~30 min")
    return "\n".join(estimates)

def generate_assignment(session_num, indicators, total_sessions=46):
    """Generate assignment markdown for a session"""

    # Determine category info
    main_category = indicators[0]['category']
    subcategory = indicators[0]['subcategory']
    category_name = f"{subcategory}" if subcategory != main_category else main_category

    # Generate indicator list
    indicator_list = []
    file_list = []
    for idx, ind in enumerate(indicators, 1):
        indicator_list.append(f"{idx}. **{ind['name']}**")
        slug = slugify(ind['name'])
        file_list.append(f"{slug}_qa_pairs.json")

    indicator_list_str = "\n".join(indicator_list)
    file_list_str = "\n".join(file_list)

    # Calculate progress
    total_indicators = session_num * INDICATORS_PER_SESSION
    progress_pct = (total_indicators / 227) * 100
    estimated_qa = total_indicators * 76

    # Context explanation
    context = f"These {len(indicators)} indicators from {category_name} provide complementary analysis approaches for cryptocurrency markets."

    # Next session preview
    next_session = session_num + 1
    next_preview = "TBD - Next indicator set"

    # Categories complete
    categories_complete = "Derivatives, " + category_name if session_num > 1 else "Derivatives"

    # Generate the assignment
    assignment = ASSIGNMENT_TEMPLATE.format(
        session_num=session_num,
        category_name=category_name,
        date=datetime.now().strftime("%Y-%m-%d"),
        main_category=main_category,
        subcategory=subcategory,
        count=len(indicators),
        indicator_list=indicator_list_str,
        file_list=file_list_str,
        category_slug=slugify(category_name),
        indicator_guidance=generate_indicator_guidance(indicators),
        time_estimates=generate_time_estimates(len(indicators)),
        context_explanation=context,
        total_sessions=total_sessions,
        total_indicators=total_indicators,
        progress_pct=f"{progress_pct:.1f}",
        estimated_qa=estimated_qa,
        categories_complete=categories_complete,
        next_session=next_session,
        next_preview=next_preview
    )

    return assignment

def generate_all_assignments():
    """Generate all session assignments"""

    print("=" * 70)
    print("ASSIGNMENT GENERATOR AGENT")
    print("=" * 70)

    # Create assignments directory
    os.makedirs(ASSIGNMENTS_DIR, exist_ok=True)

    # Parse indicators
    print(f"\n[*] Parsing {INDICATORS_FILE}...")
    indicators = parse_indicators()
    print(f"[*] Found {len(indicators)} indicators")

    # Group into sessions
    print(f"[*] Grouping into sessions ({INDICATORS_PER_SESSION} per session)...")
    sessions = group_into_sessions(indicators)
    print(f"[*] Created {len(sessions)} sessions")

    # Generate assignments
    print(f"\n[*] Generating assignment files...")
    for idx, session_indicators in enumerate(sessions, 1):
        # Skip session 1 (already done)
        if idx == 1:
            print(f"    Session {idx}: SKIPPED (already complete)")
            continue

        assignment = generate_assignment(idx, session_indicators, len(sessions))

        filename = f"{ASSIGNMENTS_DIR}/session-{idx:02d}-assignment.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(assignment)

        print(f"    Session {idx:02d}: {filename}")
        print(f"               Category: {session_indicators[0]['subcategory']}")
        print(f"               Indicators: {len(session_indicators)}")

    # Generate summary
    print("\n" + "=" * 70)
    print("ASSIGNMENT GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nGenerated: {len(sessions) - 1} assignment files")
    print(f"Directory: {ASSIGNMENTS_DIR}/")
    print(f"\nSessions 2-{len(sessions)} are ready for Droid!")
    print("\nNext steps:")
    print("  1. Copy assignment to inbox/droid/ as needed")
    print("  2. Droid executes session")
    print("  3. Gemini refines output")
    print("  4. Import to database")
    print("=" * 70)

if __name__ == "__main__":
    generate_all_assignments()
