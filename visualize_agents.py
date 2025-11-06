"""
Agent Performance Visualization
================================

Creates visual comparisons and charts of agent performance metrics.
Useful for presentations, reports, and decision-making.
"""

from agent_instances import droid, claude, gemini, zai, all_agents
from agent_instances import all_processes, all_products


def print_capability_matrix():
    """Print a capability matrix showing which agents have which capabilities"""
    print("\n" + "="*100)
    print("AGENT CAPABILITY MATRIX")
    print("="*100)
    print()

    # Collect all capability types
    all_capabilities = set()
    for agent in all_agents:
        for cap in agent.capabilities:
            all_capabilities.add(cap.capability_type)

    # Sort alphabetically
    sorted_caps = sorted(all_capabilities)

    # Header
    print(f"{'Capability':<20} | {'Droid':<12} | {'Claude':<12} | {'Gemini':<12} | {'Zai':<12}")
    print("-" * 100)

    # Rows
    for cap_type in sorted_caps:
        row = f"{cap_type.capitalize():<20} |"
        for agent in [droid, claude, gemini, zai]:
            grade = agent.get_capability_grade(cap_type)
            if grade != "N/A":
                cap = agent.get_capability(cap_type)
                throughput = f"{cap.throughput}" if cap.throughput else "N/A"
                row += f" {grade:>2} ({throughput:<6}) |"
            else:
                row += f" {'--':<11} |"
        print(row)

    print("\nLegend: Grade (Throughput)")
    print("Throughput units vary by capability: queries/min, parses/min, lines/hour, etc.")


def print_performance_dashboard():
    """Print a performance dashboard with key metrics"""
    print("\n" + "="*100)
    print("AGENT PERFORMANCE DASHBOARD")
    print("="*100)
    print()

    for agent in all_agents:
        print(f"\n{'='*50}")
        print(f"{agent.name.upper()} - {agent.role}")
        print(f"{'='*50}")
        print(f"Overall Grade: {agent.get_overall_grade()}")
        print(f"Status: {agent.status}")
        print(f"Version: {agent.version}")
        print()

        if agent.capabilities:
            print("Capabilities:")
            for cap in agent.capabilities:
                summary = cap.get_performance_summary()
                print(f"\n  {cap.capability_type.upper()}: Grade {summary['grade']}")

                metrics = []
                if cap.throughput:
                    metrics.append(f"Throughput: {cap.throughput}")
                if cap.accuracy:
                    metrics.append(f"Accuracy: {cap.accuracy*100:.1f}%")
                if cap.error_rate is not None:
                    metrics.append(f"Error: {cap.error_rate*100:.1f}%")
                if cap.quality_score:
                    metrics.append(f"Quality: {cap.quality_score*100:.1f}%")

                if metrics:
                    print(f"    {' | '.join(metrics)}")

                if cap.custom_metrics:
                    print(f"    Custom: {list(cap.custom_metrics.keys())[:3]}")
        else:
            print("No capabilities defined")


def print_side_by_side_comparison():
    """Print side-by-side comparison of agents"""
    print("\n" + "="*100)
    print("SIDE-BY-SIDE AGENT COMPARISON")
    print("="*100)
    print()

    # Collect all unique capabilities
    all_caps = set()
    for agent in all_agents:
        for cap in agent.capabilities:
            all_caps.add(cap.capability_type)

    # Print header
    print(f"{'Metric':<25} | {'Droid':<15} | {'Claude':<15} | {'Gemini':<15} | {'Zai':<15}")
    print("-" * 100)

    # Overall grade
    row = f"{'Overall Grade':<25} |"
    for agent in [droid, claude, gemini, zai]:
        row += f" {agent.get_overall_grade():<14} |"
    print(row)

    # Status
    row = f"{'Status':<25} |"
    for agent in [droid, claude, gemini, zai]:
        row += f" {agent.status:<14} |"
    print(row)

    # Capabilities count
    row = f"{'Total Capabilities':<25} |"
    for agent in [droid, claude, gemini, zai]:
        row += f" {len(agent.capabilities):<14} |"
    print(row)

    print()
    print("Capability Grades:")
    print("-" * 100)

    # Each capability
    for cap_type in sorted(all_caps):
        row = f"  {cap_type.capitalize():<23} |"
        for agent in [droid, claude, gemini, zai]:
            grade = agent.get_capability_grade(cap_type)
            row += f" {grade:<14} |"
        print(row)


