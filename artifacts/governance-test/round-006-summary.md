# Governance Test Round 6 Summary

**Runs covered**: Run 022 – Run 025 (in progress)
**Date**: 2026-05-08
**Agent**: claude
**Status**: In progress — Run 022 accepted; Runs 023-025 pending

---

## Run Summary

| Run | Task | Files Modified | Key Output | Hard Failure |
|-----|------|---------------|------------|--------------|
| 022 | CDC_STRATEGY_REQUIRED full governance sync | docs/cdc-contract.md (new), contract.yaml, validators/precondition_gate_validator.py, scripts/precondition_gate_smoke.py, docs/contract-sync-check.md, governance/rules/RULE_INDEX.md | Rule 5 + 2 regex; PG-006/007 new; 7/7 PASS; gaps G-022-01~05 fixed | false |
| 023 | Round 5-6 summary documents | artifacts/governance-test/round-005-summary.md (new), round-006-summary.md (new) | Round 5 complete; Round 6 in-progress frame | false |
| 024 | precondition-gate smoke artifact update | artifacts/precondition-gate/2026-04-22-smoke.json | PG-004/005/006/007 results recorded | false |
| 025 | FSM explicit smoke case PG-008 | scripts/precondition_gate_smoke.py, artifacts | FSM keyword trigger + state model defined test | false |

---

## Aggregate Metrics (Round 6)

| Metric | Value |
|--------|-------|
| scope_violation_count | 0 |
| claim_overreach_count | 0 |
| unintended_change_count | 0 |
| hard_failure | false |
| evidence_traceability | 1.0 (all completed runs) |

---

## Cumulative State (Run 001–022, partial)

| Category | Count |
|----------|-------|
| Total runs | 22 |
| High-confidence runs | 21 |
| Medium-confidence runs | 1 (run-002) |
| Hard failures | 0 |
| Scope violations | 0 |
| Claim overreach | 0 |
| Reviewer decisions accepted | 22 / 22 |

### Automated checks now in place (as of Run 022)

| Check | Script | Status |
|-------|--------|--------|
| documents completeness | validators/check_documents.py | PASS |
| precondition gate (RESET) | validators/precondition_gate_validator.py Rule 1 | Active |
| precondition gate (HANDSHAKE) | validators/precondition_gate_validator.py Rule 2 | Active |
| precondition gate (FSM) | validators/precondition_gate_validator.py Rule 3 | Active |
| precondition gate (ASSIGNMENT_SEMANTICS) | validators/precondition_gate_validator.py Rule 4 | Active |
| precondition gate (CDC) | validators/precondition_gate_validator.py Rule 5 | Active (added Run 022) |
| advisory hook | scripts/check_advisory.py (Stop hook) | Active tier B |

### Verilog Domain Contract Rules — full coverage status

| Rule | Leaf Doc | governance_rules | precondition_effects | validator | smoke |
|------|----------|-----------------|---------------------|-----------|-------|
| RESET_DEFINITION_REQUIRED | ✓ | ✓ | ✓ | Rule 1 | PG-001 |
| HANDSHAKE_TIMING_DEFINITION_REQUIRED | ✓ | ✓ | ✓ | Rule 2 | PG-002/003 |
| FSM_CONTRACT_REQUIRED | ✓ | ✓ | ✓ | Rule 3 | (implicit PG-003, explicit PG-008 pending) |
| ASSIGNMENT_SEMANTICS_REQUIRED | ✓ | ✓ | ✓ | Rule 4 | PG-004/005 |
| CDC_STRATEGY_REQUIRED | ✓ | ✓ | ✓ | Rule 5 | PG-006/007 |

---

## Open Items (to be closed in Runs 023-025)

| Item | Run | Status |
|------|-----|--------|
| Round 5-6 summary documents | 023 | **This run** |
| precondition-gate/2026-04-22-smoke.json update with PG-004~007 | 024 | Pending |
| FSM explicit smoke case PG-008 | 025 | Pending |
