# Python Rule Pack

- **rule_id**: `PY-001`
- **severity**: `informational`
- **rationale**: Baseline Python style, testability, and dependency discipline.


- 保持實作簡潔、可測試。
- 除非 repo 本來就依賴其他方案，否則優先使用 standard library。
- 除非 `PLAN` 明確授權，否則不要改變既有 CLI behavior。
