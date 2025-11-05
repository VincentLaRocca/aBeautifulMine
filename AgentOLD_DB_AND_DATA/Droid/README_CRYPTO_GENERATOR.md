# Crypto Question Generator

**Enhanced Gemini-powered question generation system for cryptocurrency trading topics**

## 📋 PROJECT SUMMARY

This project parses a comprehensive crypto topics document (132 topics across 22 categories) and generates 15 AI-crafted questions per topic using OpenRouter's Gemini API.

### Files Created:
- `crypto_question_generator.py` - Main script with full functionality
- `run_generator.py` - Helper script for easy API key management  
- `demo_generator.py` - Demo version showing parsing capability
- `test_crypto_parser.py` - Parser testing script

## 🚀 HOW TO USE

### Option 1: Quick Start with API Key
```bash
# Replace YOUR_KEY with your actual OpenRouter API key
python run_generator.py YOUR_KEY_HERE
```

### Option 2: Environment Variable Method
```bash
# Set environment variable (Windows)
set OPENROUTER_API_KEY=your_api_key_here

# Run the generator
python crypto_question_generator.py
```

### Option 3: Test Without API Key
```bash
# See how it works without API calls
python demo_generator.py
```

## 📊 EXPECTED OUTPUT

**Input File:** `CRYPTO_TOPICS_FOR_QUESTION_HARVESTING.md`
- 16 topic blocks with detailed content
- Categories: Price Patterns, Technical Indicators, On-Chain Analysis, etc.
- Complexity levels: Beginner to Expert
- Applications: Theory, Practice, Strategy, Risk Management

**Output Directory:** `crypto_questions/`
- 16 individual text files
- Each file contains 15 questions
- Total: ~240 questions generated

**Sample File Format:**
```
# Questions for: Head and shoulders pattern identification and trading

# Category: Price Patterns
# Topic ID: PP_001  
# Complexity: Intermediate
# Application: Theory + Practice

1. How can head and shoulders patterns be used to identify trend reversals in cryptocurrency markets?
2. What are the key volume confirmation signals needed for valid head and shoulders patterns?
... (13 more questions)
```

## 🔧 TECHNICAL FEATURES

### Topic Metadata Extraction:
- Category classification
- Complexity level tagging  
- Application focus identification
- Asset type specification
- Timeframe recommendations

### Question Generation Strategy:
- **5 Fundamental Questions** - Core concept understanding
- **5 Strategy Questions** - Practical trading applications
- **3 Risk Questions** - Risk management considerations  
- **2 Advanced Questions** - Edge cases and expert scenarios

### AI Integration:
- Uses OpenRouter API with Gemini 2.0 Flash model
- Structured prompts for consistent quality
- Crypto market context integration
- Question diversity and validation

## 📈 TOPIC COVERAGE

The generator covers these major categories:

1. **Price Patterns & Chart Analysis** (PP_001, PP_002)
2. **Technical Indicators** (MA_001, MOM_001, VOL_001)
3. **On-Chain Analysis** (ONCHAIN_001, ONCHAIN_ADV_001)
4. **Trading Psychology** (PSYCH_001)
5. **Risk Management** (RISK_001)
6. **Regulatory Analysis** (REG_001)
7. **DeFi Analysis** (DEFI_001)
8. **Data Analytics** (DATA_001)
9. **Quantitative Trading** (QUANT_001)
10. **Portfolio Management** (PORTFOLIO_001)
11. **Security** (SECURITY_001)

## 🎯 READY TO USE

The system is fully functional and ready to generate your complete crypto Q&A knowledge base. 

**Next Steps:**
1. Get your OpenRouter API key from https://openrouter.ai/
2. Run the generator with your API key
3. Review the 16 generated question files
4. Use for RAG training, education, or assessment creation

## 💡 CUSTOMIZATION OPTIONS

The script can be easily modified to:
- Change question counts per topic
- Adjust question complexity distribution  
- Add different focus areas (e.g., more DeFi-specific questions)
- Change AI model or provider
- Modify output formatting

---

**Total Expected Questions: 240**  
**Processing Time: ~5-10 minutes**  
**Estimated API Cost: <$1**
