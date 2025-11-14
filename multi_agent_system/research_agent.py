"""
Research Agent
Step 3: Performs deep research on questions using web search and synthesis
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ResearchAgent:
    """
    Agent that performs deep research on questions
    Uses web search and synthesizes information from multiple sources
    """

    def __init__(self, model_url: Optional[str] = None, domain_config: Optional[Dict] = None):
        """
        Initialize the research agent
        
        Args:
            model_url: URL of the LLM server
            domain_config: Domain configuration dictionary (for domain-specific prompts)
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        
        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )
        
        # Domain configuration (defaults to cryptocurrency if not provided)
        self.domain_config = domain_config
        if self.domain_config is None:
            from .domain_config import get_domain_config
            self.domain_config = get_domain_config("cryptocurrency")

    def research_question(self, question: str) -> Dict[str, Any]:
        """
        Perform deep research on a question
        
        Args:
            question: The question to research
            
        Returns:
            Dictionary with research data
        """
        # Use domain-specific prompts
        from .domain_config import get_research_prompt, get_research_user_prompt_template
        
        system_prompt = get_research_prompt(self.domain_config)
        user_prompt_template = get_research_user_prompt_template(self.domain_config)
        user_prompt = user_prompt_template.format(question=question)

        try:
            print(f"  [RESEARCHING] {question[:60]}...")
            
            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for factual research
                max_tokens=2048
            )
            
            research_content = response.choices[0].message.content.strip()
            
            # Structure the research data
            research_data = {
                "question": question,
                "research_notes": research_content,
                "key_concepts": self._extract_key_concepts(research_content),
                "research_length": len(research_content)
            }
            
            return {
                "success": True,
                "research_data": research_data
            }
            
        except Exception as e:
            print(f"  [ERROR] Research failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "research_data": {}
            }

    def _extract_key_concepts(self, research_content: str) -> List[str]:
        """Extract key concepts from research content"""
        # Simple extraction - can be enhanced
        import re
        
        # Look for capitalized terms, technical terms, etc.
        concepts = []
        
        # Find terms in quotes or after "concept:", "term:", etc.
        patterns = [
            r'"([^"]+)"',
            r'concept[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'term[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, research_content, re.IGNORECASE)
            concepts.extend(matches)
        
        # Remove duplicates and return top 10
        concepts = list(dict.fromkeys(concepts))[:10]
        return concepts

