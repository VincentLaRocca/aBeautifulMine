# Wave 2 Batch Submission - Preparation Plan

**Date Created:** November 2, 2025
**Status:** STAGED - Awaiting Wave 1 Validation
**Project:** WeMineHope.com Cryptocurrency Knowledge Base

---

## Executive Summary

Wave 2 consists of **701 new Q&A pairs** from Droid covering DeFi metrics (Sessions 30-31). These will be processed after Wave 1 (204 batches, 20,400 pairs) completes and quality is validated.

### Wave 2 Statistics

| Metric | Value |
|--------|-------|
| **Total Q&A Pairs** | 701 |
| **Sessions** | 30-31 (DeFi Metrics) |
| **Batches Required** | 7 (batches 205-211) |
| **Expected Cost** | $2.40-3.20 (Batch API 50% discount) |
| **Processing Time** | ~24 hours after submission |
| **Staging Location** | `inbox/droid/wave2_staging/` |

---

## Wave 2 Data Inventory

### Session 30: DEX Volume Metrics (500 pairs)

1. **dex_volume_24h_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: dex_volume_24h

2. **dex_volume_7d_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: dex_volume_7d

3. **dex_volume_30d_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: dex_volume_30d

4. **dex_to_cex_volume_ratio_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: dex_to_cex_volume_ratio

5. **liquidity_pool_depth_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: liquidity_pool_depth

### Session 31: DeFi Lending/Protocol Metrics (201 pairs)

6. **impermanent_loss_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: impermanent_loss

7. **supply_rate_qa_pairs.json**
   - Q&A Pairs: 100
   - Category: dex_metrics
   - Indicator: supply_rate

8. **borrow_rate_qa_pairs.json** ⚠️
   - Q&A Pairs: 1
   - Category: dex_metrics
   - Indicator: borrow_rate
   - **Note:** Low count - may need regeneration

9. **slippage_qa_pairs.json** ❌
   - Q&A Pairs: 0
   - Category: dex_metrics
   - Indicator: slippage
   - **Note:** Failed - needs regeneration or exclusion

---

## Processing Plan

### Phase 1: Wave 1 Validation (Current - November 3, 2025)

**Wait for Wave 1 completion:**
1. Monitor batch job status (204 batches)
2. Download completed results
3. Validate refinement quality:
   - Grammar and clarity improvements
   - Technical accuracy preserved
   - Natural conversation flow
   - Compare sample before/after

**Success Criteria for Wave 2 Approval:**
- ✓ 95%+ batch completion rate
- ✓ Refinement improves readability
- ✓ Technical accuracy maintained
- ✓ No significant formatting issues

### Phase 2: Wave 2 Preparation (November 3-4, 2025)

**If Wave 1 validation successful:**

1. **Extract and Format Q&A Pairs**
   ```bash
   python extract_wave2_sessions.py
   ```
   - Input: 9 JSON files in `wave2_staging/`
   - Output: `wave2_extracted.json` (701 pairs)
   - Handle: Low-count files (borrow_rate, slippage)

2. **Create Batch Files (205-211)**
   ```bash
   python create_wave2_batches.py
   ```
   - Batch 205: 100 pairs (dex_volume_24h)
   - Batch 206: 100 pairs (dex_volume_7d)
   - Batch 207: 100 pairs (dex_volume_30d)
   - Batch 208: 100 pairs (dex_to_cex + liquidity_pool)
   - Batch 209: 100 pairs (impermanent_loss)
   - Batch 210: 100 pairs (supply_rate)
   - Batch 211: 1 pair (borrow_rate) - **Consider combining with others**

3. **Update Tracking Files**
   - Append to `batch_tracking.json`
   - Update `WAVE_2_PREPARATION.md` → `WAVE_2_SUBMISSION.md`

### Phase 3: Wave 2 Submission (November 4, 2025)

**Use existing batch submission agent:**

```bash
# Option 1: Manual submission via agent
python batch_submission_agent_mcp.py 205 211

# Option 2: Via Claude Code
"Use the batch submission agent to submit Wave 2 batches 205-211"
```

