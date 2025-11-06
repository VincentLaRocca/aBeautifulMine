"""
View Stored Agent Details
==========================

Quick script to view details of stored agents.
"""

from agent_storage import AgentStorage, load_agent


def view_agent_details(agent_name: str):
    """View detailed information about a stored agent"""
    agent = load_agent(agent_name)

    if not agent:
        print(f"Agent '{agent_name}' not found")
        return

    print("\n" + "="*80)
    print(f"AGENT: {agent.name}")
    print("="*80)
    print()

    # Basic info
    print(f"Role: {agent.role}")
    print(f"Status: {agent.status}")
    print(f"Version: {agent.version}")
    print(f"Overall Grade: {agent.get_overall_grade()}")
    print()

    # Capabilities
    print("CAPABILITIES:")
    print("-" * 80)

    for cap in agent.capabilities:
        print(f"\n{cap.capability_type.upper()}")
        print(f"  Grade: {cap.get_grade()}")

        if cap.throughput:
            print(f"  Throughput: {cap.throughput}")
        if cap.accuracy:
            print(f"  Accuracy: {cap.accuracy*100:.1f}%")
        if cap.error_rate is not None:
            print(f"  Error Rate: {cap.error_rate*100:.1f}%")
        if cap.quality_score:
            print(f"  Quality Score: {cap.quality_score*100:.1f}%")
        if cap.max_concurrent:
            print(f"  Max Concurrent: {cap.max_concurrent}")

        # Custom metrics
        if cap.custom_metrics:
            print(f"  Custom Metrics:")
            for key, value in cap.custom_metrics.items():
                if isinstance(value, float) and 0 < value < 1:
                    print(f"    - {key}: {value*100:.1f}%")
                else:
                    print(f"    - {key}: {value}")

    # Metadata
    if agent.metadata:
        print("\n" + "-" * 80)
        print("METADATA:")
        for key, value in agent.metadata.items():
            print(f"  {key}: {value}")

    print("\n" + "="*80)


def view_all_agents():
    """View summary of all stored agents"""
    storage = AgentStorage()
    agents = storage.list_agents()

    print("\n" + "="*80)
    print("ALL STORED AGENTS")
    print("="*80)
    print()

    if not agents:
        print("No agents stored yet.")
        return

    print(f"Total Agents: {len(agents)}\n")

    for agent_name in agents:
        agent = load_agent(agent_name)
        if agent:
            print(f"{agent.name}")
            print(f"  Role: {agent.role}")
            print(f"  Grade: {agent.get_overall_grade()}")
            print(f"  Capabilities: {len(agent.capabilities)}")
            print(f"  Status: {agent.status}")
            print()

    print("="*80)


def compare_stored_agents(agent1_name: str, agent2_name: str):
    """Compare two stored agents"""
    agent1 = load_agent(agent1_name)
    agent2 = load_agent(agent2_name)

    if not agent1 or not agent2:
        print("One or both agents not found")
        return

    comparison = agent1.compare_with(agent2)

    print("\n" + "="*80)
    print(f"COMPARISON: {agent1.name} vs {agent2.name}")
    print("="*80)
    print()

    print(f"Overall Grades:")
    print(f"  {agent1.name}: {comparison['overall_grades'][0]}")
    print(f"  {agent2.name}: {comparison['overall_grades'][1]}")
    print()

    if comparison['capabilities']:
        print("Common Capabilities:")
        print("-" * 80)
        for cap_type, data in comparison['capabilities'].items():
            print(f"\n{cap_type.upper()}:")
            print(f"  {agent1.name}: {data[agent1.name]}")
            print(f"  {agent2.name}: {data[agent2.name]}")

            throughput = data.get('throughput_comparison', {})
            if throughput:
                print(f"  Throughput:")
                print(f"    {agent1.name}: {throughput.get(agent1.name, 'N/A')}")
                print(f"    {agent2.name}: {throughput.get(agent2.name, 'N/A')}")
    else:
        print("No common capabilities found")

    print("\n" + "="*80)


if __name__ == "__main__":
    # View all agents
    view_all_agents()

    # View Droid in detail
    print("\n")
    view_agent_details("Droid")
