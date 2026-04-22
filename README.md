# Verilog / RTL Domain Contract Pack

This repository defines a machine-interpretable Verilog / RTL domain contract pack for integration with `ai-governance-framework`.

It is a domain boundary layer, not a generic Verilog tutorial and not a full coding standard.

## What This Repo Is For

- constrain AI behavior in RTL tasks with explicit assumptions and preconditions
- force assumption disclosure before/with code generation
- downgrade behavior when key RTL inputs are missing
- constrain completion claims unless evidence is sufficient
- support reviewer-auditable reasoning, not implicit confidence

Domain integration principle:

- extract only constraints that change AI decisions (`PRECONDITION`, `SEMANTIC_RULE`, `ASSUMPTION_RISK`, `COMPLETION_POLICY`, `VERIFICATION_REQUIREMENT`)
- reject low-value tutorial/style content that does not change governance behavior

## What This Repo Is Not For

- full Verilog or SystemVerilog language reference
- full CDC/DFT/formal/lint methodology pack
- vendor-specific synthesis/timing closure handbook
- proof of correctness

## Integration With AI Governance Framework

This repository consumes the governance runtime baseline from:

- `additional/ai-governance-framework` (git submodule)

Domain contract content in this repo is consumed by governance tooling through:

- [contract.yaml](/e:/BackUp/Git_EE/verilog-domain-contract/contract.yaml)
- [AGENTS.md](/e:/BackUp/Git_EE/verilog-domain-contract/AGENTS.md)
- [docs/](/e:/BackUp/Git_EE/verilog-domain-contract/docs)
- [docs/rule-extraction-table.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/rule-extraction-table.md)
- [docs/behavioral-replay-oracle.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/behavioral-replay-oracle.md)
- [docs/framework-surface-mapping.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/framework-surface-mapping.md)
- [docs/precondition-completeness-model.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/precondition-completeness-model.md)
- [docs/completion-evidence-levels.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/completion-evidence-levels.md)
- [docs/coverage-model.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/coverage-model.md)
- [docs/refusal-vs-error-metrics.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/refusal-vs-error-metrics.md)
- [docs/mode-volatility-note.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/mode-volatility-note.md)
- [docs/contract-format-evolution-note.md](/e:/BackUp/Git_EE/verilog-domain-contract/docs/contract-format-evolution-note.md)
- [schemas/review-checklist.yaml](/e:/BackUp/Git_EE/verilog-domain-contract/schemas/review-checklist.yaml)
- [schemas/behavioral-replay-results.yaml](/e:/BackUp/Git_EE/verilog-domain-contract/schemas/behavioral-replay-results.yaml)
- [artifacts/replay-results/2026-04-22-baseline.md](/e:/BackUp/Git_EE/verilog-domain-contract/artifacts/replay-results/2026-04-22-baseline.md)
- [artifacts/replay-results/2026-04-22-cross-run.md](/e:/BackUp/Git_EE/verilog-domain-contract/artifacts/replay-results/2026-04-22-cross-run.md)

## v0.1 Scope

Included:

- RTL scope boundary
- synthesizable vs testbench-only distinctions
- clock/reset assumption rules
- assignment semantics (blocking/non-blocking)
- FSM contract basics
- handshake/interface timing assumptions
- verification minimum expectations
- completion claim policy

Excluded:

- full CDC methodology
- formal contracts
- DFT/scan/MBIST policy
- vendor-specific directives
- full protocol packs (AXI/APB/AHB)
- power intent concerns

## Repository Structure

```text
verilog-domain-contract/
├── README.md
├── AGENTS.md
├── PLAN.md
├── contract.yaml
├── docs/
│   ├── rtl-scope-boundary.md
│   ├── synthesizable-vs-testbench.md
│   ├── clock-reset-contract.md
│   ├── assignment-semantics.md
│   ├── fsm-contract.md
│   ├── handshake-contract.md
│   ├── verification-minimums.md
│   └── completion-claim-policy.md
├── examples/
│   ├── good/
│   └── bad/
└── schemas/
    └── review-checklist.yaml
```
