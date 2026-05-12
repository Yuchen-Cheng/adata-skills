# Layout 09 — Pattern D: Department / Unit Cards Grid (2 × 3)

**When to use:** Comparing multiple teams, units, or items that each have a count, sub-breakdown, and short description. Renders 6 cards in two rows of three.

Best combined with Pattern A (section tag header) so the body area starts high enough to fit both rows.

## Visual Structure

```
 ┌──── dept A ────┐  ┌──── dept B ────┐  ┌──── dept C ────┐
 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│  ← coloured header
 │  22            │  │  36            │  │  23            │  ← large count
 │  個項目        │  │  個項目        │  │  個項目        │
 │ 描述說明文字   │  │ 描述說明文字   │  │ 描述說明文字   │
 └────────────────┘  └────────────────┘  └────────────────┘
 x=0.5               x=3.5               x=6.5
 ← repeat row 2 at y=3.45 →
```

Card dimensions: `w=2.9`, `h=1.65`

## pptxgenjs Code

```javascript
function addUnitCard(slide, { x, y, deptName, count, desc, accent }) {
  const W = 2.9, H = 1.65, HEADER_H = 0.38;
  const NAVY = "0E2841";

  // Card background
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w: W, h: H,
    fill: { color: "FFFFFF" }, line: { color: "D0D0D0", pt: 0.5 },
    rectRadius: 0.05
  });
  // Coloured header bar
  slide.addShape(pres.ShapeType.rect, {
    x, y, w: W, h: HEADER_H,
    fill: { color: accent }, line: { color: accent }
  });
  // Department name — Arial Black, white
  slide.addText(deptName, {
    x: x + 0.15, y: y + 0.04, w: W - 0.2, h: HEADER_H - 0.08,
    fontFace: "Arial Black", fontSize: 16, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });
  // Large count number — Arial Black, accent colour
  slide.addText(String(count), {
    x: x + 0.12, y: y + HEADER_H + 0.05, w: 1.2, h: 0.55,
    fontFace: "Arial Black", fontSize: 36, bold: true, color: accent,
    valign: "middle", margin: 0
  });
  // "個項目" sub-label
  slide.addText("個項目", {
    x: x + 0.12, y: y + HEADER_H + 0.6, w: 1.3, h: 0.22,
    fontFace: "Arial", fontSize: 11, color: "555555",
    valign: "middle", margin: 0
  });
  // Description
  slide.addText(desc, {
    x: x + 0.12, y: y + HEADER_H + 0.85, w: W - 0.2, h: 0.72,
    fontFace: "Arial", fontSize: 11, color: NAVY,
    valign: "top", margin: 0, wrap: true
  });
}

// Row 1
addUnitCard(slide, { x: 0.5, y: 1.7,  deptName: "部門 A", count: 22, desc: "項目 / 子項目 / 類型...", accent: "5097FF" });
addUnitCard(slide, { x: 3.5, y: 1.7,  deptName: "部門 B", count: 36, desc: "項目 / 子項目 / 類型...", accent: "19C711" });
addUnitCard(slide, { x: 6.5, y: 1.7,  deptName: "部門 C", count: 23, desc: "項目 / 子項目 / 類型...", accent: "FF9000" });
// Row 2
addUnitCard(slide, { x: 0.5, y: 3.45, deptName: "部門 D", count: 20, desc: "項目 / 子項目 / 類型...", accent: "5097FF" });
addUnitCard(slide, { x: 3.5, y: 3.45, deptName: "部門 E", count: 9,  desc: "項目 / 子項目 / 類型...", accent: "19C711" });
addUnitCard(slide, { x: 6.5, y: 3.45, deptName: "部門 F", count: 15, desc: "項目 / 子項目 / 類型...", accent: "FF9000" });
```

## Notes

- When using this pattern, prefer Pattern A (section tag header) so the body starts at `y ≈ 1.7` and both card rows fit.
- Replace accent colours with the current section's accent colour; different accents per card are allowed to distinguish units.
- The sub-label "個項目" can be replaced with any short unit (e.g., "件", "tasks", "項作業").
