# Clock / Reset Contract

## Reset Definition Requirement

### Rule

Reset behavior must be explicitly defined before generating synthesizable RTL.

Required fields:

- reset polarity (`active-high` or `active-low`)
- reset type (`synchronous` or `asynchronous`)

## Risk

If reset is implicit:

- AI may choose wrong polarity
- AI may choose sync vs async arbitrarily
- generated RTL may pass syntax checks but fail system behavior

## Constraint on AI Behavior

If reset definition is missing:

- AI must not generate final RTL implementation
- AI must not silently assume polarity or reset type

Allowed behavior:

- `analysis_only`
- `draft_with_explicit_assumptions`

Enforcement effect:

- `restrict_codegen`
- `escalate`

## Required Disclosure

If draft is provided under missing reset input, AI must disclose:

- assumed reset polarity
- assumed reset type
- risk of assumption mismatch

## Completion Policy

Without explicit reset definition, AI must not claim:

- `implementation_complete`
- `synthesizable_ready`

## Non-Equivalence Warning

Compilation, lint, or a simple simulation pass is not equivalent to reset-correct implementation.
