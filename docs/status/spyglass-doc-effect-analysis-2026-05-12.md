# SpyGlass 兩份文件對本 Repo 的功效分析（2026-05-12）

## 分析對象
- `SpyGlass_BuiltInRules_Reference.md`
- `SpyGlass_ClockResetRules_Reference.md`

## 對本 Repo 的直接功效
1. 強化 precondition completeness 證據
- Clock/Reset CDC 文件明確提供「未約束/unconstrained」類型檢查（例如 `Clock_info18`, `Reset_info09a`, `Reset_info09b`）。
- 這能直接支援本 repo 的 `RESET_DEFINITION_REQUIRED` 與 `CDC_STRATEGY_REQUIRED` 前置條件審核，不改變既有語義。

2. 強化 completion claim 的「證據密度」
- Built-In 文件提供語法/語意/綜合訊息的分類與嚴重度語境，適合當作「負面證據」來源。
- Clock/Reset 文件提供 rule-level violation 與 constraint 關聯，適合補足「為何不能升級 claim」的可追溯理由。

3. 強化 Gate C（Phase 2）可觀測性
- 可將 rule 結果映射為 `tool_evidence_completeness`（complete/partial/absent/unknown）作為觀測維度。
- 此維度可先 informational，不干擾現行 Gate C pass 判定。

## 對本 Repo 的間接功效
1. 降低「隱性假設」風險
- `unconstrained` 類訊號可對應到本 repo 禁止的 implicit clock/reset/CDC 假設。

2. 提升審查一致性
- 透過固定 mapping（rule family -> contract field），不同 lane 會得到更一致的 downgrade/stop 理由。

3. 改善事後稽核
- 可把 rule_id、severity、waiver_state、report_ref 收斂到統一 evidence profile，便於回放與比較。

## 侷限與邊界
1. 這兩份文件無法替代 core governance 判決
- 工具 clean 或低嚴重度訊息，不等於 `implementation_complete` 或 `verified_implementation`。

2. vendor 規則不能直接進入 v0.1 core 規範
- 應保持在 extension/profile 層，避免污染 core rule 語義。

3. 缺失 precondition 的處理不可被工具結果覆蓋
- 仍必須維持 `missing precondition -> downgrade/stop`。

## 導入優先級（建議）
1. 優先導入 `Clock_info18`, `Reset_info09a`, `Reset_info09b` 對應的 completeness 訊號。
2. 次階段導入 `Clockmatrix01`, `Derived_clocks_info` 以補強 domain 關係與衍生時鐘證據。
3. 最後導入 waiver hygiene（例如 `waived_without_rationale` -> partial）。

## 與現有合約對齊結論
- 與 `contract.yaml` 的 `CDC_STRATEGY_REQUIRED`、`RESET_DEFINITION_REQUIRED` 高度相容。
- 與 `must_not_assume` 與 completion claim policy 一致。
- 建議路線：**可導入，且應維持 extension-only。**
