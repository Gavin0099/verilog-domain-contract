#!/usr/bin/env python3
"""
Epistemic decision scoring smoke runner.

Implements calibration fixes:
- premise gate precedence
- epistemic_risk-aware scoring
- non-zero bounded_trial cost
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASES_FILE = REPO / "artifacts" / "decision-semantics" / "epistemic_cases_v1.json"
OUT_FILE = REPO / "artifacts" / "decision-semantics" / "2026-04-23-epistemic-smoke.json"


def epistemic_risk(case: dict) -> str:
    premise = case["premise_status"]
    evidence = case["evidence_quality"]
    if premise == "unsupported":
        return "high"
    if premise == "unknown" and evidence == "weak":
        return "high"
    if premise == "unknown" and evidence == "moderate":
        return "medium"
    return "low"


def decide(case: dict) -> tuple[str, dict]:
    premise = case["premise_status"]
    e_risk = epistemic_risk(case)
    trial_cost = float(case["bounded_trial_cost"])
    trial_ok = bool(case["bounded_trial_justification"]) and case["scope_local_reversible"] and trial_cost <= 0.25

    # Fix 1: premise gate precedence
    if premise == "unsupported":
        return "reframe", {"reason": "unsupported_premise_blocks_proceed", "epistemic_risk": e_risk}

    # Fix 2: epistemic risk gate
    if premise == "unknown":
        if e_risk == "high":
            return "need_more_info", {"reason": "unknown_premise_high_epistemic_risk", "epistemic_risk": e_risk}
        if e_risk == "medium" and not trial_ok:
            return "need_more_info", {"reason": "unknown_premise_medium_risk_without_justified_trial", "epistemic_risk": e_risk}
        if e_risk == "medium" and trial_ok:
            return "proceed_with_assumption", {"reason": "bounded_trial_justified", "epistemic_risk": e_risk}

    # premise supported path
    if premise == "supported":
        return "proceed_with_assumption", {"reason": "supported_premise_with_sufficient_evidence", "epistemic_risk": e_risk}

    return "need_more_info", {"reason": "fallback", "epistemic_risk": e_risk}


def main() -> int:
    payload = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    results = []
    failed = 0
    for case in payload["cases"]:
        action, meta = decide(case)
        ok = action == case["expected_action"]
        if not ok:
            failed += 1
        results.append(
            {
                "id": case["id"],
                "expected_action": case["expected_action"],
                "observed_action": action,
                "pass": ok,
                "epistemic_risk": meta["epistemic_risk"],
                "reason": meta["reason"],
            }
        )

    summary = {
        "suite": payload["suite"],
        "total_cases": len(results),
        "failed_cases": failed,
        "pass_rate": (len(results) - failed) / len(results) if results else 0.0,
        "results": results,
    }
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
