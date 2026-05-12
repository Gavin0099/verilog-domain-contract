#!/usr/bin/env python3
"""
Advisory-only validator for SpyGlass extension boundary usage.

Scope:
- Detect boundary-misuse wording in reports/logs.
- Output PASS/WARN only.
- Never affects Gate C pass/fail and always exits 0.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_TARGETS = [
    "docs/status/gate-c-window-report-2026-05-11-spyglass-extension.md",
    "docs/status/spyglass-phase2-mapping-2026-05-12.md",
    "docs/status/spyglass-extension-manifest-2026-05-12.yaml",
    "docs/status/gate-c-review-log.ndjson",
]


RULES = [
    ("quality_ranking", re.compile(r"\bquality\s+ranking\b", re.IGNORECASE)),
    ("model_capability_ranking", re.compile(r"\bmodel\s+capability\s+ranking\b", re.IGNORECASE)),
    ("upgrade_implementation_completeness", re.compile(r"\bupgrade\s+implementation\s+completeness\b", re.IGNORECASE)),
    ("authority_signal", re.compile(r"\bauthority\s+signal\b", re.IGNORECASE)),
    ("gate_c_pass_fail_coupling", re.compile(r"\bgate\s*c\s*pass\s*/\s*fail\b", re.IGNORECASE)),
]

NEGATION_HINTS = (
    "do not",
    "does not",
    "not ",
    "disallowed",
    "prohibited",
    "forbidden",
    "advisory_only",
    "does_not_affect_gate_c",
)

POSITIVE_MISUSE_PATTERNS = [
    ("authority_signal", re.compile(r"\b(use|treat|consider)\b.{0,60}\bauthority signal\b", re.IGNORECASE)),
    ("quality_ranking", re.compile(r"\b(use|treat|consider)\b.{0,60}\bquality ranking\b", re.IGNORECASE)),
    ("model_capability_ranking", re.compile(r"\b(use|treat|consider)\b.{0,80}\bmodel capability ranking\b", re.IGNORECASE)),
    ("upgrade_implementation_completeness", re.compile(r"\b(can|should|may)\b.{0,80}\bupgrade implementation completeness\b", re.IGNORECASE)),
    ("gate_c_pass_fail_coupling", re.compile(r"\b(included in|affects|drives)\b.{0,80}\bgate\s*c\s*pass\s*/\s*fail\b", re.IGNORECASE)),
    ("quality_proxy_from_completeness", re.compile(
        r"\btool_evidence_completeness\b.{0,120}\b(better|higher|stronger)\b.{0,80}\bimplementation quality\b",
        re.IGNORECASE,
    )),
]


def scan_file(path: Path) -> list[tuple[str, int, str]]:
    hits: list[tuple[str, int, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return [("read_error", 0, f"cannot read file: {path}")]

    for lineno, line in enumerate(lines, start=1):
        low = line.lower()
        if any(hint in low for hint in NEGATION_HINTS):
            continue

        for rule_id, pattern in POSITIVE_MISUSE_PATTERNS:
            if pattern.search(line):
                hits.append((rule_id, lineno, line.strip()))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Advisory-only boundary misuse detector.")
    parser.add_argument("paths", nargs="*", help="Optional explicit paths to scan")
    args = parser.parse_args()

    targets = [Path(p) for p in (args.paths if args.paths else DEFAULT_TARGETS)]

    print("SpyGlass Manifest Usage Validator")
    print("advisory_only: true")
    print("does_not_affect_gate_c: true")
    print()

    any_warn = False
    scanned = 0
    for path in targets:
        if not path.exists():
            print(f"[WARN] missing target: {path}")
            any_warn = True
            continue
        scanned += 1
        hits = scan_file(path)
        if not hits:
            print(f"[PASS] {path}")
            continue
        any_warn = True
        print(f"[WARN] {path}")
        for rule_id, lineno, snippet in hits:
            if rule_id == "read_error":
                print(f"  - read_error: {snippet}")
            else:
                print(f"  - {rule_id} @L{lineno}: {snippet}")

    print()
    print(f"files_scanned: {scanned}")
    print(f"result: {'WARN' if any_warn else 'PASS'}")
    print("exit_behavior: always_zero")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
