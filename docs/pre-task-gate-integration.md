# Pre-Task Gate Integration (Minimal Executable Slice)

This slice executes only pre-task-appropriate rules:

- reset definition completeness
- interface/handshake definition completeness

It intentionally excludes assignment-semantic ambiguity from pre-task gating because that signal is usually output-review dependent.

## Validator

- `validators/precondition_gate_validator.py`

Output fields:

- `ok`
- `missing_preconditions`
- `recommended_mode`
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

This keeps enforcement incremental and avoids immediate hard-stop coupling.

## Smoke Cases

Run:

```bash
python scripts/precondition_gate_smoke.py
```

Coverage:

- missing reset definition -> `restrict_codegen`
- missing handshake protocol semantics -> `allow_analysis_only`
- sufficiently defined task -> `allow_draft_with_assumptions` (allow-codegen contrast)
