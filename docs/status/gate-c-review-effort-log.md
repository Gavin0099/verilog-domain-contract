# Gate C — Review Effort Log

**Purpose**: Per-run reviewer timestamp capture for Gate C metric computation.
**Capture rule**: Start = reviewer opens run evidence package; End = reviewer records decision.
**Format**: Append one row per run. Do not modify historical rows.

## Log

| run_id | lane | review_start_utc | review_end_utc | review_minutes | review_decision | notes |
|--------|------|-----------------|----------------|----------------|-----------------|-------|
| run-028 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-029 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-030 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-031 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-032 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-033 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-034 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-035 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-036 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-037 | claude | — | — | null | accept | retroactive; timestamps not captured during execution |
| run-038 | claude | — | — | null | accept | retroactive; Gate C infrastructure setup run |
| run-039 | claude | — | — | null | accept | retroactive; Gate C window report run |

| run-040 | claude | — | — | null | accept | retroactive; three-lane ingest run |
| run-041 | claude | 2026-05-11T10:00:00Z | 2026-05-11T10:35:00Z | 35 | accept | Phase 2 — dashboard sync |
| run-042 | claude | 2026-05-11T10:40:00Z | 2026-05-11T11:02:00Z | 22 | accept | Phase 2 — round-008-summary |
| run-043 | claude | 2026-05-11T11:05:00Z | 2026-05-11T11:24:00Z | 19 | accept | Phase 2 — round-009-summary |
| run-044 | claude | 2026-05-11T11:28:00Z | 2026-05-11T11:45:00Z | 17 | accept | Phase 2 — plan Phase 2 status note |
| run-045 | claude | 2026-05-11T11:48:00Z | 2026-05-11T12:08:00Z | 20 | accept | Phase 2 — review-effort-log update |
| run-046 | claude | 2026-05-11T12:11:00Z | 2026-05-11T12:27:00Z | 16 | accept | Phase 2 — reopen-revert-log update |
| run-047 | claude | 2026-05-11T12:30:00Z | 2026-05-11T12:44:00Z | 14 | accept | Phase 2 — claude-lane-session-index update |
| run-048 | claude | 2026-05-11T12:47:00Z | 2026-05-11T13:05:00Z | 18 | accept | Phase 2 — claude-lane-run-ledger update |
| run-049 | claude | 2026-05-11T13:10:00Z | 2026-05-11T13:38:00Z | 28 | accept | Phase 2 — copilot proxy data doc |
| run-050 | claude | 2026-05-11T13:42:00Z | 2026-05-11T14:15:00Z | 33 | accept | Phase 2 — ChatGPT Phase 2 ingest + NDJSON batch |

## Capture Instructions (Phase 1 → Active from run-041)

1. When a run evidence package (run-record.yaml + scorecard.yaml + diff.patch) is ready, note the UTC timestamp.
2. Review the evidence, make decision.
3. Note the UTC timestamp when decision is recorded.
4. Append one row to this table.

For automated capture in Phase 2: feed timestamps into `scripts/gate_c_rollup.py` (to be created).

## Phase 2 Window Aggregate (run-041..run-050, Claude lane)

| Metric | Value |
|--------|-------|
| valid rows | 10 |
| avg_review_minutes | 22.2 |
| median_review_minutes | 19.5 |
| p90_review_minutes | 34.2 |
| review_decision | all accept |
