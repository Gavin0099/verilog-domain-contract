#!/usr/bin/env python3
"""Build a machine-readable governance closeout summary from deterministic artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to build governance closeout summary.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    claim_artifact_path,
    claim_conformance_path,
    closeout_summary_conformance_path,
    closeout_summary_path,
    default_artifact_tag,
    precondition_gate_artifact_path,
    precondition_gate_conformance_path,
    replay_artifact_path,
    replay_conformance_path,
)


def _load(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def build_summary(artifact_tag: str) -> dict[str, object]:
    precondition_artifact = precondition_gate_artifact_path(REPO_ROOT, artifact_tag)
    replay_artifact = replay_artifact_path(REPO_ROOT, artifact_tag)
    claim_artifact = claim_artifact_path(REPO_ROOT, artifact_tag)
    runtime_hook_smoke_artifact = REPO_ROOT / f"artifacts/governance/{artifact_tag}-runtime-hook-smoke.json"
    precondition_conformance_artifact = precondition_gate_conformance_path(REPO_ROOT, artifact_tag)
    replay_conformance_artifact = replay_conformance_path(REPO_ROOT, artifact_tag)
    claim_conformance_artifact = claim_conformance_path(REPO_ROOT, artifact_tag)
    precondition = _load(precondition_artifact)
    replay = _load(replay_artifact)
    claim = _load(claim_artifact)
    runtime_hooks = _load(runtime_hook_smoke_artifact)
    precondition_conformance = _load(precondition_conformance_artifact)
    replay_conformance = _load(replay_conformance_artifact)
    claim_conformance = _load(claim_conformance_artifact)

    precondition_summary = precondition["summary"]
    replay_summary = replay["summary"]
    claim_summary = claim["summary"]
    runtime_summary = runtime_hooks["summary"]

    return {
        "schema_version": "0.1",
        "name": "governance-closeout-summary",
        "generated_from": {
            "precondition_gate_artifact": str(precondition_artifact.relative_to(REPO_ROOT)),
            "behavioral_replay_artifact": str(replay_artifact.relative_to(REPO_ROOT)),
            "claim_enforcement_artifact": str(claim_artifact.relative_to(REPO_ROOT)),
            "runtime_hook_smoke_artifact": str(runtime_hook_smoke_artifact.relative_to(REPO_ROOT)),
            "precondition_gate_conformance": str(precondition_conformance_artifact.relative_to(REPO_ROOT)),
            "behavioral_replay_conformance": str(replay_conformance_artifact.relative_to(REPO_ROOT)),
            "claim_enforcement_conformance": str(claim_conformance_artifact.relative_to(REPO_ROOT)),
        },
        "surfaces": {
            "precondition_gate": {
                "artifact_family": precondition["artifact_family"],
                "suite_id": precondition["suite_id"],
                "execution_surface": precondition["execution_surface"],
                "coverage_summary": precondition.get("coverage_summary", {}),
                "summary": precondition_summary,
                "schema_conformance_ok": precondition_conformance["ok"],
                "schema_conformance_errors": precondition_conformance["errors"],
            },
            "behavioral_replay": {
                "artifact_family": replay["artifact_family"],
                "suite_id": replay["suite_id"],
                "execution_surface": replay["execution_surface"],
                "coverage_summary": replay.get("coverage_summary", {}),
                "summary": replay_summary,
                "schema_conformance_ok": replay_conformance["ok"],
                "schema_conformance_errors": replay_conformance["errors"],
            },
            "claim_enforcement": {
                "artifact_family": claim["artifact_family"],
                "suite_id": claim["suite_id"],
                "execution_surface": claim["execution_surface"],
                "coverage_summary": claim.get("coverage_summary", {}),
                "summary": claim_summary,
                "schema_conformance_ok": claim_conformance["ok"],
                "schema_conformance_errors": claim_conformance["errors"],
            },
            "runtime_hooks": {
                "artifact_family": "runtime_hooks",
                "suite_id": f"runtime-hook-smoke-{artifact_tag}",
                "execution_surface": "repo_local_runtime_hook_smoke",
                "coverage_summary": {},
                "summary": runtime_summary,
                "schema_conformance_ok": runtime_summary["overall_ok"],
                "schema_conformance_errors": [] if runtime_summary["overall_ok"] else ["runtime_hook_smoke_failed"],
            },
        },
        "overall": {
            "schema_conformance_ok": (
                precondition_conformance["ok"] and replay_conformance["ok"] and claim_conformance["ok"]
            ),
            "precondition_fail": precondition_summary["fail"],
            "replay_fail": replay_summary["fail"],
            "claim_fail": claim_summary["fail"],
            "claim_not_executed": claim_summary["not_executed"],
            "runtime_hook_fail": runtime_summary["fail"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build governance closeout summary artifact.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = build_summary(args.artifact_tag)
    out_path = Path(args.out) if args.out else closeout_summary_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    closeout_ok = result["overall"]["schema_conformance_ok"] and result["name"] == "governance-closeout-summary"
    closeout_conformance = closeout_summary_conformance_path(REPO_ROOT, args.artifact_tag)
    closeout_conformance.parent.mkdir(parents=True, exist_ok=True)
    closeout_conformance.write_text(
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
        print(f"precondition_fail={result['overall']['precondition_fail']}")
        print(f"replay_fail={result['overall']['replay_fail']}")
        print(f"claim_fail={result['overall']['claim_fail']}")
        print(f"claim_not_executed={result['overall']['claim_not_executed']}")
        print(f"runtime_hook_fail={result['overall']['runtime_hook_fail']}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
    return 0 if result["overall"]["schema_conformance_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
