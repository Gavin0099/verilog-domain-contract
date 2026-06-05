# Completion Claim Policy

## Allowed Claim Levels

- `analysis_provided`
- `draft_rtl_provided`
- `candidate_implementation_provided`

## Restricted Claim

- `verified_implementation`

`verified_implementation` is disallowed unless evidence explicitly covers required behavior and stated verification scope.
Evidence requirements per claim level are defined in `docs/completion-evidence-levels.md`.

Missing required or conditional preconditions lower the maximum claim ceiling:

- missing reset, handshake, FSM, or CDC required inputs -> no `implementation_complete`
- missing CDC strategy under multi-clock intent -> no `verified_implementation`
- L0 compile or lint evidence does not override missing preconditions
- `verified_implementation` requires both required preconditions satisfied and evidence at `L2` + `L3`

## Mandatory Output Fields

- assumptions made
- missing preconditions
- verification performed
- unresolved risks
- claim level