**Expected Timeline:**
- Submission: ~30 minutes (7 batches with rate limit handling)
- Processing: ~24 hours
- Download: ~1 hour
- Total: ~25 hours

### Phase 4: Combined Processing (November 5+, 2025)

**After Wave 2 completion:**
1. Aggregate all results (batches 1-211)
2. Total Q&A pairs: 21,101 (20,400 + 701)
3. Deduplication across all data
4. Generate embeddings for entire dataset
5. Import to production database

---

## Batch Grouping Strategy

### Option A: Keep 7 Batches (RECOMMENDED)
```
Batch 205: dex_volume_24h (100)
Batch 206: dex_volume_7d (100)
Batch 207: dex_volume_30d (100)
Batch 208: dex_to_cex_ratio (100)
Batch 209: liquidity_pool_depth (100)
Batch 210: impermanent_loss (100)
Batch 211: supply_rate + borrow_rate (101)
```
**Skip:** slippage (0 pairs)

### Option B: Consolidate to 6 Batches
```
Batch 205: dex_volume_24h (100)
Batch 206: dex_volume_7d (100)
Batch 207: dex_volume_30d (100)
Batch 208: dex_to_cex_ratio (100)
Batch 209: liquidity_pool_depth + borrow_rate (101)
Batch 210: impermanent_loss (100)
Batch 211: supply_rate (100)
```

---

## Files to Create

### Script 1: `extract_wave2_sessions.py`
**Purpose:** Extract Q&A pairs from Wave 2 JSON files
**Input:** 9 JSON files in `wave2_staging/`
**Output:** `wave2_extracted.json`
**Logic:**
- Load each JSON file
- Extract qa_pairs array
- Add session/indicator metadata
- Handle edge cases (0 pairs, 1 pair)
- Consolidate into single dataset

### Script 2: `create_wave2_batches.py`
**Purpose:** Create JSONL batch files (205-211)
**Input:** `wave2_extracted.json`
**Output:** 7 JSONL files in `gemini_batch_submissions_proper/`
**Format:** Same as Wave 1 (single request per file)
**Refinement Prompt:** Reuse from Wave 1

### Script 3: `update_batch_tracking.py`
**Purpose:** Update tracking file with Wave 2 batches
**Input:** `batch_tracking.json`, Wave 2 batch info
**Output:** Updated `batch_tracking.json` (211 batches total)

---

## Decision Points

### Issue 1: Borrow Rate (1 pair)
**Options:**
- A) Skip - too few pairs for meaningful batch
- B) Combine with another batch
- C) Ask Droid to regenerate with full 100 pairs

**Recommendation:** Option B - Combine with supply_rate in batch 211

### Issue 2: Slippage (0 pairs)
**Options:**
- A) Skip - no data available
- B) Ask Droid to regenerate
- C) Research separately later

**Recommendation:** Option B - Request regeneration from Droid

### Issue 3: Batch Consolidation
**Options:**
- A) Keep natural topic grouping (7 batches)
- B) Consolidate to fewer batches (6 batches)
- C) Wait to see Wave 1 optimal batch size

**Recommendation:** Option C - Decide after Wave 1 validation

---

## Cost Estimate

### Wave 2 Only
- **Q&A Pairs:** 701
- **Estimated Tokens:** ~91,000 tokens (130 tokens/pair avg)
- **Batch API Rate:** $0.0034 per 1K tokens (50% discount)
- **Estimated Cost:** $2.40-3.20

### Combined (Wave 1 + Wave 2)
- **Total Q&A Pairs:** 21,101
- **Total Batches:** 211
- **Estimated Total Cost:** $70-96

---

## Quality Considerations

### Data Quality Checks (Before Wave 2 Submission)
1. Verify all JSON files are valid
2. Check Q&A pair structure consistency
3. Validate session/indicator metadata
4. Compare format to Wave 1 batches
5. Test 1 sample batch before bulk submission

