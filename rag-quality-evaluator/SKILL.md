---
name: rag-quality-evaluator
description: 評估檔案作為 RAG（Retrieval-Augmented Generation）知識來源的品質。根據使用者自訂的評估準則，動態生成一份 100 分制評分表，並對指定的單一檔案或資料夾內所有檔案逐一評分，最終輸出包含「各檔案評估結果」與「統計總表」的 Markdown 評估報告。Use when: 評估 RAG 知識庫品質、評估文件作為知識來源是否合適、審查檔案是否符合 RAG ingestion 標準、rag 品質、知識庫評估、文件品質檢查。Do NOT use for: 評估程式碼邏輯正確性、比較兩份文件內容相似度、執行文件格式轉換、文件摘要生成。
---

# RAG 品質評估器 操作指南

> **核心理念：** 由使用者定義標準，LLM 負責判斷，腳本負責檔案探索

---

## A. 適用場景

- ✅ 評估一份或多份文件是否適合作為 RAG 知識來源
- ✅ 為知識庫建立客觀的品質篩選流程
- ✅ 批量審查資料夾中所有文件的 RAG 適用性
- ✅ 根據組織或專案特定標準進行客製化評估
- ⛔ 單純的文件格式轉換（使用其他工具）
- ⛔ 文件摘要生成（使用摘要工具）
- ⛔ 程式碼邏輯審查（使用 code review 工具）

---

## B. 完整執行流程（5 個步驟）

> **⚠️ UI 互動規範：本流程所有選擇題均須使用 `ask_questions` UI 工具呈現，禁止以純文字列出選項後等待使用者輸入。** 可在單次 `ask_questions` 呼叫中批次提問（最多 4 題）。

### 步驟 1：收集使用者評估準則

**使用 `ask_questions` 工具，一次呈現問題 1–4（批次提問）：**

```yaml
# ask_questions 呼叫範例（問題 1–4 批次）
questions:
  - header: "評估面向"
    question: "您最關心文件的哪些面向？"
    multiSelect: true
    allowFreeformInput: true
    options:
      - label: "內容完整性"
        description: "資訊是否涵蓋主題、無明顯缺漏、有具體細節"
      - label: "結構清晰度"
        description: "是否有明確邏輯"
      - label: "資訊正確性"
        description: "事實是否正確、無錯誤"
      - label: "RAG 可檢索性"
        description: "語句是否獨立、關鍵詞是否豐富"

  - header: "文件類型"
    question: "您的文件屬於哪種類型？"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "技術文件"
        description: "API 文件、系統說明、操作手冊"
      - label: "法規/合規文件"
        description: "法律條文、政策規範"
      - label: "FAQ/問答集/IT ticket"
        description: "常見問題、內部問答、客服紀錄"
      - label: "產品說明/行銷文件"
      - label: "SOP/流程文件"

  - header: "一票否決"
    question: "有哪些您認為「一票否決」的條件嗎？"
    multiSelect: true
    allowFreeformInput: true
    options:
      - label: "含無法解析的掃描圖片（純圖片 PDF）"
      - label: "檔案加密或受密碼保護"
      - label: "內容完全為亂碼或無意義文字"
      - label: "內容含有敏感資訊（如個資、機密資料）"
        description: "評估過程中若發現此類內容，立即標記為不合格"
      - label: "無一票否決條件"

  - header: "特殊面向"
    question: "您希望額外評估哪些特殊面向？"
    multiSelect: true
    allowFreeformInput: true
    options:
      - label: "是否包含具體範例或案例"
      - label: "是否有明確的日期/版本資訊"
      - label: "是否有參考來源或引用出處"
      - label: "是否適合多語言或翻譯使用"
      - label: "無特殊需求"
```

**等待 `ask_questions` 回傳結果後繼續。**

---

### 步驟 2：生成評估清單（100 分制）

根據使用者回覆，**動態生成**一份評估清單。原則：

- **總分必須恰好等於 100 分**
- 每個評估項目配分為 5 的倍數（建議 5～25 分之間）
- 項目數量建議 5～10 項
- 每項必須有：名稱、滿分、具體評分說明（達到滿分的條件、部分得分的條件、0 分的條件）

