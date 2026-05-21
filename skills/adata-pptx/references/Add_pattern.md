# 如何增加新 Pattern (Add a New Pattern)

本指南說明如何為 PowerPoint 簡報技能添加一個全新的內容 pattern。

## 快速概述

一個 pattern 代表簡報投影片**內容區域**的可重用佈局（圖表、表格、列表等）。Pattern 檔案位於 `layouts/patterns/` 資料夾。

目前系統支援 **16 個 pattern**，每個專注於特定的內容型態。

---

## Pattern 命名約定

Pattern 檔案命名格式：

```
pattern-<short-name>.md
```

例如：
- `pattern-section-tag-header.md`
- `pattern-stat-cards.md`
- ...
- `pattern-enhanced-unit-grid.md`

命名建議：使用能清楚描述 pattern 用途的簡短名稱，以連字符分隔英文單詞。

---

## 步驟 1：設計 Pattern 結構

### 1a · 決定用途
明確定義該 pattern 解決的問題。例如：
- "展示 4 個並排的關鍵指標"
- "左右對比兩項方案"  
- "組織架構圖"
- "時間軸 + 里程碑"

### 1b · 視覺設計
在紙上或設計工具中描繪該 pattern 的視覺佈局：
- 元件位置和大小
- 顏色使用（採用 template 的色碼）
- 字體大小和樣式
- 間距和對齐

### 1c · 座標和尺寸
在 pptxgenjs 座標系統中測量：
- 參考背景圖尺寸（寬 10 英寸、高 5.625 英寸）
- 計算各元件的 x, y, w, h 值  
- 注意 safe zone（若 template 有定義）

---

## 步驟 2：建立 Pattern 定義檔

在 `layouts/patterns/` 資料夾建立 `pattern-<name>.md` 檔案。

### 基本結構

```markdown
# Pattern — [Pattern 完整名稱]

**When to use:** [獨立敘述，說明何時使用此 pattern]

## Visual Structure

[ASCII art 或文字描述投影片佈局，包括座標參考]

例：
\`\`\`
┌────────────────────────────────────────────────────────────┐
│ [標題區]  y=0.4                                             │
├────────────────────────────────────────────────────────────┤
│ [主要內容]  y=1.8                                           │
│ • 項目 1                                                    │
│ • 項目 2                                                    │
│ • 項目 3                                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
\`\`\`

## Key Elements

| Element | X | Y | Width | Height | Font | Colour |
|---------|---|---|-------|--------|------|--------|
| 標題 | 0.5 | 0.4 | 8.5 | 0.5 | Bold 36pt | Primary |
| 內容區 | 0.5 | 1.8 | 8.5 | 3.5 | Regular 18pt | Body |

## pptxgenjs Code

```javascript
// Pattern [Name]
// 假設背景已添加，slide 物件已存在

slide.addText("[標題文字]", {
  x: 0.5, y: 0.4, w: 8.5, h: 0.5,
  fontSize: 36, bold: true, color: "0066CC"
});

slide.addText("[內容文字]", {
  x: 0.5, y: 1.8, w: 8.5, h: 3.5,
  fontSize: 18, color: "333333"
});
// ... 其他元件
```

## Usage Notes

- 此 pattern 適用於 [描述適用情況]
- 可搭配 Pattern [X]、[Y] 組合使用
- 注意 safe zone 上限：y ≤ 5.35（若 template 有此限制）

## Example

[簡短的實際使用示例或參考]
```

### 重要要點

1. **"When to use" 敘述必須獨立**——不應引用其他 pattern 或詳細說明  
2. **座標精確**——根據背景圖測量，確保 safe zone 無覆蓋
3. **完整的 pptxgenjs code**——應可直接複製使用，無需調整座標
4. **視覺參考**——ASCII art 有助於快速理解佈局

---

## 步驟 3：驗證 Pattern 格式

運行 `list-patterns.js` 腳本驗證新 pattern 是否正確格式化：

```bash
node scripts/list-patterns.js
```

檢查輸出：
- 新 pattern 是否出現在清單中
- "When to use" 描述是否正確提取

## 步驟 3b：從範例簡報分析 Pattern（推薦）

