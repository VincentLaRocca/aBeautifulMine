#!/usr/bin/env python3
"""
Assemble complete Session 10 with all 30 Q&A pairs
Combines Droid's 2 completed indicators with Claude's 3 completed indicators
"""

import json

# Session 10 will include all 5 indicators with 30 total Q&A pairs

session_10 = {
    "session": 10,
    "date": "2025-11-01",
    "category": "On-Chain Indicators - Network Activity Metrics (Transaction Analysis)",
    "indicators": [
        "Transaction Count (Total)",
        "Transaction Count (Per Block)",
        "Transaction Count (Per Day)",
        "Transaction Volume (Total Value Transferred)",
        "Mean Transaction Value"
    ],
    "total_qa_pairs": 30,
    "qa_pairs": []
}

# Load existing incomplete Session 10 (has 12 Q&A pairs for first 2 indicators)
print("Loading Droid's incomplete Session 10...")
with open(r"C:\Users\vlaro\DreamTeam\Droid\outbox\claude\crypto-indicators-session-10-qa-FINAL.json", 'r', encoding='utf-8') as f:
    existing = json.load(f)

# Extract the 12 existing Q&A pairs (indicators 1-2)
session_10["qa_pairs"] = existing["qa_pairs"]

print(f"Loaded {len(session_10['qa_pairs'])} existing Q&A pairs from Droid")
print(f"Indicators covered: {existing['indicators']}")

# Note: The remaining 18 Q&A pairs (indicators 3-5) were generated via Gemini
# They will need to be manually added to complete the session

print("\n" + "="*60)
print("SESSION 10 STRUCTURE PREPARED")
print("="*60)
print(f"Total indicators: {len(session_10['indicators'])}")
print(f"Current Q&A pairs: {len(session_10['qa_pairs'])}")
print(f"Expected Q&A pairs: 30")
print(f"Missing Q&A pairs: {30 - len(session_10['qa_pairs'])}")

print("\nIndicators status:")
for i, ind in enumerate(session_10['indicators'], 1):
    # Count Q&A pairs for this indicator
    count = sum(1 for qa in session_10['qa_pairs'] if qa['indicator'] == ind)
    status = "✓ Complete" if count == 6 else f"✗ Incomplete ({count}/6)"
    print(f"  {i}. {ind}: {status}")

# Save the structure
output_path = r"C:\Users\vlaro\dreamteam\claude\session_10_structure.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(session_10, f, indent=2, ensure_ascii=False)

print(f"\nStructure saved to: {output_path}")
print("\nNext step: Add remaining 18 Q&A pairs from Gemini generations")
