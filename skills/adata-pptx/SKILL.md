---
name: adata-pptx
description: >
  Create branded PowerPoint presentations from a selectable template library with reusable content patterns. ADATA template built-in; extensible architecture to add custom templates and patterns. Use this skill whenever the user wants to make a presentation, slides, or deck — or asks to generate a .pptx file. Always use this skill for any presentation request, even if the user just says 'make a deck' or 'make slides'. See references/Add_template.md and references/Add_pattern.md to extend with new templates or patterns.
---

# Universal Presentation Skill

Produces `.pptx` files using background images, colour palettes, and typography rules defined by the **selected template**. Templates live in `layouts/template/`; each template describes its own assets folder, colour system, and design rules.

This skill is fully self-contained:
- **`layouts/template/`** — one `.md` file per available template (e.g. `adata.md`); contains background library, colours, typography, all slide layout details (placeholders, coordinates, pptxgenjs code), and design rules; read the selected template before writing any code
- **`layouts/patterns/`** — body content patterns; read all pattern files before choosing a body layout
- **`assets/`** — background images grouped by template sub-folder (e.g. `assets/adata_backgrounds/`)
- **`scripts/`** — pptx utility scripts (thumbnail, unpack, pack, add_slide, clean)

---

## ⚠ MANDATORY STEP 0: Ask the User Which Template to Use

**Before doing anything else — before reading files, before planning — follow these steps in order:**

1. Run `node .agents/skills/adata-pptx/scripts/list-templates.js` in the terminal to get the current list of available templates.
2. Parse the output to extract each template's **ID** and **name**.
3. Build the `options` array dynamically from that output — one option per template found.
4. Always append a final option: `label: "Other / Custom"`, `description: "I will provide my own template or describe the style I want"`.
5. Use the `vscode_askQuestions` tool with the dynamically built options:

```
Use vscode_askQuestions with:
  header: "Presentation Template"
  question: "Which presentation template would you like to use for this deck?"
  options: <dynamically built from list-templates.js output>
```

> **Never hardcode template names or options.** Always run `list-templates.js` first so newly added templates are always included.

After the user selects a template, proceed with Step 1 below.

---

## ⚠ MANDATORY: Read These Files Before Writing Any Code

Once the template is selected, **read all of the following before planning or writing code.**

### 1. Template file
Run `node scripts/list-templates.js` to see available templates and their details. Then `read_file` on the selected template's `.md` file . The template file is the **single authoritative source** for all slide layout details (Layouts 01–05), including background file names, placeholder coordinates, colours, fonts, and ready-to-use pptxgenjs code.

### 2. Pattern files (all files in `layouts/patterns/`):
Run `node scripts/list-patterns.js` to see all available patterns and their purposes. Then `read_file` on every pattern file found. New patterns may have been added — do not assume the list is fixed.

> The inline reference material in this file is for orientation only. The **template file** (`layouts/template/<name>.md`) is the single authoritative source for all slide layout details — coordinates, colour overrides, background file names, and ready-to-use pptxgenjs code. Do not write slide code without reading the template file first.

---

## Quick Workflow

0. **Ask the user which template to use** — via `vscode_askQuestions` (see Step 0 above)
1. **List and read template and pattern files** — Run `node scripts/list-templates.js` to see available templates, then `read_file` on the selected template `.md` (background library, colours, typography, all 5 slide layout details). Run `node scripts/list-patterns.js` to see all patterns, then `read_file` on every pattern file found in `layouts/patterns/`
2. **Gather requirements** — topic, sections, number of slides, language
3. **Plan slide structure** — map each section to a layout; assign a body pattern (from `layouts/patterns/`) to every content slide; share the plan with the user and confirm before writing code
4. **Write `generate.js`** — copy the pptxgenjs code **from the layout/pattern files you just read**; do not invent coordinates or colours
5. **Run the script** — `node generate.js` (from the workspace root)
6. **QA** — convert to images and inspect visually

---

## Available Templates

Run the following command to list all available templates:

```bash
node scripts/list-templates.js
```

This script displays all templates with their IDs, names, and background image counts. New templates may be added — always run the script to see the current list.

> **Each template's `.md` file defines:** background folder, background image library, colour palette, typography, section colour cycling, background path (JavaScript), and design rules. Always read the file — do not rely on the list alone.

---

## Template-Agnostic Design Principles

These rules apply regardless of which template is selected:

- **Background images are mandatory** on every slide — never use a plain white or default background.
- **Respect the safe zone** — every template defines areas where text must not be placed; check the template file.
- **Use only the palette from the template** — do not invent colours.
- **Use only the fonts from the template** — do not substitute.
- **Never use unicode bullet characters** (•, ◆, etc.) — use pptxgenjs `bullet: true`.
- **Bold all titles** as specified by the template.
- **Every content slide must use a named pattern from `layouts/patterns/`** — plain bullet lists are a last resort (no more than one per deck).

---

## Step-by-Step Generation

### 0 · Ask Which Template  ← **Do this first, before anything else**

