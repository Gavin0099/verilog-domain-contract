# Governance Closeout Summary

## Overall

- `schema_conformance_ok`: `true`
- `replay_fail`: `0`
- `claim_fail`: `0`
- `claim_not_executed`: `1`

## Behavioral Replay

- `suite_id`: `validator-replay-2026-06-05`
- `execution_surface`: `validator_backed_deterministic_replay`
- `summary.total`: `7`
- `summary.pass`: `7`
- `summary.fail`: `0`
- `schema_conformance_ok`: `true`

## Claim Enforcement

- `suite_id`: `claim-enforcement-2026-06-05`
- `execution_surface`: `validator_backed_deterministic_claim_enforcement`
- `summary.total`: `4`
- `summary.pass`: `3`
- `summary.fail`: `0`
- `summary.not_executed`: `1`
- `schema_conformance_ok`: `true`

## Inputs

- replay artifact: `artifacts\replay-results\2026-06-05-validator-replay.yaml`
- claim artifact: `artifacts\claim-enforcement\checker-tests\2026-06-05-claim-enforcement-suite.json`
- replay conformance: `artifacts\schema-conformance\2026-06-05-validator-replay-conformance.json`
- claim conformance: `artifacts\schema-conformance\2026-06-05-claim-enforcement-conformance.json`

