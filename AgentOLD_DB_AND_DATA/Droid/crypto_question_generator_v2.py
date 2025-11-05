#!/usr/bin/env python3

import re
import os
import time
from typing import List, Dict, Tuple
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

class CryptoQuestionGeneratorV2:
    """Enhanced version with better rate limiting and question parsing"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.output_dir = Path("crypto_questions")
        self.output_dir.mkdir(exist_ok=True)
    
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
    
    def generate_questions_for_topic(self, topic: Topic, max_retries: int = 2) -> List[str]:
        """Generate 15 questions for a specific topic using AI with improved parsing"""
        import requests
        import json
        
        # Much longer initial wait to avoid rate limits
        time.sleep(3)
        
        prompt = f"""Generate exactly 15 diverse, practice-oriented questions about this cryptocurrency trading topic:

TOPIC: {topic.title}
CATEGORY: {topic.category}
COMPLEXITY LEVEL: {topic.complexity}
APPLICATION: {topic.application}
ASSET TYPES: {topic.asset_types}
TIMEFRAMES: {topic.timeframes}

KEY SUBTOPICS:
{chr(10).join(f"{i+1}. {subtopic}" for i, subtopic in enumerate(topic.subtopics[:8]) if subtopic)}

Generate questions that cover:
1. Fundamental understanding (5 questions)
2. Practical application strategies (5 questions) 
3. Risk management considerations (3 questions)
4. Advanced/edge cases (2 questions)

Requirements:
- Each question must be specific and answerable
- Include cryptocurrency market context
- Vary question complexity appropriately
- Make questions practical for traders
- Format as a numbered list (1. Question here?)
- No yes/no questions - use "how", "what", "why", "when" starters
- Each question should be substantial (15-25 words)
- Normal writing - no special characters or extra spaces

