#!/usr/bin/env python3

import os
import sys
from datetime import datetime

def test_defi_hierarchical_direct(api_key):
    """Test the hierarchical crypto generator with direct API key"""
    
    print("TESTING HIERARCHICAL DEFI GENERATOR")
    print("=" * 60)
    print(f"Using API key: {api_key[:10]}...{api_key[-10:]}")
    
    # Try the hierarchical generator with DeFi as topic
    try:
        from hierarchical_crypto_generator import HierarchicalCryptoGenerator
        from pathlib import Path
        
        print("\nStarting DeFi hierarchical generation test...")
        print("This will generate 4 subtopics with 3 questions each (12 total)")
        print("=" * 60)
        
        generator = HierarchicalCryptoGenerator(api_key)
        
        # Test with "Decentralized Finance" topic
        print("Testing with topic: Decentralized Finance")
        
        hierarchical_topic = generator.generate_hierarchical_topic(
            "Decentralized Finance", 
            num_subtopics=4, 
            questions_per_subtopic=3
        )
        
        if hierarchical_topic:
            print("\nSUCCESS: DeFi hierarchical structure generated!")
            
            # Display results
            print(f"\nGenerated Structure:")
            print(f"Main Topic: {hierarchical_topic.title}")
            print(f"Subtopics Generated: {len(hierarchical_topic.subtopics)}")
            print(f"Total Questions: {sum(len(s.questions) for s in hierarchical_topic.subtopics)}")
            
            print(f"\nSubtopics Preview:")
            for i, subtopic in enumerate(hierarchical_topic.subtopics, 1):
                print(f"  {i}. {subtopic.name}")
                print(f"     Questions ({len(subtopic.questions)}):")
                for j, question in enumerate(subtopic.questions, 1):
                    print(f"        {j}. {question}")
                print()
            
            # Save the results
            save_path = generator.save_hierarchical_topic(hierarchical_topic)
            print(f"Results saved to: {save_path}")
            
            # Show what files were created
            save_dir = Path(save_path)
            if save_dir.exists():
                print(f"\nFiles created in {save_dir.name}/:")
                for file_path in save_dir.iterdir():
                    file_size = file_path.stat().st_size / 1024  # KB
                    print(f"  - {file_path.name} ({file_size:.1f} KB)")
            
            return True
            
        else:
            print("FAILED: Could not generate hierarchical structure")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function for PowerShell testing"""
    
    print("HIERARCHICAL DEFI TEST RUNNER (PowerShell Version)")
    print("=" * 50)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get API key from command line argument
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("Using API key from command line")
    else:
        # Or prompt for it
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print("ERROR: No API key provided")
            return
    
    # Validate API key format
    if not api_key.startswith("sk-or-"):
        print("ERROR: Invalid API key format - should start with 'sk-or-'")
        return
    
    if len(api_key) < 20:
        print("ERROR: API key too short")
        return
    
    print(f"API key format looks valid")
    
    # Run the test
    success = test_defi_hierarchical_direct(api_key)
    
    if success:
        print("\nTEST COMPLETED SUCCESSFULLY!")
        print("Check the 'hierarchical_crypto_questions/' directory for results.")
        print("\nYour DeFi hierarchical structure is ready for RAG implementation!")
    else:
        print("\nTEST FAILED")
        print("Please check the error messages above and try again.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
