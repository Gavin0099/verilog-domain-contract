# SpyGlass Manifest Usage Negative Test (Advisory-Only)

Date: 2026-05-12
Validator: `scripts/validate_spyglass_manifest_usage.py`

## Test Input
File: `docs/status/spyglass-misuse-negative-sample-2026-05-12.md`
Sentence:
`tool_evidence_completeness shows Claude has better implementation quality.`

## Expected
- result: WARN
- advisory_only: true
- does_not_affect_gate_c: true
- exit code: 0

## Observed
- result: WARN
- advisory_only: true
- does_not_affect_gate_c: true
- exit_behavior: always_zero

## Conclusion
Misuse is visible, but does not become gate authority.