**範例格式（僅供參考，實際內容依使用者準則生成）：**

```markdown
## 📋 評估標準（草稿）

| # | 評估項目 | 配分 | 滿分條件 | 部分得分 | 0 分條件 |
|:--|:--------|-----:|:--------|:--------|:--------|
| 1 | 內容完整性 | 25 | 涵蓋主題完整，無明顯缺漏 | 涵蓋主要內容但有次要缺漏 | 內容嚴重不完整 |
| 2 | 結構清晰度 | 20 | 有明確標題層級，邏輯清晰 | 有部分結構但不一致 | 無結構或難以閱讀 |
| 3 | 資訊精確性 | 20 | 事實正確，無明顯錯誤 | 大致正確，有少量存疑 | 含有明顯錯誤資訊 |
| 4 | 語言品質 | 15 | 語言流暢，無語法重大錯誤 | 尚可理解但有明顯錯誤 | 難以理解 |
| 5 | RAG 可檢索性 | 20 | 語句獨立性高，關鍵詞豐富 | 部分語句依賴上下文 | 大量需要上下文才能理解 |
| | **合計** | **100** | | | |
```

**生成後，使用 `ask_questions` 工具詢問使用者（問題 5–6 批次）：**

```yaml
# ask_questions 呼叫範例（問題 5–6 批次）
questions:
  - header: "配分滿意度"
    question: "您對評估項目的配分是否滿意？"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "滿意，請直接使用此配分"
        recommended: true
      - label: "不滿意，需要調整分數"
        description: "請在自由輸入欄說明要調整的項目與分數"

  - header: "項目調整"
    question: "評估項目的數量與內容是否符合您的需求？"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "符合，無需變動"
        recommended: true
      - label: "需要新增評估項目"
        description: "請在自由輸入欄說明要新增的項目"
      - label: "需要移除某些評估項目"
        description: "請在自由輸入欄告知要移除的項目名稱"
      - label: "需要同時新增與移除項目"
        description: "請在自由輸入欄分別說明"
```

**等待 `ask_questions` 回傳結果後，鎖定最終評估標準。**

---

### 步驟 3：確認合格門檻

確認評估標準後，使用 `ask_questions` 工具詢問（問題 7）：

```yaml
# ask_questions 呼叫範例（問題 7）
questions:
  - header: "合格門檻"
    question: "請選擇合格的通過分數門檻。超過門檻 → ✅ 合格，未達門檻 → ❌ 不合格"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "60 分"
        description: "寬鬆標準，適合初步篩選"
      - label: "70 分"
        description: "一般標準"
        recommended: true
      - label: "75 分"
        description: "中高標準"
      - label: "80 分"
        description: "嚴格標準，適合高品質知識庫"
      - label: "90 分"
        description: "極嚴格標準"
      - label: "自訂分數"
        description: "請在自由輸入欄輸入 0–100 之間的數字"
```

**等待 `ask_questions` 回傳結果後，記錄門檻值。**

---

### 步驟 4：掃描並讀取目標檔案

**4a. 使用 `ask_questions` 工具詢問評估目標（問題 8）：**

```yaml
# ask_questions 呼叫範例（問題 8）
questions:
  - header: "評估目標"
    question: "您要評估的目標是哪種形式？請在自由輸入欄提供對應路徑。"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "單一檔案"
        description: "請提供完整檔案路徑，例如：C:\\docs\\knowledge.md"
      - label: "整個資料夾"
        description: "請提供資料夾路徑，例如：C:\\docs\\knowledge_base\\"
      - label: "多個指定檔案"
        description: "請在自由輸入欄依序提供每個檔案的完整路徑，換行分隔"
```

**4b. 掃描目標路徑（取得檔案清單）：**

執行以下指令取得檔案清單：

```bash
python {{SKILL_ROOT}}/scripts/scan_files.py "{{TARGET_PATH}}"
```

- 如果路徑是單一檔案，直接進入 4c
- 如果是資料夾，向使用者確認掃描發現的檔案清單，詢問是否要排除某些檔案

