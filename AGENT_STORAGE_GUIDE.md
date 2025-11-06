# Agent Storage System - Quick Guide

## Overview

Your agents are now stored as **persistent objects** in `agents_storage.json`. You can save, load, modify, and retrieve them anytime.

## Current Stored Agents

### Droid - Data Generation Specialist
**Overall Grade: A**

| Capability | Throughput | Grade | Details |
|------------|------------|-------|---------|
| **reading** | 30 WPM | A | 95% comprehension rate |
| **writing** | 10/hour | A | Clarity: 10/10, Conciseness: 10/10 |
| **parsing** | 30 pairs/hour | A | 3,000 char avg, 60% formula/example inclusion |
| **queries** | 100 Q&A pairs/hour | A | 100 concurrent, 88% success rate |
| **code** | 500 lines/hour | A | Specialty: logic, Python |

## Quick Usage

### Load an Agent
```python
from agent_storage import load_agent

# Load Droid
droid = load_agent("Droid")

# Check performance
print(droid.get_overall_grade())  # "A"
print(droid.get_capability_grade("queries"))  # "A"
```

### View Agent Capabilities
```python
from agent_storage import load_agent

droid = load_agent("Droid")

# Get summary
summary = droid.get_performance_summary()
print(f"Name: {summary['name']}")
print(f"Grade: {summary['overall_grade']}")

# List capabilities
for cap in summary['capabilities']:
    print(f"{cap['capability']}: {cap['grade']} ({cap['throughput']})")
```

### Create a New Agent
```python
from agent_models import Agent, AgentCapability
from agent_storage import store_agent

# Create agent
claude = Agent(
    name="Claude",
    role="Integration Specialist",
    status="active"
)

# Add capabilities
claude.add_capability(AgentCapability(
    capability_type="integrate",
    throughput=100,  # 100 pairs per minute
    accuracy=1.0,    # 100% accuracy
    error_rate=0.0,  # 0% errors
    custom_metrics={
        "unit": "pairs per minute",
        "batch_size": 1500
    }
))

# Store it
store_agent(claude)
```

### List All Agents
```python
from agent_storage import list_stored_agents

# List all agent names
agents = list_stored_agents()
print(agents)  # ['Droid', 'Claude', ...]
```

### Load All Agents
```python
from agent_storage import AgentStorage

storage = AgentStorage()
all_agents = storage.load_all_agents()

for agent in all_agents:
    print(f"{agent.name}: {agent.get_overall_grade()}")
```

### Update an Agent
```python
from agent_storage import load_agent, store_agent
from agent_models import AgentCapability

# Load agent
droid = load_agent("Droid")

# Add new capability
droid.add_capability(AgentCapability(
    capability_type="validate",
    throughput=50,
    accuracy=0.95
))

# Save updated agent
store_agent(droid)
```

### Delete an Agent
```python
from agent_storage import AgentStorage

storage = AgentStorage()
storage.delete_agent("AgentName")
```

## Storage Format

Agents are stored in `agents_storage.json` with this structure:

```json
{
  "agents": {
    "Droid": {
      "name": "Droid",
      "role": "Data Generation Specialist",
      "status": "active",
      "version": "2.0.0",
      "capabilities": [
        {
          "capability_type": "reading",
          "throughput": 30,
          "accuracy": 0.95,
          "custom_metrics": {
            "unit": "words per minute"
          }
        }
      ]
    }
  },
  "metadata": {
    "last_updated": "2025-11-05T23:44:49"
  }
}
```

## Key Features

✅ **Persistent Storage**: Agents saved as JSON objects
✅ **Easy Load/Save**: One-line load and store functions
✅ **Full Object Support**: All capabilities and metrics preserved
✅ **Custom Metrics**: Store any additional data you need
✅ **Version Control**: Track agent versions over time
✅ **Bulk Operations**: Load/save multiple agents at once

## Storage Location

- **Default file**: `agents_storage.json`
- **Custom file**: Pass `storage_path` parameter to functions

```python
from agent_storage import load_agent

# Load from custom file
droid = load_agent("Droid", storage_path="my_agents.json")
```

## Export/Import

```python
from agent_storage import AgentStorage

storage = AgentStorage()

# Export to backup
storage.export_to_json("backup_agents.json")

# Import from backup
storage.import_from_json("backup_agents.json")
```

## Command Line Quick Check

```bash
# View stored agents
python -c "from agent_storage import AgentStorage; s = AgentStorage(); print('\n'.join(s.list_agents()))"

# Load and check Droid
python -c "from agent_storage import load_agent; d = load_agent('Droid'); print(d.get_overall_grade())"
```

## Integration with Existing System

This storage system is **fully compatible** with:
- `agent_models.py` - Core classes
- `agent_instances.py` - Pre-defined agents
- `demo_agent_models.py` - Demos
- `visualize_agents.py` - Visualizations

You can store any agent created with the system and load it back with full functionality.

## Example Workflow

```python
# 1. Load agent from storage
from agent_storage import load_agent

droid = load_agent("Droid")

# 2. Use agent for task allocation
if droid.get_capability_grade("queries") == "A":
    print("Droid is optimal for query generation tasks")

# 3. Check specific metrics
query_cap = droid.get_capability("queries")
print(f"Throughput: {query_cap.throughput} Q&A pairs per hour")
print(f"Success rate: {query_cap.custom_metrics['success_rate']*100}%")

# 4. Compare with other agents
from agent_instances import claude

comparison = droid.compare_with(claude)
print(comparison)
```

## Next Steps

1. Load Droid and explore its capabilities
2. Create agents for Claude, Gemini, and Zai with their specs
3. Store all agents in the system
4. Use storage for persistent agent management
5. Export regularly for backups

## Support

- **Core system**: `agent_models.py`
- **Storage system**: `agent_storage.py`
- **Full docs**: `AGENT_MODELING_SYSTEM.md`
- **Quick ref**: `QUICK_REFERENCE.md`
