# SpyGlass 擴大導入條件（Gate-Expansion Criteria）

Date: 2026-05-12
Status: agreed

## Expansion Criteria
1. 邊界穩定期通過
- 連續 30 天無 `advisory -> ranking/gating` 漂移跡象。

2. 低風險試點先成功
- 先導入 3-5 個高價值 rule family（非全量）並證明不改變
  `missing precondition -> downgrade/stop`。

3. 版本治理機制就緒
- 明確 SpyGlass 版本對應、更新流程、回滾策略。

4. 可追溯性完整
- 每個導入規則可對應
  `source -> mapping -> allowed/disallowed use -> evidence field`。
- 負向測試覆蓋誤用場景。

5. 不進 Gate C authority
- 新訊號先 advisory/informational。
- 至少一個觀察窗口後再評估權重。
- 不得直接成為 pass/fail gate。

6. Reviewer 行為未被指標馴化
- 審查紀錄中不得把 completeness/WARN 當品質排名、能力比較、
  或 claim 升級依據。

## Boundary Reminder
Tool evidence completeness improves reviewer visibility, but does not by itself
upgrade implementation completeness or override missing-precondition
downgrade/stop semantics.
