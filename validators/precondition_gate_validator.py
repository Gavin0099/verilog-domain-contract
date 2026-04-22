#!/usr/bin/env python3
"""
Pre-task precondition gate validator for Verilog/RTL tasks.

Minimal v0.1 scope:
- reset definition completeness (polarity + type)
- interface/handshake definition completeness

Verdict vocabulary (intentionally small):
- allow_analysis_only
- allow_draft_with_assumptions
- restrict_codegen
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field

try:
    from governance_tools.validator_interface import DomainValidator, ValidatorResult
except Exception:  # pragma: no cover
    # Lightweight fallback for local CLI usage when framework import path is absent.
    @dataclass
    class ValidatorResult:  # type: ignore[override]
        ok: bool
        rule_ids: list[str]
        violations: list[str] = field(default_factory=list)
        warnings: list[str] = field(default_factory=list)
        evidence_summary: str = ""
        metadata: dict[str, object] = field(default_factory=dict)

        def to_dict(self) -> dict:
            return asdict(self)

    class DomainValidator:  # type: ignore[override]
        @property
        def rule_ids(self) -> list[str]:
            return []


RE_IMPLEMENTATION_INTENT = re.compile(
    r"\b(synthesizable|rtl|verilog|module|implement|implementation|generate)\b",
    re.IGNORECASE,
)
RE_INTERFACE_INTENT = re.compile(
    r"\b(interface|handshake|valid|ready|req|ack|protocol|control logic|pipeline)\b",
    re.IGNORECASE,
)
RE_RESET_MENTION = re.compile(r"\b(reset|rst|rst_n|reset_n)\b", re.IGNORECASE)
RE_RESET_POLARITY = re.compile(r"\b(active[- ]low|active[- ]high|polarity|rst_n|reset_n)\b", re.IGNORECASE)
RE_RESET_TYPE = re.compile(r"\b(sync(?:hronous)? reset|async(?:hronous)? reset|reset type)\b", re.IGNORECASE)
RE_POLARITY_UNSPEC = re.compile(r"\b(reset\s+)?polarity\b.{0,40}\b(not specified|unspecified|unknown|tbd)\b", re.IGNORECASE)
RE_TYPE_UNSPEC = re.compile(r"\b(reset\s+)?type\b.{0,40}\b(not specified|unspecified|unknown|tbd)\b", re.IGNORECASE)
RE_PROTOCOL = re.compile(r"\b(valid\s*/?\s*ready|ready\s*/?\s*valid|req\s*/?\s*ack|handshake semantics)\b", re.IGNORECASE)
RE_BACKPRESSURE = re.compile(r"\b(backpressure|stall|downstream not ready|ready deassert)\b", re.IGNORECASE)
RE_LATENCY = re.compile(r"\b(latency|cycle|one-cycle|two-cycle|throughput)\b", re.IGNORECASE)


def _has(regex: re.Pattern[str], text: str) -> bool:
    return bool(regex.search(text))


def _defined_with_negation(positive_re: re.Pattern[str], negative_re: re.Pattern[str], text: str) -> bool:
    if not _has(positive_re, text):
        return False
    if _has(negative_re, text):
        return False
    return True


def evaluate_precondition_gate(task_text: str) -> dict[str, object]:
    text = task_text or ""
    missing_preconditions: list[str] = []
    forbidden_claims = [
        "implementation_complete",
        "synthesizable_ready",
        "verified_implementation",
    ]
    rule_refs: list[str] = []

    implementation_intent = _has(RE_IMPLEMENTATION_INTENT, text)
    interface_intent = _has(RE_INTERFACE_INTENT, text)

    recommended_mode = "allow_draft_with_assumptions"

    # Rule 1: reset definition gate (pre-task).
    if implementation_intent and _has(RE_RESET_MENTION, text):
        reset_polarity_defined = _defined_with_negation(RE_RESET_POLARITY, RE_POLARITY_UNSPEC, text)
        reset_type_defined = _defined_with_negation(RE_RESET_TYPE, RE_TYPE_UNSPEC, text)
        if not reset_polarity_defined:
            missing_preconditions.append("reset_polarity_defined")
        if not reset_type_defined:
            missing_preconditions.append("reset_type_defined")
        if not (reset_polarity_defined and reset_type_defined):
            rule_refs.append("RESET_DEFINITION_REQUIRED")
            # Missing both -> stricter recommendation.
            if not reset_polarity_defined and not reset_type_defined:
                recommended_mode = "restrict_codegen"
            else:
                recommended_mode = "allow_draft_with_assumptions"

    # Rule 2: interface/handshake gate (pre-task).
    if implementation_intent and interface_intent:
        protocol_defined = _has(RE_PROTOCOL, text)
        backpressure_defined = _has(RE_BACKPRESSURE, text)
        latency_defined = _has(RE_LATENCY, text)
        if not protocol_defined:
            missing_preconditions.append("interface_protocol_semantics_defined")
            rule_refs.append("HANDSHAKE_TIMING_DEFINITION_REQUIRED")
            # protocol missing is stricter than draft path.
            if recommended_mode != "restrict_codegen":
                recommended_mode = "allow_analysis_only"
        else:
            if not backpressure_defined:
                missing_preconditions.append("backpressure_behavior_defined")
            if not latency_defined:
                missing_preconditions.append("latency_expectation_defined")
            if (not backpressure_defined or not latency_defined):
                rule_refs.append("HANDSHAKE_TIMING_DEFINITION_REQUIRED")
                if recommended_mode not in {"restrict_codegen", "allow_analysis_only"}:
                    recommended_mode = "allow_draft_with_assumptions"

    ok = len(missing_preconditions) == 0
    if ok:
        forbidden_claims = []

    return {
        "ok": ok,
        "missing_preconditions": sorted(set(missing_preconditions)),
        "recommended_mode": recommended_mode,
        "forbidden_claims": forbidden_claims,
        "rule_refs": sorted(set(rule_refs)),
    }


class PreconditionGateValidator(DomainValidator):
    @property
    def rule_ids(self) -> list[str]:
        return ["RESET_DEFINITION_REQUIRED", "HANDSHAKE_TIMING_DEFINITION_REQUIRED"]

    def validate(self, payload: dict) -> ValidatorResult:
        checks = payload.get("checks") or {}
        task_text = str(checks.get("task_text") or payload.get("task_text") or "")
        gate = evaluate_precondition_gate(task_text)
        violations = [f"missing precondition: {item}" for item in gate["missing_preconditions"]]
        return ValidatorResult(
            ok=bool(gate["ok"]),
            rule_ids=self.rule_ids,
            violations=violations,
            warnings=[],
            evidence_summary=f"recommended_mode={gate['recommended_mode']}",
            metadata=gate,
        )


def _main() -> int:
    parser = argparse.ArgumentParser(description="Run Verilog precondition gate validator.")
    parser.add_argument("--task-text", default="", help="Task text to evaluate.")
    parser.add_argument("--task-file", default="", help="Optional path to a file containing task text.")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    task_text = args.task_text
    if args.task_file:
        task_text = open(args.task_file, "r", encoding="utf-8").read()

    result = evaluate_precondition_gate(task_text)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[precondition_gate]")
        print(f"ok={result['ok']}")
        print(f"recommended_mode={result['recommended_mode']}")
        print(f"missing_preconditions={','.join(result['missing_preconditions']) or '(none)'}")
        print(f"rule_refs={','.join(result['rule_refs']) or '(none)'}")
        if result["forbidden_claims"]:
            print(f"forbidden_claims={','.join(result['forbidden_claims'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
