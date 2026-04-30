# CLAIM_BOUNDARY

## Purpose
Define the maximum claim posture allowed by current evidence.

## Boundary Rules
- Claims must not exceed evidence scope.
- Strong wording such as "proven", "production-ready", or equivalent is disallowed unless explicitly backed by higher-tier evidence.
- If required preconditions are missing, enforcement scenarios are not executable.

## Required Preconditions
- docs/CLAIM_BOUNDARY.md exists.
- docs/CLAIM_ENFORCEMENT_MINIMAL_SPEC.md exists.

## Enforcement Outcome Mapping
- Preconditions met + bounded claim -> claim_level=bounded_support, semantic_drift_risk=false.
- Stronger claim with same evidence -> claim_level=stronger_than_allowed, semantic_drift_risk=true.
- Same evidence posture escalation -> semantic_drift_risk=true.
