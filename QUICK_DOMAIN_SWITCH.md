# Quick Domain Switch Guide

## 🎯 Training on a Brand New Subject

Your multi-agent system is now **domain-agnostic**! Here's how to train on any subject:

## Quick Examples

### Medicine
```python
from multi_agent_system import MultiAgentOrchestrator
from multi_agent_system.domain_config import get_domain_config

domain_config = get_domain_config("medicine")
config = {"domain_config": domain_config, "output_dir": "medicine_output"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Cardiovascular Diseases")
```

### Law
```python
domain_config = get_domain_config("law")
config = {"domain_config": domain_config, "output_dir": "law_output"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Contract Law")
```

### Programming
```python
domain_config = get_domain_config("programming")
config = {"domain_config": domain_config, "output_dir": "programming_output"}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Python Web Development")
```

### Custom Domain
```python
from multi_agent_system.domain_config import create_custom_domain

my_domain = create_custom_domain(
    name="Your Subject",
    research_specialization="what researchers specialize in",
    research_sources="authoritative sources",
    example_context="example context",
    example_types="example types",
    practical_context="practical context",
    audience="target audience",
    domain_characteristics="key characteristics"
)

config = {"domain_config": my_domain}
orchestrator = MultiAgentOrchestrator(config=config)
orchestrator.run_full_pipeline("Your Topic")
```

## Available Presets

- `cryptocurrency` - Crypto & Trading (default)
- `medicine` - Medicine & Healthcare
- `law` - Law & Legal
- `programming` - Programming & Software Development
- `finance` - Finance & Investment
- `general` - General Knowledge

## What Changes?

When you switch domains:
- ✅ **Research Agent** - Uses domain-specific prompts
- ✅ **Answer Generator** - Uses domain-specific examples
- ✅ **All prompts** - Automatically adapted to domain

## Just Changing Research Agent?

```python
from multi_agent_system import ResearchAgent
from multi_agent_system.domain_config import get_domain_config

domain_config = get_domain_config("medicine")
research_agent = ResearchAgent(domain_config=domain_config)
result = research_agent.research_question("What is hypertension?")
```

## Full Documentation

See `multi_agent_system/DOMAIN_SETUP_GUIDE.md` for complete details!

