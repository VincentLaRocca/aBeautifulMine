# Quick Start Guide

## Prerequisites

1. **LLM Server Running**: Make sure your Mixtral server (or other LLM) is running:
   ```bash
   python run_server.py
   # Server should be at http://localhost:8080/v1
   ```

2. **Dependencies Installed**:
   ```bash
   pip install chromadb openai python-dotenv
   ```

3. **Environment Variables** (optional, defaults provided):
   ```bash
   # .env file
   MIXTRAL_SERVER_URL=http://localhost:8080/v1
   CHROMADB_PATH=chroma_db
   ```

## Quick Start

### Option 1: Command Line (Easiest)

```bash
python run_multi_agent.py "Cryptocurrency Technical Analysis"
```

That's it! The system will:
1. Generate subtopics
2. Create 100 questions per subtopic
3. Research each question
4. Generate comprehensive answers
5. Insert into ChromaDB

### Option 2: Python Script

```python
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()
results = orchestrator.run_full_pipeline("Your Topic Here")
```

### Option 3: Step by Step (For Testing)

```python
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

# Step 1: Generate subtopics
step1 = orchestrator.step1_generate_subtopics("Cryptocurrency Trading")

# Step 2: Generate questions (just for first subtopic)
step2 = orchestrator.step2_generate_questions(step1["subtopics"][0], 0)

# Step 3: Research (just first 5 questions for testing)
step3 = orchestrator.step3_research_questions(step2["questions"][:5], step1["subtopics"][0])

# Step 4: Generate answers
step4 = orchestrator.step4_generate_answers(step2["questions"][:5], step3["research_results"], step1["subtopics"][0])

# Step 5: Insert to database
step5 = orchestrator.step5_insert_to_database(step4["qa_pairs"])
```

## Output

All output is saved to `multi_agent_output/`:
- `task_lists/` - Subtopic task lists
- `questions/` - Generated questions
- `research/` - Research results
- `answers/` - Q&A pairs
- `pipeline_results_*.json` - Complete pipeline results

## Resuming

If the pipeline is interrupted, you can resume from a specific subtopic:

```bash
python run_multi_agent.py "Your Topic" 5
# Resumes from subtopic index 5
```

## Customization

### Change Number of Questions

Edit `config.json` or pass custom config:

```python
config = {"questions_per_topic": 50}  # Instead of 100
orchestrator = MultiAgentOrchestrator(config=config)
```

### Custom Answer Prompt

```python
custom_prompt = """Your custom prompt here..."""
config = {"answer_prompt": custom_prompt}
orchestrator = MultiAgentOrchestrator(config=config)
```

## Troubleshooting

### "Connection refused" error
→ Make sure your LLM server is running

### "chromadb not installed"
→ Run: `pip install chromadb`

### Answers too short
→ The system automatically expands answers <3000 chars

### Out of memory
→ Process subtopics one at a time or reduce `questions_per_topic`

## Performance

- **Per Question**: ~1-2 minutes (research + answer)
- **100 Questions**: ~2-3 hours
- **10 Subtopics**: ~20-30 hours total

Consider running overnight or in batches!

