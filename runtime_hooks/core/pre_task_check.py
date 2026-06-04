#!/usr/bin/env python3
"""No-op pre_task_check runtime hook."""

import sys


def main() -> int:
    if len(sys.argv) > 1:
        _ = sys.argv[1:]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
