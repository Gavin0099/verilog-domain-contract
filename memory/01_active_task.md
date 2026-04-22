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

## Next Steps

- Continue domain-pack authoring with Markdown knowledge sources.
- Keep `memory/*.md` updated on each meaningful change, then commit/push.
- Expand behavior validation from expected matrix to executable scenario tests in next iteration.
- Execute replay cases BR-001 to BR-005 against target agent runtime and collect pass/fail evidence.
- Record replay outcomes with `schemas/behavioral-replay-results.yaml` and compute refusal/error trade-off metrics.
