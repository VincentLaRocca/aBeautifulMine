import requests
import json
import time
from typing import Dict, List, Optional
from config import Config

class OpenRouterClient:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        
        
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ultra-deep-research",
            "X-Title": "Ultra Deep Research CLI"
        }
    
    def make_request(self, model: str, messages: List[Dict[str, str]], 
                     temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict:
        """Make a synchronous request to OpenRouter API"""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            return response.json()
            
        except requests.Timeout:
            raise Exception(f"Request timeout after {Config.REQUEST_TIMEOUT} seconds")
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def generate_response(self, model: str, prompt: str, 
                         system_prompt: Optional[str] = None) -> dict:
        """Generate response from specified model, returns response with token usage"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(Config.RETRY_ATTEMPTS):
            try:
                response = self.make_request(model, messages)
                
                # Extract token usage information
                usage = response.get("usage", {})
                tokens_used = {
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                }
                
                return {
                    "content": response["choices"][0]["message"]["content"].strip(),
                    "tokens": tokens_used
                }
                
            except Exception as e:
                if attempt == Config.RETRY_ATTEMPTS - 1:
                    raise Exception(f"Failed to generate response after {Config.RETRY_ATTEMPTS} attempts: {str(e)}")
                
                time.sleep(2 ** attempt)  # Exponential backoff
