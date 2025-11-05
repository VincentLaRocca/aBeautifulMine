import os
import shutil
from pathlib import Path

droid_dir = Path(r'c:\Users\VLARO\dreamteam\claude\inbox\droid')
processed_dir = droid_dir / 'processed'

# Keep only the most recent export (075728)
keep_files = {
    'qa_pairs_rag_export_20251102_075728.json',
    'qa_pairs_rag_export_20251102_075728_flattened.json'
}

moved_count = 0
for file_path in droid_dir.glob('qa_pairs_rag_export_*.json'):
    if file_path.name not in keep_files:
        dest = processed_dir / file_path.name
        print(f"Moving {file_path.name}...")
        try:
            shutil.move(str(file_path), str(dest))
            moved_count += 1
        except Exception as e:
            print(f"  Error: {e}")

print(f"\nMoved {moved_count} files to processed/")
print(f"\nRemaining RAG export files in inbox/droid:")
remaining = list(droid_dir.glob('qa_pairs_rag_export_*.json'))
for f in remaining:
    print(f"  - {f.name}")
