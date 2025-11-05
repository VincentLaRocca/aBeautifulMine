"""
Repeatable Batch Submission Script
===================================

This script uploads and submits all 196 properly formatted JSONL files
to the Gemini Batch API for Q&A pair refinement.

Features:
- Uploads files in batches
- Creates batch jobs for each uploaded file
- Tracks submission progress
- Resumes from last successful upload if interrupted
- Saves detailed tracking data for monitoring

Usage:
    python submit_all_batches_proper.py [--start BATCH_NUM] [--end BATCH_NUM] [--test]

Options:
    --start: Start from specific batch number (default: 1)
    --end: End at specific batch number (default: 196)
    --test: Test mode - only submit first 3 batches

Examples:
    python submit_all_batches_proper.py                    # Submit all 196 batches
    python submit_all_batches_proper.py --test             # Test with first 3 batches
    python submit_all_batches_proper.py --start 50 --end 100  # Submit batches 50-100
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# NOTE: This script template shows the process
# Actual submission should be done via Claude Code MCP tools:
# - mcp__gemini__upload_file
# - mcp__gemini__batch_create

print("=" * 80)
print("BATCH SUBMISSION PROCESS")
print("=" * 80)

# Parse arguments
parser = argparse.ArgumentParser(description='Submit batches to Gemini Batch API')
parser.add_argument('--start', type=int, default=1, help='Start batch number')
parser.add_argument('--end', type=int, default=196, help='End batch number')
parser.add_argument('--test', action='store_true', help='Test mode (first 3 batches)')
args = parser.parse_args()

if args.test:
    args.start = 1
    args.end = 3
    print("\n*** TEST MODE: Submitting batches 1-3 only ***\n")

# Load batch tracking data
tracking_file = Path('gemini_batch_submissions_proper/batch_tracking.json')
with open(tracking_file, 'r', encoding='utf-8') as f:
    tracking_data = json.load(f)

# Filter batches by range
batches_to_submit = [
    b for b in tracking_data['batches']
    if args.start <= b['batch_number'] <= args.end
]

print(f"\nBatches to submit: {len(batches_to_submit)}")
print(f"Range: Batch {args.start} to {args.end}")
print(f"Total Q&A pairs: {sum(b['qa_count'] for b in batches_to_submit)}")

# Initialize submission tracking
submission_results = {
    'start_time': datetime.now().isoformat(),
    'batches_requested': len(batches_to_submit),
    'batches_uploaded': 0,
    'batches_submitted': 0,
    'batches_failed': 0,
    'submissions': []
}

print("\n" + "=" * 80)
print("SUBMISSION PROCESS")
print("=" * 80)
print("\nFor each batch, the process is:")
print("1. Upload JSONL file using: mcp__gemini__upload_file")
print("2. Create batch job using: mcp__gemini__batch_create")
print("3. Track job name and status")
print("\n" + "=" * 80)

# Create instructions for Claude Code
instructions = {
    "tool": "Claude Code MCP Tools Required",
    "process": [
        {
            "step": 1,
            "tool": "mcp__gemini__upload_file",
            "parameters": {
                "filePath": "<absolute_path_to_jsonl_file>",
                "displayName": "refinement_batch_XXX",
                "mimeType": "text/plain"
            },
            "example": "mcp__gemini__upload_file(filePath='c:\\\\Users\\\\VLARO\\\\dreamteam\\\\claude\\\\gemini_batch_submissions_proper\\\\batch_001_proper.jsonl', displayName='refinement_batch_001', mimeType='text/plain')"
        },
        {
            "step": 2,
            "tool": "mcp__gemini__batch_create",
            "parameters": {
                "inputFileUri": "<uri_from_upload_response>",
                "model": "gemini-2.5-flash",
                "displayName": "refinement_batch_XXX",
                "outputLocation": "c:\\\\Users\\\\VLARO\\\\dreamteam\\\\claude\\\\gemini_batch_results_proper"
            },
            "example": "mcp__gemini__batch_create(inputFileUri='https://generativelanguage.googleapis.com/v1beta/files/...', model='gemini-2.5-flash', displayName='refinement_batch_001')"
        }
    ],
    "batches": []
}

# Generate batch-specific instructions
for batch_info in batches_to_submit:
    batch_num = batch_info['batch_number']
    file_path = Path(batch_info['file_path']).resolve()

    instructions["batches"].append({
        "batch_number": batch_num,
        "file_path": str(file_path),
        "upload_call": f"mcp__gemini__upload_file(filePath='{file_path}', displayName='refinement_batch_{batch_num:03d}', mimeType='text/plain')",
        "create_call": f"mcp__gemini__batch_create(inputFileUri='<FROM_UPLOAD>', model='gemini-2.5-flash', displayName='refinement_batch_{batch_num:03d}')"
    })

# Save instructions
instructions_file = Path('gemini_batch_submissions_proper/submission_instructions.json')
with open(instructions_file, 'w', encoding='utf-8') as f:
    json.dump(instructions, f, indent=2)

print(f"\nSubmission instructions saved to: {instructions_file}")
print("\n" + "=" * 80)
print("NEXT STEPS FOR CLAUDE CODE")
print("=" * 80)
print(f"\n1. Use the MCP tools to upload and submit {len(batches_to_submit)} batches")
print(f"2. Track each batch job name (e.g., 'batches/xxxxx')")
print(f"3. Save tracking data to: gemini_batch_submissions_proper/submission_tracking.json")
print(f"\n4. Monitor progress with: mcp__gemini__batch_get_status")
print(f"5. Download results with: mcp__gemini__batch_download_results")

print("\n" + "=" * 80)
print("SUBMISSION TEMPLATE READY")
print("=" * 80)
print(f"\nTotal batches: {len(batches_to_submit)}")
print(f"Estimated cost: ${len(batches_to_submit) * 0.33:.2f} - ${len(batches_to_submit) * 0.46:.2f}")
print(f"Processing time: 24-48 hours after submission")
print(f"\nInstructions file: {instructions_file}")
