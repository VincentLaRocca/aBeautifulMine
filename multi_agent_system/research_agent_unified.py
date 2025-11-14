"""
Unified Research Agent
Single agent that can use either RAG or Web Search based on configuration
Provides flexible research capability with automatic fallback
"""

import os
from typing import Dict, List, Optional, Any, Literal
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class UnifiedResearchAgent:
    """
    Unified research agent that supports multiple research methods:
    - RAG: Retrieval from curated knowledge base (ChromaDB or JSONL)
    - WEB: Real-time web search
    - HYBRID: Combines both RAG and web search
    """

    def __init__(
        self,
        model_url: Optional[str] = None,
        domain_config: Optional[Dict] = None,
        research_mode: Literal["rag", "web", "hybrid"] = "rag",
        # RAG parameters
        knowledge_base_path: Optional[str] = None,
        db_path: str = "chroma_db",
        collection_name: str = "qa_dataset",
        max_context_examples: int = 5,
        # Web search parameters
        search_provider: str = "auto",
        max_search_results: int = 5
    ):
        """
        Initialize unified research agent

        Args:
            model_url: URL of the LLM server
            domain_config: Domain configuration dictionary
            research_mode: Research method ("rag", "web", or "hybrid")
            knowledge_base_path: Path to training data JSONL file (for RAG)
            db_path: Path to ChromaDB directory (for RAG)
            collection_name: ChromaDB collection name (for RAG)
            max_context_examples: Maximum examples to include (for RAG)
            search_provider: Search provider for web search ("auto", "brave", "google", "duckduckgo")
            max_search_results: Maximum search results to retrieve (for web)
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        self.research_mode = research_mode
        self.max_context_examples = max_context_examples
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

        print(f"  [RESEARCH] Initializing Unified Research Agent (mode: {research_mode})")

        # Initialize RAG components if needed
        self.rag_available = False
        self.rag_retriever = None
        self.knowledge_base = []

        if research_mode in ["rag", "hybrid"]:
            self._initialize_rag(db_path, collection_name, knowledge_base_path)

        # Initialize web search if needed
        self.web_search_available = False
        self.web_search = None

        if research_mode in ["web", "hybrid"]:
            self._initialize_web_search()

        # Log availability
        print(f"  [RESEARCH] RAG available: {self.rag_available}")
        print(f"  [RESEARCH] Web search available: {self.web_search_available}")

    def _initialize_rag(
        self,
        db_path: str,
        collection_name: str,
        knowledge_base_path: Optional[str]
    ):
        """Initialize RAG components"""
        # Try ChromaDB first
        try:
            import chromadb
            db_path_obj = Path(db_path)
            if db_path_obj.exists():
                chroma_client = chromadb.PersistentClient(path=str(db_path_obj))
                collections = chroma_client.list_collections()

                if any(c.name == collection_name for c in collections):
                    self.rag_retriever = chroma_client.get_collection(name=collection_name)
                    self.rag_available = True
                    print(f"  [RAG] Loaded ChromaDB: {self.rag_retriever.count()} items")
                    return
        except Exception as e:
            print(f"  [RAG] ChromaDB not available: {e}")

        # Fall back to JSONL knowledge base
        if knowledge_base_path:
            kb_path = Path(knowledge_base_path)
        else:
            # Try to find any training data file
            kb_path = Path("compiled_datasets")
            if kb_path.exists():
                jsonl_files = list(kb_path.glob("*.jsonl"))
                if jsonl_files:
                    kb_path = jsonl_files[0]
                else:
                    kb_path = None
            else:
                kb_path = None

        if kb_path and kb_path.exists():
            import json
            print(f"  [RAG] Loading JSONL: {kb_path}")
            with open(kb_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.knowledge_base.append(json.loads(line))
            self.rag_available = True
            print(f"  [RAG] Loaded {len(self.knowledge_base)} Q&A pairs")

    def _initialize_web_search(self):
        """Initialize web search"""
        try:
            from .web_search import web_search
            self.web_search = web_search
            self.web_search_available = True
            print(f"  [WEB] Web search enabled (provider: {self.search_provider})")
        except ImportError:
            print(f"  [WEB] Web search not available (install required packages)")

    def research_question(
        self,
        question: str,
        subtopic: Optional[str] = None,
        override_mode: Optional[Literal["rag", "web", "hybrid"]] = None
    ) -> Dict[str, Any]:
        """
        Perform research on a question

        Args:
            question: The question to research
            subtopic: Optional subtopic for context
            override_mode: Override the default research mode for this query

        Returns:
            Dictionary with research data
        """
        mode = override_mode or self.research_mode

        # Route to appropriate research method
        if mode == "rag":
            return self._research_rag(question, subtopic)
        elif mode == "web":
            return self._research_web(question, subtopic)
        elif mode == "hybrid":
            return self._research_hybrid(question, subtopic)
        else:
            return {
                "success": False,
                "error": f"Invalid research mode: {mode}",
                "research_data": {}
            }

    def _research_rag(self, question: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        """Research using RAG"""
        if not self.rag_available:
            print(f"  [RAG] Not available, falling back to LLM only")
            return self._research_llm_only(question)

        # Retrieve relevant context
        context = self._retrieve_rag_context(question, subtopic)

        if not context:
            print(f"  [RAG] No relevant context found")
            return self._research_llm_only(question)

        # Format context and create prompt
        rag_context_text = self._format_rag_context(context)

        from .domain_config import get_research_prompt

        system_prompt = get_research_prompt(self.domain_config)
        user_prompt = f"""Question to research: {question}
{f"Subtopic: {subtopic}" if subtopic else ""}

