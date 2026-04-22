# AGENTS.md
<!-- governance-baseline: overridable -->
<!-- baseline_version: 1.0.0 -->

This file extends `AGENTS.base.md` with repo-specific rules for Verilog / RTL domain contract authoring.

## Repo-Specific Risk Levels
<!-- governance:key=risk_levels -->

- HIGH: changes to `contract.yaml` preconditions/effects, completion-claim semantics, or downgrade behavior
- HIGH: changes that loosen "must not assume" boundaries for clock/reset/interface timing
- MEDIUM: edits to core docs in `docs/` that alter operational rules
- MEDIUM: changes to example RTL that may change rule interpretation
- LOW: wording clarifications that do not change decisions, gates, or policy outcomes

## Must-Test Paths
<!-- governance:key=must_test_paths -->

- `contract.yaml`: validate with readiness + drift check
- `schemas/review-checklist.yaml`: must parse as YAML and preserve required keys
- `docs/clock-reset-contract.md`: no regression of "missing precondition -> downgrade/stop" behavior
- `docs/verification-minimums.md`: no weakening of completion evidence expectations
- `docs/completion-claim-policy.md`: no claim escalation without explicit evidence basis

## L1 -> L2 Escalation Triggers
<!-- governance:key=escalation_triggers -->

- any proposal to allow implementation claims from compile/lint-only evidence
- any proposal to treat missing clock/reset/interface specs as acceptable for final RTL generation
- any expansion to CDC/protocol/vendor-specific rules inside v0.1 core docs
- any change introducing implicit defaults for reset polarity, clock edge, or handshake latency

## Repo-Specific Forbidden Behaviors
<!-- governance:key=forbidden_behaviors -->

- do not turn this repository into a general Verilog tutorial or style guide
- do not represent the contract pack as proof of RTL correctness
- do not silently fill missing critical preconditions during code generation
- do not claim "verified implementation" without explicit verification evidence scope
- do not mix project-local conventions into core domain docs without explicit labeling

## Repo Workflow Default

- Before each push, update relevant files in `memory/` (`01_active_task.md` to `04_review_log.md`) with current task state, validations, and decisions.
- After memory update, commit and push in the same work cycle unless explicitly instructed not to push.
