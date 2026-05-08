# C# Native Boundary

- **rule_id**: `CSH-001`
- **severity**: `advisory`
- **rationale**: Isolates native interop behind explicit adapter boundaries to keep domain logic clean.


- native interop 必須留在明確的 adapter 或 boundary interface 後面。
- `DllImport` 與 native handle management 不得滲入 domain logic。
- resource ownership、dispose、與 error translation 必須明確且可 review。
