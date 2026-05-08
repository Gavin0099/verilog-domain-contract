# Governance Test Reviewer Dashboard

**Generated**: 2026-05-08
**Total runs**: 14 (run-001 ~ run-014)
**Pending reviewer decisions**: 14

This document summarises every run for human review. For each run, the reviewer should:
1. Read the `round_note` in the scorecard
2. Verify the diff.patch is plausible (spot check)
3. Fill `reviewer_decision` in the scorecard (accept / accept_with_note / reject)
4. Optionally fill `one_line_note` in run-record reviewer section

---

## Quick Status Table

| Run | Task | Round | Hard Fail | Scope Viol | Claim Viol | Artifact Confidence | Reviewer Decision |
|-----|------|-------|-----------|------------|------------|--------------------|--------------------|
| run-001 | Contract consistency (A) | 1 | false | 0 | 0 | high | **pending** |
| run-002 | Rule normalization (B) | 1 | false | 0 | 0 | **medium** (data corrected) | **pending** |
| run-003 | Failure-state boundary (C) | 1 | false | 0 | 0 | high | **pending** |
| run-004 | Traceability contract (D) | 1 | false | 0 | 0 | high | **pending** |
| run-005 | Cross-verify A-rerun | 1 | false | 0 | 0 | high | **pending** |
| run-006 | FSM governance backfill | 2 | false | 0 | 0 | high | **pending** |
| run-007 | gate_policy.yaml add | 2 | false | 0 | 0 | high | **pending** |
| run-008 | Traceability cross-verify (C replay) | 2 | false | 0 | 0 | high | **pending** |
| run-009 | Validator smoke (obs-only) | 2 | false | 0 | 0 | high | **pending** |
| run-010 | Validator FSM extension | 3 | false | 0 | 0 | high | **pending** |
| run-011 | Contract sync-check doc | 3 | false | 0 | 0 | high | **pending** |
| run-012 | Round 3 cross-verify | 3 | false | 0 | 0 | high | **pending** |
| run-013 | Documents completeness script | 4 | false | 0 | 0 | high | **pending** |
| run-014 | Sync-check CLAIM docs | 4 | false | 0 | 0 | high | **pending** |

---

## Per-Run Review Notes

### run-001 — Contract Consistency (Task A)
**Key change**: docs/rule-extraction-table.md R-003 HANDSHAKE sub-cases; docs/completion-claim-policy.md token normalisation; docs/fsm-contract.md enforcement sections added.
**Reviewer check**: Was the R-003 HANDSHAKE sub-case split accurate? Did completion-claim-policy.md tokens match contract.yaml?
**Files**: [run-record](runs/run-001/run-record.yaml) | [scorecard](runs/run-001/scorecard.yaml) | [diff](runs/run-001/diff.patch)

### run-002 — Rule Pack Normalization (Task B) ⚠️ medium confidence
**Key change**: Added rule_id/severity/rationale to all 19 governance/rules/ files; created RULE_INDEX.md.
**Data quality note**: Original run-record had placeholder zeros — corrected in audit 2026-05-08 from diff.patch evidence (+57/-4 lines). See `data_quality_note` field.
**Reviewer check**: Are the rule_id assignments in migration-note.md consistent with what's in the files?
**Files**: [run-record](runs/run-002/run-record.yaml) | [scorecard](runs/run-002/scorecard.yaml) | [diff](runs/run-002/diff.patch) | [migration-note](runs/run-002/migration-note.md)

### run-003 — Failure-State Boundary (Task C)
**Key change**: New docs/failure-state-reviewer-template.md + docs/negative-claim-list.md (NC-001~008).
**Reviewer check**: Are NC-001~008 non-overlapping and complete? Does the template correctly enforce no single-case escalation?
**Files**: [run-record](runs/run-003/run-record.yaml) | [scorecard](runs/run-003/scorecard.yaml) | [diff](runs/run-003/diff.patch)

### run-004 — Traceability Contract (Task D)
**Key change**: New docs/traceability-contract.md (schema + TRC-001~005) + docs/traceability-examples.md (TC-001 PASS, TC-BAD-001 FAIL).
**Reviewer check**: Does TC-BAD-001 correctly demonstrate all TRC violations? Is the schema minimally sufficient?
**Files**: [run-record](runs/run-004/run-record.yaml) | [scorecard](runs/run-004/scorecard.yaml) | [diff](runs/run-004/diff.patch)

### run-005 — Cross-verify A-rerun
**Key change**: C-004: HANDSHAKE allowed_if_missing sub-case annotation in contract.yaml; C-005: 5 new docs registered.
**Reviewer check**: Do the sub-case annotations in governance_rules match the rule-extraction-table.md R-003 fix from run-001?
**Files**: [run-record](runs/run-005/run-record.yaml) | [scorecard](runs/run-005/scorecard.yaml) | [diff](runs/run-005/diff.patch)

