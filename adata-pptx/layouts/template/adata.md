# Template: ADATA (威剛科技)

**Template ID:** `adata`  
**Background folder:** `assets/adata_backgrounds/`  
**Background count:** 11

---

## Background Image Library

| Slide # | File | Layout Role | When to use |
|---------|------|-------------|-------------|
| 1 | `slide01_cover.jpg` | **Cover** | First slide — title, subtitle, date |
| 2 | `slide02_agenda.jpg` | **Agenda** | Table of contents / outline |
| 3 | `slide03_section_divider_blue.jpg` | **Section Divider — Blue (§1)** | Opening slide for Section 1 |
| 4 | `slide04_content_blue.jpg` | **Content — Blue (§1)** | Content slides in Section 1 |
| 5 | `slide05_section_divider_green.jpg` | **Section Divider — Green (§2)** | Opening slide for Section 2 |
| 6 | `slide06_content_green.jpg` | **Content — Green (§2)** | Content slides in Section 2 |
| 7 | `slide07_section_divider_orange.jpg` | **Section Divider — Orange (§3)** | Opening slide for Section 3 |
| 8 | `slide08_content_orange.jpg` | **Content — Orange (§3)** | Content slides in Section 3 |
| 9 | `slide09_section_divider_magenta.jpg` | **Section Divider — Magenta (§4)** | Opening slide for Section 4 |
| 10 | `slide10_content_magenta.jpg` | **Content — Magenta (§4)** | Content slides in Section 4 |
| 11 | `slide11_blank.jpg` | **End / Blank** | Closing / thank-you slide |

**Section colour cycling**: if there are more than 4 sections, cycle back through blue → green → orange → magenta.

---

## Colour Palette

| Role | Hex | Usage |
|------|-----|-------|
| Deep Navy | `#0E2841` | All dark backgrounds, top bar on content slides |
| White | `#FFFFFF` | All text on dark-background slides |
| Section 1 — Blue | `#5097FF` | Cover/section divider accent; content slide titles & subtitle |
| Section 2 — Green | `#19C711` | Cover/section divider accent; content slide titles & subtitle |
| Section 3 — Orange | `#FF9000` | Cover/section divider accent; content slide titles & subtitle |
| Section 4 — Magenta | `#FF47FF` | Cover/section divider accent; content slide titles & subtitle |
| Body text on light slides | `#0E2841` | Body copy on white-background content slides |

---

## Typography

| Element | Font | Size | Colour |
|---------|------|------|--------|
| Cover main title | Arial Black (bold) | 66 pt | `#FFFFFF` |
| Cover subtitle | Arial | 32 pt | `#FFFFFF` |
| Cover date | Arial | 16 pt | `#FFFFFF` |
| Section divider title | Arial Black (bold) | 66 pt | `#FFFFFF` |
| Section divider subtitle | Arial | 28 pt | `#FFFFFF` |
| Agenda title | Arial Black (bold) | 66 pt | `#FFFFFF` |
| Agenda body | Arial | 28 pt | `#FFFFFF` |
| Content slide title | Arial Black (bold) | 55 pt | Section accent colour |
| Content slide subtitle/category | Arial | 30 pt | Section accent colour |
| Content body lvl 1 | Arial | 24 pt | `#0E2841` |
| Content body lvl 2 | Arial | 20 pt | `#0E2841` |
| Content body lvl 3 | Arial | 18 pt | `#0E2841` |
| Content body lvl 4+ | Arial | 16 pt | `#0E2841` |

---

## Section Colour Reference

```javascript
const SECTION_COLORS = {
  1: { accent: "5097FF", bg_divider: "slide03_section_divider_blue.jpg",    bg_content: "slide04_content_blue.jpg" },
  2: { accent: "19C711", bg_divider: "slide05_section_divider_green.jpg",   bg_content: "slide06_content_green.jpg" },
  3: { accent: "FF9000", bg_divider: "slide07_section_divider_orange.jpg",  bg_content: "slide08_content_orange.jpg" },
  4: { accent: "FF47FF", bg_divider: "slide09_section_divider_magenta.jpg", bg_content: "slide10_content_magenta.jpg" },
};
// For section N > 4: SECTION_COLORS[((N - 1) % 4) + 1]
```

---

## Background Path (JavaScript)