**4c. 逐一讀取每個檔案內容：**

對每個待評檔案，**先判斷副檔名與檔案類型**，再選擇適合的讀取方式：

| 檔案類型 | 讀取方式 |
|:--------|:--------|
| `.md`, `.txt`, `.rst`, `.log` 等純文字 | 使用 `read_file` 工具直接讀取 |
| `.json`, `.yaml`, `.yml`, `.xml`, `.html`, `.csv` 等結構化文字 | 使用 `read_file` 工具直接讀取 |
| `.docx`, `.xlsx`, `.pptx` 等 Office 格式 | 使用終端機搭配適合的解析工具（如 `python-docx`、`openpyxl`）萃取純文字 |
| `.pdf` | 使用終端機搭配 PDF 解析工具（如 `pdfplumber`、`pymupdf`）萃取純文字 |
| 無法識別、加密或純圖片格式 | 標記「⚠️ 無法讀取」，跳過評分並計入統計 |

> **Context 保護：** 每個檔案讀取建議不超過 6000 字元，超過部分請截斷並在評語中標注「⚠️ 內容已截斷，評估基於前段內容」。
> **一次處理一個檔案**，評估完成後再讀取下一個，避免 context 溢出。

**4d. 前置處理：過濾 Metadata 結構**

讀取檔案內容後，**在送入評估前**，先識別並移除以下類型的 Metadata 結構（這些內容在建立知識庫時通常會被拿掉，不應影響內容品質評分）：

| Metadata 類型 | 識別特徵 | 處理方式 |
|:-------------|:--------|:--------|
| YAML Front Matter | 檔案開頭 `---` 與 `---` 之間的區塊 | 整段移除 |
| TOML Front Matter | 檔案開頭 `+++` 與 `+++` 之間的區塊 | 整段移除 |
| JSON-LD / 結構化資料 | `<script type="application/ld+json">...</script>` | 整段移除 |
| 文件屬性區塊 | 形如 `Author:`, `Date:`, `Version:`, `Status:` 等獨立鍵值列 | 整段移除 |
| 系統標籤或分類標記 | 形如 `tags: [...]`, `categories: [...]`, `keywords: [...]` | 整段移除 |

> **重要：** 移除 Metadata 後，評估的是**實際內容本體**。若移除後內容所剩極少（< 200 字元），則在報告中標注「⚠️ 有效內容過少（Metadata 占比過高）」並給予低分。

---

### 步驟 5：生成評估報告

**5a. 對每個檔案，逐項評分：**

- 評估對象為**已過濾 Metadata 後的實際內容**（見步驟 4d）
- 根據確認後的評估標準，為每個項目給出 0 至滿分之間的分數
- 給出每個評估項目的具體評語（1-2 句）
- 計算該檔案的總分
- 判斷是否合格（總分 ≥ 門檻值）

**5b. 生成 Markdown 報告，嚴格遵循以下結構：**

````markdown
# RAG 知識來源品質評估報告

> **評估日期：** {{TODAY}}
> **評估路徑：** `{{TARGET_PATH}}`
> **合格門檻：** {{THRESHOLD}} 分（滿分 100 分）

---

## 評估標準總覽

| # | 評估項目 | 配分 | 滿分條件 |
|:--|:--------|-----:|:--------|
| 1 | {{CRITERION_NAME}} | {{MAX_SCORE}} | {{FULL_SCORE_CONDITION}} |
...
| | **合計** | **100** | |

---

## 各檔案評估結果

### 📄 {{FILE_1_NAME}}

**路徑：** `{{FILE_1_PATH}}`
**檔案大小：** {{SIZE}} KB ｜ **類型：** {{EXT}}

#### 評分明細

| 評估項目 | 滿分 | 得分 | 評語 |
|:--------|-----:|-----:|:-----|
| {{CRITERION_1}} | {{MAX_1}} | {{SCORE_1}} | {{COMMENT_1}} |
| {{CRITERION_2}} | {{MAX_2}} | {{SCORE_2}} | {{COMMENT_2}} |
...
| **合計** | **100** | **{{TOTAL}}** | |

