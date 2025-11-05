"""
Direct submission of all remaining batches 61-204 using Gemini API
This will be much faster than manual MCP calls
"""

import os
import json
import time
from pathlib import Path
import google.generativeai as genai

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BATCH_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_submissions_proper")
OUTPUT_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper")
TRACKING_FILE = Path(r"C:\Users\vlaro\dreamteam\claude\batch_submission_complete_tracking.json")

# Already submitted batches (51-60)
ALREADY_SUBMITTED = {
    51: "batches/ej8mfplrwj9lhg9i1k0fibc1m5qhnxaqlmeq",
    52: "batches/stgtetixp5xxw0nzm5uv4n7tjgpftfl27nbw",
    53: "batches/ci3inwvjsfr1ji925xcz2yly0po6hr1jfjnu",
    54: "batches/g0nyg6kct41eudmjcuvhvu1j9vshgd7khkro",
    55: "batches/3sm5rg8t2acxfsviyrwtkrtxtzavxke7hlj9",
    56: "batches/eyrbhb9p3mpo6wl6m22ueqx500lv22c1idlz",
    57: "batches/969rmcbvvmyg6a4cp892wezizoqv3lew7pg3",
    58: "batches/53ba0n5g9hyt4l1bp961xsgbxmmn8uwc5uvp",
    59: "batches/kdad6diwzrodvvf4v4fz43dqmlseysn57lkn",
    60: "batches/50sdth2luvh5pz21xgu1jrp2wnbf9inin294"
}

START_BATCH = 61
END_BATCH = 204
MODEL = "gemini-2.5-flash"

def load_tracking():
    """Load tracking data"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, 'r') as f:
            return json.load(f)
    return {
        "batches": {},
        "completed_count": 0,
        "target_count": 154,
        "errors": []
    }

def save_tracking(data):
    """Save tracking data"""
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def upload_and_create_batch(batch_num, tracking):
    """Upload file and create batch job"""
    batch_file = BATCH_DIR / f"batch_{batch_num:03d}_proper.jsonl"

    if not batch_file.exists():
        print(f"  ERROR: File not found: {batch_file}")
        tracking["errors"].append({
            "batch_num": batch_num,
            "error": "File not found"
        })
        return None

    try:
        # Upload file
        print(f"  Uploading {batch_file.name}...")
        uploaded_file = genai.upload_file(
            path=str(batch_file),
            display_name=f"batch_{batch_num:03d}_proper.jsonl",
            mime_type="application/json"
        )

        # Wait for file to be processed
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(0.5)
            uploaded_file = genai.get_file(uploaded_file.name)

        if uploaded_file.state.name != "ACTIVE":
            raise Exception(f"File upload failed: {uploaded_file.state.name}")

        print(f"  File uploaded: {uploaded_file.uri}")

        # Create batch job
        batch_job = genai.create_batch(
            input_file=uploaded_file,
            model=MODEL,
            display_name=f"refinement_batch_{batch_num:03d}"
        )

        print(f"  Batch created: {batch_job.name}")

        # Record in tracking
        tracking["batches"][str(batch_num)] = {
            "batch_num": batch_num,
            "file_path": str(batch_file),
            "file_uri": uploaded_file.uri,
            "batch_job_name": batch_job.name,
            "display_name": f"refinement_batch_{batch_num:03d}",
            "state": batch_job.state.name,
            "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        return batch_job.name

    except Exception as e:
        print(f"  ERROR: {e}")
        tracking["errors"].append({
            "batch_num": batch_num,
            "error": str(e)
        })
        return None

def main():
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        return

    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)

    # Load tracking
    tracking = load_tracking()

    # Add already submitted batches
    for batch_num, job_name in ALREADY_SUBMITTED.items():
        if str(batch_num) not in tracking["batches"]:
            tracking["batches"][str(batch_num)] = {
                "batch_num": batch_num,
                "batch_job_name": job_name,
                "display_name": f"refinement_batch_{batch_num:03d}",
                "state": "PENDING"
            }

    save_tracking(tracking)

    print(f"Starting batch submission")
    print(f"Already submitted: {len(ALREADY_SUBMITTED)} batches (51-60)")
    print(f"Processing: batches {START_BATCH}-{END_BATCH} ({END_BATCH - START_BATCH + 1} batches)")
    print("=" * 80)

    # Process remaining batches
    successful = 0
    failed = 0

    for batch_num in range(START_BATCH, END_BATCH + 1):
        print(f"\nBatch {batch_num}/{END_BATCH}")

        result = upload_and_create_batch(batch_num, tracking)

        if result:
            successful += 1
            tracking["completed_count"] = len(ALREADY_SUBMITTED) + successful
        else:
            failed += 1

        # Save progress periodically
        if batch_num % 10 == 0:
            save_tracking(tracking)
            print(f"\n--- Progress checkpoint: {successful} successful, {failed} failed ---")

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    # Final save
    save_tracking(tracking)

    print("\n" + "=" * 80)
    print("SUBMISSION COMPLETE")
    print(f"Already submitted: {len(ALREADY_SUBMITTED)}")
    print(f"New submissions: {successful}")
    print(f"Failed: {failed}")
    print(f"Total submitted: {len(ALREADY_SUBMITTED) + successful}/{END_BATCH}")
    print(f"\nTracking file: {TRACKING_FILE}")

if __name__ == "__main__":
    main()
