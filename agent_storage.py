"""
Agent Object Storage System
============================

Store and retrieve agent objects with their capabilities and metrics.
Supports JSON serialization for persistence.

Usage:
    from agent_storage import AgentStorage, store_agent, load_agent

    # Store an agent
    storage = AgentStorage("agents_db.json")
    storage.save_agent(droid)

    # Load an agent
    loaded_droid = storage.load_agent("Droid")

    # List all agents
    all_agents = storage.list_agents()
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from agent_models import Agent, AgentCapability, Process, Product


class AgentStorage:
    """
    Handles persistence of Agent objects to/from JSON storage.
    """

    def __init__(self, storage_path: str = "agents_storage.json"):
        """
        Initialize agent storage.

        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not self.storage_path.exists():
            self._write_storage({"agents": {}, "processes": {}, "products": {}, "metadata": {}})

    def _read_storage(self) -> Dict:
        """Read storage file"""
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def _write_storage(self, data: Dict):
        """Write to storage file"""
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _serialize_agent(self, agent: Agent) -> Dict:
        """Convert Agent object to JSON-serializable dict"""
        return {
            "name": agent.name,
            "role": agent.role,
            "status": agent.status,
            "version": agent.version,
            "created_date": agent.created_date.isoformat(),
            "metadata": agent.metadata,
            "capabilities": [
                {
                    "capability_type": cap.capability_type,
                    "throughput": cap.throughput,
                    "accuracy": cap.accuracy,
                    "error_rate": cap.error_rate,
                    "latency_ms": cap.latency_ms,
                    "max_concurrent": cap.max_concurrent,
                    "quality_score": cap.quality_score,
                    "cost_per_operation": cap.cost_per_operation,
                    "custom_metrics": cap.custom_metrics
                }
                for cap in agent.capabilities
            ]
        }

    def _deserialize_agent(self, data: Dict) -> Agent:
        """Convert dict back to Agent object"""
        agent = Agent(
            name=data["name"],
            role=data["role"],
            status=data["status"],
            version=data["version"],
            created_date=datetime.fromisoformat(data["created_date"]),
            metadata=data["metadata"]
        )

        for cap_data in data["capabilities"]:
            capability = AgentCapability(
                capability_type=cap_data["capability_type"],
                throughput=cap_data["throughput"],
                accuracy=cap_data["accuracy"],
                error_rate=cap_data["error_rate"],
                latency_ms=cap_data["latency_ms"],
                max_concurrent=cap_data["max_concurrent"],
                quality_score=cap_data["quality_score"],
                cost_per_operation=cap_data["cost_per_operation"],
                custom_metrics=cap_data["custom_metrics"]
            )
            agent.add_capability(capability)

        return agent

    def save_agent(self, agent: Agent) -> bool:
        """
        Save an agent to storage.

        Args:
            agent: Agent object to save

        Returns:
            True if successful
        """
        try:
            data = self._read_storage()
            data["agents"][agent.name] = self._serialize_agent(agent)
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            self._write_storage(data)
            print(f"[SUCCESS] Agent '{agent.name}' saved successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Error saving agent '{agent.name}': {e}")
            return False

    def load_agent(self, agent_name: str) -> Optional[Agent]:
        """
        Load an agent from storage.

        Args:
            agent_name: Name of the agent to load

        Returns:
            Agent object if found, None otherwise
        """
        try:
            data = self._read_storage()
            if agent_name in data["agents"]:
                agent = self._deserialize_agent(data["agents"][agent_name])
                print(f"[SUCCESS] Agent '{agent_name}' loaded successfully")
                return agent
            else:
                print(f"[ERROR] Agent '{agent_name}' not found in storage")
                return None
        except Exception as e:
            print(f"[ERROR] Error loading agent '{agent_name}': {e}")
            return None

    def delete_agent(self, agent_name: str) -> bool:
        """
        Delete an agent from storage.

        Args:
            agent_name: Name of the agent to delete

        Returns:
            True if successful
        """
        try:
            data = self._read_storage()
            if agent_name in data["agents"]:
                del data["agents"][agent_name]
                data["metadata"]["last_updated"] = datetime.now().isoformat()
                self._write_storage(data)
                print(f"[SUCCESS] Agent '{agent_name}' deleted successfully")
                return True
            else:
                print(f"[ERROR] Agent '{agent_name}' not found in storage")
                return False
        except Exception as e:
            print(f"[ERROR] Error deleting agent '{agent_name}': {e}")
            return False

    def list_agents(self) -> List[str]:
        """
        List all agent names in storage.

        Returns:
            List of agent names
        """
        data = self._read_storage()
        return list(data["agents"].keys())

    def load_all_agents(self) -> List[Agent]:
        """
        Load all agents from storage.

        Returns:
            List of Agent objects
        """
        agents = []
        for agent_name in self.list_agents():
            agent = self.load_agent(agent_name)
            if agent:
                agents.append(agent)
        return agents

    def save_all_agents(self, agents: List[Agent]) -> bool:
        """
        Save multiple agents to storage.

        Args:
            agents: List of Agent objects to save

        Returns:
            True if all successful
        """
        success = True
        for agent in agents:
            if not self.save_agent(agent):
                success = False
        return success

    def get_agent_summary(self, agent_name: str) -> Optional[Dict]:
        """
        Get a summary of an agent's capabilities without loading full object.

        Args:
            agent_name: Name of the agent

        Returns:
            Summary dict or None
        """
        data = self._read_storage()
        if agent_name in data["agents"]:
            agent_data = data["agents"][agent_name]
            return {
                "name": agent_data["name"],
                "role": agent_data["role"],
                "status": agent_data["status"],
                "capabilities": [cap["capability_type"] for cap in agent_data["capabilities"]],
                "capability_count": len(agent_data["capabilities"])
            }
        return None

    def export_to_json(self, filepath: str):
        """Export entire storage to a different JSON file"""
        import shutil
        shutil.copy(self.storage_path, filepath)
        print(f"[SUCCESS] Storage exported to {filepath}")

    def import_from_json(self, filepath: str):
        """Import agents from another JSON file"""
        import shutil
        shutil.copy(filepath, self.storage_path)
        print(f"[SUCCESS] Storage imported from {filepath}")


