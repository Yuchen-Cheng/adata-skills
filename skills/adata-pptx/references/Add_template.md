# 如何增加新模板 (Add a New Template)

本指南說明如何為 PowerPoint 簡報技能添加一個全新的 template。

## 快速概述

一個 template 包含：
1. **Template 定義檔** (`layouts/template/<name>.md`) — 背景圖庫、色碼、字體、所有 slide layout 細節
2. **背景資料夾** (`assets/<name>_backgrounds/`) — 該 template 所需的背景圖片
3. **註冊** — 在 SKILL.md 中列出（可選，但建議新增到文檔）

---

## 步驟 1：規劃 Template 架構

### 1a · 決定背景圖清單
列出該 template 需要的所有背景圖片。例如 ADATA 有 11 張：
- `slide01_cover.jpg` — 封面  
- `slide02_agenda.jpg` — 議程
- `slide03_section_divider_blue.jpg` — §1 分隔線
- `slide04_content_blue.jpg` — §1 內容
- 等等...

建議至少包含：
- 1 × 封面背景
- 1 × 議程背景  
- N × 內容背景（可依色系/分段變化）
- 1 × 結尾背景

### 1b · 定義色碼系統
決定該 template 的調色盤。ADATA 使用：
- Deep Navy
- White  
- Section 1–4 accent 顏色

記錄每個顏色的 RGB/Hex 值。

### 1c · 定義字體
選擇 2–3 種字體，列出各級別標題、內文、說明文字的大小和顏色。

### 1d · Slide Layout 細節
規劃 5 種基本 layout（或依需要調整）：
- **Layout 01 — Cover** ： 標題、副標題、日期位置
- **Layout 02 — Agenda** ： 章節列表
- **Layout 03 — Section Divider** ： 分段標題  
- **Layout 04 — Content** ： 通用內容（搭配 patterns）
- **Layout 05 — End** ： 結尾頁

---

## 步驟 2：建立 Template 定義檔

在 `layouts/template/` 資料夾建立 `<name>.md` 檔案。

### 基本結構

```markdown
# Template: [Template 完整名稱]

## Template Metadata

**Template ID:** <name>  
**Background folder:** assets/<name>_backgrounds/  
**Background count:** [數量]

## Background Image Library

| Filename | Slide Role | Usage |
|----------|-----------|-------|
| slide01_cover.jpg | Cover | 封面 |
| slide02_agenda.jpg | Agenda | 議程 |
| ... | ... | ... |

## Colour Palette

| Name | RGB / Hex | Usage |
|------|-----------|-------|
| Primary | (R, G, B) | 標題、重點 |
| Secondary | (R, G, B) | 副標題 |
| ... | ... | ... |

## Typography

| Element | Font | Size | Colour |
|---------|------|------|--------|
| Title (Large) | Font Name | 55pt | Primary |
| Subtitle | Font Name | 30pt | Secondary |
| Body | Font Name | 24pt | Text |
| ... | ... | ... | ... |

## Design Rules

1. 背景圖片在每張投影片上都是必須的——不能使用純白或預設背景。
2. ...（列出該 template 的所有設計規則）

## Slide Layouts

### Layout 01 — Cover

**Background:** slide01_cover.jpg

**Placeholders:**
- Title: x:0.5 y:2.0 w:5.5 h:1.8, 55pt, bold
- Subtitle: x:0.5 y:3.9 w:5.5 h:0.8, 30pt
- Date: x:0.5 y:4.9 w:5.5 h:0.5, 16pt

**pptxgenjs Code:**
```javascript
const slide01 = pres.addSlide();
addBackground(slide01, "slide01_cover.jpg");
slide01.addText(title, {
  x: 0.5, y: 2.0, w: 5.5, h: 1.8,
  fontSize: 55, bold: true, color: "PRIMARY_COLOR"
});
// ...subtitle and date text...
```

### Layout 02 — Agenda

**Background:** slide02_agenda.jpg  
**Content:** 章節列表 (使用 pptxgenjs bullets)

**pptxgenjs Code:**
```javascript
const slide02 = pres.addSlide();
addBackground(slide02, "slide02_agenda.jpg");
slide02.addText(title, { x: ..., y: ..., ... });
slide02.addText(agendaItems.join("\n"), {
  x: ..., y: ..., bullet: true, ...
});
```

### Layout 03 — Section Divider

...

### Layout 04 — Content

...

### Layout 05 — End

...
```

### 關鍵要點

- **詳細的 pptxgenjs Code block**——直接複製即可用，無需調整
- **準確的座標**——檢查背景圖尺寸，確保 safe zone（安全區域）無覆蓋
- **色碼參考**——若使用變數，需在檔案頂部定義（例如 `SECTION_COLORS`）

