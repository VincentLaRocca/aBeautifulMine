"""
Universal Assignment Generator
Creates session-based research assignments for ANY domain

Reads domain configuration and generates structured assignments for Droid
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_domain_config(config_file):
    """Load domain configuration from JSON"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_session_assignments(config, output_dir=None):
    """
    Generate session assignments from domain config

    Args:
        config: Domain configuration dict or path to config file
        output_dir: Where to save assignments (default: inbox/droid/)

    Returns:
        list: Assignment file paths created
    """
    # Load config if path provided
    if isinstance(config, str):
        config = load_domain_config(config)

    domain_name = config['domain']['name']
    domain_id = config['domain']['id']
    sessions = config['sessions']

    print(f"\n{'='*60}")
    print(f"GENERATING ASSIGNMENTS: {domain_name}")
    print(f"Sessions: {len(sessions)}")
    print(f"{'='*60}\n")

    # Setup output directory
    if output_dir is None:
        output_dir = f"inbox/droid/{domain_id}"

    os.makedirs(output_dir, exist_ok=True)

    assignment_files = []

    # Generate assignment for each session
    for session in sessions:
        assignment_file = generate_session_assignment(
            session,
            domain_name,
            domain_id,
            output_dir
        )
        assignment_files.append(assignment_file)

    print(f"\n{'='*60}")
    print(f"ASSIGNMENTS GENERATED: {len(assignment_files)}")
    print(f"Output: {output_dir}/")
    print(f"{'='*60}\n")

    return assignment_files


def generate_session_assignment(session, domain_name, domain_id, output_dir):
    """Generate single session assignment"""
    session_num = session['session_number']
    category = session['category']
    subcategory = session.get('subcategory', '')
    topics = session['topics']

    filename = f"SESSION_{session_num}_{domain_id.upper()}.md"
    filepath = os.path.join(output_dir, filename)

    # Build assignment content
    content = f"""# {domain_name} Research Assignment - Session {session_num}

**Category:** {category}
**Subcategory:** {subcategory if subcategory else 'N/A'}
**Topics:** {len(topics)}
**Target:** {session.get('target_qa', 100)} Q&A pairs per topic
**Total Target:** {len(topics) * session.get('target_qa', 100)} Q&A pairs

---

## Instructions for Droid

Please conduct **Ultra Deep Research** on the following topics from the {domain_name} domain.

### Research Parameters
- **Depth:** 100 parallel queries per topic
- **Format:** Research report with Q&A pairs
- **Output:** research_report_[topic]_[date].txt
- **Also:** Export to RAG database for future extraction

---

## Topics to Research

"""

    # Add each topic with details
    for i, topic in enumerate(topics, 1):
        content += f"### {i}. {topic['name']}\n\n"

        if topic.get('description'):
            content += f"**Description:** {topic['description']}\n\n"

        if topic.get('focus_areas'):
            content += "**Focus Areas:**\n"
            for area in topic['focus_areas']:
                content += f"- {area}\n"
            content += "\n"

        if topic.get('example_questions'):
            content += "**Example Questions:**\n"
            for question in topic['example_questions']:
                content += f"- {question}\n"
            content += "\n"

        content += f"**Target:** {topic.get('target_qa', 100)} Q&A pairs\n"
        content += "\n---\n\n"

    # Add summary
    content += f"""## Summary

**Session:** {session_num}
**Category:** {category}
**Topics:** {len(topics)}
**Total Q&A Target:** {len(topics) * session.get('target_qa', 100)}

---

## Next Steps

1. ✅ Conduct Ultra Deep Research for each topic
2. ✅ Generate research_report_*.txt files
3. ✅ Export to RAG database
4. ✅ Notify when complete

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Domain:** {domain_name}
**Assignment ID:** SESSION_{session_num}_{domain_id.upper()}
"""

    # Write assignment file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Generated: {filename}")
    print(f"   Topics: {len(topics)}")
    print(f"   Target: {len(topics) * session.get('target_qa', 100)} Q&A pairs\n")

    return filepath


