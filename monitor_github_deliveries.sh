#!/bin/bash
# GitHub Delivery Monitor for Claude Code

echo "🔍 GitHub Delivery Monitor Active"
echo "Watching for: Gemini/Droid/Zai deliverables"
echo "Location: inbox/droid/ and outbox/zai/"
echo ""

while true; do
    # Pull latest from GitHub
    git pull origin main 2>/dev/null
    
    # Check for new files in inbox/droid
    NEW_DROID_FILES=$(ls inbox/droid/*.json 2>/dev/null | wc -l)
    
    # Check for new files in outbox/zai
    NEW_ZAI_FILES=$(ls outbox/zai/*.json 2>/dev/null | wc -l)
    
    if [ $NEW_DROID_FILES -gt 0 ]; then
        echo "📦 Detected $NEW_DROID_FILES new files from Gemini/Droid"
        echo "🔄 Running integration..."
        python integrate_droid_inbox_batch.py
        echo "✅ Integration complete!"
    fi
    
    if [ $NEW_ZAI_FILES -gt 0 ]; then
        echo "📊 Detected $NEW_ZAI_FILES new files from Zai"
        echo "📈 Processing reports..."
    fi
    
    # Wait 2 minutes before next check
    sleep 120
done
