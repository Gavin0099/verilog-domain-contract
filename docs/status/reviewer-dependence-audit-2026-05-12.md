# Reviewer Dependence Audit (Observability Anti-Drift)

Date: 2026-05-12
Cadence: per Gate C window

## Audit Questions
1. Did reviewer treat tool evidence as supplemental context, not a gate authority?
2. Did reviewer explicitly check missing preconditions before reading tool completeness?
3. Did reviewer avoid using "tool clean" as implementation evidence?
4. Did reviewer document when completeness is `unknown` due to missing field fallback?
5. Did reviewer avoid cross-lane capability claims from completeness distribution?

## Drift Indicators
- Reviewer decision text frequently references completeness rank without precondition checks.
- Downgrade/stop decisions decrease while precondition gaps remain.
- Completion claims increase despite unresolved missing-precondition records.

## Required Mitigation on Drift
1. Re-state boundary sentence in review summary.
2. Re-run checklist with precondition-first ordering.
3. Flag session for governance review.
4. Keep Gate C pass/fail independent from completeness metrics.
