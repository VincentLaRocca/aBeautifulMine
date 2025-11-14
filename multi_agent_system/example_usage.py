"""
Example usage of the Multi-Agent System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system.orchestrator import MultiAgentOrchestrator
import json

def example_full_pipeline():
    """Run the complete pipeline"""
    print("="*80)
    print("EXAMPLE: Full Pipeline")
    print("="*80)
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Run full pipeline
    topic = "Cryptocurrency Technical Analysis"
    results = orchestrator.run_full_pipeline(topic)
    
    # Save results
    print("\n[SAVED] Results saved to pipeline output directory")
    return results


def example_step_by_step():
    """Run step by step"""
    print("="*80)
    print("EXAMPLE: Step by Step")
    print("="*80)
    
    orchestrator = MultiAgentOrchestrator()
    
    # Step 1: Generate subtopics
    print("\n--- Step 1: Generating Subtopics ---")
    step1 = orchestrator.step1_generate_subtopics("Cryptocurrency Trading Strategies")
    
    if not step1["success"]:
        print("Failed to generate subtopics")
        return
    
    print(f"Generated {step1['total_subtopics']} subtopics")
    
    # Step 2: Generate questions for first subtopic
    if step1["subtopics"]:
        print("\n--- Step 2: Generating Questions ---")
        first_subtopic = step1["subtopics"][0]
        step2 = orchestrator.step2_generate_questions(first_subtopic, subtopic_index=0)
        
        if step2["success"]:
            print(f"Generated {step2['total_questions']} questions")
            
            # Step 3: Research (optional - can skip for faster testing)
            print("\n--- Step 3: Researching Questions ---")
            step3 = orchestrator.step3_research_questions(
                step2["questions"][:5],  # Just research first 5 for example
                first_subtopic
            )
            
            if step3["success"]:
                # Step 4: Generate answers
                print("\n--- Step 4: Generating Answers ---")
                step4 = orchestrator.step4_generate_answers(
                    step2["questions"][:5],  # Just answer first 5 for example
                    step3["research_results"],
                    first_subtopic
                )
                
                if step4["success"]:
                    print(f"Generated {step4['total_pairs']} Q&A pairs")
                    
                    # Step 5: Insert to database
                    print("\n--- Step 5: Inserting to Database ---")
                    step5 = orchestrator.step5_insert_to_database(step4["qa_pairs"])
                    
                    if step5["success"]:
                        print(f"Inserted {step5['stats']['inserted']} pairs")


def example_custom_config():
    """Example with custom configuration"""
    print("="*80)
    print("EXAMPLE: Custom Configuration")
    print("="*80)
    
    custom_config = {
        "model_url": "http://localhost:8080/v1",
        "questions_per_topic": 50,  # Fewer questions for testing
        "output_dir": "custom_output",
        "db_path": "custom_chromadb"
    }
    
    orchestrator = MultiAgentOrchestrator(config=custom_config)
    
    # Use as normal
    results = orchestrator.step1_generate_subtopics("DeFi Protocols")
    print(f"Generated {results.get('total_subtopics', 0)} subtopics")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "full":
            example_full_pipeline()
        elif mode == "step":
            example_step_by_step()
        elif mode == "config":
            example_custom_config()
        else:
            print("Usage: python example_usage.py [full|step|config]")
    else:
        print("Running step-by-step example...")
        example_step_by_step()

