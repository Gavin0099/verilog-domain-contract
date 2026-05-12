# SpyGlass 規則文件導入與 Phase 2 可行性評估（2026-05-12）

## 1. 結論
可行，但建議採「治理證據層（policy evidence）先行」而非「直接放寬實作 claim」。

- 可行性判定: **可行（條件式）**
- 導入方式: 先把 SpyGlass 規則映射為 precondition completeness / evidence completeness 的檢查清單，再決定是否升級 Gate C 權重。
- 風險等級: **中高**（涉及 clock/reset/CDC 邊界，需維持 missing-precondition -> downgrade/stop 行為）

## 2. 已完成事項
- `SpyGlass_BuiltInRules_Reference.pdf` -> `SpyGlass_BuiltInRules_Reference.md`
- `SpyGlass_ClockResetRules_Reference.pdf` -> `SpyGlass_ClockResetRules_Reference.md`

## 3. 為何可行（與現有 repo 對齊）
現有合約已包含：
- clock/reset precondition gate（`docs/clock-reset-contract.md`）
- CDC strategy gate（`docs/cdc-contract.md`, `contract.yaml` 的 `CDC_STRATEGY_REQUIRED`）
- Gate C Phase 2 度量管線（`scripts/gate_c_ingest_check.py` + NDJSON logs）

SpyGlass CDC 文件可補強的剛好是：
- SGDC 約束完備性（例：未約束 ports / clock-reset 推導）
- 規則級嚴重度與 violation 類型（unsync crossing, reset sync, glitch, convergence）
- waiver/constraint 使用痕跡（可作為 evidence provenance）

因此可作為 Phase 2 的「外部工具證據來源」加入，不必改動核心 policy 的保守邊界。

## 4. 主要風險（需明確禁止）
1. 不可把 lint/compile/單次工具 clean 當成 implementation_complete。
2. 不可因工具可 auto-infer 就放寬缺失 precondition（clock edge/reset polarity/CDC strategy）
3. 不可把 vendor 特定規則直接寫進 v0.1 core contract，除非標示為 profile/extension。

## 5. 建議的 Phase 2 導入切法
1. 建立 `spyglass_profile`（extension 層）
- 只定義 evidence schema 與 mapping，不改 core must-not-assume。

2. 加一層 evidence mapping
- 將 SpyGlass 觀測結果映射到既有 gate 欄位，例如：
  - `cdc_strategy_present_when_multi_clock_implied`
  - `cdc_synchronizer_scheme_defined`
  - reset/clock 約束完整性訊號

3. Gate C 指標擴充（不替代）
- 在 reopen/revert/stability 之外新增 `tool_evidence_completeness`（可選欄位）。
- 先以 informational 模式跑一個 window，再決定是否納入通過條件。

## 6. 實務判定
在目前 repo 狀態下，做 Phase 2 導入是可行的；前提是維持：
- 缺 precondition 一律 downgrade/stop
- claim 不因 vendor report 自動升級
- SpyGlass 僅作 evidence 強化，而非 policy 取代