# Quick-access functions
def store_agent(agent: Agent, storage_path: str = "agents_storage.json"):
    """Quick function to store an agent"""
    storage = AgentStorage(storage_path)
    return storage.save_agent(agent)


def load_agent(agent_name: str, storage_path: str = "agents_storage.json") -> Optional[Agent]:
    """Quick function to load an agent"""
    storage = AgentStorage(storage_path)
    return storage.load_agent(agent_name)


def list_stored_agents(storage_path: str = "agents_storage.json") -> List[str]:
    """Quick function to list all stored agents"""
    storage = AgentStorage(storage_path)
    return storage.list_agents()


# Create agent based on your specifications
def create_droid_agent() -> Agent:
    """
    Create Droid agent with your specified metrics:
    - reading: 30 WPM
    - writing clear: 10
    - writing concise: 10
    - parsing: 30 pairs per hour
    - queries: 100 Q&A pairs per hour
    - codes: logic
    """
    droid = Agent(
        name="Droid",
        role="Data Generation Specialist",
        status="active",
        version="2.0.0",
        metadata={
            "specialization": "Ultra deep research and Q&A generation",
            "output_format": "JSON Q&A pairs"
        }
    )

    # Reading capability - 30 words per minute
    droid.add_capability(AgentCapability(
        capability_type="reading",
        throughput=30,  # 30 words per minute
        accuracy=0.95,
        quality_score=0.94,
        custom_metrics={
            "unit": "words per minute",
            "comprehension_rate": 0.95
        }
    ))

    # Writing capability - clear: 10, concise: 10
    droid.add_capability(AgentCapability(
        capability_type="writing",
        throughput=10,  # 10 units per hour (adjustable based on what unit means)
        accuracy=0.92,
        quality_score=0.93,
        custom_metrics={
            "clarity_score": 10,
            "conciseness_score": 10,
            "unit": "content pieces per hour",
            "style": "clear and concise"
        }
    ))

    # Parsing capability - 30 pairs per hour
    droid.add_capability(AgentCapability(
        capability_type="parsing",
        throughput=30,  # 30 pairs per hour
        accuracy=0.95,
        error_rate=0.05,
        quality_score=0.92,
        custom_metrics={
            "unit": "pairs per hour",
            "average_pair_length": 3000,
            "formula_inclusion": 0.60,
            "example_inclusion": 0.60
        }
    ))

    # Query capability - 100 Q&A pairs per hour
    droid.add_capability(AgentCapability(
        capability_type="queries",
        throughput=100,  # 100 Q&A pairs per hour
        accuracy=0.95,
        error_rate=0.05,
        quality_score=0.96,
        max_concurrent=100,
        custom_metrics={
            "unit": "Q&A pairs per hour",
            "queries_per_indicator": 100,
            "success_rate": 0.88,
            "concurrent_execution": True
        }
    ))

    # Code capability - logic
    droid.add_capability(AgentCapability(
        capability_type="code",
        throughput=500,  # 500 lines per hour (estimated)
        accuracy=0.90,
        error_rate=0.10,
        quality_score=0.89,
        custom_metrics={
            "unit": "lines per hour",
            "specialty": "logic",
            "languages": ["Python"],
            "complexity_handling": "high"
        }
    ))

    return droid


