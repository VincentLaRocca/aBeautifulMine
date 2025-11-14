"""
Multi-Agent Orchestrator
Coordinates all agents in the Q&A dataset creation pipeline
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

from .subtopic_generator import SubtopicGeneratorAgent
from .question_generator import QuestionGeneratorAgent
from .research_agent import ResearchAgent
from .answer_generator import AnswerGeneratorAgent
from .database_agent import DatabaseAgent

load_dotenv()


class MultiAgentOrchestrator:
    """
    Orchestrates the complete Q&A dataset creation pipeline:
    1. Topic → Subtopics → Task List
    2. Subtopic → 100 Questions
    3. Questions → Deep Research
    4. Questions → Answers (using your prompt)
    5. Q&A Pairs → Database
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the orchestrator with all agents
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._load_default_config()
        
        # Get domain configuration
        if "domain_config" in self.config:
            self.domain_config = self.config["domain_config"]
        elif "domain" in self.config:
            from .domain_config import get_domain_config
            self.domain_config = get_domain_config(self.config["domain"])
        else:
            from .domain_config import get_domain_config
            self.domain_config = get_domain_config("cryptocurrency")  # Default
        
        # Initialize all agents
        print("[INIT] Initializing agents...")
        print(f"[DOMAIN] Using domain: {self.domain_config.get('name', 'Unknown')}")
        self.subtopic_agent = SubtopicGeneratorAgent(
            model_url=self.config.get("model_url")
        )
        self.question_agent = QuestionGeneratorAgent(
            model_url=self.config.get("model_url"),
            questions_per_topic=self.config.get("questions_per_topic", 100)
        )
        self.research_agent = ResearchAgent(
            model_url=self.config.get("model_url"),
            domain_config=self.domain_config
        )
        self.answer_agent = AnswerGeneratorAgent(
            model_url=self.config.get("model_url"),
            answer_prompt=self.config.get("answer_prompt")
        )
        self.database_agent = DatabaseAgent(
            db_path=self.config.get("db_path")
        )
        
        # Pipeline state
        self.state = {
            "topic": None,
            "subtopics": [],
            "task_list_path": None,
            "current_subtopic": None,
            "questions": [],
            "research_results": {},
            "qa_pairs": [],
            "database_stats": {}
        }
        
        # Output directories
        self.output_dir = Path(self.config.get("output_dir", "multi_agent_output"))
        self.output_dir.mkdir(exist_ok=True)
        
        self.task_list_dir = self.output_dir / "task_lists"
        self.task_list_dir.mkdir(exist_ok=True)
        
        self.questions_dir = self.output_dir / "questions"
        self.questions_dir.mkdir(exist_ok=True)
        
        self.research_dir = self.output_dir / "research"
        self.research_dir.mkdir(exist_ok=True)
        
        self.answers_dir = self.output_dir / "answers"
        self.answers_dir.mkdir(exist_ok=True)
        
        print("[OK] All agents initialized")

    def _load_default_config(self) -> Dict:
        """Load default configuration"""
        return {
            "model_url": os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1"),
            "questions_per_topic": 100,
            "output_dir": "multi_agent_output",
            "db_path": "chroma_db",
            "answer_prompt": """Core Task:

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
        }

    def step1_generate_subtopics(self, topic: str) -> Dict[str, Any]:
        """
        Step 1: Generate subtopics from main topic and save to task list
        
        Args:
            topic: Main topic for the dataset
            
        Returns:
            Dictionary with subtopics and task list path
        """
        print("\n" + "="*80)
        print("STEP 1: GENERATING SUBTOPICS")
        print("="*80)
        print(f"Topic: {topic}")
        print()
        
        self.state["topic"] = topic
        
        # Generate subtopics
        result = self.subtopic_agent.generate_subtopics(topic)
        
        if not result["success"]:
            return result
        
        self.state["subtopics"] = result["subtopics"]
        
        # Save to task list file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.replace(' ', '_').lower()
        
        task_list_filename = f"{safe_topic}_task_list_{timestamp}.json"
        task_list_path = self.task_list_dir / task_list_filename
        
        task_list_data = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "subtopics": result["subtopics"],
            "total_subtopics": len(result["subtopics"]),
            "status": "pending"
        }
        
        with open(task_list_path, 'w', encoding='utf-8') as f:
            json.dump(task_list_data, f, indent=2, ensure_ascii=False)
        
        self.state["task_list_path"] = str(task_list_path)
        
        print(f"[OK] Generated {len(result['subtopics'])} subtopics")
        print(f"[SAVED] Task list: {task_list_path}")
        
        return {
            "success": True,
            "subtopics": result["subtopics"],
            "task_list_path": str(task_list_path),
            "total_subtopics": len(result["subtopics"])
        }

    def step2_generate_questions(self, subtopic: str, subtopic_index: int) -> Dict[str, Any]:
        """
        Step 2: Generate 100 questions for a subtopic
        
        Args:
            subtopic: The subtopic to generate questions for
            subtopic_index: Index of subtopic in the list
            
        Returns:
            Dictionary with questions
        """
        print("\n" + "="*80)
        print(f"STEP 2: GENERATING QUESTIONS ({subtopic_index + 1}/{len(self.state['subtopics'])})")
        print("="*80)
        print(f"Subtopic: {subtopic}")
        print()
        
        self.state["current_subtopic"] = subtopic
        
        # Generate questions
        result = self.question_agent.generate_questions(subtopic)
        
        if not result["success"]:
            return result
        
        questions = result["questions"]
        self.state["questions"] = questions
        
        # Save questions to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subtopic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in subtopic)
        safe_subtopic = safe_subtopic.replace(' ', '_').lower()
        
        questions_filename = f"{safe_subtopic}_questions_{timestamp}.json"
        questions_path = self.questions_dir / questions_filename
        
        questions_data = {
            "topic": self.state["topic"],
            "subtopic": subtopic,
            "subtopic_index": subtopic_index,
            "generated_at": datetime.now().isoformat(),
            "questions": questions,
            "total_questions": len(questions),
            "status": "pending_research"
        }
        
        with open(questions_path, 'w', encoding='utf-8') as f:
            json.dump(questions_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Generated {len(questions)} questions")
        print(f"[SAVED] Questions: {questions_path}")
        
        return {
            "success": True,
            "questions": questions,
            "questions_path": str(questions_path),
            "total_questions": len(questions)
        }

    def step3_research_questions(self, questions: List[str], subtopic: str) -> Dict[str, Any]:
        """
        Step 3: Perform deep research on questions
        
        Args:
            questions: List of questions to research
            subtopic: The subtopic these questions belong to
            
        Returns:
            Dictionary with research results
        """
        print("\n" + "="*80)
        print("STEP 3: DEEP RESEARCH")
        print("="*80)
        print(f"Researching {len(questions)} questions for: {subtopic}")
        print()
        
        research_results = {}
        
        for i, question in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] Researching: {question[:60]}...")
            
            result = self.research_agent.research_question(question)
            
            if result["success"]:
                research_results[question] = result["research_data"]
                print(f"  [OK] Research complete")
            else:
                print(f"  [WARNING] Research failed: {result.get('error', 'Unknown error')}")
                research_results[question] = {"error": result.get("error", "Research failed")}
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        # Save research results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subtopic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in subtopic)
        safe_subtopic = safe_subtopic.replace(' ', '_').lower()
        
        research_filename = f"{safe_subtopic}_research_{timestamp}.json"
        research_path = self.research_dir / research_filename
        
        research_data = {
            "topic": self.state["topic"],
            "subtopic": subtopic,
            "generated_at": datetime.now().isoformat(),
            "questions": questions,
            "research_results": research_results,
            "status": "ready_for_answers"
        }
        
        with open(research_path, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)
        
        self.state["research_results"][subtopic] = research_results
        
        print(f"\n[OK] Research complete for {len(questions)} questions")
        print(f"[SAVED] Research: {research_path}")
        
        return {
            "success": True,
            "research_results": research_results,
            "research_path": str(research_path)
        }

    def step4_generate_answers(self, questions: List[str], research_results: Dict[str, Any], subtopic: str) -> Dict[str, Any]:
        """
        Step 4: Generate answers using your specific prompt
        
        Args:
            questions: List of questions
            research_results: Research data for each question
            subtopic: The subtopic
            
        Returns:
            Dictionary with Q&A pairs
        """
        print("\n" + "="*80)
        print("STEP 4: GENERATING ANSWERS")
        print("="*80)
        print(f"Generating answers for {len(questions)} questions")
        print()
        
        qa_pairs = []
        
        for i, question in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] Generating answer: {question[:60]}...")
            
            # Get research context if available
            research_context = research_results.get(question, {})
            
            # Generate answer
            result = self.answer_agent.generate_answer(
                question=question,
                research_context=research_context
            )
            
            if result["success"]:
                qa_pair = {
                    "question": question,
                    "answer": result["answer"],
                    "subtopic": subtopic,
                    "topic": self.state["topic"],
                    "answer_length": len(result["answer"]),
                    "generated_at": datetime.now().isoformat()
                }
                qa_pairs.append(qa_pair)
                print(f"  [OK] Answer generated ({len(result['answer'])} chars)")
            else:
                print(f"  [ERROR] Failed: {result.get('error', 'Unknown error')}")
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        # Save Q&A pairs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subtopic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in subtopic)
        safe_subtopic = safe_subtopic.replace(' ', '_').lower()
        
        answers_filename = f"{safe_subtopic}_qa_pairs_{timestamp}.json"
        answers_path = self.answers_dir / answers_filename
        
        qa_data = {
            "topic": self.state["topic"],
            "subtopic": subtopic,
            "generated_at": datetime.now().isoformat(),
            "qa_pairs": qa_pairs,
            "total_pairs": len(qa_pairs),
            "status": "ready_for_database"
        }
        
        with open(answers_path, 'w', encoding='utf-8') as f:
            json.dump(qa_data, f, indent=2, ensure_ascii=False)
        
        self.state["qa_pairs"].extend(qa_pairs)
        
        print(f"\n[OK] Generated {len(qa_pairs)} Q&A pairs")
        print(f"[SAVED] Q&A pairs: {answers_path}")
        
        return {
            "success": True,
            "qa_pairs": qa_pairs,
            "answers_path": str(answers_path),
            "total_pairs": len(qa_pairs)
        }

    def step5_insert_to_database(self, qa_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Step 5: Insert Q&A pairs into RAG database
        
        Args:
            qa_pairs: List of Q&A pair dictionaries
            
        Returns:
            Dictionary with database stats
        """
        print("\n" + "="*80)
        print("STEP 5: INSERTING TO DATABASE")
        print("="*80)
        print(f"Inserting {len(qa_pairs)} Q&A pairs")
        print()
        
        result = self.database_agent.insert_qa_pairs(qa_pairs)
        
        if not result["success"]:
            return result
        
        self.state["database_stats"] = result["stats"]
        
        print(f"[OK] Inserted {result['stats']['inserted']} pairs")
        print(f"[STATS] Total in database: {result['stats']['total_in_db']}")
        
        return result

    def run_full_pipeline(self, topic: str, start_from_subtopic: Optional[int] = None) -> Dict[str, Any]:
        """
        Run the complete pipeline from topic to database
        
        Args:
            topic: Main topic
            start_from_subtopic: Optional subtopic index to resume from
            
        Returns:
            Complete pipeline results
        """
        print("\n" + "="*80)
        print("MULTI-AGENT Q&A DATASET PIPELINE")
        print("="*80)
        print(f"Topic: {topic}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        pipeline_results = {
            "topic": topic,
            "started_at": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 1: Generate subtopics
            step1_result = self.step1_generate_subtopics(topic)
            pipeline_results["steps"]["step1_subtopics"] = step1_result
            
            if not step1_result["success"]:
                return pipeline_results
            
            subtopics = step1_result["subtopics"]
            start_idx = start_from_subtopic or 0
            
            # Process each subtopic
            for idx, subtopic in enumerate(subtopics[start_idx:], start=start_idx):
                print(f"\n{'='*80}")
                print(f"PROCESSING SUBTOPIC {idx + 1}/{len(subtopics)}: {subtopic}")
                print(f"{'='*80}\n")
                
                # Save checkpoint before processing each subtopic
                self.state["current_subtopic_index"] = idx
                try:
                    import sys
                    from pathlib import Path
                    sys.path.insert(0, str(Path(__file__).parent.parent))
                    from save_checkpoint import save_checkpoint
                    checkpoint_file = save_checkpoint(self.state, self.output_dir)
                    print(f"[CHECKPOINT] Saved: {checkpoint_file.name}")
                except Exception as e:
                    pass  # Don't fail if checkpoint save fails
                
                # Step 2: Generate questions
                step2_result = self.step2_generate_questions(subtopic, idx)
                pipeline_results["steps"][f"subtopic_{idx}_questions"] = step2_result
                
                if not step2_result["success"]:
                    print(f"[ERROR] Failed to generate questions for subtopic {idx}")
                    continue
                
                questions = step2_result["questions"]
                
                # Step 3: Research questions
                step3_result = self.step3_research_questions(questions, subtopic)
                pipeline_results["steps"][f"subtopic_{idx}_research"] = step3_result
                
                if not step3_result["success"]:
                    print(f"[WARNING] Research incomplete for subtopic {idx}")
                
                research_results = step3_result.get("research_results", {})
                
                # Step 4: Generate answers
                step4_result = self.step4_generate_answers(questions, research_results, subtopic)
                pipeline_results["steps"][f"subtopic_{idx}_answers"] = step4_result
                
                if not step4_result["success"]:
                    print(f"[ERROR] Failed to generate answers for subtopic {idx}")
                    continue
                
                qa_pairs = step4_result["qa_pairs"]
                
                # Step 5: Insert to database (batch insert at end, or insert incrementally)
                step5_result = self.step5_insert_to_database(qa_pairs)
                pipeline_results["steps"][f"subtopic_{idx}_database"] = step5_result
            
            # Final database stats
            pipeline_results["completed_at"] = datetime.now().isoformat()
            pipeline_results["final_stats"] = {
                "total_subtopics": len(subtopics),
                "total_qa_pairs": len(self.state["qa_pairs"]),
                "database_stats": self.state["database_stats"]
            }
            
            print("\n" + "="*80)
            print("PIPELINE COMPLETE")
            print("="*80)
            print(f"Total Q&A pairs created: {len(self.state['qa_pairs'])}")
            print(f"Database stats: {self.state['database_stats']}")
            print("="*80)
            
        except Exception as e:
            print(f"\n[ERROR] Pipeline failed: {e}")
            pipeline_results["error"] = str(e)
            pipeline_results["failed_at"] = datetime.now().isoformat()
        
        return pipeline_results


def main():
    """CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <topic> [start_from_subtopic_index]")
        print()
        print("Example:")
        print('  python orchestrator.py "Cryptocurrency Technical Analysis"')
        print('  python orchestrator.py "DeFi Protocols" 5  # Resume from subtopic 5')
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
    start_from = int(sys.argv[-1]) if sys.argv[-1].isdigit() else None
    
    orchestrator = MultiAgentOrchestrator()
    results = orchestrator.run_full_pipeline(topic, start_from_subtopic=start_from)
    
    # Save results
    results_path = orchestrator.output_dir / f"pipeline_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVED] Pipeline results: {results_path}")


if __name__ == "__main__":
    main()

