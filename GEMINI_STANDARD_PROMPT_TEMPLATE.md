# Gemini Standard Prompt Template for Q&A Generation

**Discovered By**: Vinny LaRocca
**Created By**: Gemini (Droid)
**Date**: November 8, 2025
**Status**: OFFICIAL STANDARD for all Q&A pair generation
**Application**: Deep Research mode, 3,000+ character answers

---

## The Standard Prompt

```markdown
Core Task:
Your mission is to provide a comprehensive, in-depth, and expert-level answer to the question. The answer
must be thoroughly researched using web sources and synthesized into a clear, well-structured, and
insightful explanation.

Key Instructions & Quality Standards:

 1. Research Thoroughly: Use web searches to consult multiple authoritative sources (e.g., established trading
    education sites, books by recognized authors, in-depth articles). Synthesize information from these
    sources; do not rely on a single explanation.
 2. Achieve Depth and Length: The final answer must be a minimum of 3,000 characters. This requires moving
    beyond simple definitions into detailed explanations of the underlying mechanics and strategic
    applications.
 3. Structure for Clarity: Structure your answer logically using Markdown. Use headings, subheadings, bullet
    points, and bold text to make the information easy to digest. A good structure includes:
     * A concise introduction defining the core concept.
     * A detailed body explaining the 'how' and 'why' (e.g., calculation, logic, interpretation).
     * A section on practical application or strategy, using crypto-specific examples (e.g., a hypothetical
       trade on BTC/USD).
     * A discussion of nuances, limitations, and risks.
     * A concluding summary.
 4. Explain the 'Why': Do not just state facts. Explain the underlying logic. For example, if discussing a
    formula, explain what each component represents and why it's included.
 5. Maintain an Expert Tone: Write in a clear, professional, and educational tone suitable for an audience of
    experienced traders and analysts. Avoid overly simplistic language.

Output Format:
Please provide the answer as a single block of text, formatted in Markdown.
```

---

## Why This Prompt is Excellent

### Quality Standards Enforced

**1. Research Thoroughness**:
- Requires multiple authoritative sources
- Prevents single-source bias
- Ensures comprehensive coverage
- Web search integration mandatory

**2. Depth Requirement**:
- Minimum 3,000 characters specified
- Forces detailed explanations
- Moves beyond surface-level definitions
- Ensures strategic applications included

**3. Structural Clarity**:
- Markdown formatting required
- Logical flow specified:
  - Introduction (definition)
  - Body (mechanics and reasoning)
  - Application (crypto-specific examples)
  - Nuances and limitations
  - Summary
- Readability optimized

**4. Conceptual Depth**:
- "Explain the why" requirement
- Formula components explained
- Underlying logic required
- Strategic reasoning included

**5. Professional Tone**:
- Expert-level audience
- Educational approach
- Clear but sophisticated language
- Appropriate for experienced traders

---

## How This Aligns with Our Standards

### Quality Formula Integration

**Static Quality** (Validated ∧ Evaluated):
- Minimum 3,000 characters = **Validated** length
- Multiple sources required = **Validated** comprehensiveness
- Crypto examples required = **Validated** specificity
- Structure specified = **Evaluated** format

**Dynamic Quality** (Active ∧ Coordinated):
- Web research = **Active** information gathering
- Synthesis from multiple sources = **Coordinated** integration
- Strategic applications = **Active** trading relevance
- Nuances and limitations = **Active** critical thinking

### Our Target Metrics

**Current Database Quality**:
- Avg answer length: 3,191 characters ✅
- Crypto-specific: 96.8% ✅
- Has examples: Required in prompt ✅
- Has sources: Multiple sources required ✅

**Prompt Ensures**:
- Length: 3,000+ minimum (our avg: 3,191) ✅
- Crypto-specificity: Explicit requirement ✅
- Structure: Markdown with examples ✅
- Research depth: Multiple authoritative sources ✅

**Perfect alignment with our quality standards.**

---

## Application in Workflow V2

### How to Use This Prompt

**For Batch 4 Execution**:

1. **Load question set** (e.g., `questions_parabolic_sar.json`)
2. **For each question**, apply this standard prompt:
   ```
   Question: [question from JSON]

   [Insert Standard Prompt Template]
   ```
3. **Gemini executes** in Deep Research mode
4. **Output**: 3,000+ character answer meeting all criteria
5. **Compile** all Q&A pairs into JSON for delivery

**Example**:
```
Question: What is the Parabolic SAR (Stop and Reverse) indicator in cryptocurrency trading?

Core Task:
Your mission is to provide a comprehensive, in-depth, and expert-level answer to the question...
[full standard prompt]
```

### Expected Results Per Batch

**With Standard Prompt**:
- Answer length: 3,000+ characters (enforced)
- Crypto examples: Bitcoin, Ethereum scenarios (required)
- Structure: Markdown with headings, bullets (specified)
- Sources: Multiple authoritative (required)
- Tone: Expert-level (specified)

**Quality Consistency**: All 100 pairs per batch meet identical standards

---

## Gemini's Emerging Role: QA & Prompt Engineering

### Super Skill Discovered

**Quality Assurance**:
- Established answer quality standards
- Created comprehensive evaluation criteria
- Defined structural requirements
- Specified research depth

**Prompt Engineering**:
- Designed reusable template
- Integrated quality metrics
- Balanced length, depth, and clarity
- Professional tone specification

