#!/usr/bin/env python3
"""Deterministic session-start hook backed by release handoff artifacts."""

from __future__ import annotations

import argparse
import json
import sys

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    release_handoff_index_path,
    reviewer_verdict_path,
)
from runtime_hooks.core.artifact_runtime_context import load_json, missing_rel_paths, rel_repo


def _build_session_payload(artifact_tag: str, task_text: str, task_level: str) -> dict[str, object]:
    handoff_path = release_handoff_index_path(REPO_ROOT, artifact_tag)
    reviewer_path = reviewer_verdict_path(REPO_ROOT, artifact_tag)

    if not handoff_path.exists() or not reviewer_path.exists():
        missing = missing_rel_paths([handoff_path, reviewer_path])
        return {
            "ok": True,
            "project_root": str(REPO_ROOT),
            "task_level": task_level,
            "task_text": task_text,
            "state": {
                "artifact_tag": artifact_tag,
                "release_status": "not_available",
                "recommended_action": "emit_release_handoff",
            },
            "pre_task_check": {},
            "suggested_rules_preview": [],
            "suggested_skills": [],
            "suggested_agent": None,
            "rule_pack_suggestions": {},
            "governance_classification": {
                "effective_agent_class": "instruction_capable",
                "governance_strategy": "deterministic_runtime_context",
                "classification_evidence": {
                    "release_handoff": "missing",
                    "reviewer_verdict": "missing",
                },
            },
            "closeout_context": {
                "available": False,
                "artifact_tag": artifact_tag,
                "missing_artifacts": missing,
            },
        }

    handoff = load_json(handoff_path)
    reviewer = load_json(reviewer_path)
    release_status = handoff.get("release_status", "unknown")
    reviewer_result = reviewer.get("result", "unknown")

    return {
        "ok": True,
        "project_root": str(REPO_ROOT),
        "task_level": task_level,
        "task_text": task_text,
        "state": {
            "artifact_tag": artifact_tag,
            "release_status": release_status,
            "recommended_action": "use_release_handoff_context",
        },
        "pre_task_check": {},
        "suggested_rules_preview": [],
        "suggested_skills": [],
        "suggested_agent": None,
        "rule_pack_suggestions": {},
        "governance_classification": {
            "effective_agent_class": "instruction_capable",
            "governance_strategy": "deterministic_runtime_context",
            "classification_evidence": {
                "release_handoff": release_status,
                "reviewer_verdict": reviewer_result,
            },
        },
        "closeout_context": {
            "available": True,
            "artifact_tag": artifact_tag,
            "release_status": release_status,
            "reviewer_result": reviewer_result,
            "primary_entrypoints": handoff.get("primary_entrypoints", {}),
            "coverage_snapshot": handoff.get("coverage_snapshot", {}),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime session_start compatibility wrapper.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--plan", default="PLAN.md")
    parser.add_argument("--plan-path")
    parser.add_argument("--contract")
    parser.add_argument("--rules", default="common")
    parser.add_argument("--risk", default="low")
    parser.add_argument("--oversight", default="auto")
    parser.add_argument("--memory-mode")
    parser.add_argument("--task-text", default="")
    parser.add_argument("--task-level", default="L1")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args, _ = parser.parse_known_args(argv)

    _ = (
        args.project_root,
        args.plan,
        args.plan_path,
        args.contract,
        args.rules,
        args.risk,
        args.oversight,
        args.memory_mode,
        args.task_text,
        args.task_level,
    )

    payload = _build_session_payload(args.artifact_tag, args.task_text, args.task_level)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=True))
    else:
        print("[session_start]")
        print(f"ok={'true' if payload['ok'] else 'false'}")
        print(f"artifact_tag={payload['state']['artifact_tag']}")
        print(f"release_status={payload['state']['release_status']}")
        print(f"closeout_context_available={'true' if payload['closeout_context']['available'] else 'false'}")
        print(f"recommended_action={payload['state']['recommended_action']}")
        missing_artifacts = payload["closeout_context"].get("missing_artifacts", [])
        if missing_artifacts:
            print("missing_artifacts=" + ",".join(missing_artifacts))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