1. Run `node .agents/skills/adata-pptx/scripts/list-templates.js` to get the live template list.
2. Build `vscode_askQuestions` options dynamically from the output (plus an "Other / Custom" fallback).
3. Present the question — see "MANDATORY STEP 0" above for the full procedure.

### 1 · List and Read All Files

1. Run `node scripts/list-templates.js` → `read_file` on the selected template `.md` (contains background library, colours, typography, JS path, design rules, **and** all 5 slide layout details).
2. Run `node scripts/list-patterns.js` → `read_file` on every pattern file found in `layouts/patterns/`.

### 2 · Plan

Before writing code, produce a slide plan. For **every content slide** assign a body pattern:

```
Slide 1  — Cover          — [Presentation title] / [Subtitle] / [Date]
Slide 2  — Agenda         — [List of section names]
Slide 3  — §1 Divider     — [Section 1 name]
Slide 4  — §1 Content     — [Slide title] | Pattern: Stat Cards
Slide 5  — §1 Content     — [Slide title] | Pattern: Table Layout
…
Slide N  — End            — Thank you / Q&A
```

Rules for pattern assignment:
- **Every content slide must use a named pattern.** Plain bullet lists are only acceptable when the content is a sequential list that genuinely cannot be expressed with any pattern.
- **The same pattern may be reused** — no variety requirement. Choose whichever pattern best fits.
- **Never assign plain bullets to two or more consecutive content slides.**
- Maximise pattern coverage: aim for patterns on every content slide in the deck.

Share the plan with the user and confirm before writing any code.

### 3 · Resolve Background Paths

The template file specifies the background folder. Resolve paths relative to the skill directory:

```javascript
const path = require('path');
// When generate.js is in the workspace root:
const SKILL_DIR = path.join(__dirname, '.agents', 'skills', 'adata-pptx');
// BG path comes from the template definition — e.g. for ADATA:
const BG = path.join(SKILL_DIR, 'assets', 'adata_backgrounds');
```

### 4 · pptxgenjs Boilerplate

```javascript
const pptxgen = require("pptxgenjs");
const path = require("path");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625"
```

### 5 · Helper — addBackground

```javascript
function addBackground(slide, bgFile) {
  slide.addImage({
    path: path.join(BG, bgFile),
    x: 0, y: 0, w: "100%", h: "100%",
    sizing: { type: "cover", w: "100%", h: "100%" }
  });
}
```

### 6 · Output Filename — Derive from Content

**Never hardcode the output filename.** Generate it dynamically from the presentation content:

```javascript
// Rules for filename generation:
// 1. Start with the template ID (e.g. "ADATA").
// 2. Append a short slug derived from the presentation topic/title
//    (2–5 words, spaces replaced with underscores, special chars removed).
// 3. Append the current date in YYYYMMDD format.
// 4. Extension: .pptx
//
// Examples:
//   ADATA_AI_Agent_Report_20260513.pptx
//   ADATA_Finance_Roadmap_20260513.pptx
//   ADATA_CS_Agent_20260513.pptx

const today = new Date();
const dateStr = today.getFullYear().toString() +
  String(today.getMonth() + 1).padStart(2, '0') +
  String(today.getDate()).padStart(2, '0');

// Replace TEMPLATE_ID and TOPIC_SLUG with values derived from the presentation content:
const fileName = `TEMPLATE_ID_TOPIC_SLUG_${dateStr}.pptx`;

pres.writeFile({ fileName });
```

> `TEMPLATE_ID` = the template's ID string from `list-templates.js` output (e.g. `ADATA`).
> `TOPIC_SLUG` = 2–5 keywords from the presentation title, underscored (e.g. `AI_Agent_Report`).

```bash
npm install pptxgenjs   # only needed once
node generate.js
```

---

## QA

After generating the file, convert slides to images and inspect:

```bash
# LibreOffice (cross-platform)
soffice --headless --convert-to png Presentation.pptx

# Thumbnail script bundled in this skill
python .agents/skills/adata-pptx/scripts/thumbnail.py Presentation.pptx
```

Check each slide for:
- Background image fully covers the slide
- Text is not cut off or overflowing the safe zone
- Correct accent colour on every content slide title (per template)
- No leftover placeholder or lorem-ipsum text
- Agenda lists all sections
- Section colour cycling is consistent (if applicable)

---

## Bundled Resources

| Resource | Purpose | Command / Location |
|---------|---------|-------------|
| `scripts/list-templates.js` | List all available templates with metadata | Run: `node scripts/list-templates.js` |
| `layouts/template/` | Template definitions — backgrounds, colours, typography, all slide layout details | Read after selecting template |
| `assets/<template>_backgrounds/` | Background images per template | Required for every slide |
| `scripts/list-patterns.js` | List all available body content patterns | Run: `node scripts/list-patterns.js` |
| `layouts/patterns/` | Body content patterns with detailed specifications | Read all files after listing patterns |
| `references/Add_template.md` | Guide to creating new templates | When adding a new template |
| `references/Add_pattern.md` | Guide to creating new patterns | When adding a new pattern |
| `references/pptxgenjs.md` | pptxgenjs full API reference | Shapes, charts, images, advanced text |
| `references/editing.md` | Unpack/edit XML/pack workflow | Editing existing .pptx files |
