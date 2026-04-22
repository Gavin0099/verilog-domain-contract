# Assignment Semantics Contract

## Semantic Requirement

### Rule

Assignment operators and process partitioning must match logic intent:

- sequential state updates -> non-blocking assignment
- combinational logic -> blocking assignment with complete assignment paths

## Risk

Syntax-valid code can still be semantically wrong when:

- blocking and non-blocking assignments are mixed on state
- combinational outputs are incompletely assigned
- combinational vs sequential intent is unclear

## Constraint on AI Behavior

If assignment intent or partitioning is unclear:

- AI must not claim implementation completion
- AI must downgrade to:
  - `analysis_only`, or
  - `draft_with_explicit_semantic_assumptions`

Enforcement effect:

- `draft_only`
- `escalate`

## Forbidden Behavior

- mixed blocking/non-blocking assignment on the same state path
- latch-prone combinational logic from incomplete assignments
- implicit interpretation of process intent without disclosure

## Required Disclosure

If draft is provided under ambiguity, AI must disclose:

- state update model
- combinational logic model
- residual semantic risk
