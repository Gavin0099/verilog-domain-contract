# Rule Extraction Table (Governance Pipeline)

This table captures only constraints that can change AI agent behavior.

## R-001

- rule_id: `RESET_DEFINITION_REQUIRED`
- category: `PRECONDITION|ASSUMPTION_RISK`
- rule: Reset polarity and reset type (`sync` or `async`) must be explicitly defined before synthesizable RTL generation.
- why_risk: Implicit reset assumptions can produce functionally incorrect or unsafe RTL without syntax errors.
- preconditions_required: `reset_polarity_defined`, `reset_type_defined`
- missing_precondition_effect: `restrict_codegen`, `escalate`
- allowed_output_if_missing: `analysis_only`, `draft_with_explicit_assumptions`
- forbidden_behavior: `implicit_reset_assumption`, `silent_default_reset`
- forbidden_claim: `implementation_complete`, `synthesizable_ready`
- required_disclosure_if_draft: `assumed_reset_polarity`, `assumed_reset_type`
- source:
  - file: `docs/knowhow/digital_system_design_with_system_verilog.md`
  - anchor_id: `RESET_ASYNC_SYNC_DIFF`
  - page: `101-102`
  - file: `docs/knowhow/Verilog_HDL_A_guide_to_digital_design_and_synthesis_v2.md`
  - anchor_id: `RESET_PROCEDURAL_MODELING`
  - page: `32`

## R-002

- rule_id: `ASSIGNMENT_SEMANTICS_REQUIRED`
- category: `SEMANTIC_RULE|ASSUMPTION_RISK`
- rule: Sequential intent must use non-blocking assignment and combinational intent must use blocking assignment with complete assignment paths.
- why_risk: Syntax-valid RTL can still mis-model behavior when assignment semantics are mixed or intent is ambiguous.
- preconditions_required: `state_update_intent_defined`, `comb_or_seq_partition_defined`
- missing_precondition_effect: `draft_only`, `escalate`
- allowed_output_if_missing: `analysis_only`, `draft_with_explicit_semantic_assumptions`
- forbidden_behavior: `mixed_blocking_nonblocking_on_state`, `latch_prone_incomplete_comb_logic`
- forbidden_claim: `implementation_complete`, `behaviorally_verified`
- required_disclosure_if_draft: `state_update_model`, `comb_logic_model`
- source:
  - file: `docs/knowhow/digital_system_design_with_system_verilog.md`
  - anchor_id: `NONBLOCKING_FOR_SEQUENTIAL_LOGIC`
  - page: `101-102`
  - file: `docs/knowhow/Verilog_HDL_A_guide_to_digital_design_and_synthesis_v2.md`
  - anchor_id: `BLOCKING_NONBLOCKING_PROCEDURAL_ASSIGNMENT`
  - page: `131`

## R-003

- rule_id: `HANDSHAKE_TIMING_DEFINITION_REQUIRED`
- category: `PRECONDITION|ASSUMPTION_RISK|VERIFICATION_REQUIREMENT`
- rule: Interface acceptance and timing behavior must be explicitly defined (protocol semantics, backpressure behavior, and latency expectation) before implementation claims.
- why_risk: AI may assume always-ready or fixed-latency behavior that breaks integration semantics.
- preconditions_required: `interface_protocol_semantics_defined`, `backpressure_behavior_defined`, `latency_expectation_defined`
- missing_precondition_effect:
  - if `interface_protocol_semantics_defined` missing: `analysis_only`, `escalate`
  - if protocol defined but `backpressure_behavior_defined` or `latency_expectation_defined` missing: `draft_only`, `escalate`
- allowed_output_if_missing:
  - if `interface_protocol_semantics_defined` missing: `analysis_only` only — `draft_with_explicit_handshake_assumptions` is not allowed in this sub-case
  - if protocol defined but timing/backpressure missing: `analysis_only`, `draft_with_explicit_handshake_assumptions`
- forbidden_behavior: `implicit_always_ready_sink`, `implicit_one_cycle_acceptance`, `silent_fixed_latency_assumption`
- forbidden_claim: `implementation_complete`, `interface_timing_verified`
- required_disclosure_if_draft: `assumed_protocol_semantics`, `assumed_backpressure_model`, `assumed_latency_model`
- source:
  - file: `docs/knowhow/RTS5264_Datasheet_1.0.md`
  - anchor_id: `INTERFACE_TIMING_LATENCY_CONSTRAINT`
  - page: `8, 37`
  - file: `docs/knowhow/digital_system_design_with_system_verilog.md`
  - anchor_id: `SYSTEM_INTERFACE_TIMING_DEPENDENCY`
  - page: `27`
