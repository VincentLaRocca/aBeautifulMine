#!/usr/bin/env python3
"""
Export all Q&A pairs from database to JSON format suitable for RAG systems.
"""

import os
import sys
import json
from datetime import datetime
try:
    from .database.database_setup import DatabaseManager
except ImportError:
    from database.database_setup import DatabaseManager

def export_all_qa_pairs_to_json(output_file: str = None, chunk_size: int = 1000):
    """
    Export all Q&A pairs from database to JSON format optimized for RAG systems.
    
    Args:
        output_file: Output file path. If None, generates timestamped filename.
        chunk_size: Number of Q&A pairs per JSON array chunk for memory efficiency.
    
    Returns:
        str: Path to the created JSON file.
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
        output_file = f"qa_pairs_rag_export_{timestamp}.json"
    
    # Prepare RAG-optimized JSON structure
    rag_data = {
        "metadata": {
            "export_timestamp": datetime.now().isoformat(),
            "total_sessions": len(sessions),
            "format_version": "1.0",
            "description": "Q&A pairs optimized for RAG (Retrieval-Augmented Generation) systems",
            "source_database": "research_qa.db"
        },
        "sessions": []
    }
    
    # Get database statistics
    stats = db.get_statistics()
    rag_data["metadata"].update({
        "total_qa_pairs": stats['total_qa_pairs'],
        "total_tokens_used": stats['total_tokens_used'],
        "average_answer_length": stats['average_answer_length'],
        "top_sessions": stats['top_sessions']
    })
    
    # Process each session
    total_pairs_exported = 0
    
    for session in sessions:
        qa_pairs = db.get_session_qa_pairs(session['id'])
        
        if not qa_pairs:
            continue
        
        # Create session-level data for RAG
        session_data = {
            "session_id": session['id'],
            "topic": session['topic'],
            "created_at": session['created_at'],
            "total_queries": session['total_queries'],
            "successful_queries": session['successful_queries'],
            "tokens_used": session['tokens_used'],
            "qa_pairs": []
        }
        
        # Process each Q&A pair with RAG-optimized structure
        for pair in qa_pairs:
            # Create text content for vector indexing (combining question and answer)
            combined_text = f"Question: {pair['question']}\nAnswer: {pair['answer']}"
            
            # RAG-optimized document structure
            rag_document = {
                "id": f"{session['id']}_{pair['query_index']}",
                "content": combined_text,
                "question": pair['question'],
                "answer": pair['answer'],
                "metadata": {
                    "session_id": session['id'],
                    "topic": session['topic'],
                    "created_at": pair['created_at'],
                    "query_index": pair['query_index'],
                    "question_length": pair['question_length'],
                    "answer_length": pair['answer_length'],
                    "tokens_used": pair['tokens_used'],
                    "chunk_id": len(session_data["qa_pairs"]) + 1
                },
                # RAG-specific fields for better chunking and retrieval
                "rag_optimized": {
                    "text": combined_text,
                    "chunk_type": "question_answer_pair",
                    "source": "research_database",
                    "language": "english",
                    "word_count": len(combined_text.split()),
                    "char_count": len(combined_text)
                }
            }
            
            session_data["qa_pairs"].append(rag_document)
            total_pairs_exported += 1
        
        rag_data["sessions"].append(session_data)
        
        print(f"Processed session {session['id']}: {session['topic']} ({len(qa_pairs)} pairs)")
    
    # Write the complete JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rag_data, f, indent=2, ensure_ascii=False)
    
    # Also create a flattened version for simple RAG ingestion
    flattened_file = output_file.replace('.json', '_flattened.json')
    flattened_data = {
        "metadata": rag_data["metadata"],
        "documents": []
    }
    
    for session in rag_data["sessions"]:
        for pair in session["qa_pairs"]:
            flattened_data["documents"].append(pair)
    
    # Remove nested sessions info for flattened format
    flattened_data["metadata"]["total_documents"] = len(flattened_data["documents"])
    
    with open(flattened_file, 'w', encoding='utf-8') as f:
        json.dump(flattened_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {total_pairs_exported} Q&A pairs to {output_file}")
    print(f"Created flattened version for RAG ingestion: {flattened_file}")
    return output_file

def create_rag_ready_chunks(output_file: str = None, max_chunk_size: int = 4000):
    """
    Create RAG-ready chunks optimized for vector database ingestion.
    Each chunk contains meaningful units of text with proper metadata.
    
    Args:
        output_file: Base filename for output files
        max_chunk_size: Maximum characters per chunk
    
    Returns:
        dict: Paths to created files
    """
    # First export the full JSON
    main_json = export_all_qa_pairs_to_json(output_file)
    
    if not main_json:
        return {"error": "No data to export"}
    
    # Initialize database connection
    db = DatabaseManager()
    sessions = db.get_sessions()
    
    # Generate chunked files for better RAG performance
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_file:
        base_output = f"rag_chunks_{timestamp}"
    else:
        base_output = output_file.replace('.json', '')
    
    chunks_file = f"{base_output}_chunks.json"
    all_chunks = []
    chunk_id = 1
    
    # Process sessions and create chunks
    for session in sessions:
        qa_pairs = db.get_session_qa_pairs(session['id'])
        
        for pair in qa_pairs:
            # Split long answers into chunks if needed
            answer_text = pair['answer']
            
            if len(answer_text) <= max_chunk_size:
                # Use single chunk for the entire Q&A
                combined_text = f"Q: {pair['question']}\nA: {answer_text}"
                
                chunk = {
                    "id": f"chunk_{chunk_id:06d}",
                    "text": combined_text,
                    "metadata": {
                        "source": "research_database",
                        "session_id": session['id'],
                        "topic": session['topic'],
                        "qa_pair_id": pair['id'],
                        "query_index": pair['query_index'],
                        "chunk_type": "complete_qa",
                        "created_at": pair['created_at'],
                        "tokens_used": pair['tokens_used']
                    }
                }
                
                all_chunks.append(chunk)
                chunk_id += 1
            else:
                # Split long answers into multiple chunks
                combined_text = f"Q: {pair['question']}\nA: "
                
                # Start with question part
                chunk = {
                    "id": f"chunk_{chunk_id:06d}",
                    "text": combined_text,
                    "metadata": {
                        "source": "research_database",
                        "session_id": session['id'],
                        "topic": session['topic'],
                        "qa_pair_id": pair['id'],
                        "query_index": pair['query_index'],
                        "chunk_type": "question_only",
                        "created_at": pair['created_at'],
                        "tokens_used": pair['tokens_used']
                    }
                }
                
                all_chunks.append(chunk)
                chunk_id += 1
                
                # Split answer into overlapping chunks
                answer_sentences = answer_text.split('. ')
                current_chunk = combined_text
                
                for i, sentence in enumerate(answer_sentences):
                    if sentence.strip():
                        test_chunk = current_chunk + sentence + ". "
                        
                        if len(test_chunk) <= max_chunk_size:
                            current_chunk = test_chunk
                        else:
                            # Save current chunk and start new one
                            if current_chunk.strip():
                                chunk = {
                                    "id": f"chunk_{chunk_id:06d}",
                                    "text": current_chunk,
                                    "metadata": {
                                        "source": "research_database",
                                        "session_id": session['id'],
                                        "topic": session['topic'],
                                        "qa_pair_id": pair['id'],
                                        "query_index": pair['query_index'],
                                        "chunk_type": "answer_partial",
                                        "sentence_index": i,
                                        "created_at": pair['created_at'],
                                        "tokens_used": pair['tokens_used']
                                    }
                                }
                                
                                all_chunks.append(chunk)
                                chunk_id += 1
                            
                            # Start new chunk with overlap
                            overlap_text = sentence + ". "
                            if i < len(answer_sentences) - 1:
                                # Include some context from next sentence
                                next_sentence = answer_sentences[i + 1]
                                if len(overlap_text + next_sentence) <= max_chunk_size:
                                    overlap_text += next_sentence
                                    
                            current_chunk = overlap_text
                
                # Add the last chunk if there's remaining text
                if current_chunk.strip():
                    chunk = {
                        "id": f"chunk_{chunk_id:06d}",
                        "text": current_chunk,
                        "metadata": {
                            "source": "research_database",
                            "session_id": session['id'],
                            "topic": session['topic'],
                            "qa_pair_id": pair['id'],
                            "query_index": pair['query_index'],
                            "chunk_type": "answer_final",
                            "created_at": pair['created_at'],
                            "tokens_used": pair['tokens_used']
                        }
                    }
                    all_chunks.append(chunk)
                    chunk_id += 1
    
    # Save chunks to file
    chunks_data = {
        "metadata": {
            "export_timestamp": datetime.now().isoformat(),
            "total_chunks": len(all_chunks),
            "max_chunk_size": max_chunk_size,
            "format": "rag_ready_chunks",
            "description": "Pre-chunked documents optimized for vector database ingestion"
        },
        "chunks": all_chunks
    }
    
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(all_chunks)} RAG-ready chunks in {chunks_file}")
    
    return {
        "main_json": main_json,
        "flattened_json": main_json.replace('.json', '_flattened.json'),
        "chunks_json": chunks_file,
        "total_chunks": len(all_chunks)
    }

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export Q&A pairs to JSON format for RAG systems")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--chunks", action="store_true", 
                        help="Create RAG-ready chunks for vector database ingestion")
    parser.add_argument("--max-chunk-size", type=int, default=4000,
                        help="Maximum characters per chunk when using --chunks")
    
    args = parser.parse_args()
    
    try:
        if args.chunks:
            result = create_rag_ready_chunks(args.output, args.max_chunk_size)
            if "error" in result:
                print(f"Error: {result['error']}")
                sys.exit(1)
            else:
                print(f"RAG chunks export completed:")
                print(f"  Main JSON: {result['main_json']}")
                print(f"  Flattened JSON: {result['flattened_json']}")
                print(f"  Chunks JSON: {result['chunks_json']}")
                print(f"  Total chunks: {result['total_chunks']}")
        else:
            output_file = export_all_qa_pairs_to_json(args.output)
            if output_file:
                print(f"JSON export completed successfully: {output_file}")
                flattened_file = output_file.replace('.json', '_flattened.json')
                print(f"Flattened version for RAG: {flattened_file}")
            else:
                print("No Q&A pairs found in database")
                sys.exit(1)
    except Exception as e:
        print(f"Error during export: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
