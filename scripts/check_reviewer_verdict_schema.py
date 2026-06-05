#!/usr/bin/env python3
"""Validate reviewer checklist verdict artifacts against the repo-local reviewer verdict schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run reviewer verdict schema checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
VERDICT_SCHEMA = REPO_ROOT / "schemas/reviewer-checklist-verdict.yaml"

from scripts.governance_artifact_paths import (
    default_artifact_tag,
    reviewer_verdict_conformance_path,
    reviewer_verdict_path,
)


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_verdict(verdict_artifact: Path) -> dict[str, object]:
    schema = _load_yaml(VERDICT_SCHEMA)
    payload = _load_json(verdict_artifact)
    errors: list[str] = []

    missing_top = _missing_fields(payload, schema["fields"])
    if missing_top:
        errors.append("missing_top_level=" + ",".join(missing_top))

    if payload.get("name") != schema.get("name"):
        errors.append(f"name_mismatch=expected:{schema.get('name')} observed:{payload.get('name')}")

    result = payload.get("result")
    if result not in {"pass", "fail"}:
        errors.append(f"invalid_result={result}")

    sections = payload.get("sections")
    if not isinstance(sections, list):
        errors.append("sections_not_list")
        sections = []

    for idx, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(f"section_{idx}_not_object")
            continue

        missing_section = _missing_fields(section, schema["section_fields"])
        if missing_section:
            errors.append(f"section_{idx}_missing=" + ",".join(missing_section))

        section_result = section.get("result")
        if section_result not in {"pass", "fail"}:
            errors.append(f"section_{idx}_invalid_result={section_result}")

        items = section.get("items")
        if not isinstance(items, list):
            errors.append(f"section_{idx}_items_not_list")
            continue

        for item_idx, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"section_{idx}_item_{item_idx}_not_object")
                continue

            missing_item = _missing_fields(item, schema["item_fields"])
            if missing_item:
                errors.append(f"section_{idx}_item_{item_idx}_missing=" + ",".join(missing_item))

            item_result = item.get("result")
            if item_result not in {"pass", "fail"}:
                errors.append(f"section_{idx}_item_{item_idx}_invalid_result={item_result}")

            evidence = item.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"section_{idx}_item_{item_idx}_evidence_not_list")

    return {
        "schema": str(VERDICT_SCHEMA.relative_to(REPO_ROOT)),
        "artifact": str(verdict_artifact.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def write_validation_result(result: dict[str, object], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check reviewer verdict artifact/schema conformance.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--artifact")
    parser.add_argument("--out")
    args = parser.parse_args()

    artifact_path = Path(args.artifact) if args.artifact else reviewer_verdict_path(REPO_ROOT, args.artifact_tag)
    if not artifact_path.is_absolute():
        artifact_path = REPO_ROOT / artifact_path

    result = validate_verdict(artifact_path)
    payload = {
        "total": 1,
        "pass": 1 if result["ok"] else 0,
        "fail": 0 if result["ok"] else 1,
        "results": [result],
    }

    out_path = Path(args.out) if args.out else reviewer_verdict_conformance_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    write_validation_result(payload, out_path)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[reviewer_verdict_schema_check]")
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
