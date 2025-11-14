"""
Question Generator Agent
Step 2: Takes a subtopic and generates 100 high-quality questions
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class QuestionGeneratorAgent:
    """
    Agent that generates 100 comprehensive questions for a subtopic
    """

    def __init__(self, model_url: Optional[str] = None, questions_per_topic: int = 100):
        """
        Initialize the question generator
        
        Args:
            model_url: URL of the LLM server
            questions_per_topic: Number of questions to generate per subtopic
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        self.questions_per_topic = questions_per_topic
        
        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )

    def generate_questions(self, subtopic: str) -> Dict[str, Any]:
        """
        Generate 100 questions for a subtopic
        
        Args:
            subtopic: The subtopic to generate questions for
            
        Returns:
            Dictionary with list of questions
        """
        system_prompt = """You are an expert at generating comprehensive, high-quality questions for AI training datasets.

Your role is to create diverse, well-structured questions that:
1. Cover all aspects of the subtopic
2. Range from foundational to advanced
3. Include different question types (what, how, why, when, where, compare, analyze)
4. Are specific and answerable
5. Avoid yes/no questions (prefer open-ended)
6. Are suitable for generating detailed, expert-level answers (3000+ characters each)

Question Types to Include:
- Definition/Explanation questions (What is...)
- How-to/Application questions (How do you...)
- Analysis questions (Why does...)
- Comparison questions (What's the difference between...)
- Best practices questions (What are the best practices for...)
- Risk/Consideration questions (What are the risks of...)
- Advanced/Expert questions (How can professionals...)
- Edge case questions (What happens when...)

Quality Standards:
- Each question should be clear and specific
- Questions should build knowledge progressively
- Avoid redundancy
- Ensure comprehensive coverage of the subtopic"""

        user_prompt = f"""Generate exactly {self.questions_per_topic} high-quality questions about the following subtopic:

SUBTOPIC: {subtopic}

Requirements:
- Generate exactly {self.questions_per_topic} questions
- Cover all aspects of the subtopic comprehensively
- Include various question types (what, how, why, compare, analyze, etc.)
- Range from beginner to expert level
- Each question should be capable of generating a detailed 3000+ character answer
- Avoid yes/no questions
- Ensure questions are specific and answerable

Return ONLY a JSON array of question strings, no additional text. Example format:
["Question 1?", "Question 2?", "Question 3?", ...]"""

        try:
            print(f"[GENERATING] {self.questions_per_topic} questions for: {subtopic}")
            
            # Generate in batches if needed (to handle token limits)
            all_questions = []
            batch_size = 50
            
            if self.questions_per_topic <= batch_size:
                # Single batch
                response = self.client.chat.completions.create(
                    model="mixtral",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,  # Higher creativity for diverse questions
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content.strip()
                questions = self._parse_questions(content)
                all_questions.extend(questions)
            else:
                # Multiple batches
                batches_needed = (self.questions_per_topic + batch_size - 1) // batch_size
                
                for batch_num in range(batches_needed):
                    batch_start = batch_num * batch_size
                    batch_end = min((batch_num + 1) * batch_size, self.questions_per_topic)
                    batch_count = batch_end - batch_start
                    
                    batch_prompt = f"""Generate exactly {batch_count} high-quality questions about the following subtopic:

SUBTOPIC: {subtopic}

This is batch {batch_num + 1} of {batches_needed}. Generate questions {batch_start + 1} to {batch_end}.

Requirements:
- Generate exactly {batch_count} questions
- Ensure diversity from previous batches
- Cover different aspects of the subtopic
- Include various question types

Return ONLY a JSON array of question strings."""
                    
                    response = self.client.chat.completions.create(
                        model="mixtral",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": batch_prompt}
                        ],
                        temperature=0.8,
                        max_tokens=4096
                    )
                    
                    content = response.choices[0].message.content.strip()
                    questions = self._parse_questions(content)
                    all_questions.extend(questions)
                    
                    print(f"  [BATCH {batch_num + 1}/{batches_needed}] Generated {len(questions)} questions")
            
            # Trim to exact count if needed
            all_questions = all_questions[:self.questions_per_topic]
            
            if len(all_questions) < self.questions_per_topic * 0.8:  # Less than 80% of target
                print(f"[WARNING] Only generated {len(all_questions)}/{self.questions_per_topic} questions")
            
            print(f"[OK] Generated {len(all_questions)} questions")
            
            return {
                "success": True,
                "questions": all_questions,
                "count": len(all_questions)
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to generate questions: {e}")
            return {
                "success": False,
                "error": str(e),
                "questions": []
            }

    def _parse_questions(self, content: str) -> List[str]:
        """Parse questions from LLM response"""
        import json
        import re
        
        # Remove markdown code blocks
        content = re.sub(r'```json\n?', '', content)
        content = re.sub(r'```\n?', '', content)
        content = content.strip()
        
        # Try JSON parsing first
        try:
            questions = json.loads(content)
            if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
                return questions
        except json.JSONDecodeError:
            pass
        
        # Fallback: parse from text
        questions = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            # Remove numbering
            line = re.sub(r'^\d+[\.\)]\s*', '', line)
            # Remove quotes
            line = re.sub(r'^["\']|["\']$', '', line)
            line = line.strip()
            
            # Check if it looks like a question
            if line and ('?' in line or line.endswith('?')) and len(line) > 10:
                questions.append(line)
        
        return questions

