import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Model configurations
    QUERY_GENERATOR_MODEL = "anthropic/claude-3-haiku"
    SEARCH_MODEL = "anthropic/claude-3-haiku"
    REPORT_AGGREGATOR_MODEL = "anthropic/claude-3-haiku"
    
    # API settings
    MAX_CONCURRENT_SEARCHES = 10
    REQUEST_TIMEOUT = 60
    RETRY_ATTEMPTS = 3
    
    @classmethod
    def validate_config(cls):
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
