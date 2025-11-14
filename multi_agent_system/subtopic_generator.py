"""
Subtopic Generator Agent
Step 1: Takes a main topic and generates a comprehensive list of subtopics
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class SubtopicGeneratorAgent:
    """
    Agent that generates comprehensive subtopics from a main topic
    Creates a task list for the Q&A generation pipeline
    """

    def __init__(self, model_url: Optional[str] = None):
        """
        Initialize the subtopic generator
        
        Args:
            model_url: URL of the LLM server
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        
        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )

    def generate_subtopics(self, topic: str, min_subtopics: int = 10, max_subtopics: int = 50) -> Dict[str, Any]:
        """
        Generate comprehensive subtopics for a main topic
        
        Args:
            topic: Main topic to break down
            min_subtopics: Minimum number of subtopics
            max_subtopics: Maximum number of subtopics
            
        Returns:
            Dictionary with subtopics list
        """
        system_prompt = """You are an expert at breaking down complex topics into comprehensive, well-organized subtopics.

Your role is to analyze a main topic and create a detailed list of subtopics that:
1. Cover all important aspects of the topic
2. Are specific enough to generate 100 high-quality questions each
3. Are organized logically (foundational → intermediate → advanced)
4. Avoid overlap between subtopics
5. Are suitable for creating AI training datasets

Guidelines:
- Start with foundational/basic concepts
- Progress to intermediate applications
- Include advanced/expert-level topics
- Consider different perspectives (technical, practical, strategic, risk management)
- Ensure each subtopic is substantial enough for 100 questions
- Use clear, descriptive names for subtopics

Output format: Return a JSON array of subtopic strings, ordered from foundational to advanced."""

        user_prompt = f"""Analyze the following topic and generate between {min_subtopics} and {max_subtopics} comprehensive subtopics:

TOPIC: {topic}

Requirements:
- Each subtopic should be specific and focused
- Each subtopic should be capable of generating 100 high-quality questions
- Organize from foundational to advanced
- Cover all major aspects of the topic
- Ensure good coverage without excessive overlap

Return ONLY a JSON array of strings, no additional text. Example format:
["Subtopic 1", "Subtopic 2", "Subtopic 3", ...]"""

        try:
            print(f"[GENERATING] Subtopics for: {topic}")
            
            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON array
            import json
            import re
            
            # Remove markdown code blocks if present
            content = re.sub(r'```json\n?', '', content)
            content = re.sub(r'```\n?', '', content)
            content = content.strip()
            
            # Try to parse as JSON
            try:
                subtopics = json.loads(content)
                if isinstance(subtopics, list) and all(isinstance(s, str) for s in subtopics):
                    print(f"[OK] Generated {len(subtopics)} subtopics")
                    return {
                        "success": True,
                        "subtopics": subtopics,
                        "count": len(subtopics)
                    }
                else:
                    raise ValueError("Invalid format")
            except json.JSONDecodeError:
                # Try to extract list items manually
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                subtopics = []
                for line in lines:
                    # Remove numbering and quotes
                    line = re.sub(r'^\d+[\.\)]\s*', '', line)
                    line = re.sub(r'^["\']|["\']$', '', line)
                    line = line.strip()
                    if line and len(line) > 5:  # Filter out very short lines
                        subtopics.append(line)
                
                if subtopics:
                    print(f"[OK] Generated {len(subtopics)} subtopics (parsed from text)")
                    return {
                        "success": True,
                        "subtopics": subtopics,
                        "count": len(subtopics)
                    }
                else:
                    raise ValueError("Could not parse subtopics")
            
        except Exception as e:
            print(f"[ERROR] Failed to generate subtopics: {e}")
            return {
                "success": False,
                "error": str(e),
                "subtopics": []
            }

