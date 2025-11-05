#!/usr/bin/env python3

import os
import subprocess
import sys

def main():
    """Helper script to run the crypto question generator with proper setup"""
    
    print("Crypto Question Generator Launcher")
    print("=" * 50)
    
    # Check if API key is provided as argument
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("Using provided API key")
    else:
        print("Please provide your OpenRouter API key:")
        print("Usage: python run_generator.py YOUR_API_KEY")
        print("\nGet your API key from: https://openrouter.ai/")
        print("After running, check the 'crypto_questions' directory for results")
        
        # Ask for API key
        api_key = input("\nEnter your OpenRouter API key: ").strip()
        if not api_key:
            print("ERROR: No API key provided")
            return
    
    # Set environment variable and run the generator
    env = os.environ.copy()
    env['OPENROUTER_API_KEY'] = api_key
    
    print("Running crypto question generator...")
    print("This will take several minutes to process all 15 topics...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'crypto_question_generator_fixed.py'],
            env=env,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\nSUCCESS: Question generation completed!")
            print("Check the 'crypto_questions' directory for all generated files")
        else:
            print("\nFAILED: Question generation failed")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
