# Tech Stack

## Repo Facts

- Domain: Verilog / RTL governance contract pack
- Governance runtime: `ai-governance-framework` (git submodule)
- Primary tooling: Python governance tools, Git submodule workflow, Markdown + YAML contract artifacts
- PDF to Markdown extraction: `pypdf` (`PdfReader.extract_text`) for knowledge ingestion
- Governance rule normalization: flat machine-readable rule encoding in `contract.yaml` to match framework parser constraints
- Behavior evidence assets: replay prompt oracle (`docs/behavioral-replay-oracle.md`) and runtime surface mapping (`docs/framework-surface-mapping.md`)
- Measurement and enforcement modeling assets:
  - `docs/precondition-completeness-model.md`
  - `docs/completion-evidence-levels.md`
  - `docs/coverage-model.md`
- `docs/refusal-vs-error-metrics.md`
- `schemas/behavioral-replay-results.yaml`
- Baseline evidence artifact path: `artifacts/replay-results/2026-04-22-baseline.md` and `.yaml`
- Cross-run interpretation guardrail: `docs/mode-volatility-note.md`
- Key integration commands:
  - `python additional/ai-governance-framework/governance_tools/adopt_governance.py --target . --framework-root additional/ai-governance-framework`
  - `python additional/ai-governance-framework/governance_tools/governance_drift_checker.py --repo . --framework-root additional/ai-governance-framework`
  - `python additional/ai-governance-framework/governance_tools/external_repo_readiness.py --repo . --framework-root additional/ai-governance-framework --format human`
