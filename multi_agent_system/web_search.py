"""
Web Search Module
Provides web search capability for research agents
Supports multiple search providers with fallback options
"""

import os
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()


def web_search_brave(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Search using Brave Search API

    Args:
        query: Search query
        count: Number of results to return

    Returns:
        List of search result dictionaries with 'title', 'snippet', 'url'
    """
    try:
        import requests

        api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        if not api_key:
            return []

        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }
        params = {
            "q": query,
            "count": count
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get('web', {}).get('results', [])[:count]:
            results.append({
                'title': item.get('title', ''),
                'snippet': item.get('description', ''),
                'url': item.get('url', ''),
                'content': item.get('description', '')  # Use description as content
            })

        return results

    except Exception as e:
        print(f"  [WARNING] Brave search failed: {e}")
        return []


def web_search_google(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Search using Google Custom Search API

    Args:
        query: Search query
        count: Number of results to return

    Returns:
        List of search result dictionaries with 'title', 'snippet', 'url'
    """
    try:
        import requests

        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

        if not api_key or not search_engine_id:
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": count
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get('items', [])[:count]:
            results.append({
                'title': item.get('title', ''),
                'snippet': item.get('snippet', ''),
                'url': item.get('link', ''),
                'content': item.get('snippet', '')
            })

        return results

    except Exception as e:
        print(f"  [WARNING] Google search failed: {e}")
        return []


def web_search_duckduckgo(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Search using DuckDuckGo (no API key required)

    Args:
        query: Search query
        count: Number of results to return

    Returns:
        List of search result dictionaries with 'title', 'snippet', 'url'
    """
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=count):
                results.append({
                    'title': r.get('title', ''),
                    'snippet': r.get('body', ''),
                    'url': r.get('href', ''),
                    'content': r.get('body', '')
                })

        return results

    except Exception as e:
        print(f"  [WARNING] DuckDuckGo search failed: {e}")
        return []


def web_search(query: str, count: int = 5, provider: str = "auto") -> Optional[List[Dict[str, str]]]:
    """
    Perform web search with automatic provider fallback

    Args:
        query: Search query
        count: Number of results to return
        provider: Search provider ("auto", "brave", "google", "duckduckgo")

    Returns:
        List of search result dictionaries or None if all providers fail
    """
    if provider == "auto":
        # Try providers in order of preference
        providers = ["brave", "google", "duckduckgo"]
    else:
        providers = [provider]

    for prov in providers:
        if prov == "brave":
            results = web_search_brave(query, count)
        elif prov == "google":
            results = web_search_google(query, count)
        elif prov == "duckduckgo":
            results = web_search_duckduckgo(query, count)
        else:
            continue

        if results:
            print(f"  [WEB SEARCH] Found {len(results)} results via {prov.upper()}")
            return results

    print(f"  [WEB SEARCH] All providers failed for query: {query[:60]}...")
    return None


# Example usage
if __name__ == "__main__":
    # Test web search
    results = web_search("Bitcoin price prediction cryptocurrency", count=3)

    if results:
        print("\nSearch Results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Snippet: {result['snippet'][:200]}...")
    else:
        print("\nNo results found. Please configure search API keys in .env:")
        print("  - BRAVE_SEARCH_API_KEY (recommended)")
        print("  - GOOGLE_SEARCH_API_KEY + GOOGLE_SEARCH_ENGINE_ID")
        print("  - Or install: pip install duckduckgo-search")
