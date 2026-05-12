---
name: adata-pptx
description: "Create ADATA (威剛科技) branded PowerPoint presentations. Use this skill whenever the user wants to make a presentation, slides, or deck in ADATA style, or asks to generate a 威剛 / ADATA branded .pptx file.  Always use this skill for any ADATA or 威剛 presentation request, even if the user just says 'make a deck' or 'make slides' in the context of ADATA work."
---

# ADATA Presentation Skill

Produces `.pptx` files that follow the official ADATA (威剛科技) design system. All slides use background images from `assets/backgrounds/` combined with typography and colour rules from the ADATA template.

This skill is fully self-contained:
- **`layouts/slides/`** — 5 structural slide layouts (cover, agenda, section divider, content, end); **read the relevant file before writing any slide code**
- **`layouts/patterns/`** — body content patterns (see the folder for the full list; new patterns may be added over time); read all pattern files before choosing a body layout
- **`assets/backgrounds/`** — 11 ADATA background JPGs (one per layout)
- **`references/template-styles.md`** — detailed placeholder specs; read this when you need pixel-level precision or want to verify colour values
- **`scripts/`** — pptx utility scripts (thumbnail, unpack, pack, add_slide, clean)

---

## ⚠ MANDATORY: Read These Files Before Writing Any Code

**Do this immediately upon loading this skill — before planning, before writing code.**

Read ALL of the following files using `read_file`:

### Slide layout files (read all 5):
- `layouts/slides/01-cover.md`
- `layouts/slides/02-agenda.md`
- `layouts/slides/03-section-divider.md`
- `layouts/slides/04-content-standard.md`
- `layouts/slides/05-end.md`

### Pattern files (read ALL `.md` files in `layouts/patterns/`):

Use `list_dir` on `layouts/patterns/` to get the current file list, then `read_file` on every file found. New patterns may have been added — do not assume the list is fixed.

> The inline boilerplate in this file is for orientation only. The layout and pattern files contain the **authoritative coordinates, ADATA overrides, and ready-to-use pptxgenjs code**. Do not write a single slide without reading the corresponding file first.

---

## Quick Workflow

0. **Read ALL layout and pattern files** — use `read_file` on every file listed in the "MANDATORY" section above before doing anything else
1. **Gather requirements** — topic, sections, number of slides, language
2. **Plan slide structure** — map each section to an ADATA layout; assign a body pattern (from `layouts/patterns/`) to every content slide
3. **Write `generate.js`** — copy the pptxgenjs code **from the layout/pattern files you just read**; do not invent coordinates
4. **Run the script** — `node generate.js` (from the workspace root)
5. **QA** — convert to images and inspect visually

---

## ADATA Slide Library

The template provides 11 background images. Choose the correct one for each slide.

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

## ADATA Design System

### Colour Palette

| Role | Hex | Usage |
|------|-----|-------|
| Deep Navy | `#0E2841` | All dark backgrounds, top bar on content slides |
| White | `#FFFFFF` | All text on dark-background slides |
| Section 1 — Blue | `#5097FF` | Cover/section divider accent; content slide titles & subtitle |
| Section 2 — Green | `#19C711` | Cover/section divider accent; content slide titles & subtitle |
| Section 3 — Orange | `#FF9000` | Cover/section divider accent; content slide titles & subtitle |
| Section 4 — Magenta | `#FF47FF` | Cover/section divider accent; content slide titles & subtitle |
| Body text on light slides | `#0E2841` | Body copy on white-background content slides |

### Typography

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

## Layout Library

Layouts are split into two subfolders. **Before writing any slide code, read the relevant file.**

### `layouts/patterns/` — Body Content Patterns

Use these **inside** the body area of a content slide instead of plain bullet lists.

| Pattern | When to use |
|---------|-------------|
| **A — Section Tag Header** | Compact header; frees up extra body height |
| **B — Stat Cards (4 across)** | Showing 3–4 key metrics side by side |
| **C — Proportional Category Bar** | Visualising distribution across categories |
| **D — Unit / Department Grid (2×3)** | Comparing multiple teams or items with counts |
| **E — Table Layout** | Structured task/action tables with 3–4 columns |
| **F — Bottom Note Band** | Update notes, caveats, or risk callouts at bottom |

> **Additional patterns may exist.** Always use `list_dir` on `layouts/patterns/` to get the current full list before planning. The table above shows the baseline set only.

---

## Step-by-Step Generation

### 0 · Read ALL Layout and Pattern Files  ← **Do this before anything else**

1. Use `list_dir` on `layouts/patterns/` to get the current pattern file list.
2. Use `read_file` on all 5 slide layout files and every pattern file found.

Only after reading all files may you proceed to Step 1.

### 1 · Plan

Before writing code, produce a slide plan. For **every content slide** assign a body pattern:

```
Slide 1  — Cover          — [Presentation title] / [Subtitle] / [Date]
Slide 2  — Agenda         — [List of section names]
Slide 3  — §1 Divider     — [Section 1 name]
Slide 4  — §1 Content     — [Slide title] | Pattern: B (Stat Cards)
Slide 5  — §1 Content     — [Slide title] | Pattern: E (Table)
…
Slide N  — End            — Thank you / Q&A
```

Rules for pattern assignment:
- **Every content slide must use a named pattern from `layouts/patterns/`.** Plain bullet lists are a last resort and only acceptable when the content is a sequential list that genuinely cannot be expressed with any pattern.
- **The same pattern may be reused on multiple slides** — there is no variety requirement. Choose whichever pattern best fits the content, even if it repeats.
- **Never assign plain bullets to two or more consecutive content slides.**
- Choose the pattern whose "When to use" description best matches the slide content. When in doubt, prefer stat cards, unit grid, or table patterns, as they fit the widest range of business content.
- Maximise pattern coverage: aim for patterns on every content slide in the deck.

