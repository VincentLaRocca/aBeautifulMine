# Multi-Agent Training Pipeline - Complete System

**Version:** 1.0
**Last Updated:** 2025-01-12
**Status:** Production Ready

---

## 🎯 What This System Does

This is a **complete end-to-end pipeline** that transforms a single topic into a fully trained, domain-expert AI model:

```
Topic → Dataset Generation → ChromaDB Storage → Data Extraction → Model Training → Deployed Model
```

**Input:** A single topic string (e.g., "Cryptocurrency Technical Analysis")
**Output:** A fine-tuned AI model expert in that domain

---

## 📦 Complete System Components

### **Phase 1: Dataset Generation** (Agents 1-5)

| Agent | File | Purpose |
|-------|------|---------|
| **Orchestrator** | `orchestrator.py` | Coordinates all agents |
| **Agent 1** | `subtopic_generator.py` | Topic → 10-50 subtopics |
| **Agent 2** | `question_generator.py` | Subtopic → 100 questions |
| **Agent 3** | `research_agent.py` | Questions → Research notes |
| **Agent 4** | `answer_generator.py` | Questions → 3000+ char answers |
| **Agent 5** | `database_agent.py` | Q&A pairs → ChromaDB |

### **Phase 2: Data Extraction** (New!)

| Tool | File | Purpose |
|------|------|---------|
| **Extractor** | `extract_training_data.py` | ChromaDB → Training formats |

**Supported Formats:**
- ✅ OpenAI (messages format) - Most compatible
- ✅ Alpaca (instruction format)
- ✅ ShareGPT (conversation format)
- ✅ JSONL (simple format)
- ✅ Raw (with full metadata)

**Features:**
- Train/Val/Test splits (80/10/10)
- Topic/subtopic filtering
- Quality statistics
- Batch processing (1000s of Q&A pairs)

### **Phase 3: Training Preparation** (New!)

| Tool | File | Purpose |
|------|------|---------|
| **Trainer** | `train_model.py` | Generate training scripts |

**Supported Frameworks:**
- ✅ Unsloth (2x faster, recommended)
- ✅ Axolotl (advanced config)
- ✅ Transformers (standard)

**Features:**
- Auto-generated training scripts
- GGUF export (for llama.cpp)
- LoRA fine-tuning
- 4-bit quantization
- Comprehensive quick start guide

### **Phase 4: Domain Configuration**

| Tool | File | Purpose |
|------|------|---------|
| **Config** | `domain_config.py` | Domain-specific settings |

**Built-in Domains:**
- 🪙 Cryptocurrency (default)
- 🏥 Medicine
- ⚖️ Law
- 💻 Programming
- 💰 Finance
- 📚 General knowledge

---

## 🚀 Quick Start

### **Option 1: Automated Pipeline (Recommended)**

```bash
# Run complete pipeline
complete_pipeline.bat "Your Topic"

# Follow the prompts to:
# 1. Generate dataset (20-30 hours)
# 2. Extract training data (5 mins)
# 3. Prepare training scripts (2 mins)
# 4. Train model (2-6 hours)
```

### **Option 2: Step-by-Step**

```bash
# Step 1: Generate dataset
python run_multi_agent.py "Cryptocurrency Technical Analysis"

# Step 2: Extract training data
python multi_agent_system/extract_training_data.py openai --split

# Step 3: Prepare training
python multi_agent_system/train_model.py training_data/train_openai_*.jsonl

# Step 4: Train model
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
python trained_models/train_unsloth_*.py
```

### **Option 3: Python API**

```python
from multi_agent_system import (
    MultiAgentOrchestrator,
    TrainingDataExtractor,
    ModelTrainer
)

# 1. Generate dataset
orchestrator = MultiAgentOrchestrator()
results = orchestrator.run_full_pipeline("Cryptocurrency Trading")

# 2. Extract training data
extractor = TrainingDataExtractor()
extraction = extractor.export_splits(output_format="openai")

# 3. Prepare training
trainer = ModelTrainer(framework="unsloth")
script = trainer.prepare_unsloth_training(
    training_data_path=extraction["splits"]["train"]["file"]
)

# 4. Run training script
# python {script}
```

---

## 📊 Expected Results

### **Dataset Quality**
- ✅ 1000+ Q&A pairs (10 subtopics × 100 questions)
- ✅ 3000+ characters per answer
- ✅ Expert-level comprehensive explanations
- ✅ Structured markdown formatting
- ✅ Domain-specific examples

