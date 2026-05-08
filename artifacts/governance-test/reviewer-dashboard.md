# Governance Test Reviewer Dashboard

**Generated**: 2026-05-08 (updated Run 027)
**Total runs**: 27 (run-001 ~ run-027)
**Reviewer decisions**: 27 / 27 accepted

This document summarises every run for human review. For each run, the reviewer should:
1. Read the `round_note` in the scorecard
2. Verify the diff.patch is plausible (spot check)
3. Fill `reviewer_decision` in the scorecard (accept / accept_with_note / reject)
4. Optionally fill `one_line_note` in run-record reviewer section

---

## Quick Status Table

| Run | Task | Round | Hard Fail | Scope Viol | Claim Viol | Artifact Confidence | Reviewer Decision |
|-----|------|-------|-----------|------------|------------|--------------------|--------------------|
| run-001 | Contract consistency (A) | 1 | false | 0 | 0 | high | accept |
| run-002 | Rule normalization (B) | 1 | false | 0 | 0 | **medium** (data corrected) | accept |
| run-003 | Failure-state boundary (C) | 1 | false | 0 | 0 | high | accept |
| run-004 | Traceability contract (D) | 1 | false | 0 | 0 | high | accept |
| run-005 | Cross-verify A-rerun | 1 | false | 0 | 0 | high | accept |
| run-006 | FSM governance backfill | 2 | false | 0 | 0 | high | accept |
| run-007 | gate_policy.yaml add | 2 | false | 0 | 0 | high | accept |
| run-008 | Traceability cross-verify (C replay) | 2 | false | 0 | 0 | high | accept |
| run-009 | Validator smoke (obs-only) | 2 | false | 0 | 0 | high | accept |
| run-010 | Validator FSM extension | 3 | false | 0 | 0 | high | accept |
| run-011 | Contract sync-check doc | 3 | false | 0 | 0 | high | accept |
| run-012 | Round 3 cross-verify | 3 | false | 0 | 0 | high | accept |
| run-013 | Documents completeness script | 4 | false | 0 | 0 | high | accept |
| run-014 | Sync-check CLAIM docs | 4 | false | 0 | 0 | high | accept |
| run-015 | Reviewer dashboard (initial) | 4 | false | 0 | 0 | high | accept |
| run-016 | Round 4 cross-verify (meta) | 4 | false | 0 | 0 | high | accept |
| run-017 | Dashboard sync (meta) | 5 | false | 0 | 0 | high | accept |
| run-018 | check_advisory hook integration | 5 | false | 0 | 0 | high | accept |
| run-019 | ASSIGNMENT_SEMANTICS validator sync | 5 | false | 0 | 0 | high | accept |
| run-020 | governance/rules architecture classification | 5 | false | 0 | 0 | high | accept |
| run-021 | Dashboard sync to 20 runs (meta) | 5 | false | 0 | 0 | high | accept |
| run-022 | CDC_STRATEGY_REQUIRED full governance sync | 6 | false | 0 | 0 | high | accept |
| run-023 | Round 5-6 summary documents (meta) | 6 | false | 0 | 0 | high | accept |
| run-024 | Precondition-gate smoke artifact v2 | 6 | false | 0 | 0 | high | accept |
| run-025 | FSM explicit smoke cases PG-008/009 | 6 | false | 0 | 0 | high | accept |
| run-026 | Dashboard sync to 25 runs (meta) | 7 | false | 0 | 0 | high | accept |
| run-027 | FSM+CDC replay oracle extension BR-006/007 | 8 | false | 0 | 0 | high | accept |

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

### run-015 — Reviewer Dashboard (initial)
**Key change**: New artifacts/governance-test/reviewer-dashboard.md; 15-run review guide with per-run check questions and decision instructions.
**Reviewer check**: Do the per-run check questions target the right concerns for each run? Is the decision instruction section clear?
**Files**: [run-record](runs/run-015/run-record.yaml) | [scorecard](runs/run-015/scorecard.yaml) | [diff](runs/run-015/diff.patch)

### run-016 — Round 4 Cross-verify (meta run)
**Key change**: run-ledger.ndjson +4 entries (run-013~016); session-index.ndjson +1 entry (session-current-20260508-round4, reconstructed).
**Reviewer check**: Are the 4 ledger entries consistent with the actual run artifacts? Is session-current-20260508-round4 correctly marked `reconstructed`?
**Files**: [run-record](runs/run-016/run-record.yaml) | [scorecard](runs/run-016/scorecard.yaml) | [diff](runs/run-016/diff.patch)

### run-017 — Dashboard Sync (meta run)
**Key change**: reviewer-dashboard.md updated to 16 runs / all accept; round-004-summary.md cumulative state corrected.
**Reviewer check**: Is the updated run count (16) accurate? Are all reviewer decisions correctly reflected?
**Files**: [run-record](runs/run-017/run-record.yaml) | [scorecard](runs/run-017/scorecard.yaml) | [diff](runs/run-017/diff.patch)

### run-018 — check_advisory Hook Integration
**Key change**: scripts/check_advisory.py (non-blocking advisory wrapper); Stop hook registered in .claude/settings.json; gate_policy.yaml tier C→B.
**Reviewer check**: Does check_advisory.py correctly call check_documents() and write to artifacts/runtime/advisory/? Is exit 0 always appropriate?
**Files**: [run-record](runs/run-018/run-record.yaml) | [scorecard](runs/run-018/scorecard.yaml) | [diff](runs/run-018/diff.patch)

