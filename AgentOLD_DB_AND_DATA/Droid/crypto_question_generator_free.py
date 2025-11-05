#!/usr/bin/env python3

import re
import os
import time
from typing import List, Dict
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Topic:
    """Data class for storing topic information"""
    category: str
    topic_id: str
    complexity: str
    application: str
    asset_types: str
    timeframes: str
    title: str
    subtopics: List[str]

class CryptoQuestionGeneratorFree:
    """Free-tier friendly question generator with fallback models"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.output_dir = Path("crypto_questions")
        self.output_dir.mkdir(exist_ok=True)
        
        # List of free models to try in order
        self.free_models = [
            "meta-llama/llama-3.1-8b-instruct:free",
            "microsoft/wizardlm-2-8x22b:free", 
            "qwen/qwen-2.5-7b-instruct:free",
            "meta-llama/llama-3-8b-instruct:free"
        ]
    
    def parse_topics_document(self, file_path: str) -> List[Topic]:
        """Parse the crypto topics document and extract structured topics"""
        topics = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by BEGIN_TOPIC/END_TOPIC blocks, but filter out template examples
        topic_blocks = re.findall(r'@BEGIN_TOPIC(.*?)@END_TOPIC', content, re.DOTALL)
        
        # Filter out the template blocks (those with placeholder values)
        valid_blocks = []
        for block in topic_blocks:
            # Skip blocks that have template placeholder values
            if '[Category Name]' in block or '[Unique identifier]' in block:
                continue
            valid_blocks.append(block)
        
        for block in valid_blocks:
            # Extract metadata
            category_match = re.search(r'CATEGORY:\s*(.+)', block)
            topic_id_match = re.search(r'TOPIC_ID:\s*(.+)', block)
            complexity_match = re.search(r'COMPLEXITY:\s*(.+)', block)
            application_match = re.search(r'APPLICATION:\s*(.+)', block)
            asset_types_match = re.search(r'ASSET_TYPES:\s*(.+)', block)
            timeframes_match = re.search(r'TIMEFRAMES:\s*(.+)', block)
            
            # Extract the main content (topic title and subtopics)
            content_lines = block.strip().split('\n')
            content_lines = [line.strip() for line in content_lines if not line.startswith('@') and line.strip()]
            
            if content_lines:
                title = content_lines[0].split('.')[1].strip() if '.' in content_lines[0] else content_lines[0]
                subtopics = []
                
                for line in content_lines[1:]:
                    if re.match(r'^\d+\.', line.strip()):
                        # Main subtopic
                        clean_line = re.sub(r'^\d+\.\s*', '', line.strip())
                        subtopics.append(clean_line)
                    elif line.strip().startswith('   -'):
                        # Sub-subtopic (indentation)
                        clean_line = re.sub(r'^\s*-\s*', '', line.strip())
                        if subtopics:
                            subtopics[-1] += f" | {clean_line}"
            
                topic = Topic(
                    category=category_match.group(1) if category_match else "Unknown",
                    topic_id=topic_id_match.group(1) if topic_id_match else "Unknown",
                    complexity=complexity_match.group(1) if complexity_match else "Unknown",
                    application=application_match.group(1) if application_match else "Unknown",
                    asset_types=asset_types_match.group(1) if asset_types_match else "Unknown",
                    timeframes=timeframes_match.group(1) if timeframes_match else "Unknown",
                    title=title,
                    subtopics=subtopics
                )
                
                topics.append(topic)
        
        return topics
    
    def generate_questions_for_topic(self, topic: Topic) -> List[str]:
        """Generate 15 questions using free models with fallback logic"""
        import requests
        
        # shorter wait time for free models
        time.sleep(2)
        
        prompt = f"""Generate 15 practice-oriented questions about cryptocurrency trading:

Topic: {topic.title}
Category: {topic.category}
Level: {topic.complexity}

Key areas to cover:
{chr(10).join(f"- {subtopic[:60]}..." for i, subtopic in enumerate(topic.subtopics[:6]) if subtopic)}

Requirements:
- 15 numbered questions
- Practical trading focus
- Include crypto market context
- Use "How, What, Why" starters
- Each question 15-25 words
- No yes/no questions

Format as numbered list from 1-15:

