#!/usr/bin/env python3

import re
import os
import time
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Subtopic:
    """Data class for subtopic information"""
    name: str
    description: str
    questions: List[str]
    complexity: str
    estimated_time_to_master: str

@dataclass
class EnhancedTopic:
    """Enhanced topic with hierarchical subtopics"""
    category: str
    topic_id: str
    complexity: str
    application: str
    asset_types: str
    timeframes: str
    title: str
    main_concepts: List[str]
    subtopics: List[Subtopic]

class HierarchicalCryptoGenerator:
    """Generate hierarchical topic-subtopic Q&A structures"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.output_dir = Path("hierarchical_crypto_questions")
        self.output_dir.mkdir(exist_ok=True)
        
        self.free_models = [
            "meta-llama/llama-3.1-8b-instruct:free",
            "microsoft/wizardlm-2-8x22b:free", 
            "qwen/qwen-2.5-7b-instruct:free",
            "meta-llama/llama-3-8b-instruct:free"
        ]
    
    def create_subtopics_for_topic(self, topic_info: str, num_subtopics: int = 4) -> List[str]:
        """Generate subtopics for a given main topic"""
        import requests
        
        print(f"  Generating {num_subtopics} subtopics...")
        
        prompt = f"""Given this cryptocurrency trading topic, create {num_subtopics} logical subtopics that organize the knowledge hierarchically:

TOPIC: {topic_info}

Requirements for subtopics:
- Each subtopic should be a focused area of study
- Subtopics should be distinct but related
- Learning should progress logically between them
- Each subtopic should be comprehensive enough for 3-5 specific questions
- Use clear, descriptive names (2-4 words each)
- Focus on practical, actionable knowledge

Format as numbered list:
1. [Subtopic Name]
2. [Subtopic Name]
3. [Subtopic Name]
{f'4. [Subtopic Name]' if num_subtopics >= 4 else ''}

