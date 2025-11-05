#!/usr/bin/env python3

from pathlib import Path

def fix_file_extensions():
    """Fix missing .txt extensions in generated files"""
    
    crypto_questions_dir = Path("crypto_questions")
    
    if not crypto_questions_dir.exists():
        print("crypto_questions directory not found")
        return
    
    fixed_count = 0
    
    print("Fixing file extensions...")
    print("=" * 40)
    
    for file_path in crypto_questions_dir.iterdir():
        if file_path.is_file() and not file_path.name.endswith('.txt'):
            # This is a file that's missing the .txt extension
            new_name = file_path.name + '.txt'
            new_path = file_path.with_name(new_name)
            
            try:
                file_path.rename(new_path)
                print(f"Fixed: {file_path.name} -> {new_name}")
                fixed_count += 1
            except Exception as e:
                print(f"Error fixing {file_path.name}: {e}")
    
    print(f"\nFixed {fixed_count} file extensions")
    print("Now all files should have proper .txt extensions")

if __name__ == "__main__":
    fix_file_extensions()
