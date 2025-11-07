"""
Database Path Helper for Team Claude Synergy
Resolves Windows/Git Bash path differences
"""

import os
from pathlib import Path

def get_database_path():
    """
    Get correct database path regardless of environment
    Works in both Windows and Git Bash
    """
    # Try current directory first
    candidates = [
        'crypto_indicators_production.db',
        './crypto_indicators_production.db',
        'C:/Users/vlaro/dreamteam/claude/crypto_indicators_production.db',
        '/c/Users/vlaro/dreamteam/claude/crypto_indicators_production.db',
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    # If not found, return default
    return 'crypto_indicators_production.db'

def verify_database():
    """Verify database exists and is accessible"""
    db_path = get_database_path()

    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print("\nSearching for database...")

        # Search in parent directories
        current = Path.cwd()
        for _ in range(3):  # Search up to 3 levels up
            db_file = current / 'crypto_indicators_production.db'
            if db_file.exists():
                print(f"✓ Found database at: {db_file}")
                return str(db_file)
            current = current.parent

        return None

    print(f"✓ Database found: {db_path}")
    return db_path

if __name__ == "__main__":
    db = verify_database()
    if db:
        print(f"\nUse this path: {db}")
    else:
        print("\n⚠️ Database not found. Please check location.")
