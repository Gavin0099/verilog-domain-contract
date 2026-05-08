#!/usr/bin/env python3
"""
Smoke cases for precondition_gate_validator.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from validators.precondition_gate_validator import evaluate_precondition_gate


CASES = [
    {
        "id": "PG-001",
        "task": "Implement synthesizable Verilog counter. Reset exists but reset polarity and reset type are not specified.",
        "expected_mode": "restrict_codegen",
    },
    {
        "id": "PG-002",
        "task": "Implement synthesizable producer/consumer control logic for interface, but protocol semantics are not defined.",
        "expected_mode": "allow_analysis_only",
    },
    {
        "id": "PG-003",
        "task": (
            "Implement synthesizable Verilog module with reset active-low and async reset type. "
            "Use valid/ready protocol semantics, include backpressure behavior, and target one-cycle latency."
        ),
        "expected_mode": "allow_draft_with_assumptions",
    },
    {
        "id": "PG-004",
        "task": (
            "Implement synthesizable Verilog module using flip-flop registers and sequential logic. "
            "Assignment semantics and comb/seq partitioning details have not been provided."
        ),
        "expected_mode": "allow_draft_with_assumptions",
    },
    {
        "id": "PG-005",
        "task": (
            "Implement synthesizable Verilog module with flip-flop registers. "
            "State update model: non-blocking for sequential registers. "
            "Process partition: always_ff for sequential state, always_comb for combinational logic paths."
        ),
        "expected_mode": "allow_draft_with_assumptions",
    },
    {
        "id": "PG-006",
        "task": (
            "Implement synthesizable Verilog module with multi-clock design "
            "where signals cross between clock domains. "
            "No handoff approach or crossing boundary plan has been specified."
        ),
        "expected_mode": "restrict_codegen",
    },
    {
        "id": "PG-007",
        "task": (
            "Implement synthesizable Verilog module with clock domain crossing. "
            "CDC strategy: two-flop synchronizer for all crossing signals. "
            "Clock domain boundary map: clk_a domain drives data_out, clk_b domain samples data_in. "
            "Metastability mitigation: synchronizer chain on all crossing signals."
        ),
        "expected_mode": "allow_draft_with_assumptions",
    },
]


def main() -> int:
    results = []
    failed = 0
    for case in CASES:
        verdict = evaluate_precondition_gate(case["task"])
        ok = verdict["recommended_mode"] == case["expected_mode"]
        if not ok:
            failed += 1
        results.append(
            {
                "id": case["id"],
                "expected_mode": case["expected_mode"],
                "observed_mode": verdict["recommended_mode"],
                "pass": ok,
                "missing_preconditions": verdict["missing_preconditions"],
            }
        )

    print(json.dumps({"cases": results, "failed": failed}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
