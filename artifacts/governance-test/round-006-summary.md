# Governance Test Round 6 Summary

**Runs covered**: Run 022 – Run 026
**Date**: 2026-05-08
**Agent**: claude
**Status**: Complete — Runs 022-026 all accepted

---

## Run Summary

| Run | Task | Files Modified | Key Output | Hard Failure |
|-----|------|---------------|------------|--------------|
| 022 | CDC_STRATEGY_REQUIRED full governance sync | docs/cdc-contract.md (new), contract.yaml, validators/precondition_gate_validator.py, scripts/precondition_gate_smoke.py, docs/contract-sync-check.md, governance/rules/RULE_INDEX.md | Rule 5 + 2 regex; PG-006/007 new; 7/7 PASS; gaps G-022-01~05 fixed | false |
| 023 | Round 5-6 summary documents (meta) | round-005-summary.md (new), round-006-summary.md (new) | Round 5 complete; Round 6 in-progress frame | false |
| 024 | Precondition-gate smoke artifact v2 | artifacts/precondition-gate/2026-05-08-smoke.json (new), contract.yaml | PG-001~007 in single updated artifact with rule labels | false |
| 025 | FSM explicit smoke cases PG-008/009 | scripts/precondition_gate_smoke.py, 2026-05-08-smoke.json | PG-008 (FSM missing) + PG-009 (FSM defined); 9/9 PASS | false |
| 026 | Dashboard sync to 25 runs (meta) | artifacts/governance-test/reviewer-dashboard.md | run-021~025 rows + review notes; round numbers corrected | false |

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

## Cumulative State (Run 001–026)

| Category | Count |
|----------|-------|
| Total runs | 26 |
| High-confidence runs | 25 |
| Medium-confidence runs | 1 (run-002) |
| Hard failures | 0 |
| Scope violations | 0 |
| Claim overreach | 0 |
| Reviewer decisions accepted | 26 / 26 |

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
| FSM_CONTRACT_REQUIRED | ✓ | ✓ | ✓ | Rule 3 | PG-008/009 |
| ASSIGNMENT_SEMANTICS_REQUIRED | ✓ | ✓ | ✓ | Rule 4 | PG-004/005 |
| CDC_STRATEGY_REQUIRED | ✓ | ✓ | ✓ | Rule 5 | PG-006/007 |

---

## Closed Items

| Item | Run | Status |
|------|-----|--------|
| Round 5-6 summary documents | 023 | **Done** |
| Precondition-gate smoke artifact v2 with PG-004~007 | 024 | **Done** |
| FSM explicit smoke cases PG-008/009 | 025 | **Done** |
| Dashboard sync to 25 runs | 026 | **Done** |

All 4 planned items for Round 6 closed. No open governance gaps remain as of Run 026.
