#!/usr/bin/env python3
"""Minimal deterministic pre_task_check runtime hook."""

from __future__ import annotations

import argparse
import json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime pre_task_check compatibility wrapper.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--rules", default="common")
    parser.add_argument("--risk", default="low")
    parser.add_argument("--oversight", default="auto")
    parser.add_argument("--memory-mode")
    parser.add_argument("--task-text", default="")
    parser.add_argument("--task-level", default="L1")
    parser.add_argument("--contract")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args, _ = parser.parse_known_args(argv)

    _ = (
        args.project_root,
        args.rules,
        args.risk,
        args.oversight,
        args.memory_mode,
        args.task_text,
        args.task_level,
        args.contract,
    )

    payload = {"ok": True}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=True))
    else:
        print("[pre_task_check]")
        print("ok=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
