"""
Simple Token Monitor for Claude Desktop Sessions
Tracks approximate usage based on conversation context
"""

import sys
import os
from datetime import datetime

# Configuration
TOKEN_BUDGET = 200000  # Claude Desktop typical budget
WARNING_THRESHOLD = 0.85  # 85%
CRITICAL_THRESHOLD = 0.95  # 95%

def estimate_tokens_from_input():
    """
    Estimate token usage from user input
    This is a simplified approximation until we have API access
    """
    if len(sys.argv) > 1:
        current_usage = int(sys.argv[1])
    else:
        # Prompt for current usage
        print("Enter current token usage (from Claude interface):")
        current_usage = int(input().strip())

    return current_usage

def get_status(percentage):
    """Determine session status based on percentage"""
    if percentage >= CRITICAL_THRESHOLD:
        return 'CRITICAL - WRAP NOW'
    elif percentage >= WARNING_THRESHOLD:
        return 'WARNING - START WRAPPING'
    else:
        return 'HEALTHY'

def get_color_status(percentage):
    """Get colored status indicator"""
    if percentage >= CRITICAL_THRESHOLD:
        return '🔴'
    elif percentage >= WARNING_THRESHOLD:
        return '🟡'
    else:
        return '🟢'

def display_status(current_usage):
    """Display current token status"""
    percentage = current_usage / TOKEN_BUDGET
    remaining = TOKEN_BUDGET - current_usage
    status = get_status(percentage)
    color = get_color_status(percentage)

    print(f"\n{'='*60}")
    print(f"{'TOKEN USAGE MONITOR':^60}")
    print(f"{'='*60}")
    print(f"Status: {color} {status}")
    print(f"{'='*60}")
    print(f"Current Usage:     {current_usage:>10,} tokens")
    print(f"Budget:            {TOKEN_BUDGET:>10,} tokens")
    print(f"Remaining:         {remaining:>10,} tokens")
    print(f"Percentage Used:   {percentage*100:>10.1f}%")
    print(f"{'='*60}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Recommendations
    if percentage >= CRITICAL_THRESHOLD:
        print("⚠️  IMMEDIATE ACTION REQUIRED:")
        print("   1. Complete current task QUICKLY")
        print("   2. Run: git add . && git commit")
        print("   3. Create handoff notes")
        print("   4. Exit and start fresh session")
        print(f"   5. You have ~{remaining} tokens left!\n")
    elif percentage >= WARNING_THRESHOLD:
        print("⚡ RECOMMENDED ACTIONS:")
        print("   1. Look for natural stopping point")
        print("   2. Prepare to wrap up work")
        print("   3. Start session handoff document")
        print(f"   4. You have ~{remaining} tokens remaining\n")
    else:
        tokens_until_warning = int(TOKEN_BUDGET * WARNING_THRESHOLD) - current_usage
        print(f"✅ Session healthy. ~{tokens_until_warning:,} tokens until warning threshold.\n")

    return {
        'current': current_usage,
        'budget': TOKEN_BUDGET,
        'remaining': remaining,
        'percentage': percentage,
        'status': status
    }

def main():
    """Main execution"""
    try:
        current_usage = estimate_tokens_from_input()
        stats = display_status(current_usage)

        # Return exit code based on status
        if stats['percentage'] >= CRITICAL_THRESHOLD:
            sys.exit(2)  # Critical
        elif stats['percentage'] >= WARNING_THRESHOLD:
            sys.exit(1)  # Warning
        else:
            sys.exit(0)  # Healthy

    except ValueError:
        print("Error: Please provide a valid number for token usage")
        sys.exit(3)
    except KeyboardInterrupt:
        print("\n\nMonitoring cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()
