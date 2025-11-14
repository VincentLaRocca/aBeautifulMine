"""
Main entry point for Multi-Agent Q&A Dataset Creation System
"""

import sys
from pathlib import Path

# Add multi_agent_system to path
sys.path.insert(0, str(Path(__file__).parent))

from multi_agent_system.orchestrator import MultiAgentOrchestrator
import json


def main():
    """Main CLI entry point"""
    print("\n" + "="*80)
    print("MULTI-AGENT Q&A DATASET CREATION SYSTEM")
    print("="*80)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python run_multi_agent.py <topic> [start_from_subtopic_index|--continue]")
        print()
        print("Examples:")
        print('  python run_multi_agent.py "Cryptocurrency Technical Analysis"')
        print('  python run_multi_agent.py "DeFi Protocols"')
        print('  python run_multi_agent.py "Cryptocurrency Trading" 5  # Resume from subtopic 5')
        print('  python run_multi_agent.py "Cryptocurrency Trading" --continue  # Auto-detect resume point')
        print()
        print("The system will:")
        print("  1. Generate subtopics from your topic")
        print("  2. Create 100 questions per subtopic")
        print("  3. Research each question")
        print("  4. Generate comprehensive answers (3000+ chars each)")
        print("  5. Insert Q&A pairs into ChromaDB")
        print()
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    
    # Check for --continue flag
    if "--continue" in args or "-c" in args:
        # Auto-detect resume point
        from resume_pipeline import find_latest_task_list, get_subtopics_from_task_list, find_completed_subtopics
        output_dir = Path("multi_agent_output")
        
        task_list_path = find_latest_task_list(output_dir)
        if not task_list_path:
            print("[ERROR] No previous run found. Please specify a topic.")
            sys.exit(1)
        
        subtopics, topic = get_subtopics_from_task_list(task_list_path)
        completed = find_completed_subtopics(output_dir, topic)
        
        if completed:
            start_from = max(completed) + 1
            print(f"[AUTO-RESUME] Found {len(completed)} completed subtopics")
            print(f"[AUTO-RESUME] Resuming from subtopic {start_from}")
        else:
            start_from = 0
            print(f"[AUTO-RESUME] No completed subtopics found, starting from beginning")
        
        # Remove --continue from args
        args = [arg for arg in args if arg not in ["--continue", "-c"]]
        if args:
            topic = " ".join(args)
        else:
            topic = topic  # Use topic from task list
    else:
        # Normal parsing
        topic = " ".join(args[:-1]) if len(args) > 1 and args[-1].isdigit() else " ".join(args)
        start_from = int(args[-1]) if len(args) > 1 and args[-1].isdigit() else None
    
    print(f"Topic: {topic}")
    if start_from is not None:
        print(f"Resuming from subtopic index: {start_from}")
    print()
    
    # Check if server is running (basic check)
    import os
    server_url = os.getenv("MIXTRAL_SERVER_URL", "http://localhost:8080/v1")
    print(f"Using LLM server: {server_url}")
    print("Make sure your LLM server is running!")
    print()
    
    # Initialize orchestrator
    try:
        orchestrator = MultiAgentOrchestrator()
    except Exception as e:
        print(f"[ERROR] Failed to initialize orchestrator: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure chromadb is installed: pip install chromadb")
        print("  2. Check your .env file for MIXTRAL_SERVER_URL")
        sys.exit(1)
    
    # Run pipeline
    try:
        results = orchestrator.run_full_pipeline(topic, start_from_subtopic=start_from)
        
        # Save results summary
        results_path = orchestrator.output_dir / f"pipeline_results_{orchestrator.state['topic'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print("PIPELINE COMPLETE")
        print("="*80)
        print(f"Results saved to: {results_path}")
        
        if "final_stats" in results:
            stats = results["final_stats"]
            print(f"\nFinal Statistics:")
            print(f"  Total Subtopics: {stats.get('total_subtopics', 0)}")
            print(f"  Total Q&A Pairs: {stats.get('total_qa_pairs', 0)}")
            print(f"  Database Stats: {stats.get('database_stats', {})}")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Pipeline stopped by user")
        print(f"Current state saved. You can resume from subtopic {len(orchestrator.state.get('subtopics', []))}")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    from datetime import datetime
    main()

