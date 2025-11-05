#!/usr/bin/env python3
import sqlite3
import json

db_path = r"C:\Users\vlaro\dreamteam\claude\AgentOLD_DB_AND_DATA\Droid\ultra_deep_research\data\research_qa.db"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Total sessions
    cursor.execute("SELECT COUNT(*) FROM research_sessions")
    total_sessions = cursor.fetchone()[0]

    # Total QA pairs
    cursor.execute("SELECT COUNT(*) FROM question_answer_pairs")
    total_pairs = cursor.fetchone()[0]

    # Average lengths
    cursor.execute("SELECT AVG(question_length), AVG(answer_length) FROM question_answer_pairs")
    avg_q_len, avg_a_len = cursor.fetchone()

    # Total tokens
    cursor.execute("SELECT SUM(tokens_used) FROM question_answer_pairs")
    total_tokens = cursor.fetchone()[0] or 0

    # Sample Q&A
    cursor.execute("""
        SELECT q.question, q.answer, r.topic
        FROM question_answer_pairs q
        JOIN research_sessions r ON q.session_id = r.id
        LIMIT 3
    """)
    samples = cursor.fetchall()

    # Top topics
    cursor.execute("""
        SELECT r.topic, COUNT(q.id) as pair_count
        FROM research_sessions r
        LEFT JOIN question_answer_pairs q ON r.id = q.session_id
        GROUP BY r.id, r.topic
        ORDER BY pair_count DESC
        LIMIT 10
    """)
    top_topics = cursor.fetchall()

    print(f"=== OLD DATABASE STATISTICS ===")
    print(f"Total Sessions: {total_sessions}")
    print(f"Total Q&A Pairs: {total_pairs}")
    print(f"Average Question Length: {avg_q_len:.1f} chars")
    print(f"Average Answer Length: {avg_a_len:.1f} chars")
    print(f"Total Tokens Used: {total_tokens:,}")
    print()
    print("=== TOP 10 TOPICS ===")
    for topic, count in top_topics:
        print(f"  {topic}: {count} pairs")
    print()
    print("=== SAMPLE Q&A ===")
    for i, (q, a, topic) in enumerate(samples, 1):
        print(f"\nSample {i} - Topic: {topic}")
        print(f"Q: {q[:150]}...")
        print(f"A: {a[:200]}...")
