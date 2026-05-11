---
name: adata-pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# ADATA 威剛簡報 Skill

本 Skill 專為產出 **ADATA（威剛）品牌風格**的簡報而設計。所有簡報一律使用官方模板 `adata-template/adata-template.pptx`，嚴格遵守品牌色彩、字型與版面規範。

## Quick Reference

| Task | Guide |
|------|-------|
| 讀取 / 分析現有簡報 | `python -m markitdown presentation.pptx` |
| **來源為現有 PPTX → 轉換 ADATA 風格** | **見下方 [Source Conversion Mode](#source-conversion-mode-保留內容只改樣式)** |
| 從零建立（無來源）→ 使用 ADATA 模板 | Read [editing.md](editing.md) |
| 無模板從零建立（不建議） | Read [pptxgenjs.md](pptxgenjs.md) |

---

## 工作模式選擇

> **⚠️ 判斷模式是第一步，錯誤的模式會浪費大量時間。**

| 情境 | 使用模式 |
|------|---------|
| 使用者提供 source `.pptx` / `.ppt`，要求轉換為威剛風格 | **Source Conversion Mode**（保留內容，只改樣式） |
| 從零開始建立新簡報，或提供的 source 是文字/PDF/逐字稿 | **Template Mode**（以 ADATA 模板為起點，重建內容） |

**選擇規則：只要 source 是 PPTX 檔案 → 一律使用 Source Conversion Mode。**

---

## 模板路徑

**永遠使用以下官方模板作為起點：**

```
adata-template/adata-template.pptx
```

請勿自訂或替換模板。所有色彩、字型、版面已內建於模板中。

---

## ADATA 品牌規範（強制遵守）

### 品牌色彩

| 角色 | Hex | 使用場合 |
|------|-----|---------|
| 深海軍藍 | `#0E2841` | 封面、章節標題、結尾投影片背景 |
| 白色 | `#FFFFFF` | 深色背景上的所有文字 |
| 淺灰 | `#E8E8E8` | 內容投影片次要背景 |

### 章節強調色（依序循環）

循環順序：**Blue → Green → Orange → Magenta → Blue → …**

| 章節 | 名稱 | Hex | 主題參照 |
|------|------|-----|---------|
| 第 1 節 | 藍色 | `#5097FF` | `accent1` |
| 第 2 節 | 綠色 | `#19C711` | `accent2` |
| 第 3 節 | 橘色 | `#FF9000` | `accent3` |
| 第 4 節 | 洋紅色 | `#FF47FF` | `accent4` |
| 強調色 | 青色 | `#5FE6FF` | `accent5` |
| 強調色 | 亮綠色 | `#40FF00` | `accent6` |
| 超連結 | 紫色 | `#734BFF` | 僅用於連結 |

### 字型規範

| 元素 | 字型 | 大小 |
|------|------|------|
| 封面 / 章節標題 | **Arial Black** | 66pt |
| 內容標題 | **Arial Black** | 55pt |
| 副標題 | 版面預設 | 28–32pt |
| 內文 | 版面預設 | 24pt |

> ⚠️ 字型大小定義於版面配置的 `<a:lstStyle>` 中，**不得**於個別投影片覆蓋。

---

## 模板投影片結構

模板預設包含 **11 張投影片**，請依此規劃內容：

| 投影片 | 類型 | 用途 |
|--------|------|------|
| 1 | 封面（Cover） | 標題、副標題、日期 |
| 2 | 議程（Agenda） | 目錄 |
| 3 | 章節標題（Section Divider） | 第 1 節（藍色 `#5097FF`） |
| 4 | 內容（Content） | 第 1 節內容 |
| 5 | 章節標題（Section Divider） | 第 2 節（綠色 `#19C711`） |
| 6 | 內容（Content） | 第 2 節內容 |
| 7 | 章節標題（Section Divider） | 第 3 節（橘色 `#FF9000`） |
| 8 | 內容（Content） | 第 3 節內容 |
| 9 | 章節標題（Section Divider） | 第 4 節（洋紅色 `#FF47FF`） |
| 10 | 內容（Content） | 第 4 節內容 |
| 11 | 空白（Blank） | 結尾投影片 |

章節數量可依需求增減，但**強調色必須依 Blue → Green → Orange → Magenta 循環**。

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. 以模板為起點：`adata-template/adata-template.pptx`
2. Analyze template with `thumbnail.py`
3. Unpack → 調整投影片結構 → 編輯內容 → clean → pack

---

## Source Conversion Mode（保留內容，只改樣式）

**當 source 是 PPTX 檔案時，不重建投影片 — 直接在原始 XML 上套用 ADATA 品牌樣式。**

### 目標

| 修改項目 | 方式 |
|---------|------|
| 主題色彩 | 替換 `ppt/theme/theme1.xml`（一次修改，全部生效） |
| 標題字型與顏色 | 自動偵測每張投影片的標題文字，套用 Arial Black + 對應顏色 |
| 標題偵測方式 | ① `<p:ph type="title/ctrTitle">` 佔位符（最優先）② 位於投影片上方 30% 且有實質文字的文字框（位置啟發） |
| 副標題 | `<p:ph type="subTitle/body">` 套用相同顏色規則 |
| 顏色規則 | 深色背景頁：白色 `#FFFFFF`；淺色背景頁：海軍藍 `#0E2841` |
| 投影片背景 | 封面/章節頁：`#0E2841`；內容頁：白色/`#E8E8E8` |
| 硬編碼顏色 | 掃描 `<a:srgbClr>` 並對應替換為最近的 ADATA 品牌色 |

### 保留項目（不動）

- 所有投影片的文字內容、段落結構
- 圖片、圖表、表格位置與尺寸
- 投影片張數與順序
- 動畫與轉場（若有）

### 工作流程

```
1. 解壓縮 source
   python scripts/office/unpack.py source.pptx source-unpacked/

2. 解壓縮 ADATA 模板（取得 theme 參考）
   python scripts/office/unpack.py adata-template/adata-template.pptx adata-unpacked/

3. 替換主題檔（若 source 主題不是 ADATA；若已是 ADATA 主題則跳過）
   cp adata-unpacked/ppt/theme/theme1.xml source-unpacked/ppt/theme/theme1.xml

4. 執行轉換腳本

   若 source 已有 ADATA 背景圖片（blipFill），只替換顏色與字型：
   python scripts/convert_to_adata.py source-unpacked/ --colors-only

   若 source 背景是純色或無 ADATA 背景（從零轉換）：
   python scripts/convert_to_adata.py source-unpacked/ --dark-slides 1 44

5. 人工修正（腳本無法處理的細節）
   - 檢查每張投影片的背景分類是否正確（深色/淺色）
   - 修正過長標題（超出文字框）
   - 修正對比不足的文字顏色

6. Clean → Pack
   python scripts/clean.py source-unpacked/
   python scripts/office/pack.py source-unpacked/ output.pptx --original source.pptx
```

### 背景分類規則

| 投影片類型 | 背景色 | 文字色 |
|-----------|--------|--------|
| 封面（第 1 張） | `#0E2841` | `#FFFFFF` |
| 章節標題（Section Divider） | `#0E2841` + 章節強調色裝飾 | `#FFFFFF` |
| 內容投影片 | 白色或 `#E8E8E8` | `#0E2841` |
| 結尾投影片（最後 1 張） | `#0E2841` | `#FFFFFF` |

章節強調色必須依循 **Blue `#5097FF` → Green `#19C711` → Orange `#FF9000` → Magenta `#FF47FF`** 順序，不可跳序。

### 顏色對應表（硬編碼色 → ADATA）

| 原始色類型 | 替換為 |
|-----------|--------|
| 任何深藍底色 | `#0E2841` |
| 任何亮藍強調色 | `#5097FF` |
| 任何亮綠強調色 | `#19C711` |
| 任何橘色強調色 | `#FF9000` |
| 任何洋紅/紫強調色 | `#FF47FF` |
| 深色背景上的文字 | `#FFFFFF` |
| 淺色背景上的標題文字 | `#0E2841` |

> **注意**：腳本只替換確定是背景或裝飾用的顏色；圖片內的顏色無法修改。

### convert_to_adata.py 腳本

位於 `scripts/convert_to_adata.py`，執行以下操作：

1. 掃描所有 `ppt/slides/slide*.xml`
2. **自動偵測每張投影片的標題形狀**：
   - 優先：`<p:ph type="title">` / `type="ctrTitle"` 佔位符
   - 備選：位於投影片高度前 30%（y < 2057400 EMU）且含有實質文字的文字框
   - 略過：頁腳、日期、投影片編號佔位符
3. 將偵測到的標題形狀套用 **Arial Black** 字型 + 正確文字顏色
   - 深色背景頁 → `#FFFFFF`；淺色背景頁 → `#0E2841`
4. 同樣處理副標題佔位符（`subTitle` / `body idx=1`）
5. 批次替換所有硬編碼的非 ADATA 強調色（見顏色對應表）
6. 視模式調整投影片背景（`--colors-only` 模式下略過）
7. 輸出修改摘要（修改了幾張投影片、幾處顏色、幾處樣式）

**閱讀 [editing.md → Source Conversion Details](editing.md#source-conversion-details) 取得腳本完整說明與手動覆寫指引。**

---

## 內容設計規則

### 背景

- **深色背景**（`#0E2841`）：封面、章節標題、結尾投影片
- **淺色背景**：內容投影片（由模板版面配置控制）

### 內容密度

- 每張內容投影片最多 **6 個項目**，每項最多 **15 字**
- 每張章節標題最多 **3 個副標題**，每項最多 **8 字**

### 章節一致性

- 內容投影片標題的強調色必須與其對應章節標題顏色相同
- 所有標題使用 **Arial Black**，不得替換

### 內容呈現優先順序

優先使用視覺化結構，而非純文字：

| 內容類型 | 建議呈現方式 |
|---------|------------|
| 順序步驟、流程、工作流程 | 流程圖（帶箭頭） |
| 分支邏輯、決策樹 | 流程圖（含決策節點） |
| 多項目或屬性比較 | 表格 |
| 結構化資料、規格、功能列表 | 表格 |
| 簡單列舉（≤ 6 個簡短項目） | 項目符號清單 |
| 敘述性或說明性文字 | 純段落 |
| 時間序列趨勢數據 | 折線圖 |
| 類別數字比較 | 長條圖 / 直條圖 |
| 整體佔比分析（≤ 6 段） | 圓餅圖 / 環形圖 |

### 表格樣式

- 標題列：深海軍藍底（`#0E2841`）、白色粗體文字
- 資料列：白色 / 淺灰（`#E8E8E8`）交替，海軍藍文字
- 欄寬：依投影片寬度平均分配

### 圖表樣式

- 系列色彩循環使用章節強調色（藍 `#5097FF` → 綠 `#19C711` → 橘 `#FF9000` → 洋紅 `#FF47FF`）
- 繪圖背景：白色或透明，**不使用深海軍藍**
- 座標軸標籤：最小 12pt，使用 `#0E2841`
- 最多 5 個系列（可讀性限制）

---

## ADATA 設計禁止事項

- **禁止**更改品牌色彩或使用模板外的色彩
- **禁止**替換 Arial Black 字型
- **禁止**在深色背景上使用深色文字（對比不足）
- **禁止**在內容投影片使用深海軍藍（`#0E2841`）作為背景
- **禁止**章節強調色亂序使用（必須依 Blue → Green → Orange → Magenta 循環）
- **禁止**在標題下方加裝飾性底線
- **禁止**每張投影片使用相同版面（應善用章節標題、表格、圖表等多樣版面）
- **禁止**在模板既有版面上覆蓋字型大小

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

### Windows (use PowerPoint COM automation)

`soffice.py` relies on `socket.AF_UNIX` and **fails on Windows**. Use PowerPoint COM instead:

```python
import win32com.client, os, pathlib

pptx_path = str(pathlib.Path("output.pptx").resolve())
out_dir    = str(pathlib.Path("slides_qa").resolve())
os.makedirs(out_dir, exist_ok=True)

ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = 1
prs = ppt.Presentations.Open(pptx_path, ReadOnly=True, Untitled=False, WithWindow=False)
for i, slide in enumerate(prs.Slides, 1):
    slide.Export(os.path.join(out_dir, f"slide-{i:02d}.jpg"), "JPG", 1920, 1080)
prs.Close()
ppt.Quit()
```

Save as `export_slides.py` and run with `python export_slides.py`.

### Linux / macOS (LibreOffice)

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images
