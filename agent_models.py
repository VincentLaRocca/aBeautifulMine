"""
Agent, Process, and Product Object Models
==========================================

Models agents, processes, and products as objects with measurable capabilities,
performance metrics, and grading systems.

Usage:
    from agent_models import Agent, Process, Product, AgentCapability

    # Create an agent with capabilities
    droid = Agent(
        name="Droid",
        role="Data Generation Specialist",
        capabilities=[
            AgentCapability("query", queries_per_minute=10, max_concurrent=100),
            AgentCapability("parse", parses_per_minute=50, accuracy=0.95),
            AgentCapability("code", lines_per_hour=500, bug_rate=0.02)
        ]
    )

    # Grade the agent
    print(droid.get_capability_grade("query"))  # Returns letter grade
    print(droid.get_overall_performance())      # Returns performance summary
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class CapabilityType(Enum):
    """Types of capabilities an agent can have"""
    QUERY = "query"
    PARSE = "parse"
    CODE = "code"
    ANALYZE = "analyze"
    INTEGRATE = "integrate"
    GENERATE = "generate"
    VALIDATE = "validate"
    ORCHESTRATE = "orchestrate"


@dataclass
class AgentCapability:
    """
    Represents a specific capability of an agent with measurable performance metrics.

    Attributes:
        capability_type: Type of capability (query, parse, code, etc.)
        throughput: Primary performance metric (e.g., queries per minute)
        accuracy: Accuracy rate (0.0 to 1.0)
        error_rate: Error rate (0.0 to 1.0)
        latency_ms: Average latency in milliseconds
        max_concurrent: Maximum concurrent operations
        quality_score: Quality assessment (0.0 to 1.0)
        cost_per_operation: Cost per operation (if applicable)
        custom_metrics: Additional custom metrics
    """
    capability_type: str
    throughput: Optional[float] = None  # operations per minute
    accuracy: Optional[float] = None  # 0.0 to 1.0
    error_rate: Optional[float] = None  # 0.0 to 1.0
    latency_ms: Optional[float] = None  # milliseconds
    max_concurrent: Optional[int] = None
    quality_score: Optional[float] = None  # 0.0 to 1.0
    cost_per_operation: Optional[float] = None
    custom_metrics: Dict[str, Any] = field(default_factory=dict)

    def get_grade(self) -> str:
        """
        Calculate letter grade based on performance metrics.

        Grading criteria:
        - A: 90-100% (excellent performance)
        - B: 80-89% (good performance)
        - C: 70-79% (acceptable performance)
        - D: 60-69% (needs improvement)
        - F: <60% (unacceptable performance)
        """
        scores = []

        # Accuracy score (if available)
        if self.accuracy is not None:
            scores.append(self.accuracy * 100)

        # Error rate score (inverted - lower is better)
        if self.error_rate is not None:
            scores.append((1 - self.error_rate) * 100)

        # Quality score
        if self.quality_score is not None:
            scores.append(self.quality_score * 100)

        # Throughput score (relative to benchmarks)
        if self.throughput is not None:
            # Normalize throughput to 0-100 scale based on capability type
            throughput_benchmarks = {
                "query": 10,  # 10 queries/min is 100%
                "parse": 50,  # 50 parses/min is 100%
                "code": 500,  # 500 lines/hour is 100%
            }
            benchmark = throughput_benchmarks.get(self.capability_type, 10)
            normalized = min((self.throughput / benchmark) * 100, 100)
            scores.append(normalized)

        if not scores:
            return "N/A"

        avg_score = sum(scores) / len(scores)

        if avg_score >= 90:
            return "A"
        elif avg_score >= 80:
            return "B"
        elif avg_score >= 70:
            return "C"
        elif avg_score >= 60:
            return "D"
        else:
            return "F"

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of all performance metrics"""
        return {
            "capability": self.capability_type,
            "grade": self.get_grade(),
            "throughput": self.throughput,
            "accuracy": self.accuracy,
            "error_rate": self.error_rate,
            "latency_ms": self.latency_ms,
            "max_concurrent": self.max_concurrent,
            "quality_score": self.quality_score,
            "cost_per_operation": self.cost_per_operation,
            "custom_metrics": self.custom_metrics
        }


