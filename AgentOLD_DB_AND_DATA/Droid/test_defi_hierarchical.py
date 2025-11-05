#!/usr/bin/env python3

def test_defi_hierarchical():
    """Test the hierarchical crypto question generator specifically for DeFi"""
    
    print("TESTING HIERARCHICAL DEFI GENERATOR")
    print("=" * 60)
    
    # Set up environment check
    import os
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("ERROR: OpenRouter API key not set!")
        print("\nTo set up API key:")
        print("1. Get key from: https://openrouter.ai/keys")
        print("2. Run: set OPENROUTER_API_KEY=sk-or-v1-your-key-here")
        print("3. Then run this test again")
        return False
    
    print("API key found!")
    
    # Test the hierarchical generator with DeFi as topic
    try:
        from hierarchical_crypto_generator import CryptoQuestionGeneratorFree
        from pathlib import Path
        
        print("\nStarting DeFi hierarchical generation test...")
        print("This will generate 4 subtopics with 3 questions each (12 total)")
        print("=" * 60)
        
        generator = CryptoQuestionGeneratorFree(api_key)
        
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

def show_quick_test():
    """Show what to expect from the test"""
    
    print("\n" + "="*60)
    print("WHAT TO EXPECT FROM THE TEST:")
    print("="*60)
    print("The generator will:")
    print("1. Create 4 logical DeFi subtopics")
    print("2. Generate 3 targeted questions for each subtopic")
    print("3. Save results in multiple formats")
    print("\nExample structure:")
    print("-> Decentralized Finance")
    print("    -> DeFi Lending Protocols")
    print("       <- 3 specific questions")
    print("    -> Decentralized Exchanges")
    print("       <- 3 specific questions")  
    print("    -> Yield Farming Strategies")
    print("       <- 3 specific questions")
    print("    -> DeFi Security & Risks")
    print("        <- 3 specific questions")
    print("\nTotal: 12 focused questions across 4 subtopics")
    print("="*60)

if __name__ == "__main__":
    from datetime import datetime
    
    print("HIERARCHICAL DEFI TEST RUNNER")
    print("=" * 50)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show what to expect
    show_quick_test()
    
    # Run the test
    success = test_defi_hierarchical()
    
    if success:
        print("\nTEST COMPLETED SUCCESSFULLY!")
        print("Check the 'hierarchical_crypto_questions/' directory for results.")
        print("\nYour DeFi hierarchical structure is ready for RAG implementation!")
    else:
        print("\nTEST FAILED")
        print("Please check the error messages above and try again.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
