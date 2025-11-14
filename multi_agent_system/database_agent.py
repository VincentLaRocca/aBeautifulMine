"""
Database Agent
Step 5: Inserts Q&A pairs into RAG database (ChromaDB)
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from dotenv import load_dotenv

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

load_dotenv()


class DatabaseAgent:
    """
    Agent that inserts Q&A pairs into ChromaDB for RAG
    """

    def __init__(self, db_path: Optional[str] = None, collection_name: str = "qa_dataset"):
        """
        Initialize the database agent
        
        Args:
            db_path: Path to ChromaDB directory
            collection_name: Name of the collection
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("chromadb is not installed. Install with: pip install chromadb")
        
        self.db_path = db_path or os.getenv("CHROMADB_PATH", "chroma_db")
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"[DB] Connected to existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Q&A dataset for AI training"}
            )
            print(f"[DB] Created new collection: {collection_name}")

    def insert_qa_pairs(self, qa_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Insert Q&A pairs into the database
        
        Args:
            qa_pairs: List of Q&A pair dictionaries
            
        Returns:
            Dictionary with insertion stats
        """
        if not qa_pairs:
            return {
                "success": False,
                "error": "No Q&A pairs provided",
                "stats": {}
            }
        
        try:
            print(f"[DB] Inserting {len(qa_pairs)} Q&A pairs...")
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            # Get current count
            current_count = self.collection.count()
            
            for idx, qa_pair in enumerate(qa_pairs):
                # Create ID
                qa_id = f"qa_{current_count + idx + 1}_{qa_pair.get('subtopic', 'unknown').replace(' ', '_')}"
                
                # Create document text (question + answer)
                doc_text = f"Question: {qa_pair['question']}\n\nAnswer: {qa_pair['answer']}"
                
                # Create metadata
                metadata = {
                    "question": qa_pair["question"],
                    "answer": qa_pair["answer"][:500],  # First 500 chars for search
                    "topic": qa_pair.get("topic", "unknown"),
                    "subtopic": qa_pair.get("subtopic", "unknown"),
                    "answer_length": qa_pair.get("answer_length", len(qa_pair.get("answer", ""))),
                    "generated_at": qa_pair.get("generated_at", ""),
                    "type": "qa_pair"
                }
                
                ids.append(qa_id)
                documents.append(doc_text)
                metadatas.append(metadata)
            
            # Insert in batches (ChromaDB handles batching internally, but we can do it explicitly)
            batch_size = 100
            inserted = 0
            
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i+batch_size]
                batch_docs = documents[i:i+batch_size]
                batch_metas = metadatas[i:i+batch_size]
                
                self.collection.add(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas
                )
                inserted += len(batch_ids)
                print(f"  [BATCH] Inserted {inserted}/{len(ids)} pairs")
            
            # Get final count
            final_count = self.collection.count()
            
            stats = {
                "inserted": inserted,
                "total_in_db": final_count,
                "before_insert": current_count,
                "new_added": final_count - current_count
            }
            
            print(f"[OK] Inserted {inserted} pairs. Total in database: {final_count}")
            
            return {
                "success": True,
                "stats": stats
            }
            
        except Exception as e:
            print(f"[ERROR] Database insertion failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "stats": {}
            }

    def query_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query similar Q&A pairs (for testing/verification)
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar Q&A pairs
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            return []

