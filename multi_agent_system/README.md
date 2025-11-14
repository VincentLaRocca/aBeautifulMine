# Multi-Agent Q&A Dataset Creation System

A comprehensive multi-agent system for creating high-quality AI training datasets in the form of question-answer pairs.

## Overview

This system automates the complete pipeline for creating Q&A datasets:

1. **Topic → Subtopics**: Break down a main topic into comprehensive subtopics
2. **Subtopic → 100 Questions**: Generate 100 high-quality questions per subtopic
3. **Questions → Research**: Perform deep research on each question
4. **Questions → Answers**: Generate comprehensive 3000+ character answers using your specific prompt
5. **Q&A Pairs → Database**: Insert Q&A pairs into ChromaDB for RAG/training

## Architecture

The system consists of 5 specialized agents:

- **SubtopicGeneratorAgent**: Generates comprehensive subtopic lists
- **QuestionGeneratorAgent**: Creates 100 questions per subtopic
- **ResearchAgent**: Performs deep research on questions
- **AnswerGeneratorAgent**: Generates detailed answers using your prompt
- **DatabaseAgent**: Inserts Q&A pairs into ChromaDB

All agents are orchestrated by the **MultiAgentOrchestrator**.

## Installation

1. **Install dependencies**:
```bash
pip install chromadb openai python-dotenv
```

2. **Ensure your LLM server is running** (e.g., Mixtral via llama.cpp):
```bash
# In another terminal
python run_server.py  # or your server startup command
```

3. **Set environment variables** (optional, defaults provided):
```bash
# .env file
MIXTRAL_SERVER_URL=http://localhost:8080/v1
CHROMADB_PATH=chroma_db
```

## Usage

### Basic Usage

```python
from multi_agent_system import MultiAgentOrchestrator

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator()

# Run full pipeline
results = orchestrator.run_full_pipeline("Cryptocurrency Technical Analysis")
```

### Command Line

```bash
# Run full pipeline
python multi_agent_system/orchestrator.py "Cryptocurrency Technical Analysis"

# Resume from a specific subtopic (if pipeline was interrupted)
python multi_agent_system/orchestrator.py "Cryptocurrency Technical Analysis" 5
```

### Step-by-Step Usage

You can also run individual steps:

```python
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

# Step 1: Generate subtopics
step1 = orchestrator.step1_generate_subtopics("Cryptocurrency Trading")

# Step 2: Generate questions for a subtopic
step2 = orchestrator.step2_generate_questions("Price Patterns", subtopic_index=0)

# Step 3: Research questions
step3 = orchestrator.step3_research_questions(step2["questions"], "Price Patterns")

# Step 4: Generate answers
step4 = orchestrator.step4_generate_answers(
    step2["questions"], 
    step3["research_results"], 
    "Price Patterns"
)

# Step 5: Insert to database
step5 = orchestrator.step5_insert_to_database(step4["qa_pairs"])
```

## Output Structure

The system creates the following directory structure:

```
multi_agent_output/
├── task_lists/          # Subtopic task lists (JSON)
├── questions/           # Generated questions (JSON)
├── research/            # Research results (JSON)
├── answers/             # Q&A pairs (JSON)
└── pipeline_results_*.json  # Complete pipeline results
```

## Configuration

Edit `config.json` or pass configuration to `MultiAgentOrchestrator()`:

```python
config = {
    "model_url": "http://localhost:8080/v1",
    "questions_per_topic": 100,
    "output_dir": "my_output",
    "db_path": "my_chromadb",
    "answer_prompt": "Your custom prompt..."
}

orchestrator = MultiAgentOrchestrator(config=config)
```

## Features

- **Parallel Processing**: Agents can work on different subtopics simultaneously
- **Resume Capability**: Resume from any subtopic if pipeline is interrupted
- **Comprehensive Logging**: Detailed progress tracking and statistics
- **Error Handling**: Robust error handling with graceful degradation
- **Modular Design**: Use individual agents independently if needed
- **Database Integration**: Automatic ChromaDB integration for RAG

## Example Workflow

1. **Start with a topic**: "Cryptocurrency Technical Analysis"
2. **System generates subtopics**: 
   - Price Patterns
   - Moving Averages
   - Support and Resistance
   - Indicators (RSI, MACD, etc.)
   - ... (10-50 subtopics)
3. **For each subtopic**:
   - Generate 100 questions
   - Research each question
   - Generate 100 comprehensive answers
   - Insert into database
4. **Result**: Thousands of high-quality Q&A pairs ready for training

## Performance Considerations

- **Processing Time**: ~1-2 minutes per question (research + answer generation)
- **100 Questions**: ~2-3 hours per subtopic
- **10 Subtopics**: ~20-30 hours total
- **Rate Limiting**: Built-in delays to avoid overwhelming the LLM server

## Troubleshooting

### LLM Server Not Running
```
Error: Connection refused
```
**Solution**: Start your LLM server (`python run_server.py`)

### ChromaDB Not Installed
```
ImportError: chromadb is not installed
```
**Solution**: `pip install chromadb`

### Answers Too Short
The system automatically detects and expands answers that are too short (<3000 chars).

### Out of Memory
If processing many questions, consider:
- Processing subtopics one at a time
- Reducing `questions_per_topic` in config
- Using batch processing

## Advanced Usage

### Custom Answer Prompt

```python
custom_prompt = """Your custom prompt here..."""

orchestrator = MultiAgentOrchestrator(config={
    "answer_prompt": custom_prompt
})
```

### Query Database

```python
from multi_agent_system import DatabaseAgent

db_agent = DatabaseAgent()
results = db_agent.query_similar("What is RSI?", n_results=5)
```

## Contributing

The system is designed to be modular. You can:
- Add new agents
- Customize prompts
- Add new output formats
- Integrate with other databases

## License

Part of the crypto AI training dataset project.

