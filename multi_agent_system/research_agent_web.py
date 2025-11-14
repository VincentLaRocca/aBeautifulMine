"""
Web Search-Based Research Agent
Uses real-time web search to gather current information
Synthesizes information from multiple web sources
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ResearchAgentWeb:
    """
    Research agent that uses web search for real-time information
    Performs web searches and synthesizes results
    """

    def __init__(
        self,
        model_url: Optional[str] = None,
        domain_config: Optional[Dict] = None,
        search_provider: str = "auto",
        max_search_results: int = 5
    ):
        """
        Initialize web search-based research agent

        Args:
            model_url: URL of the LLM server
            domain_config: Domain configuration dictionary
            search_provider: Search provider ("auto", "brave", "google", "duckduckgo")
            max_search_results: Maximum search results to retrieve
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        self.search_provider = search_provider
        self.max_search_results = max_search_results

        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )

        # Domain configuration
        self.domain_config = domain_config
        if self.domain_config is None:
            from .domain_config import get_domain_config
            self.domain_config = get_domain_config("cryptocurrency")

        # Import web search with fallback
        try:
            from .web_search import web_search
            self.web_search = web_search
            self.web_search_available = True
            print(f"  [WEB] Web search enabled (provider: {search_provider})")
        except ImportError:
            print(f"  [WEB] Web search not available (web_search.py not found)")
            self.web_search = None
            self.web_search_available = False

    def research_question(self, question: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform research using web search

        Args:
            question: The question to research
            subtopic: Optional subtopic for context

        Returns:
            Dictionary with research data
        """
        if not self.web_search_available:
            print(f"  [ERROR] Web search not available")
            return {
                "success": False,
                "error": "Web search module not available",
                "research_data": {}
            }

        # Perform web search
        search_results = self._perform_search(question, subtopic)

        if not search_results:
            print(f"  [WEB] No search results found, using LLM only")
            return self._research_without_web(question)

        # Synthesize search results using LLM
        return self._synthesize_search_results(question, subtopic, search_results)

    def _perform_search(self, question: str, subtopic: Optional[str] = None) -> Optional[List[Dict]]:
        """Perform web search"""
        if not self.web_search:
            return None

        # Construct search query
        domain_name = self.domain_config.get('name', 'general')
        if subtopic:
            search_query = f"{domain_name} {subtopic} {question}"
        else:
            search_query = f"{domain_name} {question}"

        # Perform search
        try:
            results = self.web_search(
                query=search_query,
                count=self.max_search_results,
                provider=self.search_provider
            )
            return results
        except Exception as e:
            print(f"  [ERROR] Web search failed: {e}")
            return None

    def _synthesize_search_results(
        self,
        question: str,
        subtopic: Optional[str],
        search_results: List[Dict]
    ) -> Dict[str, Any]:
        """Synthesize search results using LLM"""
        # Format search results
        search_context = self._format_search_results(search_results)

        # Use domain-specific prompts
        from .domain_config import get_research_prompt, get_research_user_prompt_template

        system_prompt = get_research_prompt(self.domain_config)

        # Enhance system prompt for web search synthesis
        system_prompt += """

You are now synthesizing information from web search results. Your task is to:
1. Analyze the search results provided
2. Extract key facts, concepts, and insights
3. Synthesize the information into comprehensive research notes
4. Cite sources when referencing specific information
5. Note any conflicting information or varying perspectives"""

        user_prompt = f"""Question to research: {question}
{f"Subtopic: {subtopic}" if subtopic else ""}

Web search results:
{search_context}

Based on these web search results, provide comprehensive research notes that:
- Summarize key findings
- Identify important concepts and terminology
- Note any patterns or consensus across sources
- Highlight any conflicting views
- Extract actionable insights

Format your research notes clearly with key concepts, definitions, and supporting information."""

        try:
            print(f"  [WEB RESEARCH] {question[:60]}... (synthesizing {len(search_results)} sources)")

            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2048
            )

            research_content = response.choices[0].message.content.strip()

            # Structure the research data
            research_data = {
                "question": question,
                "research_notes": research_content,
                "key_concepts": self._extract_key_concepts(research_content),
                "research_length": len(research_content),
                "web_search_used": True,
                "sources_count": len(search_results),
                "sources": [
                    {
                        "title": r.get('title', ''),
                        "url": r.get('url', ''),
                        "snippet": r.get('snippet', '')[:200]
                    }
                    for r in search_results
                ]
            }

            return {
                "success": True,
                "research_data": research_data
            }

        except Exception as e:
            print(f"  [ERROR] Web research synthesis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "research_data": {}
            }

    def _format_search_results(self, search_results: List[Dict]) -> str:
        """Format search results for LLM prompt"""
        formatted = []

        for i, result in enumerate(search_results, 1):
            formatted.append(f"Source {i}:")
            formatted.append(f"Title: {result.get('title', 'N/A')}")
            formatted.append(f"URL: {result.get('url', 'N/A')}")
            formatted.append(f"Content: {result.get('snippet', result.get('content', 'N/A'))}")
            formatted.append("")

        return "\n".join(formatted)

    def _research_without_web(self, question: str) -> Dict[str, Any]:
        """Fall back to LLM-only research if web search fails"""
        from .domain_config import get_research_prompt, get_research_user_prompt_template

        system_prompt = get_research_prompt(self.domain_config)
        user_prompt_template = get_research_user_prompt_template(self.domain_config)
        user_prompt = user_prompt_template.format(question=question)

        try:
            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2048
            )

            research_content = response.choices[0].message.content.strip()

            research_data = {
                "question": question,
                "research_notes": research_content,
                "key_concepts": self._extract_key_concepts(research_content),
                "research_length": len(research_content),
                "web_search_used": False
            }

            return {
                "success": True,
                "research_data": research_data
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "research_data": {}
            }

    def _extract_key_concepts(self, research_content: str) -> List[str]:
        """Extract key concepts from research content"""
        import re

        concepts = []

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
