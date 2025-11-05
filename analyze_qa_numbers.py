import re
from collections import Counter

with open(r'C:\Users\vlaro\dreamteam\session42_nft_metrics_part1_complete.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all Q numbers
pattern = r'Q(\d+):'
matches = re.findall(pattern, content)
nums = [int(m) for m in matches]

print(f"Total Q: marks found: {len(nums)}")
print(f"Unique numbers: {len(set(nums))}")
print(f"Range: {min(nums)} to {max(nums)}")

counts = Counter(nums)
dups = [(n, c) for n, c in counts.items() if c > 1]

print(f"\nDuplicate numbers: {len(dups)}")
if dups:
    print("First 20 duplicates (number: count):")
    for n, c in sorted(dups)[:20]:
        print(f"  Q{n}: appears {c} times")
