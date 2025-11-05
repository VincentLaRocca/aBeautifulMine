"""
Automated batch submission script using Gemini MCP
Processes batches 56-204 (remaining 149 batches)
"""

import json
from pathlib import Path

# Already submitted: 51-55 (5 batches)
SUBMITTED = {
    51: {"file_uri": "https://generativelanguage.googleapis.com/v1beta/files/4a3686ru8h6q",
         "batch_job": "batches/ej8mfplrwj9lhg9i1k0fibc1m5qhnxaqlmeq"},
    52: {"file_uri": "https://generativelanguage.googleapis.com/v1beta/files/9sdrq6oprp7u",
         "batch_job": "batches/stgtetixp5xxw0nzm5uv4n7tjgpftfl27nbw"},
    53: {"file_uri": "https://generativelanguage.googleapis.com/v1beta/files/5dg7i34r902r",
         "batch_job": "batches/ci3inwvjsfr1ji925xcz2yly0po6hr1jfjnu"},
    54: {"file_uri": "https://generativelanguage.googleapis.com/v1beta/files/m79wu6d7jx95",
         "batch_job": "batches/g0nyg6kct41eudmjcuvhvu1j9vshgd7khkro"},
    55: {"file_uri": "https://generativelanguage.googleapis.com/v1beta/files/2zlc4th2cjas",
         "batch_job": "batches/3sm5rg8t2acxfsviyrwtkrtxtzavxke7hlj9"}
}

BATCH_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_submissions_proper")
OUTPUT_DIR = Path(r"c:\Users\VLARO\dreamteam\claude\gemini_batch_results_proper")
START_BATCH = 56
END_BATCH = 204

def generate_batch_list():
    """Generate list of batches to process"""
    batches = []
    for batch_num in range(START_BATCH, END_BATCH + 1):
        batch_file = BATCH_DIR / f"batch_{batch_num:03d}_proper.jsonl"
        if batch_file.exists():
            batches.append({
                "batch_num": batch_num,
                "file_path": str(batch_file),
                "display_name": f"refinement_batch_{batch_num:03d}"
            })
        else:
            print(f"WARNING: Missing {batch_file}")
    return batches

def main():
    batches = generate_batch_list()
    print(f"Total batches to process: {len(batches)}")
    print(f"Range: {START_BATCH} to {END_BATCH}")
    print(f"Already submitted: {len(SUBMITTED)} batches (51-55)")
    print(f"\nReady to process batches {START_BATCH}-{END_BATCH}")

    # Save batch list for reference
    output_file = Path(r"C:\Users\vlaro\dreamteam\claude\batches_to_process.json")
    with open(output_file, 'w') as f:
        json.dump({
            "already_submitted": SUBMITTED,
            "to_process": batches,
            "total_remaining": len(batches)
        }, f, indent=2)

    print(f"\nBatch list saved to: {output_file}")

if __name__ == "__main__":
    main()