### **Training Performance (RTX 5090)**
- ⏱️ Training time: 2-4 hours (1000 pairs, 3 epochs)
- 💾 VRAM usage: 20-25GB
- 📈 Loss: Steadily decreasing
- 🎯 Quality: Expert-level domain responses

### **Model Capabilities**
After training, your model will:
- Answer domain questions with 3000+ char comprehensive responses
- Maintain consistent style from training data
- Use domain-specific terminology correctly
- Provide practical examples and applications
- Demonstrate deep knowledge from curated dataset

---

## 🎛️ Configuration

### **Dataset Generation Config**

```python
# In orchestrator.py or via config dict
config = {
    "domain": "cryptocurrency",  # or medicine, law, programming, finance
    "questions_per_topic": 100,  # 50-200
    "model_url": "http://localhost:8080/v1",
    "output_dir": "multi_agent_output",
    "db_path": "chroma_db",
    "answer_prompt": "..."  # Custom answer generation prompt
}

orchestrator = MultiAgentOrchestrator(config=config)
```

### **Domain-Specific Configuration**

```python
from multi_agent_system import get_domain_config

# Use built-in domain
crypto_config = get_domain_config("cryptocurrency")
medicine_config = get_domain_config("medicine")

# Or create custom domain
from multi_agent_system import create_custom_domain

custom = create_custom_domain(
    name="Machine Learning",
    research_specialization="machine learning and artificial intelligence",
    research_sources="peer-reviewed papers, ML frameworks, recognized researchers",
    example_context="ML model examples and training scenarios",
    example_types="machine learning examples",
    practical_context="ML development scenarios",
    audience="ML engineers and data scientists",
    domain_characteristics="model training, hyperparameters, evaluation metrics"
)
```

### **Training Hyperparameters**

```python
# In train_model.py or generated script
max_seq_length = 2048      # 1024-4096 (context window)
learning_rate = 2e-4       # 1e-4 to 5e-4
num_epochs = 3             # 1-10 (3-5 recommended)
batch_size = 2             # 1-4 (depends on VRAM)
gradient_accumulation = 4  # Effective batch = batch_size * this
lora_r = 16                # 8-64 (LoRA rank)
lora_alpha = 16            # Usually same as lora_r
lora_dropout = 0.05        # 0-0.1
```

---

## 📁 Output Structure

```
crypto/
├── multi_agent_output/              # Phase 1: Generated Q&A data
│   ├── task_lists/                  # Subtopic lists
│   ├── questions/                   # Generated questions
│   ├── research/                    # Research notes
│   └── answers/                     # Q&A pairs
│
├── chroma_db/                       # Phase 1: Vector database
│   └── qa_dataset/                  # ChromaDB collection
│
├── training_data/                   # Phase 2: Extracted training data
│   ├── train_openai_*.jsonl         # Training set (80%)
│   ├── val_openai_*.jsonl           # Validation set (10%)
│   └── test_openai_*.jsonl          # Test set (10%)
│
└── trained_models/                  # Phase 3 & 4: Training & models
    ├── train_unsloth_*.py           # Generated training script
    ├── TRAINING_QUICKSTART.md       # Training guide
    ├── checkpoints/                 # Training checkpoints
    ├── final_model/                 # HuggingFace format
    └── final_model_gguf/            # GGUF for llama.cpp
```

---

## 🔧 Advanced Usage

### **Resume Interrupted Generation**

```bash
# Auto-detect resume point
python run_multi_agent.py --continue

# Or specify subtopic index
python run_multi_agent.py "Your Topic" 5  # Resume from subtopic 5
```

### **Extract Specific Data**

```bash
# Extract specific topic
python multi_agent_system/extract_training_data.py openai --topic "Cryptocurrency"

# Extract specific subtopic
python multi_agent_system/extract_training_data.py openai --subtopic "Price Patterns"

# Custom output directory
python multi_agent_system/extract_training_data.py openai --output my_data_dir
```

### **Multiple Domains**

```bash
# Generate datasets for multiple related domains
python run_multi_agent.py "Cryptocurrency Trading"
python run_multi_agent.py "DeFi Protocols"
python run_multi_agent.py "NFT Markets"

# Extract all together into one training set
python multi_agent_system/extract_training_data.py openai --split

# Train on combined multi-domain dataset
python multi_agent_system/train_model.py training_data/train_openai_*.jsonl --epochs 5
```

### **Custom Training Frameworks**

