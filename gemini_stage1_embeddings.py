#!/usr/bin/env python3
"""
Gemini Refinement Stage 1: Generate Embeddings
Created: 2025-11-02
Purpose: Generate embeddings for Session 1 Q&A pairs using Gemini

Process:
1. Export Session 1 Q&A pairs from database
2. Prepare for Gemini batch embeddings
3. Generate embeddings via Gemini MCP
4. Store embeddings back in database
"""

import sqlite3
import json
from datetime import datetime
import os

DB_NAME = "crypto_indicators_production.db"
OUTPUT_DIR = "gemini_refinement"

def export_session_1_for_embeddings():
    """Export Session 1 Q&A pairs in format ready for Gemini embeddings"""

    print("=" * 70)
    print("STAGE 1: PREPARE SESSION 1 DATA FOR EMBEDDINGS")
    print("=" * 70)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get Session 1 Q&A pairs with indicator context
    cursor.execute("""
        SELECT
            qa.qa_id,
            qa.indicator_id,
            i.indicator_name,
            i.indicator_slug,
            qa.pair_number,
            qa.question,
            qa.answer,
            qa.topic
        FROM qa_pairs qa
        JOIN indicators i ON qa.indicator_id = i.indicator_id
        WHERE i.session_number = 1
        ORDER BY qa.indicator_id, qa.pair_number
    """)

    rows = cursor.fetchall()
    print(f"\n[*] Found {len(rows)} Q&A pairs from Session 1")

    # Prepare for embeddings - create text content to embed
    embeddings_input = []

    for row in rows:
        qa_id, indicator_id, indicator_name, indicator_slug, pair_number, question, answer, topic = row

        # Create rich text for embedding (question + answer gives better semantic representation)
        embedding_text = f"INDICATOR: {indicator_name}\nQUESTION: {question}\nANSWER: {answer[:500]}..."

        embeddings_input.append({
            "qa_id": qa_id,
            "indicator_id": indicator_id,
            "indicator_name": indicator_name,
            "indicator_slug": indicator_slug,
            "pair_number": pair_number,
            "question": question,
            "answer": answer,
            "topic": topic,
            "embedding_text": embedding_text
        })

    # Save to JSON for Gemini batch processing
    output_file = f"{OUTPUT_DIR}/session_1_for_embeddings.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings_input, f, indent=2, ensure_ascii=False)

    print(f"[*] Exported to: {output_file}")

    # Also create JSONL format for Gemini batch embeddings
    jsonl_file = f"{OUTPUT_DIR}/session_1_embeddings_batch.jsonl"
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for item in embeddings_input:
            batch_request = {
                "key": f"qa_{item['qa_id']}",
                "request": {
                    "content": {
                        "parts": [{
                            "text": item['embedding_text']
                        }]
                    },
                    "taskType": "SEMANTIC_SIMILARITY"
                }
            }
            f.write(json.dumps(batch_request) + '\n')

    print(f"[*] Created batch JSONL: {jsonl_file}")

    # Create summary
    cursor.execute("""
        SELECT i.indicator_name, COUNT(*) as qa_count
        FROM qa_pairs qa
        JOIN indicators i ON qa.indicator_id = i.indicator_id
        WHERE i.session_number = 1
        GROUP BY i.indicator_id
        ORDER BY i.indicator_id
    """)

    print("\n" + "=" * 70)
    print("SESSION 1 BREAKDOWN")
    print("=" * 70)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} Q&A pairs")

    print("\n" + "=" * 70)
    print("NEXT STEPS - USE GEMINI MCP")
    print("=" * 70)
    print("\n1. Upload the JSONL file to Gemini:")
    print(f"   File: {jsonl_file}")
    print("\n2. Create embeddings batch job:")
    print("   Task Type: SEMANTIC_SIMILARITY")
    print("   Model: gemini-embedding-001")
    print("\n3. Wait for completion (~2 hours)")
    print("\n4. Download embeddings results")
    print("\n5. Run next script to process embeddings")
    print("=" * 70)

    conn.close()

    return output_file, jsonl_file

if __name__ == "__main__":
    export_session_1_for_embeddings()
