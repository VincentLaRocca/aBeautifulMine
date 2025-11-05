#!/usr/bin/env python3

import re
from pathlib import Path

def test_parsing():
    """Test the topic parsing without API calls"""
    
    print("Testing Crypto Topics Parser...")
    print("=" * 50)
    
    file_path = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
    
    if not Path(file_path).exists():
        print(f"ERROR: File not found: {file_path}")
        return
    
    topics = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by BEGIN_TOPIC/END_TOPIC blocks
    topic_blocks = re.findall(r'@BEGIN_TOPIC(.*?)@END_TOPIC', content, re.DOTALL)
    
    print(f"Found {len(topic_blocks)} topic blocks")
    
    for i, block in enumerate(topic_blocks[:3], 1):  # Test first 3 topics
        print(f"\n--- Topic {i} ---")
        
        # Extract metadata
        category_match = re.search(r'CATEGORY:\s*(.+)', block)
        topic_id_match = re.search(r'TOPIC_ID:\s*(.+)', block)
        complexity_match = re.search(r'COMPLEXITY:\s*(.+)', block)
        application_match = re.search(r'APPLICATION:\s*(.+)', block)
        
        # Extract content
        content_lines = block.strip().split('\n')
        content_lines = [line.strip() for line in content_lines if not line.startswith('@') and line.strip()]
        
        if content_lines:
            title = content_lines[0].split('.')[1].strip() if '.' in content_lines[0] else content_lines[0]
            subtopics = []
            
            for line in content_lines[1:]:
                if re.match(r'^\d+\.', line.strip()):
                    clean_line = re.sub(r'^\d+\.\s*', '', line.strip())
                    subtopics.append(clean_line[:80] + "..." if len(clean_line) > 80 else clean_line)
            
            print(f"Category: {category_match.group(1) if category_match else 'Unknown'}")
            print(f"Topic ID: {topic_id_match.group(1) if topic_id_match else 'Unknown'}")
            print(f"Complexity: {complexity_match.group(1) if complexity_match else 'Unknown'}")
            print(f"Application: {application_match.group(1) if application_match else 'Unknown'}")
            print(f"Title: {title}")
            print(f"Subtopics: {len(subtopics)} found")
            for j, subtopic in enumerate(subtopics[:3], 1):
                print(f"  {j}. {subtopic}")
            if len(subtopics) > 3:
                print(f"  ... and {len(subtopics) - 3} more")
        
        # Stop after first 3 for testing
        if i >= 3:
            break
    
    print(f"\n{'='*50}")
    print("Parsing test complete!")
    print(f"Total topics available: {len(topic_blocks)}")
    print("Each topic will generate 15 questions when run with API key")

if __name__ == "__main__":
    test_parsing()
