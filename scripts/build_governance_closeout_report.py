#!/usr/bin/env python3
"""Render a human-readable governance closeout report from the aggregate summary JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_CONFORMANCE = REPO_ROOT / "artifacts/schema-conformance/2026-06-05-governance-closeout-report-conformance.json"


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _render(summary: dict[str, object]) -> str:
    surfaces = summary["surfaces"]
    overall = summary["overall"]
    generated_from = summary["generated_from"]

    lines = [
        "# Governance Closeout Summary",
        "",
        "## Overall",
        "",
        f"- `schema_conformance_ok`: `{str(overall['schema_conformance_ok']).lower()}`",
        f"- `replay_fail`: `{overall['replay_fail']}`",
        f"- `claim_fail`: `{overall['claim_fail']}`",
        f"- `claim_not_executed`: `{overall['claim_not_executed']}`",
        "",
        "## Behavioral Replay",
        "",
        f"- `suite_id`: `{surfaces['behavioral_replay']['suite_id']}`",
        f"- `execution_surface`: `{surfaces['behavioral_replay']['execution_surface']}`",
        f"- `summary.total`: `{surfaces['behavioral_replay']['summary']['total']}`",
        f"- `summary.pass`: `{surfaces['behavioral_replay']['summary']['pass']}`",
        f"- `summary.fail`: `{surfaces['behavioral_replay']['summary']['fail']}`",
        f"- `schema_conformance_ok`: `{str(surfaces['behavioral_replay']['schema_conformance_ok']).lower()}`",
        "",
        "## Claim Enforcement",
        "",
        f"- `suite_id`: `{surfaces['claim_enforcement']['suite_id']}`",
        f"- `execution_surface`: `{surfaces['claim_enforcement']['execution_surface']}`",
        f"- `summary.total`: `{surfaces['claim_enforcement']['summary']['total']}`",
        f"- `summary.pass`: `{surfaces['claim_enforcement']['summary']['pass']}`",
        f"- `summary.fail`: `{surfaces['claim_enforcement']['summary']['fail']}`",
        f"- `summary.not_executed`: `{surfaces['claim_enforcement']['summary']['not_executed']}`",
        f"- `schema_conformance_ok`: `{str(surfaces['claim_enforcement']['schema_conformance_ok']).lower()}`",
        "",
        "## Inputs",
        "",
        f"- replay artifact: `{generated_from['behavioral_replay_artifact']}`",
        f"- claim artifact: `{generated_from['claim_enforcement_artifact']}`",
        f"- replay conformance: `{generated_from['behavioral_replay_conformance']}`",
        f"- claim conformance: `{generated_from['claim_enforcement_conformance']}`",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build human-readable governance closeout report.")
    parser.add_argument(
        "--summary",
        default="artifacts/closeout/2026-06-05-governance-closeout-summary.json",
    )
    parser.add_argument(
        "--out",
        default="artifacts/closeout/2026-06-05-governance-closeout-summary.md",
    )
    args = parser.parse_args()

    summary_path = REPO_ROOT / args.summary if not Path(args.summary).is_absolute() else Path(args.summary)
    out_path = REPO_ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    report = _render(_load(summary_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    REPORT_CONFORMANCE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_CONFORMANCE.write_text(
        json.dumps(
            {
                "schema": "schemas/governance-closeout-report.yaml",
                "artifact": str(out_path.relative_to(REPO_ROOT)),
                "ok": True,
                "errors": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("[governance_closeout_report]")
    print(f"out={out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
