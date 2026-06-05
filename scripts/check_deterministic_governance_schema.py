#!/usr/bin/env python3
"""Validate deterministic governance artifacts against repo-local extension schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run schema conformance checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TARGETS = (
    ("schemas/behavioral-replay-results.yaml", "artifacts/replay-results/2026-06-05-validator-replay.yaml"),
    ("schemas/claim-enforcement-results.yaml", "artifacts/claim-enforcement/checker-tests/2026-06-05-claim-enforcement-suite.json"),
)


def _load_doc(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _ordered_union(*groups: list[str]) -> list[str]:
    seen: list[str] = []
    for group in groups:
        for item in group:
            if item not in seen:
                seen.append(item)
    return seen


def _load_schema(schema_path: Path) -> dict[str, object]:
    schema = _load_doc(schema_path)
    extends = schema.get("extends")
    if not extends:
        return schema

    base_schema = _load_schema(REPO_ROOT / str(extends))
    merged = dict(schema)
    merged["fields"] = _ordered_union(base_schema.get("top_level_fields", []), schema.get("fields", []))
    merged["case_fields"] = _ordered_union(base_schema.get("case_fields", []), schema.get("case_fields", []))
    merged["summary_fields"] = _ordered_union(base_schema.get("summary_fields", []), schema.get("summary_fields", []))
    merged["observed_fields"] = _ordered_union(base_schema.get("observed_fields", []), schema.get("observed_fields", []))
    merged["checks_fields"] = _ordered_union(base_schema.get("checks_fields", []), schema.get("checks_fields", []))
    return merged


def _validate_required_fields(container: dict[str, object], required: list[str]) -> list[str]:
    return [field for field in required if field not in container]


def validate_artifact(schema_path: Path, artifact_path: Path) -> dict[str, object]:
    schema = _load_schema(schema_path)
    artifact = _load_doc(artifact_path)
    errors: list[str] = []

    missing_top = _validate_required_fields(artifact, schema.get("fields", []))
    if missing_top:
        errors.append(f"missing_top_level={','.join(missing_top)}")

    if artifact.get("name") != schema.get("name"):
        errors.append(f"name_mismatch=expected:{schema.get('name')} observed:{artifact.get('name')}")

    cases = artifact.get("cases")
    if not isinstance(cases, list):
        errors.append("cases_not_list")
        cases = []

    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case_{idx}_not_object")
            continue
        missing_case = _validate_required_fields(case, schema.get("case_fields", []))
        if missing_case:
            errors.append(f"case_{idx}_missing={','.join(missing_case)}")

        observed_required = schema.get("observed_fields", [])
        if observed_required:
            observed = case.get("observed")
            if observed is None:
                errors.append(f"case_{idx}_observed_missing")
            elif not isinstance(observed, dict):
                errors.append(f"case_{idx}_observed_not_object")
            else:
                missing_observed = _validate_required_fields(observed, observed_required)
                if missing_observed:
                    errors.append(f"case_{idx}_observed_missing={','.join(missing_observed)}")

        checks_required = schema.get("checks_fields", [])
        if checks_required:
            checks = case.get("checks")
            if not isinstance(checks, dict):
                errors.append(f"case_{idx}_checks_not_object")
            else:
                missing_checks = _validate_required_fields(checks, checks_required)
                if missing_checks:
                    errors.append(f"case_{idx}_checks_missing={','.join(missing_checks)}")

    summary = artifact.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary_not_object")
        summary = {}
    else:
        missing_summary = _validate_required_fields(summary, schema.get("summary_fields", []))
        if missing_summary:
            errors.append(f"summary_missing={','.join(missing_summary)}")

    total = summary.get("total")
    pass_count = summary.get("pass")
    fail_count = summary.get("fail")
    not_executed = summary.get("not_executed")
    if all(isinstance(item, int) for item in [total, pass_count, fail_count, not_executed]):
        if total != pass_count + fail_count + not_executed:
            errors.append("summary_total_mismatch")

    return {
        "schema": str(schema_path.relative_to(REPO_ROOT)),
        "artifact": str(artifact_path.relative_to(REPO_ROOT)),
        "ok": len(errors) == 0,
        "errors": errors,
    }


def write_validation_result(result: dict[str, object], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check deterministic governance artifact/schema conformance.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--schema")
    parser.add_argument("--artifact")
    parser.add_argument("--out")
    args = parser.parse_args()

    if bool(args.schema) != bool(args.artifact):
        raise SystemExit("--schema and --artifact must be provided together")

    targets = (
        [(args.schema, args.artifact)]
        if args.schema and args.artifact
        else list(DEFAULT_TARGETS)
    )

    results = [
        validate_artifact(REPO_ROOT / schema_path, REPO_ROOT / artifact_path)
        for schema_path, artifact_path in targets
    ]
    fail_count = sum(1 for item in results if not item["ok"])
    payload = {
        "total": len(results),
        "pass": len(results) - fail_count,
        "fail": fail_count,
        "results": results,
    }

    if args.out:
        write_validation_result(payload, (REPO_ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out))

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("[deterministic_governance_schema_check]")
        print(f"total={payload['total']}")
        print(f"pass={payload['pass']}")
        print(f"fail={payload['fail']}")
        for item in results:
            print(
                f"{item['schema']} -> {item['artifact']}: "
                f"{'PASS' if item['ok'] else 'FAIL'}"
            )
            for error in item["errors"]:
                print(f"  error={error}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
