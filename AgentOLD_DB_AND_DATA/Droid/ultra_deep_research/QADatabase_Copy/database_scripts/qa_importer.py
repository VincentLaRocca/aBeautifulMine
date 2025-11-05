#!/usr/bin/env python3
"""
Import question-answer pairs from research reports into the database.
"""

import json
import os
import sys
from typing import Dict, Any, List
try:
    from .database_setup import DatabaseManager
except ImportError:
    from database_setup import DatabaseManager
from colorama import Fore, Style, init
init()

class QAImporter:
    def __init__(self):
        self.db = DatabaseManager()
    
    def import_from_search_results(self, topic: str, search_results: List[Dict[str, Any]], tokens_used: int = 0) -> Dict[str, Any]:
        """Import Q&A pairs from search results data"""
        print(f"{Fore.YELLOW}Importing Q&A pairs for topic: {topic}{Style.RESET_ALL}")
        
        # Create research session
        total_queries = len(search_results)
        successful_queries = sum(1 for r in search_results if r.get("success", False))
        session_id = self.db.create_research_session(
            topic=topic,
            total_queries=total_queries,
            successful_queries=successful_queries,
            tokens_used=tokens_used
        )
        
        print(f"{Fore.GREEN}Created research session ID: {session_id}{Style.RESET_ALL}")
        
        # Store question-answer pairs
        import_result = self.db.store_question_answer_pairs(session_id, search_results)
        
        # Update session stats with actual token usage if available
        actual_tokens = sum(r.get("tokens", {}).get("total_tokens", 0) for r in search_results)
        if actual_tokens > 0:
            self.db.update_session_stats(session_id, total_queries, successful_queries, actual_tokens)
        
        print(f"+ Stored {import_result['stored']} Q&A pairs")
        if import_result['skipped'] > 0:
            print(f"+ Skipped {import_result['skipped']} failed/uncomplete pairs")
        
        return {
            "session_id": session_id,
            "topic": topic,
            "stored": import_result["stored"],
            "skipped": import_result["skipped"]
        }
    
    def import_from_json_file(self, file_path: str) -> Dict[str, Any]:
        """Import Q&A pairs from a JSON file"""
        print(f"{Fore.BLUE}Importing from JSON file: {file_path}{Style.RESET_ALL}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Expecting JSON format: {"topic": "...", "pairs": [{"question": "...", "answer": "..."}]}
            topic = data.get("topic", os.path.basename(file_path))
            pairs = data.get("pairs", data.get("question_answer_pairs", []))
            
            # Convert to search_results format
            search_results = []
            for i, pair in enumerate(pairs):
                tokens_used = pair.get("metadata", {}).get("tokens_used", 0)
                tokens_dict = {"total_tokens": tokens_used} if tokens_used else {}
                
                search_results.append({
                    "query": pair.get("question", ""),
                    "response": pair.get("answer", ""),
                    "success": True,
                    "index": i,
                    "tokens": tokens_dict
                })
            
            return self.import_from_search_results(topic, search_results)
            
        except Exception as e:
            print(f"{Fore.RED}Error importing JSON file: {str(e)}{Style.RESET_ALL}")
            return {"error": str(e)}
    
    def export_session_to_json(self, session_id: int, output_file: str = None):
        """Export a session's Q&A pairs to a JSON file"""
        try:
            json_data = self.db.get_session_qa_pairs_json(session_id)
            
            if not output_file:
                # Generate filename based on session topic and ID
                sessions = self.db.get_sessions()
                session = next((s for s in sessions if s["id"] == session_id), None)
                if session:
                    topic = session["topic"].replace(" ", "_").replace("/", "_").lower()
                    output_file = f"qa_export_{topic}_{session_id}.json"
                else:
                    output_file = f"qa_export_session_{session_id}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            print(f"{Fore.GREEN}Exported session {session_id} to {output_file}{Style.RESET_ALL}")
            return output_file
            
        except Exception as e:
            print(f"{Fore.RED}Error exporting session: {str(e)}{Style.RESET_ALL}")
            return None
    
    def list_sessions(self):
        """List all research sessions"""
        sessions = self.db.get_sessions()
        
        if not sessions:
            print(f"{Fore.YELLOW}No research sessions found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print("RESEARCH SESSIONS")
        print(f"{'=' * 80}{Style.RESET_ALL}")
        
        for session in sessions:
            # Get QA pair count for this session
            qa_count = len(self.db.get_session_qa_pairs(session["id"]))
            
            print(f"\n{Fore.GREEN}Session ID: {session['id']}{Style.RESET_ALL}")
            print(f"Topic: {session['topic']}")
            print(f"Created: {session['created_at']}")
            print(f"Q&A Pairs: {qa_count}")
            print(f"Total Queries: {session['total_queries']}")
            print(f"Successful: {session['successful_queries']}")
            print(f"Tokens Used: {session['tokens_used']:,}")
            print("-" * 40)
    
    def show_session_details(self, session_id: int):
        """Show detailed information about a session"""
        qa_pairs = self.db.get_session_qa_pairs(session_id)
        
        if not qa_pairs:
            print(f"{Fore.YELLOW}No Q&A pairs found for session {session_id}{Style.RESET_ALL}")
            return
        
        session = next((s for s in self.db.get_sessions() if s["id"] == session_id), None)
        
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"SESSION DETAILS: {session['topic'] if session else 'Unknown'}")
        print(f"{'=' * 80}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Session ID:{Style.RESET_ALL} {session_id}")
        print(f"{Fore.GREEN}Topic:{Style.RESET_ALL} {session['topic'] if session else 'Unknown'}")
        print(f"{Fore.GREEN}Created:{Style.RESET_ALL} {session['created_at'] if session else 'Unknown'}")
        print(f"{Fore.GREEN}Q&A Pairs:{Style.RESET_ALL} {len(qa_pairs)}")
        
        total_question_chars = sum(p['question_length'] for p in qa_pairs)
        total_answer_chars = sum(p['answer_length'] for p in qa_pairs)
        total_tokens = sum(p['tokens_used'] for p in qa_pairs)
        
        print(f"{Fore.GREEN}Total Question Characters:{Style.RESET_ALL} {total_question_chars:,}")
        print(f"{Fore.GREEN}Total Answer Characters:{Style.RESET_ALL} {total_answer_chars:,}")
        print(f"{Fore.GREEN}Total Characters:{Style.RESET_ALL} {total_question_chars + total_answer_chars:,}")
        print(f"{Fore.GREEN}Total Tokens Used:{Style.RESET_ALL} {total_tokens:,}")
        
        # Show first few pairs as preview
        print(f"\n{Fore.YELLOW}Preview (first 3 pairs):{Style.RESET_ALL}")
        for i, pair in enumerate(qa_pairs[:3]):
            print(f"\n{Fore.CYAN}Pair {pair['query_index'] + 1}:{Style.RESET_ALL}")
            print(f"Q: {pair['question'][:100]}{'...' if len(pair['question']) > 100 else ''}")
            print(f"A: {pair['answer'][:150]}{'...' if len(pair['answer']) > 150 else ''}")
        
        if len(qa_pairs) > 3:
            print(f"\n{Fore.YELLOW}... and {len(qa_pairs) - 3} more pairs{Style.RESET_ALL}")
    
    def search_pairs(self, query_text: str, limit: int = 10):
        """Search question-answer pairs"""
        results = self.db.search_qa_pairs(query_text, limit)
        
        if not results:
            print(f"{Fore.YELLOW}No results found for: {query_text}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Search Results for: {query_text}{Style.RESET_ALL}")
        print(f"Found {len(results)} results (showing first {min(len(results), limit)})")
        print("-" * 60)
        
        for result in results[:limit]:
            print(f"\n{Fore.GREEN}Session {result['session_id']} - {result['topic']}{Style.RESET_ALL}")
            print(f"Q: {result['question'][:80]}{'...' if len(result['question']) > 80 else ''}")
            print(f"A: {result['answer'][:100]}{'...' if len(result['answer']) > 100 else ''}")
    
    def show_statistics(self):
        """Display database statistics"""
        stats = self.db.get_statistics()
        
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print("DATABASE STATISTICS")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Total Research Sessions:{Style.RESET_ALL} {stats['total_sessions']}")
        print(f"{Fore.GREEN}Total Q&A Pairs:{Style.RESET_ALL} {stats['total_qa_pairs']:,}")
        print(f"{Fore.GREEN}Average Answer Length:{Style.RESET_ALL} {stats['average_answer_length']} characters")
        print(f"{Fore.GREEN}Total Tokens Used:{Style.RESET_ALL} {stats['total_tokens_used']:,}")
        
        if stats['top_sessions']:
            print(f"\n{Fore.YELLOW}Top Sessions by Q&A Pairs:{Style.RESET_ALL}")
            for i, session in enumerate(stats['top_sessions'], 1):
                print(f"  {i}. {session['topic']} ({session['pair_count']} pairs)")

def print_usage():
    """Print usage instructions"""
    print(f"{Fore.CYAN}QA Importer Usage:{Style.RESET_ALL}")
    print("  python qa_importer.py <command> [options]")
    print("")
    print(f"{Fore.YELLOW}Commands:{Style.RESET_ALL}")
    print("  list                     List all research sessions")
    print("  stats                    Show database statistics")
    print("  show <session_id>        Show details for a specific session")
    print("  export <session_id>      Export session to JSON file")
    print("  search <query>           Search Q&A pairs")
    print("  import-json <file.json>  Import from JSON file")
    print("")
    print(f"{Fore.BLUE}Examples:{Style.RESET_ALL}")
    print("  python qa_importer.py list")
    print("  python qa_importer.py show 1")
    print("  python qa_importer.py export 1")
    print("  python qa_importer.py search \"blockchain\"")

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    importer = QAImporter()
    command = sys.argv[1]
    
    try:
        if command == "list":
            importer.list_sessions()
        elif command == "stats":
            importer.show_statistics()
        elif command == "show" and len(sys.argv) >= 3:
            session_id = int(sys.argv[2])
            importer.show_session_details(session_id)
        elif command == "export" and len(sys.argv) >= 3:
            session_id = int(sys.argv[2])
            importer.export_session_to_json(session_id)
        elif command == "search" and len(sys.argv) >= 3:
            query = " ".join(sys.argv[2:])
            importer.search_pairs(query)
        elif command == "import-json" and len(sys.argv) >= 3:
            file_path = sys.argv[2]
            importer.import_from_json_file(file_path)
        else:
            print(f"{Fore.RED}Invalid command or missing arguments{Style.RESET_ALL}")
            print_usage()
            sys.exit(1)
            
    except ValueError as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
