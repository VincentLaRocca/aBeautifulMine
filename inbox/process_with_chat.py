"""
Process Session 6 questions using individual chat API calls
This is the backup approach when batch processing encounters issues
"""
import json
import sys

# Read questions
with open('session-06-questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Prepare output structure
output = {
    "session": 6,
    "date": "2025-11-01",
    "indicators": [
        "Keltner Channels",
        "Donchian Channels",
        "Standard Deviation",
        "Historical Volatility",
        "Chaikin Volatility"
    ],
    "processing_method": "gemini_chat_api_individual_calls",
    "note": "Processed using chat API as backup when batch download encountered technical issues",
    "qa_pairs": []
}

print(f"Ready to process {len(questions)} questions")
print(f"\nIndicators: {', '.join(output['indicators'])}")
print(f"\nWill output questions in format for manual processing...")

# Output all prompts for processing
for idx, q in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"Question {idx}/30")
    print(f"Indicator: {q['indicator']}")
    print(f"Question: {q['question']}")
    print(f"{'='*80}")
    print(f"PROMPT: {q['prompt']}")
