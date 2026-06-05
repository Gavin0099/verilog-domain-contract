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

## FSM_CONTRACT_REQUIRED

- pre-task precondition:
  - `fsm_state_model_defined`
  - `fsm_decomposition_style_declared`
  - `fsm_illegal_state_handling_defined`
- pre-task effect if missing:
  - `draft_only`
  - `escalate`
- post-task checks:
  - no implicit FSM style or illegal-state recovery behavior
  - assumptions disclosed when draft is emitted
- claim policy impact:
  - block `implementation_complete`
  - block `behaviorally_verified`

## CDC_STRATEGY_REQUIRED

- pre-task precondition:
  - `cdc_strategy_present_when_multi_clock_implied`
  - `cdc_synchronizer_scheme_defined`
- pre-task effect if missing:
  - `restrict_codegen`
  - `blocking_effect=stop_insufficient_preconditions`
  - `escalate`
- post-task checks:
  - no implicit single-clock-domain assumption
  - no silent boundary crossing without declared synchronizer scheme
  - explicit disclosure if draft is emitted under bounded CDC assumptions
- claim policy impact:
  - block `implementation_complete`
  - block `verified_implementation`
  - pre-task blocks implementation-level crossing RTL when strategy is absent

## Enforcement Gap Marker

`domain_contract_loader PASS` and `external_repo_readiness ready=True` prove contract ingestion/adoption only.

Behavior enforcement requires replay validation using:

- [behavior-validation.md](behavior-validation.md)
- [behavioral-replay-oracle.md](behavioral-replay-oracle.md)
- [precondition-completeness-model.md](precondition-completeness-model.md)
- [completion-evidence-levels.md](completion-evidence-levels.md)
- [refusal-vs-error-metrics.md](refusal-vs-error-metrics.md)

## Reviewer Closeout Surface

- reviewer checklist schema:
  - `schemas/review-checklist.yaml`
- reviewer handoff guide:
  - `docs/reviewer-handoff-guide.md`
- bundle selection rule:
  - reviewer should download the bundle that matches the review task instead of unpacking all governance artifacts
- bundle purposes:
  - `governance-replay-artifacts`: replay evidence and replay schema conformance for rule-behavior review
  - `governance-claim-artifacts`: claim-enforcement evidence and claim schema conformance for claim-boundary review
  - `governance-closeout-artifacts`: aggregate closeout JSON/markdown and closeout schema conformance for closeout review
  - `governance-reviewer-artifacts`: executable reviewer verdict, reviewer-verdict conformance, and bundle manifest for reviewer handoff
- reviewer bundle index:
  - `artifacts/closeout/<artifact-tag>-governance-bundle-manifest.json`
- aggregate closeout files:
  - `artifacts/closeout/<artifact-tag>-governance-closeout-summary.json`
  - `artifacts/closeout/<artifact-tag>-governance-closeout-summary.md`
- required backing evidence by bundle:
  - replay: `artifacts/replay-results/<artifact-tag>-validator-replay.yaml`, `artifacts/schema-conformance/<artifact-tag>-validator-replay-conformance.json`
  - claim: `artifacts/claim-enforcement/checker-tests/<artifact-tag>-claim-enforcement-suite.json`, `artifacts/schema-conformance/<artifact-tag>-claim-enforcement-conformance.json`
  - closeout: `artifacts/schema-conformance/<artifact-tag>-governance-closeout-summary-conformance.json`, `artifacts/schema-conformance/<artifact-tag>-governance-closeout-report-conformance.json`
  - reviewer: `artifacts/closeout/<artifact-tag>-reviewer-checklist-verdict.json`, `artifacts/schema-conformance/<artifact-tag>-reviewer-checklist-verdict-conformance.json`
