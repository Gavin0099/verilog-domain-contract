# Contract Format Evolution Note

`contract.yaml` currently uses flat pipe-delimited fields for rule payloads (for example `governance_rules`, `rule_sources`).

## Current Status

- This is an ingestion-friendly v0.1 format.
- It is sufficient for loader/readiness integration in current framework tooling.

## Known Limitation

Flat strings become fragile when adding:

- multi-effect branching
- per-rule severity and confidence
- rule versioning and backward compatibility metadata
- explicit linkage to replay oracles and measured outcomes

## Policy

- Treat current encoding as `v0.1 transitional format`, not final schema.
- Preserve backward compatibility for current loader while preparing structured schema migration in a future version.

## Migration Trigger

Move to structured nested schema when any of the following becomes required:

- rule-level versioning
- machine-level conflict resolution
- automated aggregation of rule coverage and replay outcome evidence
