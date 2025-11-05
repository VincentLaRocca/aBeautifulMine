#!/usr/bin/env python3

import requests
import json

def test_available_models(api_key):
    """Test which free models are available on OpenRouter"""
    
    print("TESTING AVAILABLE FREE MODELS")
    print("=" * 50)
    
    # Try different free models that should work
    test_models = [
        "meta-llama/llama-3.1-8b-instruct",
        "microsoft/wizardlm-2-8x22b",
        "qwen/qwen-2.5-7b-instruct", 
        "meta-llama/llama-3-8b-instruct",
        "anthropic/claude-3.5-haiku"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    working_models = []
    
    for model in test_models:
        print(f"\nTesting: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'Model working: [model_name]'"}
            ],
            "max_tokens": 30
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"  ✓ SUCCESS: {content[:50]}...")
                working_models.append(model)
            else:
                error_info = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                print(f"  - FAILED: {response.status_code}")
                if 'error' in error_info:
                    print(f"    {error_info['error'].get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"  - ERROR: {str(e)[:50]}")
    
    print(f"\n{'='*50}")
    print(f"Working models ({len(working_models)}):")
    for model in working_models:
        print(f"  ✓ {model}")
    
    return working_models

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your OpenRouter API key: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided")
        sys.exit(1)
    
    working_models = test_available_models(api_key)
    
    if working_models:
        print(f"\n🎉 Found {len(working_models)} working models!")
        print("You can now run the DeFi test with these models.")
    else:
        print(f"\n❌ No working models found.")
        print("Please check your API key or OpenRouter account.")
