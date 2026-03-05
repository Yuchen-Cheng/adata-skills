# RAG 知識來源品質評估報告

> **評估日期：** {{EVAL_DATE}}
> **評估路徑：** `{{TARGET_PATH}}`
> **合格門檻：** {{PASS_THRESHOLD}} 分（滿分 100 分）
> **評估標準版本：** {{CRITERIA_VERSION}}

---

## 評估標準總覽

| # | 評估項目 | 配分 | 說明 |
|:--|:--------|-----:|:-----|
{{CRITERIA_TABLE_ROWS}}
| | **合計** | **100** | |

---

## 各檔案評估結果

{{FILE_SECTIONS}}

---

## 統計總表

| 檔案名稱 | 路徑 |{{CRITERIA_HEADER_COLS}} 總分 | 結果 |
|:--------|:-----|{{CRITERIA_HEADER_SEP}}-----:|:----:|
{{SUMMARY_TABLE_ROWS}}

### 統計摘要

| 指標 | 數值 |
|:----|-----:|
| 評估檔案總數 | {{TOTAL_FILES}} |
| 合格檔案數 | {{PASS_COUNT}} |
| 不合格檔案數 | {{FAIL_COUNT}} |
| 合格率 | {{PASS_RATE}}% |
| 平均分數 | {{AVG_SCORE}} |
| 最高分 | {{MAX_SCORE}} |
| 最低分 | {{MIN_SCORE}} |

---

*本報告由 rag-quality-evaluator skill 自動生成*

---

<!--
=== FILE_SECTION 範本（每個檔案重複一次）===

### 📄 {{FILE_NAME}}

**路徑：** `{{FILE_PATH}}`
**檔案大小：** {{FILE_SIZE_KB}} KB
**檔案類型：** {{FILE_EXT}}

#### 評分明細

| 評估項目 | 滿分 | 得分 | 評語 |
|:--------|-----:|-----:|:-----|
| {{CRITERION_1}} | {{MAX_1}} | {{SCORE_1}} | {{COMMENT_1}} |
...
| **合計** | **100** | **{{TOTAL_SCORE}}** | |

**整體評語：** {{OVERALL_COMMENT}}

**結果：** {{PASS_ICON}} {{PASS_LABEL}}（{{TOTAL_SCORE}} 分，門檻 {{THRESHOLD}} 分）

---
-->
