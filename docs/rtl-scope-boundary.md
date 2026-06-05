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

## Governance Authority

RTL precondition claims are governed by `contract.yaml` `governance_rules` (the 5 Verilog domain rules:
RESET, ASSIGNMENT, HANDSHAKE, FSM, CDC). General behavioral discipline such as scope enforcement,
escalation, traceability, and refactor boundaries is governed by `governance/rules/` (19 cross-domain behavioral rules).

These are two distinct systems operating at different levels. See `governance/rules/RULE_INDEX.md`
section `Authority Resolution Policy` for the resolution policy when both systems apply to the same task.
