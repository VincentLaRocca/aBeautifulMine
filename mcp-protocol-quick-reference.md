# MCP Protocol v1.0: Quick Reference Card

**For:** Sessions 12-13 (Pilot Test)
**Goal:** 5 indicators, 30 Q&A pairs in 2-3 hours for <$2.00

---

## 🚀 Quick Start

### 1. Initialize (5 min)
```python
mcp__gemini__start_conversation(id="session_12")
```

### 2. For Each Indicator (×5):

**Batch 1: Q1-Q3** (2-3 min)
```python
prompt = f"Generate Q1-Q3 for {indicator}, 1200-1500 words each"
response = mcp__gemini__chat(message=prompt, conversationId="session_12", maxTokens=15000)
```

**Batch 2: Q4-Q6** (2-3 min)
```python
prompt = f"Generate Q4-Q6 for {indicator}, 1200-1500 words each"
response = mcp__gemini__chat(message=prompt, conversationId="session_12", maxTokens=15000)
```

### 3. Assemble JSON with Python (30 min)
- Parse all responses
- Build proper JSON structure
- Validate (30 pairs, all >1000 words)

### 4. Deliver & Import (10 min)
- Copy to Gemini inbox
- Run `import_session_generic.py`
- Verify integrity

---

## ⚠️ Error Handling

**Token Limit Hit?**
→ Request completion: "Complete the previous answer from where it was cut off"

**500 Error?**
→ Retry 3× with exponential backoff (2s, 4s, 8s wait)

**Answer Too Short?**
→ Request expansion: "Previous answer was {X} words, please expand to 1200-1500"

---

## 📊 Success Metrics

### Must-Have
- ✅ 30 Q&A pairs
- ✅ Valid JSON
- ✅ All answers ≥1000 words
- ✅ Import successful

### Target
- 🎯 <3 hours
- 🎯 <$2.00
- 🎯 ≥95% quality
- 🎯 <5% error rate

---

## 🔧 Key Adaptations from Session 10

1. **Small batches** (2-3 questions, not 6)
2. **Python assembles JSON** (not Gemini)
3. **Retry logic built-in** (3 attempts)
4. **Pragmatic completion** (95% > 100%)

---

## 📍 File Locations

**Protocol:** `~/dreamteam/claude/mcp-protocol-v1-practical.md`
**This Card:** `~/dreamteam/claude/mcp-protocol-quick-reference.md`
**Template:** `session_10_current_structure.json`
**Import:** `import_session_generic.py`

---

## 🚨 Escalation

If after Session 12:
- Quality <90% → Switch to Hybrid
- Cost >$3.00 → Review approach
- Time >4 hours → Inbox/outbox fallback

---

*Full protocol details in `mcp-protocol-v1-practical.md`*
