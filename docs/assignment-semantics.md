# Assignment Semantics Contract

## Intent

Prevent semantic blur between combinational and sequential logic.

## Operational Constraints

- sequential state updates use non-blocking assignments in clocked processes
- combinational logic uses blocking assignments in combinational processes
- temporary variables in combinational blocks must not be presented as state
- state-transition and output logic partitioning must be explicit when FSM-like behavior exists

## Violation Signals

- mixed blocking/non-blocking updates to state register in one sequential path
- latch-prone combinational blocks from incomplete assignment intent
- code that obscures whether behavior is combinational or sequential
