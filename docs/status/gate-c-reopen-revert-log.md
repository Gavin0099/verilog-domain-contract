# Gate C — Reopen/Revert Event Log

**Purpose**: Track post-decision reopen and revert events per run.
**Update rule**: Append an event row whenever a run is reopened or reverted AFTER initial decision.
**Never modify**: historical event rows.

## Event Log

| event_date | event_type | run_id | lane | original_decision | reason | resolution |
|------------|------------|--------|------|------------------|--------|------------|
| — | — | — | — | — | — | — |

*(No events recorded as of 2026-05-11. All runs 028–050 accepted with no reopen/revert.)*

## Event Type Definitions

| type | definition |
|------|------------|
| `reopen` | Run re-enters review after initial `accept` decision (e.g., late quality concern discovered) |
| `revert` | Previously accepted run changes are rolled back due to quality or safety concerns |

## Window Aggregate (run-028..run-039, Phase 1)

| Metric | Value |
|--------|-------|
| reopen_count | 0 |
| revert_count | 0 |
| total_changes | 12 |
| reopen_revert_rate | 0.0 |

## Window Aggregate (run-040..run-050, Phase 2)

| Metric | Value |
|--------|-------|
| reopen_count | 0 |
| revert_count | 0 |
| total_changes | 11 |
| reopen_revert_rate | 0.0 |

## Combined Aggregate (run-028..run-050, all Claude Phase 1+2)

| Metric | Value |
|--------|-------|
| reopen_count | 0 |
| revert_count | 0 |
| total_changes | 23 |
| reopen_revert_rate | 0.0 |

## Append Instructions

When a reopen or revert event occurs:
1. Add a row with: event_date (UTC), event_type, run_id, lane, original_decision, reason (short), resolution (once known).
2. Update the Window Aggregate section at the bottom of the current window log.
3. If `reopen_revert_rate` increases for 2 consecutive windows, trigger Gate C `pause` per plan §5.
