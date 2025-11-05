#!/usr/bin/env python3
"""
Batch Research Script
This script reads topics from a file and runs ultra-deep research on each topic.
"""

import sys
import os
import time
from typing import List
from colorama import Fore, Style

def read_topics_from_file(file_path: str) -> List[str]:
    """Read topics from a text file, one topic per line"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return topics
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' not found.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error reading file '{file_path}': {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def run_batch_research(topics_file: str):
    """Run research on multiple topics from file"""
    print(f"{Fore.CYAN}{'=' * 64}")
    print("               BATCH RESEARCH MODE")
    print("          Processing Multiple Research Topics")
    print(f"{'=' * 64}{Style.RESET_ALL}")
    
    # Read topics from file
    topics = read_topics_from_file(topics_file)
    
    if not topics:
        print(f"{Fore.YELLOW}No topics found in file '{topics_file}'{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}Found {len(topics)} topics to research:{Style.RESET_ALL}")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    print()
    
    # Track results
    successful_research = []
    failed_research = []
    total_start_time = time.time()
    
    # Process each topic
    for i, topic in enumerate(topics, 1):
        print(f"{Fore.BLUE}{'=' * 80}")
        print(f"Research {i}/{len(topics)}: {topic}")
        print(f"{'=' * 80}{Style.RESET_ALL}")
        
        topic_start_time = time.time()
        
        try:
            # Import and run the main research function
            # We'll run main.py as a subprocess to avoid conflicts
            import subprocess
            
            # Run main.py with the topic as argument
            result = subprocess.run([
                sys.executable, 'main.py', topic
            ], capture_output=True, text=True, timeout=1800)  # 30 minute timeout per topic
            
            topic_end_time = time.time()
            topic_duration = topic_end_time - topic_start_time
            
            if result.returncode == 0:
                successful_research.append({
                    'topic': topic,
                    'duration': topic_duration,
                    'output': result.stdout
                })
                print(f"{Fore.GREEN}✓ Research completed for '{topic}' in {topic_duration:.2f} seconds{Style.RESET_ALL}")
            else:
                failed_research.append({
                    'topic': topic,
                    'error': result.stderr,
                    'returncode': result.returncode
                })
                print(f"{Fore.RED}✗ Research failed for '{topic}' (Exit code: {result.returncode}){Style.RESET_ALL}")
                if result.stderr:
                    print(f"{Fore.YELLOW}Error details: {result.stderr[:200]}...{Style.RESET_ALL}")
        
        except subprocess.TimeoutExpired:
            failed_research.append({
                'topic': topic,
                'error': 'Research timed out after 30 minutes'
            })
            print(f"{Fore.RED}✗ Research timed out for '{topic}' after 30 minutes{Style.RESET_ALL}")
        
        except Exception as e:
            failed_research.append({
                'topic': topic,
                'error': str(e)
            })
            print(f"{Fore.RED}✗ Unexpected error for '{topic}': {str(e)}{Style.RESET_ALL}")
        
        # Add delay between topics to avoid API rate limits
        if i < len(topics):
            print(f"{Fore.YELLOW}Waiting 30 seconds before next topic...{Style.RESET_ALL}")
            time.sleep(30)
    
    # Summary
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print("                    BATCH RESEARCH SUMMARY")
    print(f"{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Successful research:{Style.RESET_ALL} {len(successful_research)}/{len(topics)}")
    print(f"{Fore.RED}Failed research:{Style.RESET_ALL} {len(failed_research)}/{len(topics)}")
    print(f"{Fore.YELLOW}Total time:{Style.RESET_ALL} {total_duration:.2f} seconds ({total_duration/3600:.2f} hours)")
    
    if successful_research:
        print(f"\n{Fore.GREEN}Successfully researched topics:{Style.RESET_ALL}")
        for item in successful_research:
            print(f"  ✓ {item['topic']} ({item['duration']:.2f}s)")
        
        avg_time = sum(item['duration'] for item in successful_research) / len(successful_research)
        print(f"{Fore.CYAN}Average time per successful research:{Style.RESET_ALL} {avg_time:.2f} seconds")
    
    if failed_research:
        print(f"\n{Fore.RED}Failed research topics:{Style.RESET_ALL}")
        for item in failed_research:
            error_msg = item['error'][:100] + "..." if len(item['error']) > 100 else item['error']
            print(f"  ✗ {item['topic']} - {error_msg}")

def create_sample_topics_file():
    """Create a sample topics file for demonstration"""
    sample_content = """# Sample Research Topics
# Each line below is a separate research topic
# Lines starting with # are comments and will be ignored

artificial intelligence in healthcare
renewable energy technologies
quantum computing applications
blockchain technology in supply chain
space exploration advancements
machine learning ethics
climate change solutions
biotechnology innovations
cybersecurity trends
autonomous vehicle technology
"""
    
    with open('sample_topics.txt', 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"{Fore.GREEN}Sample topics file 'sample_topics.txt' created{Style.RESET_ALL}")

def print_usage():
    """Print usage instructions"""
    print(f"{Fore.CYAN}Batch Research Script Usage:{Style.RESET_ALL}")
    print("  python batch_research.py <topics_file.txt>")
    print("")
    print(f"{Fore.YELLOW}Options:{Style.RESET_ALL}")
    print("  --sample    Create a sample topics file")
    print("")
    print(f"{Fore.GREEN}Topics file format:{Style.RESET_ALL}")
    print("  - One topic per line")
    print("  - Lines starting with # are ignored (comments)")
    print("  - Empty lines are ignored")
    print("")
    print(f"{Fore.BLUE}Example:{Style.RESET_ALL}")
    print("  python batch_research.py my_topics.txt")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == '--sample':
        create_sample_topics_file()
        return
    
    if not os.path.exists(arg):
        print(f"{Fore.RED}Error: File '{arg}' does not exist{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Use --sample to create a sample topics file{Style.RESET_ALL}")
        sys.exit(1)
    
    try:
        run_batch_research(arg)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}* Batch research cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}* Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
