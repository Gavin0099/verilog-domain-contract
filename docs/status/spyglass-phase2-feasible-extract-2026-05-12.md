# SpyGlass Phase 2 可行資訊摘錄（Executable Extract）

## A. 可直接導入（Now)
1. 導入層級
- 採 `profile/extension` 層導入 SpyGlass 證據。
- 不修改 core contract 的 must-not-assume 與 completion claim 邊界。

2. 證據來源（可納入）
- CDC/Clock/Reset 報告中的 violation 類型：
  - unsynchronized crossing
  - reset synchronization
  - convergence
  - glitch
- SGDC 約束完備性訊號：
  - unconstrained ports/clocks/resets
  - derived/generated clock/reset 資訊
- waiver 使用痕跡：
  - waiver 是否存在
  - waiver 是否有理由與範圍

3. 與現有欄位 mapping（最小集）
- `cdc_strategy_present_when_multi_clock_implied`
  - 由 CDC crossing 分析 + clock domain 證據輔助檢核
- `cdc_synchronizer_scheme_defined`
  - 由 reset/CDC synchronizer 相關報告輔助檢核
- clock/reset precondition completeness
  - 由 SGDC 約束覆蓋率訊號輔助檢核

4. Gate C Phase 2 對接（可先 informational）
- 新增可選欄位：`tool_evidence_completeness`
- 評分先不影響 pass/fail，只做 window 觀測
- 穩定後再決定是否升級為 hard condition

## B. 不可導入（Not Allowed)
1. 不可把 compile/lint/tool clean 視為 `implementation_complete`。
2. 不可因工具 auto-infer 而放寬缺失 precondition。
3. 不可把 vendor-specific 規則直接寫進 v0.1 core docs（除非明確標示 profile/extension）。

## C. 最小落地方案（3 步）
1. 定義 SpyGlass evidence schema（extension 檔）
- 建議欄位：rule_id, severity, object, domain_pair, constrained_state, waiver_state, report_ref

2. 建立 mapping 表（extension 檔）
- `spyglass_signal -> contract precondition/evidence field`

3. 在 Gate C ingest 增加 optional ingest
- 若有 SpyGlass 證據：填 `tool_evidence_completeness`
- 若無：維持現行 Gate C 計算，不降級

## D. Go / No-Go 判定
- Go（建議）：先以 extension + informational metric 上線。
- No-Go：任何會改變「缺 precondition -> downgrade/stop」語義的改動。
