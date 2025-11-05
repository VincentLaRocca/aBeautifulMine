import json
from pathlib import Path

# Track the 4 batches we just submitted
submitted_batches = [
    {
        'batch_number': 1,
        'job_name': 'batches/w2svtdivbn1nl6vdis6e9f5g7qbwurvrarim',
        'file_uri': 'https://generativelanguage.googleapis.com/v1beta/files/2xk9tzftmt6k'
    },
    {
        'batch_number': 2,
        'job_name': 'batches/ng3ytqktnlxu3zcm0y5o36znp0485x6tl82n',
        'file_uri': 'https://generativelanguage.googleapis.com/v1beta/files/cs9ruq1g7s9f'
    },
    {
        'batch_number': 3,
        'job_name': 'batches/nygopfkw1hu6bgp5h594o262ah5u1r57s9wk',
        'file_uri': 'https://generativelanguage.googleapis.com/v1beta/files/z0ku9tqhk610'
    },
    {
        'batch_number': 4,
        'job_name': 'batches/idyn0sl56x4w3a1e1oh1wimah16ty7xvbw24',
        'file_uri': 'https://generativelanguage.googleapis.com/v1beta/files/ru6futy0ptlo'
    }
]

# Save progress
progress_file = Path('gemini_batch_results/submission_progress.json')
progress_file.parent.mkdir(exist_ok=True)

progress_data = {
    'submitted_count': 4,
    'total_batches': 196,
    'submitted_batches': submitted_batches,
    'next_batches': list(range(5, 11)),  # Batches 5-10 next
    'process': [
        '1. batch_ingest_content for batch_00X_content.txt',
        '2. upload_file with mimeType="text/plain" for batch_00X_content.jsonl',
        '3. batch_create with returned file URI'
    ]
}

with open(progress_file, 'w') as f:
    json.dump(progress_data, f, indent=2)

print("="*80)
print("SUBMISSION PROGRESS")
print("="*80)
print(f"Batches submitted: 4/196")
print(f"Next to submit: Batches 5-10 (6 more batches)")
print(f"\nSubmitted batch jobs:")
for batch in submitted_batches:
    print(f"  Batch {batch['batch_number']}: {batch['job_name']}")
print(f"\nProgress saved to: {progress_file}")
print("="*80)
