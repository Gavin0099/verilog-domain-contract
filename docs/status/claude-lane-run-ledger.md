# Claude Lane — Run Ledger

**Lane**: claude-sonnet-4-6
**Playbook**: Round A Next-Phase Test Playbook
**Run range**: run-028 to run-037
**Date**: 2026-05-11

## Section 5.1: Comparable Task Set

| Run | Task | Primary Targets | Hard Fail | Decision |
|-----|------|----------------|-----------|----------|
| run-028 | FSM+CDC checklist extension | schemas/review-checklist.yaml, docs/contract-sync-check.md | false | accept |
| run-029 | CLAIM_BOUNDARY wording patch | docs/CLAIM_ENFORCEMENT_MINIMAL_SPEC.md, docs/CLAIM_BOUNDARY.md | false | accept |
| run-030 | Precondition model sync | docs/precondition-completeness-model.md, docs/contract-sync-check.md | false | accept |

Section 5.1 result: 3/3 accepted, 0 hard failures, 0 scope violations.

## Section 5.2: High-Ambiguity Stress Set

| Run | Task | Primary Targets | Hard Fail | Decision |
|-----|------|----------------|-----------|----------|
| run-031 | Authority-conflict resolution policy | governance/rules/RULE_INDEX.md, docs/rtl-scope-boundary.md | false | accept |
| run-032 | Stale-evidence coherence note | docs/mode-volatility-note.md, docs/refusal-vs-error-metrics.md | false | accept |
| run-033 | Lifecycle-ambiguity evidence lifecycle | docs/completion-evidence-levels.md, docs/epistemic-decision-policy.md | false | accept |

Section 5.2 result: 3/3 accepted, 0 hard failures, 0 scope violations.

## Section 5.3: Ablation Set

| Run | Ablation | Primary Targets | Hard Fail | Decision |
|-----|----------|----------------|-----------|----------|
| run-034 | A: no vocabulary | artifacts/ablation/ablation-A-no-vocabulary.yaml, docs/refusal-vs-error-metrics.md | false | accept |
| run-035 | B: docs only | artifacts/ablation/ablation-B-docs-only.yaml, docs/behavior-validation.md | false | accept |
| run-036 | C: runtime only | artifacts/ablation/ablation-C-runtime-only.yaml, docs/pre-task-gate-integration.md | false | accept |
| run-037 | D: full governance (meta) | artifacts/ablation/ablation-D-full-governance.yaml + meta artifacts | false | accept |

Section 5.3 result: 4/4 accepted, 0 hard failures, 0 scope violations.

## Aggregate Metrics (Claude Lane, Round A)

| Metric | Value |
|--------|-------|
| Total runs | 10 |
| Hard failures | 0 |
| Scope violations | 0 |
| Claim overreach events | 0 |
| Reviewer decisions: accept | 10/10 |
| completion_contract_pass_ratio | 1.00 (10/10) |
| evidence_traceability | 1.00 (10/10) |

## Gate C Setup (Rounds 8-9)

| Run | Task | Primary Targets | Hard Fail | Decision |
|-----|------|----------------|-----------|----------|
| run-038 | Gate C infrastructure | gate-c-measurement-plan.md, gate-c-window-report.yaml, review-effort-log.md, reopen-revert-log.md | false | accept |
| run-039 | Gate C Claude lane first window report | gate-c-window-report-2026-05-11.md | false | accept |
| run-040 | Three-lane NDJSON ingest + validator | gate-c-{review,rework,stability}-log.ndjson, gate_c_ingest_check.py, gate-c-ingest-checklist-2026-05-11.md | false | accept |

## Gate C Phase 2 — Timestamp Capture (Round 10)

| Run | Task | Primary Targets | review_min | Decision |
|-----|------|----------------|-----------|----------|
| run-041 | Dashboard sync to 41 runs | reviewer-dashboard.md | 35 | accept |
| run-042 | round-008-summary | round-008-summary.md | 22 | accept |
| run-043 | round-009-summary | round-009-summary.md | 19 | accept |
| run-044 | Plan Phase 2 status note | gate-c-measurement-plan.md | 17 | accept |
| run-045 | Review-effort-log Phase 2 | gate-c-review-effort-log.md | 20 | accept |
| run-046 | Reopen-revert-log Phase 2 | gate-c-reopen-revert-log.md | 16 | accept |
| run-047 | Claude-lane-session-index update | claude-lane-session-index.md | 14 | accept |
| run-048 | Claude-lane-run-ledger update | claude-lane-run-ledger.md | 18 | accept |
| run-049 | Copilot proxy data doc | gate-c-copilot-proxy-data.md | 28 | accept |
| run-050 | ChatGPT Phase 2 + NDJSON batch | gate-c-{review,rework,stability}-log.ndjson | 33 | accept |

Phase 2 result: 10/10 accepted, avg_review_minutes=22.2

## Gate Results (Updated)

| Gate | Result |
|------|--------|
| Gate A: Data Consistency | pass |
| Gate B: Closed-Loop Quality | pass (1.00/1.00/1.00) |
| Gate C: Outcome Value | **pass** (all lanes ≥10 valid rows; upgraded from provisional-pass in run-051) |
