#!/usr/bin/env python3
"""Build a reviewer-facing manifest for governance artifact bundles under one artifact tag."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    claim_artifact_path,
    claim_conformance_path,
    closeout_report_conformance_path,
    closeout_report_path,
    closeout_summary_conformance_path,
    closeout_summary_path,
    default_artifact_tag,
    precondition_gate_artifact_path,
    precondition_gate_conformance_path,
    replay_artifact_path,
    replay_conformance_path,
    reviewer_bundle_manifest_path,
    reviewer_verdict_conformance_path,
    reviewer_verdict_path,
)


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def build_manifest(artifact_tag: str) -> dict[str, object]:
    precondition_artifact = precondition_gate_artifact_path(REPO_ROOT, artifact_tag)
    precondition_conformance = precondition_gate_conformance_path(REPO_ROOT, artifact_tag)
    replay_artifact = replay_artifact_path(REPO_ROOT, artifact_tag)
    replay_conformance = replay_conformance_path(REPO_ROOT, artifact_tag)
    claim_artifact = claim_artifact_path(REPO_ROOT, artifact_tag)
    claim_conformance = claim_conformance_path(REPO_ROOT, artifact_tag)
    closeout_summary = closeout_summary_path(REPO_ROOT, artifact_tag)
    closeout_report = closeout_report_path(REPO_ROOT, artifact_tag)
    closeout_summary_conformance = closeout_summary_conformance_path(REPO_ROOT, artifact_tag)
    closeout_report_conformance = closeout_report_conformance_path(REPO_ROOT, artifact_tag)
    reviewer_verdict = reviewer_verdict_path(REPO_ROOT, artifact_tag)
    reviewer_verdict_conformance = reviewer_verdict_conformance_path(REPO_ROOT, artifact_tag)

    return {
        "schema_version": "0.1",
        "name": "governance-bundle-manifest",
        "artifact_tag": artifact_tag,
        "bundles": [
            {
                "bundle_name": "governance-precondition-artifacts",
                "purpose": "Precondition-gate evidence, grouped coverage summary, and precondition schema conformance.",
                "files": [_rel(precondition_artifact), _rel(precondition_conformance)],
            },
            {
                "bundle_name": "governance-replay-artifacts",
                "purpose": "Replay rule-behavior evidence and replay schema conformance.",
                "files": [_rel(replay_artifact), _rel(replay_conformance)],
            },
            {
                "bundle_name": "governance-claim-artifacts",
                "purpose": "Claim-enforcement evidence and claim schema conformance.",
                "files": [_rel(claim_artifact), _rel(claim_conformance)],
            },
            {
                "bundle_name": "governance-closeout-artifacts",
                "purpose": "Aggregate closeout summary/report and closeout schema conformance.",
                "files": [
                    _rel(closeout_summary),
                    _rel(closeout_report),
                    _rel(closeout_summary_conformance),
                    _rel(closeout_report_conformance),
                ],
            },
            {
                "bundle_name": "governance-reviewer-artifacts",
                "purpose": "Executable reviewer verdict plus reviewer-verdict schema conformance and bundle index.",
                "files": [
                    _rel(reviewer_verdict),
                    _rel(reviewer_verdict_conformance),
                    _rel(reviewer_bundle_manifest_path(REPO_ROOT, artifact_tag)),
                ],
            },
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build governance artifact bundle manifest.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    manifest = build_manifest(args.artifact_tag)
    out_path = Path(args.out) if args.out else reviewer_bundle_manifest_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("[governance_bundle_manifest]")
        print(f"artifact_tag={manifest['artifact_tag']}")
        print(f"bundles={len(manifest['bundles'])}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for bundle in manifest["bundles"]:
            print(f"{bundle['bundle_name']}: {len(bundle['files'])} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
