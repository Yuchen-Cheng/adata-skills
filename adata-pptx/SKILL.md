---
name: adata-pptx
description: "Use this skill whenever creating or editing ADATA PowerPoint presentations using the 2026-ADATA-PPT Template.potx. Covers cover slides, agenda, section dividers, content slides, charts, images, and bulk generation from data — all constrained to ADATA brand colors and layouts. Trigger whenever the user mentions ADATA (威剛) slides, ADATA (威剛) deck, ADATA (威剛) presentation, or asks to create a presentation in the ADATA (威剛) style."
---

# ADATA PPT Skill

Two workflows available — pick the one that fits your task.

| Workflow | When to use | Command |
|----------|-------------|---------|
| **Convert existing PPTX** | Re-brand an existing deck to ADATA style | `python .agents/skills/adata-pptx/scripts/convert_pptx.py source.pptx [output.pptx]` |
| **Build from scratch** | Create a new ADATA deck from Markdown content | See [editing.md](editing.md) |
| **Add charts / images** | Enrich slides with charts, product images, or data visualizations | See § [Chart Slides](#chart-slides-python-pptx-chart) / [Image Slides](#image-slides) |
| **Bulk generation** | Generate many slides automatically from CSV / JSON data | See § [Bulk Generation](#bulk-generation-from-data) |

Dependency: `pip install python-pptx lxml pandas pillow`

---

## 1 — Convert an Existing PPTX

### Usage

```powershell
python .agents/skills/adata-pptx/scripts/convert_pptx.py  source.pptx  output-adata.pptx
```

Omit the output name to auto-generate `<source>-adata.pptx`.

### What is preserved

| Element | Status | Notes |
|---------|--------|-------|
| Title text | ✅ | Placed into template title placeholder; font/size/colour from template |
| Subtitle text | ✅ | Placed into subtitle placeholder |
| Body text (paragraphs) | ✅ | Placed into body placeholder; inherits template styling |
| Images | ✅ | Re-inserted with coordinates scaled to ADATA slide dimensions |
| Tables | ✅ | Recreated with dark-navy header, accent first column |
| Speaker notes | ✅ | Copied verbatim |
| Charts / SmartArt | ⚠️ | Text extracted as plain paragraphs; graphic not preserved |
| Animations / transitions | ❌ | Stripped (ADATA template has none) |
| Source fonts / colours | ❌ | Replaced by ADATA brand (Arial Black titles, template body styling) |

### Slide auto-classification

| Source slide | Mapped to | Rule |
|---|---|---|
| First slide | **Cover** | Always |
| Title only, no body/images/tables | **Section Divider** | Empty content |
| Title + ≤ 2 body lines, no images/tables | **Section Divider** | Sparse content |
| Last slide if empty | **Closing** | Position + empty |
| Everything else | **Content** | Default |

Section dividers increment a section counter. Accent colours cycle:
**Blue** `#5097FF` → **Green** `#19C711` → **Orange** `#FF9000` → **Magenta** `#FF47FF` (wraps after 4).

### Layout mapping

| Slide type | Template layout | Placeholders used |
|---|---|---|
| Cover | Layout 0 — 標題投影片 | idx 0 (title 66pt), idx 10 (subtitle 32pt) |
| Divider | Layout 2 — 章節標題 | idx 0 (title 66pt), idx 10 (subtitles 28pt) |
| Content | Layout 5 — 只有標題 | idx 0 (title 55pt), idx 1 (subtitle 30pt), idx 2 (body 24pt) |
| Closing | Layout 10 — 空白 | Text box if title present |

All title sizes, subtitle sizes, and body sizes are **inherited from the template layout** — no hardcoded overrides.

### Post-conversion checklist

1. Open in PowerPoint and review visually.
2. Confirm section divider + following content slides share the same accent colour.
3. Adjust slides where images or tables overlap text.
4. If a content slide has > 6 body items, consider splitting.

---

## 2 — Build from Scratch

See [editing.md](editing.md) for the full template-based workflow:
`content.md` → `md2json.py` → `unpack` → `add_slide` → `edit_slides` (auto-reorder) → `clean` → `pack`.

Unlimited sections supported — colours cycle Blue → Green → Orange → Magenta → …

---

## Template Reference

### Template structure (11 slides)

| Slide | Type | Purpose |
|-------|------|---------|
| 1 | Cover | Title, subtitle, date |
| 2 | Agenda | Table of contents |
| 3 | Section Divider | Section 1 (Blue) |
| 4 | Content | Section 1 content |
| 5 | Section Divider | Section 2 (Green) |
| 6 | Content | Section 2 content |
| 7 | Section Divider | Section 3 (Orange) |
| 8 | Content | Section 3 content |
| 9 | Section Divider | Section 4 (Magenta) |
| 10 | Content | Section 4 content |
| 11 | Blank | Closing |

### Slide layouts (0-based index)

| Index | Name (zh-TW) | English | Placeholders |
|-------|-------------|---------|--------------|
| 0 | 標題投影片 | Cover | idx 0 (66pt), idx 10 (32pt), idx 11 (16pt) |
| 1 | 標題及內容 | Title + Content | idx 0 (66pt), idx 13 (28pt body) |
| 2 | 章節標題 | Section Header | idx 0 (66pt), idx 10 (28pt) |
| 3 | 兩個內容 | Two Content | idx 0 (55pt), idx 1, idx 2 (24pt) |
| 4 | 比較 | Comparison | idx 0 (66pt), idx 10 (28pt) |
| 5 | 只有標題 | Title Only | idx 0 (55pt), idx 1 (30pt), idx 2 (24pt) |
| 6 | 1_比較 | Sec 1 Comparison | idx 0 (66pt), idx 10 (28pt) |
| 7 | 1_只有標題 | Sec 1 Title Only | idx 0 (55pt), idx 1 (30pt), idx 2 (24pt) |
| 8 | 2_比較 | Sec 2 Comparison | idx 0 (66pt), idx 10 (28pt) |
| 9 | 2_只有標題 | Sec 2 Title Only | idx 0 (55pt), idx 1 (30pt), idx 2 (24pt) |
| 10 | 空白 | Blank | (none) |

### Color palette

| Role | Hex | Usage |
|------|-----|-------|
| Dark Navy | `#0E2841` | Background, dark emphasis |
| White | `#FFFFFF` | Text on dark backgrounds |
| Light Gray | `#E8E8E8` | Secondary backgrounds |
| Section 1 — Blue | `#5097FF` | accent1 |
| Section 2 — Green | `#19C711` | accent2 |
| Section 3 — Orange | `#FF9000` | accent3 |
| Section 4 — Magenta | `#FF47FF` | accent4 |
| Cyan | `#5FE6FF` | accent5 — highlights |
| Bright Green | `#40FF00` | accent6 — sparingly |
| Hyperlink Purple | `#734BFF` | Links only |

### Typography

| Element | Font | Size | Source |
|---------|------|------|--------|
| Cover / divider title | Arial Black | 66pt | Layout lstStyle |
| Content title | Arial Black | 55pt | Layout lstStyle |
| Subtitle | Layout default | 28–32pt | Layout lstStyle |
| Body text | Layout default | 24pt | Layout lstStyle |

> Font sizes are defined in the template layout's `<a:lstStyle>`. The conversion script does **not** override sizes — it only sets font face (Arial Black) and colour on titles.

### Design rules

- **Dark backgrounds** on cover, dividers, and closing
- **Light backgrounds** on content slides
- **Section accent colour** on content slide titles must match its divider
- **Arial Black** for all titles — never substitute
- Max **6 body items** per content slide, **15 words** per item
- Max **3 subtitles** per divider, **8 words** each

#### Content representation priority

**Prefer visual structures over plain text whenever the content allows it.**

| Content type | Preferred representation |
|---|---|
| Sequential steps, processes, workflows | **Flowchart** (`shape: rect`, with arrows) |
| Branching logic, decision trees | **Flowchart** (include `diamond` decision nodes) |
| Comparisons across multiple items or attributes | **Table** |
| Structured data, specs, feature lists | **Table** |
| Simple enumeration (≤ 6 short items, no natural structure) | Bullet list |
| Narrative or explanatory text | Plain paragraphs |
| Trend data over time | **Line chart** (§ Chart Slides) |
| Numeric comparisons across categories | **Bar / column chart** (§ Chart Slides) |
| Parts-of-whole breakdown (≤ 6 segments) | **Pie / donut chart** (§ Chart Slides) |

> **Rule:** If content can be expressed as a chart, flowchart, or table, always choose that over bullet text. Use bullet lists only when no visual structure applies. Never convert a natural table, process, or data set into a bullet list.

---

## Scripts

All scripts are in `.agents/skills/adata-pptx/scripts/`. Paths below are relative to the skill folder.

| Script | Purpose |
|--------|---------|
| `scripts/convert_pptx.py` | Convert existing PPTX → ADATA style |
| `scripts/md2json.py` | Markdown → slides.json |
| `scripts/edit_slides.py` | Bulk-edit slide content from JSON |
| `scripts/add_slide.py` | Duplicate a content slide |
| `scripts/clean.py` | Remove orphaned slide files |
| `scripts/thumbnail.py` | Generate thumbnail grid |
| `scripts/flowchart.py` | Render flowcharts + native tables onto slides |
| `scripts/office/unpack.py` | Unpack PPTX to folder |
| `scripts/office/pack.py` | Pack folder to PPTX |

**Rules:**
- If a topic needs more than 6 bullets, **split it across two content slides** (duplicate the slide with `add_slide.py`).
- Prefer short, scannable phrases over full sentences.
- Each item should express one idea only — no compound bullets joined with `;` or `,`.
- When converting source material (articles, docs), **summarise and condense** — do not copy paragraphs verbatim.

---

## Flowchart Slides (Native PPT Shapes)

Flowcharts use **PowerPoint's built-in preset geometry shapes** (`flowChartProcess`, `flowChartDecision`, `flowChartTerminator`, etc.) and `<p:cxnSp>` connectors with arrow heads — **not images or SmartArt**.

### Supported node shapes

| `shape` value | PPT preset | Use for |
|---------------|-----------|---------|
| `oval`    | flowChartTerminator | Start / End |
| `rect`    | flowChartProcess    | Process step |
| `diamond` | flowChartDecision   | Decision / Branch |
| `para`    | flowChartInputOutput | Input / Output |
| `doc`     | flowChartDocument   | Document output |
| `db`      | flowChartDatabase   | Database / Storage |

### `content.md` syntax — flowchart code block

Place a ` ```flowchart ` fenced block inside a `###` slide.  
First token after the fence sets the layout direction (`TB` = top-to-bottom, `LR` = left-to-right).

```markdown
### Process Flow
> System Overview

```flowchart TB
oval:n1:開始
rect:n2:讀取資料
diamond:n3:資料正確?
rect:n4:寫入資料庫
rect:n5:記錄錯誤
oval:n6:結束
n1->n2
n2->n3
n3->n4:Yes
n3->n5:No
n4->n6
n5->n6
```
```

### `slides.json` format — flowchart

```json
"slide4.xml": {
  "title": "Process Flow",
  "subtitle": "System Overview",
  "flowchart": {
    "direction": "TB",
    "nodes": [
      {"id": "n1", "shape": "oval",    "text": "Start"},
      {"id": "n2", "shape": "rect",    "text": "Process"},
      {"id": "n3", "shape": "diamond", "text": "Success?"},
      {"id": "n4", "shape": "rect",    "text": "Done"},
      {"id": "n5", "shape": "oval",    "text": "End"}
    ],
    "edges": [
      {"from": "n1", "to": "n2"},
      {"from": "n2", "to": "n3"},
      {"from": "n3", "to": "n4", "label": "Yes"},
      {"from": "n3", "to": "n2", "label": "No"},
      {"from": "n4", "to": "n5"}
    ]
  }
}
```

Optional flowchart keys: `fill_color` (hex, overrides section accent), `line_color` (default white), `text_color` (default white).

> **Body text is cleared** when a flowchart is present — do not specify `"body"` on the same slide.

---

## Table Slides (Native PPT Table)

Tables use **PowerPoint's native `<a:tbl>` table element** — not text boxes or images.  
Header row: dark-navy fill, white bold text.  
Data rows: alternating white / light-gray rows, navy text.

### `content.md` syntax — Markdown pipe table

Place a standard pipe table inside a `###` slide:

```markdown
### Feature Comparison
> ADATA vs Competitors

| Feature      | ADATA        | Brand A      | Brand B      |
|-------------|-------------|-------------|-------------|
| Read Speed   | 7,400 MB/s  | 6,800 MB/s  | 5,000 MB/s  |
| Write Speed  | 6,900 MB/s  | 6,000 MB/s  | 4,200 MB/s  |
| DRAM Buffer  | ✓           | ✓           | ✗           |
| Warranty     | 5 years     | 5 years     | 3 years     |
```

### `slides.json` format — table

```json
"slide6.xml": {
  "title": "Feature Comparison",
  "subtitle": "ADATA vs Competitors",
  "table": {
    "header": ["Feature", "ADATA", "Brand A", "Brand B"],
    "rows": [
      ["Read Speed",  "7,400 MB/s", "6,800 MB/s", "5,000 MB/s"],
      ["Write Speed", "6,900 MB/s", "6,000 MB/s", "4,200 MB/s"],
      ["DRAM Buffer", "✓",          "✓",           "✗"],
      ["Warranty",    "5 years",    "5 years",     "3 years"]
    ]
  }
}
```

Optional key: `header_fill` (hex, default `0E2841` dark navy).

> **Body text is cleared** when a table is present — do not specify `"body"` on the same slide.

### Section Divider Structure

Section divider slides (3, 5, 7, 9) have:
```
[Section Title — white, Arial Black 66pt, bottom-aligned]
[3 subtitle items — listed bullet points]
```

---

## Chart Slides (python-pptx Chart)

Charts use **python-pptx's native chart objects** placed on content slides (Layout 5 — 只有標題).  
Always apply ADATA brand colors to chart series — never use the library's default color scheme.

### ADATA color constants for charts

```python
from pptx.dml.color import RGBColor

# Cycle through these for multi-series charts
ADATA_ACCENT = [
    RGBColor(0x50, 0x97, 0xFF),  # Blue    (section 1)
    RGBColor(0x19, 0xC7, 0x11),  # Green   (section 2)
    RGBColor(0xFF, 0x90, 0x00),  # Orange  (section 3)
    RGBColor(0xFF, 0x47, 0xFF),  # Magenta (section 4)
    RGBColor(0x5F, 0xE6, 0xFF),  # Cyan    (highlight)
]
ADATA_NAVY  = RGBColor(0x0E, 0x28, 0x41)
ADATA_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
```

### Adding a chart to a content slide

```python
from pptx import Presentation
from pptx.util import Inches
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation('.agents/skills/adata-pptx/adata-template.pptx')
layout = prs.slide_layouts[5]   # 只有標題 — Title Only
slide  = prs.slides.add_slide(layout)
slide.shapes.title.text = "Q4 Sales Comparison"

chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('ADATA',      (120, 145, 130, 180))
chart_data.add_series('Competitor', ( 90, 110, 105, 130))

# Position chart below title placeholder (top ≈ 1.5")
chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1.5), Inches(9.0), Inches(5.0),
    chart_data)
chart = chart_frame.chart

# Apply ADATA accent colors to series
for i, series in enumerate(chart.series):
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = ADATA_ACCENT[i % len(ADATA_ACCENT)]

# Hide chart title — the slide title is sufficient
chart.has_title = False

prs.save('output.pptx')
```

### Supported chart types

| Chart type | `XL_CHART_TYPE` constant | Best for |
|---|---|---|
| Clustered column | `COLUMN_CLUSTERED` | Category comparisons |
| Stacked column (%) | `COLUMN_STACKED_100` | Composition breakdown |
| Clustered bar | `BAR_CLUSTERED` | Long category labels |
| Line | `LINE` | Trends over time |
| Pie | `PIE` | Parts-of-whole (≤ 6 segments) |
| Scatter | `XY_SCATTER` | Correlation / distribution |

### Chart design rules

- **Series colors:** cycle `ADATA_ACCENT` list (`blue → green → orange → magenta`)
- **Chart title:** `chart.has_title = False` — slide title serves as the chart title
- **Plot background:** white (`#FFFFFF`) or transparent — never dark navy
- **Axis labels:** minimum 12 pt; use ADATA Navy (`#0E2841`) for text
- **Legend:** bottom or right; hide when only one series
- **Max series per chart:** 5 (readability)
- **Gridlines:** light gray only; remove vertical gridlines for column/bar charts
- **Chart placeholder text:** `chart.has_title = False` already suppresses the embedded title

---

## Image Slides

Images are placed on content slides using `add_picture()`.  
Always position below the title placeholder (top ≥ 1.4") with at least 0.5" margin from all edges.

### Adding an image to a content slide

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation('.agents/skills/adata-pptx/adata-template.pptx')
layout = prs.slide_layouts[5]   # 只有標題 — Title Only
slide  = prs.slides.add_slide(layout)
slide.shapes.title.text = "Product Overview"

# Add image — auto-width preserves aspect ratio
pic = slide.shapes.add_picture(
    'product.png',
    Inches(0.5), Inches(1.5),
    height=Inches(5.0))

# Center horizontally
pic.left = int((prs.slide_width - pic.width) / 2)

prs.save('output.pptx')
```

### Pre-compressing with Pillow (images > 2 MB)

```python
from PIL import Image
import io

img = Image.open('large_photo.jpg')
img.thumbnail((1920, 1080))            # Resize to max 1920×1080
buf = io.BytesIO()
img.save(buf, format='JPEG', quality=85, optimize=True)
buf.seek(0)
pic = slide.shapes.add_picture(buf, Inches(0.5), Inches(1.5), height=Inches(5))
```

### Image rules

- **Position:** top ≥ 1.4" (below title); 0.5" margin from all slide edges
- **Max size:** slide is 10" × 7.5" — keep images within bounds; max height ≈ 5.5"
- **Format:** PNG (supports transparency); JPEG for photos
- **Compression:** pre-compress with Pillow if source file > 2 MB
- **Paths:** use `os.path.abspath()` to avoid file-not-found errors in scripts

---

## Bulk Generation from Data

Generate multiple ADATA content slides from CSV or JSON data.  
**Always** start from the ADATA template — never use a blank `Presentation()`.

### From CSV (pandas)

```python
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt

prs    = Presentation('.agents/skills/adata-pptx/adata-template.pptx')
layout = prs.slide_layouts[5]   # 只有標題 — Title Only

df = pd.read_csv('products.csv')   # expected columns: name, spec, speed, capacity

for _, row in df.iterrows():
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = row['name']

    # Subtitle placeholder (idx 1)
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 1:
            ph.text = row['spec']
            break

    # Body text box for additional specs
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(9), Inches(4))
    tf    = txBox.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = f"Speed: {row['speed']}   Capacity: {row['capacity']}"

prs.save('product-catalog.pptx')
```

### From JSON

```python
import json
from pptx import Presentation

prs    = Presentation('.agents/skills/adata-pptx/adata-template.pptx')
layout = prs.slide_layouts[5]

with open('data.json', encoding='utf-8') as f:
    records = json.load(f)

for item in records:
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = item['title']
    # ... populate remaining placeholders

prs.save('output.pptx')
```

### Bulk generation rules

- **Template:** always `Presentation('adata-template.pptx')` — never `Presentation()`
- **Layout:** use Layout 5 (`只有標題`) for data-driven content slides
- **Max items per slide:** ≤ 6 body items — split large records into additional slides
- **Large datasets:** split into multiple PPTX files if slide count > 30
- **Font / color:** set titles to Arial Black; body inherits template defaults
- **Dependencies:** `pip install pandas` (CSV), `pip install openpyxl` (Excel `.xlsx`)

---

## Markdown Content File Format

Create a `content.md` file as the **single source of truth** before building the PPT. The markdown structure maps directly to ADATA slide types.

### Format

```markdown
---
title:
  - Line 1
  - Line 2
subtitle: Presentation subtitle
date: 2026/04/24
---

## Section Title
- Subtopic A
- Subtopic B
- Subtopic C

### Slide Title
> Slide subtitle

- Bullet item 1
- Bullet item 2
- Bullet item 3

### Another Slide
> Another subtitle

1. Numbered item 1
2. Numbered item 2
3. Numbered item 3
```

### Mapping Rules

| Markdown Element | ADATA Slide Element | PowerPoint XML |
|-----------------|---------------------|----------------|
| YAML `title` (list) | Cover title (multi-line) | `<a:br/>` between lines |
| YAML `subtitle` | Cover subtitle | — |
| YAML `date` | Cover date (defaults to today) | — |
| `## Heading` | Section divider slide | slide 3/5/7/9 |
| `- item` after `##` | Divider subtitles (max 3) | — |
| `### Heading` | Content slide title | slide 4/6/8/10 or duplicated |
| `> text` after `###` | Content slide subtitle | — |
| `- item` in body | Bullet point | `<a:buChar char="&#x2022;"/>` |
| `1. item` in body | Numbered item | `<a:buAutoNum type="arabicPeriod"/>` |
| Plain text line | Plain paragraph (no bullet) | — |

> **Density rule:** A `###` slide must have **≤ 6 body items**. If your outline produces more, add a second `###` slide for the overflow. A `##` divider must have **≤ 3 subtitles**.

### Conversion

```bash
python .agents/skills/adata-pptx/scripts/md2json.py content.md slides.json
```

The script outputs:
- `slides.json` — ready for `edit_slides.py`
- Duplication commands — `add_slide.py` commands to run during structural edits
- Deletion info — unused section pairs to remove if fewer than 4 sections

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
python -m markitdown $FILENAME
```

Check for placeholder text still present:

```bash
python -m markitdown $FILENAME | grep -iE "Main Title|Section Title|Subtitle|xxxx|lorem"
```

If grep returns results, replace them before declaring success.

### Visual QA

Convert to images and inspect:

```bash
python .agents/skills/adata-pptx/scripts/office/soffice.py --headless --convert-to pdf $FILENAME
pdftoppm -jpeg -r 150 output.pdf slide
```

**⚠️ USE SUBAGENTS** for visual inspection. Prompt:

```
Visually inspect these ADATA presentation slides. Assume there are issues — find them.

ADATA-specific checks:
- Section accent colors match between divider and content slides
- Arial Black used for titles (check font rendering)
- Dark backgrounds on cover/dividers, appropriate backgrounds on content slides
- Section numbering/color scheme is consistent

General checks:
- Overlapping elements or text overflow
- Placeholder text still present (e.g., "Main Title", "Section Title", "Subtitle")
- Insufficient margin from slide edges (< 0.5")
- Low-contrast text
- Uneven spacing between content blocks

For each slide, list issues or areas of concern, even if minor.
```

### Verification Loop

1. Generate → convert to images → inspect
2. List all issues (if none found, look harder)
3. Fix → re-inspect affected slides
4. Repeat until clean pass

---

## Converting to Images

```bash
python .agents/skills/adata-pptx/scripts/office/soffice.py --headless --convert-to pdf $FILENAME
pdftoppm -jpeg -r 150 output.pdf slide
```

---

## CJK / Codec Pitfalls

The ADATA template was authored in zh-TW PowerPoint. Two files contain Chinese metadata that **will cause errors** on systems using cp950 or other non-UTF-8 default encodings.

> **These fixes are applied automatically by `unpack.py`** when unpacking any `.pptx` file. No manual intervention needed.

### 1. `docProps/app.xml` — cp950 codec error

`pack.py` validates XML files by decoding them with the system default codec. Chinese strings in `app.xml` (e.g. `寬螢幕`, `使用字型`, `佈景主題`, `投影片標題`, `PowerPoint 簡報`) can fail with:

```
'cp950' codec can't decode byte 0x9e in position 366: illegal multibyte sequence
```

`unpack.py` replaces these with ASCII equivalents (`Widescreen`, `Fonts Used`, `Theme`, `Slide Titles`, `PowerPoint Presentation`, `Office Theme`) automatically.

The `<Slides>` count is **automatically updated** by `edit_slides.py` — no manual step needed.

### 2. `[Content_Types].xml` — template content type

Because the template is a `.potx`, the content type is `presentationml.template.main+xml`. This causes `markitdown` (and some PPTX readers) to reject the output `.pptx` file.

`unpack.py` converts this to `presentationml.presentation.main+xml` automatically.

### 3. Chinese text in slide XML

When inserting Chinese characters into slide XML, use **XML numeric character references** (`&#x4E2D;` for 中) to avoid encoding issues entirely. The XML declaration is `encoding="utf-8"`, so literal UTF-8 also works — but entity encoding is safer when building XML strings in Python.

---

## PowerShell Inline Python Pitfall

When running Python code inline with `python -c "..."` in PowerShell, **regex patterns containing backslash sequences** (`\d+`, `\s+`, etc.) will be misinterpreted by the shell. PowerShell strips or reinterprets `\d`, `\s`, etc. before Python sees them.

**Symptom:** `CommandNotFoundException` errors like `\d+ : 無法辨識 '\d+' 詞彙`.

**Fix:** Always write a temporary `.py` script file and run it with `python script.py` instead of using `python -c` for any code containing regex patterns.

---

## Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `pip install Pillow` — thumbnail grids + image pre-compression
- `pip install pandas` — bulk generation from CSV / Excel
- `pip install openpyxl` — Excel `.xlsx` support for bulk generation
- LibreOffice (`soffice`) — PDF conversion (via `.agents/skills/adata-pptx/scripts/office/soffice.py`)
- Poppler (`pdftoppm`) — PDF to images

> For general python-pptx techniques (advanced chart formatting, SmartArt, animations), refer to the `pptx` skill. All such techniques must be applied through the ADATA template with ADATA brand colors and layouts.
