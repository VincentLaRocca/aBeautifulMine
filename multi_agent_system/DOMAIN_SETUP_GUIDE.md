# Domain Setup Guide - Training on New Subjects

## Overview

The multi-agent system is now **domain-agnostic**! You can train on any subject by configuring domain-specific settings.

## Quick Start: Using a New Domain

### Option 1: Use a Preset Domain

```python
from multi_agent_system import MultiAgentOrchestrator
from multi_agent_system.domain_config import get_domain_config

# Get domain configuration
domain_config = get_domain_config("medicine")  # or "law", "programming", "finance", etc.

# Create config with domain settings
config = {
    "domain": "medicine",
    "domain_config": domain_config
}

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator(config=config)

# Run pipeline
results = orchestrator.run_full_pipeline("Cardiovascular Diseases")
```

### Option 2: Create Custom Domain

```python
from multi_agent_system.domain_config import create_custom_domain, get_domain_config

# Create custom domain
ml_domain = create_custom_domain(
    name="Machine Learning",
    research_specialization="machine learning and artificial intelligence",
    research_sources="peer-reviewed papers, established ML frameworks, recognized ML researchers",
    example_context="ML model examples and training scenarios",
    example_types="machine learning examples",
    practical_context="ML development scenarios",
    audience="ML engineers and data scientists",
    domain_characteristics="model training, hyperparameter tuning, data preprocessing"
)

# Use it
config = {
    "domain": "machine_learning",
    "domain_config": ml_domain
}

orchestrator = MultiAgentOrchestrator(config=config)
results = orchestrator.run_full_pipeline("Neural Networks")
```

## Available Preset Domains

1. **cryptocurrency** - Crypto & Trading (default)
2. **medicine** - Medicine & Healthcare
3. **law** - Law & Legal
4. **programming** - Programming & Software Development
5. **finance** - Finance & Investment
6. **general** - General Knowledge

## What Gets Customized

When you change domains, the system automatically updates:

1. **Research Agent Prompts**
   - Research specialization
   - Authoritative sources
   - Example context

2. **Answer Generator Prompts**
   - Domain-specific examples
   - Audience tone
   - Domain characteristics

3. **Question Generator** (can be customized)
   - Domain-specific question types
   - Domain terminology

## Step-by-Step: Training on a New Subject

### Example: Training on "Medicine"

```python
from multi_agent_system import MultiAgentOrchestrator
from multi_agent_system.domain_config import get_domain_config

# 1. Get medicine domain config
domain_config = get_domain_config("medicine")

# 2. Create config
config = {
    "domain": "medicine",
    "domain_config": domain_config,
    "model_url": "http://localhost:8080/v1",
    "questions_per_topic": 100,
    "output_dir": "medicine_training_output",
    "db_path": "medicine_chromadb"
}

# 3. Initialize
orchestrator = MultiAgentOrchestrator(config=config)

# 4. Run pipeline
results = orchestrator.run_full_pipeline("Cardiovascular Medicine")
```

### Example: Training on "Law"

```python
domain_config = get_domain_config("law")

config = {
    "domain": "law",
    "domain_config": domain_config,
    "output_dir": "law_training_output",
    "db_path": "law_chromadb"
}

orchestrator = MultiAgentOrchestrator(config=config)
results = orchestrator.run_full_pipeline("Contract Law")
```

## Customizing Research Agent

You can also customize just the research agent:

```python
from multi_agent_system import ResearchAgent
from multi_agent_system.domain_config import get_domain_config

# Get domain config
domain_config = get_domain_config("programming")

# Create research agent with domain config
research_agent = ResearchAgent(
    model_url="http://localhost:8080/v1",
    domain_config=domain_config
)

# Use it
result = research_agent.research_question("What is React and how does it work?")
```

## Creating Your Own Domain

### Step 1: Define Domain Characteristics

```python
from multi_agent_system.domain_config import create_custom_domain

my_domain = create_custom_domain(
    name="Your Subject Name",
    research_specialization="what researchers specialize in",
    research_sources="types of authoritative sources",
    example_context="context for examples",
    example_types="types of examples",
    practical_context="practical application context",
    audience="target audience",
    domain_characteristics="key characteristics"
)
```

### Step 2: Use It

```python
config = {
    "domain": "your_subject",
    "domain_config": my_domain
}

orchestrator = MultiAgentOrchestrator(config=config)
results = orchestrator.run_full_pipeline("Your Topic")
```

## Domain Configuration Structure

Each domain config has:

```python
{
    "name": "Domain Name",
    "research_specialization": "What the researcher specializes in",
    "research_sources": "Types of authoritative sources",
    "example_context": "Context for examples",
    "example_types": "Types of examples to use",
    "practical_context": "Context for practical applications",
    "audience": "Target audience",
    "domain_characteristics": "Key characteristics"
}
```

## Command Line Usage

You can also specify domain via command line (if we add support):

```bash
# Using preset
python run_multi_agent.py "Medicine Topic" --domain medicine

# Using custom domain config file
python run_multi_agent.py "Your Topic" --domain-config custom_domain.json
```

## Examples

### Medicine Example

```python
domain_config = get_domain_config("medicine")
config = {"domain_config": domain_config}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Cardiovascular Diseases")
```

**Research Agent will:**
- Specialize in "medical science and healthcare"
- Use "peer-reviewed medical journals" as sources
- Provide "medical case studies" as examples
- Target "medical professionals" as audience

### Programming Example

```python
domain_config = get_domain_config("programming")
config = {"domain_config": domain_config}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Python Web Development")
```

**Research Agent will:**
- Specialize in "software engineering and computer science"
- Use "technical documentation" as sources
- Provide "code examples" as examples
- Target "software engineers" as audience

## Adding New Presets

To add a new preset domain, edit `domain_config.py`:

```python
DOMAIN_PRESETS["your_domain"] = {
    "name": "Your Domain Name",
    "research_specialization": "...",
    # ... rest of config
}
```

## Summary

✅ **System is now domain-agnostic**
✅ **Easy to switch domains** - just change config
✅ **Preset domains available** - medicine, law, programming, etc.
✅ **Custom domains supported** - create your own
✅ **Research agent customizable** - domain-specific prompts
✅ **Answer generator customizable** - domain-specific examples

**You can now train on ANY subject!** 🎉

