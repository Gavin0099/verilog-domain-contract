#!/usr/bin/env python3
"""
check_advisory.py — advisory wrapper for check_documents.

Runs check_documents() and writes results to artifacts/runtime/advisory/.
Always exits 0 (advisory = non-blocking; gate_policy fail_mode: audit).

Intended to be registered as a Claude Code Stop hook:
  .claude/settings.json → hooks → Stop →
    command: "python scripts/check_advisory.py"

Output:
  artifacts/runtime/advisory/check_documents_<timestamp>.json
  stdout: one-line advisory summary
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "validators"))

from check_documents import check_documents  # noqa: E402


def main() -> int:
    result = check_documents(REPO_ROOT)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    advisory = {
        "advisory_type": "check_documents",
        "timestamp": ts,
        "repo_root": str(REPO_ROOT),
        "status": "PASS" if result["ok"] else "FAIL",
        "ok": result["ok"],
        "contract_doc_count": result["contract_doc_count"],
        "governed_file_count": result["governed_file_count"],
        "broken_refs": result["broken_refs"],
        "missing_entries": result["missing_entries"],
    }

    out_dir = REPO_ROOT / "artifacts" / "runtime" / "advisory"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"check_documents_{ts}.json"
    out_path.write_text(json.dumps(advisory, ensure_ascii=False, indent=2), encoding="utf-8")

    # stdout summary (visible in hook output)
    status = "PASS" if result["ok"] else "FAIL"
    print(f"[check_advisory] {status} — docs:{result['contract_doc_count']} "
          f"broken:{len(result['broken_refs'])} missing:{len(result['missing_entries'])} "
          f"→ {out_path.relative_to(REPO_ROOT)}")

    if not result["ok"]:
        if result["broken_refs"]:
            print(f"  BROKEN REFS: {result['broken_refs']}")
        if result["missing_entries"]:
            print(f"  MISSING ENTRIES: {result['missing_entries']}")

    return 0  # always advisory — never blocks session close


if __name__ == "__main__":
    raise SystemExit(main())