if __name__ == "__main__":
    # Demo: Create and store Droid agent
    print("="*80)
    print("AGENT STORAGE SYSTEM DEMO")
    print("="*80)
    print()

    # Create Droid with your specifications
    print("Creating Droid agent with specifications:")
    print("  - reading: 30 WPM")
    print("  - writing: clear 10, concise 10")
    print("  - parsing: 30 pairs per hour")
    print("  - queries: 100 Q&A pairs per hour")
    print("  - code: logic")
    print()

    droid = create_droid_agent()

    # Store it
    storage = AgentStorage("agents_storage.json")
    storage.save_agent(droid)
    print()

    # List all agents
    print("All stored agents:")
    for name in storage.list_agents():
        summary = storage.get_agent_summary(name)
        print(f"  - {name}: {summary['role']}")
        print(f"    Capabilities: {', '.join(summary['capabilities'])}")
    print()

    # Load it back
    print("Loading Droid from storage...")
    loaded_droid = storage.load_agent("Droid")
    print()

    # Show performance
    if loaded_droid:
        print("Droid Performance Summary:")
        summary = loaded_droid.get_performance_summary()
        print(f"  Name: {summary['name']}")
        print(f"  Role: {summary['role']}")
        print(f"  Overall Grade: {summary['overall_grade']}")
        print(f"  Status: {summary['status']}")
        print()
        print("  Capabilities:")
        for cap in summary['capabilities']:
            print(f"    - {cap['capability']}: Grade {cap['grade']}")
            if cap['throughput']:
                print(f"      Throughput: {cap['throughput']}")
            if 'custom_metrics' in cap and cap['custom_metrics']:
                custom = cap['custom_metrics']
                if 'unit' in custom:
                    print(f"      Unit: {custom['unit']}")
                if 'clarity_score' in custom:
                    print(f"      Clarity: {custom['clarity_score']}/10")
                if 'conciseness_score' in custom:
                    print(f"      Conciseness: {custom['conciseness_score']}/10")

    print()
    print("="*80)
    print("STORAGE DEMO COMPLETE")
    print("="*80)
    print()
    print("Agent stored in: agents_storage.json")
    print("Use load_agent('Droid') to retrieve it anytime")
