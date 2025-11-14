"""
RAG-Based Research Agent
Uses Retrieval-Augmented Generation with ChromaDB or training data
Searches curated knowledge base for relevant information
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ResearchAgentRAG:
    """
    Research agent that uses RAG (Retrieval-Augmented Generation)
    Searches curated knowledge base instead of the web
    """

    def __init__(
        self,
        model_url: Optional[str] = None,
        domain_config: Optional[Dict] = None,
        knowledge_base_path: Optional[str] = None,
        db_path: str = "chroma_db",
        collection_name: str = "qa_dataset",
        max_context_examples: int = 5
    ):
        """
        Initialize RAG-based research agent

        Args:
            model_url: URL of the LLM server
            domain_config: Domain configuration dictionary
            knowledge_base_path: Path to training data JSONL file
            db_path: Path to ChromaDB directory
            collection_name: ChromaDB collection name
            max_context_examples: Maximum examples to include
        """
        self.model_url = model_url or os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
        self.max_context_examples = max_context_examples

        self.client = OpenAI(
            base_url=self.model_url,
            api_key="not-needed"
        )

        # Domain configuration
        self.domain_config = domain_config
        if self.domain_config is None:
            from .domain_config import get_domain_config
            self.domain_config = get_domain_config("cryptocurrency")

        # Try to load from ChromaDB first, then fall back to JSONL
        self.rag_retriever = None
        self.knowledge_base = []

        try:
            import chromadb
            db_path_obj = Path(db_path)
            if db_path_obj.exists():
                print(f"  [RAG] Loading from ChromaDB: {db_path}/{collection_name}")
                chroma_client = chromadb.PersistentClient(path=str(db_path_obj))
                collections = chroma_client.list_collections()

                if any(c.name == collection_name for c in collections):
                    self.rag_retriever = chroma_client.get_collection(name=collection_name)
                    print(f"  [RAG] ChromaDB collection loaded: {self.rag_retriever.count()} items")
                else:
                    print(f"  [RAG] Collection '{collection_name}' not found in ChromaDB")
        except Exception as e:
            print(f"  [RAG] ChromaDB not available: {e}")

        # Fall back to JSONL knowledge base
        if not self.rag_retriever:
            if knowledge_base_path:
                kb_path = Path(knowledge_base_path)
            else:
                # Try to find any training data file
                kb_path = Path("compiled_datasets")
                if kb_path.exists():
                    jsonl_files = list(kb_path.glob("*.jsonl"))
                    if jsonl_files:
                        kb_path = jsonl_files[0]  # Use first available
                    else:
                        kb_path = None
                else:
                    kb_path = None

            if kb_path and kb_path.exists():
                print(f"  [RAG] Loading from JSONL: {kb_path}")
                self.knowledge_base = self._load_knowledge_base(str(kb_path))
                print(f"  [RAG] Loaded {len(self.knowledge_base)} Q&A pairs")
            else:
                print(f"  [RAG] No knowledge base found. RAG will not be available.")

    def _load_knowledge_base(self, path: str) -> List[Dict]:
        """Load training data from JSONL file"""
        knowledge = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    knowledge.append(json.loads(line))
        return knowledge

    def research_question(self, question: str, subtopic: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform research using RAG

        Args:
            question: The question to research
            subtopic: Optional subtopic for context

        Returns:
            Dictionary with research data
        """
        # Retrieve relevant context from knowledge base
        context = self._retrieve_context(question, subtopic)

        if not context:
            print(f"  [RAG] No relevant context found, using LLM only")
            return self._research_without_rag(question)

        # Use domain-specific prompts with RAG context
        from .domain_config import get_research_prompt, get_research_user_prompt_template

        system_prompt = get_research_prompt(self.domain_config)
        user_prompt_template = get_research_user_prompt_template(self.domain_config)

        # Enhance user prompt with RAG context
        rag_context_text = self._format_context(context)
        enhanced_prompt = f"""Question to research: {question}

Retrieved knowledge from database:
{rag_context_text}

Based on the above knowledge and your understanding, provide comprehensive research notes for this question."""

        try:
            print(f"  [RAG RESEARCH] {question[:60]}... (using {len(context)} examples)")

            response = self.client.chat.completions.create(
                model="mixtral",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": enhanced_prompt}
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
                "rag_context_used": True,
                "rag_examples_count": len(context)
            }

            return {
                "success": True,
                "research_data": research_data
            }

        except Exception as e:
            print(f"  [ERROR] RAG research failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "research_data": {}
            }

    def _retrieve_context(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve relevant context from knowledge base"""
        if self.rag_retriever:
            return self._retrieve_from_chromadb(question, subtopic)
        elif self.knowledge_base:
            return self._retrieve_from_jsonl(question, subtopic)
        else:
            return []

    def _retrieve_from_chromadb(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve from ChromaDB"""
        try:
            # Create query with subtopic if available
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
                        'answer': doc,
                        'topic': metadata.get('topic', ''),
                        'subtopic': metadata.get('subtopic', '')
                    })

            return context

        except Exception as e:
            print(f"  [ERROR] ChromaDB retrieval failed: {e}")
            return []

    def _retrieve_from_jsonl(self, question: str, subtopic: Optional[str] = None) -> List[Dict]:
        """Retrieve from JSONL knowledge base using simple keyword matching"""
        from rank_bm25 import BM25Okapi
        import re

        # Prepare documents for BM25
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
                # Tokenize for BM25
                doc_text = f"{q_text} {a_text}"
                tokenized = re.findall(r'\w+', doc_text.lower())
                documents.append(tokenized)
                qa_pairs.append({'question': q_text, 'answer': a_text})

        if not documents:
            return []

        # Create BM25 index
        bm25 = BM25Okapi(documents)

        # Tokenize query
        query_text = f"{subtopic} {question}" if subtopic else question
        tokenized_query = re.findall(r'\w+', query_text.lower())

        # Get top results
        scores = bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:self.max_context_examples]

        context = [qa_pairs[i] for i in top_indices if scores[i] > 0]

        return context

    def _format_context(self, context: List[Dict]) -> str:
        """Format retrieved context for prompt"""
        formatted = []
        for i, item in enumerate(context, 1):
            formatted.append(f"Example {i}:")
            formatted.append(f"Q: {item.get('question', '')}")
            formatted.append(f"A: {item.get('answer', '')[:500]}...")  # Truncate long answers
            formatted.append("")

        return "\n".join(formatted)

    def _research_without_rag(self, question: str) -> Dict[str, Any]:
        """Fall back to LLM-only research if RAG unavailable"""
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
                "rag_context_used": False
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