Subtopics:"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for model_name in self.free_models:
            data = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are an expert cryptographer and educator creating structured learning materials."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6,
                "max_tokens": 300
            }
            
            try:
                print(f"    Trying model: {model_name}")
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=20
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Extract subtopics
                    subtopics = []
                    lines = content.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        # Match numbered subtopics
                        if re.match(r'^\d+\.\s*[^.]+$', line) and len(line) > 5:
                            subtopic = re.sub(r'^\d+\.\s*', '', line).strip()
                            if len(subtopic) > 3:
                                subtopics.append(subtopic)
                    
                    if len(subtopics) >= num_subtopics:
                        print(f"    + Generated {len(subtopics)} subtopics")
                        return subtopics[:num_subtopics]
                
            except Exception as e:
                print(f"    - Error with {model_name}: {str(e)[:30]}")
                continue
        
        print(f"    - Could not generate subtopics")
        return []
    
    def generate_questions_for_subtopic(self, main_topic: str, subtopic: str, num_questions: int = 3) -> List[str]:
        """Generate specific questions for a subtopic"""
        import requests
        
        print(f"    Generating {num_questions} questions for: {subtopic}")
        
        # Determine complexity based on subtopic nature
        complexity_keywords = {
            'beginner': ['introduction', 'basics', 'fundamentals', 'getting started'],
            'intermediate': ['analysis', 'strategies', 'techniques', 'patterns'],
            'expert': ['advanced', 'optimization', 'risk management', 'portfolio']
        }
        
        complexity = 'intermediate'
        for level, keywords in complexity_keywords.items():
            if any(keyword in subtopic.lower() for keyword in keywords):
                complexity = level
                break
        
        prompt = f"""Generate exactly {num_questions} targeted practice questions for this crypto subtopic:

MAIN TOPIC: {main_topic}
SUBTOPIC: {subtopic}
COMPLEXITY LEVEL: {complexity}

Requirements:
- Questions should be specific to this subtopic only
- Use practical, real-world trading scenarios
- Include cryptocurrency market context
- Questions should test both understanding and application
- Mix theory questions with "how would you" practical questions
- Use "How, What, Why, When, Explain" starters
- Each question: 12-20 words

Generate as numbered list 1-{num_questions}:"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for model_name in self.free_models:
            data = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a cryptocurrency trading expert creating targeted practice questions."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=25
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Extract questions
                    questions = []
                    lines = content.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if re.match(r'^\d+\.\s*.*\?$', line):
                            question = re.sub(r'^\d+\.\s*', '', line).strip()
                            if len(question) > 10:
                                questions.append(question)
                    
                    if len(questions) >= num_questions:
                        print(f"      + Got {len(questions)} questions")
                        return questions[:num_questions]
                
            except Exception as e:
                continue
        
        return []
    
    def generate_hierarchical_topic(self, topic_title: str, num_subtopics: int = 4, questions_per_subtopic: int = 3) -> Optional[EnhancedTopic]:
        """Generate complete hierarchical topic structure"""
        
        print(f"Generating hierarchical topic: {topic_title}")
        print("=" * 60)
        
        # Step 1: Generate subtopics
        subtopic_names = self.create_subtopics_for_topic(topic_title, num_subtopics)
        
        if not subtopic_names:
            print(f"Could not generate subtopics for {topic_title}")
            return None
        
        # Step 2: Generate questions for each subtopic
        subtopic_objects = []
        
        for i, subtopic_name in enumerate(subtopic_names, 1):
            print(f"\n[{i}/{len(subtopic_names)}] Processing: {subtopic_name}")
            
            questions = self.generate_questions_for_subtopic(topic_title, subtopic_name, questions_per_subtopic)
            
            if questions:
                subtopic = Subtopic(
                    name=subtopic_name,
                    description=f"Focused learning module for {subtopic_name} in the context of {topic_title}",
                    questions=questions,
                    complexity="intermediate",
                    estimated_time_to_master="2-4 hours"
                )
                subtopic_objects.append(subtopic)
                print(f"      → {len(questions)} questions created")
            else:
                print(f"      → No questions generated")
            
            # Delay between subtopics
            if i < len(subtopic_names):
                time.sleep(3)
        
        # Step 3: Create enhanced topic object
        if subtopic_objects:
            enhanced_topic = EnhancedTopic(
                category="Cryptocurrency Trading",
                topic_id=topic_title.lower().replace(' ', '_')[0:20],
                complexity="intermediate",
                application="theory + practice",
                asset_types="all crypto",
                timeframes="1h, 4h, 1D",
                title=topic_title,
                main_concepts=subtopic_names,
                subtopics=subtopic_objects
            )
            
            print(f"\n✅ Complete hierarchical topic generated!")
            print(f"   Subtopics: {len(subtopic_objects)}")
            print(f"   Total questions: {sum(len(s.questions) for s in subtopic_objects)}")
            
            return enhanced_topic
        
        return None
    
    def save_hierarchical_topic(self, topic: EnhancedTopic) -> str:
        """Save hierarchical topic to multiple formats"""
        
        # Create directory for this topic
        topic_dir = self.output_dir / f"{topic.topic_id}"
        topic_dir.mkdir(exist_ok=True)
        
        formats_saved = []
        
        # Format 1: Complete JSON file
        json_data = {
            "metadata": {
                "title": topic.title,
                "category": topic.category,
                "topic_id": topic.topic_id,
                "complexity": topic.complexity,
                "generated": time.strftime('%Y-%m-%d %H:%M:%S')
            },
            "subtopics": [
                {
                    "name": subtopic.name,
                    "description": subtopic.description,
                    "questions": subtopic.questions,
                    "complexity": subtopic.complexity,
                    "estimated_time": subtopic.estimated_time_to_master
                }
                for subtopic in topic.subtopics
            ]
        }
        
        json_file = topic_dir / f"{topic.topic_id}_complete.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        formats_saved.append(str(json_file))
        
        # Format 2: Individual text files per subtopic
        for subtopic in topic.subtopics:
            filename = f"{subtopic.name.replace(' ', '_').lower()}.txt"
            filepath = topic_dir / filename
            
            content = f"""# {subtopic.name}
# Part of: {topic.title}
# Complexity: {subtopic.complexity}
# Questions: {len(subtopic.questions)}
# Estimated study time: {subtopic.estimated_time_to_master}

{subtopic.description}

{'=' * 80}

QUESTIONS:
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(subtopic.questions))}

{'=' * 80}

Total Questions: {len(subtopic.questions)}
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            formats_saved.append(str(filepath))
        
        # Format 3: Summary index file
        index_file = topic_dir / f"{topic.topic_id}_index.txt"
        total_questions = sum(len(s.questions) for s in topic.subtopics)
        
        index_content = f"""# {topic.title}
# Hierarchical Topic Index
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 80}

TOPIC OVERVIEW:
- Category: {topic.category}
- Main Concepts: {', '.join(topic.main_concepts)}
- Total Subtopics: {len(topic.subtopics)}
- Total Questions: {total_questions}
- Structure: Hierarchical learning path

{'=' * 80}

SUBTOPICS BREAKDOWN:
{chr(10).join(f"{i+1}. {subtopic.name} ({len(subtopic.questions)} questions)" for i, subtopic in enumerate(topic.subtopics))}

{'=' * 80}

SUBTOPIC DETAILS:
"""
        
        for subtopic in topic.subtopics:
            index_content += f"""
{subtopic.name}:
  Complexity: {subtopic.complexity}
  Questions: {len(subtopic.questions)}
  Study Time: {subtopic.estimated_time_to_master}
  Key Questions Preview:
{chr(10).join(f"    - {q[:60]}..." for q in subtopic.questions[:2])}
"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        formats_saved.append(str(index_file))
        
        # Format 4: RAG-ready pairs (question-answer style)
        rag_file = topic_dir / f"{topic.topic_id}_rag_pairs.txt"
        rag_content = f"""# RAG-Ready Question Pairs