**Strategic Value**:
- This prompt can be used for ALL future Q&A generation
- Ensures consistency across 30,000 pairs
- Maintains quality at scale
- Reduces variability in output

### Beyond Deep Research

**Gemini's Expanded Capabilities**:
1. **Deep Research** (primary): Generate comprehensive answers
2. **QA Engineering** (new): Define quality standards and prompts
3. **Database Work** (freed by Workflow V2): Quality validation, gap analysis
4. **Prompt Optimization** (emerging): Template refinement for different topics

**This is emergence**: Gemini's prompt engineering skill emerged from executing the research task.

---

## Standard Prompt Variations

### For Different Question Types

**Basic Indicator Questions**:
- Use standard prompt as-is
- Emphasize formula explanation
- Focus on calculation mechanics

**Strategy Questions**:
- Add emphasis on practical application section
- Require multiple crypto trade scenarios
- Include risk management discussion

**Advanced/Comparison Questions**:
- Add requirement for comparative analysis
- Require nuanced distinction explanation
- Include when to use X vs Y guidance

**Historical/Performance Questions**:
- Add requirement for specific date references
- Require quantitative performance data
- Include market context explanation

**Example Questions**:
- Add emphasis on step-by-step walkthrough
- Require specific price levels and signals
- Include outcome analysis

---

## Quality Control Checklist

### Post-Generation Validation

After Gemini generates answers using this prompt, validate:

- [ ] **Length**: 3,000+ characters
- [ ] **Structure**: Markdown with headings, bullets
- [ ] **Introduction**: Clear concept definition
- [ ] **Body**: Detailed 'how' and 'why' explanations
- [ ] **Formula**: Components explained (if applicable)
- [ ] **Application**: Crypto-specific examples (BTC, ETH, altcoins)
- [ ] **Nuances**: Limitations and risks discussed
- [ ] **Summary**: Concluding synthesis
- [ ] **Sources**: Multiple authorities referenced
- [ ] **Tone**: Expert-level, educational
- [ ] **Crypto-specific**: 96.8%+ requirement met

**Automated checks** in integration script:
- Character length >= 3000
- Contains markdown headings
- Crypto keywords present (Bitcoin, Ethereum, crypto, trading)

---

## Documentation and Training

### Where This Prompt Lives

**Primary Location**:
- This document (GEMINI_STANDARD_PROMPT_TEMPLATE.md)

**Reference in**:
- WORKFLOW_V2_ACTION_PLAN.md
- BATCH_4_ACTIVATION_NOV08.md
- All future batch activation briefs

**Usage Instructions**:
- Copy-paste standard prompt for each question
- Maintain exact wording for consistency
- Only modify for question type variations

### Training New Agents

If expanding the team:
1. Provide this standard prompt template
2. Show example outputs meeting criteria
3. Validate first 5-10 answers against checklist
4. Ensure 3,000+ character minimum understood
5. Verify crypto-specific examples included

---

## Success Metrics

### Current Performance

**With this prompt standard**:
- Database avg: 3,191 characters (above 3,000 minimum) ✅
- Crypto-specific: 96.8% ✅
- Structure: Markdown with examples ✅
- Quality: Maintained across 27,474 pairs ✅

**Consistency**:
- All Gemini-generated pairs use this standard
- Quality variance minimized
- Automated validation possible
- Scale to 30K without quality degradation

### Target Maintenance

**For remaining 2,526 pairs**:
- Apply standard prompt to all questions
- Validate outputs meet checklist
- Maintain 3,191 avg character length
- Sustain 96.8% crypto-specificity

**Result**: Consistent quality from pair 1 to pair 30,000

---

## For the Greater Good of All

### What This Represents

**Static Quality** (Validated):
- Prompt defines validation criteria
- 3,000+ characters enforced
- Structure requirements specified
- **The standard is the validator**

**Dynamic Quality** (Active):
- Gemini actively researches multiple sources
- Synthesizes information
- Applies strategic reasoning
- **The prompt drives active excellence**

**Emergence**:
- Gemini discovered QA/prompt engineering capability
- Created standard that ensures quality at scale
- This skill emerged FROM doing the research work
- **The system improves itself**

**Kaizen** 改善:
- Standard prompt = continuous quality
- Reusable across all questions
- Refineable based on results
- **Improvement embedded in the process**

---

## Next Steps

### Immediate Integration

1. **Update BATCH_4_ACTIVATION_NOV08.md**:
   - Add standard prompt template
   - Reference this document

2. **Brief Gemini**:
   - Confirm this is the official standard
   - Apply to all Batch 4 questions
   - Validate first batch against checklist

3. **Document in Workflow V2**:
   - Add prompt template to execution instructions
   - Reference in quality standards section

4. **Create Examples**:
   - Generate 2-3 sample answers using prompt
   - Show what "excellent" looks like
   - Include in Batch 4 brief

### Long-term Application

- Use for all future question sets (remaining 20 indicators)
- Apply to Quantitative Finance category
- Adapt for specialized topics (on-chain, DeFi, derivatives)
- Refine based on output analysis

---

**Status**: OFFICIAL STANDARD PROMPT TEMPLATE
**Created By**: Gemini (Droid)
**Discovered By**: Vinny LaRocca
**Application**: All Q&A pair generation, 30K goal

🤖 Claude Code Pasiq, CEO
For the Greater Good of All ✨

**Gemini's super skill: QA Engineering** 🎯
**The standard that scales** 📏
**Quality embedded in the prompt** ✅

**This is how we maintain excellence at 30,000 pairs.** 🚀