Share the plan with the user and confirm before writing any code.

### 2 · Resolve Background Paths

The background images live in the `backgrounds/` folder inside this skill. When writing the generation script, resolve the path relative to the skill directory. Do **not** hard-code absolute paths.

```javascript
const path = require('path');
// Skill root: .agents/skills/adata-pptx/
// Place generate.js in the skill root so this resolves correctly:
const BG = path.join(__dirname, 'assets', 'backgrounds');
```

If the user's output script is placed elsewhere (e.g. in the workspace root), adjust accordingly:
```javascript
const SKILL_DIR = path.join(__dirname, '.agents', 'skills', 'adata-pptx');
const BG = path.join(SKILL_DIR, 'assets', 'backgrounds');
```

### 3 · pptxgenjs Boilerplate

```javascript
const pptxgen = require("pptxgenjs");
const path = require("path");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625"
```

### 4 · Helper — addBackground

Add this helper at the top of the script so every slide gets its background image easily:

```javascript
function addBackground(slide, bgFile) {
  slide.addImage({
    path: path.join(BG, bgFile),
    x: 0, y: 0, w: "100%", h: "100%",
    sizing: { type: "cover", w: "100%", h: "100%" }
  });
}
```

### 5 · Save

```javascript
pres.writeFile({ fileName: "ADATA_Presentation.pptx" });
```

### 7 · Install & Run

`generate.js` is written by Claude into the **workspace root** (next to `package.json` if one exists, otherwise in the project directory the user specifies). Run from that directory:

```bash
npm install pptxgenjs   # only needed once
node generate.js
```

The output `ADATA_Presentation.pptx` is saved in the same directory as `generate.js`.

---

## Section Colour Reference (quick copy)

```javascript
const SECTION_COLORS = {
  1: { accent: "5097FF", bg_divider: "slide03_section_divider_blue.jpg",    bg_content: "slide04_content_blue.jpg" },
  2: { accent: "19C711", bg_divider: "slide05_section_divider_green.jpg",   bg_content: "slide06_content_green.jpg" },
  3: { accent: "FF9000", bg_divider: "slide07_section_divider_orange.jpg",  bg_content: "slide08_content_orange.jpg" },
  4: { accent: "FF47FF", bg_divider: "slide09_section_divider_magenta.jpg", bg_content: "slide10_content_magenta.jpg" },
};
// For section N > 4, use: SECTION_COLORS[((N - 1) % 4) + 1]
```

---

## Design Rules (non-negotiable)

- **Background images are mandatory** on every slide — never leave a slide with a plain white or navy background.
- **Keep text in the safe zone**: on cover and section divider slides, the right ~40% is occupied by ADATA's geometric graphic. Keep all text within the left 55–60% of the slide width.
- **Do not invent colours** — use only the palette defined above.
- **Do not change fonts** — Arial Black for headings, Arial for body. No substitutions.
- **Never use unicode bullet characters** (•, ◆, etc.) — use pptxgenjs `bullet: true`.
- **Bold all titles** — set `bold: true` on every title and section heading text box.
- **Agenda slide**: list section names as a bulleted or numbered list, one per line, 28pt Arial white.
- **Maximise pattern usage**: **every content slide must use a named pattern from `layouts/patterns/`.** Re-read the assigned pattern file before writing each content slide and copy the pptxgenjs code from that file. The same pattern may appear on multiple slides — reuse is encouraged. Plain bullet lists are only acceptable when the content is genuinely a sequential list that cannot fit any available pattern, and such exceptions must be rare (no more than one per deck).

---

## QA

After generating the file, convert slides to images and inspect:

```bash
# LibreOffice (cross-platform)
soffice --headless --convert-to png ADATA_Presentation.pptx

# Thumbnail script bundled in this skill
python .agents/skills/adata-pptx/scripts/thumbnail.py ADATA_Presentation.pptx

# For detailed QA (full resolution), use LibreOffice:
soffice --headless --convert-to png ADATA_Presentation.pptx
```

Check each slide for:
- Background image fully covers the slide
- Text is not cut off or overflowing the safe zone (left 55% on dark slides)
- Correct section accent colour on every content slide title
- No leftover placeholder or lorem-ipsum text
- Agenda lists all sections
- Section colour cycling is consistent throughout

---

## Bundled Resources

| Resource | Purpose | When to use |
|---------|---------|-------------|
| `assets/backgrounds/` | 11 ADATA background JPGs | Required for every slide |
| `layouts/slides/` | 5 structural slide layouts (cover, agenda, divider, content, end) | Writing any slide |
| `layouts/patterns/` | Body content patterns (use `list_dir` to get current full list) | Choosing body layout for content |
| `references/template-styles.md` | Placeholder specs & colour tables | Pixel-level precision |
| `references/pptxgenjs.md` | pptxgenjs full API reference | Shapes, charts, images, advanced text |
| `references/editing.md` | Unpack/edit XML/pack workflow | Editing existing .pptx files |
| `scripts/` | Python utility scripts (thumbnail, unpack, pack, add_slide, clean) | QA & PPTX manipulation |

For general pptxgenjs API (shapes, charts, image embedding), see [references/pptxgenjs.md](references/pptxgenjs.md). For editing an existing ADATA `.pptx` file via XML, see [references/editing.md](references/editing.md).
