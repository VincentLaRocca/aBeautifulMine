from typing import List
from utils.api_client import OpenRouterClient
from config import Config
import threading
from concurrent.futures import ThreadPoolExecutor

class QueryGenerator:
    def __init__(self):
        self.client = OpenRouterClient()
        self.query_tokens = {}
    
    def generate_search_queries(self, topic: str, num_queries: int = 100) -> List[str]:
        """Generate diverse search queries for the given topic"""
        
        system_prompt = """You are an expert research strategist. Your task is to generate diverse, comprehensive search queries that will uncover deep insights about a topic.

Generate search queries that cover:
1. Different perspectives and angles
2. Various time periods and historical context
3. Expert opinions and research findings
4. Practical applications and case studies
5. Contrasting viewpoints and debates
6. Future trends and predictions
7. Technical details and methodologies
8. Real-world implications and consequences

Make queries specific, varied, and designed to return high-quality, unique information. Each query should be phrased as if you're using a search engine."""
        
        user_prompt = f"""Generate exactly {num_queries} diverse search queries about: {topic}

Return the queries as a numbered list, with each query on a new line. Make sure each query is unique and explores different aspects of the topic."""
        
        try:
            query_response = self.client.generate_response(
                model=Config.QUERY_GENERATOR_MODEL,
                prompt=user_prompt,
                system_prompt=system_prompt
            )
            
            # Store token usage for tracking
            self.query_tokens = query_response.get("tokens", {})
            response = query_response.get("content", "")
            
            # Parse the response to extract individual queries
            queries = []
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                # Remove numbering and clean up
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                    # Remove number, period, and any leading spaces
                    clean_query = line
                    for char_num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        if clean_query.startswith(char_num):
                            parts = clean_query.split('.', 1)
                            if len(parts) > 1:
                                clean_query = parts[1].strip()
                            break
                    
                    # Remove bullet points
                    clean_query = clean_query.lstrip('-* ').strip()
                    
                    # Skip if too short or empty
                    if len(clean_query) > 10:
                        queries.append(clean_query)
            
            # Ensure we have the requested number of queries
            if len(queries) < num_queries:
                print(f"Warning: Generated {len(queries)} queries instead of {num_queries}")
            else:
                queries = queries[:num_queries]
            
            return queries
            
        except Exception as e:
            raise Exception(f"Failed to generate search queries: {str(e)}")
