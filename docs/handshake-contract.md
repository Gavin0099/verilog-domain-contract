# Handshake / Interface Timing Contract

## Interface Definition Requirement

### Rule

Before implementation claims, interface behavior must define:

- protocol semantics (`valid/ready`, `req/ack`, or explicit equivalent)
- acceptance and backpressure behavior
- latency/timing expectation

## Risk

If these are not explicit, AI may assume:

- always-ready sink
- one-cycle acceptance
- fixed latency

These assumptions can break integration while still looking plausible in local simulation.

## Constraint on AI Behavior

If interface protocol semantics are missing:

- allowed output: `analysis_only`
- enforcement effect: `analysis_only`, `escalate`

If protocol exists but timing expectation is missing:

- allowed output: `draft_with_explicit_assumptions`
- enforcement effect: `draft_only`, `escalate`

## Forbidden Behavior

- implicit always-ready downstream assumption
- implicit one-cycle forward progress assumption
- silent fixed-latency assumption

## Required Disclosure

If draft is provided, AI must disclose:

- assumed protocol semantics
- assumed backpressure model
- assumed latency model

## Completion Policy

Without explicit protocol and timing definition, AI must not claim:

- `implementation_complete`
- `interface_timing_verified`
