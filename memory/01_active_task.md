# Active Task

## Current Status

- Imported `ai-governance-framework` as submodule at `additional/ai-governance-framework`.
- Adopted governance baseline and created Verilog/RTL domain contract v0.1 skeleton.
- Readiness check is `ready = True`; drift check is `ok = True` with warning-level expansion-boundary notice.
- Converted three Verilog knowhow PDFs to Markdown under `docs/knowhow/`.
- Implemented end-to-end governance pipeline for three core rules: reset, assignment semantics, and handshake timing.
- Added rule extraction table and behavior validation matrix to verify decision-impacting constraints.
- Added replay-oracle prompts and framework-surface mapping to close the enforcement-evidence gap.
- Added deterministic precondition completeness model, completion evidence levels, and refusal-vs-error metric model.
- Added baseline replay result artifacts (`artifacts/replay-results/2026-04-22-baseline.md/.yaml`) as first observed behavior evidence.
- Added cross-run replay result artifacts (`artifacts/replay-results/2026-04-22-cross-run.md/.yaml`) for repeated-run evidence in same environment.
- Added `docs/mode-volatility-note.md` to separate boundary stability from mode determinism in cross-run interpretation.
- Added `docs/mode-calibration-note.md` to define preferred/acceptable/suboptimal modes per replay case.
- Fixed CI governance workflow checkout/drift behavior:
  - avoid recursive submodule fetch (prevents nested `.latest-main` submodule failure)
  - fail only on `critical` drift severity, keep `warning` as non-blocking notice
- Added executable pre-task gate slice for missing preconditions:
  - `validators/precondition_gate_validator.py`
  - `scripts/precondition_gate_smoke.py`
  - `docs/pre-task-gate-integration.md`
  - `artifacts/precondition-gate/2026-04-22-smoke.json`
- Added epistemic decision calibration slice:
  - `docs/epistemic-decision-policy.md`
  - `artifacts/decision-semantics/epistemic_cases_v1.json`
  - `scripts/epistemic_scoring_smoke.py`
  - `artifacts/decision-semantics/2026-04-23-epistemic-smoke.json`

## Next Steps

- Continue domain-pack authoring with Markdown knowledge sources.
- Keep `memory/*.md` updated on each meaningful change, then commit/push.
- Expand behavior validation from expected matrix to executable scenario tests in next iteration.
- Execute replay cases BR-001 to BR-005 against target agent runtime and collect pass/fail evidence.
- Record replay outcomes with `schemas/behavioral-replay-results.yaml` and compute refusal/error trade-off metrics.
- Expand replay from single-session baseline to multi-run and cross-agent evidence.
- Next evidence gap: cross-model replay and mixed-completeness prompts that include full-codegen paths.
- Keep external status wording aligned to "oracle-bounded stability" and avoid deterministic-enforcement overclaim.
- Use calibration labels in replay artifacts to compute over-refusal rate and guide strictness tuning.
- Monitor workflow runs after this patch to confirm checkout and drift gate behavior.
- Feed precondition-gate output into runtime pre-task payload path as machine-readable decision input.
- Integrate epistemic-risk scoring into pre-task decision inputs after baseline smoke validation.
- [2026-04-30] Completed CLAIM_ENFORCEMENT precondition docs + pilot A/B/C rerun (pass).
- [2026-04-30] Added expansion aggregate summary for writing-contract and SpecAuthority.
- [2026-05-08] Completed governance-test Rounds 1–4 (Runs 001–016): full audit trail with run-record, scorecard, diff.patch per run; all scorecards reviewer_decision = accept.
- [2026-05-08] Run 017: reviewer-dashboard sync to 16 runs; round-004-summary cumulative state corrected.
- [2026-05-08] Run 018: `scripts/check_advisory.py` Stop hook integrated; `gate_policy.yaml` hook_coverage_tier upgraded C → B.
- [2026-05-08] Run 019: ASSIGNMENT_SEMANTICS_REQUIRED full validator sync — 2 precondition_effects entries added, Rule 4 + 3 regex patterns in validator, PG-004/005 smoke cases added (5/5 PASS).
- [2026-05-08] Run 020: governance/rules/ classified as cross-domain general rule pack (D-020-01); RULE_INDEX.md rewritten with two-system classification.
- [2026-05-08] Run 021: reviewer-dashboard sync to 20 runs; all decisions accept.
- [2026-05-08] Run 022: CDC_STRATEGY_REQUIRED full governance sync — docs/cdc-contract.md new; validator Rule 5 + RE_CDC_INTENT + RE_CDC_STRATEGY; PG-006/007 smoke; 7/7 PASS; contract.yaml fully updated.
- [2026-05-08] Run 023: round-005-summary.md + round-006-summary.md created.
- [2026-05-08] Run 024: artifacts/precondition-gate/2026-05-08-smoke.json created (PG-001~007, rule labels, v3 updated in Run 025).
- [2026-05-08] Run 025: FSM explicit smoke PG-008/009 added; smoke 9/9 PASS.
- [2026-05-08] Run 026: reviewer-dashboard sync to 25 runs; round-006-summary completed.
- [2026-05-08] run-001~021 scorecards: status → accepted; session-index Round 7 entry added.

## Governance Gaps Status

**All gaps closed as of Run 026. No open governance gaps remain.**

Previous gap list (all fixed):
- CDC rule → Fixed Run 022 (leaf doc, governance_rules, validator Rule 5, smoke PG-006/007)
- FSM explicit smoke → Fixed Run 025 (PG-008/009)
- Round 5–6 summaries → Fixed Run 023
- smoke artifact stale → Fixed Run 024 (2026-05-08-smoke.json, v3 in Run 025)

## Long-Term Backlog (not blocked, no urgency)

- Execute replay cases BR-001~BR-005 against target agent runtime; record outcomes with schemas/behavioral-replay-results.yaml
- Cross-model replay and mixed-completeness prompts (full-codegen paths)
- Feed precondition-gate output into runtime pre-task payload path as machine-readable decision input
- Integrate epistemic-risk scoring into pre-task decision inputs