@dataclass
class Agent:
    """
    Represents an AI agent with capabilities, metrics, and performance tracking.

    Attributes:
        name: Agent name (e.g., "Droid", "Claude", "Gemini")
        role: Agent's primary role
        capabilities: List of agent capabilities with metrics
        status: Current status (active, idle, busy, offline)
        version: Agent version
        created_date: When the agent was created
        metadata: Additional metadata
    """
    name: str
    role: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    status: str = "active"
    version: str = "1.0.0"
    created_date: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_capability(self, capability: AgentCapability):
        """Add a capability to the agent"""
        self.capabilities.append(capability)

    def get_capability(self, capability_type: str) -> Optional[AgentCapability]:
        """Get a specific capability by type"""
        for cap in self.capabilities:
            if cap.capability_type == capability_type:
                return cap
        return None

    def get_capability_grade(self, capability_type: str) -> str:
        """Get the grade for a specific capability"""
        cap = self.get_capability(capability_type)
        return cap.get_grade() if cap else "N/A"

    def get_overall_grade(self) -> str:
        """Calculate overall agent performance grade"""
        if not self.capabilities:
            return "N/A"

        grades = [cap.get_grade() for cap in self.capabilities]
        grade_values = {"A": 95, "B": 85, "C": 75, "D": 65, "F": 50, "N/A": 0}

        valid_grades = [g for g in grades if g != "N/A"]
        if not valid_grades:
            return "N/A"

        avg_value = sum(grade_values[g] for g in valid_grades) / len(valid_grades)

        if avg_value >= 90:
            return "A"
        elif avg_value >= 80:
            return "B"
        elif avg_value >= 70:
            return "C"
        elif avg_value >= 60:
            return "D"
        else:
            return "F"

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get complete performance summary for the agent"""
        return {
            "name": self.name,
            "role": self.role,
            "overall_grade": self.get_overall_grade(),
            "status": self.status,
            "version": self.version,
            "capabilities": [cap.get_performance_summary() for cap in self.capabilities],
            "metadata": self.metadata
        }

    def compare_with(self, other: 'Agent') -> Dict[str, Any]:
        """Compare this agent with another agent"""
        comparison = {
            "agents": [self.name, other.name],
            "overall_grades": [self.get_overall_grade(), other.get_overall_grade()],
            "capabilities": {}
        }

        # Compare common capabilities
        for cap in self.capabilities:
            other_cap = other.get_capability(cap.capability_type)
            if other_cap:
                comparison["capabilities"][cap.capability_type] = {
                    self.name: cap.get_grade(),
                    other.name: other_cap.get_grade(),
                    "throughput_comparison": {
                        self.name: cap.throughput,
                        other.name: other_cap.throughput
                    }
                }

        return comparison


@dataclass
class Process:
    """
    Represents a process/workflow with performance metrics.

    Attributes:
        name: Process name
        description: Process description
        inputs: List of required inputs
        outputs: List of expected outputs
        steps: List of process steps
        agents_involved: List of agent names involved
        avg_duration_minutes: Average execution time
        success_rate: Success rate (0.0 to 1.0)
        throughput: Items processed per execution
        cost_per_run: Cost per execution
        metadata: Additional metadata
    """
    name: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    agents_involved: List[str] = field(default_factory=list)
    avg_duration_minutes: Optional[float] = None
    success_rate: Optional[float] = None
    throughput: Optional[int] = None  # items per run
    cost_per_run: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_grade(self) -> str:
        """Calculate process performance grade"""
        scores = []

        if self.success_rate is not None:
            scores.append(self.success_rate * 100)

        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score >= 90:
                return "A"
            elif avg_score >= 80:
                return "B"
            elif avg_score >= 70:
                return "C"
            elif avg_score >= 60:
                return "D"
            else:
                return "F"
        return "N/A"

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get process performance summary"""
        return {
            "name": self.name,
            "grade": self.get_grade(),
            "avg_duration_minutes": self.avg_duration_minutes,
            "success_rate": self.success_rate,
            "throughput": self.throughput,
            "cost_per_run": self.cost_per_run,
            "agents_involved": self.agents_involved,
            "steps_count": len(self.steps)
        }


