"""
Answer Generator Agent
Step 4: Generates comprehensive answers using your specific prompt
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AnswerGeneratorAgent:
    """
    Agent that generates comprehensive answers using your specific prompt
    Ensures 3000+ character answers with proper structure
    """

    def __init__(self, model_url: Optional[str] = None, answer_prompt: Optional[str] = None):
        """
        Initialize the answer generator
        
        Args:
            model_url: URL of the LLM server
            answer_prompt: The specific prompt template for answers
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        
        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )
        
        # Default prompt (your provided prompt)
        self.answer_prompt = answer_prompt or """Core Task:

  Your mission is to provide a comprehensive, in-depth, and expert-level answer to the question. The answer

  must be thoroughly researched using web sources and synthesized into a clear, well-structured, and

  insightful explanation.

  CRITICAL: This is for ONE QUESTION ONLY. You will answer each question individually, one at a time.

  Do NOT write comprehensive essays covering multiple questions. Each question receives its own separate,

  complete answer of 3,000+ characters.

  Key Instructions & Quality Standards:

   1. Research Thoroughly: Use web searches to consult multiple authoritative sources (e.g., established trading

      education sites, books by recognized authors, in-depth articles). Synthesize information from these

      sources; do not rely on a single explanation.

   2. Achieve Depth and Length: The final answer must be a minimum of 3,000 characters PER INDIVIDUAL QUESTION.

      This requires moving beyond simple definitions into detailed explanations of the underlying mechanics and

      strategic applications. Each question gets its own 3,000+ character answer.

   3. Structure for Clarity: Structure your answer logically using Markdown. Use headings, subheadings, bullet

      points, and bold text to make the information easy to digest. A good structure includes:

       * A concise introduction defining the core concept.

       * A detailed body explaining the 'how' and 'why' (e.g., calculation, logic, interpretation).

       * A section on practical application or strategy, using crypto-specific examples (e.g., a hypothetical

         trade on BTC/USD).

       * A discussion of nuances, limitations, and risks.

       * A concluding summary.

   4. Explain the 'Why': Do not just state facts. Explain the underlying logic. For example, if discussing a

      formula, explain what each component represents and why it's included.

   5. Maintain an Expert Tone: Write in a clear, professional, and educational tone suitable for an audience of

      experienced traders and analysts. Avoid overly simplistic language.

   6. ONE QUESTION = ONE ANSWER: When you receive 100 questions, you must produce 100 separate answers, each

      meeting the 3,000+ character minimum. Do not consolidate multiple questions into comprehensive essays.

  Output Format:

  Please provide the answer as a single block of text, formatted in Markdown. This answer is for ONE question only."""

    def generate_answer(self, question: str, research_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive answer to a question
        
        Args:
            question: The question to answer
            research_context: Optional research data from research agent
            
        Returns:
            Dictionary with answer
        """
        # Build the user prompt
        user_prompt = f"{self.answer_prompt}\n\nQUESTION: {question}\n"
        
        # Add research context if available
        if research_context:
            research_notes = research_context.get("research_notes", "")
            if research_notes:
                user_prompt += f"\nRESEARCH CONTEXT:\n{research_notes}\n"
            
            key_concepts = research_context.get("key_concepts", [])
            if key_concepts:
                user_prompt += f"\nKEY CONCEPTS: {', '.join(key_concepts)}\n"
        
        user_prompt += "\nPlease provide your comprehensive answer now."
        
        try:
            print(f"    [GENERATING] Answer...")
            
            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": "You are an expert cryptocurrency and blockchain consultant with deep knowledge of trading, technical analysis, and market dynamics."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4096  # Adjust based on model limits
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Check length
            if len(answer) < 3000:
                print(f"    [WARNING] Answer is {len(answer)} chars (target: 3000+)")
                # Try to expand if too short
                if len(answer) < 2000:
                    expansion_prompt = f"""The following answer is too short. Please expand it to at least 3,000 characters by adding more detail, examples, and explanations.

CURRENT ANSWER:
{answer}

Please provide an expanded version with:
- More detailed explanations
- Additional practical examples
- More comprehensive coverage of nuances and edge cases
- Deeper analysis of the underlying mechanics"""
                    
                    expansion_response = self.client.chat.completions.create(
                        model="mixtral",
                        messages=[
                            {"role": "user", "content": expansion_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=4096
                    )
                    answer = expansion_response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "answer": answer,
                "length": len(answer),
                "meets_minimum": len(answer) >= 3000
            }
            
        except Exception as e:
            print(f"    [ERROR] Failed to generate answer: {e}")
            return {
                "success": False,
                "error": str(e),
                "answer": ""
            }

