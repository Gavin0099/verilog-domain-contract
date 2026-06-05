# Governance Closeout Summary

## Overall

- `schema_conformance_ok`: `true`
- `precondition_fail`: `0`
- `replay_fail`: `0`
- `claim_fail`: `0`
- `claim_not_executed`: `1`

## Precondition Gate

- `suite_id`: `precondition-gate-2026-06-05`
- `execution_surface`: `validator_backed_deterministic_precondition_gate`
- `summary.total`: `20`
- `summary.pass`: `20`
- `summary.fail`: `0`
- `schema_conformance_ok`: `true`
- `coverage_summary.total_cases`: `20`
- `coverage_summary.groups.negation.count`: `12`
- `coverage_summary.groups.boundary.count`: `3`
- `coverage_summary.groups.positive.count`: `5`

## Behavioral Replay

- `suite_id`: `validator-replay-2026-06-05`
- `execution_surface`: `validator_backed_deterministic_replay`
- `summary.total`: `7`
- `summary.pass`: `7`
- `summary.fail`: `0`
- `schema_conformance_ok`: `true`
- `coverage_summary.total_cases`: `7`
- `coverage_summary.groups.precondition.count`: `5`
- `coverage_summary.groups.claim_boundary.count`: `1`
- `coverage_summary.groups.cdc.count`: `1`

## Claim Enforcement

- `suite_id`: `claim-enforcement-2026-06-05`
- `execution_surface`: `validator_backed_deterministic_claim_enforcement`
- `summary.total`: `7`
- `summary.pass`: `6`
- `summary.fail`: `0`
- `summary.not_executed`: `1`
- `schema_conformance_ok`: `true`
- `coverage_summary.total_cases`: `7`
- `coverage_summary.groups.baseline.count`: `1`
- `coverage_summary.groups.drift.count`: `2`
- `coverage_summary.groups.boundary.count`: `3`
- `coverage_summary.groups.blocked.count`: `1`

## Inputs

- precondition artifact: `artifacts\precondition-gate\2026-06-05-precondition-gate-suite.json`
- replay artifact: `artifacts\replay-results\2026-06-05-validator-replay.yaml`
- claim artifact: `artifacts\claim-enforcement\checker-tests\2026-06-05-claim-enforcement-suite.json`
- precondition conformance: `artifacts\schema-conformance\2026-06-05-precondition-gate-conformance.json`
- replay conformance: `artifacts\schema-conformance\2026-06-05-validator-replay-conformance.json`
- claim conformance: `artifacts\schema-conformance\2026-06-05-claim-enforcement-conformance.json`

