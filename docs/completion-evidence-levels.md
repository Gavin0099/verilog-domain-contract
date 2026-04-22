# Completion Evidence Levels (v0.1)

This model defines what evidence is required for each claim level.

## Evidence Levels

### L0: `syntax_valid`

- definition: source parses/compiles
- non-equivalence warning: not functional correctness

### L1: `sim_passed`

- definition: simulation pass exists for declared scenarios
- minimum disclosure:
  - scenario scope
  - uncovered scenarios
- non-equivalence warning: does not imply integration correctness

### L2: `waveform_verified`

- definition: waveform-level checks performed against stated expectations
- minimum disclosure:
  - checked signals
  - observation window
  - acceptance criteria

### L3: `assertion_checked`

- definition: assertion/property checks run for declared behaviors
- minimum disclosure:
  - assertion scope
  - pass/fail summary
  - unproven/uncovered assertions

## Claim Policy Mapping

- `analysis_provided`: no evidence requirement
- `draft_rtl_provided`: L0 optional, assumptions mandatory when preconditions missing
- `candidate_implementation_provided`: L0 recommended, L1 preferred
- `verified_implementation`: requires at least L2 + L3 for declared critical behaviors

## Forbidden Claim Conditions

- no evidence level stated
- evidence stated but scope not disclosed
- missing required preconditions while claiming `verified_implementation`
