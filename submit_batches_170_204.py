#!/usr/bin/env python3
"""
Submit batches 170-204 to Gemini Batch API with rate limit handling.
"""
import subprocess
import json
import time
import os
from pathlib import Path

# Configuration
BATCH_SUBMISSION_DIR = r"C:\Users\VLARO\dreamteam\claude\gemini_batch_submissions_proper"
OUTPUT_DIR = r"C:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper"
RESULTS_FILE = r"C:\Users\VLARO\dreamteam\claude\batch_170_204_job_names.json"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def upload_file(file_path):
    """Upload a file to Gemini using mcp__gemini__upload_file."""
    try:
        result = subprocess.run(
            [
                "claude",
                "mcp", "call",
                "mcp__gemini__upload_file",
                json.dumps({"filePath": str(file_path)})
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"  Error uploading: {result.stderr}")
            return None

        # Parse the result
        output = result.stdout.strip()
        if output:
            data = json.loads(output)
            file_uri = data.get("fileUri") or data.get("uri")
            return file_uri
    except Exception as e:
        print(f"  Exception uploading: {e}")

    return None

def create_batch_job(file_uri, batch_num):
    """Create a batch job for the uploaded file."""
    try:
        batch_name = f"batch-{batch_num:03d}-crypto-qa"

        result = subprocess.run(
            [
                "claude",
                "mcp", "call",
                "mcp__gemini__batch_create",
                json.dumps({
                    "inputFileUri": file_uri,
                    "model": "gemini-2.5-flash",
                    "displayName": batch_name,
                    "outputLocation": OUTPUT_DIR
                })
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            error_msg = result.stderr
            # Check for rate limit error
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                return {"error": "rate_limit", "message": error_msg}
            print(f"  Error creating batch job: {error_msg}")
            return None

        # Parse the result
        output = result.stdout.strip()
        if output:
            data = json.loads(output)
            job_name = data.get("name") or data.get("displayName")
            return {"job_name": job_name, "batch_name": batch_name}
    except Exception as e:
        print(f"  Exception creating batch: {e}")

    return None

def submit_batch(batch_num):
    """Submit a single batch."""
    file_name = f"batch_{batch_num:03d}_proper.jsonl"
    file_path = Path(BATCH_SUBMISSION_DIR) / file_name

    if not file_path.exists():
        print(f"ERROR: Batch {batch_num} file not found: {file_path}")
        return None

    print(f"\n{'='*70}")
    print(f"Submitting Batch {batch_num}/{file_name}")
    print(f"{'='*70}")

    # Step 1: Upload file
    print(f"  [1/2] Uploading file...")
    file_uri = upload_file(file_path)
    if not file_uri:
        print(f"  FAILED to upload batch {batch_num}")
        return None
    print(f"  File uploaded: {file_uri}")

    # Step 2: Create batch job
    print(f"  [2/2] Creating batch job...")
    result = create_batch_job(file_uri, batch_num)

    if result is None:
        print(f"  FAILED to create batch job for {batch_num}")
        return None

    if isinstance(result, dict) and result.get("error") == "rate_limit":
        print(f"  RATE LIMIT HIT: {result['message']}")
        return {"error": "rate_limit", "batch": batch_num}

    job_name = result.get("job_name")
    batch_name = result.get("batch_name")
    print(f"  Batch job created: {batch_name}")
    print(f"  Job name: {job_name}")

    return {
        "batch_num": batch_num,
        "file_name": file_name,
        "job_name": job_name,
        "batch_name": batch_name,
        "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    """Main submission process."""
    print("\n" + "="*70)
    print("GEMINI BATCH API SUBMISSION: Batches 170-204")
    print("="*70)

    submitted_jobs = []
    failed_batches = []

    # Batches to submit
    batch_numbers = list(range(170, 205))  # 170-204 inclusive

    print(f"Total batches to submit: {len(batch_numbers)}")
    print(f"Batch numbers: {batch_numbers[0]}-{batch_numbers[-1]}")

    # Submit in groups of 10 with pauses
    group_size = 10
    pause_between_groups = 180  # 3 minutes

    for group_idx in range(0, len(batch_numbers), group_size):
        group = batch_numbers[group_idx:group_idx + group_size]
        group_num = (group_idx // group_size) + 1

        print(f"\n\n{'#'*70}")
        print(f"GROUP {group_num}: Batches {group[0]}-{group[-1]}")
        print(f"{'#'*70}")

        for batch_num in group:
            result = submit_batch(batch_num)

            if result is None:
                failed_batches.append(batch_num)
            elif isinstance(result, dict) and result.get("error") == "rate_limit":
                print(f"\n>>> RATE LIMIT HIT at batch {batch_num}")
                print(f">>> Waiting 180 seconds before retry...")
                time.sleep(180)

                # Retry this batch
                result = submit_batch(batch_num)
                if result is None:
                    failed_batches.append(batch_num)
                else:
                    submitted_jobs.append(result)
            else:
                submitted_jobs.append(result)

            # Small delay between submissions
            time.sleep(5)

        # Pause between groups
        if group_idx + group_size < len(batch_numbers):
            print(f"\n>>> Group {group_num} complete. Waiting {pause_between_groups}s before next group...")
            time.sleep(pause_between_groups)

    # Save results
    print("\n\n" + "="*70)
    print("SUBMISSION COMPLETE")
    print("="*70)

    summary = {
        "total_to_submit": len(batch_numbers),
        "successfully_submitted": len(submitted_jobs),
        "failed": len(failed_batches),
        "failed_batch_numbers": failed_batches,
        "submitted_jobs": submitted_jobs,
        "completion_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(RESULTS_FILE, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nTotal Submitted: {len(submitted_jobs)}/{len(batch_numbers)}")
    print(f"Success Rate: {(len(submitted_jobs)/len(batch_numbers)*100):.1f}%")

    if failed_batches:
        print(f"\nFailed Batches: {failed_batches}")
    else:
        print("\n✓ ALL BATCHES SUCCESSFULLY SUBMITTED!")

    print(f"\nResults saved to: {RESULTS_FILE}")

    # Print first few job names
    if submitted_jobs:
        print("\nFirst 5 submitted jobs:")
        for job in submitted_jobs[:5]:
            print(f"  - {job['batch_name']}: {job['job_name']}")

        if len(submitted_jobs) > 5:
            print(f"  ... and {len(submitted_jobs)-5} more")

    return len(submitted_jobs) == len(batch_numbers)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
