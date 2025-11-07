"""
WeMineHope Library - Subject Queue System
==========================================

Manages the infinite pipeline of subjects to mine into training data.

The final piece of the perpetual data machine:
1. Topic → Subtopics → Q&A Pairs → Database → NEXT TOPIC

Author: Team Claude
Date: 2025-11-06
For the Greater Good of All
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class SubjectQueue:
    """
    Manages the queue of subjects to mine into training data.

    Each subject becomes a complete database of Q&A pairs for AI training.
    The queue ensures perpetual mining across infinite domains.
    """

    def __init__(self, storage_path: str = 'subject_queue.json'):
        self.storage_path = Path(storage_path)
        self._ensure_storage()

    def _ensure_storage(self):
        """Create storage file if it doesn't exist"""
        if not self.storage_path.exists():
            initial_data = {
                "subjects": {},
                "completed": {},
                "library_stats": {
                    "total_subjects": 0,
                    "active_subjects": 0,
                    "completed_subjects": 0,
                    "total_databases": 0,
                    "total_qa_pairs": 0
                },
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }
            self._write_data(initial_data)

    def _read_data(self) -> Dict:
        """Read queue data from storage"""
        with open(self.storage_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_data(self, data: Dict):
        """Write queue data to storage"""
        data['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def add_subject(self,
                   subject_id: str,
                   subject_name: str,
                   description: str,
                   subtopics: List[str],
                   priority: int = 5,
                   target_pairs: int = 30000,
                   category: str = "General",
                   metadata: Optional[Dict] = None) -> bool:
        """
        Add a new subject to the queue

        Args:
            subject_id: Unique identifier (e.g., 'crypto_technology')
            subject_name: Display name (e.g., 'Cryptocurrency Technology')
            description: What this subject covers
            subtopics: List of subtopics to mine
            priority: Lower number = higher priority (1-10)
            target_pairs: Goal number of Q&A pairs
            category: Subject category for organization
            metadata: Additional metadata

        Returns:
            True if added successfully
        """
        data = self._read_data()

        if subject_id in data['subjects']:
            print(f"Subject '{subject_id}' already exists")
            return False

        subject = {
            "subject_id": subject_id,
            "subject_name": subject_name,
            "description": description,
            "category": category,
            "priority": priority,
            "status": "pending",
            "subtopics": subtopics,
            "subtopics_total": len(subtopics),
            "subtopics_completed": 0,
            "target_pairs": target_pairs,
            "current_pairs": 0,
            "databases": [],
            "created": datetime.now().isoformat(),
            "started": None,
            "completed": None,
            "metadata": metadata or {}
        }

        data['subjects'][subject_id] = subject
        data['library_stats']['total_subjects'] += 1
        self._write_data(data)

        print(f"[SUCCESS] Added subject: {subject_name}")
        print(f"  Priority: {priority}")
        print(f"  Subtopics: {len(subtopics)}")
        print(f"  Target pairs: {target_pairs:,}")

        return True

    def get_next_subject(self) -> Optional[Dict]:
        """
        Get the next subject to work on (highest priority pending)

        Returns:
            Subject dict or None if no pending subjects
        """
        data = self._read_data()

        # Filter pending subjects
        pending = [
            s for s in data['subjects'].values()
            if s['status'] == 'pending'
        ]

        if not pending:
            return None

        # Sort by priority (lower number = higher priority)
        pending.sort(key=lambda x: (x['priority'], x['created']))

        return pending[0]

    def start_subject(self, subject_id: str) -> bool:
        """Mark a subject as in progress"""
        data = self._read_data()

        if subject_id not in data['subjects']:
            print(f"Subject not found: {subject_id}")
            return False

        subject = data['subjects'][subject_id]

        if subject['status'] != 'pending':
            print(f"Subject not pending: {subject_id} (status: {subject['status']})")
            return False

        subject['status'] = 'in_progress'
        subject['started'] = datetime.now().isoformat()

        data['library_stats']['active_subjects'] += 1

        self._write_data(data)
        print(f"[STARTED] {subject['subject_name']}")

        return True

    def update_progress(self,
                       subject_id: str,
                       current_pairs: int,
                       subtopics_completed: int = None,
                       databases: List[str] = None):
        """Update subject progress"""
        data = self._read_data()

        if subject_id not in data['subjects']:
            return False

        subject = data['subjects'][subject_id]
        subject['current_pairs'] = current_pairs

        if subtopics_completed is not None:
            subject['subtopics_completed'] = subtopics_completed

        if databases is not None:
            subject['databases'] = databases

        # Calculate progress percentage
        progress = (current_pairs / subject['target_pairs']) * 100
        subject['progress_percentage'] = round(progress, 1)

        self._write_data(data)
        return True

    def complete_subject(self, subject_id: str, final_pairs: int) -> bool:
        """Mark subject as completed and move to library"""
        data = self._read_data()

        if subject_id not in data['subjects']:
            return False

        subject = data['subjects'][subject_id]
        subject['status'] = 'completed'
        subject['completed'] = datetime.now().isoformat()
        subject['current_pairs'] = final_pairs

        # Move to completed
        data['completed'][subject_id] = subject
        del data['subjects'][subject_id]

        # Update stats
        data['library_stats']['active_subjects'] -= 1
        data['library_stats']['completed_subjects'] += 1
        data['library_stats']['total_databases'] += len(subject['databases'])
        data['library_stats']['total_qa_pairs'] += final_pairs

        self._write_data(data)

        print(f"\n[COMPLETED] {subject['subject_name']}")
        print(f"  Final pairs: {final_pairs:,}")
        print(f"  Databases: {len(subject['databases'])}")
        print(f"  Progress: 100%")

        return True

    def list_subjects(self, status: str = None) -> List[Dict]:
        """
        List all subjects, optionally filtered by status

        Args:
            status: Filter by status (pending, in_progress, completed)

        Returns:
            List of subject dicts
        """
        data = self._read_data()

        subjects = list(data['subjects'].values())

        if status:
            subjects = [s for s in subjects if s['status'] == status]

        # Sort by priority
        subjects.sort(key=lambda x: (x['priority'], x['created']))

        return subjects

    def get_subject(self, subject_id: str) -> Optional[Dict]:
        """Get specific subject by ID"""
        data = self._read_data()

        if subject_id in data['subjects']:
            return data['subjects'][subject_id]

        if subject_id in data['completed']:
            return data['completed'][subject_id]

        return None

    def get_library_stats(self) -> Dict:
        """Get overall library statistics"""
        data = self._read_data()
        return data['library_stats']

    def print_queue(self):
        """Print formatted queue status"""
        data = self._read_data()

        print("\n" + "="*70)
        print("WEMINEHOPE LIBRARY - SUBJECT QUEUE")
        print("="*70)

        # Stats
        stats = data['library_stats']
        print(f"\nLibrary Statistics:")
        print(f"  Total subjects: {stats['total_subjects']}")
        print(f"  Active: {stats['active_subjects']}")
        print(f"  Completed: {stats['completed_subjects']}")
        print(f"  Total databases: {stats['total_databases']}")
        print(f"  Total Q&A pairs: {stats['total_qa_pairs']:,}")

        # Active subjects
        in_progress = [s for s in data['subjects'].values() if s['status'] == 'in_progress']
        if in_progress:
            print(f"\n{'='*70}")
            print("ACTIVE SUBJECTS")
            print("="*70)
            for subject in in_progress:
                progress = (subject['current_pairs'] / subject['target_pairs']) * 100
                print(f"\n[IN PROGRESS] {subject['subject_name']}")
                print(f"  Progress: {subject['current_pairs']:,} / {subject['target_pairs']:,} ({progress:.1f}%)")
                print(f"  Subtopics: {subject['subtopics_completed']} / {subject['subtopics_total']}")
                print(f"  Databases: {len(subject['databases'])}")

        # Pending subjects
        pending = [s for s in data['subjects'].values() if s['status'] == 'pending']
        if pending:
            print(f"\n{'='*70}")
            print("PENDING SUBJECTS (Priority Order)")
            print("="*70)
            pending.sort(key=lambda x: (x['priority'], x['created']))
            for i, subject in enumerate(pending, 1):
                print(f"\n{i}. [{subject['priority']}] {subject['subject_name']}")
                print(f"   {subject['description']}")
                print(f"   Subtopics: {subject['subtopics_total']} | Target: {subject['target_pairs']:,} pairs")

        # Completed subjects
        if data['completed']:
            print(f"\n{'='*70}")
            print("COMPLETED SUBJECTS")
            print("="*70)
            for subject in data['completed'].values():
                print(f"\n[COMPLETED] {subject['subject_name']}")
                print(f"  Final pairs: {subject['current_pairs']:,}")
                print(f"  Databases: {len(subject['databases'])}")

        print(f"\n{'='*70}\n")

    def export_catalog(self, output_path: str = 'library_catalog.json'):
        """Export library catalog for external use"""
        data = self._read_data()

        catalog = {
            "library_name": "WeMineHope Training Data Library",
            "description": "Perpetually mined Q&A training data across infinite subjects",
            "created": data['metadata']['created'],
            "last_updated": data['metadata']['last_updated'],
            "statistics": data['library_stats'],
            "subjects": []
        }

        # Add all subjects (active and completed)
        for subject in data['subjects'].values():
            catalog['subjects'].append({
                "id": subject['subject_id'],
                "name": subject['subject_name'],
                "description": subject['description'],
                "category": subject['category'],
                "status": subject['status'],
                "pairs": subject['current_pairs'],
                "target": subject['target_pairs'],
                "databases": subject['databases']
            })

        for subject in data['completed'].values():
            catalog['subjects'].append({
                "id": subject['subject_id'],
                "name": subject['subject_name'],
                "description": subject['description'],
                "category": subject['category'],
                "status": "completed",
                "pairs": subject['current_pairs'],
                "target": subject['target_pairs'],
                "databases": subject['databases']
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2)

        print(f"[SUCCESS] Library catalog exported to: {output_path}")


# CLI Interface
def main():
    import sys

    if len(sys.argv) < 2:
        print("WeMineHope Library - Subject Queue")
        print("\nUsage:")
        print("  python subject_queue.py list                    # List all subjects")
        print("  python subject_queue.py stats                   # Show statistics")
        print("  python subject_queue.py next                    # Get next subject")
        print("  python subject_queue.py export                  # Export catalog")
        return

    queue = SubjectQueue()
    command = sys.argv[1]

    if command == 'list':
        queue.print_queue()

    elif command == 'stats':
        stats = queue.get_library_stats()
        print("\nLibrary Statistics:")
        print(f"  Total subjects: {stats['total_subjects']}")
        print(f"  Active: {stats['active_subjects']}")
        print(f"  Completed: {stats['completed_subjects']}")
        print(f"  Total databases: {stats['total_databases']}")
        print(f"  Total Q&A pairs: {stats['total_qa_pairs']:,}")

    elif command == 'next':
        next_subject = queue.get_next_subject()
        if next_subject:
            print(f"\nNext subject to mine:")
            print(f"  Name: {next_subject['subject_name']}")
            print(f"  Priority: {next_subject['priority']}")
            print(f"  Subtopics: {next_subject['subtopics_total']}")
            print(f"  Target pairs: {next_subject['target_pairs']:,}")
        else:
            print("\nNo pending subjects in queue")

    elif command == 'export':
        queue.export_catalog()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
