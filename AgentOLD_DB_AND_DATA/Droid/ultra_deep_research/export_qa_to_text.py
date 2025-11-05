#!/usr/bin/env python3
"""
Export all Q&A pairs from database to a text file.
"""

import os
import sys
from datetime import datetime
try:
    from .database.database_setup import DatabaseManager
except ImportError:
    from database.database_setup import DatabaseManager

def export_all_qa_pairs_to_text(output_file: str = None):
    """
    Export all Q&A pairs from database to a formatted text file.
    
    Args:
        output_file: Output file path. If None, generates timestamped filename.
    
    Returns:
        str: Path to the created text file.
    """
    # Initialize database connection
    db = DatabaseManager()
    
    # Get all sessions
    sessions = db.get_sessions()
    
    if not sessions:
        print("No research sessions found in database.")
        return None
    
    # Generate output filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"qa_pairs_export_{timestamp}.txt"
    
    # Write all Q&A pairs to text file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("QUESTION AND ANSWER PAIRS EXPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Sessions: {len(sessions)}\n")
        f.write("="*80 + "\n\n")
        
        # Get database statistics
        stats = db.get_statistics()
        f.write("DATABASE STATISTICS\n")
        f.write("-"*40 + "\n")
        f.write(f"Total Q&A Pairs: {stats['total_qa_pairs']:,}\n")
        f.write(f"Total Sessions: {stats['total_sessions']:,}\n")
        f.write(f"Average Answer Length: {stats['average_answer_length']} characters\n")
        f.write(f"Total Tokens Used: {stats['total_tokens_used']:,}\n")
        f.write("\n" + "="*80 + "\n\n")
        
        # Export each session's Q&A pairs
        for session in sessions:
            qa_pairs = db.get_session_qa_pairs(session['id'])
            
            if not qa_pairs:
                continue
                
            f.write(f"SESSION {session['id']}\n")
            f.write(f"Topic: {session['topic']}\n")
            f.write(f"Created: {session['created_at']}\n")
            f.write(f"Number of Pairs: {len(qa_pairs)}\n")
            f.write("-"*80 + "\n\n")
            
            for i, pair in enumerate(qa_pairs, 1):
                f.write(f"PAIR {i} (Index: {pair['query_index']})\n")
                f.write(f"Question Length: {pair['question_length']} chars\n")
                f.write(f"Answer Length: {pair['answer_length']} chars\n")
                f.write(f"Tokens Used: {pair['tokens_used']}\n")
                f.write(f"Created: {pair['created_at']}\n")
                f.write("-"*40 + "\n")
                f.write(f"Question:\n{pair['question']}\n\n")
                f.write(f"Answer:\n{pair['answer']}\n\n")
                f.write("="*80 + "\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
        
    print(f"Exported {stats['total_qa_pairs']} Q&A pairs to {output_file}")
    return output_file

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export all Q&A pairs to text file")
    parser.add_argument("-o", "--output", help="Output file path")
    
    args = parser.parse_args()
    
    try:
        output_file = export_all_qa_pairs_to_text(args.output)
        if output_file:
            print(f"Export completed successfully: {output_file}")
        else:
            print("No Q&A pairs found in database")
            sys.exit(1)
    except Exception as e:
        print(f"Error during export: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
