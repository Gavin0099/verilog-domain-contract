# Synthesizable vs Testbench Contract

## Required Task Input

Task must declare one of:

- synthesizable RTL
- testbench-only artifact
- mixed scope with explicit separation

## Operational Constraints

- do not emit testbench-only constructs into synthesizable modules
- do not emit synthesizable completion claims when scope is testbench-only
- if scope is ambiguous, downgrade to analysis or draft with explicit assumptions

## Evidence Expectation

Output must include a scope disclosure line:

- `scope: synthesizable`
- `scope: testbench`
- `scope: mixed (explicit partitioning provided)`