### Post-Refinement Validation
1. Compare Wave 2 refinement quality to Wave 1
2. Check for DeFi-specific terminology preservation
3. Validate technical accuracy (DEX, liquidity pools, etc.)
4. Assess if refinement prompt needs tuning

---

## Timeline

| Date | Milestone | Status |
|------|-----------|--------|
| Nov 2 | Wave 1 submission complete (204 batches) | ✅ Done |
| Nov 2 | Wave 2 data staged | ✅ Done |
| Nov 3 | Wave 1 results download begins | ⏳ Pending |
| Nov 3 | Wave 1 quality validation | ⏳ Pending |
| Nov 4 | Wave 2 preparation (if approved) | ⏳ Pending |
| Nov 4 | Wave 2 submission (7 batches) | ⏳ Pending |
| Nov 5 | Wave 2 results download | ⏳ Pending |
| Nov 5-6 | Combined processing & database import | ⏳ Pending |

---

## Automation Strategy

### Repeatable Process (Already Built)
✅ Batch submission agent created
✅ State tracking implemented
✅ Rate limit handling automated
✅ Resume capability verified

### Wave 2 Reuses Existing Infrastructure
- Same agent: `batch_submission_agent_mcp.py`
- Same output dir: `gemini_batch_results_proper/`
- Same monitoring: `mcp__gemini__batch_get_status`
- Same download: `mcp__gemini__batch_download_results`

### Only Need to Create
1. Wave 2 extraction script (simple JSON parsing)
2. Wave 2 batch creation script (copy Wave 1 format)
3. Update tracking file (append to existing)

---

## Risk Mitigation

### Risk 1: Wave 1 Quality Issues
**Mitigation:** Thorough validation before Wave 2 approval
**Contingency:** Adjust refinement prompt if needed

### Risk 2: Low-Quality Data in Wave 2
**Mitigation:** Pre-validate JSON files before processing
**Contingency:** Skip or regenerate problematic files

### Risk 3: Quota Limits
**Mitigation:** Smaller batch count (7 vs 204)
**Contingency:** Reuse proven rate limit handling

### Risk 4: Format Inconsistencies
**Mitigation:** Test 1 batch before bulk submission
**Contingency:** Quick format correction if needed

---

## Next Actions

### Immediate (Now)
✅ Stage Wave 2 data files
✅ Create Wave 2 preparation plan
✅ Document decision to wait for Wave 1 validation

### When Wave 1 Completes (~Nov 3)
1. Download first 10 Wave 1 results
2. Perform quality validation
3. Make go/no-go decision for Wave 2
4. Adjust refinement prompt if needed

### If Wave 2 Approved (~Nov 4)
1. Extract Wave 2 Q&A pairs
2. Create batches 205-211
3. Run batch submission agent
4. Monitor processing

---

## Supporting Files

**Already Created:**
- ✅ `batch_submission_agent.py`
- ✅ `batch_submission_agent_mcp.py`
- ✅ `BATCH_AGENT_USAGE.md`
- ✅ `BATCH_SUBMISSION_COMPLETE.md`

**Staged Data:**
- ✅ `inbox/droid/wave2_staging/*.json` (9 files)

**To Create (When Approved):**
- ⏳ `extract_wave2_sessions.py`
- ⏳ `create_wave2_batches.py`
- ⏳ `WAVE_2_SUBMISSION_REPORT.md`

---

## Contact Droid

### Regeneration Requests
If Wave 1 validation successful, request from Droid:

1. **Slippage Indicator** (Session 31)
   - Current: 0 pairs
   - Requested: 100 pairs
   - Category: dex_metrics
   - Priority: Medium

2. **Borrow Rate Indicator** (Session 31)
   - Current: 1 pair
   - Requested: 99 additional pairs (total 100)
   - Category: dex_metrics
   - Priority: Low (can combine with existing data)

---

**Document Status:** ACTIVE - Awaiting Wave 1 Validation
**Next Review Date:** November 3, 2025
**Owner:** Claude Code / WeMineHope.com Team