Retrieved knowledge from database:
{rag_context_text}

Based on the above knowledge, provide comprehensive research notes for this question."""

        try:
            print(f"  [RAG] Researching with {len(context)} examples")

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

            return {
                "success": True,
                "research_data": {
                    "question": question,
                    "research_notes": research_content,
                    "key_concepts": self._extract_key_concepts(research_content),
                    "research_length": len(research_content),
                    "research_method": "rag",
                    "rag_examples_count": len(context)
                }
            }

        except Exception as e:
            print(f"  [ERROR] RAG research failed: {e}")
            return {"success": False, "error": str(e), "research_data": {}}

    def _research_web(self, question: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        """Research using web search"""
        if not self.web_search_available:
            print(f"  [WEB] Not available, falling back to LLM only")
            return self._research_llm_only(question)

        # Perform web search
        search_results = self._perform_web_search(question, subtopic)

        if not search_results:
            print(f"  [WEB] No search results found")
            return self._research_llm_only(question)

        # Synthesize search results
        search_context = self._format_web_results(search_results)

        from .domain_config import get_research_prompt

        system_prompt = get_research_prompt(self.domain_config)
        system_prompt += """

You are synthesizing information from web search results. Extract key facts, concepts, and insights."""

        user_prompt = f"""Question to research: {question}
{f"Subtopic: {subtopic}" if subtopic else ""}

Web search results:
{search_context}

Based on these web search results, provide comprehensive research notes."""

        try:
            print(f"  [WEB] Researching with {len(search_results)} sources")

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

            return {
                "success": True,
                "research_data": {
                    "question": question,
                    "research_notes": research_content,
                    "key_concepts": self._extract_key_concepts(research_content),
                    "research_length": len(research_content),
                    "research_method": "web",
                    "sources_count": len(search_results),
                    "sources": [{"title": r.get('title', ''), "url": r.get('url', '')} for r in search_results]
                }
            }

        except Exception as e:
            print(f"  [ERROR] Web research failed: {e}")
            return {"success": False, "error": str(e), "research_data": {}}

    def _research_hybrid(self, question: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        """Research using both RAG and web search"""
        rag_context = []
        web_results = []

        # Try RAG first
        if self.rag_available:
            rag_context = self._retrieve_rag_context(question, subtopic)

        # Try web search
        if self.web_search_available:
            web_results = self._perform_web_search(question, subtopic)

        # Check if we have any data
        if not rag_context and not web_results:
            print(f"  [HYBRID] No data from either source")
            return self._research_llm_only(question)

        # Combine both sources
        combined_context = ""

        if rag_context:
            combined_context += "=== Knowledge Base Context ===\n"
            combined_context += self._format_rag_context(rag_context)
            combined_context += "\n\n"

        if web_results:
            combined_context += "=== Web Search Results ===\n"
            combined_context += self._format_web_results(web_results)

        from .domain_config import get_research_prompt

        system_prompt = get_research_prompt(self.domain_config)
        system_prompt += """

You are synthesizing information from both a curated knowledge base and web search results. Combine insights from both sources."""

        user_prompt = f"""Question to research: {question}
{f"Subtopic: {subtopic}" if subtopic else ""}

{combined_context}

