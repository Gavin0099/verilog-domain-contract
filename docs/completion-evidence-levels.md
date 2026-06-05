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

## Evidence Lifecycle Policy

Evidence anchors from a previous session or run remain valid for `claim_level` assessment only when:

1. The governed scope has not changed (same module, same rule, same precondition set)
2. The evidence artifact still resolves (source_ref points to an existing, unchanged file)
3. No governance rule has been updated that changes the evaluation criteria for that evidence type

If any condition fails, the evidence is classified as `stale_evidence` and must be re-collected
or the claim level must be downgraded.

`stale_evidence` treatment:
- evidence_quality degrades to `weak` in `epistemic-decision-policy` scoring
- forces `need_more_info` outcome under high epistemic risk
- blocks `verified_implementation` claim; allows downgrade to `candidate_implementation_provided`

## Cross-Session Non-Equivalence Warning

Evidence collected in session A does not automatically transfer to session B. A session boundary
is an evidence lifecycle boundary unless the artifact and scope are explicitly carried forward
and all three lifecycle conditions above are confirmed.

Implicit evidence transfer is a `stale_evidence` risk and must be treated as `unknown` premise
under `docs/epistemic-decision-policy.md`.

## Forbidden Claim Conditions

- no evidence level stated
- evidence stated but scope not disclosed
- missing required preconditions while claiming `verified_implementation`
- using evidence from a prior session without confirming lifecycle conditions above
