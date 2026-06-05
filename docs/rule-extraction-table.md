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

## R-004

- rule_id: `FSM_CONTRACT_REQUIRED`
- category: `SEMANTIC_RULE|ASSUMPTION_RISK`
- rule: FSM state model, decomposition style, and illegal-state handling must be explicit before implementation claims.
- why_risk: syntax-valid state-machine RTL can still diverge functionally when state structure or illegal-state behavior is assumed.
- preconditions_required: `fsm_state_model_defined`, `fsm_decomposition_style_declared`, `fsm_illegal_state_handling_defined`
- missing_precondition_effect: `draft_only`, `escalate`
- allowed_output_if_missing: `analysis_only`, `draft_with_explicit_assumptions`
- forbidden_behavior: `implicit_state_encoding`, `implicit_fsm_style`, `implicit_illegal_state_recovery`
- forbidden_claim: `implementation_complete`, `behaviorally_verified`
- required_disclosure_if_draft: `assumed_state_model`, `assumed_decomposition_style`, `assumed_illegal_state_policy`
- source:
  - file: `docs/knowhow/digital_system_design_with_system_verilog.md`
  - anchor_id: `FSM_STATE_MODEL_AND_ENCODING`
  - page: `135`
  - file: `docs/knowhow/Verilog_HDL_A_guide_to_digital_design_and_synthesis_v2.md`
  - anchor_id: `FSM_TRAFFIC_CONTROLLER_STATE_ENCODING`
  - page: `165-166`

## R-005

- rule_id: `CDC_STRATEGY_REQUIRED`
- category: `PRECONDITION|ASSUMPTION_RISK`
- rule: Multi-clock implementation requires an explicit boundary map and synchronizer strategy before implementation-level RTL generation.
- why_risk: AI may otherwise assume a safe crossing model and emit RTL that appears plausible while leaving metastability hazards unresolved.
- preconditions_required: `cdc_strategy_present_when_multi_clock_implied`, `cdc_synchronizer_scheme_defined`
- missing_precondition_effect: `stop_insufficient_preconditions`, `escalate`
- allowed_output_if_missing: `analysis_only`, `draft_with_explicit_cdc_assumptions`
- forbidden_behavior: `implicit_single_clock_domain_assumption`, `silent_cdc_boundary_crossing`, `derived_clock_treated_as_safe`
- forbidden_claim: `implementation_complete`, `verified_implementation`
- required_disclosure_if_draft: `assumed_cdc_strategy`, `clock_domain_boundary_map`, `synchronizer_scheme`
- source:
  - file: `docs/knowhow/digital_system_design_with_system_verilog.md`
  - anchor_id: `MULTI_CLOCK_DOMAIN_INTERFACE_DEPENDENCY`
  - page: `27`
  - file: `docs/knowhow/Verilog_HDL_A_guide_to_digital_design_and_synthesis_v2.md`
  - anchor_id: `CLOCK_DOMAIN_SYNCHRONIZATION_REQUIREMENT`
  - page: `32`
