# YouTube to Q&A Workflow - Created!

**Date**: 2025-10-31
**Status**: ✅ Complete and Ready to Use

---

## What Was Created

### 🎬 Repeatable YouTube → Q&A Workflow

A fully automated pipeline that:
1. Takes a YouTube URL (e.g., `https://www.youtube.com/watch?v=qAF1NjEVHhY`)
2. Fetches the transcript via Gemini (using YouTube API)
3. Parses transcript into Q&A pairs via Droid
4. Outputs structured JSON suitable for AI consumption

**One command does everything**:
```bash
dreamteam-workflow youtube-to-qa https://www.youtube.com/watch?v=qAF1NjEVHhY
```

---

## Files Created

### 1. Workflow Orchestrator
**Location**: `shared/workflows/youtube-to-qa.sh`
- Automated multi-agent coordination
- Timeout handling (5 min per step)
- Progress monitoring
- Output validation
- Error handling

### 2. Workflow Template
**Location**: `shared/workflows/TEMPLATE_youtube-to-qa.md`
- Complete documentation
- Agent instructions
- Input/Output formats
- Quality guidelines
- Troubleshooting guide

### 3. Workflow CLI
**Location**: `shared/bin/dreamteam-workflow`
- Easy command-line interface
- List available workflows
- Run workflows with simple syntax

### 4. Workflows Guide
**Location**: `WORKFLOWS.md` (project root)
- How workflows work
- Usage examples
- Creating custom workflows
- Best practices
- Troubleshooting

### 5. Agent Quick Reference
**Location**: `AGENT_QUICKREF.md` (project root)
- Quick commands for agents
- Step-by-step instructions
- Common issues and solutions
- Quality guidelines

---

## How to Use It

### Simple Usage

```bash
# Run the workflow
dreamteam-workflow youtube-to-qa https://www.youtube.com/watch?v=qAF1NjEVHhY

# With custom output filename
dreamteam-workflow youtube-to-qa https://www.youtube.com/watch?v=qAF1NjEVHhY --output my_qa.json
```

### What Happens

**Automatic Process**:
1. ✅ Validates YouTube URL
2. ✅ Creates workflow directory
3. ✅ Delegates transcript task to Gemini
4. ⏳ Waits for Gemini (max 5 min)
5. ✅ Delegates parsing task to Droid
6. ⏳ Waits for Droid (max 5 min)
7. ✅ Validates JSON output
8. ✅ Saves final result

**Output**:
- `qa_output.json` (or custom name)
- Structured Q&A pairs ready for AI training

---

## Output Format

```json
{
  "video_id": "qAF1NjEVHhY",
  "video_url": "https://www.youtube.com/watch?v=qAF1NjEVHhY",
  "processed_at": "2025-10-31T12:00:00Z",
  "qa_pairs": [
    {
      "id": "qa_001",
      "question": "What is the main topic discussed in this video?",
      "answer": "The video discusses...",
      "timestamp": "00:01:23",
      "context": "Introduction section",
      "confidence": "high"
    },
    {
      "id": "qa_002",
      "question": "How does the process work?",
      "answer": "The process works by...",
      "timestamp": "00:03:45",
      "context": "Technical explanation",
      "confidence": "high"
    }
  ],
  "metadata": {
    "total_pairs": 15,
    "transcript_length": 5000,
    "processing_notes": "Extracted Q&A from educational content"
  }
}
```

---

## Setup (One-time)

### For Gemini Terminal

```bash
cd /c/Users/vlaro/dreamteam/Gemini
dreamteam-checkin gemini --status idle
dreamteam-poll gemini --watch --interval 5
```

Keep this running - it will alert when transcript tasks arrive.

### For Droid Terminal

```bash
cd /c/Users/vlaro/dreamteam/Droid
dreamteam-checkin droid --status idle
dreamteam-poll droid --watch --interval 5
```

Keep this running - it will alert when parsing tasks arrive.

---

## Full Example

### Terminal 1: Gemini (keep running)
```bash
cd /c/Users/vlaro/dreamteam/Gemini
dreamteam-poll gemini --watch
# Waiting for tasks...
```

### Terminal 2: Droid (keep running)
```bash
cd /c/Users/vlaro/dreamteam/Droid
dreamteam-poll droid --watch
# Waiting for tasks...
```

### Terminal 3: Claude (run workflow)
```bash
cd /c/Users/vlaro/dreamteam/claude
dreamteam-workflow youtube-to-qa https://www.youtube.com/watch?v=qAF1NjEVHhY

# Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎬 YouTube to Q&A Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Workflow ID: yt_qa_1761909287
YouTube URL: https://www.youtube.com/watch?v=qAF1NjEVHhY
Video ID: qAF1NjEVHhY
Output File: qa_output.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Step 1: Fetching YouTube transcript...
   Delegating to: Gemini
   ✓ Task delegated
   Handoff ID: gemini_1761909287_abc123

⏳ Waiting for Gemini to complete...
.....
   ✓ Transcript fetching completed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Step 2: Parsing transcript into Q&A pairs...
   Delegating to: Droid
   ✓ Task delegated
   Handoff ID: droid_1761909288_def456

⏳ Waiting for Droid to complete...
.....
   ✓ Q&A parsing completed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Workflow Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Output saved to: qa_output.json

Summary:
  • Video ID: qAF1NjEVHhY
  • Q&A Pairs: 15
  • Transcript: shared/workflows/runs/yt_qa_1761909287/transcript.txt
  • Q&A JSON: qa_output.json
```

