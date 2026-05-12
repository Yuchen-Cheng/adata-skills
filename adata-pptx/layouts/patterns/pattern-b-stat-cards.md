# Layout 07 — Pattern B: Stat Cards (4 across)

**When to use:** Showing 3–4 key metrics side by side in a horizontal row.

Place inside the body area of a standard content slide (`y ≈ 2.4`, below the subtitle).

## Visual Structure

```
 ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
 ├ accent ──┤  ├ accent ──┤  ├ accent ──┤  ├ accent ──┤
 │   95%    │  │   66     │  │   33     │  │   6      │
 │label one │  │label two │  │ label 3  │  │ label 4  │
 └──────────┘  └──────────┘  └──────────┘  └──────────┘
  x=0.5         x=2.7         x=4.9         x=7.1
```

Card dimensions: `w=2.1`, `h=1.2`

## Placeholders (per card)

```
Card bg:      roundRect  w:2.1  h:1.2  fill:#FFFFFF  border:#D0D0D0
Top stripe:   rect       w:2.1  h:0.07  fill:accent
Metric value: x+0        y+0.12  w:2.1  h:0.72   Arial Black  40pt  accent  centre
Label:        x+0        y+0.87  w:2.1  h:0.28   Arial        12pt  #0E2841  bold  centre
```

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // replace with section colour
const NAVY   = "0E2841";

const CARD_Y = 2.4;  // adjust to fit below subtitle
const CARD_H = 1.2;
const CARD_W = 2.1;

const cards = [
  { x: 0.5, value: "95%", label: "指標一", accent: ACCENT },
  { x: 2.7, value: "66",  label: "指標二", accent: ACCENT },
  { x: 4.9, value: "33",  label: "指標三", accent: ACCENT },
  { x: 7.1, value: "6",   label: "指標四", accent: "FF9000" },
];

cards.forEach(({ x, value, label, accent }) => {
  // Card background (white rounded)
  slide.addShape(pres.ShapeType.roundRect, {
    x, y: CARD_Y, w: CARD_W, h: CARD_H,
    fill: { color: "FFFFFF" }, line: { color: "D0D0D0", pt: 0.5 },
    rectRadius: 0.05
  });
  // Top accent stripe
  slide.addShape(pres.ShapeType.rect, {
    x, y: CARD_Y, w: CARD_W, h: 0.07,
    fill: { color: accent }, line: { color: accent }
  });
  // Metric number — Arial Black, accent colour
  slide.addText(value, {
    x, y: CARD_Y + 0.12, w: CARD_W, h: 0.72,
    fontFace: "Arial Black", fontSize: 40, bold: true, color: accent,
    align: "center", valign: "middle", margin: 0
  });
  // Label — Arial, navy
  slide.addText(label, {
    x, y: CARD_Y + 0.87, w: CARD_W, h: 0.28,
    fontFace: "Arial", fontSize: 12, bold: true, color: NAVY,
    align: "center", valign: "middle", margin: 0
  });
});
```

## Notes

- Use 3 cards by adjusting `x` positions to `0.5`, `3.3`, `6.1` with `w=3.0`.
- Each card can have a different accent colour to highlight outliers or warnings.