```javascript
const path = require('path');
// When generate.js is in the workspace root:
const SKILL_DIR = path.join(__dirname, '.agents', 'skills', 'adata-pptx');
const BG = path.join(SKILL_DIR, 'assets', 'adata_backgrounds');
```

---

## Design Rules

- **Background images are mandatory** on every slide — never leave a slide with a plain white or navy background.
- **Safe zone**: on cover and section divider slides, the right ~40% is occupied by ADATA's geometric graphic. Keep all text within the left 55–60% of the slide width.
- **Do not invent colours** — use only the palette defined above.
- **Do not change fonts** — Arial Black for headings, Arial for body. No substitutions.
- **Never use unicode bullet characters** (•, ◆, etc.) — use pptxgenjs `bullet: true`.
- **Bold all titles** — set `bold: true` on every title and section heading text box.
- **Agenda slide**: list section names as a bulleted or numbered list, one per line, 28 pt Arial white.
- **Body safe limit**: do not place content below `y = 5.35` on content slides (ADATA branding zone).

---

## Output Filename Convention

Do **not** hardcode the filename. Derive it dynamically from the presentation content:

```
ADATA_<TopicSlug>_<YYYYMMDD>.pptx
```

- `ADATA` — this template's ID (always uppercase)
- `<TopicSlug>` — 2–5 keywords from the presentation title, joined with underscores, no special characters (e.g. `AI_Agent_Report`, `Finance_Roadmap`, `CS_Agent`)
- `<YYYYMMDD>` — generation date

**Examples:**
- `ADATA_AI_Agent_Report_20260513.pptx`
- `ADATA_Finance_Roadmap_20260513.pptx`
- `ADATA_CS_Agent_20260513.pptx`

---

## Slide Layouts (ADATA)

### Layout 01 — Cover Slide

**Background:** `slide01_cover.jpg`  
**When to use:** First slide — title, subtitle, date.

> Safe zone: keep all text within the **left 55%** of the slide (right ~40% is the ADATA geometric graphic).

**Placeholders:**

```
Main title:  x:0.5  y:2.0  w:5.5  h:1.8   Arial Black  66pt  #FFFFFF  bold
Subtitle:    x:0.5  y:3.9  w:5.5  h:0.8   Arial        32pt  #FFFFFF
Date:        x:0.5  y:4.9  w:5.5  h:0.5   Arial        16pt  #FFFFFF
```

**pptxgenjs code:**

```javascript
const cover = pres.addSlide();
addBackground(cover, "slide01_cover.jpg");

cover.addText("Presentation Title", {
  x: 0.5, y: 2.0, w: 5.5, h: 1.8,
  fontFace: "Arial Black", fontSize: 66, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0, wrap: true
});
cover.addText("Subtitle text", {
  x: 0.5, y: 3.9, w: 5.5, h: 0.8,
  fontFace: "Arial", fontSize: 32, color: "FFFFFF",
  valign: "middle", margin: 0
});
cover.addText("May 2026", {
  x: 0.5, y: 4.9, w: 5.5, h: 0.5,
  fontFace: "Arial", fontSize: 16, color: "FFFFFF",
  margin: 0
});
```

---

### Layout 02 — Agenda Slide

**Background:** `slide02_agenda.jpg`  
**When to use:** Table of contents / outline — list all section names.

**Placeholders:**

```
Title:  x:0.5  y:0.4  w:9.0  h:1.2   Arial Black  66pt  #FFFFFF  bold
Body:   x:0.5  y:1.8  w:8.5  h:3.5   Arial        28pt  #FFFFFF
```

**pptxgenjs code:**

```javascript
const agenda = pres.addSlide();
addBackground(agenda, "slide02_agenda.jpg");

agenda.addText("Agenda", {
  x: 0.5, y: 0.4, w: 9.0, h: 1.2,
  fontFace: "Arial Black", fontSize: 66, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0
});
agenda.addText([
  { text: "Section 1 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 2 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 3 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 4 Name", options: { bullet: true } },
], {
  x: 0.5, y: 1.8, w: 8.5, h: 3.5,
  fontFace: "Arial", fontSize: 28, color: "FFFFFF",
  valign: "top", margin: 0
});
```

**Rules:** List section names one per line with `bullet: true` — never unicode bullet characters.

