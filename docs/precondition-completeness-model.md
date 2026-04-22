# Precondition Completeness Model (v0.1)

This model makes downgrade/stop behavior deterministic.

## Decision Inputs

- `clock_definition`
- `reset_definition`
- `interface_spec`
- `timing_expectation`
- `assignment_intent_partition`
- `verification_expectation`

## Completeness Rules

### Required

- `clock_definition`: required
- `reset_definition`: required
- `interface_spec`: required
- `assignment_intent_partition`: required for implementation claims
- `verification_expectation`: required for completion claims

### Conditionally Required

- `timing_expectation`: required when interface/control timing behavior is part of requested output

## Deterministic Action Matrix

- missing `clock_definition` -> `restrict_codegen` + `escalate`
- missing `reset_definition` -> `restrict_codegen` + `escalate`
- missing `interface_spec` -> `analysis_only`
- missing `assignment_intent_partition` -> `draft_only` + `escalate`
- missing `timing_expectation` (timing-relevant task) -> `draft_with_explicit_assumptions`
- missing `verification_expectation` -> allow draft, block completion claims

## Stop Conditions (v0.1)

- multi-clock behavior implied and CDC strategy absent -> `stop_insufficient_preconditions`

## Output Mode Mapping

- `analysis_only`: no implementation claim, no final RTL
- `draft_with_explicit_assumptions`: draft RTL allowed with assumption disclosure
- `draft_only`: draft allowed, completion claim blocked
- `restrict_codegen`: no final synthesizable implementation output
- `stop_insufficient_preconditions`: stop and request missing inputs
