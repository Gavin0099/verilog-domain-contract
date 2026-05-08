# Rule Pack Normalization — Migration Note

**Run**: run-002 / Task B
**Date**: 2026-05-08

---

## 問題診斷（舊狀態）

| 問題 | 影響範圍 |
|------|---------|
| 無 `rule_id` 欄位 | 18/19 檔案 |
| 無 `severity` 欄位 | 18/19 檔案（`error_path_coverage.md` 有 `## Enforcement`） |
| 無 `rationale` 欄位 | 19/19 檔案 |
| `error_path_coverage.md` 用 `## Rule ID` / `## Enforcement` section header 格式，與其他文件風格不一致 | 1/19 |
| Pack 標題無統一 "Rule Pack" 命名規則 | 混用（見下表） |

## 欄位映射（舊 → 新）

| 舊格式 | 新格式 | 說明 |
|--------|--------|------|
| （無）| `- **rule_id**: \`XXX-NNN\`` | 新增到所有文件，緊接 H1 標題後 |
| `## Enforcement` + `` `hard-stop` `` | `- **severity**: \`hard-stop\`` | `error_path_coverage.md` 專用，section → inline |
| `## Rule ID` + `` `REF-ERROR-001` `` | `- **rule_id**: \`REF-ERROR-001\`` | 同上，保留原 ID 值 |
| （無）| `- **rationale**: ...` | 新增到所有文件 |

## Rule ID 命名規則

格式：`{PACK}-{NUM}` (PACK 全大寫，NUM 3位數字)

| Pack | ID 前綴 | 範例 |
|------|---------|------|
| common | `CMN` | `CMN-001` |
| refactor | `REF` | `REF-001`..`REF-005`，legacy: `REF-ERROR-001` |
| kernel-driver | `KDRV` | `KDRV-001`..`KDRV-003` |
| gl-hub-vendor-cmd | `GLHUB` | `GLHUB-001` |
| avalonia | `AVL` | `AVL-001`..`AVL-002` |
| cpp | `CPP` | `CPP-001` |
| csharp | `CSH` | `CSH-001`..`CSH-002` |
| python | `PY` | `PY-001` |
| swift | `SWT` | `SWT-001`..`SWT-002` |

**Legacy ID 注意**：`REF-ERROR-001` 為 `error_path_coverage.md` 的既有 ID，保留不變。
新 REF pack 從 `REF-001` 開始，序號跳過 `REF-ERROR-001` 原本的位置。

## Severity 詞彙對照

| 舊語言 | 正規化 severity | 範例文件 |
|--------|----------------|---------|
| `hard-stop`（已使用）| `hard-stop` | `error_path_coverage.md` |
| "不得"、"must not"、"forbidden" | `hard-stop` | kernel-driver/*, gl-hub-vendor-cmd, refactor/no_partial_cleanup |
| "應"、"必須"（非 forbidden）| `advisory` | 大部分 refactor/*, avalonia/*, csharp/* |
| 風格/流程指引 | `informational` | `python/coding.md` |

## 未修改項目

| 項目 | 理由 |
|------|------|
| Pack 標題（`# Refactor Behavior Lock Rule Pack` 等）| 不修改 naming，避免超範圍 |
| 各文件規則的 bullet content | 只做 metadata 正規化，不改規則本體 |
| `error_path_coverage.md` 的 `## Requirement`、`## Hard-stop conditions`、`## Scope boundary` sections | 這些是 content，保留 |

## 新增文件

| 文件 | 說明 |
|------|------|
| `governance/rules/RULE_INDEX.md` | 正規化 rule table，全 19 條規則的索引 |
