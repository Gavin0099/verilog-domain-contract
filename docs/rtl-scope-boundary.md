# RTL Scope Boundary

## Intent

Define what this contract governs and what it does not.

## In Scope

- synthesizable RTL intent and constraints
- assumptions required before code generation
- boundaries for claimable output states
- reviewable risk disclosures

## Out of Scope

- full language tutorial content
- vendor flow specifics
- end-to-end implementation proof

## Operational Rule

When a task request mixes domain contract concerns with broad tutorial requests, prioritize contract behavior:

1. identify required preconditions
2. classify missing inputs
3. constrain permitted output level
