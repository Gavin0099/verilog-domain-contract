# Governance Test — Cumulative Summary

> This document provides the current overall state. Individual round summaries
> (`round-001-summary.md` through `round-006-summary.md`) remain unchanged as
> historical records. See them for per-round detail.

**Last updated**: 2026-05-08
**Snapshot basis**: Run 026 (dashboard-sync-run026)

---

## Cumulative Run Totals

| Metric | Value |
|--------|-------|
| Total runs completed | 26 |
| Hard failures | 0 |
| Reviewer decisions: accept | 26 |
| Reviewer decisions: reject | 0 |
| Awaiting reviewer | 0 |

---

## Round Breakdown

| Round | Runs | Focus |
|-------|------|-------|
| Round 1 | 001–005 | Infrastructure bootstrap: contract.yaml, rule stubs, directory layout |
| Round 2 | 006–009 | HANDSHAKE rule, diff.patch gaps, session-index alignment |
| Round 3 | 010–012 | FSM_CONTRACT_REQUIRED full propagation, gate_policy.yaml |
| Round 4 | 013–016 | check_documents.py, sync-check CLAIM docs, reviewer-dashboard |
| Round 5 | 017–021 | Dashboard sync, check_advisory hook, ASSIGNMENT_SEMANTICS, governance/rules classification |
| Round 6 | 022–026 | CDC_STRATEGY_REQUIRED full sync, round summaries, smoke v3, FSM explicit smoke, dashboard sync |

---

## Verilog Domain Contract Rule Coverage (as of Run 026)

| Rule | Leaf Doc | governance_rules | Validator Gate | Smoke (neg+pos) |
|------|----------|-----------------|---------------|-----------------|
| RESET_DEFINITION_REQUIRED | docs/reset-contract.md | yes | Rule 1 | PG-001 / PG-002 |
| HANDSHAKE_TIMING_DEFINITION_REQUIRED | docs/handshake-contract.md | yes | Rule 2 | PG-003 / PG-004 |
| FSM_CONTRACT_REQUIRED | docs/fsm-contract.md | yes | Rule 3 | PG-005 / PG-008 / PG-009 |
| ASSIGNMENT_SEMANTICS_REQUIRED | docs/assignment-semantics-contract.md | yes | Rule 4 | PG-004 / PG-005 |
| CDC_STRATEGY_REQUIRED | docs/cdc-contract.md | yes | Rule 5 | PG-006 / PG-007 |

All 5 rules: leaf doc + governance_rules + precondition_effects + must_not_assume +
completion_claim_disallow + rule_sources + validator gate + smoke (positive + negative).

---

## Smoke Suite (as of Run 026)

| Artifact | Cases | Result |
|----------|-------|--------|
| artifacts/precondition-gate/2026-05-08-smoke.json | 9 (PG-001~009) | 9/9 PASS |

---

## Session Index

| Status | Count |
|--------|-------|
| reconstructed | 7 |
| valid (runtime hook) | 2 |
| total | 9 |

---

## Note on round-004-summary.md

`round-004-summary.md` states "Total runs: 16" and "Reviewer decisions accepted: 16/16"
— those figures were accurate at the time of writing (Run 016). They are not updated
here to avoid historical pollution; consult this document for current totals.
