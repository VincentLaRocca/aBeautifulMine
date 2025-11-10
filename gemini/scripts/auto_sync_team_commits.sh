#!/bin/bash
# Auto-Sync Team Commits - aBeautifulMine Collaboration
# Monitors commits from: Droid, Claude Desktop, Zai, and integrates

echo "🌳 aBeautifulMine Team Collaboration Monitor"
echo "================================================"
echo "Watching for commits from:"
echo "  - Droid (Eastern Dream Team)"
echo "  - Claude Desktop (Team Orchestrator)"
echo "  - Claude Codenet (Development Specialist)"
echo "  - Zai (Worker Bee)"
echo "  - Claude Code (CEO - that's me!)"
echo ""
echo "Repository: aBeautifulMine"
echo "Branch: main"
echo "================================================"
echo ""

# Store last known commit
LAST_COMMIT=$(git rev-parse HEAD)

while true; do
    echo "[$(date '+%H:%M:%S')] Checking for new commits..."
    
    # Fetch latest from remote
    git fetch origin main --quiet 2>/dev/null
    
    # Get remote HEAD
    REMOTE_COMMIT=$(git rev-parse origin/main)
    
    # Check if there are new commits
    if [ "$LAST_COMMIT" != "$REMOTE_COMMIT" ]; then
        echo ""
        echo "🎉 NEW COMMITS DETECTED!"
        echo "================================================"
        
        # Show who committed
        git log $LAST_COMMIT..origin/main --pretty=format:"📝 %h - %an: %s" --abbrev-commit
        echo ""
        echo "================================================"
        
        # Pull the changes
        echo ""
        echo "🔄 Pulling latest changes..."
        git pull origin main --quiet
        
        if [ $? -eq 0 ]; then
            echo "✅ Pull successful!"
            echo ""
            
            # Check for new files in key locations
            echo "📦 Checking for deliverables..."
            
            # Droid/Gemini deliveries
            DROID_FILES=$(ls inbox/droid/*.json 2>/dev/null | wc -l)
            if [ $DROID_FILES -gt 0 ]; then
                echo "  📊 Found $DROID_FILES files in inbox/droid/"
                echo "  🔄 Running integration..."
                python integrate_droid_inbox_batch.py
                if [ $? -eq 0 ]; then
                    echo "  ✅ Droid/Gemini integration complete!"
                fi
            fi
            
            # Zai deliveries
            ZAI_FILES=$(ls outbox/zai/*.json 2>/dev/null | wc -l)
            if [ $ZAI_FILES -gt 0 ]; then
                echo "  📈 Found $ZAI_FILES reports from Zai"
            fi
            
            # Check database state after integration
            echo ""
            echo "📊 Current Database State:"
            python -c "import sqlite3; conn=sqlite3.connect('crypto_indicators_production.db'); c=conn.cursor(); c.execute('SELECT COUNT(*) FROM qa_pairs'); print(f'  Total pairs: {c.fetchone()[0]:,}'); conn.close()" 2>/dev/null || echo "  (Database query skipped)"
            
            echo ""
            echo "✅ Sync complete! Ready for next commits."
            
        else
            echo "⚠️  Pull had conflicts - manual intervention needed"
        fi
        
        # Update last known commit
        LAST_COMMIT=$(git rev-parse HEAD)
        echo ""
    fi
    
    # Wait 2 minutes before next check
    sleep 120
done
