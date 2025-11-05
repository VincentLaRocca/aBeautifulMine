# Refinement Batch Submission Guide

## Summary
- **Total Q&A Pairs:** 19,556
- **Total Batches:** 196
- **Batch Size:** ~100 pairs
- **Estimated Tokens:** ~23,520,000 tokens (~11,760,000 with 50% discount)

## Batch Processing Strategy

Given the test success (3 pairs → quality scores 92-96), we're using:
- **100 pairs per batch** for optimal quality
- **196 total batches** for full dataset
- **Gemini 2.5 Flash** for cost-effective refinement

## Options for Submission

### Option A: Gemini Batch API (Recommended for Scale)
Use the Gemini batch processing MCP tools to submit all batches:
- Lower cost (50% discount)
- Automated processing (~24 hours)
- Best for processing all 196 batches

### Option B: Sequential Chat API (For Testing)
Process a few batches first to validate:
- Use `mcp__gemini__chat` for first 5-10 batches
- Validate results quality
- Then switch to batch API for remainder

### Option C: Hybrid Approach (Recommended)
1. Process first 10 batches via chat API (validate quality)
2. If quality is good, submit remaining 186 via batch API
3. Monitor and adjust as needed

## File Structure
Each batch has:
- `refinement_batch_XXX.json` - Structured data
- `refinement_batch_XXX_content.txt` - Human-readable version

## Estimated Timeline
- **Batch API:** ~24 hours for all batches
- **Chat API:** ~2-3 hours per 10 batches (if done sequentially)
- **Recommended:** Mix of both (~2-3 days total)

## Next Command
```python
# For chat API test (process first 5 batches):
# Use mcp__gemini__chat with content from refinement_batch_001.json

# For batch API (full processing):
# Use mcp__gemini__batch_create with prepared content files
```
