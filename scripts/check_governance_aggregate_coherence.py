#!/usr/bin/env python3
"""Check coherence across closeout summary, reviewer verdict, and release handoff."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    aggregate_coherence_path,
    closeout_summary_path,
    default_artifact_tag,
    release_handoff_index_path,
    reviewer_verdict_path,
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def check_coherence(artifact_tag: str) -> dict[str, object]:
    closeout_path = closeout_summary_path(REPO_ROOT, artifact_tag)
    handoff_path = release_handoff_index_path(REPO_ROOT, artifact_tag)
    reviewer_path = reviewer_verdict_path(REPO_ROOT, artifact_tag)

    closeout = _load(closeout_path)
    handoff = _load(handoff_path)
    reviewer = _load(reviewer_path)

    overall = closeout["overall"]
    surfaces = closeout["surfaces"]
    expected_ready = (
        bool(overall["schema_conformance_ok"])
        and overall["precondition_fail"] == 0
        and overall["replay_fail"] == 0
        and overall["claim_fail"] == 0
        and overall["runtime_hook_fail"] == 0
        and reviewer["result"] == "pass"
    )

    checks = {
        "artifact_tag_match": handoff.get("artifact_tag") == artifact_tag,
        "precondition_summary_matches_handoff": (
            handoff["surface_status"]["precondition_gate"]["fail"] == surfaces["precondition_gate"]["summary"]["fail"]
        ),
        "replay_summary_matches_handoff": (
            handoff["surface_status"]["behavioral_replay"]["fail"] == surfaces["behavioral_replay"]["summary"]["fail"]
        ),
        "claim_summary_matches_handoff": (
            handoff["surface_status"]["claim_enforcement"]["fail"] == surfaces["claim_enforcement"]["summary"]["fail"]
        ),
        "runtime_summary_matches_handoff": (
            handoff["surface_status"]["runtime_hooks"]["fail"] == surfaces["runtime_hooks"]["summary"]["fail"]
            and bool(handoff["coverage_snapshot"]["runtime_hooks"]["overall_ok"])
            == bool(surfaces["runtime_hooks"]["summary"]["overall_ok"])
        ),
        "reviewer_result_matches_handoff": handoff["surface_status"]["reviewer_verdict"]["result"] == reviewer["result"],
        "reviewer_sections_match_handoff": handoff["surface_status"]["reviewer_verdict"]["sections"] == len(reviewer["sections"]),
        "release_status_matches_aggregate_inputs": (
            (handoff["release_status"] == "ready_for_handoff") == expected_ready
        ),
    }

    ok = all(checks.values())
    return {
        "schema_version": "0.1",
        "name": "governance-aggregate-coherence-check",
        "artifact_tag": artifact_tag,
        "ok": ok,
        "checks": checks,
        "artifacts": {
            "closeout_summary": _rel(closeout_path),
            "release_handoff": _rel(handoff_path),
            "reviewer_verdict": _rel(reviewer_path),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check governance aggregate coherence.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = check_coherence(args.artifact_tag)
    out_path = Path(args.out) if args.out else aggregate_coherence_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[governance_aggregate_coherence]")
        print(f"artifact_tag={result['artifact_tag']}")
        print(f"ok={str(result['ok']).lower()}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for key, value in result["checks"].items():
            print(f"{key}={'pass' if value else 'fail'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
