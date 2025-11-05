import json
import sys

# Read the questions
with open('session-06-questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")
print("Ready to process with Gemini chat API")
print("\nFirst 3 questions:")
for i, q in enumerate(questions[:3]):
    print(f"{i+1}. [{q['indicator']}] {q['question']}")