### run-006 — FSM Governance Backfill
**Key change**: contract.yaml: +3 precondition_effects, +2 must_not_assume, +1 FSM_CONTRACT_REQUIRED governance_rule, +1 completion_claim_disallow entry.
**Reviewer check**: Are the FSM precondition token names consistent with fsm-contract.md enforcement sections?
**Files**: [run-record](runs/run-006/run-record.yaml) | [scorecard](runs/run-006/scorecard.yaml) | [diff](runs/run-006/diff.patch)

### run-007 — gate_policy.yaml Add
**Key change**: New governance/gate_policy.yaml: fail_mode:audit, skip_test_result_check:true, hook_coverage_tier:C.
**Reviewer check**: Are the policy choices correct for a documentation repo with no automated test suite?
**Files**: [run-record](runs/run-007/run-record.yaml) | [scorecard](runs/run-007/scorecard.yaml) | [diff](runs/run-007/diff.patch)

### run-008 — Traceability Cross-verify (C replay)
**Key change**: NC-006 added to TC-BAD-001 table; cross-references added between traceability-contract.md and failure-state template.
**Reviewer check**: Is NC-006 ("ready for integration" = scope expansion) a legitimate addition?
**Files**: [run-record](runs/run-008/run-record.yaml) | [scorecard](runs/run-008/scorecard.yaml) | [diff](runs/run-008/diff.patch)

### run-009 — Validator Smoke (observation only)
**Key change**: None. V-009-01 coverage gap (FSM not in validator) identified.
**Reviewer check**: Were S-009-A/B/C correct? Is V-009-01 fairly characterised as advisory?
**Files**: [run-record](runs/run-009/run-record.yaml) | [scorecard](runs/run-009/scorecard.yaml) | [diff](runs/run-009/diff.patch)

### run-010 — Validator FSM Extension
**Key change**: validators/precondition_gate_validator.py: +4 regex patterns, +Rule 3 FSM gate logic, +FSM_CONTRACT_REQUIRED to rule_ids.
**Reviewer check**: Do S-010-A/B/C correctly test the FSM gate? Is LIM-010-01 (semantic negation) an acceptable known limitation?
**Files**: [run-record](runs/run-010/run-record.yaml) | [scorecard](runs/run-010/scorecard.yaml) | [diff](runs/run-010/diff.patch)

### run-011 — Contract Sync-Check Doc
**Key change**: New docs/contract-sync-check.md; contract.yaml: +2 FSM rule_sources, +1 document entry.
**Reviewer check**: Is the 7-item sync-check process complete and unambiguous? Are the FSM rule_source page references accurate?
**Files**: [run-record](runs/run-011/run-record.yaml) | [scorecard](runs/run-011/scorecard.yaml) | [diff](runs/run-011/diff.patch)

### run-012 — Round 3 Cross-verify
**Key change**: contract.yaml: +9 documents (CLAIM_BOUNDARY, CLAIM_ENFORCEMENT, 7 governance/*.md files).
**Reviewer check**: Are all 9 added files legitimate governed documents (not tooling or test artifacts)?
**Files**: [run-record](runs/run-012/run-record.yaml) | [scorecard](runs/run-012/scorecard.yaml) | [diff](runs/run-012/diff.patch)

### run-013 — Documents Completeness Script
**Key change**: New validators/check_documents.py; smoke pass 51/51.
**Reviewer check**: Are the GOVERNED_GLOBS and EXEMPT_PREFIXES correct? Does the two-way check cover all relevant cases?
**Files**: [run-record](runs/run-013/run-record.yaml) | [scorecard](runs/run-013/scorecard.yaml) | [diff](runs/run-013/diff.patch)

### run-014 — Sync-Check CLAIM Docs
**Key change**: docs/contract-sync-check.md: CLAIM_BOUNDARY + CLAIM_ENFORCEMENT added to Supporting Docs; vocabulary note table added.
**Reviewer check**: Is the vocabulary distinction between the two claim_level systems correctly characterised?
**Files**: [run-record](runs/run-014/run-record.yaml) | [scorecard](runs/run-014/scorecard.yaml) | [diff](runs/run-014/diff.patch)

---

## How to Fill Reviewer Decisions

Edit the `scorecard.yaml` for each run. Change:

```yaml
disposition:
  reviewer_decision: null        # ← change to one of: accept | accept_with_note | reject
  round_note: >                  # keep existing
    ...
```

For `accept_with_note` or `reject`, also fill `one_line_note` in run-record:

```yaml
reviewer:
  disposition: ""                # ← "accept_with_note" or "reject"
  one_line_note: ""              # ← brief note
```

After all decisions are filled, this dashboard should be re-generated (or the table updated manually).
