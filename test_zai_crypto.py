import requests
import json

url = "https://api.z.ai/api/paas/v4/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 1799f7bc0add4cd8abd83343b32a4e33.EJhs1tr4OUXi0zyA"
}

payload = {
    "model": "glm-4-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are an expert in cryptocurrency fundamentals and institutional investment."
        },
        {
            "role": "user",
            "content": "Explain Bitcoin's halving cycle and its impact on institutional adoption. Provide a detailed answer suitable for professional investors."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

response = requests.post(url, headers=headers, json=payload, timeout=60)
result = response.json()

print("="*80)
print("Z.AI CRYPTO RESEARCH TEST")
print("="*80)

if 'choices' in result:
    content = result['choices'][0]['message']['content']
    print("\nResponse:")
    print(content)
    print(f"\nTokens used: {result['usage']['total_tokens']}")
    print(f"Model: {result['model']}")
    print("\n✅ SUCCESS - Z.AI is ready for institutional crypto research!")
else:
    print("\nError:")
    print(json.dumps(result, indent=2))

print("="*80)
