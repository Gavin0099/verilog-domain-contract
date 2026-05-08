# Contract Sync Check (v0.1)

Purpose: document the authoritative mapping between `contract.yaml` `governance_rules`
entries and their corresponding leaf doc enforcement sections. Used to prevent
carry-forward drift (the class of gap where a leaf doc gets an enforcement section
but contract.yaml is not updated, or vice versa).

---

## Mapping Table

| Rule ID | Leaf Doc | Enforcement Section | contract.yaml section | rule_sources |
|---------|----------|--------------------|-----------------------|--------------|
| RESET_DEFINITION_REQUIRED | docs/clock-reset-contract.md | `## Constraint on AI Behavior` | `governance_rules` ✓ | 2 sources ✓ |
| ASSIGNMENT_SEMANTICS_REQUIRED | docs/assignment-semantics.md | `## Constraint on AI Behavior`, `## Forbidden Behavior` | `governance_rules` ✓ | 2 sources ✓ |
| HANDSHAKE_TIMING_DEFINITION_REQUIRED | docs/handshake-contract.md | `## Constraint on AI Behavior`, `## Forbidden Behavior` | `governance_rules` ✓ | 2 sources ✓ |
| FSM_CONTRACT_REQUIRED | docs/fsm-contract.md | `## Constraint on AI Behavior`, `## Forbidden Behavior`, `## Forbidden Claim` | `governance_rules` ✓ | 2 sources ✓ (added Run 011) |
| CDC_STRATEGY_REQUIRED | docs/cdc-contract.md | `## Constraint on AI Behavior`, `## Forbidden Behavior`, `## Completion Policy` | `governance_rules` ✓ | 2 sources ✓ (added Run 022) |

---

## Sync Check Process

When a leaf doc gains a new enforcement section (or has one modified):

1. Identify the rule name from the enforcement section header or rule ID comment.
2. Check `contract.yaml` `governance_rules`: does a matching entry exist?
   - If not: add it. Use the existing RESET/ASSIGNMENT/HANDSHAKE format as template.
3. Check `contract.yaml` `precondition_effects`: are the precondition tokens from `required:` present?
   - If not: add the missing precondition_effects entries.
4. Check `contract.yaml` `must_not_assume`: are the forbidden-assumption tokens present?
   - If not: add them.
5. Check `contract.yaml` `completion_claim_disallow_without_evidence`: is there an entry blocking
   `implementation_complete_without_{rule_domain}_definition`?
   - If not: add it.
6. Check `contract.yaml` `rule_sources`: is there at least one authority source for the rule?
   - If not: add a source from the knowhow directory.
7. Check `validators/precondition_gate_validator.py` `rule_ids`: does the validator declare this rule?
   - If not: add gate logic and update `rule_ids`.

---

## Known Gaps History

| Gap ID | Run Detected | Rule | Section | Status |
|--------|-------------|------|---------|--------|
| C-004 | Run 005 | HANDSHAKE_TIMING_DEFINITION_REQUIRED | `governance_rules` allowed_if_missing sub-cases | Fixed Run 005 |
| G-006-01 | Run 006 | FSM_CONTRACT_REQUIRED | `precondition_effects` | Fixed Run 006 |
| G-006-02 | Run 006 | FSM_CONTRACT_REQUIRED | `must_not_assume` | Fixed Run 006 |
| G-006-03 | Run 006 | FSM_CONTRACT_REQUIRED | `governance_rules` | Fixed Run 006 |
| G-006-04 | Run 006 | FSM_CONTRACT_REQUIRED | `completion_claim_disallow_without_evidence` | Fixed Run 006 |
| V-009-01 | Run 009 | FSM_CONTRACT_REQUIRED | validator coverage | Fixed Run 010 |
| G-011-01 | Run 011 | FSM_CONTRACT_REQUIRED | `rule_sources` | Fixed Run 011 |
| G-014-01 | Run 014 | CLAIM_BOUNDARY vocabulary | `claim_level` token vocabulary ambiguity between CLAIM_BOUNDARY.md and contract.yaml | Documented Run 014 (no code change needed) |
| G-019-01 | Run 019 | ASSIGNMENT_SEMANTICS_REQUIRED | `precondition_effects` missing `state_update_intent_defined`, `comb_or_seq_partition_defined` | Fixed Run 019 |
| G-019-02 | Run 019 | ASSIGNMENT_SEMANTICS_REQUIRED | validator coverage absent (rule_ids missing, no gate logic) | Fixed Run 019 |
| D-020-01 | Run 020 | governance/rules/ structure | 19 general behavioral rules in governance/rules/ are NOT Verilog domain rules — no contract.yaml entry required; classified as cross-domain general rule pack | Documented Run 020 (architectural decision; no code change) |
| G-022-01 | Run 022 | CDC_STRATEGY_REQUIRED | leaf doc `docs/cdc-contract.md` absent | Fixed Run 022 |
| G-022-02 | Run 022 | CDC_STRATEGY_REQUIRED | `governance_rules` entry absent | Fixed Run 022 |
| G-022-03 | Run 022 | CDC_STRATEGY_REQUIRED | `must_not_assume` missing CDC entries | Fixed Run 022 |
| G-022-04 | Run 022 | CDC_STRATEGY_REQUIRED | `completion_claim_disallow_without_evidence` missing CDC entry | Fixed Run 022 |
| G-022-05 | Run 022 | CDC_STRATEGY_REQUIRED | validator Rule 5 + regex absent (PG-006/007 added) | Fixed Run 022 |

