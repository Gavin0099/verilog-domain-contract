# Knowledge Base

## Gotchas

- `contract.yaml` parser in framework is flat-only; nested YAML maps are rejected.
- `PLAN.md` freshness parser expects header key `最後更新` exactly.
- In this sandbox user context, `git rev-parse` inside submodule may fail with dubious ownership unless safe-directory is set.
- Framework warnings about `expansion_boundary` may appear even when repo readiness is `True`.
- Extracted Markdown text from PDF may include OCR/encoding noise (for example special characters in author names); keep source page markers for traceability.
- Governance value comes from constraints that change AI decisions, not from tutorial coverage volume.
- Prefer boundary taxonomy mapping (`PRECONDITION`, `SEMANTIC_RULE`, `ASSUMPTION_RISK`, `COMPLETION_POLICY`, `VERIFICATION_REQUIREMENT`) before admitting new rules.
- `loader/readiness PASS` confirms ingestion/adoption only; behavior enforcement must be proven with replay oracle evidence.
- Refusal-driven error reduction can mask productivity loss; track `refusal_rate` together with `error_rate_given_codegen`.
- Documentation links in repo files should be portable (relative paths), not local absolute workspace paths.
- `oracle pass` and `deterministic mode identity` are distinct; boundary adherence can be stable while output mode still varies within safe bounds.
- `mode volatility` and `mode calibration` are separate layers: one explains variation, the other evaluates whether variation is optimal.
- `actions/checkout` with `submodules: recursive` can fail if a first-level submodule contains unresolved nested gitlinks; use `submodules: true` unless recursive nesting is intentionally configured.
- Current framework drift checker exits non-zero on warning; CI should parse JSON severity and fail only on `critical` if warning is policy-nonblocking.
- Pre-task gating should focus on input completeness (reset/interface); assignment semantic ambiguity is usually better handled in post-generation review.
- For uncertainty-heavy decisions, premise status should gate action before execution-risk convenience; otherwise low-risk permissive bias can dominate.
- Python regex injection via string replacement: when injecting regex patterns containing `\b` into Python source files using string `.replace()` or `sed`, the backslash sequence may be interpreted as `\x08` (backspace) unless written as a raw string literal (`r"\b..."`). Always write regex patterns directly into source files as raw string literals; never inject them via string substitution.
- Bash `content.replace("]", ...)` targeting a specific closing bracket: if multiple `]` characters exist in the file, string replace operates on the first match, not the intended location. Use precise index-based replacement or write the full file content to avoid partial corruption.
- `Edit` tool requires file to have been read in current context before editing; if context was compressed, re-read the file first.
- Governance-test run artifact structure: run-record.yaml must have `reviewer.disposition` and `reviewer.one_line_note` fields (empty string initially); scorecard.yaml must have `reviewer_decision: accept`. Hard gate `first_modification_in_primary_targets: true` means the run actually modified files declared in primary_targets.
- `session_context` confidence in run-ledger: use `reconstructed` for runs created after-the-fact within same session; `high` only for runs with runtime-captured artifacts.
- Contract sync-check 7-item checklist applies only to Verilog domain contract rules (RESET/ASSIGNMENT/HANDSHAKE/FSM); NOT to governance/rules/ general behavioral pack entries.
- `hook_coverage_tier` in gate_policy.yaml: A=fully automated pre+post; B=advisory automated at session stop; C=manual advisory only; D=no advisory. Run 018 upgraded C → B.
- round-NNN-summary.md `pending_count` tracks runs still open in that round; dashboard tracks cumulative state separately.
- Note: `03_knowledge_base.md` note "Pre-task gating should focus on input completeness (reset/interface); assignment semantic ambiguity is usually better handled in post-generation review" is outdated — Run 019 added Rule 4 pre-task gating for ASSIGNMENT_SEMANTICS_REQUIRED. Pre-task gating now covers reset + interface + assignment semantics.
