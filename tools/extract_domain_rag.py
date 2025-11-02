"""
Universal RAG Database Extractor
Extracts topics from Droid's RAG database for ANY domain

Discovers multi-session aggregations and generates structured JSON
"""

import json
import os
from datetime import datetime


def load_rag_export(rag_file):
    """Load Droid's RAG export JSON"""
    print(f"Loading RAG export: {rag_file}")
    with open(rag_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ Loaded {len(data.get('sessions', []))} sessions\n")
    return data


def extract_topic_from_rag(rag_data, topic_config, domain="general"):
    """
    Extract single topic from RAG database

    Args:
        rag_data: Loaded RAG export data
        topic_config: Topic configuration dict with:
            - name: Topic name
            - rag_topics: List of RAG topic keywords to match
            - description: Optional description
        domain: Domain identifier

    Returns:
        dict: Extracted topic data with Q&A pairs
    """
    topic_name = topic_config['name']
    rag_topics = topic_config['rag_topics']

    print(f"\n{'='*60}")
    print(f"EXTRACTING: {topic_name}")
    print(f"Searching for: {', '.join(rag_topics)}")
    print(f"{'='*60}\n")

    qa_pairs = []
    matched_sessions = []

    # Search through all RAG sessions
    for session in rag_data.get('sessions', []):
        session_topic = session.get('topic', '')

        # Check if this session matches any of the RAG topics
        for rag_topic in rag_topics:
            if rag_topic.lower() in session_topic.lower():
                # Found a match!
                session_qa = session.get('qa_pairs', [])

                print(f"✅ Found session: {session_topic}")
                print(f"   Q&A pairs: {len(session_qa)}")

                matched_sessions.append({
                    'topic': session_topic,
                    'qa_count': len(session_qa),
                    'session_date': session.get('created_date', 'unknown')
                })

                # Extract Q&A pairs
                for qa in session_qa:
                    qa_pairs.append({
                        'pair_number': len(qa_pairs) + 1,
                        'question': qa.get('question', ''),
                        'answer': qa.get('answer', ''),
                        'topic': topic_name,
                        'source_session': session_topic,
                        'created_date': qa.get('created_date', datetime.now().isoformat())
                    })

                break  # Move to next session

    if not qa_pairs:
        print(f"⚠️  No matches found for {topic_name}\n")
        return None

    # Build result
    result = {
        'domain': domain,
        'topic': topic_name,
        'topic_slug': slugify(topic_name),
        'description': topic_config.get('description', ''),
        'extraction_source': 'rag_database',
        'matched_sessions': matched_sessions,
        'sessions_aggregated': len(matched_sessions),
        'total_pairs_extracted': len(qa_pairs),
        'qa_pairs': qa_pairs,
        'extracted_date': datetime.now().isoformat()
    }

    print(f"\n✅ EXTRACTED: {topic_name}")
    print(f"   Sessions: {len(matched_sessions)}")
    print(f"   Q&A Pairs: {len(qa_pairs)}")
    print(f"   Average: {len(qa_pairs) / len(matched_sessions):.1f} per session\n")

    return result


def extract_batch_from_rag(rag_file, topic_configs, domain="general", output_dir=None):
    """
    Extract multiple topics from RAG database

    Args:
        rag_file: Path to RAG export JSON
        topic_configs: List of topic configuration dicts
        domain: Domain identifier
        output_dir: Where to save extracted JSON files

    Returns:
        dict: Extraction summary
    """
    # Load RAG data
    rag_data = load_rag_export(rag_file)

    print(f"\n{'='*60}")
    print(f"BATCH RAG EXTRACTION")
    print(f"Topics to extract: {len(topic_configs)}")
    print(f"Domain: {domain}")
    print(f"{'='*60}\n")

    # Setup output directory
    if output_dir is None:
        output_dir = f"parsed_qa_data/{domain}"

    os.makedirs(output_dir, exist_ok=True)

    results = []
    successful = 0
    total_qa = 0

    # Extract each topic
    for topic_config in topic_configs:
        result = extract_topic_from_rag(rag_data, topic_config, domain)

        if result:
            # Save to JSON
            output_file = f"{output_dir}/{result['topic_slug']}_qa_pairs.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"   Saved: {output_file}\n")

            results.append({
                'topic': result['topic'],
                'qa_pairs': result['total_pairs_extracted'],
                'sessions': result['sessions_aggregated'],
                'file': output_file,
                'success': True
            })

            successful += 1
            total_qa += result['total_pairs_extracted']
        else:
            results.append({
                'topic': topic_config['name'],
                'qa_pairs': 0,
                'sessions': 0,
                'file': None,
                'success': False
            })

    # Summary
    print(f"\n{'='*60}")
    print(f"BATCH EXTRACTION COMPLETE")
    print(f"Topics Attempted: {len(topic_configs)}")
    print(f"Successful: {successful}")
    print(f"Not Found: {len(topic_configs) - successful}")
    print(f"Total Q&A Extracted: {total_qa}")
    print(f"Average: {total_qa / successful:.1f} per topic" if successful > 0 else "")
    print(f"{'='*60}\n")

    return {
        'topics_attempted': len(topic_configs),
        'successful': successful,
        'not_found': len(topic_configs) - successful,
        'total_qa_extracted': total_qa,
        'results': results
    }


def analyze_rag_database(rag_file):
    """
    Analyze RAG database to see what topics are available

    Args:
        rag_file: Path to RAG export JSON

    Returns:
        dict: Analysis summary
    """
    rag_data = load_rag_export(rag_file)
    sessions = rag_data.get('sessions', [])

    print(f"\n{'='*60}")
    print(f"RAG DATABASE ANALYSIS")
    print(f"{'='*60}\n")

    print(f"Total Sessions: {len(sessions)}")

    total_qa = sum(len(s.get('qa_pairs', [])) for s in sessions)
    print(f"Total Q&A Pairs: {total_qa:,}\n")

    print("Available Topics:")
    print("-" * 60)

    topic_summary = []
    for i, session in enumerate(sessions, 1):
        topic = session.get('topic', 'Unknown')
        qa_count = len(session.get('qa_pairs', []))
        created = session.get('created_date', 'Unknown')

        print(f"{i:3d}. {topic}")
        print(f"     Q&A: {qa_count}, Created: {created[:10] if len(created) > 10 else created}")

        topic_summary.append({
            'topic': topic,
            'qa_count': qa_count,
            'created_date': created
        })

    print(f"\n{'='*60}\n")

    return {
        'total_sessions': len(sessions),
        'total_qa_pairs': total_qa,
        'topics': topic_summary
    }


def find_multi_session_topics(rag_file):
    """
    Find topics that appear in multiple sessions (multi-session aggregation)

    Args:
        rag_file: Path to RAG export JSON

    Returns:
        dict: Topics with multiple sessions
    """
    rag_data = load_rag_export(rag_file)
    sessions = rag_data.get('sessions', [])

    print(f"\n{'='*60}")
    print(f"MULTI-SESSION TOPIC ANALYSIS")
    print(f"{'='*60}\n")

    # Group sessions by similar topic names
    topic_groups = {}

    for session in sessions:
        topic = session.get('topic', '')

        # Normalize topic name (remove dates, special chars)
        normalized = normalize_topic_name(topic)

        if normalized not in topic_groups:
            topic_groups[normalized] = []

        topic_groups[normalized].append({
            'original_topic': topic,
            'qa_count': len(session.get('qa_pairs', [])),
            'created_date': session.get('created_date', 'Unknown')
        })

    # Find topics with multiple sessions
    multi_session_topics = {
        k: v for k, v in topic_groups.items()
        if len(v) > 1
    }

    print(f"Topics with multiple sessions: {len(multi_session_topics)}\n")

    for topic, sessions in multi_session_topics.items():
        total_qa = sum(s['qa_count'] for s in sessions)
        print(f"📊 {topic}")
        print(f"   Sessions: {len(sessions)}")
        print(f"   Total Q&A: {total_qa}")
        for s in sessions:
            print(f"   - {s['original_topic']}: {s['qa_count']} Q&A")
        print()

    print(f"{'='*60}\n")

    return multi_session_topics


def normalize_topic_name(topic):
    """Normalize topic name for grouping"""
    import re

    # Remove dates, parentheses, special characters
    normalized = re.sub(r'\d{4}-\d{2}-\d{2}', '', topic)
    normalized = re.sub(r'[(),\[\]]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = normalized.strip().lower()

    return normalized


def slugify(text):
    """Convert text to URL-friendly slug"""
    import re

    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    return text


# CLI Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Analyze:        python extract_domain_rag.py --analyze <rag_file>")
        print("  Multi-session:  python extract_domain_rag.py --multi <rag_file>")
        print("  Extract batch:  python extract_domain_rag.py --extract <rag_file> <topics.json> [domain]")
        print("\nExamples:")
        print("  python extract_domain_rag.py --analyze qa_pairs_rag_export_20241102.json")
        print("  python extract_domain_rag.py --multi qa_pairs_rag_export_20241102.json")
        print("  python extract_domain_rag.py --extract rag.json web_dev_topics.json web_development")
        sys.exit(1)

    command = sys.argv[1]

    if command == "--analyze":
        rag_file = sys.argv[2]
        analyze_rag_database(rag_file)

    elif command == "--multi":
        rag_file = sys.argv[2]
        find_multi_session_topics(rag_file)

    elif command == "--extract":
        rag_file = sys.argv[2]
        topics_file = sys.argv[3]
        domain = sys.argv[4] if len(sys.argv) > 4 else "general"

        with open(topics_file, 'r', encoding='utf-8') as f:
            topic_configs = json.load(f)

        extract_batch_from_rag(rag_file, topic_configs, domain)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
