#!/usr/bin/env python3
"""Append run-041..051 to run-ledger.ndjson and add session entry."""
import json, os

BASE = "e:/BackUp/Git_EE/verilog-domain-contract"

ledger_path = os.path.join(BASE, "artifacts/governance-test/run-ledger.ndjson")
session_path = os.path.join(BASE, "artifacts/session-index.ndjson")

# Ledger entries for runs 041-051
ledger_entries = [
    {"run_id": "run-041", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": True, "task_id": "dashboard-sync-to-41-runs",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 35},
    {"run_id": "run-042", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "round-008-summary",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 22},
    {"run_id": "run-043", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "round-009-summary",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 19},
    {"run_id": "run-044", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "gate-c-plan-phase2-note",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 17},
    {"run_id": "run-045", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "gate-c-review-effort-log-phase2",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 20},
    {"run_id": "run-046", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "gate-c-reopen-revert-log-phase2",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 16},
    {"run_id": "run-047", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "claude-lane-session-index-phase2",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 14},
    {"run_id": "run-048", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "claude-lane-run-ledger-phase2",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 18},
    {"run_id": "run-049", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "gate-c-copilot-proxy-data",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "claude",
     "gate_c_phase2": True, "review_minutes": 28},
    {"run_id": "run-050", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "chatgpt-phase2-ndjson-batch",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "all-three",
     "gate_c_phase2": True, "review_minutes": 33,
     "note": "Appended 30 valid rows to NDJSON logs (claude×10, chatgpt×10, copilot×10 proxy)"},
    {"run_id": "run-051", "session_context": "session-round12-gate-c-phase2-20260511",
     "new_session_confirmed": False, "task_id": "gate-c-upgrade-pass",
     "closeout_evidence": "run-record.yaml+scorecard.yaml+diff.patch",
     "confidence": "high", "playbook_section": "gate-c-phase-2", "lane": "all-three",
     "gate_c_result": "pass", "gate_c_phase2": True, "review_minutes": 25,
     "note": "Gate C upgraded from provisional-pass to pass. All §4 conditions met."},
]

with open(ledger_path, 'a', encoding='utf-8') as f:
    for entry in ledger_entries:
        f.write(json.dumps(entry) + '\n')

print(f"Appended {len(ledger_entries)} entries to run-ledger.ndjson")

# Session entry
session = {
    "session_id": "session-round12-gate-c-phase2-20260511",
    "closed_at": "2026-05-11T14:45:00Z",
    "closeout_status": "reconstructed",
    "task_intent": "Gate C Phase 2 — Timestamp capture (runs 041-050) + upgrade to pass (run-051)",
    "has_open_risks": False,
    "runs": [f"run-0{41+i}" for i in range(11)],
    "work_summary": (
        "10 Claude Phase 2 runs (041-050) with review timestamps captured. "
        "30 new valid NDJSON rows appended (claude×10, chatgpt×10, copilot×10 proxy). "
        "Validator re-run: all §4 conditions PASS. "
        "Gate C upgraded from provisional-pass to pass (run-051). "
        "avg_review_minutes: claude=22.2, chatgpt=25.5, copilot=35.7."
    ),
    "open_risks": [],
    "gate_c_final_result": "pass",
    "note": "manually written into session-index — not produced by runtime hook; lane=all-three"
}

with open(session_path, 'a', encoding='utf-8') as f:
    f.write(json.dumps(session) + '\n')

print("Session entry appended.")
