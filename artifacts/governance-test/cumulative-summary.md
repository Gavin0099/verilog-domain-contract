# Governance Test — Cumulative Summary

> This document provides the current overall state. Individual round summaries
> (`round-001-summary.md` through `round-006-summary.md`) remain unchanged as
> historical records. See them for per-round detail.

**Last updated**: 2026-05-11
**Snapshot basis**: Run 051 (gate-c-upgrade-pass)

---

## Cumulative Run Totals

| Metric | Value |
|--------|-------|
| Total runs completed | 51 |
| Hard failures | 0 |
| Reviewer decisions: accept | 51 |
| Reviewer decisions: reject | 0 |
| Awaiting reviewer | 0 |

---

## Gate Summary

| Gate | Result | Evidence |
|------|--------|----------|
| Gate A: Data Consistency | **pass** | All 5 Verilog domain rules fully synced (run-026) |
| Gate B: Closed-Loop Quality | **pass** | completion_contract=1.00, native_closeout=1.00, mapped_high=1.00 |
| Gate C: Outcome Value | **pass** | All 3 lanes: review_minutes ✓, rework_rate=0.0 ✓, stability=stable ✓ (run-051) |

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
| Round 7 | 028–037 | Round A Next-Phase Test Playbook (Claude lane): 5.1 comparable, 5.2 stress, 5.3 ablation A-D |
| Round 8 | 038–039 | Gate C Measurement Plan v0.1: infrastructure setup + Claude lane first window report |
| Round 9 | 040 | Gate C Three-Lane Ingest: NDJSON logs (claude×12 + chatgpt×10), validator, sign-off |
| Round 10 | 041–051 | Gate C Phase 2: timestamp capture (10 Claude runs) + Copilot proxy + upgrade to pass |

Note: Run 027 (2026-05-08) is a standalone BR-006/007 replay oracle extension (Round 8 in its run-record; renumbered Round 7.5 informally to avoid collision with governance-test Round 8).

---

## Verilog Domain Contract Rule Coverage (as of Run 026)

| Rule | Leaf Doc | governance_rules | Validator Gate | Smoke (neg+pos) |
|------|----------|-----------------|---------------|-----------------|
| RESET_DEFINITION_REQUIRED | docs/clock-reset-contract.md | yes | Rule 1 | PG-001 / PG-002 |
| HANDSHAKE_TIMING_DEFINITION_REQUIRED | docs/handshake-contract.md | yes | Rule 2 | PG-003 / PG-004 |
| FSM_CONTRACT_REQUIRED | docs/fsm-contract.md | yes | Rule 3 | PG-005 / PG-008 / PG-009 |
| ASSIGNMENT_SEMANTICS_REQUIRED | docs/assignment-semantics.md | yes | Rule 4 | PG-004 / PG-005 |
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
| reconstructed | 11 |
| valid (runtime hook) | 2 |
| total | 13 |

---

## Note on round-004-summary.md

`round-004-summary.md` states "Total runs: 16" and "Reviewer decisions accepted: 16/16"
— those figures were accurate at the time of writing (Run 016). They are not updated
here to avoid historical pollution; consult this document for current totals.
