# Review Log

## Entries

- 2026-04-22: Imported framework as submodule and adopted governance baseline.
- 2026-04-22: Implemented Verilog/RTL domain contract pack v0.1 skeleton (docs/examples/schema/contract).
- 2026-04-22: Validation snapshot:
  - `domain_contract_loader.py`: contract resolved and all declared files exist.
  - `external_repo_readiness.py`: `ready = True`.
  - `governance_drift_checker.py`: `ok = True`, `severity = warning` (expansion-boundary warning only).
- 2026-04-22: Workflow requirement added by user: update `memory/*.md` before each push.
- 2026-04-22: Converted knowledge PDFs to Markdown:
  - `docs/knowhow/digital_system_design_with_system_verilog.md`
  - `docs/knowhow/RTS5264_Datasheet_1.0.md`
  - `docs/knowhow/Verilog_HDL_A_guide_to_digital_design_and_synthesis_v2.md`
- 2026-04-22: Applied governance-focused pipeline for 3 core rules:
  - reset definition required
  - assignment semantics required
  - handshake timing definition required
- 2026-04-22: Added:
  - `docs/rule-extraction-table.md`
  - `docs/behavior-validation.md`
  - stronger decision constraints in `contract.yaml`
  - reviewer checks in `schemas/review-checklist.yaml`
- 2026-04-22: Validation snapshot after changes:
  - `domain_contract_loader.py`: PASS (documents resolved)
  - `external_repo_readiness.py`: `ready = True`
  - `governance_drift_checker.py`: `ok = True`, warning only on expansion-boundary
- 2026-04-22: Added enforcement-oriented assets:
  - `docs/behavioral-replay-oracle.md` (BR-001..BR-005 prompts + oracle)
  - `docs/framework-surface-mapping.md` (pre-task/post-task/claim-policy mapping)
- 2026-04-22: Re-validated after additions:
  - `domain_contract_loader.py`: PASS
  - `external_repo_readiness.py`: `ready = True`