Generate exactly 15 questions:"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try a different model that might have better rate limits
        data = {
            "model": "anthropic/claude-3.5-haiku:beta",
            "messages": [
                {"role": "system", "content": "You are an expert cryptocurrency trading educator creating high-quality practice questions for traders. Return clear, readable questions without special formatting."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        # Retry logic with longer delays
        for attempt in range(max_retries):
            try:
                print(f"  API attempt {attempt + 1}/{max_retries}...")
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=45
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    print(f"  API response received, parsing...")
                    
                    # Better question extraction
                    questions = []
                    lines = content.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        # Match numbered questions more robustly
                        if re.match(r'^\d+\.\s*.*\?$', line):
                            # Clean up the question
                            question = re.sub(r'^\d+\.\s*', '', line).strip()
                            if len(question) > 10:  # Ensure substantial questions
                                questions.append(question)
                                if len(questions) >= 15:
                                    break
                    
                    # If we didn't get 15 questions, try other patterns
                    if len(questions) < 15:
                        # Look for standalone questions
                        all_lines = content.replace('\n', ' ').split('. ')
                        for line in all_lines:
                            line = line.strip()
                            if '?' in line and len(line) > 10:
                                questions.append(line)
                                if len(questions) >= 15:
                                    break
                    
                    if questions:
                        print(f"  Successfully extracted {len(questions)} questions")
                        return questions[:15]
                    else:
                        print(f"  No valid questions found in response")
                        if attempt < max_retries - 1:
                            return []  # Try next attempt
                        else:
                            return []  # Final attempt failed
                        
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = 10 + (attempt * 5)  # 10s, 15s delays
                    print(f"  Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    if attempt == max_retries - 1:
                        print(f"  Max retries reached for {topic.title}")
                        return []
                    continue
                    
                else:
                    print(f"  API error: {response.status_code}")
                    if attempt == max_retries - 1:
                        return []
                    time.sleep(5)
                    continue
                    
            except Exception as e:
                print(f"  Error: {e}")
                if attempt == max_retries - 1:
                    return []
                time.sleep(5)
                continue
        
        return []
    
    def save_questions_to_file(self, topic: Topic, questions: List[str]) -> str:
        """Save questions to a text file with better formatting"""
        filename = f"{topic.category}_{topic.topic_id}_{topic.complexity}.txt"
        # Clean filename
        filename = re.sub(r'[^\w\s-]', '', filename).replace(' ', '_') + '.txt'
        filepath = self.output_dir / filename
        
        content = f"""# Questions for: {topic.title}
# Category: {topic.category}
# Topic ID: {topic.topic_id}
# Complexity: {topic.complexity}
# Application: {topic.application}
# Asset Types: {topic.asset_types}
# Timeframes: {topic.timeframes}
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 80}

KEY SUBTOPICS:
{chr(10).join(f"{i+1}. {subtopic}" for i, subtopic in enumerate(topic.subtopics[:10]) if subtopic)}

{'=' * 80}

GENERATED QUESTIONS:
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(questions))}

{'=' * 80}

Total Questions: {len(questions)}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_all_question_files(self, topics_file: str) -> Dict[str, str]:
        """Generate question files for all topics with conservative rate limiting"""
        from datetime import datetime
        
        start_time = datetime.now()
        print(f"Starting enhanced question generation at: {start_time.strftime('%H:%M:%S')}")
        
        topics = self.parse_topics_document(topics_file)
        print(f"Found {len(topics)} topics to process")
        
        generated_files = {}
        failed_topics = []
        
        for i, topic in enumerate(topics, 1):
            print(f"\nProcessing topic {i}/{len(topics)}: {topic.title}")
            
            try:
                questions = self.generate_questions_for_topic(topic)
                
                if questions:
                    filepath = self.save_questions_to_file(topic, questions)
                    generated_files[topic.topic_id] = filepath
                    print(f"+ Generated {len(questions)} questions -> {filepath}")
                else:
                    failed_topics.append(topic.topic_id)
                    print(f"- Failed to generate questions for {topic.title}")
                
                # CONSERVATIVE delay between topics to avoid rate limits
                if i < len(topics):
                    print("  Waiting 12 seconds before next topic...")
                    time.sleep(12)
                
            except Exception as e:
                failed_topics.append(topic.topic_id)
                print(f"- Error processing {topic.title}: {e}")
                time.sleep(10)
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n{'='*60}")
        print("ENHANCED GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total topics processed: {len(topics)}")
        print(f"Successfully generated: {len(generated_files)}")
        print(f"Failed: {len(failed_topics)}")
        print(f"Questions per topic: 15")
        print(f"Total questions created: {len(generated_files) * 15}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Completed at: {end_time.strftime('%H:%M:%S')}")
        print(f"Total duration: {duration}")
        
        if failed_topics:
            print(f"\nFailed topic IDs: {', '.join(failed_topics)}")
        
        # Generate completion summary
        print(f"\nProcess Summary:")
        print(f"- Topics processed: {len(topics)}")
        print(f"- Successfully generated: {len(generated_files)}")  
        print(f"- Failed: {len(failed_topics)}")
        print(f"- Questions created: {len(generated_files) * 15}")
        print(f"- Time per topic: {duration.total_seconds() / len(topics):.1f} seconds")
        
        return generated_files

def main():
    """Main function to run the enhanced question generator"""
    import os
    from pathlib import Path
    
    print("Enhanced Crypto Questions Generator v2.0")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: OpenRouter API key not found!")
        print("Please set OPENROUTER_API_KEY environment variable")
        print("Get your key from: https://openrouter.ai/")
        return
    
    # Check for topics file
    topics_file = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
    if not Path(topics_file).exists():
        print(f"ERROR: Topics file not found: {topics_file}")
        return
    
    try:
        generator = CryptoQuestionGeneratorV2(api_key)
        generated_files = generator.generate_all_question_files(topics_file)
        
        print(f"\nSUCCESS: Generated question files for {len(generated_files)} topics")
        print(f"Check the 'crypto_questions' directory for all files")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