# Topic: {topic.title}
# Format: Question | Context (Subtopic Name)

{'=' * 80}

QUESTION-CONTEXT PAIRS:
"""
        
        for subtopic in topic.subtopics:
            for i, question in enumerate(subtopic.questions, 1):
                rag_content += f"Q{i+sum(len(prev_sub.questions) for prev_sub in topic.subtopics if topic.subtopics.index(prev_sub) < topic.subtopics.index(subtopic))}. {question} | Context: {subtopic.name}\n"
        
        with open(rag_file, 'w', encoding='utf-8') as f:
            f.write(rag_content)
        formats_saved.append(str(rag_file))
        
        return str(topic_dir)
    
    def generate_batch_hierarchical_topics(self, topics: List[str]) -> Dict[str, str]:
        """Generate multiple hierarchical topics"""
        
        print("BATCH HIERARCHICAL GENERATION")
        print("=" * 50)
        print(f"Processing {len(topics)} topics...")
        
        results = {}
        failed = []
        
        for i, topic_title in enumerate(topics, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(topics)}] {topic_title}")
            print('=' * 60)
            
            try:
                hierarchical_topic = self.generate_hierarchical_topic(
                    topic_title, 
                    num_subtopics=4, 
                    questions_per_subtopic=3
                )
                
                if hierarchical_topic:
                    save_path = self.save_hierarchical_topic(hierarchical_topic)
                    results[topic_title] = save_path
                    print(f"✅ SAVED: {save_path}")
                else:
                    failed.append(topic_title)
                    print(f"❌ FAILED to generate topic")
                
                # Delay between topics
                if i < len(topics):
                    print(f"Waiting 8 seconds before next topic...")
                    time.sleep(8)
                
            except Exception as e:
                failed.append(topic_title)
                print(f"❌ ERROR: {str(e)[:50]}")
        
        # Summary
        print(f"\n{'='*60}")
        print("BATCH COMPLETE")
        print('='*60)
        print(f"Topics processed: {len(topics)}")
        print(f"Successfully: {len(results)}")
        print(f"Failed: {len(failed)}")
        
        total_questions = 0
        for topic_title, save_path in results.items():
            topic_dir = Path(save_path)
            if topic_dir.exists():
                json_file = topic_dir / f"{topic_title.lower().replace(' ', '_')[0:20]}_complete.json"
                if json_file.exists():
                    with open(json_file) as f:
                        data = json.load(f)
                        topic_questions = sum(len(subtopic["questions"]) for subtopic in data["subtopics"])
                        total_questions += topic_questions
        
        print(f"Total questions generated: {total_questions}")
        
        if failed:
            print(f"Failed topics: {', '.join(failed[:3])}")
        
        return results

def main():
    """Main function for hierarchical generation"""
    import os
    from pathlib import Path
    
    print("Hierarchical Crypto Question Generator")
    print("=" * 50)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        return
    
    # Option 1: Generate one specific topic
    custom_topic = os.getenv('TOPIC_NAME', None)
    
    if custom_topic:
        print(f"Generating hierarchical topic: {custom_topic}")
        generator = HierarchicalCryptoGenerator(api_key)
        
        topic = generator.generate_hierarchical_topic(custom_topic)
        if topic:
            save_path = generator.save_hierarchical_topic(topic)
            print(f"✅ Saved to: {save_path}")
        return
    
    # Option 2: Generate from main topics file
    topics_file = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
    if Path(topics_file).exists():
        print("Reading topics from main file...")
        
        generator = HierarchicalCryptoGenerator(api_key)
        
        # Extract topic titles from the main file
        with open(topics_file, 'r') as f:
            content = f.read()
        
        # Extract actual topic titles (not category headers)
        topic_blocks = re.findall(r'@BEGIN_TOPIC(.*?)@END_TOPIC', content, re.DOTALL)
        
        topic_titles = []
        for block in topic_blocks:
            if '[Category Name]' not in block:
                lines = block.strip().split('\n')
                for line in lines:
                    if re.match(r'^\d+\.', line.strip()) and not line.strip().startswith('@'):
                        title = re.sub(r'^\d+\.\s*', '', line.strip())
                        if len(title) > 10 and len(title) < 100:
                            topic_titles.append(title)
                        break
        
        # Start with a few topics for testing
        test_topics = topic_titles[:2] if topic_titles else [
            "Bitcoin Trading Patterns",
            "Ethereum Technical Analysis"
        ]
        
        print(f"Test topics: {test_topics}")
        
        # Generate hierarchical topics
        results = generator.generate_batch_hierarchical_topics(test_topics)
        
        print(f"\n🎉 Generated {len(results)} hierarchical topic structures!")
        print(f"📁 Check: hierarchical_crypto_questions/")
        
    else:
        print(f"Topics file not found: {topics_file}")

if __name__ == "__main__":
    main()
