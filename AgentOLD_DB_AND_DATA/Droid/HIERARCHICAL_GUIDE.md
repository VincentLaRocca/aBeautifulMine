# Hierarchical Crypto Question Generator

## 🎯 Next Evolution of Q&A Generation

This advanced system creates **topic → subtopic → questions** hierarchies perfect for structured RAG systems and comprehensive knowledge bases.

## 📊 What It Creates:

### 📁 Output Structure:
```
hierarchical_crypto_questions/
├── bitcoin_trading_patterns/
│   ├── bitcoin_trading_patterns_complete.json
│   ├── bitcoin_trading_patterns_index.txt
│   ├── bitcoin_trading_patterns_rag_pairs.txt
│   ├── pattern_recognition.txt
│   ├── entry_exit_strategies.txt
│   ├── volume_analysis.txt
│   └── time_frame_optimization.txt
└── technical_analysis_indicators/
    ├── [similar structure]
```

### 🔄 Hierarchical Flow:
**Main Topic** → **4 Subtopics** → **3 Questions each** = **12 focused questions per topic**

### 📝 Multiple Output Formats:

1. **`complete.json`** - Full structure for programmatic use
2. **`index.txt`** - Human-readable overview with summaries  
3. **`rag_pairs.txt`** - Question | Context for embedding generation
4. **`individual.txt`** - Each subtopic as separate file

### 🎯 Example Output:

#### Input:
```
Topic: "Bitcoin Trading Patterns"
```

#### Generated Hierarchical Structure:
```
Bitcoin Trading Patterns
├── Pattern Recognition Basics
│   1. How do you identify head and shoulders patterns in Bitcoin charts?
│   2. What volume confirmation signals validate Bitcoin triangle patterns?
│   3. When should traders consider double tops in Bitcoin analysis?
├── Entry Exit Strategies  
│   1. What are optimal entry points for Bitcoin breakout patterns?
│   2. How do you set profit targets based on Bitcoin pattern measurements?
│   3. When should you exit Bitcoin trades after pattern failures?
├── Volume Analysis Integration
│   1. How does volume divergence affect Bitcoin pattern reliability?
│   2. What role does decreasing volume play in Bitcoin consolidation patterns?
│   3. How can you use volume spikes to confirm Bitcoin trend changes?
└── Time Frame Optimization
│   1. Which time frames are most reliable for Bitcoin pattern analysis?
│   2. How do Bitcoin patterns differ between 4-hour and daily charts?
│   3. What are the risks of trading Bitcoin patterns on smaller time frames?
```

## 🚀 Usage Options:

### Option 1: Single Topic Generation
```bash
set TOPIC_NAME=Bitcoin Trading Strategies
set OPENROUTER_API_KEY=your_key_here
python hierarchical_crypto_generator.py
```

### Option 2: Batch from Existing Topics
```bash
set OPENROUTER_API_KEY=your_key_here
python hierarchical_crypto_generator.py
```

This will read your original topics file and convert the first 2 into hierarchical structures (testing mode).

## 🎯 Advantages for RAG Systems:

### 🧠 Better Retrieval:
- **Focused context** - Questions are linked to specific subtopics
- **Hierarchical indexing** - Can retrieve at topic or subtopic level
- **Context pairs** - Question | Subtopic format for embedding generation

### 📈 Enhanced Learning Path:
- **Logical progression** - Subtopics build on each other
- **Structured navigation** - Clear learning sequence
- **Scalable depth** - Easy to add more questions to any subtopic

### 🔍 Search Flexibility:
- **Multi-level search** - Topic → Subtopic → Specific Question
- **Context-aware** - Higher retrieval accuracy with subtopic metadata
- **Granular chunking** - Each subtopic is a perfect RAG chunk size

## 🛠️ Advanced Features:

### 📊 Automatic Subtopic Generation:
- **Logical breakdown** - AI creates meaningful subtopic divisions
- **Educational flow** - Subtopics progress from basic to advanced
- **Topic specificity** - Subtopics are tailored to each main topic

### 🎯 Question Distribution:
- **Equal coverage** - Consistent number of questions per subtopic
- **Targeted complexity** - Questions match subtopic difficulty
- **Practical focus** - Real-world trading applications

### 📁 Multiple Output Formats:
- **JSON** - For programmatic integration
- **Text** - For human reading and editing
- **RAG pairs** - Optimized for embedding generation
- **Index** - Overview and navigation

## 🔧 Customization Options:

### 🎛️ Adjust Parameters:
```python
# Change these in the generator:
num_subtopics = 4      # Number of subtopics per main topic
questions_per_subtopic = 3  # Questions generated for each subtopic
```

### 📝 Modify Prompts:
- **Subtopic focus areas** - Can specify what types of subtopics you want
- **Question difficulty** - Can target beginner/intermediate/expert levels
- **Question style** - Can focus on theory vs. practical applications

## 🎯 Perfect Use Cases:

### 🤖 Trading Chatbots:
- **Topic-specific expertise** - Deep knowledge in specific areas
- **Progressive explanations** - Can explain concepts step-by-step
- **Contextual responses** - Answers tied to relevant subtopics

### 📚 Educational Platforms:
- **Course structure** - Subtopics become lesson modules
- **Practice questions** - Built-in assessment materials
- **Learning paths** - Clear progression from basic to advanced

### 📊 Knowledge Management:
- **Organized repository** - Structured storage of trading knowledge
- **Easy maintenance** - Can add questions to specific subtopics
- **Scalable expansion** - Can grow knowledge base systematically

## 🎉 Next Steps:

Run the generator with your specific topic of interest:

```bash
# Custom topic
set TOPIC_NAME=Ethereum DeFi Strategies
set OPENROUTER_API_KEY=your_key
python hierarchical_crypto_generator.py

# Or batch mode
set OPENROUTER_API_KEY=your_key  
python hierarchical_crypto_generator.py
```

The hierarchical structure will give you much better organization for RAG systems and create a more comprehensive, searchable knowledge base!
