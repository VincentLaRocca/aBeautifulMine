import os
import json
import requests
from pathlib import Path

# Gemini API key from environment
API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set")
    exit(1)

# All 35 batch job names for Wave 1 (batches 170-204)
batch_jobs = [
    {'num': 170, 'name': 'batches/k71u9i0863mjc940k2r13owwxmw93l8but2i'},
    {'num': 171, 'name': 'batches/tymxmptayoj4wtjgatjy16b186ak6bzi9xin'},
    {'num': 172, 'name': 'batches/hspn9dlokicjhf93vsluduai4852ffv7fv8y'},
    {'num': 173, 'name': 'batches/b3on89h6zegji28u68fmmvtaexqjyfswh7re'},
    {'num': 174, 'name': 'batches/t3ulfsf8chef2mbu9os6gjlv3yb0uo8fh9ur'},
    {'num': 175, 'name': 'batches/s0zcszfhbhhsmmqnye3ty755eeqqvpdk8o33'},
    {'num': 176, 'name': 'batches/g0hj34prl3q782uv0351rf5p2x9671sioztu'},
    {'num': 177, 'name': 'batches/qz4nu5ogp0c8e8euewj1f2f9u7fescdmvshi'},
    {'num': 178, 'name': 'batches/lsf9wgo50m0p291h7ib9mapksfc8psp1rsf0'},
    {'num': 179, 'name': 'batches/yli7mx4hrb2vd0zhwcyqybi90zd0mstsg11b'},
    {'num': 180, 'name': 'batches/nkqqaiuff36g047u4z3txwnt6j5061myks0a'},
    {'num': 181, 'name': 'batches/met5iepzearpudzar5bwcwq2pu4gbrq42frx'},
    {'num': 182, 'name': 'batches/2dz7biudyaum8mkccsp3fk61emewutfke2lf'},
    {'num': 183, 'name': 'batches/0f6bdc78pcoo6w5c04qwxohmphlp32a6idi2'},
    {'num': 184, 'name': 'batches/iffvcs75nyh1op5nycvhkt1c4x6dybqts2dt'},
    {'num': 185, 'name': 'batches/obwuymbb7w79phnz92dttfqwixcv1gxbabgo'},
    {'num': 186, 'name': 'batches/bkddcux87s1fl1pejbwlsyai8knyjskaj3d3'},
    {'num': 187, 'name': 'batches/kk2b24nozbip6zvtbet2hkkhi9jc1w5yyj3l'},
    {'num': 188, 'name': 'batches/f77oigdkh4ogyapop0f03o0a076iyr7dvfja'},
    {'num': 189, 'name': 'batches/yuixzm42zlp8aymnwlz8x9494rda3bbdbgsp'},
    {'num': 190, 'name': 'batches/8sc4c80ei1iyfv6vuidpd0u3eb9ra14ojt8z'},
    {'num': 191, 'name': 'batches/c0e28b488a65xf92kjcadsankg0eu93biapr'},
    {'num': 192, 'name': 'batches/2jirjawu3lefi777b5dlmxo0hv7vhcccuf83'},
    {'num': 193, 'name': 'batches/ngoqgcpo7uo5achvcwwdahv6im1tx2zy3yvl'},
    {'num': 194, 'name': 'batches/sfar4yd19eestxbtzcfn4os0k4z3zu7y4xyv'},
    {'num': 195, 'name': 'batches/aih58qyhbjn2fof1c3bwcbie5eb7dle8jxev'},
    {'num': 196, 'name': 'batches/zlsjohc743snk5jxtjoelt7owmg3eld0d1ov'},
    {'num': 197, 'name': 'batches/m92xe67zw27hl2m7q7av31ezymc0eh5elnus'},
    {'num': 198, 'name': 'batches/pqv2csxhs8hktbs5kvwhfjmudzfb7w173lu5'},
    {'num': 199, 'name': 'batches/3toz7owafqkw2nsv204i8eaypmo45sx0mdk8'},
    {'num': 200, 'name': 'batches/sw2nwsd3yjolsclej2wksqmqpqyn6z3xaf7a'},
    {'num': 201, 'name': 'batches/rizky5jqc6i1nfd6o7q1lene78zgljypgl4c'},
    {'num': 202, 'name': 'batches/ar1a2itwb2k5kxx64yoye85gmzmy8z6nf7vh'},
    {'num': 203, 'name': 'batches/t9ue7wno2lxd7n5z03o7c4hxfmes2z6ajjgq'},
    {'num': 204, 'name': 'batches/xpsr9n9v7ihkhth6fi30jahvdpae8kgwbuue'},
]

output_dir = Path('gemini_batch_results_proper')
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("DOWNLOADING WAVE 1 BATCH RESULTS (Batches 170-204)")
print("=" * 80)

successful_downloads = 0
failed_downloads = 0
pending_batches = []

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
        failed_downloads += 1
        continue

    batch_data = response.json()

    # State is nested in metadata
    metadata = batch_data.get('metadata', {})
    state = metadata.get('state', 'UNKNOWN')

    print(f"  State: {state}")

    # Skip if not complete
    if state != 'BATCH_STATE_SUCCEEDED':
        print(f"  [PENDING] Batch not yet complete, skipping...")
        pending_batches.append(batch_num)
        continue

    # Check if there's an output file URI (in response.responsesFile)
    response_data = batch_data.get('response', {})
    output_uri = response_data.get('responsesFile')
    if not output_uri:
        print(f"  WARNING: No outputUri found in batch data")
        failed_downloads += 1
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
        failed_downloads += 1
        continue

    # Save the results
    output_file = output_dir / f"batch_{batch_num:03d}_results.jsonl"
    with open(output_file, 'wb') as f:
        f.write(download_response.content)

    print(f"  [SUCCESS] Saved to: {output_file}")

    # Parse and count results
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  Results: {len(lines)} responses")
        successful_downloads += 1
    except Exception as e:
        print(f"  WARNING: Could not parse results: {e}")

print("\n" + "=" * 80)
print("DOWNLOAD SUMMARY")
print("=" * 80)
print(f"Successful downloads: {successful_downloads}")
print(f"Failed downloads: {failed_downloads}")
print(f"Pending batches: {len(pending_batches)}")
if pending_batches:
    print(f"  Batch numbers: {pending_batches}")
print("=" * 80)
