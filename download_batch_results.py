import os
import json
import requests
from pathlib import Path

# Gemini API key from environment
API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set")
    exit(1)

# All 10 batch job names
batch_jobs = [
    {'num': 1, 'name': 'batches/w2svtdivbn1nl6vdis6e9f5g7qbwurvrarim'},
    {'num': 2, 'name': 'batches/ng3ytqktnlxu3zcm0y5o36znp0485x6tl82n'},
    {'num': 3, 'name': 'batches/nygopfkw1hu6bgp5h594o262ah5u1r57s9wk'},
    {'num': 4, 'name': 'batches/idyn0sl56x4w3a1e1oh1wimah16ty7xvbw24'},
    {'num': 5, 'name': 'batches/i5kozseab2dtmqkbvne77awqwd5fuxojx5fc'},
    {'num': 6, 'name': 'batches/5oaz0rwmd9qtjro2cnuszv5gs5wyg0yesko4'},
    {'num': 7, 'name': 'batches/xghx25jalld52o0bx8g5av09vwas029r0hct'},
    {'num': 8, 'name': 'batches/geve6txonnceqbcb30ok1nyt4l5ce7rzrike'},
    {'num': 9, 'name': 'batches/0zcp068v97ol9s6c5bc0mcbnp36ctkxl4ob9'},
    {'num': 10, 'name': 'batches/otnrf9zh9ovedv7po5v529m1im9wgesi34vb'},
]

output_dir = Path('gemini_batch_results')
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("DOWNLOADING BATCH RESULTS")
print("=" * 80)

for batch in batch_jobs:
    batch_name = batch['name']
    batch_num = batch['num']

    print(f"\nBatch {batch_num}: {batch_name}")

    # Get batch job details
    url = f"https://generativelanguage.googleapis.com/v1beta/{batch_name}"
    headers = {'x-goog-api-key': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"  ERROR: Failed to get batch details: {response.status_code}")
        print(f"  Response: {response.text}")
        continue

    batch_data = response.json()

    # Check if there's an output file URI
    output_uri = batch_data.get('outputUri')
    if not output_uri:
        print(f"  WARNING: No outputUri found in batch data")
        print(f"  Batch data: {json.dumps(batch_data, indent=2)}")
        continue

    print(f"  Output URI: {output_uri}")

    # Download the output file
    # The output URI is typically a file reference like "files/xyz"
    # We need to download it using the Files API
    if output_uri.startswith('https://'):
        download_url = output_uri
    else:
        # It's a file reference, construct the download URL
        download_url = f"https://generativelanguage.googleapis.com/v1beta/{output_uri}"

    print(f"  Downloading from: {download_url}")

    download_response = requests.get(download_url, headers=headers)

    if download_response.status_code != 200:
        print(f"  ERROR: Failed to download: {download_response.status_code}")
        print(f"  Response: {download_response.text}")
        continue

    # Save the results
    output_file = output_dir / f"batch_{batch_num:03d}_results.jsonl"
    with open(output_file, 'wb') as f:
        f.write(download_response.content)

    print(f"  ✅ Saved to: {output_file}")

    # Parse and count results
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  Results: {len(lines)} responses")
    except Exception as e:
        print(f"  WARNING: Could not parse results: {e}")

print("\n" + "=" * 80)
print("DOWNLOAD COMPLETE")
print("=" * 80)
