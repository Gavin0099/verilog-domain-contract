# Traceability Contract (v0.1)

Purpose: define the minimum schema that every conclusion must satisfy to be traceable
back to its supporting evidence. This is a docs/schema layer contract only.
No runtime hook is introduced.

---

## Core Requirement

Every conclusion in AI output, reviewer comment, or closeout artifact must be
traceable to at least one evidence anchor. A conclusion without an evidence anchor
is an unsupported claim and must be treated as `claim_overreach`.

---

## Minimum Traceability Schema

```yaml
traceability_entry:
  conclusion_id: ""          # unique ID for this conclusion within the artifact
  conclusion_text: ""        # exact conclusion sentence
  claim_level: ""            # analysis_provided | draft_rtl_provided |
                             # candidate_implementation_provided | verified_implementation
  evidence_anchors:          # at least one required
    - anchor_id: ""          # e.g. "BV-RESET-001", "L1-sim-run-2026-04-22", "KDRV-001"
      anchor_type: ""        # behavior_case | evidence_level | rule_id | review_checklist_item
      evidence_text: ""      # brief description of the evidence
      source_ref: ""         # file or artifact where this evidence lives
  scope_note: ""             # explicit scope limitation on this conclusion
  negative_space: []         # what is NOT covered by this evidence
  prohibited_claims: []      # NC codes from negative-claim-list.md that apply here
```

---

## Field Requirements

| Field | Required | Notes |
|-------|----------|-------|
| `conclusion_id` | yes | unique within artifact |
| `conclusion_text` | yes | verbatim; no paraphrase |
| `claim_level` | yes | must be one of the four allowed levels |
| `evidence_anchors` | yes, ≥1 | empty list = unsupported claim |
| `anchor_id` | yes per anchor | must be traceable to a known artifact or case |
| `anchor_type` | yes per anchor | see vocabulary below |
| `evidence_text` | yes per anchor | non-empty string |
| `source_ref` | yes per anchor | file path or artifact path |
| `scope_note` | yes | must be explicit; "N/A" is not acceptable |
| `negative_space` | yes | empty list only if scope is proven exhaustive |
| `prohibited_claims` | conditional | required if any NC-* pattern was avoided in drafting |

## anchor_type Vocabulary

| Value | Meaning |
|-------|---------|
| `behavior_case` | A BV-* case from `docs/behavior-validation.md` |
| `evidence_level` | L0/L1/L2/L3 from `docs/completion-evidence-levels.md` |
| `rule_id` | A rule from `governance/rules/RULE_INDEX.md` (e.g. `KDRV-001`) |
| `review_checklist_item` | An item from `schemas/review-checklist.yaml` |
| `replay_result` | A result artifact from `artifacts/replay-results/` |

---

## Validity Conditions

A `traceability_entry` is **valid** when ALL of the following hold:

1. `evidence_anchors` is non-empty
2. Each anchor's `source_ref` points to an existing artifact or document
3. `claim_level` is consistent with the minimum evidence per `docs/completion-evidence-levels.md`
4. `scope_note` is non-empty and bounds the conclusion explicitly
5. `negative_space` correctly lists unchecked behaviors (may be empty only if exhaustive coverage is proven)

A `traceability_entry` is **invalid** when ANY of the following hold:

- `evidence_anchors` is empty
- `claim_level` exceeds evidence (e.g. `verified_implementation` with only L0 evidence)
- `scope_note` is absent or set to a placeholder ("N/A", "none", "")
- conclusion text contains patterns from `docs/negative-claim-list.md`

---

## Traceability Failure Modes

| Failure | Code | Effect |
|---------|------|--------|
| No evidence anchor | `TRC-001` | conclusion invalid; must be retracted |
| Claim level exceeds evidence | `TRC-002` | claim_overreach; must be downgraded |
| Scope note absent | `TRC-003` | conclusion incomplete; must be supplemented |
| Negative space undeclared | `TRC-004` | advisory; must be declared before promotion |
| Source_ref unresolvable | `TRC-005` | anchor broken; must be corrected or removed |

---

## Placement

`traceability_entry` records belong in:
- session closeout artifacts
- reviewer handoff documents
- replay result artifacts

They must NOT be embedded in source code comments or RTL.
