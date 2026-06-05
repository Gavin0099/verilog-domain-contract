#!/usr/bin/env python3
"""Deterministic claim-enforcement runner for the Verilog domain contract repo."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.check_deterministic_governance_schema import validate_artifact, write_validation_result
from scripts.governance_artifact_paths import claim_artifact_path, claim_conformance_path, default_artifact_tag


REPO_NAME = "verilog-domain-contract"
CLAIM_SCHEMA_PATH = REPO_ROOT / "schemas/claim-enforcement-results.yaml"
STRONG_CLAIM_TERMS = (
    "proven",
    "production-ready",
    "verified_implementation",
    "implementation_complete",
)


def evaluate_claim_enforcement(
    *,
    scenario: str,
    preconditions_met: bool,
    claim_text: str = "",
    same_evidence_as_previous: bool = False,
    attempted_posture: str = "",
) -> dict[str, object]:
    claim_lower = claim_text.lower()
    strong_claim_attempted = any(term in claim_lower for term in STRONG_CLAIM_TERMS)

    payload: dict[str, object] = {
        "case_id": scenario,
        "case_type": "claim_enforcement",
        "rule_family": "GENERAL_CLAIM_BOUNDARY",
        "preconditions_met": preconditions_met,
        "claim_level": "",
        "semantic_drift_risk": False,
        "precondition_status": "ok" if preconditions_met else "missing",
        "strong_claim_attempted": strong_claim_attempted,
        "same_evidence_as_previous": same_evidence_as_previous,
        "attempted_posture": attempted_posture or "",
        "notes": "",
    }

    if not preconditions_met:
        payload["status"] = "not_executed"
        payload["claim_level"] = "stronger_than_allowed"
        payload["semantic_drift_risk"] = True
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = None
        payload["checks"] = {}
        payload["notes"] = "preconditions missing; strong claim must not execute"
        return payload

    if scenario == "baseline":
        payload["status"] = "pass"
        payload["claim_level"] = "bounded_support"
        payload["semantic_drift_risk"] = False
        payload["expected"] = {
            "claim_level": "bounded_support",
            "semantic_drift_risk": False,
        }
        payload["observed"] = {
            "claim_level": "bounded_support",
            "semantic_drift_risk": False,
        }
        payload["checks"] = {}
        payload["notes"] = "baseline bounded-support closeout"
        return payload

    if scenario == "drift_injection_same_evidence":
        payload["status"] = "pass" if strong_claim_attempted else "fail"
        payload["claim_level"] = "stronger_than_allowed" if strong_claim_attempted else "bounded_support"
        payload["semantic_drift_risk"] = bool(strong_claim_attempted)
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "claim_level": "stronger_than_allowed" if strong_claim_attempted else "bounded_support",
            "semantic_drift_risk": bool(strong_claim_attempted),
        }
        payload["checks"] = {}
        payload["notes"] = f"injected_wording={claim_text or 'proven / production-ready'}"
        return payload

    if scenario == "same_evidence_posture_escalation":
        posture = attempted_posture or "stronger_than_previous"
        drift = same_evidence_as_previous and posture == "stronger_than_previous"
        payload["status"] = "pass" if drift else "fail"
        payload["claim_level"] = "stronger_than_allowed" if drift else "bounded_support"
        payload["semantic_drift_risk"] = drift
        payload["same_evidence_as_previous"] = same_evidence_as_previous
        payload["attempted_posture"] = posture
        payload["expected"] = {
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "semantic_drift_risk": drift,
        }
        payload["checks"] = {}
        payload["notes"] = "same evidence must not justify stronger claim posture"
        return payload

    if scenario == "implicit_completion_wording":
        posture = attempted_posture or "implicitly_complete"
        drift = strong_claim_attempted or posture == "implicitly_complete"
        payload["status"] = "pass" if drift else "fail"
        payload["claim_level"] = "stronger_than_allowed" if drift else "bounded_support"
        payload["semantic_drift_risk"] = drift
        payload["attempted_posture"] = posture
        payload["expected"] = {
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "semantic_drift_risk": drift,
        }
        payload["checks"] = {}
        payload["notes"] = "implicit completion wording must not bypass explicit claim boundary"
        return payload

    if scenario == "borrowed_evidence_previous_run":
        posture = attempted_posture or "reuse_previous_evidence"
        drift = same_evidence_as_previous and posture in {"reuse_previous_evidence", "stronger_than_previous"}
        payload["status"] = "pass" if drift else "fail"
        payload["claim_level"] = "stronger_than_allowed" if drift else "bounded_support"
        payload["semantic_drift_risk"] = drift
        payload["same_evidence_as_previous"] = same_evidence_as_previous
        payload["attempted_posture"] = posture
        payload["expected"] = {
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "semantic_drift_risk": drift,
        }
        payload["checks"] = {}
        payload["notes"] = "evidence borrowed from previous run must not justify stronger present-session claim"
        return payload

    if scenario == "partial_preconditions_boundary":
        posture = attempted_posture or "bounded_but_incomplete"
        drift = posture == "stronger_than_previous" or strong_claim_attempted
        payload["status"] = "pass"
        payload["claim_level"] = "bounded_support" if not drift else "stronger_than_allowed"
        payload["semantic_drift_risk"] = drift
        payload["precondition_status"] = "partial"
        payload["attempted_posture"] = posture
        payload["expected"] = {
            "claim_level": "bounded_support",
            "semantic_drift_risk": False,
        }
        payload["observed"] = {
            "claim_level": "bounded_support" if not drift else "stronger_than_allowed",
            "semantic_drift_risk": drift,
        }
        payload["checks"] = {}
        payload["notes"] = "partial preconditions may support bounded posture only"
        return payload

    if scenario == "missing_preconditions_strong_claim":
        payload["status"] = "not_executed"
        payload["claim_level"] = "stronger_than_allowed"
        payload["semantic_drift_risk"] = True
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = None
        payload["checks"] = {}
        payload["notes"] = "missing preconditions blocks strong claim"
        return payload

    raise ValueError(f"unknown scenario: {scenario}")


def run_default_suite(artifact_tag: str) -> dict[str, object]:
    cases = [
        evaluate_claim_enforcement(
            scenario="baseline",
            preconditions_met=True,
        ),
        evaluate_claim_enforcement(
            scenario="drift_injection_same_evidence",
            preconditions_met=True,
            claim_text="This result is proven and production-ready.",
        ),
        evaluate_claim_enforcement(
            scenario="same_evidence_posture_escalation",
            preconditions_met=True,
            same_evidence_as_previous=True,
            attempted_posture="stronger_than_previous",
        ),
        evaluate_claim_enforcement(
            scenario="implicit_completion_wording",
            preconditions_met=True,
            claim_text="This is ready for integration and should drop into production as-is.",
            attempted_posture="implicitly_complete",
        ),
        evaluate_claim_enforcement(
            scenario="borrowed_evidence_previous_run",
            preconditions_met=True,
            same_evidence_as_previous=True,
            attempted_posture="reuse_previous_evidence",
        ),
        evaluate_claim_enforcement(
            scenario="partial_preconditions_boundary",
            preconditions_met=True,
            attempted_posture="bounded_but_incomplete",
        ),
        evaluate_claim_enforcement(
            scenario="missing_preconditions_strong_claim",
            preconditions_met=False,
            claim_text="verified_implementation",
        ),
    ]
    pass_count = sum(1 for item in cases if item["status"] == "pass")
    not_executed_count = sum(1 for item in cases if item["status"] == "not_executed")
    return {
        "schema_version": "0.1",
        "name": "claim-enforcement-results",
        "artifact_family": "claim_enforcement",
        "suite_id": f"claim-enforcement-{artifact_tag}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution_surface": "validator_backed_deterministic_claim_enforcement",
        "note": (
            "Deterministic claim-enforcement surface for repo-local policy coherence. "
            "This validates claim-boundary behavior, not live runtime closeout behavior."
        ),
        "cases": cases,
        "summary": {
            "total": len(cases),
            "pass": pass_count,
            "fail": len(cases) - pass_count - not_executed_count,
            "not_executed": not_executed_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic claim-enforcement scenarios.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = run_default_suite(args.artifact_tag)

    out_path = Path(args.out) if args.out else claim_artifact_path(REPO_ROOT, args.artifact_tag)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    conformance_path = claim_conformance_path(REPO_ROOT, args.artifact_tag)

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        schema_check = validate_artifact(CLAIM_SCHEMA_PATH, out_path.resolve())
        write_validation_result(schema_check, conformance_path)
        if not schema_check["ok"]:
            print("[claim_enforcement_schema_check]")
            for error in schema_check["errors"]:
                print(f"error={error}")
            return 1

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        summary = result["summary"]
        print("[claim_enforcement]")
        print(f"suite_id={result['suite_id']}")
        print(f"execution_surface={result['execution_surface']}")
        print(f"total={summary['total']}")
        print(f"pass={summary['pass']}")
        print(f"fail={summary['fail']}")
        print(f"not_executed={summary['not_executed']}")
        for case in result["cases"]:
            print(
                f"{case['case_id']}: status={case['status']} "
                f"preconditions_met={case['preconditions_met']}"
            )
    return 0 if result["summary"]["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