Based on the above information from both the knowledge base and web search, provide comprehensive research notes."""

        try:
            print(f"  [HYBRID] Researching with {len(rag_context)} KB examples + {len(web_results)} web sources")

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

            return {
                "success": True,
                "research_data": {
                    "question": question,
                    "research_notes": research_content,
                    "key_concepts": self._extract_key_concepts(research_content),
                    "research_length": len(research_content),
                    "research_method": "hybrid",
                    "rag_examples_count": len(rag_context),
                    "sources_count": len(web_results)
                }
            }

        except Exception as e:
            print(f"  [ERROR] Hybrid research failed: {e}")
            return {"success": False, "error": str(e), "research_data": {}}

    def _retrieve_rag_context(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve context from RAG"""
        if self.rag_retriever:
            return self._retrieve_from_chromadb(question, subtopic)
        elif self.knowledge_base:
            return self._retrieve_from_jsonl(question, subtopic)
        return []

    def _retrieve_from_chromadb(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve from ChromaDB"""
        try:
            query_text = f"{subtopic}: {question}" if subtopic else question
            results = self.rag_retriever.query(
                query_texts=[query_text],
                n_results=self.max_context_examples
            )

            context = []
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                    context.append({
                        'question': metadata.get('question', ''),
                        'answer': doc
                    })
            return context
        except Exception as e:
            print(f"  [ERROR] ChromaDB retrieval failed: {e}")
            return []

    def _retrieve_from_jsonl(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve from JSONL using BM25"""
        try:
            from rank_bm25 import BM25Okapi
            import re

            documents = []
            qa_pairs = []

            for example in self.knowledge_base:
                messages = example.get('messages', [])
                q_text = ""
                a_text = ""

                for msg in messages:
                    if msg.get('role') == 'user':
                        q_text = msg.get('content', '')
                    elif msg.get('role') == 'assistant':
                        a_text = msg.get('content', '')

                if q_text and a_text:
                    doc_text = f"{q_text} {a_text}"
                    tokenized = re.findall(r'\w+', doc_text.lower())
                    documents.append(tokenized)
                    qa_pairs.append({'question': q_text, 'answer': a_text})

            if not documents:
                return []

            bm25 = BM25Okapi(documents)
            query_text = f"{subtopic} {question}" if subtopic else question
            tokenized_query = re.findall(r'\w+', query_text.lower())
            scores = bm25.get_scores(tokenized_query)
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:self.max_context_examples]

            return [qa_pairs[i] for i in top_indices if scores[i] > 0]

        except Exception as e:
            print(f"  [ERROR] JSONL retrieval failed: {e}")
            return []

    def _perform_web_search(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Perform web search"""
        if not self.web_search:
            return []

        domain_name = self.domain_config.get('name', 'general')
        search_query = f"{domain_name} {subtopic} {question}" if subtopic else f"{domain_name} {question}"

        try:
            results = self.web_search(
                query=search_query,
                count=self.max_search_results,
                provider=self.search_provider
            )
            return results or []
        except Exception as e:
            print(f"  [ERROR] Web search failed: {e}")
            return []

    def _format_rag_context(self, context: List[Dict]) -> str:
        """Format RAG context"""
        formatted = []
        for i, item in enumerate(context, 1):
            formatted.append(f"Example {i}:")
            formatted.append(f"Q: {item.get('question', '')}")
            formatted.append(f"A: {item.get('answer', '')[:500]}...")
            formatted.append("")
        return "\n".join(formatted)

    def _format_web_results(self, results: List[Dict]) -> str:
        """Format web search results"""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"Source {i}:")
            formatted.append(f"Title: {result.get('title', 'N/A')}")
            formatted.append(f"URL: {result.get('url', 'N/A')}")
            formatted.append(f"Content: {result.get('snippet', result.get('content', 'N/A'))}")
            formatted.append("")
        return "\n".join(formatted)

    def _research_llm_only(self, question: str) -> Dict[str, Any]:
        """Fall back to LLM-only research"""
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

            return {
                "success": True,
                "research_data": {
                    "question": question,
                    "research_notes": research_content,
                    "key_concepts": self._extract_key_concepts(research_content),
                    "research_length": len(research_content),
                    "research_method": "llm_only"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e), "research_data": {}}

    def _extract_key_concepts(self, research_content: str) -> List[str]:
        """Extract key concepts"""
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
        return list(dict.fromkeys(concepts))[:10]
