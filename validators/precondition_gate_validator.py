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
    r"\b(interface|handshake|valid\s*/?\s*ready|ready\s*/?\s*valid|req\s*/?\s*ack|protocol|control logic|pipeline)\b",
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
RE_BACKPRESSURE_UNSPEC = re.compile(
    r"\b(backpressure|stall|acceptance behavior)\b.{0,40}\b(not specified|unspecified|unknown|tbd|not provided)\b",
    re.IGNORECASE,
)
RE_LATENCY_UNSPEC = re.compile(
    r"\b(latency|cycle|throughput)\b.{0,40}\b(not specified|unspecified|unknown|tbd|not provided)\b",
    re.IGNORECASE,
)
RE_ASSIGNMENT_INTENT = re.compile(
    r"\b(always_ff|always_comb|always_latch|"
    r"blocking\s+assignment|non-?blocking\s+assignment|"
    r"sequential\s+logic|combinational\s+logic|"
    r"flip[- ]flop|latch[- ]prone|assignment\s+semantics)\b",
    re.IGNORECASE,
)
RE_STATE_UPDATE_INTENT = re.compile(
    r"\b(non[- ]blocking\s+for\s+(?:state|seq|sequential|register)|"
    r"state\s+update\s+(?:model|rule|semantics)|"
    r"sequential\s+update\s+(?:model|semantics|rule)|"
    r"register\s+update\s+(?:model|rule)|"
    r"always_ff\s+for|clocked\s+(?:update|assignment)\s+(?:model|rule))\b",
    re.IGNORECASE,
)
RE_COMB_SEQ_PARTITION = re.compile(
    r"\b(always_comb\s+for|blocking\s+for\s+comb(?:inational)?|"
    r"comb(?:inational)?\s+vs\.?\s+seq(?:uential)?|"
    r"process\s+partition|logic\s+partition|assignment\s+partition|"
    r"partition\s+(?:style|model|scheme))\b",
    re.IGNORECASE,
)
RE_CDC_INTENT = re.compile(
    r"\b(cdc|clock\s+domain\s+cross(?:ing)?|multi[- ]clock|multiple\s+clock\s+domains?|"
    r"two\s+clock\s+domains?|clock\s+boundary|cross[- ]domain|metastabilit(?:y|ies)|"
    r"asynchronous\s+clock|different\s+clock\s+(?:domain|source))\b",
    re.IGNORECASE,
)
RE_CDC_STRATEGY_PRESENT = re.compile(
    r"\b(cdc\s+strategy|crossing\s+(?:plan|strategy|method)|handoff\s+approach|"
    r"clock\s+domain\s+boundary\s+(?:plan|strategy)|synchronization\s+(?:strategy|method))\b",
    re.IGNORECASE,
)
RE_CDC_SYNCHRONIZER_SCHEME = re.compile(
    r"\b(two[- ]flop\s+synchronizer|synchronizer\s+chain|fifo[- ](?:based\s+)?crossing|"
    r"gray[- ]code\s+(?:fifo|crossing)|asynchronous\s+fifo|"
    r"metastability\s+(?:mitigation|protection|handling)|"
    r"synchronizer\s+(?:scheme|flop|stage|cell))\b",
    re.IGNORECASE,
)
RE_CDC_BOUNDARY_MAP = re.compile(
    r"\b(clock\s+domain\s+boundary\s+map|boundary\s+map|"
    r"from\s+\w+\s+domain\s+to\s+\w+\s+domain|"
    r"\w+\s+domain\s+drives\s+\w+.*\w+\s+domain\s+samples\s+\w+)\b",
    re.IGNORECASE,
)
RE_CDC_UNSPEC = re.compile(
    r"\b(not specified|unspecified|unknown|tbd|not provided|missing)\b|"
    r"\b(no|without)\b.{0,40}\b(cdc\s+strategy|crossing\s+(?:plan|strategy|method)|"
    r"handoff\s+approach|boundary\s+map|synchroniz(?:er|ation)\s+(?:scheme|strategy|method)|"
    r"two[- ]flop\s+synchronizer|fifo[- ](?:based\s+)?crossing|gray[- ]code\s+(?:fifo|crossing))\b",
    re.IGNORECASE,
)
RE_FSM_INTENT = re.compile(
    r"\b(fsm|state machine|state diagram|state transition|next state|state register|state logic)\b",
    re.IGNORECASE,
)
RE_FSM_STATE_MODEL = re.compile(
    # "states?:" ends in non-word char so no trailing \b; other alternatives use \b via alternation
    r"(?:\bstate model\b|\bstate encoding\b|\bstate set\b|\bnumber of states\b"
    r"|\b[0-9]+\s*states?\b|\bstate list\b|\bstates?\s*:)",
    re.IGNORECASE,
)
RE_FSM_DECOMP = re.compile(
    r"\b(mealy|moore|one[- ]hot|binary encoded|gray code|two[- ]process|three[- ]process|"
    r"next[- ]state logic|output logic|fsm style|decomposition style)\b",
    re.IGNORECASE,
)
RE_FSM_ILLEGAL = re.compile(
    r"\b(illegal states?|default state|catch[- ]all|undefined state|safe state|"
    r"illegal state handling|recovery state|error state recovery)\b",
    re.IGNORECASE,
)


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
    blocking_effect = ""

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
        backpressure_defined = _defined_with_negation(RE_BACKPRESSURE, RE_BACKPRESSURE_UNSPEC, text)
        latency_defined = _defined_with_negation(RE_LATENCY, RE_LATENCY_UNSPEC, text)
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

    # Rule 3: FSM contract gate (pre-task).
    if implementation_intent and _has(RE_FSM_INTENT, text):
        fsm_state_model_defined = _has(RE_FSM_STATE_MODEL, text)
        fsm_decomp_declared = _has(RE_FSM_DECOMP, text)
        fsm_illegal_defined = _has(RE_FSM_ILLEGAL, text)
        if not fsm_state_model_defined:
            missing_preconditions.append("fsm_state_model_defined")
            rule_refs.append("FSM_CONTRACT_REQUIRED")
            # state model missing is required (not just required_for_impl_claim)
            if recommended_mode not in {"restrict_codegen", "allow_analysis_only"}:
                recommended_mode = "allow_draft_with_assumptions"
        if not fsm_decomp_declared:
            missing_preconditions.append("fsm_decomposition_style_declared")
            rule_refs.append("FSM_CONTRACT_REQUIRED")
        if not fsm_illegal_defined:
            missing_preconditions.append("fsm_illegal_state_handling_defined")
            rule_refs.append("FSM_CONTRACT_REQUIRED")

    # Rule 5: CDC strategy gate (pre-task, conditional on multi-clock intent).
    if implementation_intent and _has(RE_CDC_INTENT, text):
        cdc_strategy_statement_defined = _defined_with_negation(RE_CDC_STRATEGY_PRESENT, RE_CDC_UNSPEC, text)
        cdc_boundary_map_defined = _defined_with_negation(RE_CDC_BOUNDARY_MAP, RE_CDC_UNSPEC, text)
        cdc_synchronizer_scheme_defined = _defined_with_negation(RE_CDC_SYNCHRONIZER_SCHEME, RE_CDC_UNSPEC, text)
        cdc_strategy_defined = cdc_strategy_statement_defined and cdc_boundary_map_defined
        if not cdc_strategy_defined:
            missing_preconditions.append("cdc_strategy_present_when_multi_clock_implied")
        if not cdc_synchronizer_scheme_defined:
            missing_preconditions.append("cdc_synchronizer_scheme_defined")
        if not cdc_strategy_defined or not cdc_synchronizer_scheme_defined:
            rule_refs.append("CDC_STRATEGY_REQUIRED")
            recommended_mode = "restrict_codegen"
            blocking_effect = "stop_insufficient_preconditions"

    # Rule 4: assignment semantics gate (pre-task).
    if implementation_intent and _has(RE_ASSIGNMENT_INTENT, text):
        state_update_intent_defined = _has(RE_STATE_UPDATE_INTENT, text)
        comb_seq_partition_defined = _has(RE_COMB_SEQ_PARTITION, text)
        if not state_update_intent_defined:
            missing_preconditions.append("state_update_intent_defined")
            rule_refs.append("ASSIGNMENT_SEMANTICS_REQUIRED")
            if recommended_mode not in {"restrict_codegen", "allow_analysis_only"}:
                recommended_mode = "allow_draft_with_assumptions"
        if not comb_seq_partition_defined:
            missing_preconditions.append("comb_or_seq_partition_defined")
            rule_refs.append("ASSIGNMENT_SEMANTICS_REQUIRED")

    ok = len(missing_preconditions) == 0
    if ok:
        forbidden_claims = []

    return {
        "ok": ok,
        "missing_preconditions": sorted(set(missing_preconditions)),
        "recommended_mode": recommended_mode,
        "blocking_effect": blocking_effect,
        "forbidden_claims": forbidden_claims,
        "rule_refs": sorted(set(rule_refs)),
    }


class PreconditionGateValidator(DomainValidator):
    @property
    def rule_ids(self) -> list[str]:
        return ["RESET_DEFINITION_REQUIRED", "ASSIGNMENT_SEMANTICS_REQUIRED", "HANDSHAKE_TIMING_DEFINITION_REQUIRED", "FSM_CONTRACT_REQUIRED", "CDC_STRATEGY_REQUIRED"]

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
        if result["blocking_effect"]:
            print(f"blocking_effect={result['blocking_effect']}")
        print(f"missing_preconditions={','.join(result['missing_preconditions']) or '(none)'}")
        print(f"rule_refs={','.join(result['rule_refs']) or '(none)'}")
        if result["forbidden_claims"]:
            print(f"forbidden_claims={','.join(result['forbidden_claims'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
