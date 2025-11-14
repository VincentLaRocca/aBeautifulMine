# Enhanced Answer Prompt for AI Training Quality

## Current Prompt Analysis

Your current prompt is **solid** and covers the essentials:
- ✅ Length requirement (3000+ chars)
- ✅ Structure guidelines
- ✅ Research emphasis
- ✅ Expert tone
- ✅ One question = one answer

## Recommended Enhancements

Here's an **enhanced version** optimized specifically for AI training datasets:

---

## Enhanced Prompt (Recommended)

```markdown
Core Task:

Your mission is to create a comprehensive, expert-level answer optimized for training AI agents. This answer will be used to train models to provide high-quality responses to cryptocurrency and trading questions.

CRITICAL: This is for ONE QUESTION ONLY. Answer each question individually with a complete, standalone response of 3,000+ characters.

---

## Quality Standards for AI Training Data

### 1. Accuracy & Factual Correctness
- Base all information on established, verifiable sources
- When discussing formulas, calculations, or metrics, provide exact definitions
- Include specific numbers, percentages, and data points when available
- Distinguish between established facts and expert opinions
- If information is uncertain or debated, acknowledge multiple perspectives

### 2. Depth & Comprehensiveness
- Move beyond surface-level definitions to explain underlying mechanisms
- Explain the "why" behind concepts, not just the "what"
- Cover foundational concepts before advancing to complex applications
- Include both theoretical understanding and practical implementation
- Address edge cases, exceptions, and limitations

### 3. Structure for Learning
Structure your answer to maximize learning value:

**Introduction (200-400 chars)**
- Clear definition of the core concept
- Brief context on why it matters
- Scope of what will be covered

**Main Body (2000-2500 chars)**
- **Fundamentals**: Core concepts, definitions, basic mechanics
- **Mechanics**: How it works step-by-step, formulas, calculations
- **Application**: Real-world usage with crypto-specific examples
- **Examples**: Concrete scenarios (e.g., "When analyzing BTC/USD on a 4-hour chart...")
- **Nuances**: Edge cases, variations, common misconceptions

**Practical Section (500-800 chars)**
- Step-by-step implementation guide
- Best practices and common pitfalls
- Real trading scenarios with specific examples
- Integration with other tools/indicators

**Risks & Limitations (300-500 chars)**
- What can go wrong
- When this approach fails
- Limitations and constraints
- Risk management considerations

**Conclusion (200-300 chars)**
- Key takeaways
- When to use this approach
- Next steps for deeper learning

### 4. Educational Value
- Write as if teaching a professional trader who wants to understand deeply
- Use progressive disclosure: simple concepts first, then build complexity
- Include "why" explanations: don't just state facts, explain reasoning
- Use analogies and comparisons to clarify complex concepts
- Provide context: how this fits into broader trading strategies

### 5. Crypto-Specific Focus
- Always use cryptocurrency examples (BTC, ETH, SOL, etc.)
- Reference crypto-specific platforms, exchanges, and tools
- Address crypto market characteristics (24/7 trading, volatility, etc.)
- Include DeFi, NFT, or blockchain-specific considerations when relevant
- Use realistic price examples and scenarios

### 6. Actionability
- Provide concrete steps traders can follow
- Include specific parameter values, thresholds, or settings
- Give examples of "good" vs "bad" implementations
- Explain decision-making processes
- Include checklists or decision trees when helpful

### 7. Consistency & Clarity
- Use consistent terminology throughout
- Define technical terms on first use
- Use Markdown formatting for readability:
  - **Bold** for key concepts
  - Headings for major sections
  - Bullet points for lists
  - Code blocks for formulas or calculations
- Write in clear, professional prose (avoid overly casual or overly academic)

### 8. Training Data Optimization
- Ensure the answer is self-contained (can be understood without context)
- Avoid references to "previous questions" or "as mentioned above"
- Include enough context that an AI can learn from this single example
- Make implicit knowledge explicit (explain assumptions)
- Include common variations of the concept

---

## Output Requirements

- **Minimum Length**: 3,000 characters (strictly enforced)
- **Format**: Markdown with clear structure
- **Tone**: Expert, educational, professional
- **Style**: Clear, precise, comprehensive
- **Examples**: Include at least 2-3 concrete crypto trading examples

---

## What to Avoid

- ❌ Generic or vague statements without specifics
- ❌ Overly simplistic explanations (assume professional audience)
- ❌ Hallucinated facts or unsupported claims
- ❌ References to other questions or external context
- ❌ Repetitive content to meet length requirements
- ❌ Yes/no answers without explanation
- ❌ Marketing language or promotional content

---

## Example Structure Template

```markdown
# [Concept Name]: [Brief Definition]

[Introduction paragraph - what is it, why it matters]

## Understanding [Concept]

[Core explanation with mechanics]

## How [Concept] Works

[Step-by-step explanation]

## Practical Application in Crypto Trading

### Example 1: [Specific Scenario]
[Detailed example with numbers]

### Example 2: [Another Scenario]
[Another detailed example]

## Best Practices

[Actionable guidance]

## Common Pitfalls and Limitations

[What to watch out for]

## Key Takeaways

[Summary points]
```

---

## Quality Checklist

Before finalizing your answer, verify:
- [ ] Meets 3,000+ character minimum
- [ ] Includes at least 2-3 concrete crypto examples
- [ ] Explains "why" not just "what"
- [ ] Covers fundamentals before advanced topics
- [ ] Includes practical application section
- [ ] Addresses risks/limitations
- [ ] Uses proper Markdown formatting
- [ ] Self-contained (no external references)
- [ ] Professional, expert tone throughout
- [ ] Actionable and specific (not vague)
```

---

## Key Improvements Over Current Prompt

1. **Training-Specific Focus**: Explicitly optimized for AI training data
2. **Structured Template**: Clear section-by-section guidance
3. **Quality Checklist**: Verifiable quality standards
4. **Educational Emphasis**: Focus on teaching value
5. **Self-Contained**: Ensures answers work independently
6. **Actionability**: More emphasis on practical, actionable content
7. **Consistency**: Better guidance on terminology and style
8. **Examples**: More emphasis on concrete examples

---

## Implementation

You can replace the prompt in:
- `multi_agent_system/config.json` (answer_prompt field)
- `multi_agent_system/answer_generator.py` (default prompt)
- `multi_agent_system/orchestrator.py` (default config)

Or pass it as a config parameter when initializing the orchestrator.

