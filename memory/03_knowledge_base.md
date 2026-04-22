# Knowledge Base

## Gotchas

- `contract.yaml` parser in framework is flat-only; nested YAML maps are rejected.
- `PLAN.md` freshness parser expects header key `最後更新` exactly.
- In this sandbox user context, `git rev-parse` inside submodule may fail with dubious ownership unless safe-directory is set.
- Framework warnings about `expansion_boundary` may appear even when repo readiness is `True`.
- Extracted Markdown text from PDF may include OCR/encoding noise (for example special characters in author names); keep source page markers for traceability.
- Governance value comes from constraints that change AI decisions, not from tutorial coverage volume.
- Prefer boundary taxonomy mapping (`PRECONDITION`, `SEMANTIC_RULE`, `ASSUMPTION_RISK`, `COMPLETION_POLICY`, `VERIFICATION_REQUIREMENT`) before admitting new rules.
