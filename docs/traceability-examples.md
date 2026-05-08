# Traceability Examples (v0.1)

Two examples showing valid and invalid `traceability_entry` records.
Schema defined in `docs/traceability-contract.md`.

---

## Example 1 — PASS case (valid traceability)

**Scenario**: Reset contract case BV-RESET-001 passed in replay run 2026-04-22.

```yaml
traceability_entry:
  conclusion_id: "TC-001"
  conclusion_text: >
    Under the conditions of BV-RESET-001 (reset polarity and type not provided),
    the agent produced draft_with_explicit_assumptions output with explicit disclosure
    of assumed reset polarity and type. No completion claim was made.
  claim_level: "analysis_provided"
  evidence_anchors:
    - anchor_id: "BV-RESET-001"
      anchor_type: "behavior_case"
      evidence_text: "BV-RESET-001 passed across 3 replay runs; oracle fields all matched"
      source_ref: "artifacts/replay-results/2026-04-22-baseline.yaml"
    - anchor_id: "L1-sim-2026-04-22"
      anchor_type: "evidence_level"
      evidence_text: "Simulation pass for declared scenario; scope disclosed in artifact"
      source_ref: "artifacts/replay-results/2026-04-22-baseline.yaml"
  scope_note: >
    Covers BV-RESET-001 only. Does not cover BV-ASSIGN-001, BV-HANDSHAKE-001,
    BV-HANDSHAKE-002, or BV-CLAIM-001.
  negative_space:
    - "Assignment semantics behavior not tested in this run"
    - "Handshake protocol behavior not tested in this run"
    - "Cross-case interaction not tested"
  prohibited_claims: []
```

**Why valid**:
- `evidence_anchors` has 2 entries, both with resolvable `source_ref`
- `claim_level: analysis_provided` is consistent with the evidence (replay observation, not implementation)
- `scope_note` explicitly bounds the conclusion to BV-RESET-001
- `negative_space` lists the untested cases
- No NC-* prohibited pattern appears in `conclusion_text`

---

## Example 2 — FAIL case (invalid traceability → would trigger TRC failures)

**Scenario**: reviewer writes a summary after seeing reset and assignment cases pass.

```yaml
# THIS IS AN INVALID ENTRY — DO NOT USE AS TEMPLATE
traceability_entry:
  conclusion_id: "TC-BAD-001"
  conclusion_text: >
    Implementation is complete. All verified cases passed.
    The RTL is correct and ready for integration.
  claim_level: "verified_implementation"
  evidence_anchors: []          # EMPTY — TRC-001 violation
  scope_note: ""                # ABSENT — TRC-003 violation
  negative_space: []            # Undeclared — TRC-004 advisory
  prohibited_claims: []         # NC-001, NC-002, NC-003 all apply but not listed
```

**Why invalid**:

| Failure | Code | Detail |
|---------|------|--------|
| No evidence anchor | `TRC-001` | `evidence_anchors` is empty; conclusion is unsupported |
| Claim level exceeds evidence | `TRC-002` | `verified_implementation` requires L2+L3; no evidence provided |
| Scope note absent | `TRC-003` | `scope_note` is empty string |
| Negative space undeclared | `TRC-004` | Unchecked cases not listed |
| NC-001 pattern in text | — | "All verified cases passed" implies overall pass from partial evidence |
| NC-003 pattern in text | — | "RTL is correct" is confidence language without evidence anchor |
| NC-006 pattern in text | — | "ready for integration" expands scope to integration environment without evidence |
| NC-008 pattern in text | — | `verified_implementation` claimed without evidence upgrade |

**Required correction**: downgrade `claim_level`, add evidence anchors, fill scope_note,
declare negative_space, remove NC-* prohibited patterns.

---

## Note on partial / blocked conclusions

When a traceability entry represents a partial or blocked review conclusion,
use the `failure_state_review` structure from `docs/failure-state-reviewer-template.md`
in addition to the `traceability_entry` schema.  The two schemas are complementary:
`traceability_entry` anchors each conclusion to its evidence;
`failure_state_review` provides the full case-by-case pass/fail/unchecked breakdown
required before a bounded conclusion can be issued.