### run-019 — ASSIGNMENT_SEMANTICS_REQUIRED Validator Sync
**Key change**: contract.yaml +2 precondition_effects; precondition_gate_validator.py Rule 4 + 3 regex patterns; smoke PG-004/005 new; contract-sync-check.md G-019-01/02.
**Reviewer check**: Do PG-004/PG-005 correctly test the ASSIGNMENT_SEMANTICS gate? Is LIM-019-01 (narrow intent detection) acceptable?
**Files**: [run-record](runs/run-019/run-record.yaml) | [scorecard](runs/run-019/scorecard.yaml) | [diff](runs/run-019/diff.patch)

### run-020 — governance/rules Architecture Classification
**Key change**: RULE_INDEX.md rewritten with two-system classification; contract-sync-check.md D-020-01 + scope note.
**Reviewer check**: Is the two-system classification (Verilog domain vs general behavioral) correctly described? Does the scope note in contract-sync-check.md prevent future confusion?
**Files**: [run-record](runs/run-020/run-record.yaml) | [scorecard](runs/run-020/scorecard.yaml) | [diff](runs/run-020/diff.patch)

### run-021 — Dashboard Sync to 20 Runs (meta run)
**Key change**: reviewer-dashboard.md updated to 20 runs; run-017~020 rows + review notes added.
**Reviewer check**: Are run-021 row assignments and round numbers correct?
**Files**: [run-record](runs/run-021/run-record.yaml) | [scorecard](runs/run-021/scorecard.yaml) | [diff](runs/run-021/diff.patch)

### run-022 — CDC_STRATEGY_REQUIRED Full Governance Sync
**Key change**: docs/cdc-contract.md new; contract.yaml +CDC governance_rules + must_not_assume + precondition_effects + rule_sources + completion_claim_disallow; validator Rule 5 + RE_CDC_INTENT + RE_CDC_STRATEGY; smoke PG-006/007 new; sync-check gaps G-022-01~05; RULE_INDEX.md +CDC row.
**Reviewer check**: Is the CDC gate severity (restrict_codegen for missing strategy) proportionate? Is LIM-022-02 (semantic negation) acceptable?
**Files**: [run-record](runs/run-022/run-record.yaml) | [scorecard](runs/run-022/scorecard.yaml) | [diff](runs/run-022/diff.patch)

### run-023 — Round 5-6 Summary Documents (meta run)
**Key change**: round-005-summary.md (Runs 017-021 complete) + round-006-summary.md (Runs 022-025 in-progress frame) created.
**Reviewer check**: Are the cumulative state counts in round-005-summary.md accurate (21 runs, 0 hard failures)?
**Files**: [run-record](runs/run-023/run-record.yaml) | [scorecard](runs/run-023/scorecard.yaml) | [diff](runs/run-023/diff.patch)

### run-024 — Precondition-Gate Smoke Artifact v2
**Key change**: artifacts/precondition-gate/2026-05-08-smoke.json created with PG-001~007; contract.yaml documents updated.
**Reviewer check**: Does 2026-05-08-smoke.json correctly supersede 2026-04-22-smoke.json? Are rule labels accurate?
**Files**: [run-record](runs/run-024/run-record.yaml) | [scorecard](runs/run-024/scorecard.yaml) | [diff](runs/run-024/diff.patch)

### run-025 — FSM Explicit Smoke Cases PG-008 and PG-009
**Key change**: scripts/precondition_gate_smoke.py: PG-008 (FSM missing all) + PG-009 (FSM defined); smoke 9/9 PASS; 2026-05-08-smoke.json updated to v3.
**Reviewer check**: Does PG-008 correctly trigger Rule 3 with all 3 FSM preconditions missing? Does LIM-025-01 (semantic negation) match the class of LIM-010-01 and LIM-019-01?
**Files**: [run-record](runs/run-025/run-record.yaml) | [scorecard](runs/run-025/scorecard.yaml) | [diff](runs/run-025/diff.patch)

### run-026 — Dashboard Sync to 25 Runs
**Key change**: reviewer-dashboard.md synced 20→25 runs; run-021~025 rows + review notes added; round numbers corrected for run-019/020 (5, not 6).
**Reviewer check**: Are round numbers for all 25 runs consistent with the ledger? Are all 25 reviewer decisions accept?
**Files**: [run-record](runs/run-026/run-record.yaml) | [scorecard](runs/run-026/scorecard.yaml) | [diff](runs/run-026/diff.patch)

### run-027 — FSM+CDC Replay Oracle Extension (BR-006 and BR-007)
**Key change**: docs/behavioral-replay-oracle.md: +BR-006 (FSM_CONTRACT_REQUIRED missing) +BR-007 (CDC_STRATEGY_REQUIRED missing); 2026-05-08-replay-extended.yaml created (BR-001~007, 7/7 pass); contract.yaml documents updated.
**Reviewer check**: Do BR-006/007 oracle criteria align with PG-008/PG-006 smoke cases? Are forbidden_claims consistent with completion_claim_disallow entries in contract.yaml?
**Files**: [run-record](runs/run-027/run-record.yaml) | [scorecard](runs/run-027/scorecard.yaml) | [diff](runs/run-027/diff.patch)

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
