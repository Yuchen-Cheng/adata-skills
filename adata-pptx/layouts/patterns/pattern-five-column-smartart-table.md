# Pattern — Five-Column SmartArt Table

**When to use:** Five equal-width vertical columns each with a distinct coloured header block and four data rows below — ideal for comparing five categories, themes, or feature lists side by side on a single slide.

## Visual Structure

```
 x=0.59   x=2.38   x=4.17   x=5.96   x=7.76
 w=1.67   w=1.67   w=1.67   w=1.67   w=1.67
┌────────┬────────┬────────┬────────┬────────┐  y=1.56
│TITLE 1 │TITLE 2 │TITLE 3 │TITLE 4 │TITLE 5 │  Header h=0.82
│(color1)│(color2)│(color3)│(color4)│(color5)│
├────────┼────────┼────────┼────────┼────────┤  y=2.53
│ item A │ item A │ item A │ item A │ item A │  y=2.80, h=0.37
│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│
│ item B │ item B │ item B │ item B │ item B │  y=3.35, h=0.37
│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│
│ item C │ item C │ item C │ item C │ item C │  y=3.91, h=0.37
│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│─ ─ ─ ─│
│ item D │ item D │ item D │ item D │ item D │  y=4.47, h=0.37
└────────┴────────┴────────┴────────┴────────┘  y=5.07
```

## Key Elements

| Element | X | Y | Width | Height | Font | Colour |
|---------|---|---|-------|--------|------|--------|
| Header rect (per col) | col_x | 1.56 | 1.67 | 0.82 | — | accent |
| Header title text | col_x | 1.80 | 1.67 | 0.36 | Arial Black 14pt Bold | #FFFFFF |
| Data bg (per col) | col_x | 2.53 | 1.67 | 2.54 | — | #F5F5F5 |
| Data row divider line | col_x | 3.17 / 3.73 / 4.29 | 1.67 | 0 | — | #E0E0E0 |
| Row text (per cell) | col_x+0.08 | row_y+0.06 | 1.51 | 0.25 | Arial 11pt | #0E2841 |

**Column X positions:** `[0.59, 2.38, 4.17, 5.96, 7.76]`

**Data row Y positions:** `[2.80, 3.35, 3.91, 4.47]`

## pptxgenjs Code

```javascript
// Pattern — Five-Column SmartArt Table
// 假設 slide、pres 物件已存在

const NAVY = "0E2841";
const DATA_BG = "F5F5F5";
const DIVIDER = "D8D8D8";

// 5 columns: each has { x, accent, title, rows[] }
const COLUMNS = [
  {
    x: 0.59, accent: "5097FF", title: "類別一",
    rows: ["項目 A 說明", "項目 B 說明", "項目 C 說明", "項目 D 說明"]
  },
  {
    x: 2.38, accent: "2EA561", title: "類別二",
    rows: ["項目 A 說明", "項目 B 說明", "項目 C 說明", "項目 D 說明"]
  },
  {
    x: 4.17, accent: "FF9000", title: "類別三",
    rows: ["項目 A 說明", "項目 B 說明", "項目 C 說明", "項目 D 說明"]
  },
  {
    x: 5.96, accent: "EC4899", title: "類別四",
    rows: ["項目 A 說明", "項目 B 說明", "項目 C 說明", "項目 D 說明"]
  },
  {
    x: 7.76, accent: "18B6B4", title: "類別五",
    rows: ["項目 A 說明", "項目 B 說明", "項目 C 說明", "項目 D 說明"]
  },
];

const COL_W      = 1.67;
const HEADER_Y   = 1.56;
const HEADER_H   = 0.82;
const DATA_Y     = 2.53;
const DATA_H     = 2.54;
const ROW_Y      = [2.80, 3.35, 3.91, 4.47];
const ROW_H      = 0.37;

COLUMNS.forEach(({ x, accent, title, rows }) => {
  // ── Coloured header block ──
  slide.addShape(pres.ShapeType.rect, {
    x, y: HEADER_Y, w: COL_W, h: HEADER_H,
    fill: { color: accent }, line: { color: accent }
  });

  // Column title centred inside header
  slide.addText(title, {
    x, y: HEADER_Y + 0.22, w: COL_W, h: 0.36,
    fontFace: "Arial Black", fontSize: 14, bold: true,
    color: "FFFFFF", align: "center", valign: "middle", margin: 0
  });

  // ── Data area background ──
  slide.addShape(pres.ShapeType.rect, {
    x, y: DATA_Y, w: COL_W, h: DATA_H,
    fill: { color: DATA_BG }, line: { color: DIVIDER, pt: 0.5 }
  });

  // ── Data rows ──
  rows.forEach((text, i) => {
    const rowY = ROW_Y[i];

    // Row divider (skip before first row)
    if (i > 0) {
      slide.addShape(pres.ShapeType.line, {
        x, y: rowY - 0.09, w: COL_W, h: 0,
        line: { color: DIVIDER, pt: 0.5 }
      });
    }

    slide.addText(text, {
      x: x + 0.08, y: rowY + 0.06, w: COL_W - 0.16, h: ROW_H - 0.12,
      fontFace: "Arial", fontSize: 11, color: NAVY,
      align: "center", valign: "middle", margin: 0, wrap: true
    });
  });
});
```

## Usage Notes

- Column count is fixed at 5; for 3 or 4 columns adjust `x` positions and `COL_W` accordingly.
- Data rows are fixed at 4; add or remove entries in `ROW_Y` to change the row count.
- Each column can carry an independent accent colour to create a rainbow palette.
- Safe zone: content spans `y = 1.56 → 5.07`, within the ADATA 5.35 safe zone limit.

## Example

Use for: "5大核心功能比較"、"五個部門的季度目標"、"各產品線關鍵指標彙整".
