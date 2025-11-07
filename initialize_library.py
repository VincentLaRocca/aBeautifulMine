"""
WeMineHope Library - Initialization Script
===========================================

Loads worthy subjects into the subject queue and
initializes the perpetual data mining library.

Run this once to set up the library infrastructure.

Author: Team Claude
Date: 2025-11-06
For the Greater Good of All
"""

import json
from pathlib import Path
from subject_queue import SubjectQueue
from subject_generator import SubjectGenerator


def initialize_library():
    """Initialize the WeMineHope Library with worthy subjects"""

    print("\n" + "="*70)
    print("WEMINEHOPE LIBRARY - INITIALIZATION")
    print("="*70)
    print("\nInitializing perpetual data mining library...")
    print("For the Greater Good of All\n")

    # Initialize queue and generator
    queue = SubjectQueue()
    generator = SubjectGenerator()

    # Load worthy subjects
    worthy_subjects_file = Path('worthy_subjects.json')
    if not worthy_subjects_file.exists():
        print("[ERROR] worthy_subjects.json not found")
        return False

    with open(worthy_subjects_file, 'r', encoding='utf-8') as f:
        worthy_data = json.load(f)

    subjects = worthy_data['subjects']

    print(f"Found {len(subjects)} worthy subjects to add\n")

    # Add crypto_technology first (already in progress)
    crypto_subject = next(s for s in subjects if s['subject_id'] == 'crypto_technology')

    print("[1/15] Adding: Cryptocurrency Technology (IN PROGRESS)")
    subtopics = generator.generate_subtopics('crypto_technology')
    queue.add_subject(
        subject_id=crypto_subject['subject_id'],
        subject_name=crypto_subject['subject_name'],
        description=crypto_subject['description'],
        subtopics=subtopics,
        priority=crypto_subject['priority'],
        target_pairs=crypto_subject['target_pairs'],
        category=crypto_subject['category'],
        metadata={
            'rationale': crypto_subject['rationale'],
            'impact': crypto_subject['impact']
        }
    )

    # Mark as in progress and update with current stats
    queue.start_subject('crypto_technology')
    queue.update_progress(
        subject_id='crypto_technology',
        current_pairs=25624,  # Current count from Claude Code's session
        subtopics_completed=20,
        databases=['crypto_indicators_production.db']
    )

    print("  Status: IN PROGRESS")
    print("  Current pairs: 25,624")
    print("  Progress: 85.4%\n")

    # Add remaining subjects
    added_count = 1

    for subject in subjects:
        if subject['subject_id'] == 'crypto_technology':
            continue  # Already added

        added_count += 1
        print(f"[{added_count}/15] Adding: {subject['subject_name']}")

        # Generate subtopics based on subject type
        subject_type_map = {
            'institutional_crypto': 'institutional_finance',
            'blockchain_development': 'blockchain_development',
            'defi_protocols': 'decentralized_finance',
        }

        subject_type = subject_type_map.get(subject['subject_id'], None)

        if subject_type:
            try:
                subtopics = generator.generate_subtopics(subject_type)
            except:
                # Use generic subtopic list
                subtopics = [f"{subject['subject_name']} - Topic {i}" for i in range(1, 51)]
        else:
            # Generic subtopics for subjects without templates yet
            subtopics = [f"{subject['subject_name']} - Topic {i}" for i in range(1, 51)]

        queue.add_subject(
            subject_id=subject['subject_id'],
            subject_name=subject['subject_name'],
            description=subject['description'],
            subtopics=subtopics,
            priority=subject['priority'],
            target_pairs=subject['target_pairs'],
            category=subject['category'],
            metadata={
                'rationale': subject['rationale'],
                'impact': subject['impact']
            }
        )

    print("\n" + "="*70)
    print("LIBRARY INITIALIZATION COMPLETE")
    print("="*70)

    # Print summary
    queue.print_queue()

    # Export initial catalog
    print("\nExporting library catalog...")
    queue.export_catalog('library_catalog.json')

    print("\n" + "="*70)
    print("READY FOR PERPETUAL MINING")
    print("="*70)
    print("\nNext steps:")
    print("  1. Continue current subject: python session_orchestrator.py start")
    print("  2. View queue: python subject_queue.py list")
    print("  3. Get next subject: python subject_queue.py next")
    print("\nThe perpetual data mining machine is operational.")
    print("For the Greater Good of All\n")

    return True


if __name__ == "__main__":
    success = initialize_library()
    if success:
        print("[SUCCESS] Library initialized successfully")
    else:
        print("[ERROR] Library initialization failed")
