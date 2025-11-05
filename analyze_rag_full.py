import json
from collections import defaultdict

# Load the most recent RAG export
file_path = r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print metadata
print("="*80)
print("METADATA")
print("="*80)
for key, value in data['metadata'].items():
    if isinstance(value, (int, float, str)):
        print(f"{key}: {value}")
    elif isinstance(value, list) and len(value) <= 10:
        print(f"{key}:")
        for item in value:
            print(f"  - {item}")

# Analyze sessions
print("\n" + "="*80)
print("SESSION ANALYSIS")
print("="*80)

sessions = data['sessions']
print(f"Total sessions: {len(sessions)}")

# Count Q&A pairs by topic/indicator
topic_counts = defaultdict(int)
total_qa_pairs = 0

for session in sessions:
    topic = session.get('topic', 'Unknown')
    qa_count = len(session.get('qa_pairs', []))
    topic_counts[topic] += qa_count
    total_qa_pairs += qa_count

print(f"Total Q&A pairs across all sessions: {total_qa_pairs}")

print("\n" + "="*80)
print("TOP 30 TOPICS BY Q&A PAIR COUNT")
print("="*80)
sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
for topic, count in sorted_topics[:30]:
    print(f"{count:4d} pairs - {topic}")

print("\n" + "="*80)
print("ALL TOPICS (sorted alphabetically)")
print("="*80)
for topic, count in sorted(topic_counts.items()):
    print(f"{count:4d} pairs - {topic}")
