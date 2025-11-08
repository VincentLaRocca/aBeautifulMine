"""
Simple Token Monitor for Claude Desktop Sessions
Tracks approximate usage based on conversation context
Now includes weekly usage tracking
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Set encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration
TOKEN_BUDGET = 200000  # Claude Desktop typical session budget
WEEKLY_BUDGET = 1000000  # Claude Pro weekly budget (approximate)
WARNING_THRESHOLD = 0.85  # 85%
CRITICAL_THRESHOLD = 0.95  # 95%

# Storage for weekly usage tracking
USAGE_FILE = Path.home() / '.claude_usage_tracker.json'

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

def load_usage_data():
    """Load weekly usage data from file"""
    if not USAGE_FILE.exists():
        return {'sessions': [], 'week_start': datetime.now().isoformat()}

    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'sessions': [], 'week_start': datetime.now().isoformat()}

def save_usage_data(data):
    """Save weekly usage data to file"""
    try:
        with open(USAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save usage data: {e}")

def get_week_start(dt):
    """Get the start of the week (Monday) for a given datetime"""
    return (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

def update_weekly_usage(tokens_used):
    """Update weekly usage tracking"""
    data = load_usage_data()
    now = datetime.now()
    current_week_start = get_week_start(now)

    # Parse the stored week_start
    stored_week_start = datetime.fromisoformat(data['week_start'])

    # Check if we've crossed into a new week
    if get_week_start(stored_week_start) < current_week_start:
        # New week - reset
        data = {
            'sessions': [],
            'week_start': current_week_start.isoformat()
        }

    # Add current session
    data['sessions'].append({
        'timestamp': now.isoformat(),
        'tokens': tokens_used
    })

    save_usage_data(data)
    return data

def get_weekly_stats(data):
    """Calculate weekly usage statistics"""
    total_tokens = sum(session['tokens'] for session in data['sessions'])
    session_count = len(data['sessions'])
    week_start = datetime.fromisoformat(data['week_start'])
    week_end = week_start + timedelta(days=7)
    days_left = (week_end - datetime.now()).days

    return {
        'total_tokens': total_tokens,
        'session_count': session_count,
        'percentage': total_tokens / WEEKLY_BUDGET,
        'remaining': WEEKLY_BUDGET - total_tokens,
        'week_start': week_start,
        'week_end': week_end,
        'days_left': max(0, days_left)
    }

def display_status(current_usage):
    """Display current token status"""
    percentage = current_usage / TOKEN_BUDGET
    remaining = TOKEN_BUDGET - current_usage
    status = get_status(percentage)
    color = get_color_status(percentage)

    # Update weekly usage
    usage_data = update_weekly_usage(current_usage)
    weekly = get_weekly_stats(usage_data)

    print(f"\n{'='*60}")
    print(f"{'TOKEN USAGE MONITOR':^60}")
    print(f"{'='*60}")
    print(f"Status: {color} {status}")
    print(f"{'='*60}")

    # Session stats
    print(f"\n📊 CURRENT SESSION:")
    print(f"Current Usage:     {current_usage:>10,} tokens")
    print(f"Budget:            {TOKEN_BUDGET:>10,} tokens")
    print(f"Remaining:         {remaining:>10,} tokens")
    print(f"Percentage Used:   {percentage*100:>10.1f}%")

    # Weekly stats
    weekly_color = get_color_status(weekly['percentage'])
    print(f"\n📅 WEEKLY USAGE:")
    print(f"Week: {weekly['week_start'].strftime('%b %d')} - {weekly['week_end'].strftime('%b %d, %Y')}")
    print(f"Status:            {weekly_color} {get_status(weekly['percentage'])}")
    print(f"Total Used:        {weekly['total_tokens']:>10,} tokens")
    print(f"Weekly Budget:     {WEEKLY_BUDGET:>10,} tokens")
    print(f"Remaining:         {weekly['remaining']:>10,} tokens")
    print(f"Percentage Used:   {weekly['percentage']*100:>10.1f}%")
    print(f"Sessions Count:    {weekly['session_count']:>10}")
    print(f"Days Left:         {weekly['days_left']:>10}")

    if weekly['session_count'] > 1:
        avg_per_session = weekly['total_tokens'] / weekly['session_count']
        print(f"Avg Per Session:   {avg_per_session:>10,.0f} tokens")
        sessions_left = int(weekly['remaining'] / avg_per_session) if avg_per_session > 0 else 0
        print(f"Est. Sessions Left:{sessions_left:>10}")

    print(f"\n{'='*60}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Recommendations based on both session and weekly usage
    session_critical = percentage >= CRITICAL_THRESHOLD
    weekly_critical = weekly['percentage'] >= CRITICAL_THRESHOLD
    session_warning = percentage >= WARNING_THRESHOLD
    weekly_warning = weekly['percentage'] >= WARNING_THRESHOLD

    if session_critical or weekly_critical:
        print("⚠️  IMMEDIATE ACTION REQUIRED:")
        if session_critical:
            print("   SESSION CRITICAL:")
            print("   1. Complete current task QUICKLY")
            print("   2. Run: git add . && git commit")
            print("   3. Create handoff notes")
            print("   4. Exit and start fresh session")
            print(f"   5. You have ~{remaining:,} tokens left in session!\n")
        if weekly_critical:
            print("   WEEKLY LIMIT CRITICAL:")
            print(f"   - Only {weekly['remaining']:,} tokens left this week!")
            print(f"   - {weekly['days_left']} days until reset")
            print("   - Consider reducing usage or waiting for reset\n")
    elif session_warning or weekly_warning:
        print("⚡ RECOMMENDED ACTIONS:")
        if session_warning:
            print("   SESSION WARNING:")
            print("   1. Look for natural stopping point")
            print("   2. Prepare to wrap up work")
            print("   3. Start session handoff document")
            print(f"   4. You have ~{remaining:,} tokens remaining\n")
        if weekly_warning:
            print("   WEEKLY LIMIT WARNING:")
            print(f"   - {weekly['remaining']:,} tokens left this week")
            print(f"   - {weekly['days_left']} days until reset")
            print("   - Plan usage carefully\n")
    else:
        tokens_until_warning = int(TOKEN_BUDGET * WARNING_THRESHOLD) - current_usage
        print(f"✅ Session healthy. ~{tokens_until_warning:,} tokens until session warning threshold.")

        weekly_tokens_until_warning = int(WEEKLY_BUDGET * WARNING_THRESHOLD) - weekly['total_tokens']
        if weekly_tokens_until_warning > 0:
            print(f"✅ Weekly usage healthy. ~{weekly_tokens_until_warning:,} tokens until weekly warning threshold.\n")
        else:
            print(f"⚡ Weekly usage in warning zone. {weekly['remaining']:,} tokens remaining this week.\n")

    return {
        'current': current_usage,
        'budget': TOKEN_BUDGET,
        'remaining': remaining,
        'percentage': percentage,
        'status': status,
        'weekly': weekly
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
