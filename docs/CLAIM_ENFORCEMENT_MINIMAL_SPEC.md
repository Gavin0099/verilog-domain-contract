# CLAIM_ENFORCEMENT_MINIMAL_SPEC

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

## Hard Rule
- If preconditions=false, scenario result must be 
ot_executed and observed must be 
ull.
