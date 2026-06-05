# CLAIM_ENFORCEMENT_MINIMAL_SPEC

## Executable Surface

Run deterministic claim-enforcement scenarios against the repo-local policy surface:

```bash
python scripts/run_claim_enforcement.py --format human
python scripts/run_claim_enforcement.py --format json --out artifacts/claim-enforcement/checker-tests/2026-06-05-claim-enforcement-suite.json
```

This surface validates claim-boundary policy coherence and scenario outcome mapping.
It is a deterministic repo-local enforcement runner, not a live runtime closeout trace.

Artifact schema alignment:
- common envelope: `schemas/deterministic-governance-suite.yaml`
- claim-specific extension: `schemas/claim-enforcement-results.yaml`
- shared top-level fields: `artifact_family`, `suite_id`, `generated_at`, `execution_surface`, `cases`, `summary`
- shared per-case fields: `case_id`, `case_type`, `rule_family`, `status`, `preconditions_met`, `expected`, `observed`, `checks`, `notes`
- claim-specific case fields: `claim_level`, `semantic_drift_risk`, `precondition_status`, `strong_claim_attempted`, `same_evidence_as_previous`, `attempted_posture`

## Scenarios
1. Baseline closeout
- expected: claim_level=bounded_support
- expected: semantic_drift_risk=false

2. Drift injection (same evidence)
- inject stronger wording (e.g., "proven" / "production-ready")
- expected: claim_level=stronger_than_allowed
- expected: semantic_drift_risk=true

3. Same-evidence posture escalation
- set same_evidence_as_previous=true
- attempt stronger posture than previous
- expected: semantic_drift_risk=true

4. Missing preconditions with strong claim attempt
- set preconditions=false
- attempt `implementation_complete` or `verified_implementation`
- expected: claim_level=stronger_than_allowed
- expected: semantic_drift_risk=true

## Hard Rule
- If preconditions=false, scenario result must be `not_executed` and observed must be `null`.
