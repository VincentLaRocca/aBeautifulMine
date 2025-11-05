# Q&A Database Copy

This package contains a complete copy of the Q&A database with all research question-answer pairs.

## Package Contents

### Database Files
- **research_qa.db** - SQLite database containing all research sessions and Q&A pairs

### JSON Export Files (RAG-Ready)
- **qa_pairs_rag_export_20251028_233056.json** - Structured JSON with sessions and Q&A pairs
- **qa_pairs_rag_export_20251028_233056_flattened.json** - Flattened format for easy RAG ingestion
- **rag_chunks_20251028_233057_chunks.json** - Pre-chunked documents (737 chunks, 4K chars max)

### Database Management Scripts
- **database_scripts/database_setup.py** - Database initialization and management
- **database_scripts/qa_importer.py** - Import/export utilities
- **verify_database.py** - Database verification script

## Database Overview

The database contains:
- **Total Sessions**: 11 research sessions
- **Total Q&A Pairs**: 709 pairs
- **Total Tokens Used**: 516,665
- **Topics Covered**:
  - Technical Analysis (Moving Averages, Patterns, Indicators)
  - Artificial Intelligence Ethics
  - Sample Database Testing

## Database Schema

### research_sessions table
- id (PRIMARY KEY)
- topic
- created_at
- total_queries
- successful_queries
- tokens_used

### question_answer_pairs table
- id (PRIMARY KEY)
- session_id (FOREIGN KEY)
- query_index
- question
- answer
- question_length
- answer_length
- tokens_used
- created_at

## Usage Instructions

### 1. Verify Database Copy
```bash
cd QADatabase_Copy
python verify_database.py
```

### 2. Access Database Programmatically
```python
import sys
sys.path.append('database_scripts')
from database_setup import DatabaseManager

# Initialize database
db = DatabaseManager('research_qa.db')

# Get statistics
stats = db.get_statistics()
print(f"Total Q&A pairs: {stats['total_qa_pairs']}")

# Get all sessions
sessions = db.get_sessions()

# Get Q&A pairs for a specific session
qa_pairs = db.get_session_qa_pairs(session_id)
```

### 3. For RAG System Integration

#### Option A: Use Flattened JSON
```python
import json

with open('qa_pairs_rag_export_20251028_233056_flattened.json', 'r') as f:
    data = json.load(f)

for document in data['documents']:
    text_content = document['text']
    metadata = document['metadata']
    # Process for vector database ingestion
```

#### Option B: Use Pre-chunked JSON
```python
import json

with open('rag_chunks_20251028_233057_chunks.json', 'r') as f:
    data = json.load(f)

for chunk in data['chunks']:
    chunk_text = chunk['text']
    chunk_metadata = chunk['metadata']
    # Each chunk is optimized for vector database ingestion
```

### 4. Database Management Commands

#### List All Sessions
```bash
python database_scripts/qa_importer.py list
```

#### Show Session Details
```bash
python database_scripts/qa_importer.py show <session_id>
```

#### Export Session to JSON
```bash
python database_scripts/qa_importer.py export <session_id>
```

#### Search Q&A Pairs
```bash
python database_scripts/qa_importer.py search "search_term"
```

#### Show Database Statistics
```bash
python database_scripts/qa_importer.py stats
```

## JSON Format for RAG Systems

### Flattened Structure
Each document contains:
- **id**: Unique identifier (sessionID_queryIndex)
- **content**: Combined Q&A text for vectorization
- **question**: Original question
- **answer**: Original answer
- **metadata**: Rich metadata (topic, timestamps, lengths, tokens)
- **rag_optimized**: RAG-specific fields (chunk_type, word_count, char_count)

### Chunked Structure
Each chunk contains:
- **id**: Unique chunk identifier
- **text**: Chunked text content (≤4000 chars)
- **metadata**: Source information and chunk classification
- **chunk_type**: Classification (complete_qa, question_only, answer_partial, etc.)

## Dependencies Required

- Python 3.7+
- sqlite3 (built-in)
- json (built-in)

Note: The database scripts include colorama for colored terminal output, but this is optional.

## Database Size

- **Database file**: ~28KB (SQLite is highly compressed)
- **JSON exports**: ~15.8MB total
- **Prepared for**: Vector database ingestion, RAG systems, analysis

## Security Note

This database contains AIgenerated research Q&A pairs. No personal data or sensitive information is included. All content is for research and educational purposes.

## Support

For questions about the database structure or usage, refer to the database scripts included in the **database_scripts** folder.
