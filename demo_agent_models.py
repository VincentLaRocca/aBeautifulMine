"""
Demo: Agent Modeling System
============================

This script demonstrates how to use the agent modeling system to:
1. View agent capabilities and performance
2. Compare agents
3. Benchmark agents
4. Grade agents on specific tasks
5. Export metrics for analysis

Run: python demo_agent_models.py
"""

from agent_instances import (
    droid, claude, gemini, zai,
    all_agents, all_processes, all_products,
    benchmark_all_agents,
    export_all_metrics,
    print_agent_comparison
)
from agent_models import Agent, AgentCapability


def demo_basic_usage():
    """Demonstrate basic agent usage"""
    print("\n" + "="*80)
    print("DEMO 1: Basic Agent Usage")
    print("="*80 + "\n")

    # View Droid's capabilities
    print("Droid's Performance Summary:")
    summary = droid.get_performance_summary()
    print(f"  Name: {summary['name']}")
    print(f"  Role: {summary['role']}")
    print(f"  Overall Grade: {summary['overall_grade']}")
    print(f"  Status: {summary['status']}")
    print(f"\n  Capabilities:")
    for cap in summary['capabilities']:
        print(f"    - {cap['capability']}: Grade {cap['grade']}")
        if cap['throughput']:
            print(f"      Throughput: {cap['throughput']}/min")
        if cap['accuracy']:
            print(f"      Accuracy: {cap['accuracy']*100:.1f}%")


def demo_capability_grading():
    """Demonstrate capability-specific grading"""
    print("\n" + "="*80)
    print("DEMO 2: Capability-Specific Grading")
    print("="*80 + "\n")

    # Check query capabilities across agents
    print("Query Capability Comparison:")
    for agent in all_agents:
        query_cap = agent.get_capability("query")
        if query_cap:
            grade = agent.get_capability_grade("query")
            print(f"  {agent.name}: {grade} (throughput: {query_cap.throughput}/min)")
        else:
            print(f"  {agent.name}: No query capability")

    # Check integration capabilities
    print("\nIntegration Capability Comparison:")
    for agent in all_agents:
        integrate_cap = agent.get_capability("integrate")
        if integrate_cap:
            grade = agent.get_capability_grade("integrate")
            print(f"  {agent.name}: {grade} (throughput: {integrate_cap.throughput}/min)")
        else:
            print(f"  {agent.name}: No integration capability")


def demo_agent_comparison():
    """Demonstrate agent-to-agent comparison"""
    print("\n" + "="*80)
    print("DEMO 3: Agent Comparison")
    print("="*80 + "\n")

    # Compare Droid and Claude
    print("Comparing Droid vs Claude:")
    comparison = droid.compare_with(claude)
    print(f"  Agents: {comparison['agents']}")
    print(f"  Overall Grades: {comparison['overall_grades']}")
    print(f"\n  Common Capabilities:")
    for cap_type, data in comparison['capabilities'].items():
        print(f"    {cap_type}:")
        print(f"      Droid: {data['Droid']}")
        print(f"      Claude: {data['Claude']}")
        print(f"      Throughput: Droid={data['throughput_comparison']['Droid']}, "
              f"Claude={data['throughput_comparison']['Claude']}")


def demo_benchmarking():
    """Demonstrate agent benchmarking"""
    print("\n" + "="*80)
    print("DEMO 4: Agent Benchmarking")
    print("="*80 + "\n")

    results = benchmark_all_agents()

    print(f"Total Agents: {results['total_agents']}")
    print(f"\nOverall Rankings:")
    for i, (name, grade) in enumerate(results['rankings']['overall'], 1):
        print(f"  {i}. {name}: {grade}")

    print(f"\nRankings by Capability:")
    for cap_type, rankings in results['rankings']['by_capability'].items():
        print(f"\n  {cap_type.upper()}:")
        for i, (name, grade) in enumerate(rankings, 1):
            print(f"    {i}. {name}: {grade}")


def demo_process_metrics():
    """Demonstrate process performance metrics"""
    print("\n" + "="*80)
    print("DEMO 5: Process Performance Metrics")
    print("="*80 + "\n")

    for process in all_processes:
        summary = process.get_performance_summary()
        print(f"\n{process.name}:")
        print(f"  Grade: {summary['grade']}")
        print(f"  Duration: {summary['avg_duration_minutes']} minutes")
        print(f"  Success Rate: {summary['success_rate']*100:.1f}%")
        print(f"  Throughput: {summary['throughput']} items")
        print(f"  Agents: {', '.join(summary['agents_involved'])}")


def demo_product_metrics():
    """Demonstrate product quality metrics"""
    print("\n" + "="*80)
    print("DEMO 6: Product Quality Metrics")
    print("="*80 + "\n")

    for product in all_products:
        summary = product.get_performance_summary()
        print(f"\n{product.name}:")
        print(f"  Type: {summary['type']}")
        print(f"  Grade: {summary['grade']}")
        print(f"  Size: {summary['size']}")
        if summary['quality_score']:
            print(f"  Quality Score: {summary['quality_score']*100:.1f}%")
        if summary['completeness']:
            print(f"  Completeness: {summary['completeness']*100:.1f}%")
        if summary['accuracy']:
            print(f"  Accuracy: {summary['accuracy']*100:.1f}%")
        print(f"  Created By: {summary['created_by']}")


