import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure proper encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def integrate_batch(json_file_path, db_file_path):
    """Integrate Q&A pairs from a JSON file into the fundamentals database."""

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    print(f"\nIntegrating data from {json_file_path} into {db_file_path}...\n")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    # Extract data from JSON
    indicator = batch_data.get('indicator', 'Unknown Topic')
    category = batch_data.get('category', 'Unknown Category')
    subcategory = batch_data.get('subcategory', 'Unknown Subcategory')
    total_questions = batch_data.get('total_questions', 0)
    answers = batch_data.get('answers', [])

    if not answers:
        print("No answers found in the JSON file. Aborting integration.")
        return

    # Create a new session
    session_date = datetime.now().strftime('%Y-%m-%d')
    executor = 'Gemini' # As Gemini is performing the integration
    session_notes = f"Integration of {indicator} batch from {Path(json_file_path).name}"

    # Get the next session number
    cursor.execute("SELECT IFNULL(MAX(session_number), 0) + 1 FROM sessions")
    next_session_number = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO sessions (
            session_number, session_date, category, subcategory,
            total_topics, total_qa_pairs, executor, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        next_session_number,
        session_date,
        category,
        subcategory,
        1, # Integrating one topic per batch
        total_questions,
        executor,
        'completed',
        session_notes
    ))
    session_id = cursor.lastrowid # Get the session_id of the newly inserted session
    print(f"✓ Created Session {next_session_number}: {category} - {subcategory}")

    # Create topic entry
    topic_slug = indicator.lower().replace(' ', '_').replace('(', '').replace(')', '')
    cursor.execute("SELECT topic_id FROM topics WHERE topic_slug = ?", (topic_slug,))
    existing_topic = cursor.fetchone()

    if existing_topic:
        topic_id = existing_topic[0]
        print(f"✓ Found existing Topic: {indicator} (ID: {topic_id})")
    else:
        cursor.execute('''
            INSERT INTO topics (
                topic_name, topic_slug, session_number, category, subcategory,
                description, total_qa_pairs, priority, topic_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            indicator,
            topic_slug,
            next_session_number, # Link to the newly created session
            category,
            subcategory,
            f"Q&A pairs for {indicator} topic.", # Generic description
            total_questions,
            'high', # Default to high priority for new topics
            'technology_concept' # Default type, can be refined later if needed
        ))
        topic_id = cursor.lastrowid
        print(f"✓ Created Topic: {indicator} (ID: {topic_id})")

    # Insert Q&A pairs
    print(f"\nInserting {len(answers)} Q&A pairs...")
    inserted_count = 0

    # --- FIX STARTS HERE ---
    # Calculate pair_number offset from filename
    part_number = 0
    try:
        # e.g., bitcoin_history_questions_part_1_answers.json -> 1
        filename = Path(json_file_path).name
        part_str = filename.split('_part_')[1].split('_')[0]
        part_number = int(part_str) - 1
    except (IndexError, ValueError):
        part_number = 0 # Default to 0 if parsing fails

    pair_number_offset = part_number * 100
    # --- FIX ENDS HERE ---


    for answer_obj in answers:
        question_num = answer_obj.get('question_number')
        # Apply offset to the question number
        if question_num is not None:
            question_num += pair_number_offset
        question = answer_obj.get('question')
        answer = answer_obj.get('answer')
        answer_length = len(answer) if answer else 0

        # These fields are not in the current JSON, so default them
        subtopic = subcategory # Using subcategory as subtopic for now
        created_date = session_date
        difficulty_level = 'medium'
        tags = f"{indicator.lower()}, {category.lower()}, {subcategory.lower()}"

        # Check for examples (simple check, can be improved)
        has_examples = 1 if answer and ('example' in answer.lower() or 'scenario' in answer.lower()) else 0

        cursor.execute('''
            INSERT INTO qa_pairs (
                topic_id, pair_number, question, answer, subtopic,
                created_date, topic_name, difficulty_level, tags,
                answer_length, has_examples, has_sources, crypto_specific, technology_focus
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            topic_id,
            question_num,
            question,
            answer,
            subtopic,
            created_date,
            indicator,
            difficulty_level,
            tags,
            answer_length,
            has_examples,
            0, # has_sources - not available in current JSON
            1, # crypto_specific - assumed for fundamentals
            1  # technology_focus - assumed for fundamentals
        ))
        inserted_count += 1

    print(f"✓ Inserted all {inserted_count} Q&A pairs")

    # Update batch metadata
    cursor.execute('''
        INSERT INTO batch_metadata (
            batch_name, category, subcategory, total_topics,
            total_qa_pairs, source, integrated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        f"Batch - {indicator}",
        category,
        subcategory,
        1,
        total_questions,
        json_file_path,
        datetime.now().isoformat()
    ))
    print("✓ Created batch metadata")

    conn.commit()
    conn.close()
    print(f"\n✅ Data from {json_file_path} integrated successfully!")

def main():
    if len(sys.argv) != 3:
        print("Usage: python integrate_fundamentals_batch.py <json_file_path> <db_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    db_file_path = sys.argv[2]

    integrate_batch(json_file_path, db_file_path)

if __name__ == '__main__':
    main()
