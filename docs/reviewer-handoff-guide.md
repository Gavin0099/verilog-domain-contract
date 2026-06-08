# Reviewer Handoff Guide

This guide tells a reviewer which governance artifact bundle to download first and which file to read first for a given review task.

## 1. Start Here

- First identify the `artifact-tag` for the run under review.
- Then open:
  - `artifacts/closeout/<artifact-tag>-governance-bundle-manifest.json`
- This manifest tells you:
  - which five bundles exist for that tag
  - what each bundle is for
  - which files belong to each bundle

## 2. Which Bundle to Download

### If you are reviewing precondition-gate completeness coverage

- Download: `governance-precondition-artifacts`
- Read first:
  - `artifacts/precondition-gate/<artifact-tag>-precondition-gate-suite.json`
- Read second:
  - `artifacts/schema-conformance/<artifact-tag>-precondition-gate-conformance.json`

Use this bundle when the question is:
- did the precondition gate cover negation, boundary, and positive cases
- did the deterministic precondition suite pass cleanly
- is the precondition-gate artifact schema-clean

### If you are reviewing rule-behavior enforcement

- Download: `governance-replay-artifacts`
- Read first:
  - `artifacts/replay-results/<artifact-tag>-validator-replay.yaml`
- Read second:
  - `artifacts/schema-conformance/<artifact-tag>-validator-replay-conformance.json`

Use this bundle when the question is:
- did reset / assignment / handshake / FSM / CDC rule behavior fire correctly
- did replay cases pass without governance drift
- is the deterministic replay artifact schema-clean

### If you are reviewing claim-boundary enforcement

- Download: `governance-claim-artifacts`
- Read first:
  - `artifacts/claim-enforcement/checker-tests/<artifact-tag>-claim-enforcement-suite.json`
- Read second:
  - `artifacts/schema-conformance/<artifact-tag>-claim-enforcement-conformance.json`

Use this bundle when the question is:
- were strong claims blocked when preconditions were missing
- was semantic drift risk surfaced correctly
- is the claim-enforcement artifact schema-clean

### If you are reviewing closeout completeness

- Download: `governance-closeout-artifacts`
- Read first:
  - `artifacts/closeout/<artifact-tag>-governance-closeout-summary.json`
- Read second:
  - `artifacts/closeout/<artifact-tag>-governance-closeout-summary.md`
- Read third if needed:
  - `artifacts/schema-conformance/<artifact-tag>-governance-closeout-summary-conformance.json`
  - `artifacts/schema-conformance/<artifact-tag>-governance-closeout-report-conformance.json`

Use this bundle when the question is:
- did precondition, replay, and claim results aggregate cleanly
- is the closeout summary internally consistent
- are the closeout JSON and markdown outputs schema-clean

### If you are reviewing final reviewer-facing verdict

- Download: `governance-reviewer-artifacts`
- Read first:
  - `artifacts/closeout/<artifact-tag>-reviewer-checklist-verdict.json`
- Read second:
  - `artifacts/schema-conformance/<artifact-tag>-reviewer-checklist-verdict-conformance.json`
- Read third:
  - `artifacts/closeout/<artifact-tag>-governance-bundle-manifest.json`

Use this bundle when the question is:
- did the executable reviewer checklist pass
- which checklist sections passed or failed
- does the reviewer-facing verdict conform to its schema

## 3. Fastest Review Order

If you want the shortest possible review path:

1. Read `governance-reviewer-artifacts`
2. If the verdict looks suspicious, open `governance-closeout-artifacts`
3. If the problem is precondition coverage completeness, open `governance-precondition-artifacts`
4. If the problem is rule behavior, open `governance-replay-artifacts`
5. If the problem is claim posture, open `governance-claim-artifacts`

## 4. What Each Bundle Does Not Prove

- precondition bundle does not prove replay or claim-policy correctness
- replay bundle does not prove full RTL correctness
- claim bundle does not prove implementation quality
- closeout bundle does not replace rule-level evidence
- reviewer bundle does not replace the underlying replay / claim / closeout artifacts

## 5. Scope Reminder

This repository is a Verilog domain governance repository.

These bundles provide:
- precondition-gate completeness evidence
- rule-behavior evidence
- claim-boundary evidence
- reviewer closeout evidence

They do not by themselves prove:
- RTL functional correctness
- timing closure
- CDC signoff quality
- vendor-tool signoff completeness
