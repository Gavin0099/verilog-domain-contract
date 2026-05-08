# FSM Contract

## Required Disclosures

- state model intent (Moore/Mealy or equivalent behavior statement)
- chosen FSM decomposition style (one/two/three process), or "unspecified"
- illegal state handling expectation

## Must Not Assume

- state encoding scheme
- output model
- automatic illegal-state recovery behavior

## Constraint on AI Behavior

If FSM style details (state model, decomposition style, illegal state policy) are missing or unspecified:

- enforcement effect: `draft_only`, `escalate`
- allowed output: `analysis_only`, `draft_with_explicit_assumptions`

If FSM task scope is ambiguous (synthesizable vs testbench-only unclear):

- enforcement effect: `draft_only`
- allowed output: `analysis_only`, or `draft_with_explicit_assumptions` with scope disclosure

## Forbidden Behavior

- silent state encoding selection without disclosure
- implicit assumption of single always-block FSM style
- implicit assumption of no illegal-state handling requirement

## Forbidden Claim

- `implementation_complete` without explicit state model and decomposition style disclosure
- `behaviorally_verified` without simulation or assertion evidence

## Completion Policy

Without explicit state model intent and illegal state handling definition, AI must not claim:

- `implementation_complete`
- `behaviorally_verified`
