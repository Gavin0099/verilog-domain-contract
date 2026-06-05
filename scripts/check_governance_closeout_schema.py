#!/usr/bin/env python3
"""Validate governance closeout summary JSON and markdown report against repo-local closeout schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run governance closeout schema checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_SCHEMA = REPO_ROOT / "schemas/governance-closeout-summary.yaml"
REPORT_SCHEMA = REPO_ROOT / "schemas/governance-closeout-report.yaml"
SUMMARY_ARTIFACT = REPO_ROOT / "artifacts/closeout/2026-06-05-governance-closeout-summary.json"
REPORT_ARTIFACT = REPO_ROOT / "artifacts/closeout/2026-06-05-governance-closeout-summary.md"


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_summary() -> dict[str, object]:
    schema = _load_yaml(SUMMARY_SCHEMA)
    payload = _load_json(SUMMARY_ARTIFACT)
    errors: list[str] = []

    missing_top = _missing_fields(payload, schema["fields"])
    if missing_top:
        errors.append("missing_top_level=" + ",".join(missing_top))

    generated_from = payload.get("generated_from")
    if not isinstance(generated_from, dict):
        errors.append("generated_from_not_object")
    else:
        missing_generated = _missing_fields(generated_from, schema["generated_from_fields"])
        if missing_generated:
            errors.append("generated_from_missing=" + ",".join(missing_generated))

    surfaces = payload.get("surfaces")
    if not isinstance(surfaces, dict):
        errors.append("surfaces_not_object")
    else:
        for surface_name in ("behavioral_replay", "claim_enforcement"):
            surface = surfaces.get(surface_name)
            if not isinstance(surface, dict):
                errors.append(f"{surface_name}_not_object")
                continue
            missing_surface = _missing_fields(surface, schema["surface_fields"])
            if missing_surface:
                errors.append(f"{surface_name}_missing=" + ",".join(missing_surface))
            summary = surface.get("summary")
            if not isinstance(summary, dict):
                errors.append(f"{surface_name}_summary_not_object")
            else:
                missing_summary = _missing_fields(summary, schema["surface_summary_fields"])
                if missing_summary:
                    errors.append(f"{surface_name}_summary_missing=" + ",".join(missing_summary))

    overall = payload.get("overall")
    if not isinstance(overall, dict):
        errors.append("overall_not_object")
    else:
        missing_overall = _missing_fields(overall, schema["overall_fields"])
        if missing_overall:
            errors.append("overall_missing=" + ",".join(missing_overall))

    return {
        "schema": str(SUMMARY_SCHEMA.relative_to(REPO_ROOT)),
        "artifact": str(SUMMARY_ARTIFACT.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def validate_report() -> dict[str, object]:
    schema = _load_yaml(REPORT_SCHEMA)
    text = REPORT_ARTIFACT.read_text(encoding="utf-8")
    errors: list[str] = []

    for heading in schema["required_headings"]:
        if heading not in text:
            errors.append(f"missing_heading={heading}")

    return {
        "schema": str(REPORT_SCHEMA.relative_to(REPO_ROOT)),
        "artifact": str(REPORT_ARTIFACT.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check governance closeout summary/report schema conformance.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    results = [validate_summary(), validate_report()]
    fail = sum(1 for item in results if not item["ok"])
    payload = {"total": len(results), "pass": len(results) - fail, "fail": fail, "results": results}

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[governance_closeout_schema_check]")
        print(f"total={payload['total']}")
        print(f"pass={payload['pass']}")
        print(f"fail={payload['fail']}")
        for item in results:
            print(f"{item['schema']} -> {item['artifact']}: {'PASS' if item['ok'] else 'FAIL'}")
            for error in item["errors"]:
                print(f"  error={error}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