**前提**：你已經有一個展示該 pattern 樣子的簡報檔案。

**Step 1: 運行分析腳本**

```bash
# 分析範例簡報
node scripts/analyze-pattern.js pattern-example.pptx

# 或分析特定投影片
node scripts/analyze-pattern.js pattern-example.pptx 1
```

此命令會：
- ✅ 列出所有投影片中的文字內容
- ✅ 提取座標數據（x, y, width, height）
- ✅ 識別字體大小
- ✅ 檢測 RGB 顏色

**Step 2: 分析輸出數據**

根據腳本輸出，記錄：
- 文字框位置（座標）
- 文字大小（點數）
- 顏色代碼（RGB）
- 整體佈局結構

**Step 3: 建立 Pattern 定義檔**

使用分析數據，在 `layouts/patterns/pattern-<name>.md` 中填寫：

```markdown
# Pattern — [Name]

**When to use:** [描述用途]

## Visual Structure
[根據分析結果描述佈局]

## Key Elements
[根據座標、字體、顏色建立表格]

## pptxgenjs Code
[根據提取的座標寫出完整的 code]
```

---

## 步驟 4：測試 Pattern

### 4a · 建立測試 generate.js
建立一份測試簡報，使用新 pattern：

```javascript
const pres = new pptxgen();
const slide = pres.addSlide();
addBackground(slide, "slide04_content_blue.jpg"); // 或其他背景

// 複製新 pattern 的 pptxgenjs code，填入實際數據
slide.addText("Pattern Test", {
  x: 0.5, y: 0.4, w: 8.5, h: 0.5,
  fontSize: 36, bold: true
});
// ... 其他元件

pres.writeFile({ fileName: "PatternTest.pptx" });
```

### 4b · 視覺檢查
轉換為圖片：
```bash
soffice --headless --convert-to png PatternTest.pptx
```

檢查：
- 文字位置和大小是否符合預期
- 色碼是否正確
- 與背景的對比是否充分

### 4c · 確認 Pattern 清單
運行 `list-patterns.js` 驗證新 pattern 出現在清單中：
```bash
node scripts/list-patterns.js
```

---

## 步驟 5：現有 Pattern 清單和最佳實踐

### 查看所有已有的 Pattern

運行以下指令查看所有已有的 pattern：

```bash
node scripts/list-patterns.js
```

此命令會列出所有可用 pattern 及其用途描述。

### Pattern 設計最佳實踐

1. **單一責任**  
   每個 pattern 應專注於一種內容型態，不應過度通用。

2. **色彩一致性**  
   使用 template 定義的色碼，不應發明新顏色。

3. **安全區域**  
   確保文字和重要元件不超過 safe zone 界限。

4. **排版清晰**  
   - 標題應粗體且充分大
   - 內文應有清晰的層級
   - 間距應充分，避免擁擠

5. **可重用性**  
   Pattern 應足夠通用，可適用於多種內容，但亦應明確其用途。

6. **無 Unicode 符號**  
   使用 pptxgenjs `bullet: true` 代替 •、◆ 等符號。

---

## 檢查清單

- [ ] Pattern 名稱已決定（例：`section-tag-header`）
- [ ] 檔案已建立：`layouts/patterns/pattern-<name>.md`
- [ ] "When to use" 敘述已撰寫（獨立、簡潔）
- [ ] Visual Structure 已繪製（ASCII art 或描述）
- [ ] Key Elements 表已填寫（座標、字體、顏色）
- [ ] 完整的 pptxgenjs code block 已提供
- [ ] （推薦）使用 `analyze-pattern.js` 從範例簡報分析佈局
- [ ] 測試 generate.js 成功運行，視覺檢查無誤
- [ ] 運行 `node scripts/list-patterns.js` 驗證格式

---

## 相關檔案

- [SKILL.md](./SKILL.md) — 主技能指南
- [Add_template.md](./Add_template.md) — 如何增加新 template
- `layouts/patterns/` — 已有 pattern 檔案（16 個）
- `layouts/template/adata.md` — Template 參考（包含 pattern 使用範例）
- `scripts/list-patterns.js` — 列出所有 pattern 的工具
