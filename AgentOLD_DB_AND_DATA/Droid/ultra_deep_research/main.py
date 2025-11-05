#!/usr/bin/env python3

import sys
import time
from agents.query_generator import QueryGenerator
from agents.search_dispatcher import SearchDispatcher
from agents.report_aggregator import ReportAggregator
from utils.output_formatter import OutputFormatter
from config import Config

# Add database support
try:
    from database.database_setup import DatabaseManager
    from database.qa_importer import QAImporter
    DATABASE_ENABLED = True
except ImportError:
    DATABASE_ENABLED = False

def print_welcome():
    """Print welcome message and usage instructions"""
    from colorama import Fore, Style
    print(f"{Fore.CYAN}")
    print("=" * 64)
    print("                ULTRA DEEP RESEARCH CLI v1.0")
    print("          AI-Powered Comprehensive Research Analysis")
    print("=" * 64)
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Instructions:{Style.RESET_ALL}")
    print("* Enter a research topic to begin ultra-deep analysis")
    print("* The system will generate 100 diverse search queries")
    print("* Execute comprehensive searches via multiple AI APIs")
    print("* Generate a detailed, high-signal research report")
    print("")
    print(f"{Fore.GREEN}Example topics:{Style.RESET_ALL}")
    print("* quantum computing applications")
    print("* sustainable energy solutions")
    print("* artificial intelligence ethics")
    print("* space exploration technology")
    print("")

def validate_config():
    """Validate configuration before proceeding"""
    try:
        Config.validate_config()
        from colorama import Fore, Style
        print(f"{Fore.GREEN}* Configuration validated{Style.RESET_ALL}")
        return True
    except ValueError as e:
        from colorama import Fore, Style
        print(f"{Fore.RED}Configuration Error: {str(e)}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}To fix this:{Style.RESET_ALL}")
        print(f"1. Create a .env file in the ultra_deep_research directory")
        print(f"2. Add: OPENROUTER_API_KEY=your_api_key_here")
        print(f"3. Get your API key from: https://openrouter.ai/")
        return False

def run_research(topic: str):
    """Execute the complete research workflow"""
    from colorama import Fore, Style
    
    try:
        # Initialize components
        query_generator = QueryGenerator()
        search_dispatcher = SearchDispatcher()
        report_aggregator = ReportAggregator()
        formatter = OutputFormatter()
        
        print(f"\n{Fore.BLUE}* Starting ultra-deep research on: {topic}{Style.RESET_ALL}")
        start_time = time.time()
        
        # Step 1: Generate search queries
        print(f"{Fore.YELLOW}* Generating diverse search queries...{Style.RESET_ALL}")
        queries = query_generator.generate_search_queries(topic, num_queries=100)
        
        if not queries:
            print(f"{Fore.RED}* Failed to generate search queries{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}* Generated {len(queries)} search queries{Style.RESET_ALL}")
        
        # Step 2: Execute searches
        print(f"{Fore.YELLOW}* Executing comprehensive searches...{Style.RESET_ALL}")
        search_results = search_dispatcher.execute_searches(queries, show_progress=True)
        
        successful_results = search_dispatcher.get_successful_results(search_results)
        
        if not successful_results:
            print(f"{Fore.RED}* No successful searches completed{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}* Completed {len(successful_results)}/{len(queries)} successful searches{Style.RESET_ALL}")
        
        # Step 3: Generate comprehensive report
        print(f"{Fore.YELLOW}* Analyzing results and generating comprehensive report...{Style.RESET_ALL}")
        report = report_aggregator.generate_comprehensive_report(topic, search_results)
        
        # Step 4: Store Q&A pairs in database
        if DATABASE_ENABLED:
            try:
                print(f"{Fore.YELLOW}* Storing question-answer pairs in database...{Style.RESET_ALL}")
                qa_importer = QAImporter()
                
                # Calculate total tokens used
                token_data = formatter.calculate_token_usage(query_generator, search_dispatcher, report_aggregator)
                total_tokens = token_data['session_totals']['total_tokens']
                
                # Import to database
                import_result = qa_importer.import_from_search_results(topic, search_results, total_tokens)
                print(f"{Fore.GREEN}* Stored {import_result['stored']} Q&A pairs (session ID: {import_result['session_id']}){Style.RESET_ALL}")
                
            except Exception as e:
                print(f"{Fore.YELLOW}* Database storage failed: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}* Continuing with report generation...{Style.RESET_ALL}")
        
        # Step 5: Format and display results
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate token usage if not already calculated
        if not DATABASE_ENABLED:
            token_data = formatter.calculate_token_usage(query_generator, search_dispatcher, report_aggregator)
        
        # Build complete output
        complete_report = formatter.format_header(topic, len(queries), len(successful_results))
        complete_report += formatter.format_report_content(report)
        complete_report += formatter.format_question_answer_pairs(search_results)
        complete_report += formatter.format_statistics(search_results)
        complete_report += formatter.format_token_statistics(token_data)
        
        complete_report += f"""
{Fore.CYAN}
{'=' * 80}
RESEARCH COMPLETED
{'=' * 80}{Style.RESET_ALL}

{Fore.YELLOW}Total Time:{Style.RESET_ALL} {duration:.2f} seconds
{Fore.YELLOW}Average Search Time:{Style.RESET_ALL} {(duration/len(search_results)):.2f} seconds per query
{Fore.YELLOW}Total Cost (estimated):${token_data['session_totals']['total_tokens'] / 1000000:.4f} (assuming $1 per 1M tokens)
"""
        
        # Display results
        print(complete_report)
        
        # Save report to file
        filename = formatter.save_report(topic, complete_report)
        
        print(f"\n{Fore.GREEN}* Ultra-deep research completed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}* Research failed: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def main():
    """Main CLI entry point"""
    print_welcome()
    
    # Validate configuration first
    if not validate_config():
        sys.exit(1)
    
    # Get user input
    from colorama import Fore, Style
    
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        print(f"{Fore.GREEN}* Research topic from command line: {topic}{Style.RESET_ALL}")
    else:
        try:
            topic = input(f"\n{Fore.CYAN}Enter your research topic: {Style.RESET_ALL}").strip()
            
            if not topic:
                print(f"{Fore.RED}* No topic provided. Exiting.{Style.RESET_ALL}")
                sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}* Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
    
    # Run the research
    try:
        run_research(topic)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}* Research cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        from colorama import Fore, Style
        print(f"{Fore.RED}* Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
