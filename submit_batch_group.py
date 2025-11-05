import json
from pathlib import Path
import time

# This script will help organize batch submissions
# We'll track each batch job for monitoring

output_dir = Path('gemini_batch_submissions')
results_dir = Path('gemini_batch_results')
results_dir.mkdir(exist_ok=True)

# Track submitted batches
batch_tracker = {
    'submission_start': time.strftime('%Y-%m-%d %H:%M:%S'),
    'batches': []
}

# Batch 1 already submitted
batch_tracker['batches'].append({
    'batch_number': 1,
    'batch_id': 'refinement_batch_001',
    'file_uri': 'https://generativelanguage.googleapis.com/v1beta/files/2xk9tzftmt6k',
    'job_name': 'batches/w2svtdivbn1nl6vdis6e9f5g7qbwurvrarim',
    'state': 'PENDING',
    'qa_count': 100,
    'submitted_at': '2025-11-02 14:19:05'
})

# Save tracker
tracker_file = results_dir / 'batch_tracker.json'
with open(tracker_file, 'w', encoding='utf-8') as f:
    json.dump(batch_tracker, f, indent=2, ensure_ascii=False)

print("Batch tracker initialized")
print(f"Batch 1 submitted: batches/w2svtdivbn1nl6vdis6e9f5g7qbwurvrarim")
print(f"\nNext: Submit batches 2-10 using the same process:")
print("1. batch_ingest_content")
print("2. upload_file (with mimeType='text/plain')")
print("3. batch_create")
print(f"\nTracker saved to: {tracker_file}")
