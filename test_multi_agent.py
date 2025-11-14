"""
Test script to verify multi-agent system setup
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from multi_agent_system import (
            MultiAgentOrchestrator,
            SubtopicGeneratorAgent,
            QuestionGeneratorAgent,
            ResearchAgent,
            AnswerGeneratorAgent,
            DatabaseAgent
        )
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_orchestrator_init():
    """Test orchestrator initialization"""
    print("\nTesting orchestrator initialization...")
    try:
        from multi_agent_system import MultiAgentOrchestrator
        orchestrator = MultiAgentOrchestrator()
        print("✅ Orchestrator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Orchestrator initialization failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure chromadb is installed: pip install chromadb")
        print("  2. Check your .env file")
        return False

def test_agent_init():
    """Test individual agent initialization"""
    print("\nTesting individual agents...")
    try:
        from multi_agent_system import (
            SubtopicGeneratorAgent,
            QuestionGeneratorAgent,
            ResearchAgent,
            AnswerGeneratorAgent
        )
        
        agents = {
            "SubtopicGenerator": SubtopicGeneratorAgent(),
            "QuestionGenerator": QuestionGeneratorAgent(),
            "ResearchAgent": ResearchAgent(),
            "AnswerGenerator": AnswerGeneratorAgent()
        }
        
        print("✅ All agents initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_database_agent():
    """Test database agent (requires chromadb)"""
    print("\nTesting database agent...")
    try:
        from multi_agent_system import DatabaseAgent
        db_agent = DatabaseAgent(collection_name="test_collection")
        print("✅ Database agent initialized successfully")
        return True
    except ImportError as e:
        print(f"❌ ChromaDB not installed: {e}")
        print("  Install with: pip install chromadb")
        return False
    except Exception as e:
        print(f"❌ Database agent initialization failed: {e}")
        return False

def test_config_loading():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        import json
        config_path = Path(__file__).parent / "multi_agent_system" / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            print("✅ Configuration file loaded")
            print(f"  Model URL: {config.get('model_url', 'N/A')}")
            print(f"  Questions per topic: {config.get('questions_per_topic', 'N/A')}")
            return True
        else:
            print("⚠️  Configuration file not found (using defaults)")
            return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*80)
    print("MULTI-AGENT SYSTEM SETUP TEST")
    print("="*80)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Orchestrator", test_orchestrator_init),
        ("Individual Agents", test_agent_init),
        ("Database Agent", test_database_agent),
        ("Configuration", test_config_loading)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    print("\n" + "="*80)
    print("TEST RESULTS")
    print("="*80)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("="*80)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Make sure your LLM server is running")
        print("  2. Run: python run_multi_agent.py \"Your Topic\"")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

