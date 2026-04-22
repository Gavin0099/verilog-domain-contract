# Framework Surface Mapping (v0.1 Core Rules)

This note maps rule intent to governance runtime surfaces.

## RESET_DEFINITION_REQUIRED

- pre-task precondition:
  - `reset_polarity_defined`
  - `reset_type_defined`
- pre-task effect if missing:
  - `restrict_codegen`
  - `escalate`
- post-task checks:
  - assumptions explicitly disclosed when draft is emitted
  - no silent reset defaults in generated output
- claim policy impact:
  - block `implementation_complete`
  - block `synthesizable_ready`

## ASSIGNMENT_SEMANTICS_REQUIRED

- pre-task precondition:
  - `state_update_intent_defined`
  - `comb_or_seq_partition_defined`
- pre-task effect if missing:
  - `draft_only`
  - `escalate`
- post-task checks:
  - no mixed blocking/non-blocking on state path
  - combinational completeness and intent disclosure
- claim policy impact:
  - block `implementation_complete`
  - block `behaviorally_verified` without semantic clarity evidence

## HANDSHAKE_TIMING_DEFINITION_REQUIRED

- pre-task precondition:
  - `interface_protocol_semantics_defined`
  - `backpressure_behavior_defined`
  - `latency_expectation_defined`
- pre-task effect if missing:
  - if protocol missing: `analysis_only`
  - if timing/backpressure missing: `draft_only` + `escalate`
- post-task checks:
  - no implicit always-ready or one-cycle assumptions
  - assumptions disclosed when draft is emitted
- claim policy impact:
  - block `implementation_complete`
  - block `interface_timing_verified`

## Enforcement Gap Marker

`domain_contract_loader PASS` and `external_repo_readiness ready=True` prove contract ingestion/adoption only.

Behavior enforcement requires replay validation using:

- [behavior-validation.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/behavior-validation.md)
- [behavioral-replay-oracle.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/behavioral-replay-oracle.md)
