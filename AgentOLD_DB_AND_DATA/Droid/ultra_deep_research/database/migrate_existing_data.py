#!/usr/bin/env python3
"""
Script to migrate existing research data into the database system.
This script parses existing research report files and extracts Q&A pairs.
"""

import os
import re
import json
from typing import List, Dict, Any
from .database_setup import DatabaseManager
from .qa_importer import QAImporter
from colorama import Fore, Style, init
init()

class DataMigrator:
    def __init__(self):
        self.db = DatabaseManager()
        self.importer = QAImporter()
    
    def extract_qa_from_report_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract Q&A pairs from an existing research report file.
        This is a simplified parser - you may need to adjust based on actual file format.
        """
        print(f"{Fore.YELLOW}Processing: {file_path}{Style.RESET_ALL}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract topic from filename (basic approach)
            filename = os.path.basename(file_path)
            topic_part = filename.replace('research_report_', '').split('_2025')[0]
            topic = topic_part.replace('_', ' ').title()
            
            # Try to extract Q&A pairs using regex patterns
            # This is a simplified approach - adjust based on your actual format
            
            # Pattern to match the Q&A pairs section
            qa_section_match = re.search(r'QUESTION-ANSWER PAIRS WITH CHARACTER COUNTS.*?(?=\n\n[^A-Z])', content, re.DOTALL)
            
            if not qa_section_match:
                # Fallback: try different pattern
                qa_section_match = re.search(r'Pair [0-9]+:.*', content, re.DOTALL)
            
            search_results = []
            
            if qa_section_match:
                qa_section = qa_section_match.group(0)
                
                # Extract individual pairs using regex
                pair_pattern = r'Pair (\d+):\nquestion: (.*?)\nquestion characters: \d+\nanswer: (.*?)\nanswer characters: \d+'
                matches = re.findall(pair_pattern, qa_section, re.DOTALL)
                
                for i, (pair_num, question, answer) in enumerate(matches):
                    # Clean up the text (remove ANSI color codes)
                    question = re.sub(r'\x1b\[[0-9;]*m', '', question).strip()
                    answer = re.sub(r'\x1b\[[0-9;]*m', '', answer).strip()
                    
                    if question and answer:
                        search_results.append({
                            "query": question,
                            "response": answer,
                            "success": True,
                            "index": int(pair_num) - 1,
                            "tokens": {}  # No token info in report files
                        })
            
            print(f"{Fore.GREEN}Extracted {len(search_results)} Q&A pairs{Style.RESET_ALL}")
            
            return {
                "file_path": file_path,
                "topic": topic,
                "search_results": search_results
            }
            
        except Exception as e:
            print(f"{Fore.RED}Error processing {file_path}: {str(e)}{Style.RESET_ALL}")
            return None
    
    def migrate_from_report_files(self, pattern: str = "research_report_*.txt"):
        """Migrate Q&A pairs from existing research report files"""
        print(f"{Fore.CYAN}{'=' * 80}")
        print("DATA MIGRATION FROM RESEARCH REPORTS")
        print(f"{'=' * 80}{Style.RESET_ALL}")
        
        report_files = [f for f in os.listdir('.') if f.startswith('research_report_') and f.endswith('.txt')]
        
        if not report_files:
            print(f"{Fore.YELLOW}No report files found matching pattern: {pattern}{Style.RESET_ALL}")
            return
        
        total_imported = 0
        total_failed = 0
        
        for report_file in report_files:
            extracted = self.extract_qa_from_report_file(report_file)
            
            if extracted and extracted['search_results']:
                result = self.importer.import_from_search_results(
                    topic=extracted['topic'],
                    search_results=extracted['search_results']
                )
                
                if 'session_id' in result:
                    print(f"+ Imported {result['stored']} pairs for: {extracted['topic']}")
                    total_imported += result['stored']
                else:
                    print(f"- Failed to import: {extracted['topic']}")
                    total_failed += 1
            else:
                print(f"- No Q&A data found in: {report_file}")
                total_failed += 1
        
        print(f"\n{Fore.CYAN}Migration Summary:{Style.RESET_ALL}")
        print(f"Successfully imported: {total_imported} Q&A pairs")
        print(f"Failed files: {total_failed}")
    
    def create_sample_json_data(self):
        """Create a sample JSON file with Q&A data for testing"""
        sample_data = {
            "topic": "Sample Database Testing",
            "question_answer_pairs": [
                {
                    "id": 1,
                    "query_index": 0,
                    "question": "What is the purpose of this database system?",
                    "answer": "The database system is designed to store question and answer pairs generated during ultra-deep research sessions. It allows for efficient storage, retrieval, and analysis of research data with metadata tracking.",
                    "metadata": {
                        "question_length": 62,
                        "answer_length": 189,
                        "tokens_used": 45,
                        "created_at": "2025-01-15 10:00:00"
                    }
                },
                {
                    "id": 2,
                    "query_index": 1,
                    "question": "How does the database store research sessions?",
                    "answer": "Research sessions are stored in a dedicated table with metadata including topic, creation date, query statistics, and token usage. Each session can contain multiple question-answer pairs linked via foreign key relationships.",
                    "metadata": {
                        "question_length": 58,
                        "answer_length": 156,
                        "tokens_used": 38,
                        "created_at": "2025-01-15 10:00:05"
                    }
                },
                {
                    "id": 3,
                    "query_index": 2,
                    "question": "What search capabilities are available?",
                    "answer": "The database supports full-text searching across questions and answers, session-based filtering, and statistical analysis. It also includes JSON export functionality and comprehensive metrics reporting.",
                    "metadata": {
                        "question_length": 57,
                        "answer_length": 138,
                        "tokens_used": 33,
                        "created_at": "2025-01-15 10:00:10"
                    }
                }
            ]
        }
        
        with open('sample_qa_data.json', 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"{Fore.GREEN}Created sample data file: sample_qa_data.json{Style.RESET_ALL}")
    
    def test_json_import(self):
        """Test importing from the sample JSON file"""
        if os.path.exists('sample_qa_data.json'):
            print(f"{Fore.YELLOW}Testing JSON import...{Style.RESET_ALL}")
            result = self.importer.import_from_json_file('sample_qa_data.json')
            if 'session_id' in result:
                print(f"+ Successfully imported sample data (Session ID: {result['session_id']})")
            return result
        else:
            print(f"{Fore.YELLOW}Sample JSON file not found. Creating it first...{Style.RESET_ALL}")
            self.create_sample_json_data()
            return self.test_json_import()

def print_usage():
    """Print usage instructions"""
    print(f"{Fore.CYAN}Data Migration Tool Usage:{Style.RESET_ALL}")
    print("  python migrate_existing_data.py <command>")
    print("")
    print(f"{Fore.YELLOW}Commands:{Style.RESET_ALL}")
    print("  migrate       Migrate Q&A pairs from existing research report files")
    print("  sample-json   Create sample JSON data for testing")
    print("  test-json     Test JSON import with sample data")
    print("  clean         Clean up test data files")

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    migrator = DataMigrator()
    command = sys.argv[1]
    
    try:
        if command == "migrate":
            migrator.migrate_from_report_files()
        elif command == "sample-json":
            migrator.create_sample_json_data()
        elif command == "test-json":
            migrator.test_json_import()
        elif command == "clean":
            # Clean up test files
            if os.path.exists('sample_qa_data.json'):
                os.remove('sample_qa_data.json')
                print(f"{Fore.GREEN}Removed sample_qa_data.json{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
            print_usage()
            sys.exit(1)
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
