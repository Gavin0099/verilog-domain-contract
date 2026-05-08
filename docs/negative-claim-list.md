# Negative Claim List (v0.1)

Purpose: explicit enumeration of claim forms that are prohibited under this contract.
These are sentences or conclusion shapes that must NOT appear in reviewer output,
AI output, or session closeout artifacts.

Each entry has:
- `claim_form`: the prohibited sentence pattern
- `why_prohibited`: the governance reason
- `allowed_alternative`: what to say instead

---

## NC-001 — Single-case pass promoted to overall pass

**Prohibited forms**:
- "Tests passed." (without scope disclosure)
- "All cases verified." (when scope was partial)
- "Verification complete." (when unchecked cases exist)
- "Implementation correct." (based on a single passing case)

**Why prohibited**: passing one case does not imply passing unchecked cases.
Scope must be explicitly bounded.

**Allowed alternative**:
> "Case BV-RESET-001 passed under stated test conditions. Cases BV-ASSIGN-001 and BV-HANDSHAKE-001 were not tested in this run."

---

## NC-002 — Compile or lint success as functional correctness

**Prohibited forms**:
- "Code compiles, so it is correct."
- "Lint passed, implementation ready."
- "No syntax errors, RTL is complete."
- "Build succeeded." (used as completion evidence)

**Why prohibited**: defined in `docs/completion-evidence-levels.md` — L0 (`syntax_valid`) is explicitly not equivalent to functional correctness.

**Allowed alternative**:
> "L0 evidence (compile pass) obtained. Functional correctness at L1 or above not yet verified."

---

## NC-003 — Confidence language substituting for evidence

**Prohibited forms**:
- "Should be correct based on the implementation."
- "Likely works given the design pattern used."
- "Expected to pass integration given local results."
- "Implementation appears complete."

**Why prohibited**: subjective confidence does not constitute evidence.
Evidence must be stated and scoped per `docs/completion-evidence-levels.md`.

**Allowed alternative**:
> "No evidence above L0 was collected. Conclusion is bounded to syntax validity only."

---

## NC-004 — Unchecked cases inferred from checked cases

**Prohibited forms**:
- "Reset was verified, so clock behavior is also correct."
- "Handshake passed, so timing is implied."
- "Since assignment semantics are correct, FSM is also correct."
- "Because X passed, Y is assumed to pass."

**Why prohibited**: behavioral properties of one case do not transfer to another.
Each case requires its own evidence.

**Allowed alternative**:
> "Clock behavior was not tested in this run. Reset behavior passed under BV-RESET-001 conditions."

---

## NC-005 — Partial failure downplayed as advisory

**Prohibited forms**:
- "Minor issue, but overall pass."
- "Failed one case but still acceptable."
- "The failure is low risk, so approval is recommended."
- "Only one case failed; implementation is considered complete."

**Why prohibited**: if `failed_cases` is non-empty, `conclusion_level` must be `partial` or `blocked`.
A reviewer cannot override a failed case by characterizing it as low risk without an explicit remediation path.

**Allowed alternative**:
> "conclusion_level: partial. BV-HANDSHAKE-001 failed with severity=blocking. Remediation required before promotion."

---

## NC-006 — Implicit scope expansion

**Prohibited forms**:
- "Implementation complete for this module and similar modules."
- "Verified for this case and by extension the general pattern."
- "Passed under test, assumed to hold under production conditions."

**Why prohibited**: scope must be explicitly declared. Generalization beyond declared scope is a scope violation.

**Allowed alternative**:
> "Evidence covers the declared test scope only. Coverage beyond this scope is not claimed."

---

## NC-007 — Missing precondition treated as acceptable assumption

**Prohibited forms**:
- "Reset definition was missing but implementation assumed active-low."
- "Protocol semantics not defined but always-ready was assumed."
- "Precondition was unclear, so a reasonable default was chosen."
- "Assumed X because it's the most common case."

**Why prohibited**: silent assumption of missing preconditions is explicitly forbidden under
`docs/clock-reset-contract.md`, `docs/handshake-contract.md`, and `contract.yaml` `must_not_assume` list.

**Allowed alternative**:
> "Reset polarity was undefined. Output was downgraded to draft_with_explicit_assumptions.
> Assumed: active-low. Risk: mismatch with system specification."

---

## NC-008 — Claim level escalation without evidence upgrade

**Prohibited forms**:
- "Treating this as verified_implementation since the draft looked complete."
- "Upgrading from candidate to verified since no issues were found in review."
- "This is effectively a completed implementation."

**Why prohibited**: claim levels (`draft_rtl_provided`, `candidate_implementation_provided`, `verified_implementation`)
require specific minimum evidence as defined in `docs/completion-evidence-levels.md`.
Claim level cannot be upgraded by reviewer confidence alone.

**Allowed alternative**:
> "Claim level remains candidate_implementation_provided. Upgrade to verified_implementation
> requires minimum L2 (waveform_verified) + L3 (assertion_checked) evidence per completion-evidence-levels.md."

---

## Quick Reference Table

| Code | Pattern | Block level |
|------|---------|-------------|
| NC-001 | Single pass → overall pass | hard |
| NC-002 | Compile/lint = correctness | hard |
| NC-003 | Confidence language = evidence | hard |
| NC-004 | Case A pass → Case B inferred | hard |
| NC-005 | Partial failure downplayed | hard |
| NC-006 | Implicit scope expansion | hard |
| NC-007 | Missing precondition silently assumed | hard |
| NC-008 | Claim level escalation without evidence | hard |

All entries in this list are `hard` block level under v0.1 scope.
Exceptions require explicit reviewer attestation with specific remediation path.