```bash
# Prepare for different frameworks
python multi_agent_system/train_model.py data.jsonl --framework unsloth
python multi_agent_system/train_model.py data.jsonl --framework axolotl
python multi_agent_system/train_model.py data.jsonl --framework transformers

# Custom model and hyperparameters
python multi_agent_system/train_model.py data.jsonl \
  --framework unsloth \
  --model unsloth/mistral-7b-v0.3 \
  --epochs 5 \
  --lr 3e-4 \
  --output custom_model_dir
```

---

## 🐛 Troubleshooting

### **Dataset Generation**

**Problem:** ChromaDB insertion fails
```bash
# Solution: Check disk space, reinstall ChromaDB
pip install --upgrade chromadb
```

**Problem:** Answers too short (<3000 chars)
```bash
# Solution: Adjust temperature or modify answer_generator.py
# The agent will automatically try to expand short answers
```

**Problem:** Generation interrupted
```bash
# Solution: Resume from last checkpoint
python run_multi_agent.py "Your Topic" --continue
```

### **Data Extraction**

**Problem:** Can't find ChromaDB collection
```bash
# Solution: Verify collection name
python -c "import chromadb; client = chromadb.PersistentClient(path='chroma_db'); print(client.list_collections())"
```

**Problem:** Wrong format for training
```bash
# Solution: Re-extract in correct format
python multi_agent_system/extract_training_data.py openai --split
```

### **Training**

**Problem:** Out of memory (OOM)
```bash
# Solution 1: Reduce batch_size to 1
# Solution 2: Reduce max_seq_length to 1024
# Solution 3: Use gradient checkpointing (already enabled)
```

**Problem:** Training too slow
```bash
# Solution: Use Unsloth (2x faster than standard)
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

**Problem:** Model not learning
```bash
# Solution 1: Increase learning rate to 3e-4 or 5e-4
# Solution 2: Train for more epochs (5-10)
# Solution 3: Verify data format is correct
```

---

## 📚 Documentation

- **Complete Pipeline:** `../COMPLETE_TRAINING_PIPELINE.md`
- **System Overview:** `../MULTI_AGENT_SYSTEM_SUMMARY.md`
- **Training Guide:** `trained_models/TRAINING_QUICKSTART.md`
- **Domain Config:** `domain_config.py`
- **Quick Start:** This file

---

## 🎓 Use Cases

### **Current: Cryptocurrency Trading**
Generate expert-level crypto trading Q&A, train custom model, deploy for trading analysis

### **Medicine: Medical Q&A**
```python
config = {"domain": "medicine"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Cardiovascular Diseases")
```

### **Law: Legal Training**
```python
config = {"domain": "law"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Contract Law Fundamentals")
```

### **Programming: Coding Tutor**
```python
config = {"domain": "programming"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Python Advanced Patterns")
```

---

## 🏆 System Achievements

✅ **Fully automated** dataset generation
✅ **Domain-agnostic** - works for any field
✅ **Resume capability** - never lose progress
✅ **Quality enforced** - 3000+ char answers
✅ **Multiple formats** - OpenAI, Alpaca, ShareGPT
✅ **Train/val/test splits** - proper ML workflow
✅ **Multiple frameworks** - Unsloth, Axolotl, Transformers
✅ **GGUF export** - ready for llama.cpp
✅ **Production-ready** - error handling, logging, checkpoints

---

## 🎉 You Now Have:

1. ✅ **Automated dataset factory** - Generate 1000s of Q&A pairs
2. ✅ **Multi-format exporter** - Compatible with any training framework
3. ✅ **Training script generator** - Auto-configured for your data
4. ✅ **Domain flexibility** - Crypto, medicine, law, programming, finance
5. ✅ **Complete pipeline** - Topic → Dataset → Training → Model
6. ✅ **Production quality** - Resume, error handling, logging

**This is a complete AI training platform!** 🚀

---

## 📞 Quick Reference

### **Generate Dataset**
```bash
python run_multi_agent.py "Your Topic"
```

### **Extract Training Data**
```bash
python multi_agent_system/extract_training_data.py openai --split
```

### **Prepare Training**
```bash
python multi_agent_system/train_model.py training_data/train_openai_*.jsonl
```

### **Train Model**
```bash
python trained_models/train_unsloth_*.py
```

### **Deploy Model**
```bash
./llama-server.exe -m trained_models/final_model_gguf/model-q4_k_m.gguf --n-gpu-layers 33 -c 4096
```

---

**System ready for production use!**

Generate datasets, train models, deploy, and iterate to create custom AI experts for any domain.
