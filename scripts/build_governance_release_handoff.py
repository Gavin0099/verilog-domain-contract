#!/usr/bin/env python3
"""Build a single release-style handoff index from closeout, reviewer, and manifest artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    closeout_report_path,
    closeout_summary_path,
    default_artifact_tag,
    release_handoff_index_path,
    reviewer_bundle_manifest_path,
    reviewer_verdict_path,
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def build_handoff(artifact_tag: str) -> dict[str, object]:
    closeout_summary_artifact = closeout_summary_path(REPO_ROOT, artifact_tag)
    closeout_report_artifact = closeout_report_path(REPO_ROOT, artifact_tag)
    reviewer_verdict_artifact = reviewer_verdict_path(REPO_ROOT, artifact_tag)
    bundle_manifest_artifact = reviewer_bundle_manifest_path(REPO_ROOT, artifact_tag)

    closeout = _load(closeout_summary_artifact)
    reviewer = _load(reviewer_verdict_artifact)
    manifest = _load(bundle_manifest_artifact)

    release_ok = (
        bool(closeout["overall"]["schema_conformance_ok"])
        and closeout["overall"]["precondition_fail"] == 0
        and closeout["overall"]["replay_fail"] == 0
        and closeout["overall"]["claim_fail"] == 0
        and reviewer["result"] == "pass"
    )

    return {
        "schema_version": "0.1",
        "name": "governance-release-handoff",
        "artifact_tag": artifact_tag,
        "release_status": "ready_for_handoff" if release_ok else "review_required",
        "primary_entrypoints": {
            "closeout_summary": _rel(closeout_summary_artifact),
            "closeout_report": _rel(closeout_report_artifact),
            "reviewer_verdict": _rel(reviewer_verdict_artifact),
            "bundle_manifest": _rel(bundle_manifest_artifact),
        },
        "surface_status": {
            "precondition_gate": closeout["surfaces"]["precondition_gate"]["summary"],
            "behavioral_replay": closeout["surfaces"]["behavioral_replay"]["summary"],
            "claim_enforcement": closeout["surfaces"]["claim_enforcement"]["summary"],
            "reviewer_verdict": {
                "result": reviewer["result"],
                "sections": len(reviewer["sections"]),
            },
        },
        "coverage_snapshot": {
            "precondition_gate": reviewer["coverage_summary"]["precondition_gate"],
            "behavioral_replay": closeout["surfaces"]["behavioral_replay"]["coverage_summary"],
            "claim_enforcement": closeout["surfaces"]["claim_enforcement"]["coverage_summary"],
        },
        "recommended_review_sequence": [
            {
                "step": 1,
                "artifact": _rel(reviewer_verdict_artifact),
                "why": "Fastest top-level verdict and per-section result surface.",
            },
            {
                "step": 2,
                "artifact": _rel(closeout_summary_artifact),
                "why": "Aggregate precondition/replay/claim status and coverage snapshot.",
            },
            {
                "step": 3,
                "artifact": _rel(bundle_manifest_artifact),
                "why": "Resolve the exact bundle/files to download for deeper review.",
            },
            {
                "step": 4,
                "artifact": _rel(closeout_report_artifact),
                "why": "Human-readable closeout narrative for handoff consumption.",
            },
        ],
        "bundles": manifest["bundles"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build governance release handoff index.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    handoff = build_handoff(args.artifact_tag)
    out_path = Path(args.out) if args.out else release_handoff_index_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(handoff, ensure_ascii=False, indent=2))
    else:
        print("[governance_release_handoff]")
        print(f"artifact_tag={handoff['artifact_tag']}")
        print(f"release_status={handoff['release_status']}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
