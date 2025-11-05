#!/usr/bin/env python3

import re
from pathlib import Path

def test_parsing_fix():
    """Test that the template filtering works correctly"""
    
    print("Testing Topic Parsing Fix...")
    print("=" * 50)
    
    file_path = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
    
    if not Path(file_path).exists():
        print(f"ERROR: File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by BEGIN_TOPIC/END_TOPIC blocks
    topic_blocks = re.findall(r'@BEGIN_TOPIC(.*?)@END_TOPIC', content, re.DOTALL)
    print(f"Total topic blocks found: {len(topic_blocks)}")
    
    # Filter out the template blocks (those with placeholder values)
    valid_blocks = []
    template_blocks = 0
    
    for block in topic_blocks:
        # Skip blocks that have template placeholder values
        if '[Category Name]' in block or '[Unique identifier]' in block:
            template_blocks += 1
            continue
        valid_blocks.append(block)
    
    print(f"Template blocks filtered: {template_blocks}")
    print(f"Valid topic blocks: {len(valid_blocks)}")
    
    # Analyze the valid blocks
    print("\nValid Topics Found:")
    print("-" * 30)
    
    for i, block in enumerate(valid_blocks, 1):
        category_match = re.search(r'CATEGORY:\s*(.+)', block)
        topic_id_match = re.search(r'TOPIC_ID:\s*(.+)', block)
        complexity_match = re.search(r'COMPLEXITY:\s*(.+)', block)
        
        content_lines = block.strip().split('\n')
        content_lines = [line.strip() for line in content_lines if not line.startswith('@') and line.strip()]
        
        if content_lines:
            title = content_lines[0].split('.')[1].strip() if '.' in content_lines[0] else content_lines[0]
            
            print(f"{i}. {title}")
            print(f"   Category: {category_match.group(1) if category_match else 'Unknown'}")
            print(f"   Topic ID: {topic_id_match.group(1) if topic_id_match else 'Unknown'}")
            print(f"   Complexity: {complexity_match.group(1) if complexity_match else 'Unknown'}")
            print()
    
    print(f"{'='*50}")
    print("Parsing test complete!")
    print("Note: The fixed generator will only process the valid topics shown above")

if __name__ == "__main__":
    test_parsing_fix()