def generate_batch_assignment(topics, batch_name, domain_name, domain_id, output_dir=None):
    """
    Generate a custom batch assignment (for gap filling, etc.)

    Args:
        topics: List of topic dicts
        batch_name: Name for this batch
        domain_name: Domain name
        domain_id: Domain identifier
        output_dir: Where to save assignment

    Returns:
        str: Assignment file path
    """
    if output_dir is None:
        output_dir = f"inbox/droid/{domain_id}"

    os.makedirs(output_dir, exist_ok=True)

    filename = f"BATCH_{batch_name.upper()}_{domain_id.upper()}.md"
    filepath = os.path.join(output_dir, filename)

    content = f"""# {domain_name} Research Assignment - Batch {batch_name}

**Batch Type:** Custom Assignment
**Topics:** {len(topics)}
**Target:** 100 Q&A pairs per topic (default)
**Total Target:** {len(topics) * 100} Q&A pairs

---

## Instructions for Droid

Please conduct **Ultra Deep Research** on the following topics from the {domain_name} domain.

### Research Parameters
- **Depth:** 100 parallel queries per topic
- **Format:** Research report with Q&A pairs
- **Output:** research_report_[topic]_[date].txt
- **Also:** Export to RAG database for future extraction

---

## Topics to Research

"""

    # Add each topic
    for i, topic in enumerate(topics, 1):
        if isinstance(topic, str):
            # Simple string topic
            content += f"### {i}. {topic}\n\n"
            content += f"**Target:** 100 Q&A pairs\n\n---\n\n"
        else:
            # Full topic dict
            content += f"### {i}. {topic['name']}\n\n"
            if topic.get('description'):
                content += f"**Description:** {topic['description']}\n\n"
            if topic.get('focus_areas'):
                content += "**Focus Areas:**\n"
                for area in topic['focus_areas']:
                    content += f"- {area}\n"
                content += "\n"
            content += f"**Target:** {topic.get('target_qa', 100)} Q&A pairs\n\n---\n\n"

    content += f"""## Summary

**Batch:** {batch_name}
**Topics:** {len(topics)}
**Total Q&A Target:** {len(topics) * 100}

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Domain:** {domain_name}
**Assignment ID:** BATCH_{batch_name.upper()}_{domain_id.upper()}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Generated batch assignment: {filename}")
    print(f"   Topics: {len(topics)}")
    print(f"   Target: {len(topics) * 100} Q&A pairs\n")

    return filepath


def summarize_domain_config(config):
    """Print summary of domain configuration"""
    if isinstance(config, str):
        config = load_domain_config(config)

    domain = config['domain']
    sessions = config['sessions']

    total_topics = sum(len(s['topics']) for s in sessions)
    total_target = sum(len(s['topics']) * s.get('target_qa', 100) for s in sessions)

    print(f"\n{'='*60}")
    print(f"DOMAIN CONFIGURATION SUMMARY")
    print(f"{'='*60}")
    print(f"Domain: {domain['name']}")
    print(f"ID: {domain['id']}")
    print(f"Description: {domain.get('description', 'N/A')}")
    print(f"\nSessions: {len(sessions)}")
    print(f"Total Topics: {total_topics}")
    print(f"Total Q&A Target: {total_target:,}")
    print(f"\nSession Breakdown:")

    for session in sessions:
        topic_count = len(session['topics'])
        session_target = topic_count * session.get('target_qa', 100)
        print(f"  Session {session['session_number']}: {topic_count} topics, {session_target} Q&A")

    print(f"{'='*60}\n")


# CLI Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate all:  python generate_assignments.py <config.json>")
        print("  Summarize:     python generate_assignments.py --summary <config.json>")
        print("\nExamples:")
        print("  python generate_assignments.py config/web_development_config.json")
        print("  python generate_assignments.py --summary config/database_design_config.json")
        sys.exit(1)

    if sys.argv[1] == "--summary":
        config_file = sys.argv[2]
        config = load_domain_config(config_file)
        summarize_domain_config(config)
    else:
        config_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        config = load_domain_config(config_file)
        generate_session_assignments(config, output_dir)
