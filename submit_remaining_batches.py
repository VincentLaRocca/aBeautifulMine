"""
Submit remaining batches 51-204 to Gemini Batch API
Processes batches sequentially with progress tracking
"""

import json
import time
import sys
from pathlib import Path

# Configuration
BATCH_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_submissions_proper")
OUTPUT_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper")
START_BATCH = 51
END_BATCH = 204
MODEL = "gemini-2.5-flash"

# Progress tracking
progress_file = Path(r"C:\Users\vlaro\dreamteam\claude\batch_submission_progress.json")
results_file = Path(r"C:\Users\vlaro\dreamteam\claude\batch_submission_results.json")

def load_progress():
    """Load existing progress"""
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {
        "submitted_batches": [],
        "failed_batches": [],
        "batch_jobs": {},
        "last_batch": 50
    }

def save_progress(progress):
    """Save progress to file"""
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)

def save_results(results):
    """Save final results"""
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

def main():
    progress = load_progress()

    print(f"Starting batch submission from batch {START_BATCH} to {END_BATCH}")
    print(f"Total batches to submit: {END_BATCH - START_BATCH + 1}")
    print(f"Already submitted: {len(progress['submitted_batches'])} batches")
    print(f"Last batch submitted: {progress['last_batch']}")
    print()

    # Determine starting point
    start_from = max(START_BATCH, progress['last_batch'] + 1)

    print(f"Resuming from batch {start_from}")
    print("=" * 80)

    for batch_num in range(start_from, END_BATCH + 1):
        batch_file = BATCH_DIR / f"batch_{batch_num:03d}_proper.jsonl"

        if not batch_file.exists():
            print(f"WARNING: Batch file not found: {batch_file}")
            progress['failed_batches'].append({
                "batch_num": batch_num,
                "error": "File not found"
            })
            continue

        print(f"\nProcessing batch {batch_num}/{END_BATCH}")
        print(f"File: {batch_file.name}")

        # This will be executed via MCP tools
        print(f"UPLOAD_FILE:{batch_file}")
        print(f"BATCH_NUM:{batch_num}")
        print(f"WAITING_FOR_MCP_UPLOAD")

        # Wait for upload completion signal
        # The actual upload will be done by Claude via MCP

        # Break after printing instructions for first batch
        # Claude will process them via MCP
        if batch_num == start_from:
            print("\n" + "=" * 80)
            print("INSTRUCTIONS PREPARED")
            print(f"Ready to process batches {start_from} to {END_BATCH}")
            print("=" * 80)
            break

if __name__ == "__main__":
    main()