def demo_custom_agent():
    """Demonstrate creating a custom agent"""
    print("\n" + "="*80)
    print("DEMO 7: Creating a Custom Agent")
    print("="*80 + "\n")

    # Create a new agent with custom capabilities
    custom_agent = Agent(
        name="TestBot",
        role="Testing Specialist",
        status="active",
        version="1.0.0",
        metadata={
            "purpose": "Automated testing and validation"
        }
    )

    # Add capabilities
    custom_agent.add_capability(AgentCapability(
        capability_type="validate",
        throughput=100,  # 100 tests per minute
        accuracy=0.99,  # 99% accuracy
        error_rate=0.01,  # 1% false positives
        quality_score=0.98,
        custom_metrics={
            "test_types": ["unit", "integration", "e2e"],
            "coverage": 0.95
        }
    ))

    custom_agent.add_capability(AgentCapability(
        capability_type="code",
        throughput=300,  # 300 lines per hour
        accuracy=0.92,
        error_rate=0.08,
        quality_score=0.90,
        custom_metrics={
            "languages": ["Python", "JavaScript"]
        }
    ))

    print("Custom Agent Created:")
    summary = custom_agent.get_performance_summary()
    print(f"  Name: {summary['name']}")
    print(f"  Role: {summary['role']}")
    print(f"  Overall Grade: {summary['overall_grade']}")
    print(f"  Capabilities:")
    for cap in summary['capabilities']:
        print(f"    - {cap['capability']}: Grade {cap['grade']}")


def demo_metrics_export():
    """Demonstrate metrics export"""
    print("\n" + "="*80)
    print("DEMO 8: Metrics Export")
    print("="*80 + "\n")

    filepath = "demo_agent_metrics_export.json"
    data = export_all_metrics(filepath)

    print(f"Exported metrics to: {filepath}")
    print(f"  Total Agents: {len(data['agents'])}")
    print(f"  Total Processes: {len(data['processes'])}")
    print(f"  Total Products: {len(data['products'])}")
    print(f"  Benchmark Data: {len(data['benchmark']['rankings']['by_capability'])} capability types")


def demo_detailed_capability_analysis():
    """Demonstrate detailed capability analysis"""
    print("\n" + "="*80)
    print("DEMO 9: Detailed Capability Analysis")
    print("="*80 + "\n")

    print("Droid's Query Capability Deep Dive:")
    query_cap = droid.get_capability("query")
    if query_cap:
        print(f"  Throughput: {query_cap.throughput} queries/min")
        print(f"  Accuracy: {query_cap.accuracy*100:.1f}%")
        print(f"  Error Rate: {query_cap.error_rate*100:.1f}%")
        print(f"  Max Concurrent: {query_cap.max_concurrent}")
        print(f"  Quality Score: {query_cap.quality_score*100:.1f}%")
        print(f"  Grade: {query_cap.get_grade()}")
        print(f"\n  Custom Metrics:")
        for key, value in query_cap.custom_metrics.items():
            print(f"    {key}: {value}")

    print("\n\nClaude's Integration Capability Deep Dive:")
    integrate_cap = claude.get_capability("integrate")
    if integrate_cap:
        print(f"  Throughput: {integrate_cap.throughput} pairs/min")
        print(f"  Accuracy: {integrate_cap.accuracy*100:.1f}%")
        print(f"  Error Rate: {integrate_cap.error_rate*100:.1f}%")
        print(f"  Latency: {integrate_cap.latency_ms}ms per pair")
        print(f"  Quality Score: {integrate_cap.quality_score*100:.1f}%")
        print(f"  Grade: {integrate_cap.get_grade()}")
        print(f"\n  Custom Metrics:")
        for key, value in integrate_cap.custom_metrics.items():
            print(f"    {key}: {value}")


def run_all_demos():
    """Run all demonstration functions"""
    print("\n" + "="*80)
    print("AGENT MODELING SYSTEM - COMPLETE DEMONSTRATION")
    print("="*80)

    demo_basic_usage()
    demo_capability_grading()
    demo_agent_comparison()
    demo_benchmarking()
    demo_process_metrics()
    demo_product_metrics()
    demo_custom_agent()
    demo_detailed_capability_analysis()
    demo_metrics_export()

    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80 + "\n")

    print("\nKey Takeaways:")
    print("  1. Agents have measurable capabilities with grades (A-F)")
    print("  2. Each capability has metrics: throughput, accuracy, error rate, quality")
    print("  3. Agents can be compared and benchmarked")
    print("  4. Processes and Products also have performance metrics")
    print("  5. Custom agents can be created with specific capabilities")
    print("  6. All metrics can be exported for analysis")
    print("\nExample Use Cases:")
    print("  - Identify which agent is best for a specific task")
    print("  - Track performance improvements over time")
    print("  - Make data-driven decisions about agent allocation")
    print("  - Discover bottlenecks in processes")
    print("  - Validate product quality against targets")


if __name__ == "__main__":
    run_all_demos()
