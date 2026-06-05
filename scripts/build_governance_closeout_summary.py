#!/usr/bin/env python3
"""Build a machine-readable governance closeout summary from deterministic artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to build governance closeout summary.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]

REPLAY_ARTIFACT = REPO_ROOT / "artifacts/replay-results/2026-06-05-validator-replay.yaml"
CLAIM_ARTIFACT = REPO_ROOT / "artifacts/claim-enforcement/checker-tests/2026-06-05-claim-enforcement-suite.json"
REPLAY_CONFORMANCE = REPO_ROOT / "artifacts/schema-conformance/2026-06-05-validator-replay-conformance.json"
CLAIM_CONFORMANCE = REPO_ROOT / "artifacts/schema-conformance/2026-06-05-claim-enforcement-conformance.json"
CLOSEOUT_CONFORMANCE = REPO_ROOT / "artifacts/schema-conformance/2026-06-05-governance-closeout-summary-conformance.json"


def _load(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def build_summary() -> dict[str, object]:
    replay = _load(REPLAY_ARTIFACT)
    claim = _load(CLAIM_ARTIFACT)
    replay_conformance = _load(REPLAY_CONFORMANCE)
    claim_conformance = _load(CLAIM_CONFORMANCE)

    replay_summary = replay["summary"]
    claim_summary = claim["summary"]

    return {
        "schema_version": "0.1",
        "name": "governance-closeout-summary",
        "generated_from": {
            "behavioral_replay_artifact": str(REPLAY_ARTIFACT.relative_to(REPO_ROOT)),
            "claim_enforcement_artifact": str(CLAIM_ARTIFACT.relative_to(REPO_ROOT)),
            "behavioral_replay_conformance": str(REPLAY_CONFORMANCE.relative_to(REPO_ROOT)),
            "claim_enforcement_conformance": str(CLAIM_CONFORMANCE.relative_to(REPO_ROOT)),
        },
        "surfaces": {
            "behavioral_replay": {
                "artifact_family": replay["artifact_family"],
                "suite_id": replay["suite_id"],
                "execution_surface": replay["execution_surface"],
                "summary": replay_summary,
                "schema_conformance_ok": replay_conformance["ok"],
                "schema_conformance_errors": replay_conformance["errors"],
            },
            "claim_enforcement": {
                "artifact_family": claim["artifact_family"],
                "suite_id": claim["suite_id"],
                "execution_surface": claim["execution_surface"],
                "summary": claim_summary,
                "schema_conformance_ok": claim_conformance["ok"],
                "schema_conformance_errors": claim_conformance["errors"],
            },
        },
        "overall": {
            "schema_conformance_ok": replay_conformance["ok"] and claim_conformance["ok"],
            "replay_fail": replay_summary["fail"],
            "claim_fail": claim_summary["fail"],
            "claim_not_executed": claim_summary["not_executed"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build governance closeout summary artifact.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument(
        "--out",
        default="artifacts/closeout/2026-06-05-governance-closeout-summary.json",
    )
    args = parser.parse_args()

    result = build_summary()
    out_path = REPO_ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    closeout_ok = result["overall"]["schema_conformance_ok"] and result["name"] == "governance-closeout-summary"
    CLOSEOUT_CONFORMANCE.parent.mkdir(parents=True, exist_ok=True)
    CLOSEOUT_CONFORMANCE.write_text(
        json.dumps(
            {
                "schema": "schemas/governance-closeout-summary.yaml",
                "artifact": str(out_path.relative_to(REPO_ROOT)),
                "ok": closeout_ok,
                "errors": [] if closeout_ok else ["closeout_summary_basic_validation_failed"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[governance_closeout_summary]")
        print(f"schema_conformance_ok={result['overall']['schema_conformance_ok']}")
        print(f"replay_fail={result['overall']['replay_fail']}")
        print(f"claim_fail={result['overall']['claim_fail']}")
        print(f"claim_not_executed={result['overall']['claim_not_executed']}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
    return 0 if result["overall"]["schema_conformance_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
