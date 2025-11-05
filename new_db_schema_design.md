# Production Database Schema Design
**Date:** 2025-11-02
**Purpose:** Support ultra_deep_research methodology with 100 Q&A pairs per indicator

---

## Design Requirements

1. **Scale:** 227 indicators × 100 Q&A pairs = 22,700 total Q&A pairs
2. **Methodology:** Ultra-deep research with comprehensive answers
3. **Even Distribution:** Data spread across all indicator categories
4. **AI Training Ready:** Structured for ingestion by AI models

---

## Proposed Schema

### Table: sessions
```sql
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_number INTEGER UNIQUE NOT NULL,
    session_date TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    total_indicators INTEGER DEFAULT 5,
    total_qa_pairs INTEGER DEFAULT 500,
    research_method TEXT DEFAULT 'ultra_deep_research',
    executor TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Table: indicators
```sql
CREATE TABLE indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_name TEXT UNIQUE NOT NULL,
    indicator_slug TEXT UNIQUE NOT NULL,
    session_number INTEGER NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    master_list_position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_number) REFERENCES sessions(session_number)
);
```

### Table: qa_pairs
```sql
CREATE TABLE qa_pairs (
    qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_id INTEGER NOT NULL,
    pair_number INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    topic TEXT,
    created_date TEXT,
    answer_word_count INTEGER,
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id),
    UNIQUE(indicator_id, pair_number)
);
```

### Table: metadata
```sql
CREATE TABLE metadata (
    meta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_number INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (session_number) REFERENCES sessions(session_number)
);
```

---

## Key Differences from Old Schema

1. **No 6 Q&A limit** - Schema supports 100+ Q&A pairs per indicator
2. **pair_number field** - Tracks position in the 100-question sequence
3. **answer_word_count** - For quality metrics and filtering
4. **research_method field** - Documents ultra_deep_research approach
5. **master_list_position** - Maps to original 227 indicator list
6. **metadata table** - Flexible storage for research parameters

---

## Expected Data Volume

- **Sessions:** ~46 sessions (227 indicators ÷ 5 per session)
- **Indicators:** 227 total
- **Q&A Pairs:** ~22,700 (227 × 100)
- **Estimated DB Size:** 500-800 MB (compressed text)

---

## Performance Considerations

- Index on indicator_slug for fast lookups
- Index on session_number for session queries
- Index on category for filtering by indicator type
- Composite index on (indicator_id, pair_number) for ordered retrieval

---

## Next Steps

1. Create production database with this schema
2. Import Droid's 5 derivatives indicators (500 Q&A pairs)
3. Verify data integrity
4. Plan systematic collection of remaining 222 indicators
