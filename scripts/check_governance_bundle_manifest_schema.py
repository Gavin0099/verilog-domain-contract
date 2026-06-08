#!/usr/bin/env python3
"""Validate governance bundle manifest artifacts against the repo-local manifest schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run governance bundle manifest schema checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
MANIFEST_SCHEMA = REPO_ROOT / "schemas/governance-bundle-manifest.yaml"

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    reviewer_bundle_manifest_conformance_path,
    reviewer_bundle_manifest_path,
)


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_manifest(manifest_artifact: Path) -> dict[str, object]:
    schema = _load_yaml(MANIFEST_SCHEMA)
    payload = _load_json(manifest_artifact)
    errors: list[str] = []

    missing_top = _missing_fields(payload, schema["fields"])
    if missing_top:
        errors.append("missing_top_level=" + ",".join(missing_top))

    if payload.get("name") != schema.get("name"):
        errors.append(f"name_mismatch=expected:{schema.get('name')} observed:{payload.get('name')}")

    bundles = payload.get("bundles")
    if not isinstance(bundles, list):
        errors.append("bundles_not_list")
        bundles = []

    expected_bundle_names = schema.get("expected_bundle_names", [])
    if len(bundles) != len(expected_bundle_names):
        errors.append(f"bundle_count_mismatch={len(bundles)}")

    seen_bundle_names: list[str] = []
    for idx, bundle in enumerate(bundles):
        if not isinstance(bundle, dict):
            errors.append(f"bundle_{idx}_not_object")
            continue

        missing_bundle = _missing_fields(bundle, schema["bundle_fields"])
        if missing_bundle:
            errors.append(f"bundle_{idx}_missing=" + ",".join(missing_bundle))

        bundle_name = bundle.get("bundle_name")
        if isinstance(bundle_name, str):
            if bundle_name in seen_bundle_names:
                errors.append(f"duplicate_bundle_name={bundle_name}")
            seen_bundle_names.append(bundle_name)

        files = bundle.get("files")
        if not isinstance(files, list):
            errors.append(f"bundle_{idx}_files_not_list")
            continue
        if len(files) == 0:
            errors.append(f"bundle_{idx}_files_empty")

    if isinstance(expected_bundle_names, list):
        missing_expected = [name for name in expected_bundle_names if name not in seen_bundle_names]
        if missing_expected:
            errors.append("missing_expected_bundle_names=" + ",".join(missing_expected))

    return {
        "schema": str(MANIFEST_SCHEMA.relative_to(REPO_ROOT)),
        "artifact": str(manifest_artifact.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def write_validation_result(result: dict[str, object], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check governance bundle manifest schema conformance.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--artifact")
    parser.add_argument("--out")
    args = parser.parse_args()

    artifact_path = Path(args.artifact) if args.artifact else reviewer_bundle_manifest_path(REPO_ROOT, args.artifact_tag)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    result = validate_manifest(artifact_path)
    payload = {
        "total": 1,
        "pass": 1 if result["ok"] else 0,
        "fail": 0 if result["ok"] else 1,
        "results": [result],
    }

    out_path = Path(args.out) if args.out else reviewer_bundle_manifest_conformance_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    write_validation_result(payload, out_path)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[governance_bundle_manifest_schema_check]")
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
