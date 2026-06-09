#!/usr/bin/env python3
"""Shared artifact tag and path helpers for governance deterministic surfaces."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def default_artifact_tag() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def replay_artifact_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/replay-results/{tag}-validator-replay.yaml"


def claim_artifact_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/claim-enforcement/checker-tests/{tag}-claim-enforcement-suite.json"


def precondition_gate_artifact_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/precondition-gate/{tag}-precondition-gate-suite.json"


def replay_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-validator-replay-conformance.json"


def claim_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-claim-enforcement-conformance.json"


def precondition_gate_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-precondition-gate-conformance.json"


def closeout_summary_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/closeout/{tag}-governance-closeout-summary.json"


def closeout_report_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/closeout/{tag}-governance-closeout-summary.md"


def closeout_summary_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-governance-closeout-summary-conformance.json"


def closeout_report_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-governance-closeout-report-conformance.json"


def reviewer_verdict_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/closeout/{tag}-reviewer-checklist-verdict.json"


def reviewer_verdict_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-reviewer-checklist-verdict-conformance.json"


def reviewer_bundle_manifest_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/closeout/{tag}-governance-bundle-manifest.json"


def reviewer_bundle_manifest_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-governance-bundle-manifest-conformance.json"


def release_handoff_index_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/closeout/{tag}-governance-release-handoff.json"


def release_handoff_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-governance-release-handoff-conformance.json"


def reviewer_handoff_consistency_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/governance/{tag}-reviewer-handoff-consistency.json"


def reviewer_handoff_consistency_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-reviewer-handoff-consistency-conformance.json"


def runtime_hook_smoke_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/governance/{tag}-runtime-hook-smoke.json"


def runtime_hook_smoke_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-runtime-hook-smoke-conformance.json"


def aggregate_coherence_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/governance/{tag}-aggregate-coherence.json"


def aggregate_coherence_conformance_path(repo_root: Path, tag: str) -> Path:
    return repo_root / f"artifacts/schema-conformance/{tag}-aggregate-coherence-conformance.json"
