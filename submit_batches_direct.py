#!/usr/bin/env python3
"""
Submit batches 170-204 to Gemini Batch API using direct MCP calls.
This script will be executed in the Claude Code environment.
"""
import json
import os
from pathlib import Path

BATCH_SUBMISSION_DIR = r"C:\Users\VLARO\dreamteam\claude\gemini_batch_submissions_proper"
OUTPUT_DIR = r"C:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Verify batches exist
print("Verifying batches 170-204 exist...")
batch_numbers = list(range(170, 205))
for batch_num in batch_numbers:
    file_path = Path(BATCH_SUBMISSION_DIR) / f"batch_{batch_num:03d}_proper.jsonl"
    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
    else:
        # Check file size
        size = file_path.stat().st_size
        print(f"  Batch {batch_num}: OK ({size:,} bytes)")

print("\n" + "="*70)
print("Ready to submit 35 batches (170-204)")
print("="*70)
print("\nPreparing submission instructions for MCP tools...")

# Create submission manifest
manifest = {
    "total_batches": 35,
    "batch_range": "170-204",
    "batches": []
}

for batch_num in batch_numbers:
    file_path = str(Path(BATCH_SUBMISSION_DIR) / f"batch_{batch_num:03d}_proper.jsonl")
    manifest["batches"].append({
        "batch_num": batch_num,
        "file_path": file_path,
        "display_name": f"batch-{batch_num:03d}-crypto-qa"
    })

# Save manifest
manifest_file = r"C:\Users\VLARO\dreamteam\claude\batch_submission_manifest.json"
with open(manifest_file, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest saved to: {manifest_file}")
print(f"Total batches to submit: {len(manifest['batches'])}")
print("\nSample batches:")
for b in manifest['batches'][:3]:
    print(f"  - {b['display_name']}: {b['file_path']}")
print(f"  ...\n  - {manifest['batches'][-1]['display_name']}: {manifest['batches'][-1]['file_path']}")

print("\nREADY FOR SUBMISSION")
