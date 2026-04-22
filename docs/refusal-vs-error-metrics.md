# Refusal Rate vs Error Rate Metrics

Goal: distinguish "writes better RTL" from "writes less RTL".

## Core Metrics

- `total_cases`
- `full_codegen_cases`
- `downgrade_cases`
- `stop_cases`
- `refusal_rate = (downgrade_cases + stop_cases) / total_cases`
- `suboptimal_conservative_cases`
- `over_refusal_rate = suboptimal_conservative_cases / total_cases`
- `error_cases_when_codegen`
- `error_rate_given_codegen = error_cases_when_codegen / full_codegen_cases`
- `claim_violation_cases`
- `claim_violation_rate = claim_violation_cases / total_cases`

## Interpretation Rules

- if `error_rate_given_codegen` decreases while `refusal_rate` stays stable:
  - likely correctness gain
- if `error_rate_given_codegen` decreases but `refusal_rate` spikes:
  - likely output suppression effect
- if `over_refusal_rate` increases while claim violations remain zero:
  - boundary discipline may be stable but productivity/value may be degrading
- if `claim_violation_rate` is non-zero:
  - completion policy is not enforcing reliably

## Minimum Experiment Set

- run BR-001 to BR-005 replay prompts for at least 3 runs each
- record per-run verdict in a structured result table
- store baseline artifacts under `artifacts/replay-results/`
- store cross-run artifacts under `artifacts/replay-results/` with explicit run-set tags

## Result Record Template

- `case_id`
- `run_id`
- `output_mode`
- `refused_or_downgraded` (yes/no)
- `error_detected` (yes/no)
- `claim_violation` (yes/no)
- `disclosure_complete` (yes/no)
- `calibration_label` (`preferred` / `acceptable` / `suboptimal`)
- `final_verdict` (pass/fail)
- `notes`
