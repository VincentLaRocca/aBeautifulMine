import json
import os

# Read the questions JSON file
input_file = '/c/Users/vlaro/dreamteam/claude/inbox/session-06-questions.json'
output_file = '/c/Users/vlaro/dreamteam/claude/inbox/session-06-batch-requests.jsonl'

with open(input_file, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Convert to JSONL format with proper batch request structure
with open(output_file, 'w', encoding='utf-8') as f:
    for idx, item in enumerate(questions):
        batch_request = {
            "request": {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": item["prompt"]
                            }
                        ]
                    }
                ]
            },
            "metadata": {
                "key": f"q{idx+1:02d}",
                "indicator": item["indicator"],
                "question": item["question"]
            }
        }
        f.write(json.dumps(batch_request) + '\n')

print(f"Successfully converted {len(questions)} questions to JSONL format")
print(f"Output saved to: {output_file}")
