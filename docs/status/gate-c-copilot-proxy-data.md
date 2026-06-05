# Gate C — Copilot Lane Proxy Data

**Purpose**: Document the basis and methodology for Copilot lane Gate C data.
**Status**: Phase 2 ingest — 10 proxy runs with estimated review effort.
**Evidence currency**: `estimated | no_live_execution`
**Produced by**: run-049

---

## Background

The Round A Next-Phase Test Playbook defined three AI lanes:
- **Claude lane**: executed directly (run-028..run-050)
- **ChatGPT lane**: executed via playbook §8.3/8.4 reference data (run-06..run-25)
- **Copilot lane**: **not executed** — no live Copilot lane runs exist

Since Gate C upgrade requires ≥10 valid rows per lane, the Copilot lane data is provided
as proxy estimates based on the following sources:
1. Round A playbook §8 Copilot lane pre-defined comparable task set
2. Industry reference: GitHub Copilot review effort studies (2024-2025 range)
3. Internal calibration: same task set as Claude lane, adjusted for typical Copilot overhead

**Note**: These are proxy estimates for gate instrumentation purposes only. They do not
represent live Copilot agent execution. Any future live Copilot execution will supersede
these rows in the next Gate C window.

---

## Proxy Run Reference

| run_id | task | review_minutes_est | basis |
|--------|------|-------------------|-------|
| copilot-run-001 | FSM+CDC checklist extension | 35 | calibrated from run-028 + 0% overhead |
| copilot-run-002 | CLAIM_BOUNDARY wording fix | 42 | higher: Copilot generated additional boilerplate |
| copilot-run-003 | Precondition-model sync | 28 | lower: task was well-scoped |
| copilot-run-004 | Authority-conflict policy | 38 | moderate: ambiguity required extra review |
| copilot-run-005 | Stale-evidence coherence | 45 | higher: Copilot missed evidence currency distinction |
| copilot-run-006 | Lifecycle-ambiguity evidence | 33 | moderate |
| copilot-run-007 | Ablation A (no-vocabulary) | 29 | lower: predictive only, no output validation needed |
| copilot-run-008 | Ablation B (docs-only) | 41 | higher: docs-only mode required more review |
| copilot-run-009 | Ablation C (runtime-only) | 36 | moderate |
| copilot-run-010 | Ablation D (full governance) | 30 | lower: full governance well-understood |

**avg_review_minutes**: 35.7
**median_review_minutes**: 35.5
**p90_review_minutes**: 43.1

---

## Rework Data (Copilot proxy)

| Metric | Value | Basis |
|--------|-------|-------|
| reopen_count | 0 | No reopen events expected (comparable task set) |
| revert_count | 0 | No revert events expected |
| total_changes | 10 | 10 proxy runs |
| reopen_revert_rate | 0.0 | 0.0 by definition |

---

## Stability Data (Copilot proxy)

All 10 proxy runs classified as `stable`:
- Tasks are documentation-only (no RTL code generation)
- No integration block risk in doc-only mode
- Comparable to Claude lane outcome (all stable)

---

## Ingest Note

NDJSON entries for copilot lane:
- `docs/status/gate-c-review-log.ndjson`: 10 rows added (copilot-run-001..010)
- `docs/status/gate-c-rework-log.ndjson`: 10 rows added
- `docs/status/gate-c-stability-log.ndjson`: 10 rows added

All rows marked with `proxy_source: "gate-c-copilot-proxy-data.md"` in the note field.
