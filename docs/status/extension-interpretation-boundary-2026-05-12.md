# Extension Interpretation Boundary (Tool Evidence Completeness)

Date: 2026-05-12
Scope: SpyGlass evidence extension used in Gate C Phase 2 observability.

## Boundary
`tool_evidence_completeness` is an observability field only.
It is not an authority signal.

## Prohibited Interpretations
1. Do not use `complete > partial > absent > unknown` as a quality ranking.
2. Do not use completeness as a proxy for implementation correctness.
3. Do not use completeness as a proxy for autonomous claim eligibility.
4. Do not use tool-clean outcomes to upgrade completion claims.

## Governance Invariants
1. Core governance semantics remain closed.
2. Missing precondition handling remains: downgrade/stop.
3. Extension observability remains open and non-gating by default.

Tool evidence completeness improves reviewer visibility, but does not by itself upgrade implementation completeness or override missing-precondition downgrade/stop semantics.
