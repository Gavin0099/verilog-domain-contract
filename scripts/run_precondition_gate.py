#!/usr/bin/env python3
"""Deterministic precondition-gate runner for Verilog domain contract coverage cases."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.check_deterministic_governance_schema import validate_artifact, write_validation_result
from scripts.governance_artifact_paths import (
    default_artifact_tag,
    precondition_gate_artifact_path,
    precondition_gate_conformance_path,
)
from scripts.precondition_gate_smoke import BOUNDARY_CASES, CASES, NEGATION_CASES, POSITIVE_CASES
from validators.precondition_gate_validator import evaluate_precondition_gate


SCHEMA_PATH = REPO_ROOT / "schemas/precondition-gate-results.yaml"


def _infer_rule_family(case: dict[str, object], verdict: dict[str, object]) -> str:
    refs = verdict.get("rule_refs") or case.get("expected_rule_refs") or []
    if refs:
        return str(list(refs)[0])
    cid = str(case["id"])
    explicit_map = {
        "PG-003": "RESET_DEFINITION_REQUIRED+HANDSHAKE_TIMING_DEFINITION_REQUIRED",
        "PG-005": "ASSIGNMENT_SEMANTICS_REQUIRED",
        "PG-007": "CDC_STRATEGY_REQUIRED",
        "PG-009": "FSM_CONTRACT_REQUIRED",
    }
    if cid in explicit_map:
        return explicit_map[cid]
    if "RESET" in cid:
        return "RESET_DEFINITION_REQUIRED"
    if "HS" in cid or cid == "PG-002":
        return "HANDSHAKE_TIMING_DEFINITION_REQUIRED"
    if "ASSIGN" in cid or cid in {"PG-004", "PG-005"}:
        return "ASSIGNMENT_SEMANTICS_REQUIRED"
    if "FSM" in cid or cid in {"PG-008", "PG-009"}:
        return "FSM_CONTRACT_REQUIRED"
    if "CDC" in cid or cid in {"PG-006", "PG-007"}:
        return "CDC_STRATEGY_REQUIRED"
    return "UNKNOWN_RULE"


def _run_case(case: dict[str, object]) -> dict[str, object]:
    verdict = evaluate_precondition_gate(str(case["task"]))
    mode_match = verdict["recommended_mode"] == case["expected_mode"]
    blocking_match = (
        verdict["blocking_effect"] == case["expected_blocking_effect"]
        if "expected_blocking_effect" in case
        else True
    )
    missing_match = (
        all(item in verdict["missing_preconditions"] for item in case["expected_missing"])
        if "expected_missing" in case
        else True
    )
    refs_match = (
        all(item in verdict["rule_refs"] for item in case["expected_rule_refs"])
        if "expected_rule_refs" in case
        else True
    )
    passed = mode_match and blocking_match and missing_match and refs_match
    return {
        "case_id": case["id"],
        "case_type": "precondition_gate",
        "rule_family": _infer_rule_family(case, verdict),
        "status": "pass" if passed else "fail",
        "preconditions_met": bool(verdict["ok"]),
        "expected": {
            "recommended_mode": case["expected_mode"],
            "blocking_effect": case.get("expected_blocking_effect", ""),
            "missing_preconditions": case.get("expected_missing", []),
            "rule_refs": case.get("expected_rule_refs", []),
        },
        "observed": {
            "recommended_mode": verdict["recommended_mode"],
            "blocking_effect": verdict["blocking_effect"],
        },
        "checks": {
            "mode_match": mode_match,
            "blocking_effect_match": blocking_match,
            "missing_match": missing_match,
            "rule_refs_match": refs_match,
        },
        "notes": f"missing={','.join(verdict['missing_preconditions']) or '(none)'}; rule_refs={','.join(verdict['rule_refs']) or '(none)'}",
    }


def _coverage_summary() -> dict[str, object]:
    groups = {
        "negation": NEGATION_CASES,
        "boundary": BOUNDARY_CASES,
        "positive": POSITIVE_CASES,
    }
    return {
        "groups": {
            group: {
                "count": len(group_cases),
                "case_ids": [str(case["id"]) for case in group_cases],
            }
            for group, group_cases in groups.items()
        },
        "total_cases": len(CASES),
    }


def run_suite(artifact_tag: str) -> dict[str, object]:
    cases = [_run_case(case) for case in CASES]
    pass_count = sum(1 for case in cases if case["status"] == "pass")
    return {
        "schema_version": "0.1",
        "name": "precondition-gate-results",
        "artifact_family": "precondition_gate",
        "suite_id": f"precondition-gate-{artifact_tag}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution_surface": "validator_backed_deterministic_precondition_gate",
        "note": (
            "Deterministic precondition-gate surface for repo-local validator coverage. "
            "This validates gate behavior against curated coverage cases, not live runtime requests."
        ),
        "coverage_summary": _coverage_summary(),
        "cases": cases,
        "summary": {
            "total": len(cases),
            "pass": pass_count,
            "fail": len(cases) - pass_count,
            "not_executed": 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic precondition-gate coverage suite.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = run_suite(args.artifact_tag)
    out_path = Path(args.out) if args.out else precondition_gate_artifact_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    conformance_path = precondition_gate_conformance_path(REPO_ROOT, args.artifact_tag)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    schema_check = validate_artifact(SCHEMA_PATH, out_path.resolve())
    write_validation_result(schema_check, conformance_path)
    if not schema_check["ok"]:
        print("[precondition_gate_schema_check]")
        for error in schema_check["errors"]:
            print(f"error={error}")
        return 1

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[precondition_gate_runner]")
        print(f"suite_id={result['suite_id']}")
        print(f"execution_surface={result['execution_surface']}")
        print(f"total={result['summary']['total']}")
        print(f"pass={result['summary']['pass']}")
        print(f"fail={result['summary']['fail']}")
        for case in result["cases"]:
            print(f"{case['case_id']}: status={case['status']} rule_family={case['rule_family']}")
    return 0 if result["summary"]["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