---

### Layout 03 — Section Divider Slide

**Backgrounds (one per section, cycle after §4):**

| Section | Background file |
|---------|----------------|
| §1 | `slide03_section_divider_blue.jpg` |
| §2 | `slide05_section_divider_green.jpg` |
| §3 | `slide07_section_divider_orange.jpg` |
| §4 | `slide09_section_divider_magenta.jpg` |

**When to use:** Opening slide for each section.

> Safe zone: keep all text within the **left 55–60%** of the slide.

**Placeholders:**

```
Section title:    x:0.5  y:2.1  w:6.5  h:1.8   Arial Black  66pt  #FFFFFF  bold
Section subtitle: x:0.5  y:4.0  w:6.5  h:0.9   Arial        28pt  #FFFFFF
```

**pptxgenjs code:**

```javascript
// Replace bgFile with the appropriate section background from SECTION_COLORS
const sec = pres.addSlide();
addBackground(sec, "slide03_section_divider_blue.jpg");

sec.addText("Section Title", {
  x: 0.5, y: 2.1, w: 6.5, h: 1.8,
  fontFace: "Arial Black", fontSize: 66, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0, wrap: true
});
sec.addText("Section subtitle or tagline", {
  x: 0.5, y: 4.0, w: 6.5, h: 0.9,
  fontFace: "Arial", fontSize: 28, color: "FFFFFF",
  valign: "top", margin: 0
});
```

---

### Layout 04 — Standard Content Slide

**Backgrounds (one per section, cycle after §4):**

| Section | Background file | Accent colour |
|---------|----------------|--------------|
| §1 | `slide04_content_blue.jpg` | `#5097FF` |
| §2 | `slide06_content_green.jpg` | `#19C711` |
| §3 | `slide08_content_orange.jpg` | `#FF9000` |
| §4 | `slide10_content_magenta.jpg` | `#FF47FF` |

**When to use:** Any informational slide within a section. Prefer a richer body pattern over plain bullet lists whenever the content warrants it.

**Placeholders:**

```
Title:    x:0.5  y:0.15  w:9.0  h:1.0   Arial Black  55pt  <section-accent>  bold
Subtitle: x:0.5  y:1.2   w:9.0  h:0.6   Arial        30pt  <section-accent>
Body:     x:0.5  y:1.95  w:9.0  h:3.4   Arial        24pt  #0E2841
```

> Body safe limit: do not place content below **y = 5.35** (ADATA branding zone).

**pptxgenjs code (Section 1 — Blue example):**

```javascript
const BLUE = "5097FF";
const NAVY = "0E2841";

const content = pres.addSlide();
addBackground(content, "slide04_content_blue.jpg");

content.addText("Slide Title", {
  x: 0.5, y: 0.15, w: 9.0, h: 1.0,
  fontFace: "Arial Black", fontSize: 55, bold: true, color: BLUE,
  valign: "middle", margin: 0
});
content.addText("Category / Subtitle", {
  x: 0.5, y: 1.2, w: 9.0, h: 0.6,
  fontFace: "Arial", fontSize: 30, color: BLUE,
  valign: "middle", margin: 0
});
content.addText([
  { text: "Key point one", options: { bullet: true, breakLine: true } },
  { text: "Key point two", options: { bullet: true, breakLine: true } },
  { text: "Key point three", options: { bullet: true } },
], {
  x: 0.5, y: 1.95, w: 9.0, h: 3.4,
  fontFace: "Arial", fontSize: 24, color: NAVY,
  valign: "top", margin: 0
});
```

**Body content levels:**

| Level | Font size | Colour |
|-------|-----------|--------|
| lvl 1 | 24 pt | `#0E2841` |
| lvl 2 | 20 pt | `#0E2841` |
| lvl 3 | 18 pt | `#0E2841` |
| lvl 4+ | 16 pt | `#0E2841` |

---

### Layout 05 — End / Blank Slide

**Background:** `slide11_blank.jpg`  
**When to use:** Closing slide — thank-you, Q&A, or simply end the deck.

**Placeholders:** No mandatory placeholders. Optionally add a centred thank-you line.

**Notes** No text needed in this slide.

**pptxgenjs code:**

```javascript
const end = pres.addSlide();
addBackground(end, "slide11_blank.jpg");

```