---

## Agent Instructions

### When Gemini sees a transcript task:

```bash
# 1. Claim it
dreamteam-claim gemini <handoff_id>

# 2. Fetch transcript (use youtube-transcript-api or MCP)
python -c "
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript('qAF1NjEVHhY')
with open('transcript.txt', 'w') as f:
    for entry in transcript:
        f.write(f\"[{entry['start']}] {entry['text']}\\n\")
"

# 3. Complete task
dreamteam-complete gemini <handoff_id> \
  --output ./transcript.txt \
  --notes "Fetched 150 lines"
```

### When Droid sees a parsing task:

```bash
# 1. Claim it
dreamteam-claim droid <handoff_id>

# 2. Read transcript
cat shared/workflows/runs/<workflow_id>/transcript.txt

# 3. Parse to Q&A (use Claude Code or your preferred method)
# Create qa_pairs.json with proper format

# 4. Validate JSON
jq empty qa_pairs.json
jq . qa_pairs.json  # Preview

# 5. Complete task
dreamteam-complete droid <handoff_id> \
  --output ./qa_pairs.json \
  --notes "Generated 15 Q&A pairs"
```

---

## Monitoring

### Check workflow progress:
```bash
dreamteam-status
```

### View workflow logs:
```bash
tail -f shared/history/workflows.log
```

### Check handoff status:
```bash
ls shared/handoffs/*.json
cat shared/handoffs/<handoff_id>.json | jq
```

---

## Troubleshooting

### Issue: Workflow times out

**Check**:
```bash
# Are agents running?
dreamteam-status --agent gemini
dreamteam-status --agent droid

# Are they watching for tasks?
ps aux | grep "dreamteam-poll"
```

**Fix**:
```bash
# Restart agent polling
dreamteam-poll gemini --watch &
dreamteam-poll droid --watch &
```

---

### Issue: No transcript available

**Solution**: Some videos don't have captions/transcripts.

**Gemini should**:
```bash
dreamteam-escalate gemini \
  --handoff <id> \
  --reason "Video has no transcript/captions available" \
  --priority normal
```

---

### Issue: Poor quality Q&A output

**Solution**: Review and refine parsing logic. Droid should:
- Extract clear, specific questions
- Provide complete answers
- Include proper context
- Validate JSON format

See: `AGENT_QUICKREF.md` for quality guidelines

---

## Batch Processing

Process multiple videos:

```bash
#!/usr/bin/env bash
# batch_youtube.sh

VIDEOS=(
  "https://www.youtube.com/watch?v=VIDEO1"
  "https://www.youtube.com/watch?v=VIDEO2"
  "https://www.youtube.com/watch?v=VIDEO3"
)

for VIDEO in "${VIDEOS[@]}"; do
  VIDEO_ID=$(echo "$VIDEO" | grep -oP '(?<=v=)[^&]+')
  dreamteam-workflow youtube-to-qa "$VIDEO" --output "qa_${VIDEO_ID}.json"
  echo "Completed: $VIDEO_ID"
done

# Merge all outputs
jq -s 'map(.qa_pairs) | flatten | {qa_pairs: .}' qa_*.json > all_qa.json
echo "Merged $(jq '.qa_pairs | length' all_qa.json) total Q&A pairs"
```

---

## Next Steps

### Now you can:

1. ✅ **Run the workflow** with the example URL
2. ✅ **Process your own videos** for AI training data
3. ✅ **Batch process** multiple videos
4. ✅ **Customize** the workflow for your needs

### To try it now:

```bash
# Start agents (2 separate terminals)
dreamteam-poll gemini --watch &
dreamteam-poll droid --watch &

# Run workflow
dreamteam-workflow youtube-to-qa https://www.youtube.com/watch?v=qAF1NjEVHhY

# Check output
cat qa_output.json | jq
```

---

## Additional Workflows to Create

Using this as a template, you could create:

- **YouTube → Summary**: Video → Transcript → Summary → Blog post
- **YouTube → Flashcards**: Video → Transcript → Study flashcards
- **YouTube → Podcast Script**: Video → Transcript → Reformatted script
- **Multi-video Research**: Multiple videos → Merged insights → Report

See `WORKFLOWS.md` for more ideas!

---

## Documentation Reference

- **Workflow Script**: `shared/workflows/youtube-to-qa.sh`
- **Workflow Template**: `shared/workflows/TEMPLATE_youtube-to-qa.md`
- **Workflows Guide**: `WORKFLOWS.md`
- **Agent Quick Ref**: `AGENT_QUICKREF.md`
- **CLI Tool**: `shared/bin/dreamteam-workflow`

---

**Status**: ✅ Ready to Use!
**Created**: 2025-10-31
**First Workflow**: YouTube to Q&A
**Next**: Create your own workflows!

---

## Quick Commands

```bash
# List workflows
dreamteam-workflow list

# Get help
dreamteam-workflow help

# Run workflow
dreamteam-workflow youtube-to-qa <URL>

# Check status
dreamteam-status

# Monitor logs
tail -f shared/history/workflows.log
```

**Enjoy your automated YouTube to Q&A pipeline!** 🎉
