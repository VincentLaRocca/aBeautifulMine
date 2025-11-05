import threading
from typing import List, Dict, Any
from utils.api_client import OpenRouterClient
from config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed

class SearchDispatcher:
    def __init__(self):
        self.client = OpenRouterClient()
        self.executor = ThreadPoolExecutor(max_workers=Config.MAX_CONCURRENT_SEARCHES)
        self.search_tokens = []
    
    def search_single_query(self, query: str, index: int) -> Dict[str, Any]:
        """Execute a single search query"""
        system_prompt = """You are a research assistant with access to comprehensive information sources. 
        Provide detailed, accurate information based on web search capabilities.
        Focus on facts, insights, and valuable information that would be useful for deep research.
        Include specific details, sources, and context when possible."""
        
        try:
            search_response = self.client.generate_response(
                model=Config.SEARCH_MODEL,
                prompt=f"Research and provide comprehensive information about: {query}",
                system_prompt=system_prompt
            )
            
            # Track token usage
            self.search_tokens.append(search_response.get("tokens", {}))
            
            return {
                "query": query,
                "index": index,
                "response": search_response.get("content", ""),
                "tokens": search_response.get("tokens", {}),
                "success": True
            }
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return {
                "query": query,
                "index": index,
                "response": error_msg,
                "success": False
            }
    
    def execute_searches(self, queries: List[str], show_progress: bool = True) -> List[Dict[str, Any]]:
        """Execute all search queries concurrently using threading"""
        total_queries = len(queries)
        results = []
        
        if show_progress:
            print(f"Executing {total_queries} search queries...")
        
        # Submit all tasks to thread pool
        futures = []
        for i, query in enumerate(queries):
            future = self.executor.submit(self.search_single_query, query, i)
            futures.append(future)
        
        # Process results as they complete
        completed_tasks = 0
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                completed_tasks += 1
                
                if show_progress and completed_tasks % 10 == 0:
                    print(f"Completed {completed_tasks}/{total_queries} searches...")
                    
            except Exception as e:
                print(f"Warning: Search task failed: {str(e)}")
        
        # Sort results by original index to maintain order
        results.sort(key=lambda x: x["index"])
        
        successful_searches = sum(1 for r in results if r["success"])
        
        if show_progress:
            print(f"Search completed: {successful_searches}/{total_queries} successful")
        
        return results
    
    def get_successful_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter and return only successful search results"""
        return [r for r in results if r["success"]]
