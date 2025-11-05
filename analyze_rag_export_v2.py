import json

# Load the most recent RAG export
file_path = r'c:\Users\VLARO\dreamteam\claude\inbox\droid\qa_pairs_rag_export_20251102_075728.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Data type: {type(data)}")

if isinstance(data, dict):
    print(f"\nDict keys: {list(data.keys())}")
    print(f"Total keys: {len(data.keys())}")

    # Check first few items
    for i, (key, value) in enumerate(list(data.items())[:3]):
        print(f"\nKey {i}: {key}")
        print(f"Value type: {type(value)}")
        if isinstance(value, dict):
            print(f"Value keys: {list(value.keys())}")
        elif isinstance(value, list):
            print(f"List length: {len(value)}")
            if len(value) > 0:
                print(f"First item type: {type(value[0])}")
                if isinstance(value[0], dict):
                    print(f"First item keys: {list(value[0].keys())}")

elif isinstance(data, list):
    print(f"\nList length: {len(data)}")
    if len(data) > 0:
        print(f"First item type: {type(data[0])}")
        if isinstance(data[0], dict):
            print(f"First item keys: {list(data[0].keys())}")
else:
    print(f"Unexpected data type: {type(data)}")
