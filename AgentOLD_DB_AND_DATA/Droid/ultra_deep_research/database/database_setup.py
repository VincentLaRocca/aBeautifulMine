#!/usr/bin/env python3
"""
Database setup for storing question-answer pairs from research data.
"""

import sqlite3
import os
from typing import Dict, Any, List
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "data/research_qa.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.ensure_data_directory()
        self.init_database()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create research_sessions table to track research topics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS research_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_queries INTEGER DEFAULT 0,
                    successful_queries INTEGER DEFAULT 0,
                    tokens_used INTEGER DEFAULT 0
                )
            ''')
            
            # Create question_answer_pairs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS question_answer_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    query_index INTEGER,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    question_length INTEGER,
                    answer_length INTEGER,
                    tokens_used INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES research_sessions (id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON question_answer_pairs(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_question_length ON question_answer_pairs(question_length)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_answer_length ON question_answer_pairs(answer_length)')
            
            conn.commit()
    
    def create_research_session(self, topic: str, total_queries: int = 0, successful_queries: int = 0, tokens_used: int = 0) -> int:
        """Create a new research session and return its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO research_sessions (topic, total_queries, successful_queries, tokens_used)
                VALUES (?, ?, ?, ?)
            ''', (topic, total_queries, successful_queries, tokens_used))
            conn.commit()
            return cursor.lastrowid
    
    def store_question_answer_pairs(self, session_id: int, search_results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Store question-answer pairs for a research session"""
        stored_count = 0
        skipped_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for result in search_results:
                if result.get("success", False):
                    question = result.get("query", "")
                    answer = result.get("response", "")
                    query_index = result.get("index", 0)
                    
                    if question and answer:
                        question_length = len(question)
                        answer_length = len(answer)
                        tokens_used = result.get("tokens", {}).get("total_tokens", 0)
                        
                        cursor.execute('''
                            INSERT INTO question_answer_pairs 
                            (session_id, query_index, question, answer, question_length, answer_length, tokens_used)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (session_id, query_index, question, answer, question_length, answer_length, tokens_used))
                        stored_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            
            conn.commit()
        
        return {"stored": stored_count, "skipped": skipped_count}
    
    def update_session_stats(self, session_id: int, total_queries: int, successful_queries: int, tokens_used: int):
        """Update research session statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE research_sessions 
                SET total_queries = ?, successful_queries = ?, tokens_used = ?
                WHERE id = ?
            ''', (total_queries, successful_queries, tokens_used, session_id))
            conn.commit()
    
    def get_session_qa_pairs(self, session_id: int) -> List[Dict[str, Any]]:
        """Retrieve all question-answer pairs for a session"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM question_answer_pairs 
                WHERE session_id = ? 
                ORDER BY query_index
            ''', (session_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    import json
    
    def get_session_qa_pairs_json(self, session_id: int) -> str:
        """Retrieve question-answer pairs as JSON document"""
        qa_pairs = self.get_session_qa_pairs(session_id)
        
        # Format as structured JSON document
        json_data = {
            "session_id": session_id,
            "pairs_count": len(qa_pairs),
            "question_answer_pairs": []
        }
        
        for pair in qa_pairs:
            json_data["question_answer_pairs"].append({
                "id": pair["id"],
                "query_index": pair["query_index"],
                "question": pair["question"],
                "answer": pair["answer"],
                "metadata": {
                    "question_length": pair["question_length"],
                    "answer_length": pair["answer_length"],
                    "tokens_used": pair["tokens_used"],
                    "created_at": pair["created_at"]
                }
            })
        
        return json.dumps(json_data, indent=2)
    
    def get_sessions(self) -> List[Dict[str, Any]]:
        """Get all research sessions"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM research_sessions 
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def search_qa_pairs(self, query_text: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search question-answer pairs by text content"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            search_pattern = f"%{query_text}%"
            cursor.execute('''
                SELECT qa.*, r.topic 
                FROM question_answer_pairs qa
                JOIN research_sessions r ON qa.session_id = r.id
                WHERE qa.question LIKE ? OR qa.answer LIKE ?
                ORDER BY qa.created_at DESC
                LIMIT ?
            ''', (search_pattern, search_pattern, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total sessions
            cursor.execute("SELECT COUNT(*) FROM research_sessions")
            total_sessions = cursor.fetchone()[0]
            
            # Total QA pairs
            cursor.execute("SELECT COUNT(*) FROM question_answer_pairs")
            total_pairs = cursor.fetchone()[0]
            
            # Average answer length
            cursor.execute("SELECT AVG(answer_length) FROM question_answer_pairs")
            avg_answer_length = cursor.fetchone()[0] or 0
            
            # Total tokens
            cursor.execute("SELECT SUM(tokens_used) FROM question_answer_pairs")
            total_tokens = cursor.fetchone()[0] or 0
            
            # Sessions with most Q&A pairs
            cursor.execute('''
                SELECT r.topic, COUNT(qa.id) as pair_count
                FROM research_sessions r
                LEFT JOIN question_answer_pairs qa ON r.id = qa.session_id
                GROUP BY r.id, r.topic
                ORDER BY pair_count DESC
                LIMIT 5
            ''')
            top_sessions = cursor.fetchall()
            
            return {
                "total_sessions": total_sessions,
                "total_qa_pairs": total_pairs,
                "average_answer_length": round(avg_answer_length, 1),
                "total_tokens_used": total_tokens,
                "top_sessions": [{"topic": row[0], "pair_count": row[1]} for row in top_sessions]
            }

def init_database():
    """Initialize the database"""
    db = DatabaseManager()
    print("Database initialized successfully!")
    return db

if __name__ == "__main__":
    init_database()
