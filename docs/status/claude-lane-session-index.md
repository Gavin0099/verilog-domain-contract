# Claude Lane — Session Index

**Lane**: claude-sonnet-4-6
**Playbook**: Round A Next-Phase Test Playbook (2026-05-11)
**Phase 2 runs**: run-041 to run-050
**Last updated**: run-047

## Session Summary

| Session | Runs | Status | Work |
|---------|------|--------|------|
| session-round9-claude-lane-20260511 | run-028 to run-037 | complete | Round A playbook execution (Claude lane) |
| session-round10-gate-c-setup-20260511 | run-038 to run-039 | complete | Gate C infrastructure + first window report |
| session-round11-gate-c-ingest-20260511 | run-040 | complete | Three-lane NDJSON ingest + validator + sign-off |
| session-round12-gate-c-phase2-20260511 | run-041 to run-050 | complete | Gate C Phase 2: timestamp capture + upgrade to pass |

## Per-Run Index (Round A — Phase 1)

| Run | Task | Playbook Section | Decision |
|-----|------|-----------------|----------|
| run-028 | FSM+CDC checklist extension | 5.1 comparable | accepted |
| run-029 | CLAIM_BOUNDARY wording fix | 5.1 comparable | accepted |
| run-030 | Precondition-completeness-model sync | 5.1 comparable | accepted |
| run-031 | Authority-conflict resolution policy | 5.2 stress | accepted |
| run-032 | Stale-evidence coherence note | 5.2 stress | accepted |
| run-033 | Lifecycle-ambiguity completion-evidence | 5.2 stress | accepted |
| run-034 | Ablation A: no governance vocabulary | 5.3 ablation | accepted |
| run-035 | Ablation B: docs governance only | 5.3 ablation | accepted |
| run-036 | Ablation C: runtime hooks only | 5.3 ablation | accepted |
| run-037 | Ablation D: full governance + meta | 5.3 ablation + meta | accepted |

## Per-Run Index (Gate C Setup — Phase 1→2 transition)

| Run | Task | Gate C Role | Decision |
|-----|------|------------|----------|
| run-038 | Gate C infrastructure setup | Plan + schema + logs | accepted |
| run-039 | Claude lane first window report | provisional-pass documented | accepted |
| run-040 | Three-lane NDJSON ingest + validator | Upgrade gate instrumented | accepted |

## Per-Run Index (Gate C Phase 2 — timestamp capture)

| Run | Task | review_minutes | Decision |
|-----|------|---------------|----------|
| run-041 | Dashboard sync to 41 runs | 35 | accepted |
| run-042 | round-008-summary.md | 22 | accepted |
| run-043 | round-009-summary.md | 19 | accepted |
| run-044 | gate-c-measurement-plan Phase 2 note | 17 | accepted |
| run-045 | gate-c-review-effort-log Phase 2 entries | 20 | accepted |
| run-046 | gate-c-reopen-revert-log Phase 2 update | 16 | accepted |
| run-047 | claude-lane-session-index update | 14 | accepted |
| run-048 | claude-lane-run-ledger update | 18 | accepted |
| run-049 | gate-c-copilot-proxy-data.md | 28 | accepted |
| run-050 | ChatGPT Phase 2 ingest + NDJSON batch | 33 | accepted |

## Source of Truth Links

- Run artifacts: `artifacts/governance-test/runs/run-028/` through `run-050/`
- Run ledger: `artifacts/governance-test/run-ledger.ndjson` (entries 28-50)
- Session ledger: `artifacts/session-index.ndjson`
- Ablation artifacts: `artifacts/ablation/ablation-A/B/C/D.yaml`
- Round summaries: `artifacts/governance-test/round-007-summary.md` through `round-009-summary.md`
- Gate C logs: `docs/status/gate-c-{review,rework,stability}-log.ndjson`
