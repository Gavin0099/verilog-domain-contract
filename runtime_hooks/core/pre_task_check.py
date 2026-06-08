#!/usr/bin/env python3
"""Deterministic pre-task runtime hook backed by precondition artifacts."""

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
    precondition_gate_artifact_path,
)


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _build_pre_task_payload(artifact_tag: str) -> dict[str, object]:
    precondition_path = precondition_gate_artifact_path(REPO_ROOT, artifact_tag)
    closeout_path = closeout_summary_path(REPO_ROOT, artifact_tag)

    if not precondition_path.exists():
        payload = {
            "decision_boundary": {
                "artifact_status": "artifacts_missing",
                "suite_status": "not_available",
                "coverage_status": "not_available",
            },
            "boundary_effect": "warn",
            "preconditions_checked": [],
            "effect": "warn",
            "signals_checked": [],
            "observations": [],
            "snapshot": {
                "artifact_tag": artifact_tag,
                "recommended_action": "emit_precondition_artifact",
                "missing_artifacts": [_rel(precondition_path)],
            },
        }
        payload["ok"] = True
        return payload

    precondition = _load_json(precondition_path)
    closeout = _load_json(closeout_path) if closeout_path.exists() else None

    summary = precondition.get("summary", {})
    coverage = precondition.get("coverage_summary", {})
    groups = coverage.get("groups", {}) if isinstance(coverage, dict) else {}
    required_groups = ["negation", "boundary", "positive"]
    missing_groups = [
        group_name
        for group_name in required_groups
        if not isinstance(groups.get(group_name), dict) or int(groups[group_name].get("count", 0)) <= 0
    ]
    fail_count = int(summary.get("fail", 0))
    suite_ok = fail_count == 0
    coverage_ok = not missing_groups and int(coverage.get("total_cases", 0)) > 0
    closeout_status = "not_available"
    if isinstance(closeout, dict):
        closeout_status = (
            "pass"
            if int(closeout.get("overall", {}).get("precondition_fail", 0)) == 0
            else "review_required"
        )
    ok = suite_ok and coverage_ok
    effect = "pass" if ok else "escalate"

    checks = [
        {
            "type": "precondition_gate_suite_health",
            "applies": True,
            "present": suite_ok,
            "action": "pass" if suite_ok else "restrict_code_generation_and_escalate",
            "reason": None if suite_ok else f"deterministic precondition suite reports fail={fail_count}",
        },
        {
            "type": "precondition_gate_coverage_groups",
            "applies": True,
            "present": coverage_ok,
            "action": "pass" if coverage_ok else "analysis_only",
            "reason": None if coverage_ok else f"missing_or_empty_groups={','.join(missing_groups)}",
        },
    ]

    payload = {
        "decision_boundary": {
            "artifact_status": "present",
            "suite_status": "pass" if suite_ok else "review_required",
            "coverage_status": "pass" if coverage_ok else "review_required",
            "closeout_status": closeout_status,
            "summary": summary,
            "coverage_summary": coverage,
        },
        "boundary_effect": effect,
        "preconditions_checked": checks,
        "effect": effect,
        "signals_checked": [
            {
                "signal": "precondition_gate_artifact_available",
                "triggered": True,
                "action": "pass",
            }
        ],
        "observations": [
            {
                "observation": "precondition_gate_artifact_loaded",
                "artifact": _rel(precondition_path),
                "closeout_artifact": _rel(closeout_path) if closeout_path.exists() else None,
            }
        ],
        "snapshot": {
            "artifact_tag": artifact_tag,
            "recommended_action": "proceed_with_runtime_contract" if ok else "review_precondition_surface",
            "artifacts": {
                "precondition_gate": _rel(precondition_path),
                "closeout_summary": _rel(closeout_path) if closeout_path.exists() else None,
            },
        },
    }
    payload["ok"] = ok
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime pre_task_check compatibility wrapper.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--rules", default="common")
    parser.add_argument("--risk", default="low")
    parser.add_argument("--oversight", default="auto")
    parser.add_argument("--memory-mode")
    parser.add_argument("--task-text", default="")
    parser.add_argument("--task-level", default="L1")
    parser.add_argument("--contract")
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
    )

    payload = _build_pre_task_payload(args.artifact_tag)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=True))
    else:
        print("[pre_task_check]")
        print(f"ok={'true' if payload['ok'] else 'false'}")
        print(f"artifact_tag={payload['snapshot']['artifact_tag']}")
        print(f"boundary_effect={payload['boundary_effect']}")
        print(f"suite_status={payload['decision_boundary']['suite_status']}")
        print(f"coverage_status={payload['decision_boundary']['coverage_status']}")
        print(f"recommended_action={payload['snapshot']['recommended_action']}")
        missing_artifacts = payload["snapshot"].get("missing_artifacts", [])
        if missing_artifacts:
            print("missing_artifacts=" + ",".join(missing_artifacts))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
