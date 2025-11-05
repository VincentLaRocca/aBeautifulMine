#!/usr/bin/env python3

import requests
import sys
import json
from pathlib import Path
from datetime import datetime

def test_simple_defi_generation(api_key):
    """Simple test to generate DeFi subtopics and questions"""
    
    print("SIMPLE DEFI HIERARCHICAL GENERATION TEST")
    print("=" * 60)
    print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
    
    # Step 1: Generate subtopics for "Decentralized Finance"
    subtopics_prompt = """Create 4 logical subtopics for decentralized finance (DeFi) education:
    
Requirements:
- Each subtopic should be 2-4 words
- Focus on different aspects of DeFi
- Make them educational and progressive
- Return as numbered list

Example format:
1. Smart Contracts
2. Decentralized Exchanges
3. Yield Farming  
4. Risk Management

Create 4 subtopics for DeFi:"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a DeFi educator creating structured learning materials."},
            {"role": "user", "content": subtopics_prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 400
    }
    
    print("\n1. Generating DeFi subtopics...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print(f"✗ Subtopics response received:")
            print(content)
            
            # Extract subtopics
            subtopics = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if re.match(r'^\d+\.\s*[^.]+$', line) and len(line) > 5:
                    subtopic = re.sub(r'^\d+\.\s*', '', line).strip()
                    if len(subtopic) > 3:
                        subtopics.append(subtopic)
            
            print(f"\n✗ Extracted {len(subtopics)} subtopics:")
            for i, subtopic in enumerate(subtopics, 1):
                print(f"  {i}. {subtopic}")
            
            if len(subtopics) >= 4:
                print(f"\n2. Generating questions for each subtopic...")
                
                all_results = {}
                
                for i, subtopic in enumerate(subtopics[:4], 1):
                    print(f"\n  [{i}/4] Generating questions for: {subtopic}")
                    
                    questions_prompt = f"""Generate 3 practice questions about this DeFi subtopic:
                    
Main Topic: Decentralized Finance
Subtopic: {subtopic}

Requirements:
- Questions specific to this subtopic only
- Practical trading/DeFi context
- Use "How, What, Why" starters
- Each 15-25 words
- Return as numbered list

Questions about {subtopic}:"""
                    
                    data2 = {
                        "model": "meta-llama/llama-3.1-8b-instruct:free",
                        "messages": [
                            {"role": "system", "content": "You are a DeFi expert creating targeted practice questions."},
                            {"role": "user", "content": questions_prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                    
                    try:
                        response2 = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=data2,
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            result2 = response2.json()
                            content2 = result2['choices'][0]['message']['content']
                            
                            print(f"    Questions response:")
                            print(f"    {content2[:200]}...")
                            
                            # Extract questions
                            questions = []
                            lines2 = content2.split('\n')
                            
                            for line in lines2:
                                line = line.strip()
                                if re.match(r'^\d+\.\s*.*\?$', line):
                                    question = re.sub(r'^\d+\.\s*', '', line).strip()
                                    if len(question) > 10:
                                        questions.append(question)
                            
                            if len(questions) >= 3:
                                all_results[subtopic] = questions[:3]
                                print(f"    ✓ Got {len(questions)} questions")
                            else:
                                print(f"    - Only got {len(questions)} questions")
                        
                        else:
                            print(f"    - API error: {response2.status_code}")
                    
                    except Exception as e:
                        print(f"    - Error: {str(e)[:40]}")
                
                # Save results
                if all_results:
                    output_dir = Path("simple_defi_results")
                    output_dir.mkdir(exist_ok=True)
                    
                    # Save as JSON
                    json_file = output_dir / "defi_hierarchical_test.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(all_results, f, indent=2, ensure_ascii=False)
                    
                    # Save as readable text
                    text_file = output_dir / "defi_hierarchical_test.txt"
                    with open(text_file, 'w', encoding='utf-8') as f:
                        f.write("# Decentralized Finance - Hierarchical Structure\n")
                        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("# API Key: {api_key[:10]}...{api_key[-10:]}\n\n")
                        
                        total_questions = 0
                        for subtopic, questions in all_results.items():
                            f.write(f"## {subtopic}\n")
                            f.write(f"Questions ({len(questions)}):\n")
                            for i, question in enumerate(questions, 1):
                                f.write(f"{i}. {question}\n")
                            f.write("\n")
                            total_questions += len(questions)
                        
                        f.write(f"Total Subtopics: {len(all_results)}\n")
                        f.write(f"Total Questions: {total_questions}\n")
                    
                    print(f"\n✅ SUCCESS!")
                    print(f"   Subtopics: {len(all_results)}")
                    print(f"   Questions: {sum(len(q) for q in all_results.values())}")
                    print(f"   Files saved: {output_dir}/")
                    print(f"   - {json_file.name}")
                    print(f"   - {text_file.name}")
                    
                    return True
                else:
                    print("\n- Could not generate questions for any subtopics")
                    return False
                
            else:
                print(f"\n- Only got {len(subtopics)} subtopics, need at least 4")
                return False
        
        else:
            print(f"\n- API error: {response.status_code}")
            try:
                error_info = response.json()
                print(f"  Error details: {error_info}")
            except:
                print(f"  Response: {response.text[:200]}")
            return False
    
    except Exception as e:
        print(f"\n- Network error: {e}")
        return False

if __name__ == "__main__":
    import re
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your OpenRouter API key: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided")
        sys.exit(1)
    
    if not api_key.startswith("sk-or-"):
        print("ERROR: Invalid API key format")
        sys.exit(1)
    
    print(f"Testing hierarchical DeFi generation")
    print(f"Expected: 4 subtopics with 3 questions each (12 total)")
    
    success = test_simple_defi_generation(api_key)
    
    if success:
        print(f"\n🎉 Test completed successfully!")
        print(f"Check the simple_defi_results/ directory for your DeFi hierarchy!")
    else:
        print(f"\n❌ Test failed - check error messages above")
