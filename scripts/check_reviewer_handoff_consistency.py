#!/usr/bin/env python3
"""Validate consistency across reviewer verdict, bundle manifest, and release handoff."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    release_handoff_index_path,
    reviewer_bundle_manifest_path,
    reviewer_verdict_path,
)


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_consistency(artifact_tag: str) -> dict[str, object]:
    handoff_path = release_handoff_index_path(REPO_ROOT, artifact_tag)
    manifest_path = reviewer_bundle_manifest_path(REPO_ROOT, artifact_tag)
    verdict_path = reviewer_verdict_path(REPO_ROOT, artifact_tag)

    handoff = _load(handoff_path)
    manifest = _load(manifest_path)
    verdict = _load(verdict_path)

    closeout_bundle = next(
        bundle for bundle in manifest["bundles"] if bundle["bundle_name"] == "governance-closeout-artifacts"
    )
    reviewer_bundle = next(
        bundle for bundle in manifest["bundles"] if bundle["bundle_name"] == "governance-reviewer-artifacts"
    )

    checks = {
        "artifact_tag_match": (
            handoff.get("artifact_tag") == artifact_tag and manifest.get("artifact_tag") == artifact_tag
        ),
        "reviewer_verdict_entrypoint_match": (
            handoff["primary_entrypoints"]["reviewer_verdict"]
            == str(verdict_path.relative_to(REPO_ROOT)).replace("\\", "/")
        ),
        "bundle_manifest_entrypoint_match": (
            handoff["primary_entrypoints"]["bundle_manifest"]
            == str(manifest_path.relative_to(REPO_ROOT)).replace("\\", "/")
        ),
        "reviewer_bundle_contains_verdict": (
            str(verdict_path.relative_to(REPO_ROOT)).replace("\\", "/") in reviewer_bundle["files"]
        ),
        "closeout_bundle_contains_handoff": (
            handoff["primary_entrypoints"]["closeout_summary"] in closeout_bundle["files"]
            and handoff["primary_entrypoints"]["closeout_report"] in closeout_bundle["files"]
            and str(handoff_path.relative_to(REPO_ROOT)).replace("\\", "/") in closeout_bundle["files"]
        ),
        "reviewer_result_matches_handoff_surface": (
            handoff["surface_status"]["reviewer_verdict"]["result"] == verdict["result"]
        ),
        "reviewer_section_count_matches_handoff_surface": (
            handoff["surface_status"]["reviewer_verdict"]["sections"] == len(verdict["sections"])
        ),
        "release_status_consistent_with_verdict": (
            (handoff["release_status"] == "ready_for_handoff" and verdict["result"] == "pass")
            or (handoff["release_status"] != "ready_for_handoff")
        ),
    }

    ok = all(checks.values())
    return {
        "schema_version": "0.1",
        "name": "reviewer-handoff-consistency-check",
        "artifact_tag": artifact_tag,
        "ok": ok,
        "checks": checks,
        "artifacts": {
            "release_handoff": str(handoff_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "bundle_manifest": str(manifest_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "reviewer_verdict": str(verdict_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check reviewer handoff consistency.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = check_consistency(args.artifact_tag)
    out_path = Path(args.out) if args.out else REPO_ROOT / f"artifacts/governance/{args.artifact_tag}-reviewer-handoff-consistency.json"
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[reviewer_handoff_consistency]")
        print(f"artifact_tag={result['artifact_tag']}")
        print(f"ok={str(result['ok']).lower()}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for key, value in result["checks"].items():
            print(f"{key}={'pass' if value else 'fail'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
