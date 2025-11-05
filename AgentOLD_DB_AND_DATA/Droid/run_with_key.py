#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
    """Set environment variable and run generator"""
    
    print("Crypto Question Generator - API Key Setup")
    print("=" * 50)
    
    # Get API key from command line argument
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("Using API key from command line")
    else:
        # Ask user to input API key
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print("ERROR: No API key provided")
            return
    
    # Set environment variable for this process
    os.environ['OPENROUTER_API_KEY'] = api_key
    print(f"API Key set: {api_key[:20]}...")
    
    # Verify it's set
    if os.getenv('OPENROUTER_API_KEY'):
        print("✓ Environment variable successfully set")
    else:
        print("✗ Failed to set environment variable")
        return
    
    # Run the enhanced generator
    print("\nRunning enhanced question generator...")
    print("This version has improved rate limiting and question parsing.")
    print("=" * 50)
    
    try:
        # Import and run the generator directly
        from crypto_question_generator_v2 import CryptoQuestionGeneratorV2
        from pathlib import Path
        
        topics_file = "CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md"
        if not Path(topics_file).exists():
            print(f"ERROR: Topics file not found: {topics_file}")
            return
        
        generator = CryptoQuestionGeneratorV2(api_key)
        generated_files = generator.generate_all_question_files(topics_file)
        
        print(f"\nSUCCESS: Generated question files for {len(generated_files)} topics")
        print(f"Check the 'crypto_questions' directory for all files")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
