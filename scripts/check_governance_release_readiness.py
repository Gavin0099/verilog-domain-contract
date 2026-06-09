#!/usr/bin/env python3
"""Collapse handoff, coherence, and schema conformance into one release-readiness verdict."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    aggregate_coherence_conformance_path,
    aggregate_coherence_path,
    claim_conformance_path,
    closeout_report_conformance_path,
    closeout_summary_conformance_path,
    default_artifact_tag,
    precondition_gate_conformance_path,
    release_handoff_conformance_path,
    release_handoff_index_path,
    replay_conformance_path,
    reviewer_bundle_manifest_conformance_path,
    reviewer_handoff_consistency_conformance_path,
    reviewer_verdict_conformance_path,
    runtime_hook_smoke_conformance_path,
)


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _required_conformance_paths(artifact_tag: str) -> dict[str, Path]:
    return {
        "precondition_gate": precondition_gate_conformance_path(REPO_ROOT, artifact_tag),
        "behavioral_replay": replay_conformance_path(REPO_ROOT, artifact_tag),
        "claim_enforcement": claim_conformance_path(REPO_ROOT, artifact_tag),
        "closeout_summary": closeout_summary_conformance_path(REPO_ROOT, artifact_tag),
        "closeout_report": closeout_report_conformance_path(REPO_ROOT, artifact_tag),
        "reviewer_verdict": reviewer_verdict_conformance_path(REPO_ROOT, artifact_tag),
        "bundle_manifest": reviewer_bundle_manifest_conformance_path(REPO_ROOT, artifact_tag),
        "reviewer_handoff_consistency": reviewer_handoff_consistency_conformance_path(REPO_ROOT, artifact_tag),
        "release_handoff": release_handoff_conformance_path(REPO_ROOT, artifact_tag),
        "runtime_hook_smoke": runtime_hook_smoke_conformance_path(REPO_ROOT, artifact_tag),
        "aggregate_coherence": aggregate_coherence_conformance_path(REPO_ROOT, artifact_tag),
    }


def _evaluate_conformance(name: str, path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "name": name,
            "artifact": _rel(path),
            "ok": False,
            "reason": "missing",
        }

    payload = _load_json(path)
    if "total" in payload or "pass" in payload or "fail" in payload:
        total = int(payload.get("total", 0))
        passed = int(payload.get("pass", 0))
        failed = int(payload.get("fail", 0))
        ok = total > 0 and failed == 0 and passed == total
    else:
        total = 1
        passed = 1 if bool(payload.get("ok")) else 0
        failed = 0 if bool(payload.get("ok")) else 1
        ok = bool(payload.get("ok"))
    return {
        "name": name,
        "artifact": _rel(path),
        "ok": ok,
        "reason": "pass" if ok else "conformance_failed",
        "total": total,
        "pass": passed,
        "fail": failed,
    }


def check_release_readiness(artifact_tag: str) -> dict[str, object]:
    release_handoff_path = release_handoff_index_path(REPO_ROOT, artifact_tag)
    aggregate_coherence_artifact_path = aggregate_coherence_path(REPO_ROOT, artifact_tag)

    release_handoff = _load_json(release_handoff_path)
    aggregate_coherence = _load_json(aggregate_coherence_artifact_path)

    conformance_results = [
        _evaluate_conformance(name, path)
        for name, path in _required_conformance_paths(artifact_tag).items()
    ]

    release_handoff_ready = release_handoff.get("release_status") == "ready_for_handoff"
    aggregate_coherence_ok = bool(aggregate_coherence.get("ok"))
    conformance_all_pass = all(bool(item["ok"]) for item in conformance_results)

    checks = {
        "release_handoff_ready": release_handoff_ready,
        "aggregate_coherence_ok": aggregate_coherence_ok,
        "schema_conformance_all_pass": conformance_all_pass,
    }

    return {
        "schema_version": "0.1",
        "name": "governance-release-readiness-check",
        "artifact_tag": artifact_tag,
        "verdict": "pass" if all(checks.values()) else "fail",
        "ready_for_handoff": all(checks.values()),
        "checks": checks,
        "artifacts": {
            "release_handoff": _rel(release_handoff_path),
            "aggregate_coherence": _rel(aggregate_coherence_artifact_path),
            "schema_conformance": [item["artifact"] for item in conformance_results],
        },
        "release_status": release_handoff.get("release_status"),
        "aggregate_coherence_status": bool(aggregate_coherence.get("ok")),
        "conformance_summary": {
            "total_artifacts": len(conformance_results),
            "pass": sum(1 for item in conformance_results if item["ok"]),
            "fail": sum(1 for item in conformance_results if not item["ok"]),
            "results": conformance_results,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check release readiness from handoff, coherence, and conformance artifacts.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = check_release_readiness(args.artifact_tag)
    out_path = Path(args.out) if args.out else REPO_ROOT / f"artifacts/governance/{args.artifact_tag}-release-readiness.json"
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[governance_release_readiness]")
        print(f"artifact_tag={result['artifact_tag']}")
        print(f"verdict={result['verdict']}")
        print(f"ready_for_handoff={str(result['ready_for_handoff']).lower()}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for key, value in result["checks"].items():
            print(f"{key}={'pass' if value else 'fail'}")
        print(f"conformance_pass={result['conformance_summary']['pass']}")
        print(f"conformance_fail={result['conformance_summary']['fail']}")
    return 0 if result["ready_for_handoff"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
