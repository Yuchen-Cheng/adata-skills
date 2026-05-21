# Pattern — Five-Column Icon Band

**When to use:** Five equal columns, each with a small numbered icon badge, a bold category label, a shared coloured horizontal band across the middle containing a circular visual accent, and a short description text below — ideal for presenting five parallel features, workflows, or key messages with a strong visual connector between columns.

## Visual Structure

```
  [01]    [02]    [03]    [04]    [05]    ← icon badges  y=1.56, h=0.50
LABEL 1 LABEL 2 LABEL 3 LABEL 4 LABEL 5  ← category labels y=2.14, h=0.24

┌──────────────────────────────────────┐  y=2.53
│  (○)  │  (○)  │  (○)  │  (○)  │  (○) │  coloured band h=1.52
└──────────────────────────────────────┘  y=4.05

 desc.   desc.   desc.   desc.   desc.   ← body text  y=4.15, h=0.60
```

## Key Elements

| Element | X | Y | Width | Height | Font | Colour |
|---------|---|---|-------|--------|------|--------|
| Icon badge (rounded rect) | col_x+0.35 | 1.56 | 0.96 | 0.50 | — | accent |
| Icon number text | col_x+0.35 | 1.56 | 0.96 | 0.50 | Arial Black 18pt | #FFFFFF |
| Category label text | col_x | 2.14 | 1.66 | 0.24 | Arial 12pt Bold | #0E2841 |
| Shared band background | 0.59 | 2.53 | 8.84 | 1.52 | — | #F5F5F5 / border |
| Column band section (per col) | col_x+0.06 | 2.53 | 1.55 | 1.52 | — | accent (10% fill) |
| Circle accent (per col) | col_x+0.33 | 2.78 | 1.00 | 1.00 | — | accent |
| Column divider line | col_x+1.67 | 2.53 | 0 | 1.52 | — | #D0D0D0 |
| Description text | col_x | 4.15 | 1.66 | 0.60 | Arial 11pt | #444444 |

**Column X positions:** `[0.59, 2.38, 4.17, 5.96, 7.76]`  (each `w=1.67`)

## pptxgenjs Code

```javascript
// Pattern — Five-Column Icon Band
// 假設 slide、pres 物件已存在

const NAVY    = "0E2841";
const BODY_COLOR = "444444";
const BAND_BG = "F0F4FA";

// 5 columns: accent colour + label + description
const COLUMNS = [
  { accent: "5097FF", label: "類別一", desc: "此欄位的簡短說明，兩行以內為佳。" },
  { accent: "2EA561", label: "類別二", desc: "此欄位的簡短說明，兩行以內為佳。" },
  { accent: "FF9000", label: "類別三", desc: "此欄位的簡短說明，兩行以內為佳。" },
  { accent: "EC4899", label: "類別四", desc: "此欄位的簡短說明，兩行以內為佳。" },
  { accent: "18B6B4", label: "類別五", desc: "此欄位的簡短說明，兩行以內為佳。" },
];

const COL_X    = [0.59, 2.38, 4.17, 5.96, 7.76];
const COL_W    = 1.67;

const ICON_Y   = 1.56;
const ICON_H   = 0.50;
const ICON_W   = 0.96;

const LABEL_Y  = 2.14;
const LABEL_H  = 0.24;

const BAND_Y   = 2.53;
const BAND_H   = 1.52;
const BAND_X   = COL_X[0];                  // 0.59
const BAND_W   = COL_X[4] + COL_W - BAND_X; // 8.84

const CIRCLE_W = 1.00;
const CIRCLE_H = 1.00;

const DESC_Y   = 4.15;
const DESC_H   = 0.60;

// ── Shared band background ──
slide.addShape(pres.ShapeType.rect, {
  x: BAND_X, y: BAND_Y, w: BAND_W, h: BAND_H,
  fill: { color: BAND_BG }, line: { color: "D0D0D0", pt: 0.5 }
});

COLUMNS.forEach(({ accent, label, desc }, i) => {
  const cx = COL_X[i];
  const iconX = cx + (COL_W - ICON_W) / 2; // horizontally centred in column

  // ── Numbered icon badge ──
  slide.addShape(pres.ShapeType.roundRect, {
    x: iconX, y: ICON_Y, w: ICON_W, h: ICON_H,
    fill: { color: accent }, line: { color: accent },
    rectRadius: 0.08
  });
  slide.addText(String(i + 1).padStart(2, "0"), {
    x: iconX, y: ICON_Y, w: ICON_W, h: ICON_H,
    fontFace: "Arial Black", fontSize: 18, bold: true,
    color: "FFFFFF", align: "center", valign: "middle", margin: 0
  });

  // ── Category label ──
  slide.addText(label, {
    x: cx, y: LABEL_Y, w: COL_W, h: LABEL_H,
    fontFace: "Arial", fontSize: 12, bold: true,
    color: NAVY, align: "center", valign: "middle", margin: 0
  });

  // ── Per-column tinted section inside band ──
  slide.addShape(pres.ShapeType.rect, {
    x: cx + 0.06, y: BAND_Y, w: COL_W - 0.12, h: BAND_H,
    fill: { color: accent, transparency: 88 },   // ~12% opacity tint
    line: { color: "CCCCCC", pt: 0 }
  });

  // ── Circle accent within band ──
  const circleX = cx + (COL_W - CIRCLE_W) / 2;
  slide.addShape(pres.ShapeType.ellipse, {
    x: circleX, y: BAND_Y + (BAND_H - CIRCLE_H) / 2, w: CIRCLE_W, h: CIRCLE_H,
    fill: { color: accent }, line: { color: accent }
  });

  // Column divider (skip after last column)
  if (i < COLUMNS.length - 1) {
    slide.addShape(pres.ShapeType.line, {
      x: cx + COL_W, y: BAND_Y, w: 0, h: BAND_H,
      line: { color: "D0D0D0", pt: 0.5 }
    });
  }

  // ── Description text below band ──
  slide.addText(desc, {
    x: cx, y: DESC_Y, w: COL_W, h: DESC_H,
    fontFace: "Arial", fontSize: 11, color: BODY_COLOR,
    align: "center", valign: "top", margin: 0, wrap: true
  });
});
```

## Usage Notes

- The circle inside the band can be replaced with an icon glyph using `slide.addText("★", ...)` over the shape.
- To add text inside the circle (e.g. a metric), add a `slide.addText()` at the same coordinates after the ellipse.
- Safe zone: content spans `y = 1.56 → 4.75`, well within the ADATA 5.35 safe zone limit.
- The shared band at `y=2.53` visually connects all five columns into a single horizontal unit.

## Example

Use for: "五大服務流程"、"五個核心價值"、"產品五大亮點"、"五步驟執行框架".
