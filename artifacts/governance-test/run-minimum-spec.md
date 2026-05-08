# Governance Test Run — Minimum Deliverable Specification (v1.0)

**Effective from**: 2026-05-08
**Applies to**: all governance-test runs in this repo
**Purpose**: enforce auditable closeout loop; prevent diff.patch gaps and placeholder data

---

## Hard Gate: Minimum Files Required

Every run MUST have all three files before its scorecard status can be set to anything
other than `in_progress`:

| File | Required | Notes |
|------|----------|-------|
| `run-record.yaml` | **mandatory** | See schema below |
| `scorecard.yaml` | **mandatory** | See schema below |
| `diff.patch` | **mandatory** | For observation-only runs: create with `# N/A: observation-only run` header |

A run with any of these missing is `incomplete`, not `awaiting_reviewer`.

---

## run-record.yaml: Required Fields (non-zero)

The following fields MUST NOT be left at placeholder zero:

| Field | Rule | Violation |
|-------|------|-----------|
| `change_scope_metadata.added_line_count` | Must reflect actual lines added per diff | `0` is only valid for observation-only runs |
| `change_scope_metadata.removed_line_count` | Must reflect actual lines removed | `0` is valid if nothing was removed |
| `change_scope_metadata.accepted_change_count` | Must count actual accepted changes | `0` is never valid for a code/doc run |
| `metrics.evidence_traceability` | Must be `1.0` if all changes traced, or stated lower value with reason | `0` means no evidence exists — should be `1.0` or explicit degraded value |
| `observability_only.runtime_governance_ratio` | Estimated ratio; use `null` if unknown | `0` implies measured zero — use `null` for unknown |
| `observability_only.tokens_per_reviewer_accepted_fix` | Use `null` if not measured | `0` implies measured zero |

**Data quality note**: if a run-record must be corrected after the fact, add a
`data_quality_note` field under `change_scope_metadata` explaining what was corrected
and when (e.g., `"placeholder zeros corrected in audit 2026-05-08"`).

---

## diff.patch: Accepted Formats

| Situation | Format |
|-----------|--------|
| Session commit available | Exact `git diff -u` unified diff from commit |
| Run is within same session (uncommitted) | `reconstructed-from-run-evidence` format — show key hunks with header comment |
| New file creation | `reconstructed-from-run-evidence` format — show new file name, line count, and content summary with `# new file: ...` header |
| Observation-only run (no file modifications) | Single-line `# N/A: observation-only run` with evidence method noted |
| Meta/cross-verify run (only ledger/index appends) | `reconstructed-from-run-evidence` format — show exact ndjson lines appended; label as `meta_run` in run-ledger.ndjson |

All diff.patches MUST have a header comment identifying the source method.
`summary-format` (placeholder `{...}` lines) is **not** an accepted format — use the actual line content.

---

## session-index.ndjson: Alignment Rules

Every session that executes one or more governance-test runs MUST have an entry in
`artifacts/session-index.ndjson` with:

- `session_id`: framework session ID (from runtime hook) or a `session-{date}-{label}` label if pre-instrumentation
- `closeout_status`: **semantic rules**:
  - `valid` — ONLY when the runtime hook (`session_end_hook`) actually ran and produced the entry
  - `partial` — runtime hook ran but content was incomplete (e.g., `task_intent: null`)
  - `reconstructed` — entry written manually from run-record evidence; no runtime hook involved
  - `missing` — hook fired but produced an empty/null record (original entry before correction)
- `task_intent`: brief description of what was done
- `runs`: list of run IDs executed in this session
- `work_summary`: one sentence summary (required for `valid`; recommended for `reconstructed`)

The `run-ledger.ndjson` provides the run ↔ session mapping table.

---

## Confidence Classification

Based on the above, each run can be classified:

| Class | Criteria | Usable as |
|-------|----------|-----------|
| **high-confidence** | All 3 files present; no placeholder zeros; session-index entry exists | Formal sample |
| **medium-confidence** | All 3 files present; data corrected in audit with note; session reconstructed | Observation sample |
| **low-confidence** | Missing ≥1 file OR uncorrected placeholder zeros | Background only |

---

## Run-001 through Run-012 Confidence Assessment

| Run | Class | Notes |
|-----|-------|-------|
| 001 | high-confidence | All artifacts complete |
| 002 | **medium-confidence** | Data corrected in audit 2026-05-08 (placeholder zeros → actual values) |
| 003 | high-confidence | All artifacts complete |
| 004 | high-confidence | diff.patch added in audit 2026-05-08 (new-file-summary format) |
| 005 | high-confidence | All artifacts complete |
| 006 | high-confidence | All artifacts complete |
| 007 | high-confidence | diff.patch added in audit 2026-05-08 (new-file-summary format) |
| 008 | high-confidence | diff.patch added in audit 2026-05-08 (reconstructed-from-evidence) |
| 009 | high-confidence | diff.patch added: N/A observation-only |
| 010 | high-confidence | diff.patch is exact git unified diff |
| 011 | high-confidence | diff.patch added in audit 2026-05-08 (reconstructed-from-evidence) |
| 012 | high-confidence | diff.patch added in audit 2026-05-08 (reconstructed-from-evidence) |

**Result**: 11 high-confidence, 1 medium-confidence — all usable as formal or observation samples.

---

## Forward Policy (from Run 013 onward)

1. Before closing a run, verify: `run-record.yaml` + `scorecard.yaml` + `diff.patch` all exist.
2. No placeholder zeros — if a value is unknown, use `null`.
3. For each session, update `session-index.ndjson` at session end.
4. Update `run-ledger.ndjson` with the new run entry.
5. If a run-record must be corrected, add `data_quality_note` — never silently overwrite.
