#!/usr/bin/env python3
"""
Verify the database copy and show statistics.
"""

import sys
import os

# Add database_scripts to path
sys.path.append('database_scripts')
from database_setup import DatabaseManager

def main():
    print("=== DATABASE VERIFICATION ===")
    
    # Initialize database with correct path
    db = DatabaseManager('research_qa.db')
    
    # Get statistics
    stats = db.get_statistics()
    
    print(f"Total Research Sessions: {stats['total_sessions']}")
    print(f"Total Q&A Pairs: {stats['total_qa_pairs']:,}")
    print(f"Average Answer Length: {stats['average_answer_length']} characters")
    print(f"Total Tokens Used: {stats['total_tokens_used']:,}")
    
    # Get and show sessions
    sessions = db.get_sessions()
    
    if sessions:
        print(f"\nSessions in database:")
        for session in sessions:
            qa_count = len(db.get_session_qa_pairs(session['id']))
            print(f"  Session {session['id']}: {session['topic']} ({qa_count} pairs)")
    
    # Check file size
    db_size = os.path.getsize('research_qa.db')
    print(f"\nDatabase file size: {db_size:,} bytes")
    
    # Check JSON files
    json_files = [
        'qa_pairs_rag_export_20251028_233056.json',
        'qa_pairs_rag_export_20251028_233056_flattened.json', 
        'rag_chunks_20251028_233057_chunks.json'
    ]
    
    print(f"\nJSON export files:")
    for json_file in json_files:
        if os.path.exists(json_file):
            size = os.path.getsize(json_file)
            print(f"  [OK] {json_file} ({size:,} bytes)")
        else:
            print(f"  [MISSING] {json_file}")
    
    print(f"\n=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    main()
