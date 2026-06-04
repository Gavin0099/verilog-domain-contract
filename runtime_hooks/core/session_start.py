#!/usr/bin/env python3
"""No-op session_start runtime hook."""

import json
import sys


def main() -> int:
    # Consume optional JSON payload to remain CLI-compatible with possible callers.
    if len(sys.argv) > 1:
        _ = sys.argv[1:]
    return 0


if __name__ == "__main__":
    _ = json  # keep linter/import consumers quiet in static checks
    raise SystemExit(main())
