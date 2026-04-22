# PLAN.md
<!-- governance-baseline: overridable -->
<!-- baseline_version: 1.0.0 -->
> **最後更新**: 2026-04-22
> **Owner**: verilog-domain-contract maintainers
> **Freshness**: Sprint (7d)

## Title

Verilog / RTL Domain Contract Pack for AI Governance

## 1. Purpose

Define a machine-interpretable Verilog / RTL domain contract pack that integrates with `ai-governance-framework`.

This repo is a domain boundary layer. It is not a generic Verilog tutorial and not a full coding standard.

## 2. Primary Goal

Deliver v0.1 that:

1. defines minimal preconditions for RTL generation
2. identifies high-risk assumptions the agent must not invent
3. constrains completion claims using evidence requirements
4. is reviewable and machine-consumable

## 3. Initial Scope (v0.1)

Included:

- RTL scope boundary
- synthesizable vs testbench-only separation
- clock/reset assumption contract
- assignment semantics (blocking vs non-blocking)
- FSM basics
- handshake/interface timing assumptions
- verification minimum expectations
- completion claim policy

Excluded:

- full CDC methodology
- formal/DFT/vendor-specific policy packs
- protocol-specific packs (AXI/APB/AHB)
- power intent concerns

## 4. Milestones

### Milestone 1 - Foundation

- repository skeleton
- README.md
- AGENTS.md
- initial contract.yaml

### Milestone 2 - Core Domain Contract

- clock/reset, assignment, handshake, verification, completion-claim docs
- rules written as operational constraints

### Milestone 3 - Example Anchoring

- good and bad RTL examples mapped to contract risks

### Milestone 4 - Governance Hook Readiness

- stabilize contract.yaml
- provide machine-readable review checklist schema

## 5. Deliverables

- D1: repo skeleton
- D2: README
- D3: AGENTS.md
- D4: contract.yaml
- D5: core docs
- D6: good/bad examples
- D7: schema scaffold for review checklist

## Current Phase

- [x] Phase A: Import framework and baseline adoption
- [x] Phase B: v0.1 contract skeleton and docs
- [ ] Phase C: tighten validators and runtime mapping

## Active Sprint

- [x] add `ai-governance-framework` as submodule under `additional/`
- [x] run adoption into current repository
- [x] create v0.1 docs/examples/schemas per domain scope
- [ ] finalize precondition severity classes for runtime consumption

## Backlog

- P1: define optional severity taxonomy in `contract.yaml`
- P1: add validator script for checklist schema consistency
- P2: add project-extension guide for downstream RTL repos

## Decision Log

- 2026-04-22: keep v0.1 boundary-first; avoid expanding into general RTL tutorial
- 2026-04-22: keep CDC/protocol/vendor constraints out of v0.1 core
- 2026-04-22: classify missing critical preconditions as downgrade/stop signals

## Known Risks

- over-generalization into style-guide/tutorial content
- under-specified downgrade behavior leading to unsafe code generation
- false-authority interpretation ("contract equals proof")
