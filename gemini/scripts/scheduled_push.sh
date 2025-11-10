#!/bin/bash
# Scheduled Auto-Push - Runs periodically
# Usage: ./scheduled_push.sh [interval_minutes]
# Default: Checks every 30 minutes

INTERVAL=${1:-30}  # Default 30 minutes
INTERVAL_SECONDS=$((INTERVAL * 60))

echo "⏰ Scheduled Auto-Push to GitHub"
echo "================================================"
echo "Check interval: Every $INTERVAL minutes"
echo "Press Ctrl+C to stop"
echo "================================================"
echo ""

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking for changes..."

    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo ""
        echo "🔔 Changes detected! Initiating auto-push..."
        echo ""
        ./auto_push_to_github.sh
        echo ""
    else
        echo "   No changes to commit"
    fi

    echo "   Next check in $INTERVAL minutes..."
    echo ""
    sleep $INTERVAL_SECONDS
done