**整體評語：** {{OVERALL_COMMENT}}

**結果：** ✅ 合格 / ❌ 不合格（{{TOTAL}} 分，門檻 {{THRESHOLD}} 分）

---

（重複上述結構至所有檔案）

---

## 統計總表

| 檔案名稱 | {{COL_1}} | {{COL_2}} | ... | 總分 | 結果 |
|:--------|----------:|----------:|----:|-----:|:----:|
| {{FILE_1}} | {{S_1_1}} | {{S_1_2}} | ... | {{T_1}} | ✅ |
| {{FILE_2}} | {{S_2_1}} | {{S_2_2}} | ... | {{T_2}} | ❌ |

### 統計摘要

| 指標 | 數值 |
|:----|-----:|
| 評估檔案總數 | N |
| 合格檔案數 | n |
| 不合格檔案數 | n |
| 合格率 | N% |
| 平均分數 | N.N |
| 最高分 | N |
| 最低分 | N |
````

**5c. 使用 `ask_questions` 工具詢問儲存方式（問題 9）：**

```yaml
# ask_questions 呼叫範例（問題 9）
questions:
  - header: "報告儲存"
    question: "報告已生成完成！您希望如何處理這份報告？"
    multiSelect: false
    allowFreeformInput: true
    options:
      - label: "儲存至指定路徑"
        description: "請在自由輸入欄提供完整路徑，例如：C:\\output\\rag_report.md"
      - label: "儲存至與評估目標相同的資料夾"
        description: "自動命名為 rag_evaluation_report_{{TODAY}}.md"
        recommended: true
      - label: "不儲存，僅在對話中查看"
```

若使用者選擇前兩項，使用 `create_file` 工具儲存報告。

---

## C. 評分指南（LLM 評估時的判斷原則）

### C1. RAG 可檢索性（通用考量）

| 特徵 | 評分傾向 |
|:-----|:--------|
| 每個段落意義完整，可獨立被引用 | 高分 |
| 含有豐富的關鍵詞與具體名詞 | 高分 |
| 大量使用指代詞（它、這個、上述）而無明確對象 | 低分 |
| 全文一大段無結構 | 低分 |
| 含有大量「見附件」「如圖所示」但無圖片 | 0-低分 |

### C2. 內容品質（通用考量）

| 特徵 | 評分傾向 |
|:-----|:--------|
| 資訊有明確來源或日期 | 加分項 |
| 含有具體數字、版本號、規格 | 高分 |
| 大量廢話或填充性內容 | 扣分 |
| 語意重複或冗餘 | 扣分 |

### C3. 處理截斷檔案

若讀取內容因超過 6000 字元而截斷：
- 評估基於已讀取的部分
- 在每個評估項目評語中標注「⚠️ 內容已截斷」
- 整體評語中說明完整性無法完全確認

### C4. Metadata 過濾原則

- Metadata 結構（YAML Front Matter、文件屬性、標籤等）在知識庫建立時均會被移除，因此不應作為評估內容
- 若原始檔案 Metadata 占比極高（> 80%），應在報告中特別提示，建議檢視檔案是否有實質內容
- 移除 Metadata 不算扣分，但若移除後內容明顯匱乏，則影響「內容完整性」等相關項目得分

---

## D. 品質防護措施

- **絕對禁止** 一次讀取所有檔案後再統一評估（避免 context 溢出）
- **必須** 讀完一個檔案、評估完成後，再讀下一個
- **禁止** 虛構或推測未實際讀取的內容評分
- **若檔案無法讀取（二進位、加密等）：** 在報告中標記「⚠️ 無法讀取」，跳過評分並計入統計

---

## E. 結構目錄

```
rag-quality-evaluator/
  SKILL.md                      ← 本檔案（核心工作流程）
  scripts/
    scan_files.py               ← 掃描路徑，取得檔案清單（JSON 輸出）
  templates/
    report_template.md          ← 報告結構參考模板
```

> **注意：** 檔案讀取不依賴固定腳本，Agent 將根據副檔名與檔案類型自行選擇最適合的讀取方式。