---

## 步驟 3：準備背景圖片

1. **建立資料夾**  
   在 `assets/` 建立 `<name>_backgrounds/` 子資料夾。

2. **放置圖片**  
   將所有背景圖片放入該資料夾，命名須與 template 定義檔中的 "Background Image Library" 一致。

3. **檢驗格式**  
   - 推薦格式：JPG（高效壓縮）或 PNG（高品質）
   - 尺寸：1920×1080 px（16:9 比例）
   - 檔案大小：每張 ≤ 500 KB（保持簡報輕量）

---

## 步驟 4：測試 Template

### 4a · 驗證定義檔語法
確認 `layouts/template/<name>.md` 的 Markdown 格式正確，所有表格和 code block 都完整。

### 4b · 建立測試 generate.js
建立一個簡單的測試指令碼，使用新 template 生成一份簡報（3–5 張投影片），確認：
- 背景圖片正確載入
- 座標和文字位置符合預期
- 色碼和字體無誤

### 4c · 視覺檢查
轉換為圖片並檢查：
```bash
soffice --headless --convert-to png Presentation.pptx
```
- 文字未超出 safe zone
- 色碼正確
- 背景無扭曲

### 4d · 從現有 PPTX 分析 Template

**前提**：你已經有一個設計好的 PowerPoint 檔案，想要轉換為 template。

**Step 1: 運行分析腳本**

```bash
# 提供你的 PPTX 檔案和想要的 template 名稱
node scripts/analyze-template.js YourTemplate.pptx mytemplate
```

此命令會：
- ✅ 自動提取所有背景圖片到 `assets/mytemplate_backgrounds/`
- ✅ 提取所有 XML 檔案到 `pptx-analysis/mytemplate/xml/` 供分析
- ✅ 列出所有提取的圖片和詳細信息

**Step 2: 分析 XML 結構**

打開提取的 XML 檔案，查看投影片結構：
```
pptx-analysis/mytemplate/xml/ppt--slides--slide1.xml
```

在 XML 中尋找：
- `<p:shape>` — 文字框和圖形定義
- `<a:off x="..." y="...">` — 位置（EMU 單位）
- `<a:ext cx="..." cy="...">` — 尺寸
- `<a:rPr sz="...">` — 字體大小（百分之一的點數）
- `<a:srgbClr val="...">` — RGB 顏色

**Step 3: 建立 Template 定義檔**

參考 XML 數據，在 `layouts/template/mytemplate.md` 中記錄所有訊息：

```markdown
# Template: My Custom Template

## Template Metadata
**Template ID:** mytemplate  
**Background folder:** assets/mytemplate_backgrounds/  
**Background count:** [根據提取的圖片數量]

## Background Image Library
[根據提取的圖片列表建立表格]

## Colour Palette
[根據 XML 中的顏色數據]

## Typography
[根據 XML 中的字體大小]

## Slide Layouts
[根據 XML 座標數據建立 01–05]
```

---

## 步驟 5：在 SKILL.md 中註冊（可選）

編輯 SKILL.md，在 "Available Templates" 部分的表格中添加新行：

```markdown
| `<name>` | `layouts/template/<name>.md` | [描述] |
```

---

## 檢查清單

- [ ] Template 定義檔已建立：`layouts/template/<name>.md`
- [ ] 包含完整的背景圖庫表
- [ ] 包含色碼調色盤
- [ ] 包含字體規範  
- [ ] 包含所有 5 種 layout（或依需要調整）
- [ ] 每個 layout 都有準確的座標和 pptxgenjs code
- [ ] 背景資料夾已建立：`assets/<name>_backgrounds/`
- [ ] 所有背景圖片已放入資料夾
- [ ] 測試 generate.js 成功運行，視覺檢查無誤
- [ ] （選用）使用 `analyze-template.js` 分析現有 PPTX，提取圖片和 XML 以供參考

---

## 範例：最小 Template

若要快速建立 template，以下是最小需求：

1. **定義檔** (`layouts/template/simple.md`)
   - 至少 11 張背景圖（覆蓋 5 種 layout）
   - 1 個色碼系統（至少 3 色）
   - 字體規範（標題、內文）
   - 5 個 layout 定義 + pptxgenjs code

2. **背景資料夾** (`assets/simple_backgrounds/`)
   - 對應的 11 張 JPG/PNG

3. **測試**
   - 運行 `node generate.js`
   - 視覺驗證

---

## 相關檔案

- [SKILL.md](./SKILL.md) — 主技能指南
- [Add_pattern.md](./Add_pattern.md) — 如何增加新 pattern
- `layouts/template/adata.md` — ADATA template 參考實例
- `layouts/patterns/` — 已有的 16 個 pattern 供參考
