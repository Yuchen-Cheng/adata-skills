# Layout 03 — Section Divider Slide

**Backgrounds (one per section, cycle after §4):**

| Section | Background file |
|---------|----------------|
| §1 | `slide03_section_divider_blue.jpg` |
| §2 | `slide05_section_divider_green.jpg` |
| §3 | `slide07_section_divider_orange.jpg` |
| §4 | `slide09_section_divider_magenta.jpg` |

**When to use:** Opening slide for each section.

> Safe zone: keep all text within the **left 55–60%** of the slide.

## Placeholders

```
Section title:    x:0.5  y:2.1  w:6.5  h:1.8   Arial Black  66pt  #FFFFFF  bold
Section subtitle: x:0.5  y:4.0  w:6.5  h:0.9   Arial        28pt  #FFFFFF
```

## pptxgenjs Code

```javascript
// Replace bgFile with the appropriate section background
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

## Section Colour Map

```javascript
const SECTION_COLORS = {
  1: { accent: "5097FF", bg_divider: "slide03_section_divider_blue.jpg",    bg_content: "slide04_content_blue.jpg" },
  2: { accent: "19C711", bg_divider: "slide05_section_divider_green.jpg",   bg_content: "slide06_content_green.jpg" },
  3: { accent: "FF9000", bg_divider: "slide07_section_divider_orange.jpg",  bg_content: "slide08_content_orange.jpg" },
  4: { accent: "FF47FF", bg_divider: "slide09_section_divider_magenta.jpg", bg_content: "slide10_content_magenta.jpg" },
};
// For section N > 4: SECTION_COLORS[((N - 1) % 4) + 1]
```
