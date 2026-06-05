# Pre-Task Gate Integration (Minimal Executable Slice)

This slice executes the current five-rule pre-task subset:

- reset definition completeness
- interface/handshake definition completeness
- assignment semantic intent completeness
- FSM contract completeness
- CDC strategy completeness for multi-clock tasks

## Validator

- `validators/precondition_gate_validator.py`

Output fields:

- `ok`
- `missing_preconditions`
- `recommended_mode`
- `blocking_effect`
- `forbidden_claims`
- `rule_refs`

## Verdict Vocabulary (v0.1)

- `allow_analysis_only`
- `allow_draft_with_assumptions`
- `restrict_codegen`

## Pre-Task Connection Strategy

Current framework integration is done as decision input (not hard block):

1. run validator on task text
2. attach machine-readable findings to pre-task review surface
3. consume `recommended_mode` to guide downgrade behavior
4. treat `blocking_effect=stop_insufficient_preconditions` as the stronger policy signal for runtime surfaces that support explicit stop semantics

This keeps enforcement incremental and avoids immediate hard-stop coupling.

## Smoke Cases

Run:

```bash
python scripts/precondition_gate_smoke.py
```

Coverage:

- missing reset definition -> `restrict_codegen`
- missing handshake protocol semantics -> `allow_analysis_only`
- missing assignment/FSM preconditions -> `allow_draft_with_assumptions`
- missing CDC strategy or synchronizer scheme -> `restrict_codegen` plus `blocking_effect=stop_insufficient_preconditions`
- sufficiently defined task -> `allow_draft_with_assumptions` (allow-codegen contrast)
