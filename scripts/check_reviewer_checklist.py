#!/usr/bin/env python3
"""Evaluate review-checklist items against deterministic governance closeout artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run reviewer checklist checks.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_SCHEMA = REPO_ROOT / "schemas/review-checklist.yaml"
CLOSEOUT_SUMMARY = REPO_ROOT / "artifacts/closeout/2026-06-05-governance-closeout-summary.json"
REPLAY_ARTIFACT = REPO_ROOT / "artifacts/replay-results/2026-06-05-validator-replay.yaml"
CLAIM_ARTIFACT = REPO_ROOT / "artifacts/claim-enforcement/checker-tests/2026-06-05-claim-enforcement-suite.json"
OUTPUT_PATH = REPO_ROOT / "artifacts/closeout/2026-06-05-reviewer-checklist-verdict.json"


def _load(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _case_map(cases: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(case["case_id"]): case for case in cases}


def _pass(case: dict[str, object] | None) -> bool:
    return bool(case) and case.get("status") == "pass"


def _result(item_id: str, passed: bool, evidence: list[str], rationale: str) -> dict[str, object]:
    return {
        "item_id": item_id,
        "result": "pass" if passed else "fail",
        "evidence": evidence,
        "rationale": rationale,
    }


def build_verdict() -> dict[str, object]:
    checklist = _load(CHECKLIST_SCHEMA)
    closeout = _load(CLOSEOUT_SUMMARY)
    replay = _load(REPLAY_ARTIFACT)
    claim = _load(CLAIM_ARTIFACT)

    replay_cases = _case_map(replay["cases"])
    claim_cases = _case_map(claim["cases"])
    closeout_overall = closeout["overall"]
    closeout_surfaces = closeout["surfaces"]

    section_results: list[dict[str, object]] = []
    all_pass = True

    for section in checklist["sections"]:
        sid = section["id"]
        items: list[dict[str, object]] = []

        if sid == "reset_contract":
            br1 = replay_cases.get("BR-001")
            ok = _pass(br1) and br1["checks"]["disclosure_complete"]
            items.extend(
                [
                    _result("RESET_DEFINED", ok, ["BR-001"], "Missing reset definition replay case was correctly downgraded and disclosed."),
                    _result("RESET_TYPE_DEFINED", ok, ["BR-001"], "Reset type gap was surfaced by replay enforcement."),
                    _result("RESET_ASSUMPTION_DISCLOSED", ok, ["BR-001"], "Replay output required explicit reset assumption disclosure."),
                    _result("RESET_COMPLETION_CLAIM", ok, ["BR-001"], "Completion claims remained blocked under missing reset preconditions."),
                ]
            )
        elif sid == "assignment_contract":
            br4 = replay_cases.get("BR-004")
            ok = _pass(br4)
            items.extend(
                [
                    _result("ASSIGNMENT_INTENT_CLEAR", ok, ["BR-004"], "Ambiguous assignment intent replay case was contained by governance."),
                    _result("ASSIGNMENT_OPERATOR_MATCH", ok, ["BR-004"], "Assignment semantics replay path remained bounded to explicit assumptions."),
                    _result("ASSIGNMENT_MIXED_STATE_PATH", ok, ["BR-004"], "Assignment contract replay did not permit unsafe completion posture."),
                ]
            )
        elif sid == "handshake_contract":
            br2 = replay_cases.get("BR-002")
            br3 = replay_cases.get("BR-003")
            items.extend(
                [
                    _result("HANDSHAKE_PROTOCOL_DEFINED", _pass(br2), ["BR-002"], "Protocol-missing handshake replay case was downgraded to analysis-only."),
                    _result("HANDSHAKE_BACKPRESSURE_DEFINED", _pass(br3), ["BR-003"], "Backpressure gap replay case required explicit handshake assumptions."),
                    _result("HANDSHAKE_LATENCY_DEFINED", _pass(br3), ["BR-003"], "Latency gap replay case required explicit handshake assumptions."),
                    _result("HANDSHAKE_COMPLETION_CLAIM", _pass(br2) and _pass(br3), ["BR-002", "BR-003"], "Handshake completion claims remained bounded under missing protocol/timing detail."),
                ]
            )
        elif sid == "fsm_contract":
            br6 = replay_cases.get("BR-006")
            ok = _pass(br6)
            items.extend(
                [
                    _result("FSM_STATE_MODEL_DEFINED", ok, ["BR-006"], "FSM replay case surfaced missing state model assumptions."),
                    _result("FSM_DECOMPOSITION_DEFINED", ok, ["BR-006"], "FSM replay case surfaced missing decomposition style assumptions."),
                    _result("FSM_ILLEGAL_STATE_DEFINED", ok, ["BR-006"], "FSM replay case surfaced missing illegal-state handling assumptions."),
                    _result("FSM_COMPLETION_CLAIM", ok, ["BR-006"], "FSM completion claims remained bounded under incomplete contract inputs."),
                ]
            )
        elif sid == "cdc_contract":
            br7 = replay_cases.get("BR-007")
            ok = _pass(br7)
            items.extend(
                [
                    _result("CDC_MULTI_CLOCK_DETECTED", ok, ["BR-007"], "CDC replay case correctly detected multi-clock crossing intent."),
                    _result("CDC_STRATEGY_DEFINED", ok, ["BR-007"], "CDC replay case blocked completion without explicit CDC strategy."),
                    _result("CDC_SYNCHRONIZER_DEFINED", ok, ["BR-007"], "CDC replay case blocked completion without synchronizer scheme."),
                    _result("CDC_COMPLETION_CLAIM", ok, ["BR-007"], "CDC completion claims remained blocked under missing CDC strategy."),
                ]
            )
        elif sid == "governance_closeout":
            replay_ok = closeout_surfaces["behavioral_replay"]["summary"]["fail"] == 0
            claim_ok = closeout_surfaces["claim_enforcement"]["summary"]["fail"] == 0
            schema_ok = closeout_overall["schema_conformance_ok"]
            aggregate_ok = schema_ok and replay_ok and claim_ok
            items.extend(
                [
                    _result("CLOSEOUT_REPLAY_SUMMARY_PRESENT", replay_ok, ["governance-closeout-summary"], "Replay closeout summary is present and reports zero failures."),
                    _result("CLOSEOUT_CLAIM_SUMMARY_PRESENT", claim_ok, ["governance-closeout-summary"], "Claim closeout summary is present and reports zero failures."),
                    _result("CLOSEOUT_SCHEMA_CONFORMANCE_PRESENT", schema_ok, ["governance-closeout-summary", "schema-conformance"], "Closeout surfaces report schema conformance cleanly."),
                    _result("CLOSEOUT_AGGREGATE_PRESENT", aggregate_ok, ["governance-closeout-summary"], "Aggregate closeout summary is present and internally consistent."),
                ]
            )

        section_pass = all(item["result"] == "pass" for item in items)
        all_pass = all_pass and section_pass
        section_results.append(
            {
                "section_id": sid,
                "required": bool(section["required"]),
                "result": "pass" if section_pass else "fail",
                "items": items,
            }
        )

    return {
        "schema_version": "0.1",
        "name": "reviewer-checklist-verdict",
        "checklist_schema": str(CHECKLIST_SCHEMA.relative_to(REPO_ROOT)),
        "closeout_summary": str(CLOSEOUT_SUMMARY.relative_to(REPO_ROOT)),
        "result": "pass" if all_pass else "fail",
        "sections": section_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate reviewer checklist against governance closeout artifacts.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out", default=str(OUTPUT_PATH.relative_to(REPO_ROOT)))
    args = parser.parse_args()

    verdict = build_verdict()
    out_path = REPO_ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
    else:
        print("[reviewer_checklist_verdict]")
        print(f"result={verdict['result']}")
        print(f"sections={len(verdict['sections'])}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for section in verdict["sections"]:
            print(f"{section['section_id']}: {section['result']}")
    return 0 if verdict["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