def print_process_summary():
    """Print process performance summary"""
    print("\n" + "="*100)
    print("PROCESS PERFORMANCE SUMMARY")
    print("="*100)
    print()

    print(f"{'Process':<30} | {'Grade':<6} | {'Duration':<12} | {'Success':<8} | {'Throughput':<12} | Agents")
    print("-" * 100)

    for process in all_processes:
        summary = process.get_performance_summary()
        duration = f"{summary['avg_duration_minutes']} min" if summary['avg_duration_minutes'] else "N/A"
        success = f"{summary['success_rate']*100:.0f}%" if summary['success_rate'] else "N/A"
        throughput = f"{summary['throughput']}" if summary['throughput'] else "N/A"
        agents = ", ".join(summary['agents_involved']) if summary['agents_involved'] else "N/A"

        print(f"{process.name:<30} | {summary['grade']:<6} | {duration:<12} | {success:<8} | {throughput:<12} | {agents}")


def print_product_summary():
    """Print product quality summary"""
    print("\n" + "="*100)
    print("PRODUCT QUALITY SUMMARY")
    print("="*100)
    print()

    print(f"{'Product':<35} | {'Grade':<6} | {'Complete':<10} | {'Quality':<10} | {'Accuracy':<10} | Creator")
    print("-" * 100)

    for product in all_products:
        summary = product.get_performance_summary()
        complete = f"{summary['completeness']*100:.0f}%" if summary['completeness'] else "N/A"
        quality = f"{summary['quality_score']*100:.0f}%" if summary['quality_score'] else "N/A"
        accuracy = f"{summary['accuracy']*100:.0f}%" if summary['accuracy'] else "N/A"
        creator = summary['created_by'] if summary['created_by'] else "N/A"

        print(f"{product.name:<35} | {summary['grade']:<6} | {complete:<10} | {quality:<10} | {accuracy:<10} | {creator}")


def print_top_performers():
    """Print top performing agents by capability"""
    print("\n" + "="*100)
    print("TOP PERFORMERS BY CAPABILITY")
    print("="*100)
    print()

    from agent_instances import benchmark_all_agents

    results = benchmark_all_agents()

    for cap_type, rankings in results["rankings"]["by_capability"].items():
        print(f"\n{cap_type.upper()}:")
        for i, (name, grade) in enumerate(rankings[:3], 1):  # Top 3
            # Get actual throughput
            agent = next((a for a in all_agents if a.name == name), None)
            if agent:
                cap = agent.get_capability(cap_type)
                if cap and cap.throughput:
                    print(f"  {i}. {name}: {grade} ({cap.throughput} throughput)")
                else:
                    print(f"  {i}. {name}: {grade}")


def print_recommendations():
    """Print agent recommendations for common tasks"""
    print("\n" + "="*100)
    print("AGENT RECOMMENDATIONS FOR COMMON TASKS")
    print("="*100)
    print()

    recommendations = [
        ("Generate search queries", "query", "Research and data discovery"),
        ("Parse API responses", "parse", "Data extraction and transformation"),
        ("Write code", "code", "Implementation and scripting"),
        ("Generate Q&A pairs", "generate", "Content creation"),
        ("Integrate datasets", "integrate", "Database operations"),
        ("Orchestrate workflows", "orchestrate", "Multi-agent coordination"),
        ("Validate quality", "validate", "Quality assurance"),
        ("Analyze data", "analyze", "Data analysis and reporting")
    ]

    for task, capability, context in recommendations:
        print(f"\n{task.upper()}")
        print(f"  Context: {context}")
        print(f"  Recommended agents:")

        # Find agents with this capability
        agents_with_cap = []
        for agent in all_agents:
            cap = agent.get_capability(capability)
            if cap:
                grade = agent.get_capability_grade(capability)
                agents_with_cap.append((agent.name, grade, cap.throughput or 0))

        # Sort by grade then throughput
        grade_values = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        agents_with_cap.sort(key=lambda x: (grade_values.get(x[1], 0), x[2]), reverse=True)

        if agents_with_cap:
            for i, (name, grade, throughput) in enumerate(agents_with_cap[:3], 1):
                throughput_str = f" ({throughput} throughput)" if throughput else ""
                print(f"    {i}. {name}: {grade}{throughput_str}")
        else:
            print(f"    No agents available for this capability")


def print_all_visualizations():
    """Print all visualizations"""
    print_capability_matrix()
    print_performance_dashboard()
    print_side_by_side_comparison()
    print_process_summary()
    print_product_summary()
    print_top_performers()
    print_recommendations()

    print("\n" + "="*100)
    print("VISUALIZATION COMPLETE")
    print("="*100)


if __name__ == "__main__":
    print_all_visualizations()