@dataclass
class Product:
    """
    Represents a product/deliverable with quality metrics.

    Attributes:
        name: Product name
        type: Product type (dataset, report, model, etc.)
        size: Size of the product (records, MB, etc.)
        quality_score: Quality score (0.0 to 1.0)
        completeness: Completeness percentage (0.0 to 1.0)
        accuracy: Accuracy score (0.0 to 1.0)
        created_by: Agent that created this product
        created_date: When the product was created
        metadata: Additional metadata
    """
    name: str
    type: str
    size: Optional[Any] = None
    quality_score: Optional[float] = None
    completeness: Optional[float] = None
    accuracy: Optional[float] = None
    created_by: Optional[str] = None
    created_date: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_grade(self) -> str:
        """Calculate product quality grade"""
        scores = []

        if self.quality_score is not None:
            scores.append(self.quality_score * 100)

        if self.completeness is not None:
            scores.append(self.completeness * 100)

        if self.accuracy is not None:
            scores.append(self.accuracy * 100)

        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score >= 90:
                return "A"
            elif avg_score >= 80:
                return "B"
            elif avg_score >= 70:
                return "C"
            elif avg_score >= 60:
                return "D"
            else:
                return "F"
        return "N/A"

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get product quality summary"""
        return {
            "name": self.name,
            "type": self.type,
            "grade": self.get_grade(),
            "size": self.size,
            "quality_score": self.quality_score,
            "completeness": self.completeness,
            "accuracy": self.accuracy,
            "created_by": self.created_by,
            "metadata": self.metadata
        }


# Utility functions for benchmarking and comparison
def benchmark_agents(agents: List[Agent]) -> Dict[str, Any]:
    """
    Benchmark multiple agents and return comparison data.

    Args:
        agents: List of Agent objects to benchmark

    Returns:
        Dictionary with benchmark results and rankings
    """
    results = {
        "total_agents": len(agents),
        "agents": [],
        "rankings": {
            "overall": [],
            "by_capability": {}
        }
    }

    # Collect agent summaries
    for agent in agents:
        results["agents"].append(agent.get_performance_summary())

    # Rank by overall grade
    grade_values = {"A": 95, "B": 85, "C": 75, "D": 65, "F": 50, "N/A": 0}
    ranked = sorted(agents, key=lambda a: grade_values.get(a.get_overall_grade(), 0), reverse=True)
    results["rankings"]["overall"] = [(a.name, a.get_overall_grade()) for a in ranked]

    # Rank by individual capabilities
    capability_types = set()
    for agent in agents:
        for cap in agent.capabilities:
            capability_types.add(cap.capability_type)

    for cap_type in capability_types:
        cap_agents = [(a.name, a.get_capability_grade(cap_type)) for a in agents if a.get_capability(cap_type)]
        cap_ranked = sorted(cap_agents, key=lambda x: grade_values.get(x[1], 0), reverse=True)
        results["rankings"]["by_capability"][cap_type] = cap_ranked

    return results


def export_agent_metrics(agents: List[Agent], filepath: str):
    """Export agent metrics to JSON file"""
    import json

    data = {
        "export_date": datetime.now().isoformat(),
        "agents": [agent.get_performance_summary() for agent in agents],
        "benchmark": benchmark_agents(agents)
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Agent metrics exported to {filepath}")
