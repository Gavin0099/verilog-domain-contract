# Rule Pack Index

Normalized rule table. Each entry maps to a rule file under `governance/rules/`.
Format version: v1.0 (normalized 2026-05-08, classified 2026-05-08 Run 020)

---

## Two Distinct Rule Systems in This Repo

This repo contains **two independent rule systems** with different scopes and enforcement mechanisms:

### 1. Verilog Domain Contract Rules (contract.yaml)

Defined in `contract.yaml` → `governance_rules`. Enforced by
`validators/precondition_gate_validator.py`. Documented in `docs/` leaf docs.

| Rule ID | Leaf Doc | Validator Rule |
|---------|----------|---------------|
| `RESET_DEFINITION_REQUIRED` | `docs/clock-reset-contract.md` | Rule 1 |
| `ASSIGNMENT_SEMANTICS_REQUIRED` | `docs/assignment-semantics.md` | Rule 4 |
| `HANDSHAKE_TIMING_DEFINITION_REQUIRED` | `docs/handshake-contract.md` | Rule 2 |
| `FSM_CONTRACT_REQUIRED` | `docs/fsm-contract.md` | Rule 3 |

These rules are **RTL/Verilog-specific semantic constraints**. They govern what
preconditions an AI must have before attempting implementation claims.
The sync-check process (`docs/contract-sync-check.md`) applies to this system only.

### 2. General AI Behavioral Rules (governance/rules/)

Defined in `governance/rules/` subdirectories. Listed in the table below.
These are **cross-domain behavioral constraints** applicable to any AI task in this
workspace — not Verilog-specific. They were inherited from the ai-governance-framework
general rule pack and normalized in Run 002.

These rules do **not** appear in `contract.yaml` `governance_rules` and are **not**
subject to the contract sync-check process. They are enforced at the AGENTS.md /
behavioral guidance level, not via the precondition_gate_validator.

---

## Severity Vocabulary

| Severity | Meaning |
|----------|---------|
| `hard-stop` | Violation blocks task completion; reviewer must explicitly sign off on exception |
| `advisory` | Strong behavioral constraint; violation requires explicit rationale |
| `informational` | Style / process guidance; no blocking effect |

---

## General AI Behavioral Rules (Cross-Domain)

| rule_id | severity | pack | file | rationale |
|---------|----------|------|------|-----------|
| `CMN-001` | `advisory` | common | `common/core.md` | Baseline task scope and escalation discipline |
| `REF-001` | `advisory` | refactor | `refactor/behavior_lock.md` | Guards observable behavior from silent change under refactor framing |
| `REF-002` | `advisory` | refactor | `refactor/boundary_safety.md` | Prevents boundary crossings hidden inside refactor scope |
| `REF-ERROR-001` | `hard-stop` | refactor | `refactor/error_path_coverage.md` | Ensures error path traceability is preserved across refactor changes |
| `REF-003` | `advisory` | refactor | `refactor/interface_stability.md` | Protects external contract stability when internal structure changes |
| `REF-004` | `hard-stop` | refactor | `refactor/no_partial_cleanup.md` | Prevents resource leaks caused by partial cleanup in failure paths |
| `REF-005` | `advisory` | refactor | `refactor/required_regression_tests.md` | Requires verifiable regression evidence, not just a passing summary |
| `KDRV-001` | `hard-stop` | kernel-driver | `kernel-driver/irql.md` | Prevents IRQL-unsafe operations that cause system crashes |
| `KDRV-002` | `hard-stop` | kernel-driver | `kernel-driver/cleanup-unwind.md` | Requires symmetric unwind in all failure and unload paths |
| `KDRV-003` | `hard-stop` | kernel-driver | `kernel-driver/memory-boundary.md` | Treats external memory as hostile input requiring validation |
| `GLHUB-001` | `hard-stop` | gl-hub-vendor-cmd | `gl-hub-vendor-cmd/spec-truth.md` | Requires spec truth verification before any vendor command action |
| `AVL-001` | `advisory` | avalonia | `avalonia/ui_thread.md` | Enforces UI thread affinity for control mutations |
| `AVL-002` | `advisory` | avalonia | `avalonia/viewmodel_boundary.md` | Prevents ViewModel becoming an unbounded I/O integration layer |
| `CPP-001` | `advisory` | cpp | `cpp/build_boundary.md` | Prevents hidden coupling via include path boundary violations |
| `CSH-001` | `advisory` | csharp | `csharp/native_boundary.md` | Isolates native interop behind explicit adapter boundaries |
| `CSH-002` | `advisory` | csharp | `csharp/threading.md` | Prevents cross-thread UI mutation without synchronization strategy |
| `PY-001` | `informational` | python | `python/coding.md` | Baseline Python style, testability, and dependency discipline |
| `SWT-001` | `advisory` | swift | `swift/concurrency.md` | Enforces actor/thread boundary for Swift UI state |
| `SWT-002` | `advisory` | swift | `swift/native_interop.md` | Isolates native platform API behind explicit boundaries |

## Coverage Summary

| severity | count |
|----------|-------|
| `hard-stop` | 6 |
| `advisory` | 12 |
| `informational` | 1 |
| **total** | **19** |
