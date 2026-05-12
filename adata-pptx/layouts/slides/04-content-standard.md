# Layout 04 — Standard Content Slide

**Backgrounds (one per section, cycle after §4):**

| Section | Background file | Accent colour |
|---------|----------------|--------------|
| §1 | `slide04_content_blue.jpg` | `#5097FF` |
| §2 | `slide06_content_green.jpg` | `#19C711` |
| §3 | `slide08_content_orange.jpg` | `#FF9000` |
| §4 | `slide10_content_magenta.jpg` | `#FF47FF` |

**When to use:** Any informational slide within a section. Prefer a richer body pattern (see layouts 06–11) over plain bullet lists whenever the content warrants it.

## Placeholders

```
Title:    x:0.5  y:0.15  w:9.0  h:1.0   Arial Black  55pt  <section-accent>  bold
Subtitle: x:0.5  y:1.2   w:9.0  h:0.6   Arial        30pt  <section-accent>
Body:     x:0.5  y:1.95  w:9.0  h:3.4   Arial        24pt  #0E2841
```

> Body safe limit: do not place content below **y = 5.35** (ADATA branding zone).

## pptxgenjs Code (Section 1 — Blue example)

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

## Body Content Levels

| Level | Font size | Colour |
|-------|-----------|--------|
| Body lvl 1 | 24 pt | `#0E2841` |
| Body lvl 2 | 20 pt | `#0E2841` |
| Body lvl 3 | 18 pt | `#0E2841` |
| Body lvl 4+ | 16 pt | `#0E2841` |

> For richer body content (stat cards, tables, grids, category bars, note bands), use layouts **06-pattern-b** through **11-pattern-f** inside the body area instead of plain bullet lists.
