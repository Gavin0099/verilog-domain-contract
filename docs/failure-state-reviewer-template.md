# Failure-State Reviewer Template (v0.1)

Purpose: provide a reviewer-safe conclusion structure for partial pass / partial fail scenarios.
Non-claim: this template does not produce an "overall pass" verdict. It produces a bounded conclusion.

---

## Usage Rules

1. Fill in every section. Omitting a section is a reviewer error, not a shortcut.
2. `conclusion_level` must be derived from `failed_cases` and `unchecked_cases`, not from `passed_cases` alone.
3. Passing some cases does not allow claiming passing of unchecked cases.
4. If `failed_cases` is non-empty, `conclusion_level` must be `partial` or `blocked`.
5. `reviewer_attestation` must be filled by a human reviewer, not auto-generated.

---

## Template

```
failure_state_review:
  context:
    task_id: ""
    run_id: ""
    reviewed_at: ""
    reviewer_id: ""

  scope_declared:
    what_was_tested: ""          # explicit scope statement — e.g. "BV-RESET-001 through BV-ASSIGN-001"
    what_was_not_tested: []      # list of known untested cases or behaviors
    preconditions_verified: []   # preconditions that were confirmed before testing

  case_results:
    passed_cases:
      - case_id: ""
        evidence: ""             # L0/L1/L2/L3 per completion-evidence-levels.md
        disclosure_complete: true|false
    failed_cases:
      - case_id: ""
        failure_type: ""         # claim_violation | behavior_mismatch | disclosure_missing | hard_boundary_breach
        severity: ""             # blocking | advisory
        evidence: ""
        remediation_required: true|false
    unchecked_cases:
      - case_id: ""
        reason_not_checked: ""   # explicit reason — "out of scope", "missing precondition", "deferred"

  conclusion:
    conclusion_level: ""         # pass | partial | blocked
    claim_allowed: []            # only claims directly supported by passed_cases evidence
    claim_prohibited: []         # must list claims that CANNOT be made given current evidence
    open_risks: []               # residual risks not addressed by this review

  reviewer_attestation:
    conclusion_is_bounded: true|false    # reviewer confirms conclusion does not exceed evidence
    no_single_pass_escalation: true|false  # reviewer confirms no partial pass promoted to overall pass
    failed_cases_acknowledged: true|false
    unchecked_cases_acknowledged: true|false
    attestation_note: ""
```

---

## Conclusion Level Semantics

| `conclusion_level` | Meaning | Allowed next action |
|--------------------|---------|---------------------|
| `pass` | All declared cases passed with sufficient evidence | Promote to next stage |
| `partial` | Some cases passed, some failed or unchecked | Must list what is and is not covered; no promotion without remediation |
| `blocked` | Hard boundary breach or critical failure case present | No promotion; remediation required before re-review |

## Evidence Requirements (cross-reference)

Evidence levels (L0–L3) are defined in `docs/completion-evidence-levels.md`.
Minimum evidence per claim level is defined in `docs/completion-claim-policy.md`.
Traceability schema (linking conclusions to evidence anchors) is defined in `docs/traceability-contract.md`.
Each bounded conclusion from this template should correspond to a `traceability_entry`
with matching `conclusion_id`, `claim_level`, and `evidence_anchors`.

---

## Anti-Patterns (must not appear in reviewer output)

See `docs/negative-claim-list.md` for the full list of prohibited claim forms.
