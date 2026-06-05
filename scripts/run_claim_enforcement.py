#!/usr/bin/env python3
"""Deterministic claim-enforcement runner for the Verilog domain contract repo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_NAME = "verilog-domain-contract"
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
        "repo": REPO_NAME,
        "scenario": scenario,
        "preconditions_met": preconditions_met,
    }

    if not preconditions_met:
        payload["scenario_result"] = "not_executed"
        payload["precondition_status"] = "missing"
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = None
        return payload

    payload["precondition_status"] = "ok"

    if scenario == "baseline":
        payload["scenario_result"] = "pass"
        payload["expected"] = {
            "claim_level": "bounded_support",
            "semantic_drift_risk": False,
        }
        payload["observed"] = {
            "claim_level": "bounded_support",
            "semantic_drift_risk": False,
        }
        return payload

    if scenario == "drift_injection_same_evidence":
        payload["injected_wording"] = claim_text or "proven / production-ready"
        payload["scenario_result"] = "pass" if strong_claim_attempted else "fail"
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "claim_level": "stronger_than_allowed" if strong_claim_attempted else "bounded_support",
            "semantic_drift_risk": bool(strong_claim_attempted),
        }
        return payload

    if scenario == "same_evidence_posture_escalation":
        payload["same_evidence_as_previous"] = same_evidence_as_previous
        payload["attempted_posture"] = attempted_posture or "stronger_than_previous"
        drift = same_evidence_as_previous and payload["attempted_posture"] == "stronger_than_previous"
        payload["scenario_result"] = "pass" if drift else "fail"
        payload["expected"] = {
            "semantic_drift_risk": True,
        }
        payload["observed"] = {
            "semantic_drift_risk": drift,
        }
        return payload

    if scenario == "missing_preconditions_strong_claim":
        payload["scenario_result"] = "not_executed"
        payload["expected"] = {
            "claim_level": "stronger_than_allowed",
            "semantic_drift_risk": True,
        }
        payload["observed"] = None
        return payload

    raise ValueError(f"unknown scenario: {scenario}")


def run_default_suite() -> dict[str, object]:
    scenarios = [
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
            scenario="missing_preconditions_strong_claim",
            preconditions_met=False,
            claim_text="verified_implementation",
        ),
    ]
    pass_count = sum(1 for item in scenarios if item["scenario_result"] == "pass")
    not_executed_count = sum(1 for item in scenarios if item["scenario_result"] == "not_executed")
    return {
        "repo": REPO_NAME,
        "artifact_type": "claim-enforcement-checker-suite",
        "schema_version": "0.1",
        "scenarios": scenarios,
        "summary": {
            "total": len(scenarios),
            "pass": pass_count,
            "fail": len(scenarios) - pass_count - not_executed_count,
            "not_executed": not_executed_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic claim-enforcement scenarios.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = run_default_suite()

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        summary = result["summary"]
        print("[claim_enforcement]")
        print(f"total={summary['total']}")
        print(f"pass={summary['pass']}")
        print(f"fail={summary['fail']}")
        print(f"not_executed={summary['not_executed']}")
        for scenario in result["scenarios"]:
            print(
                f"{scenario['scenario']}: result={scenario['scenario_result']} "
                f"preconditions_met={scenario['preconditions_met']}"
            )
    return 0 if result["summary"]["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
