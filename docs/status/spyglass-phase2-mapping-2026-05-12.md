# SpyGlass -> Contract/Gate C Mapping (Phase 2 Extension)

## Purpose
This mapping defines how SpyGlass evidence can strengthen Phase 2 observability
without changing core governance decisions.

## Mapping Table
| SpyGlass signal | Contract/Gate C target | Interpretation | Action |
|---|---|---|---|
| Unconstrained clock/reset or unconstrained top ports | `clock/reset precondition completeness` | Preconditions are incomplete | Keep downgrade/stop behavior |
| Unsynchronized crossing violations | `cdc_strategy_present_when_multi_clock_implied` | CDC intent exists but strategy evidence is insufficient | Require explicit CDC strategy disclosure |
| Reset synchronization violations | `cdc_synchronizer_scheme_defined` | Synchronizer scheme may be missing or inadequate | Block implementation claim escalation |
| Convergence/glitch families | `tool_evidence_completeness` | Observed evidence coverage is incomplete | Mark `partial` until resolved |
| Waiver exists with rationale and scope | `tool_evidence_completeness` | Controlled exception with traceability | Can remain `complete` or `partial` based on residual governance gaps |
| Waiver exists without rationale | `tool_evidence_completeness` | Governance traceability gap | Force `partial` |
| No usable SpyGlass evidence for run/window | `tool_evidence_completeness` | Optional tool evidence missing | Mark `absent` (non-blocking for Gate C baseline) |

## Classification for `tool_evidence_completeness`
- `complete`: evidence present, critical constraints covered, no ungoverned waivers.
- `partial`: evidence present, but unresolved constraints/findings or weak waivers.
- `absent`: no usable evidence attached.
- `unknown`: evidence attached but parsing/classification confidence is low.

## Guardrails
1. Do not treat tool-clean outputs as `implementation_complete`.
2. Do not relax missing-precondition downgrade/stop semantics.
3. Keep vendor-specific logic in extension/profile files only.