"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try each model until one works
        for model_name in self.free_models:
            data = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a cryptocurrency trading educator. Create clear, practical numbered questions."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            try:
                print(f"  Trying model: {model_name}")
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Parse questions more robustly
                    questions = self.parse_questions_from_response(content)
                    
                    if len(questions) >= 10:  # Accept if we got most of them
                        print(f"  ✓ Success with {model_name} - got {len(questions)} questions")
                        return questions[:15]
                    else:
                        print(f"  ✗ Only got {len(questions)} questions, trying next model")
                        continue
                        
                elif response.status_code == 403:
                    print(f"  ✗ Model {model_name} not available (403)")
                    continue
                    
                elif response.status_code == 429:
                    print(f"  ✗ Rate limited on {model_name}, waiting...")
                    time.sleep(5)
                    continue
                    
                else:
                    print(f"  ✗ Error {response.status_code} on {model_name}")
                    continue
                    
            except Exception as e:
                print(f"  ✗ Exception with {model_name}: {str(e)[:50]}")
                continue
        
        print(f"  ✗ All models failed for this topic")
        return []
    
    def parse_questions_from_response(self, content: str) -> List[str]:
        """Parse questions from model response"""
        questions = []
        
        # Try different patterns to extract questions
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            # Pattern 1: Numbered questions (1. Question?)
            if re.match(r'^\d+\.\s*.*\?$', line):
                question = re.sub(r'^\d+\.\s*', '', line).strip()
                if len(question) > 8:
                    questions.append(question)
            
            # Pattern 2: Questions ending with ?
            elif line.endswith('?') and len(line) > 8:
                if not line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')):
                    # Questions without numbers
                    questions.append(line)
        
        # If few questions, try substring extraction
        if len(questions) < 10:
            all_text = content.replace('\n', ' ')
            # Split by common question words
            parts = re.split(r'(?=[?])\.?\s*(\d+\.|\d\d\.)?', all_text)
            for part in parts:
                if '?' in part and len(part) > 15:
                    clean_question = part.strip()
                    if clean_question.endswith('?'):
                        questions.append(clean_question)
                        if len(questions) >= 15:
                            break
        
        return questions
    
    def save_questions_to_file(self, topic: Topic, questions: List[str]) -> str:
        """Save questions to a text file"""
        filename = f"{topic.category}_{topic.topic_id}_{topic.complexity}.txt"
        filename = re.sub(r'[^\w\s-]', '', filename).replace(' ', '_') + '.txt'
        filepath = self.output_dir / filename
        
        content = f"""# Questions for: {topic.title}
# Category: {topic.category} ({topic.topic_id})
# Complexity: {topic.complexity} | Application: {topic.application}
# Asset Types: {topic.asset_types} | Timeframes: {topic.timeframes}
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 80}

KEY SUBTOPICS:
{chr(10).join(f"{i+1}. {subtopic}" for i, subtopic in enumerate(topic.subtopics[:8]) if subtopic)}

{'=' * 80}

GENERATED QUESTIONS ({len(questions)}):
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(questions))}

{'=' * 80}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_all_questions(self, topics_file: str) -> Dict[str, str]:
        """Generate questions for all topics with model fallback"""
        from datetime import datetime
        
        start_time = datetime.now()
        print(f"Starting FREE model generation at: {start_time.strftime('%H:%M:%S')}")
        
        topics = self.parse_topics_document(topics_file)
        print(f"Found {len(topics)} topics to process")
        print(f"Using {len(self.free_models)} different free models as fallbacks")
        
        generated_files = {}
        failed_topics = []
        
        for i, topic in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}] {topic.title} ({topic.topic_id})")
            
            try:
                questions = self.generate_questions_for_topic(topic)
                
                if questions:
                    filepath = self.save_questions_to_file(topic, questions)
                    generated_files[topic.topic_id] = filepath
                    print(f"✓ {len(questions)} → {filepath.name}")
                else:
                    failed_topics.append(topic.topic_id)
                    print(f"✗ Failed - no questions generated")
                
                # Shorter delay to be respectful but efficient
                if i < len(topics):
                    time.sleep(8)
                
            except Exception as e:
                failed_topics.append(topic.topic_id)
                print(f"✗ Error: {str(e)[:40]}")
        
        # Final summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n{'='*60}")
        print("FREE GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Topics attempted: {len(topics)}")
        print(f"Successfully: {len(generated_files)}")
        print(f"Failed: {len(failed_topics)}")
        print(f"Questions created: {len(generated_files) * 15}")
        print(f"Duration: {duration}")
        
        if failed_topics:
            print(f"\nFailed IDs: {', '.join(failed_topics[:5])}{'...' if len(failed_topics) > 5 else ''}")
        
        success_rate = (len(generated_files) / len(topics)) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        return generated_files

def main():
    """Main function"""
    import os
    from pathlib import Path
    
    print("Crypto Questions Generator - FREE MODELS")
    print("=" * 50)
    print("Using multiple free models with automatic fallback")
    print("=" * 50)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        print("Get key: https://openrouter.ai/keys")
        return
    
    topics_file = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
    if not Path(topics_file).exists():
        print(f"ERROR: {topics_file} not found")
        return
    
    try:
        generator = CryptoQuestionGeneratorFree(api_key)
        results = generator.generate_all_questions(topics_file)
        
        print(f"\n🎉 SUCCESS for {len(results)} topics!")
        print(f"📁 Check: crypto_questions/")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
