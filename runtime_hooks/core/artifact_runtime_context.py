#!/usr/bin/env python3
"""Shared deterministic artifact-loading helpers for runtime hook surfaces."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_repo(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def missing_rel_paths(paths: list[Path]) -> list[str]:
    return [rel_repo(path) for path in paths if not path.exists()]
