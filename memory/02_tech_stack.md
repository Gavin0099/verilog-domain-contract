# Tech Stack

## Repo Facts

- Domain: Verilog / RTL governance contract pack
- Governance runtime: `ai-governance-framework` (git submodule)
- Primary tooling: Python governance tools, Git submodule workflow, Markdown + YAML contract artifacts
- PDF to Markdown extraction: `pypdf` (`PdfReader.extract_text`) for knowledge ingestion
- Key integration commands:
  - `python additional/ai-governance-framework/governance_tools/adopt_governance.py --target . --framework-root additional/ai-governance-framework`
  - `python additional/ai-governance-framework/governance_tools/governance_drift_checker.py --repo . --framework-root additional/ai-governance-framework`
  - `python additional/ai-governance-framework/governance_tools/external_repo_readiness.py --repo . --framework-root additional/ai-governance-framework --format human`
