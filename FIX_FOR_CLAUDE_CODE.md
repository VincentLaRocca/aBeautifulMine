# Quick Fix: Database Path Issue

## Problem
⚠️ DATABASE: Not in current location (may be Windows path)

## Solution

The database IS there, just need correct path format.

### Option 1: Use Helper (Recommended)
```python
from database_path_helper import get_database_path

# In your script, replace:
db_path = 'crypto_indicators_production.db'

# With:
db_path = get_database_path()
```

### Option 2: Direct Path Fix
```python
# Try these paths in order:
db_paths = [
    'crypto_indicators_production.db',  # Current directory
    './crypto_indicators_production.db',  # Explicit current
    'C:/Users/vlaro/dreamteam/claude/crypto_indicators_production.db',  # Windows absolute
]

import os
for path in db_paths:
    if os.path.exists(path):
        db_path = path
        break
```

### Option 3: Verify First
```bash
# Run this to verify database location
python database_path_helper.py
```

It will show you the exact path to use.

## Quick Test

```python
import sqlite3
import os

# Check database exists
db = 'crypto_indicators_production.db'
print(f"Exists: {os.path.exists(db)}")
print(f"Full path: {os.path.abspath(db)}")

# Try connecting
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM qa_pairs')
print(f"Current pairs: {c.fetchone()[0]:,}")
conn.close()
```

## For integrate_sessions_batch_synergy.py

Update line 23:
```python
# OLD:
def __init__(self, db_path: str = 'crypto_indicators_production.db'):

# NEW:
def __init__(self, db_path: str = None):
    if db_path is None:
        from database_path_helper import get_database_path
        db_path = get_database_path()
    self.db_path = db_path
```

## Synergy Continues!

Database is at: `/c/Users/vlaro/dreamteam/claude/crypto_indicators_production.db`

Just use the helper and you're rolling! 🚀
