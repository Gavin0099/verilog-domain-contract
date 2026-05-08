# Run 001 — Task A: Domain Contract Consistency

**Spec version**: v1.2
**Session**: NEW SESSION REQUIRED (不得沿用舊 session)
**Repo**: `E:\BackUp\Git_EE\verilog-domain-contract`

---

## Primary Targets（只能動這些）

- `docs/rule-extraction-table.md`
- `docs/precondition-completeness-model.md`
- `docs/completion-claim-policy.md`
- `docs/clock-reset-contract.md`
- `docs/assignment-semantics.md`
- `docs/handshake-contract.md`
- `docs/fsm-contract.md`
- `docs/behavior-validation.md`
- `docs/verification-minimums.md`
- `contract.yaml`

## Out of Scope（不得修改）

- 所有 `.v` / `.sv` 檔案
- `scripts/`, `validators/`, `governance/rules/`
- `artifacts/` 下任何 runtime artifact

---

## 任務說明

請分析上述文件中**互相矛盾的 rule 或 assumption**，並修正一致性。

### 交付要求

1. **矛盾清單**（evidence mapping）：
   - 每條矛盾必須標明：
     - 文件 A（位置） vs 文件 B（位置）
     - 矛盾的具體內容
     - 修正方向（哪邊應以哪邊為準）

2. **修改後的文件**：
   - 只修正矛盾，不新增 rule 類別
   - 每個修改需有 1 句說明理由

3. **Evidence mapping 表**：
   - 每條 governance rule 能回溯到哪份文件 + 行號

### 邊界條件（不允許）

- 不得把 `draft_only` 升格為 `implementation_complete`
- 不得在 `forbidden_claim` 裡新增前面 `allowed` 的 claim
- 不得把單項 pass 推成 overall pass
- 不得修改 `contract.yaml` 的 `plugin_version` 或 `framework_interface_version`

---

## 開始前宣告

請在開始任何修改前輸出：

```
PRIMARY_TARGETS: [列出你計劃修改的具體檔案]
OUT_OF_SCOPE_CONFIRMED: [確認不會動的清單]
FIRST_MODIFICATION_FILE: [第一個要改的檔案]
```
