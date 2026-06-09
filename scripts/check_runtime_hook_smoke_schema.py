#!/usr/bin/env python3
"""Validate runtime hook smoke artifacts against the repo-local schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run runtime hook smoke schema checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
SCHEMA_PATH = REPO_ROOT / "schemas/runtime-hook-smoke.yaml"

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    runtime_hook_smoke_conformance_path,
    runtime_hook_smoke_path,
)


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_runtime_hook_smoke(artifact_path: Path) -> dict[str, object]:
    schema = _load_yaml(SCHEMA_PATH)
    payload = _load_json(artifact_path)
    errors: list[str] = []

    missing_top = _missing_fields(payload, schema["fields"])
    if missing_top:
        errors.append("missing_top_level=" + ",".join(missing_top))

    if payload.get("name") != schema.get("name"):
        errors.append(f"name_mismatch=expected:{schema.get('name')} observed:{payload.get('name')}")

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary_not_object")
    else:
        missing_summary = _missing_fields(summary, schema["summary_fields"])
        if missing_summary:
            errors.append("summary_missing=" + ",".join(missing_summary))

    checks = payload.get("checks")
    if not isinstance(checks, list) or len(checks) == 0:
        errors.append("checks_invalid")
    else:
        for idx, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"check_{idx}_not_object")
                continue
            missing_check = _missing_fields(check, schema["check_fields"])
            if missing_check:
                errors.append(f"check_{idx}_missing=" + ",".join(missing_check))

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
    parser = argparse.ArgumentParser(description="Check runtime hook smoke artifact/schema conformance.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--artifact")
    parser.add_argument("--out")
    args = parser.parse_args()

    artifact_path = Path(args.artifact) if args.artifact else runtime_hook_smoke_path(REPO_ROOT, args.artifact_tag)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    result = validate_runtime_hook_smoke(artifact_path)
    payload = {
        "total": 1,
        "pass": 1 if result["ok"] else 0,
        "fail": 0 if result["ok"] else 1,
        "results": [result],
    }

    out_path = Path(args.out) if args.out else runtime_hook_smoke_conformance_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    write_validation_result(payload, out_path)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[runtime_hook_smoke_schema_check]")
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
