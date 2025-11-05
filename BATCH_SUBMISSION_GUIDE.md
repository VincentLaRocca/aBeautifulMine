# Batch Submission Guide - Properly Formatted Files

**Created:** 2025-11-02
**Status:** READY FOR SUBMISSION
**Format:** Proper JSONL (single request per file)

---

## Overview

**All 196 batches are ready for submission with correct JSONL formatting:**

- ✅ Location: `gemini_batch_submissions_proper/`
- ✅ Files: `batch_001_proper.jsonl` through `batch_196_proper.jsonl`
- ✅ Format: Single request per file with complete prompt + Q&A data
- ✅ Total Q&A pairs: 19,556
- ✅ Tracking data: `batch_tracking.json`

---

## File Format (Correct)

Each `.jsonl` file contains a **single line** with this structure:

```json
{"request": {"contents": [{"parts": [{"text": "<FULL_PROMPT + ALL_QA_PAIRS>"}]}]}}
```

**Key differences from incorrect format:**
- ❌ OLD: 300-400 requests per file (one per line)
- ✅ NEW: 1 request per file (complete prompt + data)

---

## Repeatable Submission Process

### Method 1: Automated Submission (Recommended)

Create a script to automate the upload and submission of all 196 batches:

```python
import json
from pathlib import Path

# Load tracking data
with open('gemini_batch_submissions_proper/batch_tracking.json') as f:
    tracking = json.load(f)

# For each batch:
for batch_info in tracking['batches']:
    batch_num = batch_info['batch_number']
    file_path = Path(batch_info['file_path']).resolve()

    # 1. Upload file
    upload_result = mcp__gemini__upload_file(
        filePath=str(file_path),
        displayName=f'refinement_batch_{batch_num:03d}',
        mimeType='text/plain'
    )

    # 2. Create batch job
    batch_result = mcp__gemini__batch_create(
        inputFileUri=upload_result['fileUri'],
        model='gemini-2.5-flash',
        displayName=f'refinement_batch_{batch_num:03d}',
        outputLocation='c:\\Users\\VLARO\\dreamteam\\claude\\gemini_batch_results_proper'
    )

    # 3. Track submission
    print(f"Batch {batch_num}: {batch_result['batchName']}")
```

### Method 2: Manual Batch Submission

Submit in groups (e.g., 10-20 at a time):

**Step 1: Upload files**
```
For batches 1-10:
  mcp__gemini__upload_file(
    filePath='c:\\Users\\VLARO\\dreamteam\\claude\\gemini_batch_submissions_proper\\batch_001_proper.jsonl',
    displayName='refinement_batch_001',
    mimeType='text/plain'
  )
  ... repeat for batches 2-10
```

**Step 2: Create batch jobs**
```
For each uploaded file:
  mcp__gemini__batch_create(
    inputFileUri='<uri_from_upload>',
    model='gemini-2.5-flash',
    displayName='refinement_batch_XXX',
    outputLocation='c:\\Users\\VLARO\\dreamteam\\claude\\gemini_batch_results_proper'
  )
```

---

## Submission Strategy

### Option A: All at Once (Fastest)
- Submit all 196 batches immediately
- Processing: 24-48 hours
- Cost: ~$65-90
- Advantage: Done fastest
- Risk: If something wrong, all batches affected

### Option B: Phased Submission (Safer)
1. **Phase 1:** Submit batches 1-10 (test)
2. **Validate:** Check 1-2 results for quality
3. **Phase 2:** Submit batches 11-100
4. **Phase 3:** Submit batches 101-196
- Processing: 24-48 hours per phase
- Advantage: Validate quality between phases
- Timeline: ~3-4 days total

### Option C: Small Test First (Safest)
1. **Test:** Submit batches 1-3
2. **Validate:** Confirm results are correct
3. **Full:** Submit remaining 193 batches
- Recommended if uncertain about format
- Adds ~1 day to timeline

---

## Tracking Submissions

### Create Tracking File

After each batch submission, save tracking data:

```json
{
  "submission_date": "2025-11-02",
  "total_submitted": 196,
  "batches": [
    {
      "batch_number": 1,
      "file_path": "gemini_batch_submissions_proper/batch_001_proper.jsonl",
      "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/xxx",
      "batch_name": "batches/xxxxx",
      "qa_count": 100,
      "state": "JOB_STATE_PENDING",
      "submitted_at": "2025-11-02T15:00:00Z"
    },
    ...
  ]
}
```

Save to: `gemini_batch_submissions_proper/submission_tracking.json`

---

## Monitoring Progress

### Check Batch Status

```python
# Check single batch
status = mcp__gemini__batch_get_status(
    batchName='batches/xxxxx'
)

# Check all batches
with open('gemini_batch_submissions_proper/submission_tracking.json') as f:
    tracking = json.load(f)

for batch in tracking['batches']:
    status = mcp__gemini__batch_get_status(batchName=batch['batch_name'])
    print(f"Batch {batch['batch_number']}: {status['state']}")
```

