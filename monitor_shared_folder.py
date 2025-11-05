#!/usr/bin/env python3
"""
Shared Folder Monitor for Dream Team
Monitors shared folder for new files and changes
"""

import os
import time
from pathlib import Path
from datetime import datetime
import json

SHARED_FOLDER = Path(r"C:\Users\vlaro\dreamteam\Gemini\shared")
STATE_FILE = Path(r"C:\Users\vlaro\dreamteam\claude\.shared_folder_state.json")

def load_state():
    """Load the last known state of files in shared folder"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Save current state of files"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def scan_folder():
    """Scan shared folder and return file metadata"""
    files = {}
    for file_path in SHARED_FOLDER.glob("*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.txt', '.json']:
            stat = file_path.stat()
            files[file_path.name] = {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'path': str(file_path)
            }
    return files

def detect_changes(old_state, new_state):
    """Detect new, modified, or deleted files"""
    changes = {
        'new': [],
        'modified': [],
        'deleted': []
    }

    # Find new and modified files
    for filename, metadata in new_state.items():
        if filename not in old_state:
            changes['new'].append({
                'file': filename,
                'path': metadata['path'],
                'size': metadata['size']
            })
        elif metadata['modified'] != old_state[filename]['modified']:
            changes['modified'].append({
                'file': filename,
                'path': metadata['path'],
                'size': metadata['size'],
                'old_time': old_state[filename]['modified'],
                'new_time': metadata['modified']
            })

    # Find deleted files
    for filename in old_state:
        if filename not in new_state:
            changes['deleted'].append({
                'file': filename
            })

    return changes

def format_changes_report(changes):
    """Format changes into a readable report"""
    report = []

    if changes['new']:
        report.append("[NEW FILES]")
        for item in changes['new']:
            report.append(f"   - {item['file']} ({item['size']} bytes)")

    if changes['modified']:
        report.append("\n[MODIFIED FILES]")
        for item in changes['modified']:
            old_dt = datetime.fromtimestamp(item['old_time']).strftime('%H:%M:%S')
            new_dt = datetime.fromtimestamp(item['new_time']).strftime('%H:%M:%S')
            report.append(f"   - {item['file']} (was {old_dt}, now {new_dt})")

    if changes['deleted']:
        report.append("\n[DELETED FILES]")
        for item in changes['deleted']:
            report.append(f"   - {item['file']}")

    return "\n".join(report) if report else "No changes detected."

def check_for_responses():
    """Check specifically for response files to Claude's questions"""
    responses = []

    # Look for Droid's response to batch7 question
    droid_response_patterns = [
        'droid-response-batch7-data.md',
        'droid-response-data-location.md',
        'droid-to-claude-batch7.md'
    ]

    for pattern in droid_response_patterns:
        file_path = SHARED_FOLDER / pattern
        if file_path.exists():
            responses.append({
                'from': 'Droid',
                'file': pattern,
                'path': str(file_path),
                'topic': 'Batch 7 Data Location'
            })

    # Look for Gemini's response to download issue
    gemini_response_patterns = [
        'gemini-response-download-issue.md',
        'gemini-to-claude-batch-download.md'
    ]

    for pattern in gemini_response_patterns:
        file_path = SHARED_FOLDER / pattern
        if file_path.exists():
            responses.append({
                'from': 'Gemini',
                'file': pattern,
                'path': str(file_path),
                'topic': 'Batch Download Issue'
            })

    return responses

def monitor_once():
    """Single check of the shared folder"""
    print("="*70)
    print(f"SHARED FOLDER MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    old_state = load_state()
    new_state = scan_folder()
    changes = detect_changes(old_state, new_state)

    # Print changes
    print(format_changes_report(changes))

    # Check for specific responses
    responses = check_for_responses()
    if responses:
        print("\n" + "="*70)
        print("[RESPONSES TO CLAUDE'S QUESTIONS]")
        print("="*70)
        for resp in responses:
            print(f"\n[RESPONSE] {resp['from']} responded!")
            print(f"   Topic: {resp['topic']}")
            print(f"   File: {resp['file']}")
            print(f"   Path: {resp['path']}")

    # Save new state
    save_state(new_state)

    # Summary
    total_files = len(new_state)
    total_changes = len(changes['new']) + len(changes['modified']) + len(changes['deleted'])

    print("\n" + "="*70)
    print(f"Summary: {total_files} files in shared folder, {total_changes} changes detected")
    print("="*70)

    return changes, responses

def monitor_continuous(interval=30):
    """Continuously monitor the shared folder"""
    print(f"Starting continuous monitoring (checking every {interval} seconds)")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            changes, responses = monitor_once()

            # If responses found, alert user
            if responses:
                print("\n[ACTION REQUIRED] New responses detected!")
                print("Check the files above for team communications.\n")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor_continuous(interval)
    else:
        monitor_once()
