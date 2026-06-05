# Gate C Three-Lane Ingest Checklist — Completed

Window ID: `gate-c-window-2026-05-11`
Date run: 2026-05-11
Validator: `scripts/gate_c_ingest_check.py`

---

## 1) Required Files

- [x] `docs/status/gate-c-review-log.ndjson` — **PASS** (exists, 22 rows: 12 claude + 10 chatgpt)
- [x] `docs/status/gate-c-rework-log.ndjson` — **PASS** (exists, 22 rows: 12 claude + 10 chatgpt)
- [x] `docs/status/gate-c-stability-log.ndjson` — **PASS** (exists, 22 rows: 12 claude + 10 chatgpt)

---

## 2) Schema Checklist

### 2.1 Review log

- [x] `window_id` — present in all rows
- [x] `lane` — present in all rows
- [x] `run_id` — present in all rows
- [x] `review_start_utc` — present (value: null — Phase 1; timestamps not yet captured)
- [x] `review_end_utc` — present (value: null — Phase 1; timestamps not yet captured)
- [x] `review_minutes` — present (value: null — Phase 1; timestamps not yet captured)
- [x] `window_id == gate-c-window-2026-05-11` — all rows pass
- [x] `review_end_utc >= review_start_utc` — N/A (both null; no violation)
- [x] `review_minutes >= 0` — N/A (null; pending)

Minimum volume (valid rows = review_minutes is non-null and >= 0):
- [ ] Copilot: **0/10** valid rows — **FAIL** (no Copilot data ingested)
- [ ] Claude: **0/10** valid rows — **FAIL** (12 pending; timestamps null)
- [ ] ChatGPT: **0/10** valid rows — **FAIL** (10 pending; timestamps null)

### 2.2 Rework log

- [x] `window_id` — present, correct
- [x] `lane` — present
- [x] `run_id` — present
- [x] `reopen_count` — present
- [x] `revert_count` — present
- [x] `total_changes` — present
- [x] `reopen_revert_rate` — present
- [x] `window_id == gate-c-window-2026-05-11` — all rows pass
- [x] `total_changes > 0` — PASS for claude (12) and chatgpt (10); FAIL for copilot (0 rows)
- [x] `reopen_revert_rate == (reopen_count + revert_count) / total_changes` — 0.0/0.0/1 = 0.0 ✓ for all 22 rows

### 2.3 Stability log

- [x] `window_id` — present, correct
- [x] `lane` — present
- [x] `run_id` — present
- [x] `integration_stability` — present; values: `stable` only
- [x] `stability_note` — present
- [x] `window_id == gate-c-window-2026-05-11` — all rows pass
- [x] `integration_stability != unknown` — PASS for all 22 rows

---

## 3) Lane-by-Lane Ingest Checklist

### 3.1 Copilot lane

- [ ] review log rows ingested (>=10) — **FAIL**: 0 rows (no Copilot data)
- [ ] rework log row(s) ingested with valid denominator — **FAIL**: 0 rows
- [ ] stability log row(s) ingested — **FAIL**: 0 rows
- [ ] lane-level Gate C recomputed — **BLOCKED**: no input data

**Copilot status**: no data. Pending same-form ingest per original playbook §8.1.

### 3.2 Claude lane

- [ ] review log rows ingested (>=10) — **WARN**: 12 rows ingested, 0 valid (12 pending; review_minutes=null)
- [x] rework log row(s) ingested with valid denominator — **PASS**: 12 rows, total_changes=12
- [x] stability log row(s) ingested — **PASS**: 12 rows, all stable
- [ ] lane-level Gate C recomputed — **PARTIAL**: rework+stability computable; review_effort=null

Claude lane partial result:
- reopen_revert_rate: **0.0000** (PASS)
- integration_stability: **stable** (PASS)
- avg_review_minutes: **null** (PENDING)

### 3.3 ChatGPT lane

- [ ] review log rows ingested (>=10) — **WARN**: 10 rows ingested, 0 valid (10 pending; review_minutes=null)
- [x] rework log row(s) ingested with valid denominator — **PASS**: 10 rows, total_changes=10
- [x] stability log row(s) ingested — **PASS**: 10 rows, all stable
- [ ] lane-level Gate C recomputed — **PARTIAL**: rework+stability computable; review_effort=null

ChatGPT lane partial result:
- reopen_revert_rate: **0.0000** (PASS)
- integration_stability: **stable** (PASS)
- avg_review_minutes: **null** (PENDING)

---

## 4) Upgrade Gate (provisional-pass -> pass)

- [ ] All three lanes have >=10 valid review timing rows — **FAIL**
  - Copilot: 0 (no data)
  - Claude: 0 valid (12 pending)
  - ChatGPT: 0 valid (10 pending)
- [ ] All three lanes have valid reopen/revert denominator — **FAIL** (Copilot: 0 rows)
- [ ] All three lanes have non-unknown stability entries — **FAIL** (Copilot: 0 rows)
- [ ] `avg_review_minutes` is computed from valid rows per lane — **FAIL** (all null)

**Upgrade gate: BLOCKED**. Keep `provisional-pass`.

---

## 5) Final Sign-off

- Reviewer: `gate_c_ingest_check.py` (automated) + run-040
- Date: 2026-05-11
- Result: **`provisional-pass`**
- Notes:
  - Infrastructure complete: all 3 required NDJSON files exist with correct schema.
  - Claude lane rework + stability: PASS (rate=0.0, all stable).
  - ChatGPT lane rework + stability: PASS (rate=0.0, all stable).
  - Copilot lane: no data at all — pending same-form ingest.
  - All review_minutes: null — Phase 1 timestamp capture not yet active for any lane.
  - **Upgrade path**: capture review_start_utc/review_end_utc for next >=10 runs per lane, ingest Copilot lane data, re-run `scripts/gate_c_ingest_check.py`. If all conditions pass: upgrade to `pass`.

---

## Validator Output (raw)

```
§1  Required Files
  [PASS]  gate-c-review-log.ndjson
  [PASS]  gate-c-rework-log.ndjson
  [PASS]  gate-c-stability-log.ndjson

§2.1  Review Log
  [FAIL]  copilot  total=0   valid=0   pending=0
  [FAIL]  claude   total=12  valid=0   pending=12
  [FAIL]  chatgpt  total=10  valid=0   pending=10

§2.2  Rework Log
  [FAIL]  copilot  valid_rows=0   total_changes=0   rate=N/A
  [PASS]  claude   valid_rows=12  total_changes=12  rate=0.0000
  [PASS]  chatgpt  valid_rows=10  total_changes=10  rate=0.0000

§2.3  Stability Log
  [FAIL]  copilot  stable=0   degraded=0  unknown=0
  [PASS]  claude   stable=12  degraded=0  unknown=0
  [PASS]  chatgpt  stable=10  degraded=0  unknown=0

§4  Upgrade Gate: BLOCKED
  Gate C result: provisional-pass
  Blocked by: review_minutes=null for all rows; copilot lane has 0 entries
```
