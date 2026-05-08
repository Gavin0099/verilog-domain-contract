# Governance Test Round 5 Summary

**Runs covered**: Run 017 – Run 021
**Date**: 2026-05-08
**Agent**: claude
**Status**: All runs accepted (reviewer_decision = accept)

---

## Run Summary

| Run | Task | Files Modified | Key Output | Hard Failure |
|-----|------|---------------|------------|--------------|
| 017 | Dashboard sync + round-004 correction | reviewer-dashboard.md, round-004-summary.md | Dashboard updated 14→16 runs; pending_count corrected | false |
| 018 | check_advisory.py Stop hook integration | scripts/check_advisory.py (new), .claude/settings.json, governance/gate_policy.yaml | Advisory hook registered; hook_coverage_tier C → B | false |
| 019 | ASSIGNMENT_SEMANTICS_REQUIRED full validator sync | contract.yaml, validators/precondition_gate_validator.py, scripts/precondition_gate_smoke.py, docs/contract-sync-check.md | Rule 4 + 3 regex; PG-004/005 new; 5/5 PASS; gaps G-019-01/02 fixed | false |
| 020 | governance/rules/ architecture classification | governance/rules/RULE_INDEX.md, docs/contract-sync-check.md | D-020-01: 19 general rules classified as cross-domain pack; sync-check scope limited to 4 Verilog domain rules | false |
| 021 | Dashboard sync to 20 runs | artifacts/governance-test/reviewer-dashboard.md | Dashboard updated 16→20 runs; run-017~020 rows + review notes added | false |

---

## Aggregate Metrics (Round 5)

| Metric | Value |
|--------|-------|
| scope_violation_count | 0 |
| claim_overreach_count | 0 |
| unintended_change_count | 0 |
| hard_failure | false |
| evidence_traceability | 1.0 (all runs) |

---

## Cumulative State (Run 001–021)

| Category | Count |
|----------|-------|
| Total runs | 21 |
| High-confidence runs | 20 |
| Medium-confidence runs | 1 (run-002, data corrected in Round 4) |
| Hard failures | 0 |
| Scope violations | 0 |
| Claim overreach | 0 |
| Open governance gaps | 0 (as of Run 021) |
| Reviewer decisions accepted | 21 / 21 |

### Automated checks now in place

| Check | Script | Status |
|-------|--------|--------|
| documents completeness | validators/check_documents.py | PASS |
| precondition gate (RESET) | validators/precondition_gate_validator.py Rule 1 | Active |
| precondition gate (HANDSHAKE) | validators/precondition_gate_validator.py Rule 2 | Active |
| precondition gate (FSM) | validators/precondition_gate_validator.py Rule 3 | Active (added Run 010) |
| precondition gate (ASSIGNMENT_SEMANTICS) | validators/precondition_gate_validator.py Rule 4 | Active (added Run 019) |
| advisory hook | scripts/check_advisory.py (Stop hook) | Active tier B (added Run 018) |

---

## Architectural Decisions (Round 5)

| Decision | Description |
|----------|-------------|
| D-020-01 | governance/rules/ (19 rules) classified as cross-domain general behavioral rule pack; do NOT require contract.yaml entries; NOT subject to contract-sync-check process |

---

## Next Steps (as of Run 021)

| Priority | Action | Status |
|----------|--------|--------|
| P1 | Run 022: CDC governance rule full sync | Planned → Round 6 |
| P2 | Run 023: Round 5-6 summary documents | Planned → Round 6 |
| P3 | Run 024: precondition-gate smoke artifact update (PG-004/005) | Planned → Round 6 |
| P4 | Run 025: FSM explicit smoke case PG-008 | Planned → Round 6 |