### Expected States
- `JOB_STATE_PENDING`: Queued, waiting to start
- `JOB_STATE_RUNNING`: Currently processing
- `JOB_STATE_SUCCEEDED`: ✅ Complete, ready to download
- `JOB_STATE_FAILED`: ❌ Error occurred
- `JOB_STATE_CANCELLED`: Manually stopped

---

## Downloading Results

### Download Single Batch

```python
results = mcp__gemini__batch_download_results(
    batchName='batches/xxxxx',
    outputLocation='c:\\Users\\VLARO\\dreamteam\\claude\\gemini_batch_results_proper'
)
```

### Download All Completed Batches

```python
with open('gemini_batch_submissions_proper/submission_tracking.json') as f:
    tracking = json.load(f)

for batch in tracking['batches']:
    status = mcp__gemini__batch_get_status(batchName=batch['batch_name'])

    if status['state'] == 'JOB_STATE_SUCCEEDED':
        results = mcp__gemini__batch_download_results(
            batchName=batch['batch_name'],
            outputLocation='gemini_batch_results_proper'
        )
        print(f"Downloaded: batch_{batch['batch_number']:03d}_results.json")
```

---

## Cost Estimates

### By Submission Size

| Batches | Q&A Pairs | Estimated Cost |
|---------|-----------|----------------|
| 3 (test) | 300 | $1.00 - $1.40 |
| 10 | 1,000 | $3.30 - $4.60 |
| 50 | 5,000 | $16.50 - $23.00 |
| 100 | 10,000 | $33.00 - $46.00 |
| 196 (all) | 19,556 | $65.00 - $90.00 |

**Note:** Batch API provides 50% discount vs standard API

---

## Timeline

### Typical Processing Times

| Phase | Time |
|-------|------|
| Upload files (196) | 2-3 hours |
| Submit jobs (196) | 1-2 hours |
| Gemini processing | 24-48 hours |
| Download results | 1-2 hours |
| **Total** | **28-55 hours** |

### Optimized Timeline (Phased)

| Phase | Batches | Time |
|-------|---------|------|
| Phase 1: Test | 3 | ~2 hours |
| Validation | - | 1 hour |
| Phase 2: Main | 193 | ~50 hours |
| **Total** | 196 | **~53 hours (~2.2 days)** |

---

## Quality Validation

### After First Batch Completes

1. Download results
2. Check structure:
   ```python
   with open('batch_001_results.json') as f:
       results = json.load(f)

   # Should contain refined Q&A pairs
   for pair in results[:3]:
       print(f"Pair ID: {pair['pair_id']}")
       print(f"Quality Score: {pair['quality_score']}")
       print(f"Answer Length: {len(pair['refined_answer'])}")
   ```

3. Validate quality:
   - Quality scores: 85-100
   - Answer length: 2000-4000 chars
   - 2024-2025 examples included
   - Improvements documented

---

## Troubleshooting

### Batch Fails to Upload

**Error:** File not found or upload fails
**Solution:**
- Verify file path is absolute
- Check file exists and is readable
- Ensure file size < 20MB

### Batch Job Fails

**Error:** JOB_STATE_FAILED
**Solution:**
```python
status = mcp__gemini__batch_get_status(batchName='batches/xxxxx')
print(status.get('error'))  # Review error details
```

Common issues:
- Input file format problem
- Model configuration issue
- API quota limits

### Download Fails

**Error:** Cannot download results
**Solution:**
- Verify batch state is SUCCEEDED
- Check batch completed (not still processing)
- Retry download after few minutes

---

## Checklist

### Pre-Submission
- [x] All 196 JSONL files generated
- [x] Files in correct format (single request per file)
- [x] Tracking data available
- [x] Output directory created
- [ ] Decide submission strategy (all at once vs phased)
- [ ] Test batch validated (optional but recommended)

### During Submission
- [ ] Upload files with mimeType='text/plain'
- [ ] Create batch jobs with correct model
- [ ] Track each batch name and file URI
- [ ] Save submission tracking data
- [ ] Monitor first few batches

### Post-Submission
- [ ] Check batch status periodically
- [ ] Download results as they complete
- [ ] Validate quality of first results
- [ ] Process all refined Q&A pairs
- [ ] Generate completion report

---

## Quick Reference

### Key Files
- **JSONL files:** `gemini_batch_submissions_proper/batch_XXX_proper.jsonl`
- **Tracking:** `gemini_batch_submissions_proper/batch_tracking.json`
- **Submissions:** `gemini_batch_submissions_proper/submission_tracking.json`
- **Results:** `gemini_batch_results_proper/batch_XXX_results.json`

### Key Commands
```python
# Upload
mcp__gemini__upload_file(filePath='...', displayName='...', mimeType='text/plain')

# Submit
mcp__gemini__batch_create(inputFileUri='...', model='gemini-2.5-flash', displayName='...')

# Monitor
mcp__gemini__batch_get_status(batchName='batches/xxxxx')

# Download
mcp__gemini__batch_download_results(batchName='batches/xxxxx')
```

---

**Status:** READY FOR SUBMISSION
**Next Action:** Choose submission strategy and begin upload + submission process
**Expected Completion:** 2-3 days from submission start
