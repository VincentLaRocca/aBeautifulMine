#!/bin/bash
# Auto-Push to GitHub - aBeautifulMine Project
# Automatically commits and pushes changes to GitHub
# Usage: ./auto_push_to_github.sh "Your commit message"
#        OR run without message for auto-generated message

echo "🚀 GitHub Auto-Push Script"
echo "================================================"
echo "Repository: aBeautifulMine"
echo "Branch: main"
echo "================================================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit"
    echo "✅ Working directory is clean"
    exit 0
fi

# Generate commit message if not provided
if [ -z "$1" ]; then
    # Auto-generate message based on what changed
    CHANGED_FILES=$(git status --short | wc -l)
    DB_CHANGED=$(git status --short | grep -c "\.db$" || true)
    MD_CHANGED=$(git status --short | grep -c "\.md$" || true)
    JSON_CHANGED=$(git status --short | grep -c "\.json$" || true)
    PY_CHANGED=$(git status --short | grep -c "\.py$" || true)

    # Get current pair count from database
    CURRENT_PAIRS=$(python -c "import sqlite3; conn=sqlite3.connect('crypto_indicators_production.db'); c=conn.cursor(); c.execute('SELECT COUNT(*) FROM qa_pairs'); print(c.fetchone()[0]); conn.close()" 2>/dev/null || echo "unknown")

    # Build commit message
    COMMIT_MSG="Update: $CHANGED_FILES files modified"

    if [ $DB_CHANGED -gt 0 ]; then
        COMMIT_MSG="$COMMIT_MSG - Database updated ($CURRENT_PAIRS pairs)"
    fi

    if [ $MD_CHANGED -gt 0 ]; then
        COMMIT_MSG="$COMMIT_MSG - Documentation updated"
    fi

    if [ $JSON_CHANGED -gt 0 ]; then
        COMMIT_MSG="$COMMIT_MSG - Data files updated"
    fi

    if [ $PY_CHANGED -gt 0 ]; then
        COMMIT_MSG="$COMMIT_MSG - Scripts updated"
    fi

    # Add footer
    COMMIT_MSG="$COMMIT_MSG

🤖 Auto-pushed by Claude Code
For the Greater Good of All"

    echo "📝 Auto-generated commit message:"
    echo "   \"$COMMIT_MSG\""
else
    COMMIT_MSG="$1

🤖 Auto-pushed by Claude Code
For the Greater Good of All"
    echo "📝 Using provided commit message:"
    echo "   \"$1\""
fi

echo ""
echo "📊 Changes to be committed:"
git status --short
echo ""

# Stage all changes
echo "📦 Staging changes..."
git add .

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to stage changes"
    exit 1
fi

echo "✅ Changes staged"
echo ""

# Commit changes
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to commit changes"
    exit 1
fi

echo "✅ Changes committed"
echo ""

# Push to GitHub
echo "🚀 Pushing to GitHub (origin/main)..."
git push origin main

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to push to GitHub"
    echo "ℹ️  Try running: git pull origin main --rebase"
    exit 1
fi

echo "✅ Successfully pushed to GitHub!"
echo ""

# Show final status
echo "📊 Final Status:"
git log -1 --pretty=format:"   Latest commit: %h - %s" --abbrev-commit
echo ""
echo ""
echo "================================================"
echo "✅ Auto-push complete!"
echo "================================================"
