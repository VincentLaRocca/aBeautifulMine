# Agent Modeling System - Quick Reference

## Quick Start

```python
# Import agents
from agent_instances import droid, claude, gemini, zai

# View agent grade
print(droid.get_overall_grade())  # "A"

# View capability grade
print(claude.get_capability_grade("integrate"))  # "A"

# Compare agents
comparison = droid.compare_with(claude)
print(comparison)

# Benchmark all agents
from agent_instances import benchmark_all_agents
results = benchmark_all_agents()
print(results["rankings"]["overall"])
```

## Current Rankings

### Overall Performance
1. Droid: **A** (Data Generation)
2. Claude: **A** (Integration & Orchestration)
3. Gemini: **A** (Refinement & Embeddings)
4. Zai: **A** (Execution)

### By Capability

| Capability | #1 Agent | Grade | Key Metric |
|------------|----------|-------|------------|
| Query | Droid | A | 20 queries/min |
| Parse | Droid | A | 50 parses/min |
| Code | Claude | A | 500 lines/hour |
| Generate | Droid | A | 80 items/min |
| Integrate | Claude | A | 100 pairs/min |
| Orchestrate | Claude | A | 100% success |
| Validate | Gemini | A | 100 items/min |
| Analyze | Claude | A | 30 datasets/hour |

## Agent Quick Stats

### Droid
- **Role**: Data Generation Specialist
- **Best At**: Query, Parse, Generate
- **Throughput**: 440 pairs per 4-hour session
- **Quality**: 3,000+ char answers, 95% accuracy

### Claude
- **Role**: Orchestrator & Integration
- **Best At**: Integrate, Orchestrate, Analyze, Code
- **Throughput**: 1,500 pairs per 17.5-min batch
- **Quality**: 100% success rate, 0% errors

### Gemini
- **Role**: Data Processing & Refinement
- **Best At**: Generate (embeddings), Validate, Parse
- **Throughput**: 500 embeddings per 24-hour batch
- **Quality**: 1,536-dimension vectors, 50% cost savings

### Zai
- **Role**: Execution Specialist
- **Best At**: Code, Generate
- **Throughput**: 600 lines/hour (code)
- **Status**: Setup in progress

## Common Queries

### "Which agent should I use for X?"

```python
from agent_instances import all_agents

# Find best agent for a capability
for agent in all_agents:
    grade = agent.get_capability_grade("query")
    if grade != "N/A":
        print(f"{agent.name}: {grade}")
```

### "How is our production database doing?"

```python
from agent_instances import product_production_database

summary = product_production_database.get_performance_summary()
print(f"Grade: {summary['grade']}")
print(f"Completeness: {summary['completeness']*100:.1f}%")
print(f"Quality: {summary['quality_score']*100:.1f}%")
```

### "What's the performance of our integration process?"

```python
from agent_instances import process_data_integration

summary = process_data_integration.get_performance_summary()
print(f"Grade: {summary['grade']}")
print(f"Success Rate: {summary['success_rate']*100:.1f}%")
print(f"Duration: {summary['avg_duration_minutes']} min")
```

### "Create a new agent"

```python
from agent_models import Agent, AgentCapability

# Create agent
new_agent = Agent(name="MyBot", role="Specialist")

# Add capability
new_agent.add_capability(AgentCapability(
    capability_type="query",
    throughput=10,
    accuracy=0.90,
    error_rate=0.10
))

# Get grade
print(new_agent.get_overall_grade())
```

## Key Metrics Explained

### Throughput
Operations per minute (or per hour for slower operations)
- **Query**: Queries per minute
- **Parse**: Parse operations per minute
- **Code**: Lines per hour
- **Generate**: Items per minute/hour
- **Integrate**: Items per minute

### Accuracy
Percentage of successful operations (0.0 to 1.0)
- 0.95 = 95% successful operations
- Higher is better

### Error Rate
Percentage of failed operations (0.0 to 1.0)
- 0.05 = 5% failures
- Lower is better

### Quality Score
Overall quality assessment (0.0 to 1.0)
- 0.96 = 96% quality
- Based on multiple factors specific to capability

### Latency
Response time in milliseconds
- 900ms = 0.9 seconds
- Lower is better

## Grade Meanings

| Grade | Range | Meaning | Action |
|-------|-------|---------|--------|
| A | 90-100% | Excellent | Keep using |
| B | 80-89% | Good | Minor improvements |
| C | 70-79% | Acceptable | Review for optimization |
| D | 60-69% | Needs improvement | Investigate issues |
| F | <60% | Unacceptable | Fix immediately |

## File Structure

```
agent_models.py          # Core classes (Agent, Capability, Process, Product)
agent_instances.py       # Real agent instances with data
demo_agent_models.py     # Comprehensive demos
AGENT_MODELING_SYSTEM.md # Full documentation
QUICK_REFERENCE.md       # This file
```

## Demo Commands

```bash
# Run full demo
python demo_agent_models.py

# Run just agent comparison
python -c "from agent_instances import print_agent_comparison; print_agent_comparison()"

# Export metrics
python -c "from agent_instances import export_all_metrics; export_all_metrics()"
```

## Advanced Usage

### Track Custom Metrics

```python
capability = AgentCapability(
    capability_type="query",
    throughput=10,
    accuracy=0.90,
    custom_metrics={
        "my_metric": 123,
        "another_metric": "high",
        "complex_metric": {"nested": "value"}
    }
)
```

### Compare Multiple Agents

```python
from agent_instances import all_agents, benchmark_agents

# Get complete benchmark
results = benchmark_agents(all_agents)

# View rankings by capability
for cap_type, rankings in results["rankings"]["by_capability"].items():
    print(f"\n{cap_type}:")
    for name, grade in rankings:
        print(f"  {name}: {grade}")
```

### Export for Analysis

```python
from agent_instances import export_all_metrics
import json

# Export
data = export_all_metrics("my_metrics.json")

# Load and analyze
with open("my_metrics.json") as f:
    metrics = json.load(f)

# Your analysis here
```

## Troubleshooting

### "Agent has no capability X"
Check if the agent has that capability:
```python
if agent.get_capability("query"):
    print("Has query capability")
else:
    print("No query capability")
```

### "Grade shows N/A"
The agent either has no metrics for that capability, or the capability doesn't exist:
```python
cap = agent.get_capability("query")
if cap:
    print(f"Accuracy: {cap.accuracy}")
    print(f"Throughput: {cap.throughput}")
```

### "Want to see all capabilities"
```python
for cap in agent.capabilities:
    print(f"{cap.capability_type}: {cap.get_grade()}")
```

## Best Practices

1. **Use specific grades** for task allocation (not just overall)
2. **Track changes** over time by exporting metrics regularly
3. **Set benchmarks** for your specific use case
4. **Custom metrics** for domain-specific measurements
5. **Compare fairly** - only compare agents on shared capabilities

## Contact & Support

For issues, questions, or enhancements, refer to:
- Full documentation: `AGENT_MODELING_SYSTEM.md`
- Demo examples: `demo_agent_models.py`
- Core implementation: `agent_models.py`
- Real data: `agent_instances.py`
