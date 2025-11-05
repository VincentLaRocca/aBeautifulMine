from typing import Dict, List, Any
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init()

class OutputFormatter:
    @staticmethod
    def format_header(topic: str, num_queries: int, num_successful: int) -> str:
        """Format the report header"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""
{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}
{Fore.CYAN}ULTRA DEEP RESEARCH REPORT{Style.RESET_ALL}
{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}

{Fore.YELLOW}Topic:{Style.RESET_ALL} {topic}
{Fore.YELLOW}Research Completed:{Style.RESET_ALL} {timestamp}
{Fore.YELLOW}Search Queries Executed:{Style.RESET_ALL} {num_queries}
{Fore.YELLOW}Successful Searches:{Style.RESET_ALL} {num_successful}
{Fore.YELLOW}Success Rate:{Style.RESET_ALL} {(num_successful/num_queries)*100:.1f}%
"""
        return header
    
    @staticmethod
    def format_report_content(content: str) -> str:
        """Format the main report content"""
        section = f"""
{Fore.GREEN}
{Style.BRIGHT}COMPREHENSIVE RESEARCH INSIGHTS
{Style.NORMAL}{Style.RESET_ALL}
{content}
"""
        return section
    
    @staticmethod
    def calculate_token_usage(query_generator, search_dispatcher, report_aggregator) -> dict:
        """Calculate total token usage across all phases"""
        tokens = {
            "query_generation": query_generator.query_tokens,
            "search_execution": search_dispatcher.search_tokens,
            "report_synthesis": report_aggregator.report_tokens
        }
        
        # Calculate totals
        totals = {
            "query_generation": {
                "prompt_tokens": query_generator.query_tokens.get("prompt_tokens", 0),
                "completion_tokens": query_generator.query_tokens.get("completion_tokens", 0),
                "total_tokens": query_generator.query_tokens.get("total_tokens", 0)
            },
            "search_execution": {
                "prompt_tokens": sum(t.get("prompt_tokens", 0) for t in search_dispatcher.search_tokens),
                "completion_tokens": sum(t.get("completion_tokens", 0) for t in search_dispatcher.search_tokens),
                "total_tokens": sum(t.get("total_tokens", 0) for t in search_dispatcher.search_tokens)
            },
            "report_synthesis": {
                "prompt_tokens": report_aggregator.report_tokens.get("prompt_tokens", 0),
                "completion_tokens": report_aggregator.report_tokens.get("completion_tokens", 0),
                "total_tokens": report_aggregator.report_tokens.get("total_tokens", 0)
            }
        }
        
        # Calculate session totals
        session_totals = {
            "prompt_tokens": totals["query_generation"]["prompt_tokens"] + 
                           totals["search_execution"]["prompt_tokens"] + 
                           totals["report_synthesis"]["prompt_tokens"],
            "completion_tokens": totals["query_generation"]["completion_tokens"] + 
                               totals["search_execution"]["completion_tokens"] + 
                               totals["report_synthesis"]["completion_tokens"],
            "total_tokens": totals["query_generation"]["total_tokens"] + 
                         totals["search_execution"]["total_tokens"] + 
                         totals["report_synthesis"]["total_tokens"]
        }
        
        return {
            "by_phase": totals,
            "session_totals": session_totals,
            "raw": tokens
        }
    
    @staticmethod
    def format_token_statistics(token_data: dict) -> str:
        """Format token usage statistics for display"""
        from colorama import Fore, Style
        
        stats = token_data["by_phase"]
        session_totals = token_data["session_totals"]
        
        token_report = f"""
{Fore.YELLOW}
{'=' * 80}
TOKEN USAGE STATISTICS
{'=' * 80}{Style.RESET_ALL}

{Fore.CYAN}Query Generation Phase:{Style.RESET_ALL}
  Input Tokens: {stats['query_generation']['prompt_tokens']:,}
  Output Tokens: {stats['query_generation']['completion_tokens']:,}
  Total Tokens: {stats['query_generation']['total_tokens']:,}

{Fore.CYAN}Search Execution Phase:{Style.RESET_ALL}
  Input Tokens: {stats['search_execution']['prompt_tokens']:,}
  Output Tokens: {stats['search_execution']['completion_tokens']:,}
  Total Tokens: {stats['search_execution']['total_tokens']:,}

{Fore.CYAN}Report Synthesis Phase:{Style.RESET_ALL}
  Input Tokens: {stats['report_synthesis']['prompt_tokens']:,}
  Output Tokens: {stats['report_synthesis']['completion_tokens']:,}
  Total Tokens: {stats['report_synthesis']['total_tokens']:,}

{Fore.GREEN}
SESSION TOTALS:{Style.RESET_ALL}
  Total Input Tokens: {session_totals['prompt_tokens']:,}
  Total Output Tokens: {session_totals['completion_tokens']:,}
  {Fore.RED}** TOTAL TOKENS USED: {session_totals['total_tokens']:,}{Style.RESET_ALL}
"""
        return token_report

    @staticmethod
    def format_question_answer_pairs(search_results: List[Dict[str, Any]]) -> str:
        """Format search results as question-answer pairs with character counts"""
        successful_results = [r for r in search_results if r["success"]]
        
        qa_pairs = f"""
{Fore.CYAN}
{'=' * 80}
QUESTION-ANSWER PAIRS WITH CHARACTER COUNTS
{'=' * 80}{Style.RESET_ALL}

{Fore.YELLOW}Total Question-Answer Pairs:{Style.RESET_ALL} {len(successful_results)}

"""
        
        total_question_chars = 0
        total_answer_chars = 0
        
        for i, result in enumerate(successful_results, 1):
            question = result["query"]
            answer = result["response"]
            
            question_chars = len(question)
            answer_chars = len(answer)
            
            total_question_chars += question_chars
            total_answer_chars += answer_chars
            
            qa_pairs += f"""
{Fore.GREEN}Pair {i}:{Style.RESET_ALL}
{Fore.YELLOW}question:{Style.RESET_ALL} {question}
{Fore.CYAN}question characters:{Style.RESET_ALL} {question_chars:,}
{Fore.YELLOW}answer:{Style.RESET_ALL} {answer}
{Fore.CYAN}answer characters:{Style.RESET_ALL} {answer_chars:,}

"""
        
        # Add summary statistics
        qa_pairs += f"""
{Fore.GREEN}
{'=' * 80}
CHARACTER COUNT SUMMARY
{'=' * 80}{Style.RESET_ALL}

{Fore.YELLOW}Total Question Characters:{Style.RESET_ALL} {total_question_chars:,}
{Fore.YELLOW}Total Answer Characters:{Style.RESET_ALL} {total_answer_chars:,}
{Fore.RED}Total All Characters:{Style.RESET_ALL} {total_question_chars + total_answer_chars:,}
{Fore.YELLOW}Average Characters per Question:{Style.RESET_ALL} {total_question_chars/len(successful_results):.1f}
{Fore.YELLOW}Average Characters per Answer:{Style.RESET_ALL} {total_answer_chars/len(successful_results):.1f}
{Fore.YELLOW}Average Characters per Pair:{Style.RESET_ALL} {(total_question_chars + total_answer_chars)/len(successful_results):.1f}

"""
        
        return qa_pairs
    
    @staticmethod
    def format_statistics(search_results: List[Dict[str, Any]]) -> str:
        """Format search statistics"""
        successful = sum(1 for r in search_results if r["success"])
        total = len(search_results)
        
        stats = f"""
{Fore.MAGENTA}
{'=' * 80}
RESEARCH STATISTICS
{'=' * 80}{Style.RESET_ALL}

{Fore.YELLOW}Total Queries:{Style.RESET_ALL} {total}
{Fore.GREEN}Successful Searches:{Style.RESET_ALL} {successful}
{Fore.RED}Failed Searches:{Style.RESET_ALL} {total - successful}
{Fore.YELLOW}Success Rate:{Style.RESET_ALL} {(successful/total)*100:.1f}%

{Fore.CYAN}Sample Search Queries (showing first 10 of {successful} successful queries):{Style.RESET_ALL}
"""
        
        # Show first 10 successful queries as examples (increased from 5)
        successful_results = [r for r in search_results if r["success"]][:10]
        for i, result in enumerate(successful_results, 1):
            stats += f"{i}. {result['query'][:80]}...\n"
        
        stats += "\n"
        return stats
    
    @staticmethod
    def format_progress_message(message: str, is_error: bool = False) -> str:
        """Format progress message with appropriate color"""
        if is_error:
            return f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}"
        else:
            return f"{Fore.BLUE}{message}{Style.RESET_ALL}"
    
    @staticmethod
    def format_success_message(message: str) -> str:
        """Format success message"""
        return f"{Fore.GREEN}* {message}{Style.RESET_ALL}"
    
    @staticmethod
    def save_report(topic: str, content: str) -> str:
        """Generate report filename and optionally save to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = topic.replace(" ", "_").replace("/", "_").lower()
        filename = f"research_report_{sanitized_topic}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n{Fore.GREEN}Report saved to: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"\n{Fore.RED}Failed to save report: {str(e)}{Style.RESET_ALL}")
            return filename
