# Quick Integration Guide for Future Sessions

This guide documents the successful integration methodology for Session 42 that can be reused for future sessions.

---

## Integration Workflow

### 1. Preparation
```bash
# Check current database state
python check_db_status42.py  # (modify for your session)

# Verify source file exists
ls session[XX]_*.txt
```

### 2. Integration Script Template

```python
import sqlite3
import re
import json

DB_PATH = r"C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db"
SOURCE_FILE = r"C:\Users\vlaro\dreamteam\session[XX]_*.txt"
SESSION_NUMBER = XX
CATEGORY = "Your Category"

# Step 1: Cleanup existing data
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM qa_pairs WHERE indicator_id IN (SELECT id FROM crypto_indicators WHERE session_number = ?)", (SESSION_NUMBER,))
cursor.execute("DELETE FROM crypto_indicators WHERE session_number = ?", (SESSION_NUMBER,))
conn.commit()

# Step 2: Parse file
with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract indicators and Q&A pairs
# Pattern: Look for indicator section headers, then extract Q/A pairs
indicator_qa = {}

for ind_name in INDICATOR_NAMES:
    # Find section
    pattern = rf'{re.escape(ind_name.upper())}.*?\n=(.*?)(?=\n=+\s*\n\d+|$)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        section_text = match.group(1)

        # Extract Q&A pairs
        qa_pattern = r'Q(\d+):\s*(.*?)\s*\nA\1:\s*(.*?)(?=\n\s*Q\d+:|\Z)'
        pairs = []

        for qa_match in re.finditer(qa_pattern, section_text, re.DOTALL):
            pairs.append({
                'number': int(qa_match.group(1)),
                'question': ' '.join(qa_match.group(2).strip().split()),
                'answer': ' '.join(qa_match.group(3).strip().split())
            })

        indicator_qa[ind_name] = pairs

# Step 3: Create indicators
indicator_ids = {}
for ind_name, description in INDICATOR_DEFS.items():
    cursor.execute("""
        INSERT INTO crypto_indicators (indicator_name, indicator_category, session_number, description)
        VALUES (?, ?, ?, ?)
    """, (ind_name, CATEGORY, SESSION_NUMBER, description))
    indicator_ids[ind_name] = cursor.lastrowid

conn.commit()

# Step 4: Insert Q&A pairs (with sequential numbering!)
for ind_name, pairs in indicator_qa.items():
    ind_id = indicator_ids[ind_name]

    # IMPORTANT: Use enumerate to ensure sequential numbering 1, 2, 3, ...
    for idx, pair in enumerate(pairs, 1):
        cursor.execute("""
            INSERT INTO qa_pairs (
                indicator_id, indicator_name, question, answer,
                pair_number, difficulty_level, tags, answer_length,
                crypto_specific, market_year
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ind_id, ind_name, pair['question'], pair['answer'],
            idx,  # Sequential: 1, 2, 3, ...
            get_difficulty(pair['answer']),
            get_tags(pair['question'] + ' ' + pair['answer']),
            len(pair['answer']),
            1, '2024-2025'
        ))

conn.commit()
conn.close()
```

---

## Key Lessons from Session 42

### 1. **Pair Numbering**
- ❌ **Don't** use original Q numbers from file if they're sequential across indicators
- ✅ **Do** renumber sequentially (1, 2, 3...) within each indicator
- Database has UNIQUE constraint on `(indicator_id, pair_number)`

### 2. **Cleanup Before Integration**
- Always delete existing data for the session number BEFORE creating new indicators
- Order matters: Delete Q&A pairs first, then indicators

### 3. **Regex Patterns**
- Use flexible patterns to handle emoji characters and formatting variations
- Use `re.DOTALL` flag to handle multi-line answers
- Test patterns on sample data first

### 4. **Validation**
- Verify expected vs. actual counts
- Check for duplicate questions
- Validate answer lengths (minimum 50 chars recommended)
- Verify pair number sequences are complete

---

## Common Issues & Solutions

### Issue: UNIQUE constraint failed
**Cause:** Duplicate pair_number within same indicator_id
**Solution:** Use `enumerate(pairs, 1)` to ensure sequential numbering

### Issue: No Q&A pairs extracted
**Cause:** Regex pattern doesn't match file format
**Solution:** Check file format, adjust pattern, test with sample

### Issue: Wrong number of pairs
**Cause:** Incomplete Q&A pairs in source or parsing issues
**Solution:** Count Q: marks in file, adjust filtering criteria

### Issue: Foreign key constraint
**Cause:** Indicators don't exist yet
**Solution:** Create indicators before inserting Q&A pairs

---

## Verification Checklist

- [ ] Indicator count matches expected
- [ ] Q&A pair count matches expected (or close)
- [ ] No duplicate questions
- [ ] No orphaned Q&A pairs
- [ ] Pair numbers are sequential (1-N) per indicator
- [ ] Sample queries return correct data
- [ ] Metadata fields populated (difficulty, tags, etc.)

---

## Scripts to Reuse

1. **Integration:** `session42_complete_integration.py`
2. **Reporting:** `session42_integration_report.py`
3. **Verification:** `check_db_status42.py`

Modify these templates for future sessions by changing:
- `SESSION_NUMBER`
- `SOURCE_FILE`
- `INDICATOR_NAMES` / `INDICATOR_DEFS`
- `CATEGORY`

---

## Database Schema Reference

### crypto_indicators table
- `id` - Primary key (auto-increment)
- `indicator_name` - TEXT, UNIQUE
- `indicator_category` - TEXT
- `session_number` - INTEGER
- `description` - TEXT
- `created_at` - TIMESTAMP

### qa_pairs table
- `qa_id` - Primary key (auto-increment)
- `indicator_id` - INTEGER (foreign key)
- `indicator_name` - TEXT
- `question` - TEXT
- `answer` - TEXT
- `pair_number` - INTEGER
- `difficulty_level` - TEXT (beginner/intermediate/advanced)
- `tags` - TEXT (JSON array)
- `answer_length` - INTEGER
- `crypto_specific` - BOOLEAN
- `market_year` - TEXT
- `created_at` - TEXT

**UNIQUE constraint:** `(indicator_id, pair_number)`

---

## Success Rate

Session 42 Integration:
- **Planned:** 5 indicators, ~500 Q&A pairs
- **Achieved:** 5 indicators, 450 Q&A pairs
- **Success Rate:** 100% indicators, 90% Q&A pairs
- **Quality:** All data integrity checks passed

---

**Last Updated:** November 4, 2025
