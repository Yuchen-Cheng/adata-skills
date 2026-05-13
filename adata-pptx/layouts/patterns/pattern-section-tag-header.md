# Pattern — Section Tag Header

**When to use:** Use this compact header **instead of** the default 55 pt title block when the slide needs extra vertical body space, or when an English category label above the Chinese title improves readability. Combine with Stat Cards, Table Layout, Unit Grid, Note Band, or other body patterns below.

## Visual Structure

```
┌────────────────────────────────────────────────────────────────────────┐
│ ▌ CATEGORY LABEL (14pt, accent)                                        │  ← y=0.35
│                                                                        │
│ 主標題文字 (40pt Arial Black, bold, ADATA accent colour)               │  ← y=0.65
│ 副標題或說明文字 (17pt Arial, #555555)                                 │  ← y=1.35
└────────────────────────────────────────────────────────────────────────┘
Body area starts at ~y=1.95
```

## Placeholders

```
Accent bar:      x:0.45  y:0.35  w:0.12  h:0.38   filled rect, colour = accent
Category label:  x:0.62  y:0.35  w:9.0   h:0.38   Arial  14pt  accent  bold
Main title:      x:0.45  y:0.77  w:9.1   h:0.72   Arial Black  40pt  accent  bold
Subtitle:        x:0.45  y:1.52  w:9.1   h:0.38   Arial  17pt  #555555
```

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // replace with current section colour

// Thin vertical accent bar
slide.addShape(pres.ShapeType.rect, {
  x: 0.45, y: 0.35, w: 0.12, h: 0.38,
  fill: { color: ACCENT }, line: { color: ACCENT }
});

// Category label
slide.addText("CATEGORY · 子分類", {
  x: 0.62, y: 0.35, w: 9.0, h: 0.38,
  fontFace: "Arial", fontSize: 14, bold: true, color: ACCENT,
  valign: "middle", margin: 0
});

// Main title — Arial Black, ADATA accent colour
slide.addText("主標題", {
  x: 0.45, y: 0.77, w: 9.1, h: 0.72,
  fontFace: "Arial Black", fontSize: 40, bold: true, color: ACCENT,
  valign: "middle", margin: 0
});

// Subtitle / description
slide.addText("副標題或背景說明文字", {
  x: 0.45, y: 1.52, w: 9.1, h: 0.38,
  fontFace: "Arial", fontSize: 17, color: "555555",
  valign: "middle", margin: 0
});
```

## Notes

- Title must use `Arial Black` + section accent colour (never a plain dark colour such as `#222222`).
- This header frees up body area starting from approximately `y = 1.95`.
