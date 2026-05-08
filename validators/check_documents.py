#!/usr/bin/env python3
"""
Document completeness checker for verilog-domain-contract.

Two-way check:
  1. Broken refs  — files listed in contract.yaml documents that do not exist on disk.
  2. Missing entries — files on disk (in governed paths) that are not listed in contract.yaml.

Governed paths (files that MUST appear in documents list):
  docs/*.md              (excluding docs/knowhow/)
  governance/*.md        (top-level only, not rules/)
  governance/rules/*.md  (only RULE_INDEX.md — individual rule files are exempt)
  schemas/*.yaml
  artifacts/replay-results/*
  artifacts/precondition-gate/*
  artifacts/decision-semantics/*

Exempt paths (intentionally unlisted):
  docs/knowhow/          source reference material, not contract documents
  governance/rules/      individual rule files (indexed via RULE_INDEX.md)
  artifacts/governance-test/  test run artifacts, not contract documents
  validators/            tooling, not contract documents
  scripts/               tooling, not contract documents
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False


GOVERNED_GLOBS = [
    "docs/*.md",
    "governance/*.md",
    "governance/rules/RULE_INDEX.md",
    "schemas/*.yaml",
    "artifacts/replay-results/*",
    "artifacts/precondition-gate/*",
    "artifacts/decision-semantics/*",
    # top-level docs
    "AGENTS.base.md",
    "AGENTS.md",
    "PLAN.md",
    "README.md",
]

EXEMPT_PREFIXES = [
    "docs/knowhow/",
    "governance/rules/",         # individual rule files (RULE_INDEX.md is explicit)
    "artifacts/governance-test/",
    "validators/",
    "scripts/",
    ".git/",
    ".claude/",
]


def _is_exempt(path: str) -> bool:
    p = path.replace("\\", "/")
    # RULE_INDEX.md is explicitly governed — don't exempt it
    if p == "governance/rules/RULE_INDEX.md":
        return False
    return any(p.startswith(pfx) for pfx in EXEMPT_PREFIXES)


def load_contract_documents(repo_root: Path) -> list[str]:
    """Load documents list from contract.yaml."""
    contract_path = repo_root / "contract.yaml"
    if not contract_path.exists():
        raise FileNotFoundError(f"contract.yaml not found at {contract_path}")

    if _HAS_YAML:
        with open(contract_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return [str(d) for d in (data.get("documents") or [])]

    # Fallback: naive line parser (no yaml dependency required)
    docs: list[str] = []
    in_documents = False
    with open(contract_path, encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip()
            if stripped == "documents:":
                in_documents = True
                continue
            if in_documents:
                if stripped.startswith("  - "):
                    docs.append(stripped[4:].strip())
                elif stripped and not stripped.startswith(" ") and not stripped.startswith("#"):
                    in_documents = False
    return docs


def check_documents(repo_root: Path) -> dict:
    repo_root = Path(repo_root).resolve()
    contract_docs = load_contract_documents(repo_root)
    contract_set = set(contract_docs)

    # --- Check 1: broken refs (listed but not on disk) ---
    broken: list[str] = []
    for doc in contract_docs:
        if not (repo_root / doc).exists():
            broken.append(doc)

    # --- Check 2: missing entries (on disk but not listed) ---
    on_disk: set[str] = set()
    for pattern in GOVERNED_GLOBS:
        for path in glob.glob(str(repo_root / pattern)):
            rel = Path(path).relative_to(repo_root).as_posix()
            if not _is_exempt(rel):
                on_disk.add(rel)

    missing: list[str] = sorted(on_disk - contract_set)

    ok = len(broken) == 0 and len(missing) == 0
    return {
        "ok": ok,
        "broken_refs": sorted(broken),
        "missing_entries": missing,
        "contract_doc_count": len(contract_docs),
        "governed_file_count": len(on_disk),
    }


def _main() -> int:
    parser = argparse.ArgumentParser(description="Check contract.yaml documents completeness.")
    parser.add_argument("--repo-root", default=".", help="Repo root directory (default: cwd)")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    result = check_documents(repo_root)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["ok"] else "FAIL"
        print(f"[check_documents] {status}")
        print(f"  contract_doc_count : {result['contract_doc_count']}")
        print(f"  governed_file_count: {result['governed_file_count']}")
        if result["broken_refs"]:
            print(f"  BROKEN REFS ({len(result['broken_refs'])}):")
            for b in result["broken_refs"]:
                print(f"    - {b}")
        else:
            print("  broken_refs        : (none)")
        if result["missing_entries"]:
            print(f"  MISSING ENTRIES ({len(result['missing_entries'])}):")
            for m in result["missing_entries"]:
                print(f"    - {m}")
        else:
            print("  missing_entries    : (none)")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(_main())
