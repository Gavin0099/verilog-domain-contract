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
