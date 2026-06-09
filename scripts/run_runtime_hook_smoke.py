#!/usr/bin/env python3
"""Run repo-local runtime hooks against one artifact tag and persist a smoke result."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.governance_artifact_paths import default_artifact_tag


def _run_hook(script_rel: str, artifact_tag: str) -> dict[str, object]:
    script_path = REPO_ROOT / script_rel
    completed = subprocess.run(
        [sys.executable, str(script_path), "--artifact-tag", artifact_tag, "--format", "json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(completed.stdout)
    return {
        "hook": script_path.stem,
        "script": script_rel.replace("\\", "/"),
        "returncode": completed.returncode,
        "ok": bool(payload.get("ok")),
        "payload": payload,
        "stderr": completed.stderr.strip(),
    }


def run_smoke(artifact_tag: str) -> dict[str, object]:
    checks = [
        _run_hook("runtime_hooks/core/pre_task_check.py", artifact_tag),
        _run_hook("runtime_hooks/core/session_start.py", artifact_tag),
        _run_hook("runtime_hooks/core/post_task_check.py", artifact_tag),
    ]
    all_ok = all(check["ok"] and check["returncode"] == 0 for check in checks)
    return {
        "schema_version": "0.1",
        "name": "runtime-hook-smoke",
        "artifact_tag": artifact_tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "summary": {
            "total": len(checks),
            "pass": sum(1 for check in checks if check["ok"] and check["returncode"] == 0),
            "fail": sum(1 for check in checks if not check["ok"] or check["returncode"] != 0),
            "overall_ok": all_ok,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run repo-local runtime hook smoke checks.")
    parser.add_argument("--artifact-tag", default=default_artifact_tag())
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--out")
    args = parser.parse_args()

    result = run_smoke(args.artifact_tag)
    out_path = Path(args.out) if args.out else REPO_ROOT / f"artifacts/governance/{args.artifact_tag}-runtime-hook-smoke.json"
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("[runtime_hook_smoke]")
        print(f"artifact_tag={result['artifact_tag']}")
        print(f"total={result['summary']['total']}")
        print(f"pass={result['summary']['pass']}")
        print(f"fail={result['summary']['fail']}")
        print(f"overall_ok={result['summary']['overall_ok']}")
        print(f"out={out_path.relative_to(REPO_ROOT)}")
        for check in result["checks"]:
            print(
                f"{check['hook']}: ok={str(check['ok']).lower()} returncode={check['returncode']}"
            )
    return 0 if result["summary"]["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
