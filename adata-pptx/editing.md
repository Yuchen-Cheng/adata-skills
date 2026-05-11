# Editing ADATA Presentations

This file covers the **template-based workflow** for building a new ADATA deck from scratch.
For converting an existing PPTX, see [SKILL.md](SKILL.md) § "Convert an Existing PPTX".

---

## Workflow Overview

```
content.md → md2json.py → slides.json
                              ↓
            unpack template → add_slide → edit_slides (+ auto-reorder) → clean → pack → output.pptx
```

1. Write `content.md` (single source of truth for slide content)
2. `python scripts/md2json.py content.md slides.json`
3. `python scripts/office/unpack.py adata-template.pptx unpacked/`
4. Run `add_slide.py` commands (printed by md2json)
5. `python scripts/edit_slides.py unpacked/ slides.json "<FILENAME>.pptx"` — also auto-reorders slides and removes unused section pairs
6. `python scripts/clean.py unpacked/`
7. `python scripts/office/pack.py unpacked/ "<FILENAME>.pptx" --original adata-template.pptx`
8. Cleanup: `Remove-Item -Recurse -Force unpacked, slides.json, content.md -ErrorAction SilentlyContinue`

**Sections:** Unlimited. The template has 4 built-in section pairs; additional sections are duplicated automatically with cycling accent colours (Blue → Green → Orange → Magenta → Blue → …).

---

## Step 1 — Write `content.md`

This Markdown file is parsed by `md2json.py`.

### Format

```markdown
---
title:
  - Line 1
  - Line 2
subtitle: Subtitle text
date: 2026/04/29          # optional — defaults to today
---

## Section Title
- Subtopic A
- Subtopic B

### Slide Title
> Slide subtitle

- Bullet item (level 0)
  - Sub-bullet (level 1)
    - Sub-sub-bullet (level 2)
  Plain indented text (level 1, no bullet)

### Another Slide
> Another subtitle

1. Numbered item (level 0)
  1. Nested numbered (level 1)

### Flowchart Slide
> Process Overview

```flowchart TB
oval:n1:開始
rect:n2:處理資料
diamond:n3:成功?
rect:n4:輸出結果
oval:n5:結束
n1->n2
n2->n3
n3->n4:Yes
n3->n2:No
n4->n5
```

### Table Slide
> Feature Comparison

| 功能     | ADATA      | Brand A    |
|---------|------------|------------|
| 讀取速度 | 7,400 MB/s | 5,000 MB/s |
| 保固年限 | 5 年       | 3 年       |
```

### Rules

| Syntax | Mapped to |
|--------|----------|
| `## Heading` | Section divider slide |
| `- item` after `##` | Divider subtitles (max 3) |
| `### Heading` | Content slide |
| `> text` after `###` | Content slide subtitle |
| `- item` | Bullet body item (`<a:buChar>`) |
| `1. item` | Numbered body item (`<a:buAutoNum>`) |
| Plain text | Plain paragraph (no bullet) |
| ` ```flowchart TB` … ` ``` ` | **Flowchart** using native PPT shapes + arrows |
| `\| col \| col \|` pipe table | **Native PPT table** with dark-navy header |

### Indentation (nesting)

Indent with **2 spaces** per level:

```markdown
- Level 0                    → level: 0
  - Level 1                  → level: 1
    - Level 2                → level: 2
  1. Level 1 numbered        → level: 1
    Plain text at level 2    → level: 2
```

Max recommended depth: **3 levels** (0, 1, 2). Deeper nesting is supported but may crowd the slide.

## Step 2 — Convert to JSON

```powershell
python scripts/md2json.py content.md slides.json
```

The script:
- Generates `slides.json`
- Prints required `add_slide.py` duplication commands
- Reports which unused section pairs to delete

## Step 3 — Unpack the Template

```powershell
python scripts/office/unpack.py adata-template.pptx unpacked/
```

`unpack.py` automatically:
- Sanitizes zh-TW metadata in `docProps/app.xml`
- Converts `.potx` content-type to `.pptx`

## Step 4 — Structural Edits

Run the `add_slide.py` commands printed by `md2json.py`. These duplicate both content slides (for multi-slide sections) and, for sections beyond 4, divider + content pairs.

```powershell
python scripts/add_slide.py unpacked/ slide4.xml
```

`add_slide.py` auto-inserts `<p:sldId>` into `presentation.xml`. Run once per needed duplicate.

## Step 5 — Edit Content

```powershell
python scripts/edit_slides.py unpacked/ slides.json "<FILENAME>.pptx"
```

- Cover date defaults to **today** if `"date"` is omitted
- Body items use `<a:buChar>` for bullets, `<a:buAutoNum>` for numbered lists
- Indent level (`"level"` in JSON) maps to `<a:pPr lvl="N">` with progressive margins
- `edit_slides.py` **auto-reorders** slides using `slide_order` from `slides.json`
- Unused template section pairs are automatically removed from `presentation.xml`
- `edit_slides.py` auto-updates `<Slides>N</Slides>` in `docProps/app.xml`

## Steps 6–7 — Clean and Pack

```powershell
python scripts/clean.py unpacked/
python scripts/office/pack.py unpacked/ "<FILENAME>.pptx" --original adata-template.pptx
```

---

## `slides.json` Format

