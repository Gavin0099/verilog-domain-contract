# CDC Strategy Contract

## CDC Strategy Requirement

### Rule

When a multi-clock domain design is implied, the clock domain crossing (CDC) strategy
must be explicitly defined before generating synthesizable RTL.

Required fields:

- clock domain boundary map (which signals cross which domains)
- synchronization scheme (two-flop synchronizer, FIFO-based crossing, gray-code FIFO, etc.)
- metastability mitigation approach

## Risk

If CDC strategy is implicit:

- AI may generate RTL with unprotected clock domain crossings
- AI may silently assume all flops are in the same clock domain
- Generated RTL may pass lint but produce metastability or functional failures in silicon
- Derived clocks may be treated as synchronous to the source clock without disclosure

## Constraint on AI Behavior

If a multi-clock domain task is detected but CDC strategy is missing:

- AI must not generate implementation-level RTL for crossing signals
- AI must not silently assume a single clock domain
- AI must not assume derived clocks are inherently safe to cross without synchronizers

Allowed behavior:

- `analysis_only`
- `draft_with_explicit_cdc_assumptions` (with full boundary and strategy disclosure)

Enforcement effect:

- `stop_insufficient_preconditions`
- `escalate`

## Forbidden Behavior

- implicit single-clock-domain assumption when multiple clocks are mentioned
- silent clock domain boundary crossing without declared synchronizer
- treating derived clock as synchronous to source without explicit derivation disclosure
- assuming metastability-free crossing without declared synchronizer strategy

## Required Disclosure

If draft is provided under missing CDC input, AI must disclose:

- assumed clock domain boundary map
- assumed synchronization scheme
- metastability risk acknowledgment
- which crossing signals are affected

## Completion Policy

Without explicit CDC strategy definition, AI must not claim:

- `implementation_complete`
- `verified_implementation`

## Non-Equivalence Warning

Lint, simulation with a single-clock testbench, or synthesis without CDC constraints is not
equivalent to CDC-correct implementation. Metastability failures are typically not visible
in functional simulation.
