#!/usr/bin/env python3
"""Validate governance release handoff artifacts against the repo-local schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run governance release handoff schema checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
SCHEMA_PATH = REPO_ROOT / "schemas/governance-release-handoff.yaml"

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    release_handoff_conformance_path,
    release_handoff_index_path,
)


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_release_handoff(artifact_path: Path) -> dict[str, object]:
    schema = _load_yaml(SCHEMA_PATH)
    payload = _load_json(artifact_path)
    errors: list[str] = []

    missing_top = _missing_fields(payload, schema["fields"])
    if missing_top:
        errors.append("missing_top_level=" + ",".join(missing_top))

    if payload.get("name") != schema.get("name"):
        errors.append(f"name_mismatch=expected:{schema.get('name')} observed:{payload.get('name')}")

    release_status = payload.get("release_status")
    if release_status not in set(schema.get("allowed_release_status", [])):
        errors.append(f"invalid_release_status={release_status}")

    entrypoints = payload.get("primary_entrypoints")
    if not isinstance(entrypoints, dict):
        errors.append("primary_entrypoints_not_object")
    else:
        missing_entrypoints = _missing_fields(entrypoints, schema["entrypoint_fields"])
        if missing_entrypoints:
            errors.append("primary_entrypoints_missing=" + ",".join(missing_entrypoints))
        for key, value in entrypoints.items():
            if not isinstance(value, str) or not value:
                errors.append(f"primary_entrypoint_invalid={key}")

    surface_status = payload.get("surface_status")
    if not isinstance(surface_status, dict):
        errors.append("surface_status_not_object")
    else:
        missing_surfaces = _missing_fields(surface_status, schema["surface_status_fields"])
        if missing_surfaces:
            errors.append("surface_status_missing=" + ",".join(missing_surfaces))

    coverage_snapshot = payload.get("coverage_snapshot")
    if not isinstance(coverage_snapshot, dict):
        errors.append("coverage_snapshot_not_object")
    else:
        missing_coverage = _missing_fields(coverage_snapshot, schema["coverage_snapshot_fields"])
        if missing_coverage:
            errors.append("coverage_snapshot_missing=" + ",".join(missing_coverage))

    review_sequence = payload.get("recommended_review_sequence")
    if not isinstance(review_sequence, list) or len(review_sequence) == 0:
        errors.append("recommended_review_sequence_invalid")
    else:
        for idx, item in enumerate(review_sequence):
            if not isinstance(item, dict):
                errors.append(f"review_step_{idx}_not_object")
                continue
            missing_step_fields = _missing_fields(item, ["step", "artifact", "why"])
            if missing_step_fields:
                errors.append(f"review_step_{idx}_missing=" + ",".join(missing_step_fields))

    bundles = payload.get("bundles")
    if not isinstance(bundles, list) or len(bundles) == 0:
        errors.append("bundles_invalid")

    return {
        "schema": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "artifact": str(artifact_path.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def write_validation_result(result: dict[str, object], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check governance release handoff artifact/schema conformance.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--artifact")
    parser.add_argument("--out")
    args = parser.parse_args()

    artifact_path = Path(args.artifact) if args.artifact else release_handoff_index_path(REPO_ROOT, args.artifact_tag)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    result = validate_release_handoff(artifact_path)
    payload = {
        "total": 1,
        "pass": 1 if result["ok"] else 0,
        "fail": 0 if result["ok"] else 1,
        "results": [result],
    }

    out_path = Path(args.out) if args.out else release_handoff_conformance_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    write_validation_result(payload, out_path)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[governance_release_handoff_schema_check]")
        print(f"total={payload['total']}")
        print(f"pass={payload['pass']}")
        print(f"fail={payload['fail']}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for item in payload["results"]:
            print(f"{item['schema']} -> {item['artifact']}: {'PASS' if item['ok'] else 'FAIL'}")
            for error in item["errors"]:
                print(f"  error={error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
