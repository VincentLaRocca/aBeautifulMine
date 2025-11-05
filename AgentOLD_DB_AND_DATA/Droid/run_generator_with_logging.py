#!/usr/bin/env python3

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Helper script to run the crypto question generator with proper setup and logging"""
    
    print("Crypto Question Generator Launcher with Logging")
    print("=" * 60)
    
    # Check if API key is provided as argument
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("Using provided API key")
    else:
        print("Please provide your OpenRouter API key:")
        print("Usage: python run_generator_with_logging.py YOUR_API_KEY")
        print("\nGet your API key from: https://openrouter.ai/")
        print("After running, check the 'crypto_questions' directory for results")
        
        # Ask for API key
        api_key = input("\nEnter your OpenRouter API key: ").strip()
        if not api_key:
            print("ERROR: No API key provided")
            return
    
    # Create logs directory
    logs_dir = Path("crypto_questions_logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"question_generator_{timestamp}.log"
    
    print(f"Log file will be saved to: {log_file}")
    print("This will take several minutes to process all 15 topics...")
    print("=" * 60)
    
    # Set environment variable and run the generator
    env = os.environ.copy()
    env['OPENROUTER_API_KEY'] = api_key
    
    try:
        # Start time logging
        start_time = datetime.now()
        
        with open(log_file, 'w', encoding='utf-8') as log:
            log.write(f"Crypto Question Generator Log\n")
            log.write(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Process: {sys.executable} crypto_question_generator_fixed.py\n")
            log.write("=" * 60 + "\n\n")
            
            try:
                # Run the generator and capture both stdout and stderr
                process = subprocess.run(
                    [sys.executable, 'crypto_question_generator_fixed.py'],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8'
                )
                
                # Write all output to log file
                log.write(process.stdout)
                log.write(f"\n\nProcess completed with exit code: {process.returncode}")
                
                # Also display to console
                print(process.stdout)
                
                # Calculate duration
                end_time = datetime.now()
                duration = end_time - start_time
                
                log.write(f"\n\nCompleted: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                log.write(f"Duration: {duration}")
                
                if process.returncode == 0:
                    print("\n" + "=" * 60)
                    print("SUCCESS: Question generation completed!")
                    print("Check the 'crypto_questions' directory for all generated files")
                    print(f"Log file: {log_file}")
                    print(f"Duration: {duration}")
                else:
                    print("\n" + "=" * 60)
                    print("FAILED: Question generation failed")
                    print(f"Check log file for details: {log_file}")
                    
            except Exception as e:
                log.write(f"ERROR during execution: {e}")
                print(f"ERROR: {e}")
                
    except Exception as e:
        print(f"ERROR: Could not create or write to log file: {e}")

def view_recent_logs():
    """View the most recent log files"""
    logs_dir = Path("crypto_questions_logs")
    if not logs_dir.exists():
        print("No logs directory found")
        return
    
    log_files = sorted(logs_dir.glob("*.log"), reverse=True)[:3]
    
    if not log_files:
        print("No log files found")
        return
    
    print("Recent log files:")
    for i, log_file in enumerate(log_files, 1):
        print(f"{i}. {log_file.name}")
        print(f"   Modified: {log_file.stat().st_mtime}")
        print(f"   Size: {log_file.stat().st_size} bytes")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--view-logs":
        view_recent_logs()
    else:
        main()
