# Epistemic Decision Policy (Calibration Slice)

This policy addresses a known semantic risk:

- low execution risk can incorrectly dominate weak premise/evidence conditions.

## Core Principle

Decision precedence for uncertainty-sensitive tasks:

- premise_status > evidence_quality > execution_risk

## Premise Gate

- `unsupported` -> block proceed, choose `reframe`
- `unknown` -> default to `need_more_info`
- `supported` -> allow normal risk-sensitive scoring

For `unknown`, proceeding requires explicit bounded-trial justification.

## Epistemic Risk

`epistemic_risk` is derived from premise/evidence quality:

- high: unsupported premise, or unknown premise with weak evidence
- medium: unknown premise with moderate evidence
- low: supported premise with moderate/strong evidence

If epistemic risk is high, `need_more_info` outranks action-taking paths even when execution risk is low.

## Bounded Trial Cost

`bounded_trial` is no longer free.

Trial cost includes:

- state pollution
- debugging noise
- regression masking risk

If `bounded_trial_cost` exceeds threshold, `need_more_info` outranks `proceed_with_assumption`.

## Non-Claim

This policy improves decision semantics calibration. It does not prove end-to-end correctness of generated RTL.
