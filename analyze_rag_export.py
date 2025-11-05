import json
from collections import defaultdict

# Load the most recent RAG export
file_path = r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Q&A pairs: {len(data)}")

if len(data) > 0:
    print(f"\nSample entry structure:")
    print(f"Keys: {list(data[0].keys())}")
    print(f"\nFirst entry:")
    for key, value in data[0].items():
        if isinstance(value, str) and len(value) > 100:
            print(f"  {key}: {value[:100]}...")
        else:
            print(f"  {key}: {value}")

# Count by session
sessions = defaultdict(int)
indicators = defaultdict(int)
categories = defaultdict(int)

for item in data:
    sess = item.get('session', 'unknown')
    ind = item.get('indicator', 'unknown')
    cat = item.get('category', 'unknown')

    sessions[sess] += 1
    indicators[ind] += 1
    categories[cat] += 1

print(f"\n{'='*60}")
print(f"Q&A pairs by session:")
print(f"{'='*60}")
for sess in sorted(sessions.keys()):
    print(f"  Session {sess}: {sessions[sess]} pairs")

print(f"\n{'='*60}")
print(f"Q&A pairs by indicator (top 20):")
print(f"{'='*60}")
sorted_indicators = sorted(indicators.items(), key=lambda x: x[1], reverse=True)
for ind, count in sorted_indicators[:20]:
    print(f"  {ind}: {count} pairs")

print(f"\n{'='*60}")
print(f"Q&A pairs by category:")
print(f"{'='*60}")
for cat in sorted(categories.keys()):
    print(f"  {cat}: {categories[cat]} pairs")

print(f"\n{'='*60}")
print(f"Total unique indicators: {len(indicators)}")
print(f"Total sessions: {len(sessions)}")
print(f"Total categories: {len(categories)}")
print(f"{'='*60}")
