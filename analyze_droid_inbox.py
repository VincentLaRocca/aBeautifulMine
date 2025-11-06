import json
import glob

files = glob.glob('inbox/droid/*_qa_pairs.json')
total = 0
file_details = []

for f in files:
    with open(f, encoding='utf-8') as file:
        data = json.load(file)
        pairs = data.get('qa_pairs', [])
        total += len(pairs)
        file_details.append({
            'file': f.split('\\')[-1],
            'pairs': len(pairs)
        })

print(f'Total pairs in droid inbox: {total}')
print(f'Total files: {len(files)}')
if files:
    print(f'Average per file: {total/len(files):.1f}')

print('\nTop 10 files by pair count:')
for detail in sorted(file_details, key=lambda x: x['pairs'], reverse=True)[:10]:
    print(f"  {detail['file']}: {detail['pairs']} pairs")
