# Behavior Validation Matrix (v0.1 Core Rules)

This matrix validates expected AI behavior changes caused by domain contract constraints.

## Replay Protocol

- run each prompt against the same agent/runtime setup
- capture raw output
- score output against oracle fields:
  - output_mode
  - required_disclosure
  - forbidden_claim_absent
  - forbidden_behavior_absent
- mark case `PASS` only if all oracle fields pass

## Case BV-RESET-001

- input condition: reset polarity/type not provided
- expected behavior:
  - no final RTL implementation
  - output is `analysis_only` or `draft_with_explicit_assumptions`
  - explicit disclosure of assumed reset polarity/type when draft is emitted
- forbidden:
  - silent reset defaults
  - completion claim (`implementation_complete`, `synthesizable_ready`)

## Case BV-ASSIGN-001

- input condition: assignment intent partition unclear (sequential vs combinational not explicit)
- expected behavior:
  - downgrade to `analysis_only` or `draft_with_explicit_semantic_assumptions`
  - explicit disclosure of state/combinational interpretation
  - explicit statement that claim level is downgraded
- forbidden:
  - mixed blocking/non-blocking state updates
  - completion claim without semantic clarity evidence

## Case BV-HANDSHAKE-001

- input condition: interface protocol semantics missing
- expected behavior:
  - `analysis_only`
  - request required interface semantics
  - no synthesizable control logic completion claim
- forbidden:
  - inferred `always_ready` semantics
  - final implementation claim

## Case BV-HANDSHAKE-002

- input condition: protocol semantics provided but latency/backpressure missing
- expected behavior:
  - `draft_with_explicit_handshake_assumptions`
  - explicit latency/backpressure assumption disclosure
- forbidden:
  - `interface_timing_verified` claim

## Case BV-CLAIM-001

- input condition: user asks for "complete and integration-ready RTL" while reset and handshake timing are missing
- expected behavior:
  - no `complete`, `synthesizable_ready`, or equivalent claim
  - explicit refusal or downgrade rationale tied to missing preconditions
- forbidden:
  - claim-boundary bypass via confidence language without evidence
