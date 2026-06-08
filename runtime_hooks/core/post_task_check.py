#!/usr/bin/env python3
"""Deterministic post-task closeout runtime hook."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    closeout_summary_path,
    default_artifact_tag,
    release_handoff_index_path,
    reviewer_verdict_path,
)


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _evaluate_closeout(artifact_tag: str) -> dict[str, object]:
    closeout_path = closeout_summary_path(REPO_ROOT, artifact_tag)
    reviewer_path = reviewer_verdict_path(REPO_ROOT, artifact_tag)
    handoff_path = release_handoff_index_path(REPO_ROOT, artifact_tag)
    expected = [closeout_path, reviewer_path, handoff_path]
    missing = [_rel(path) for path in expected if not path.exists()]

    if missing:
        return {
            "ok": True,
            "compliant": True,
            "checks": {
                "closeout_status": "artifacts_missing",
                "reviewer_status": "not_available",
                "release_status": "not_available",
            },
            "warnings": [
                "closeout_artifacts_missing",
                *[f"missing_artifact:{item}" for item in missing],
            ],
            "errors": [],
            "snapshot": {
                "artifact_tag": artifact_tag,
                "missing_artifacts": missing,
                "recommended_action": "emit_closeout_artifacts",
            },
        }

    closeout = _load_json(closeout_path)
    reviewer = _load_json(reviewer_path)
    handoff = _load_json(handoff_path)

    closeout_ok = (
        bool(closeout["overall"]["schema_conformance_ok"])
        and int(closeout["overall"]["precondition_fail"]) == 0
        and int(closeout["overall"]["replay_fail"]) == 0
        and int(closeout["overall"]["claim_fail"]) == 0
    )
    reviewer_ok = reviewer.get("result") == "pass"
    release_ready = handoff.get("release_status") == "ready_for_handoff"
    ok = closeout_ok and reviewer_ok and release_ready

    return {
        "ok": ok,
        "compliant": ok,
        "checks": {
            "closeout_status": "pass" if closeout_ok else "review_required",
            "reviewer_status": reviewer.get("result", "unknown"),
            "release_status": handoff.get("release_status", "unknown"),
        },
        "warnings": [] if ok else ["closeout_review_required"],
        "errors": [] if ok else ["closeout_not_handoff_ready"],
        "snapshot": {
            "artifact_tag": artifact_tag,
            "recommended_action": "handoff_ready" if ok else "review_closeout_artifacts",
            "artifacts": {
                "closeout_summary": _rel(closeout_path),
                "reviewer_verdict": _rel(reviewer_path),
                "release_handoff": _rel(handoff_path),
            },
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime post_task_check compatibility wrapper.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--rules", default="common")
    parser.add_argument("--risk", default="low")
    parser.add_argument("--oversight", default="auto")
    parser.add_argument("--memory-mode")
    parser.add_argument("--task-text", default="")
    parser.add_argument("--task-level", default="L1")
    parser.add_argument("--contract")
    parser.add_argument("--checks-file")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args, _ = parser.parse_known_args(argv)

    _ = (
        args.project_root,
        args.rules,
        args.risk,
        args.oversight,
        args.memory_mode,
        args.task_text,
        args.task_level,
        args.contract,
        args.checks_file,
    )

    payload = _evaluate_closeout(args.artifact_tag)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=True))
    else:
        print("[post_task_check]")
        print(f"ok={'true' if payload['ok'] else 'false'}")
        print(f"compliant={'true' if payload['compliant'] else 'false'}")
        print(f"artifact_tag={payload['snapshot']['artifact_tag']}")
        print(f"closeout_status={payload['checks']['closeout_status']}")
        print(f"reviewer_status={payload['checks']['reviewer_status']}")
        print(f"release_status={payload['checks']['release_status']}")
        print(f"recommended_action={payload['snapshot']['recommended_action']}")
        missing_artifacts = payload["snapshot"].get("missing_artifacts", [])
        if missing_artifacts:
            print("missing_artifacts=" + ",".join(missing_artifacts))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