```json
{
  "cover": {
    "title_lines": ["Line 1", "Line 2"],
    "subtitle": "Your subtitle",
    "date": "2026 / 04 / 29"
  },
  "agenda": {
    "items": ["Section 1 Title", "Section 2 Title", "Section 3 Title"]
  },
  "dividers": {
    "slide3.xml": {
      "title": "Section Title",
      "subtitles": ["Topic A", "Topic B", "Topic C"]
****    }
  },
  "contents": {
    "slide4.xml": {
      "title": "Slide Title",
      "subtitle": "Category",
      "body": [
        {"type": "bullet", "text": "Top-level bullet"},
        {"type": "bullet", "text": "Sub-bullet", "level": 1},
        {"type": "bullet", "text": "Sub-sub-bullet", "level": 2},
        {"type": "number", "text": "Numbered item"},
        {"type": "number", "text": "Nested numbered", "level": 1},
        {"type": "plain",  "text": "Plain paragraph"}
      ]
    }
  }
}
```

**Rules:**
- `title_lines`: each entry becomes a line (joined by `<a:br/>`)
- `date`: optional — defaults to today (`YYYY / MM / DD`)
- `body` items: `{"type": "bullet|number|plain", "text": "...", "level": N}`
  - `"level"`: indent depth (0 = top, 1 = sub, 2 = sub-sub). Defaults to 0 if omitted.
  - `"bullet"` → `<a:buChar char="•"/>`, `"number"` → `<a:buAutoNum>`, `"plain"` → no bullet
- Legacy string format also accepted (`"Line 1\nLine 2"` → each line becomes a level-0 bullet)
### Flowchart slide JSON

Omit `"body"` and add `"flowchart"` instead:

```json
"slide4.xml": {
  "title": "Process Flow",
  "subtitle": "System Overview",
  "flowchart": {
    "direction": "TB",
    "nodes": [
      {"id": "n1", "shape": "oval",    "text": "Start"},
      {"id": "n2", "shape": "rect",    "text": "Process A"},
      {"id": "n3", "shape": "diamond", "text": "Decision?"},
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

`direction`: `"TB"` (top→bottom, default) or `"LR"` (left→right).  
Supported `shape` values: `oval` · `rect` · `diamond` · `para` · `doc` · `db`.  
Optional keys: `fill_color`, `line_color`, `text_color` (all hex strings).

### Table slide JSON

Omit `"body"` and add `"table"` instead:

```json
"slide6.xml": {
  "title": "Comparison",
  "subtitle": "",
  "table": {
    "header": ["Feature", "ADATA", "Competitor"],
    "rows": [
      ["Read Speed",  "7,400 MB/s", "5,000 MB/s"],
      ["Write Speed", "6,900 MB/s", "4,200 MB/s"],
      ["Warranty",    "5 years",    "3 years"]
    ]
  }
}
```

Optional key: `header_fill` (hex, default `0E2841` dark navy).  
Columns are auto-sized equally across the slide width.  
Header row: dark-navy fill, white bold text.  
Data rows: alternating white / light-gray, navy text.
---

## XML Editing Reference

### Placeholder types by slide

| Slide type | PH type / idx | Content | Font |
|---|---|---|---|
| Cover | `ctrTitle` / idx 0 | Title | Arial Black 66pt |
| Cover | idx 10 | Subtitle | 32pt |
| Cover | idx 11 | Date | 16pt |
| Section Divider | `title` / idx 0 | Section title | Arial Black 66pt |
| Section Divider | idx 10 | Subtitles | 28pt |
| Content | `title` / idx 0 | Main title | Arial Black 55pt (section accent colour) |
| Content | idx 1 | Subtitle | 30pt |
| Content | idx 2 | Body | 24pt |

### Formatting rules

- Set `lang="zh-TW"` on Chinese text, `lang="en-US"` on English
- Bold labels with `b="1"` on `<a:rPr>`
- Never use unicode bullets (`•`) — use `<a:buChar>` or `<a:buAutoNum>`
- Preserve font sizes from `<a:lstStyle>` — only override in `<a:rPr>` when necessary

### Smart quotes in Chinese text

| Character | XML Entity |
|-----------|-----------|
| `"` (left) | `&#x201C;` |
| `"` (right) | `&#x201D;` |
| `「` (CJK left) | `&#x300C;` |
| `」` (CJK right) | `&#x300D;` |

---

## Section Color Reference

| Section | Slides | Hex | XML |
|---------|--------|-----|-----|
| 1 | 3–4 | `#5097FF` | `<a:srgbClr val="5097FF"/>` |
| 2 | 5–6 | `#19C711` | `<a:srgbClr val="19C711"/>` |
| 3 | 7–8 | `#FF9000` | `<a:srgbClr val="FF9000"/>` |
| 4 | 9–10 | `#FF47FF` | `<a:srgbClr val="FF47FF"/>` |

Theme references: `<a:schemeClr val="accent1"/>` through `accent4`.

> When duplicating a content slide for a different section, update the `<a:srgbClr val="..."/>` in the title's `<a:lstStyle>` to match the target section.

---

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Duplicated slide has wrong accent colour | Update `<a:srgbClr>` in title `<a:lstStyle>` |
| Agenda items out of sync | Update agenda slide to match actual section titles |
| Multi-item bullets in one `<a:t>` | Use separate `<a:p>` elements per item |
| PowerShell inline Python regex breaks | Write a `.py` file instead of `python -c` |
