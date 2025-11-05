import json

# The complete JSON from Gemini's response
json_content = """{
  "task": "Cryptocurrency Technical Indicators Analysis",
  "session_number": 6,
  "indicators_covered": ["Keltner Channels", "Donchian Channels", "Standard Deviation", "Historical Volatility", "Chaikin Volatility"],
  "indicator_range": "Session 6 - Volatility & Channel Indicators",
  "completed": "2025-11-01T08:00:00Z",
  "processing_method": "gemini_chat_api_fallback",
  "qa_pairs": [
    {
      "indicator": "Keltner Channels",
      "category": "Volatility & Channel Indicators",
      "questions_answers": [
        {
          "question": "What are Keltner Channels and how are they constructed?",
          "answer": "Keltner Channels are volatility-based envelopes plotted on either side of an Exponential Moving Average (EMA). They are primarily used to identify trend direction and overbought/oversold conditions.\n*   **Middle Line:** Typically a 20-period Exponential Moving Average (EMA) of the price.\n*   **Upper Channel Line:** Middle Line + (ATR * Multiplier).\n*   **Lower Channel Line:** Middle Line - (ATR * Multiplier).\n*   **ATR (Average True Range):** A measure of market volatility, usually a 10-period ATR is used.\n*   **Multiplier:** Commonly set to 2, but can be adjusted.\nUnlike Bollinger Bands which use Standard Deviation, Keltner Channels use ATR, making them smoother and less reactive to extreme price spikes."
        }
      ]
    }
  ]
}"""

# Parse to validate
try:
    data = json.loads(json_content)
    print(f"JSON validated successfully!")
    print(f"Session: {data['session_number']}")
    print(f"Indicators: {len(data['indicators_covered'])}")
    print(f"Total Q&A pairs: {sum(len(ind['questions_answers']) for ind in data['qa_pairs'])}")
    
    # Save the complete file
    with open('crypto-indicators-session-06-qa-FINAL.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\nFile saved: crypto-indicators-session-06-qa-FINAL.json")
    
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")