---

## Supporting Docs (enforcement support, no governance_rules entry required)

These docs have enforcement-like content but are support infrastructure,
not primary contract domains. They do not require a corresponding `governance_rules` entry.

| Doc | Purpose |
|-----|---------|
| docs/CLAIM_BOUNDARY.md | Claim posture boundary rules — defines `claim_level` assessment vocabulary (`bounded_support`, `stronger_than_allowed`); supports `completion_claim_allow` / `completion_claim_disallow_without_evidence` in contract.yaml. **Not a governance_rule domain.** |
| docs/CLAIM_ENFORCEMENT_MINIMAL_SPEC.md | Claim enforcement test scenarios (baseline closeout, drift injection, posture escalation). Equivalent to behavioral-replay-oracle role for claim enforcement. **Not a governance_rule domain.** |
| docs/behavior-validation.md | Validation procedures — defines BV-* test cases |
| docs/behavioral-replay-oracle.md | Replay oracle mechanics — defines oracle verdict format |
| docs/mode-volatility-note.md | Mode constraint notes — BR-* constraints |
| docs/pre-task-gate-integration.md | Pre-task gate integration guide |
| docs/rule-extraction-table.md | Rule summary table — derived from governance_rules |
| docs/framework-surface-mapping.md | Framework surface mapping |

### Vocabulary Note: two distinct `claim_level` systems

| System | Tokens | Location |
|--------|--------|----------|
| contract.yaml completion claim | `analysis_provided`, `draft_rtl_provided`, `candidate_implementation_provided`, `verified_implementation` | `completion_claim_allow` / `claim_evidence_requirements` |
| CLAIM_BOUNDARY posture assessment | `bounded_support`, `stronger_than_allowed` | `docs/CLAIM_BOUNDARY.md` |

These are **different vocabularies for different purposes**. The contract.yaml tokens describe the
*type* of output an agent claims to produce. The CLAIM_BOUNDARY tokens describe a runtime
*assessment* of whether a specific claim exceeds its evidence. They must not be conflated.

---

## Drift Prevention Policy

**Every session that modifies a leaf doc enforcement section MUST also check the 7 items above.**
If any item is missing, it is a carry-forward gap and must be fixed before the run scorecard
can be filed as `governance_signal_without_material_improvement: false`.

This document should be updated whenever a new governance_rule is added or a leaf doc
enforcement section is created.

**Note on governance/rules/ scope**: The 7-item sync-check process above applies only to
`contract.yaml` `governance_rules` (the 5 Verilog domain rules: RESET, ASSIGNMENT, HANDSHAKE, FSM, CDC). The 19 general behavioral
rules in `governance/rules/` are a cross-domain rule pack and are **out of scope** for this
sync-check. See `governance/rules/RULE_INDEX.md` § "Two Distinct Rule Systems" for details.
