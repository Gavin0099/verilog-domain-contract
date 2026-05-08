# Rule Pack Index

Normalized rule table. Each entry maps to a rule file under `governance/rules/`.
Format version: v1.0 (normalized 2026-05-08)

## Severity vocabulary

| Severity | Meaning |
|----------|---------|
| `hard-stop` | Violation blocks task completion; reviewer must explicitly sign off on exception |
| `advisory` | Strong behavioral constraint; violation requires explicit rationale |
| `informational` | Style / process guidance; no blocking effect |

## Rule Table

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

## Coverage summary

| severity | count |
|----------|-------|
| `hard-stop` | 6 |
| `advisory` | 12 |
| `informational` | 1 |
| **total** | **19** |
