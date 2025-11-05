#!/usr/bin/env python3

import os
import re
import time
from pathlib import Path

def retry_failed_topics(api_key: str):
    """Retry only the topics that failed in the previous run"""
    
    # Import the fixed generator
    from crypto_question_generator_fixed import CryptoQuestionGenerator
    
    print("Retrying Failed Topics Only")
    print("=" * 50)
    
    # These are the failed topic IDs from the log
    failed_topic_ids = [
        "MA_001",      # Moving Averages
        "MOM_001",     # Momentum Indicators  
        "ONCHAIN_ADV_001",  # Advanced On-Chain
        "PSYCH_001",   # Trading Psychology
        "RISK_001",    # Risk Management
        "DATA_001",    # Data Analytics
        "QUANT_001"    # Quantitative Trading
    ]
    
    generator = CryptoQuestionGenerator(api_key)
    
    # Parse topics document to get topic objects for failed IDs
    topics = generator.parse_topics_document("CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md")
    
    # Find the failed topics
    failed_topics = [topic for topic in topics if topic.topic_id in failed_topic_ids]
    
    if failed_topics:
        print(f"Found {len(failed_topics)} topics to retry:")
        for topic in failed_topics:
            print(f"- {topic.title} ({topic.topic_id})")
        
        # Start processing with extra delays
        print(f"\nStarting retry with extended delays...")
        print("This will take longer to avoid rate limits.")
        
        generated_files = {}
        failedAgain = []
        
        for i, topic in enumerate(failed_topics, 1):
            print(f"\nRetrying topic {i}/{len(failed_topics)}: {topic.title}")
            
            try:
                # Extra initial wait
                time.sleep(3)
                
                questions = generator.generate_questions_for_topic(topic)
                
                if questions:
                    filepath = generator.save_questions_to_file(topic, questions)
                    generated_files[topic.topic_id] = filepath
                    print(f"+ Generated {len(questions)} questions -> {filepath}")
                else:
                    failedAgain.append(topic.topic_id)
                    print(f"- Failed again for {topic.title}")
                
                # Extended delay between retries
                time.sleep(8)  # 8 seconds between topics
                
            except Exception as e:
                failedAgain.append(topic.topic_id)
                print(f"- Error retrying {topic.title}: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print("RETRY COMPLETE")
        print(f"{'='*60}")
        print(f"Topics retried: {len(failed_topics)}")
        print(f"Successfully completed: {len(generated_files)}")
        print(f"Still failed: {len(failedAgain)}")
        print(f"Additional questions created: {len(generated_files) * 15}")
        
        if failedAgain:
            print(f"\nStill failing: {', '.join(failedAgain)}")
            print("Consider trying again later when API limits reset.")
        else:
            print(f"\nAll failed topics completed successfully!")
            
    else:
        print("No failed topics found matching the pattern.")

def main():
    """Main function for retry process"""
    import sys
    
    api_key = sys.argv[1] if len(sys.argv) > 1 else os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("Please provide OpenRouter API key:")
        print("Usage: python retry_failed_topics.py YOUR_API_KEY")
        return
    
    retry_failed_topics(api_key)

if __name__ == "__main__":
    main()
