# Pattern — Proportional Category Bar

**When to use:** Visualising the distribution of items across categories as a proportional horizontal bar.

Place in the body area of a standard content slide (`y ≈ 2.0`).

## Visual Structure

```
 │────────────── 類別 A: 66 ──────────────│── 類別 B: 33 ──│─ 類別 C: 16 ─│ D:6 │
   section accent                       secondary accent   grey      orange
```

## Placeholders

```
Bar container:  x:0.5  y:2.0  w:9.0  h:0.5
Each segment:   rect, width proportional to (count / total) × 9.0
Segment label:  inside segment, Arial 14pt bold #FFFFFF (omit if segment < 0.5")
```

## pptxgenjs Code

```javascript
const BAR_X = 0.5, BAR_Y = 2.0, BAR_W = 9.0, BAR_H = 0.5;
const TOTAL = 121;

const segments = [
  { count: 66, label: "類別 A  66", color: "5097FF" },
  { count: 33, label: "類別 B  33", color: "FF9000" },
  { count: 16, label: "類別 C  16", color: "888888" },
  { count: 6,  label: "類別 D  6",  color: "FF47FF" },
];

let curX = BAR_X;
segments.forEach(({ count, label, color }) => {
  const segW = BAR_W * (count / TOTAL);
  slide.addShape(pres.ShapeType.rect, {
    x: curX, y: BAR_Y, w: segW, h: BAR_H,
    fill: { color }, line: { color }
  });
  if (segW > 0.5) {
    slide.addText(label, {
      x: curX + 0.05, y: BAR_Y + 0.05, w: segW - 0.05, h: BAR_H - 0.1,
      fontFace: "Arial", fontSize: 14, bold: true, color: "FFFFFF",
      valign: "middle", margin: 0
    });
  }
  curX += segW;
});
```

## Notes

- Always replace segment colours with ADATA section accent colours — never use arbitrary greys or layout_example purple (`#6B2FA5`).
- Combine with the Stat Cards pattern below the bar for a richer summary view.
