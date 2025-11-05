"""
Resume Gemini Batch Submissions Script

This script helps resume batch submissions after quota limits are resolved.
It tracks which batches have been successfully created and which need to be processed.

Usage:
    python resume_batch_submissions.py
"""

import json
import time
import os
from pathlib import Path

# Load progress file
progress_file = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper\batch_submission_progress.json")

with open(progress_file, 'r') as f:
    progress = json.load(f)

print("=" * 80)
print("GEMINI BATCH SUBMISSION PROGRESS REPORT")
print("=" * 80)
print(f"\nSubmission Date: {progress['submission_date']}")
print(f"Total Batches Requested: {progress['total_requested']}")
print(f"Total Batches Successfully Created: {progress['total_submitted']}")
print(f"\nBatches with Jobs Created: {len(progress['batches_successfully_created'])}")
print(f"Batches Uploaded (Pending Job Creation): {len(progress['batches_uploaded_pending_job_creation'])}")
print(f"Batches Not Yet Processed: {progress['batches_not_yet_processed']['count']}")

print("\n" + "=" * 80)
print("SUCCESSFULLY CREATED BATCH JOBS")
print("=" * 80)
print("\nBatch Job Names (for monitoring):")
for batch in progress['batches_successfully_created']:
    print(f"  Batch {batch['batch_number']:03d}: {batch['batch_name']}")

print("\n" + "=" * 80)
print("FILES UPLOADED (NEED JOB CREATION)")
print("=" * 80)
print("\nThese files are uploaded and ready. Create jobs when quota allows:")
for batch in progress['batches_uploaded_pending_job_creation']:
    print(f"  Batch {batch['batch_number']:03d}: {batch['file_uri']}")

print("\n" + "=" * 80)
print("ERROR SUMMARY")
print("=" * 80)
error = progress['error_summary']
print(f"\nError Type: {error['error_type']}")
print(f"Error Code: {error['error_code']}")
print(f"Message: {error['message']}")
print(f"Occurred at Batch: {error['occurred_at_batch']}")
print(f"\nRecommendation: {error['recommendation']}")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
for i, step in enumerate(progress['next_steps'], 1):
    print(f"{i}. {step}")

print("\n" + "=" * 80)
print("COMMANDS TO CREATE JOBS FOR UPLOADED FILES (36-50)")
print("=" * 80)
print("\nUse these with the Gemini MCP batch_create tool:")
for batch in progress['batches_uploaded_pending_job_creation']:
    print(f"""
mcp__gemini__batch_create:
  inputFileUri: {batch['file_uri']}
  model: gemini-2.5-flash
  displayName: refinement_batch_{batch['batch_number']:03d}
  outputLocation: c:\\Users\\VLARO\\dreamteam\\claude\\gemini_batch_results_proper
""")

print("\n" + "=" * 80)
print("MONITORING COMMANDS")
print("=" * 80)
print("\nTo check status of all submitted jobs:")
print("\nUse mcp__gemini__batch_get_status with each batch name listed above.")
print("\n" + "=" * 80)
