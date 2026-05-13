# Pattern — Six-Card Grid (3 × 2)

**When to use:** Six content cards arranged in a 3-column × 2-row grid, each card featuring a coloured accent icon at the top-left, a bold title label, and a short description body — ideal for presenting six features, initiatives, use cases, or team items with equal visual weight.

## Visual Structure

```
 x=0.94       x=3.70       x=6.45
 w=2.61       w=2.61       w=2.61
┌──────────┐ ┌──────────┐ ┌──────────┐  y=1.41
│[■] 標題1 │ │[■] 標題2 │ │[■] 標題3 │  icon 0.69×0.45
│ 說明文字  │ │ 說明文字  │ │ 說明文字  │  h=1.79
└──────────┘ └──────────┘ └──────────┘  y=3.20

┌──────────┐ ┌──────────┐ ┌──────────┐  y=3.28
│[■] 標題4 │ │[■] 標題5 │ │[■] 標題6 │
│ 說明文字  │ │ 說明文字  │ │ 說明文字  │  h=1.79
└──────────┘ └──────────┘ └──────────┘  y=5.07
```

## Key Elements

| Element | X (relative to card) | Y (relative to card) | W | H | Font | Colour |
|---------|----------------------|-----------------------|---|---|------|--------|
| Card background | 0 | 0 | 2.61 | 1.79 | — | #FFFFFF / border #D8D8D8 |
| Accent left stripe | 0 | 0 | 0.07 | 1.79 | — | accent |
| Icon rounded rect | 0.14 | 0.08 | 0.69 | 0.45 | — | accent (light) |
| Icon label / number | 0.14 | 0.08 | 0.69 | 0.45 | Arial Black 16pt | accent |
| Card title | 0.92 | 0.12 | 1.57 | 0.32 | Arial 13pt Bold | #0E2841 |
| Body text | 0.14 | 0.62 | 2.33 | 1.08 | Arial 11pt | #444444 |

**Card column X (absolute):** `[0.94, 3.70, 6.45]`

**Card row Y (absolute):** `[1.41, 3.28]`

**Card size:** `w=2.61, h=1.79`  (gap between rows: `0.08`, gap between cols: `0.09`)

## pptxgenjs Code

```javascript
// Pattern — Six-Card Grid (3×2)
// 假設 slide、pres 物件已存在

const NAVY = "0E2841";
const BODY_COLOR = "444444";

// 6 cards: row × col layout; accent colour cycles or per-card
const CARDS = [
  // Row 1
  { title: "標題一", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "5097FF", icon: "01" },
  { title: "標題二", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "2EA561", icon: "02" },
  { title: "標題三", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "FF9000", icon: "03" },
  // Row 2
  { title: "標題四", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "EC4899", icon: "04" },
  { title: "標題五", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "18B6B4", icon: "05" },
  { title: "標題六", body: "簡短說明文字，描述此項目的核心要點與價值。", accent: "5963B0", icon: "06" },
];

const COL_X = [0.94, 3.70, 6.45];
const ROW_Y = [1.41, 3.28];
const CARD_W = 2.61;
const CARD_H = 1.79;

CARDS.forEach((card, idx) => {
  const col = idx % 3;
  const row = Math.floor(idx / 3);
  const cx = COL_X[col];
  const cy = ROW_Y[row];

  // ── Card background (white, subtle border) ──
  slide.addShape(pres.ShapeType.roundRect, {
    x: cx, y: cy, w: CARD_W, h: CARD_H,
    fill: { color: "FFFFFF" },
    line: { color: "D8D8D8", pt: 0.5 },
    rectRadius: 0.05
  });

  // ── Left accent stripe ──
  slide.addShape(pres.ShapeType.rect, {
    x: cx, y: cy, w: 0.07, h: CARD_H,
    fill: { color: card.accent }, line: { color: card.accent }
  });

  // ── Icon rounded rect (top-left, light tinted background) ──
  slide.addShape(pres.ShapeType.roundRect, {
    x: cx + 0.14, y: cy + 0.08, w: 0.69, h: 0.45,
    fill: { color: card.accent + "22" },   // 13% opacity approximation
    line: { color: card.accent, pt: 0.75 },
    rectRadius: 0.04
  });

  // Icon number / badge text centred in icon box
  slide.addText(card.icon, {
    x: cx + 0.14, y: cy + 0.08, w: 0.69, h: 0.45,
    fontFace: "Arial Black", fontSize: 16, bold: true,
    color: card.accent, align: "center", valign: "middle", margin: 0
  });

  // ── Card title (right of icon) ──
  slide.addText(card.title, {
    x: cx + 0.92, y: cy + 0.12, w: 1.57, h: 0.32,
    fontFace: "Arial", fontSize: 13, bold: true,
    color: NAVY, valign: "middle", margin: 0, wrap: true
  });

  // ── Body description text ──
  slide.addText(card.body, {
    x: cx + 0.14, y: cy + 0.62, w: 2.33, h: 1.08,
    fontFace: "Arial", fontSize: 11, color: BODY_COLOR,
    valign: "top", margin: 0, wrap: true, lineSpacingMultiple: 1.2
  });
});
```

## Usage Notes

- Replace the `icon` field with a number (e.g. `"01"`) or a short symbol (e.g. `"★"`).
- To use a uniform accent colour, set all six `accent` fields to the same hex.
- Safe zone: content spans `y = 1.41 → 5.07`, within the ADATA 5.35 safe zone limit.
- For a 3-column × 1-row layout (3 cards only), use `ROW_Y = [2.10]` with `CARD_H = 2.50` for taller cards.

## Example

Use for: "六大解決方案"、"六個產品功能一覽"、"六個月行動計畫"、"各部門 Q3 重點項目".
