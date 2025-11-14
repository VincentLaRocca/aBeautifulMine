"""
Example: Training on a New Domain
Shows how to use the system for any subject
"""

from multi_agent_system import MultiAgentOrchestrator
from multi_agent_system.domain_config import get_domain_config, create_custom_domain

# ============================================================================
# Example 1: Using a Preset Domain (Medicine)
# ============================================================================

def example_medicine():
    """Train on medicine domain"""
    print("="*80)
    print("EXAMPLE: Medicine Domain")
    print("="*80)
    
    # Get medicine domain config
    domain_config = get_domain_config("medicine")
    
    # Create config
    config = {
        "domain": "medicine",
        "domain_config": domain_config,
        "model_url": "http://localhost:8080/v1",
        "questions_per_topic": 100,
        "output_dir": "medicine_training_output",
        "db_path": "medicine_chromadb"
    }
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator(config=config)
    
    # Run pipeline
    results = orchestrator.run_full_pipeline("Cardiovascular Diseases")
    
    return results


# ============================================================================
# Example 2: Using a Preset Domain (Law)
# ============================================================================

def example_law():
    """Train on law domain"""
    print("="*80)
    print("EXAMPLE: Law Domain")
    print("="*80)
    
    domain_config = get_domain_config("law")
    
    config = {
        "domain": "law",
        "domain_config": domain_config,
        "output_dir": "law_training_output",
        "db_path": "law_chromadb"
    }
    
    orchestrator = MultiAgentOrchestrator(config=config)
    results = orchestrator.run_full_pipeline("Contract Law")
    
    return results


# ============================================================================
# Example 3: Creating a Custom Domain (Machine Learning)
# ============================================================================

def example_custom_ml():
    """Train on custom machine learning domain"""
    print("="*80)
    print("EXAMPLE: Custom Machine Learning Domain")
    print("="*80)
    
    # Create custom domain
    ml_domain = create_custom_domain(
        name="Machine Learning",
        research_specialization="machine learning and artificial intelligence",
        research_sources="peer-reviewed papers, established ML frameworks, recognized ML researchers",
        example_context="ML model examples and training scenarios",
        example_types="machine learning examples",
        practical_context="ML development scenarios",
        audience="ML engineers and data scientists",
        domain_characteristics="model training, hyperparameter tuning, data preprocessing, evaluation metrics"
    )
    
    config = {
        "domain": "machine_learning",
        "domain_config": ml_domain,
        "output_dir": "ml_training_output",
        "db_path": "ml_chromadb"
    }
    
    orchestrator = MultiAgentOrchestrator(config=config)
    results = orchestrator.run_full_pipeline("Neural Networks")
    
    return results


# ============================================================================
# Example 4: Just Customizing Research Agent
# ============================================================================

def example_custom_research_agent():
    """Use custom research agent for a specific domain"""
    from multi_agent_system import ResearchAgent
    from multi_agent_system.domain_config import get_domain_config
    
    # Get programming domain config
    domain_config = get_domain_config("programming")
    
    # Create research agent with domain config
    research_agent = ResearchAgent(
        model_url="http://localhost:8080/v1",
        domain_config=domain_config
    )
    
    # Use it
    result = research_agent.research_question("What is React and how does it work?")
    
    print(f"Research completed: {result['success']}")
    print(f"Key concepts: {result['research_data'].get('key_concepts', [])}")
    
    return result


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_new_domain.py [medicine|law|custom_ml|research]")
        print()
        print("Examples:")
        print("  python example_new_domain.py medicine")
        print("  python example_new_domain.py law")
        print("  python example_new_domain.py custom_ml")
        print("  python example_new_domain.py research")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "medicine":
        example_medicine()
    elif command == "law":
        example_law()
    elif command == "custom_ml":
        example_custom_ml()
    elif command == "research":
        example_custom_research_agent()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

