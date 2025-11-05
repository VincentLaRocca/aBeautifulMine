from typing import List, Dict, Any
from utils.api_client import OpenRouterClient
from config import Config

class ReportAggregator:
    def __init__(self):
        self.client = OpenRouterClient()
        self.report_tokens = {}
    
    def _format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """Format search results for input to the aggregator model"""
        formatted_results = []
        
        for result in results:
            if result["success"]:
                formatted = f"""
Search Query: {result['query']}
Findings: {result['response']}
---
"""
                formatted_results.append(formatted)
        
        return "\n".join(formatted_results)
    
    def generate_comprehensive_report(self, topic: str, search_results: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive, high-signal report from search results"""
        
        successful_results = [r for r in search_results if r["success"]]
        
        if not successful_results:
            return "No successful search results to analyze."
        
        formatted_results = self._format_search_results(successful_results)
        
        system_prompt = """You are an expert research analyst specializing in synthesizing large amounts of information into actionable, high-signal insights.

Your task is to analyze comprehensive search results and generate a concise, super high-signal report that:
1. Identifies the most important insights and patterns
2. Highlights key findings, trends, and implications  
3. Presents information in a clear, structured format
4. Focuses on actionable knowledge rather than noise
5. Organizes insights into logical categories
6. Provides specific details and evidence where available

Structure your report with:
- Executive Summary (key findings at a glance)
- Core Insights (main discoveries and their implications)
- Key Trends and Patterns
- Practical Applications/Implications
- Future Outlook/Considerations

Be thorough but concise. Focus on signal over noise."""
        
        user_prompt = f"""Based on the following comprehensive search results about "{topic}", generate an ultra-high signal research report:

{formatted_results}

Please create a well-structured, insightful report that distills the most valuable information from these research findings."""
        
        try:
            report_response = self.client.generate_response(
                model=Config.REPORT_AGGREGATOR_MODEL,
                prompt=user_prompt,
                system_prompt=system_prompt
            )
            
            # Store token usage for tracking
            self.report_tokens = report_response.get("tokens", {})
            
            return report_response.get("content", "")
            
        except Exception as e:
            raise Exception(f"Failed to generate comprehensive report: {str(e)}")
    
    def generate_summary_report(self, topic: str, search_results: List[Dict[str, Any]]) -> str:
        """Generate a quick summary version of the report"""
        
        successful_results = [r for r in search_results if r["success"]]
        
        if not successful_results:
            return "No successful search results to summarize."
        
        formatted_results = self._format_search_results(successful_results)
        
        system_prompt = """You are an expert at distilling complex information into clear, concise insights.
        Review search results and provide a brief, high-impact summary covering the most important findings."""
        
        user_prompt = f"""Based on these search results about "{topic}", provide a brief summary of the key insights:

{formatted_results}

Focus on the most important discoveries and takeaways."""
        
        try:
            response = self.client.generate_response(
                model=Config.REPORT_AGGREGATOR_MODEL,
                prompt=user_prompt,
                system_prompt=system_prompt
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"Failed to generate summary report: {str(e)}")
