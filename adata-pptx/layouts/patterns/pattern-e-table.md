# Layout 10 — Pattern E: Table Layout

**When to use:** Structured task/action tables with 3–4 columns — e.g., `#` | 工作內容 | 頻率 | AI方案.

## Column Widths and Positions

| Col | x | w | Typical content |
|-----|---|---|----------------|
| 1 | 0.45 | 0.34 | Row # |
| 2 | 0.79 | 2.025 | 工作內容 |
| 3 | 2.81 | 0.64 | 頻率 |
| 4 | 3.45 | 6.08 | AI 整合方案 |

Row height: `0.34"`. Place the header row at `y=1.60` (adjust per slide title).

## Alternating Row Fill Colours (by section)

| Section | Row A fill | Row B fill |
|---------|-----------|-----------|
| §1 Blue | `F5F8FF` | `FFFFFF` |
| §2 Green | `F2FBF1` | `FFFFFF` |
| §3 Orange | `FFF8F0` | `FFFFFF` |
| §4 Magenta | `FFF0FF` | `FFFFFF` |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // replace with section colour
const NAVY   = "0E2841";

const COLS = [
  { x: 0.45, w: 0.34,  label: "#"          },
  { x: 0.79, w: 2.025, label: "工作內容"   },
  { x: 2.81, w: 0.64,  label: "頻率"       },
  { x: 3.45, w: 6.08,  label: "解決方案 / Solution" },
];
const ROW_H   = 0.34;
const HEADER_Y = 1.60;  // adjust per slide

// Header row
COLS.forEach(({ x, w, label }) => {
  slide.addShape(pres.ShapeType.rect, {
    x, y: HEADER_Y, w, h: ROW_H,
    fill: { color: ACCENT }, line: { color: ACCENT }
  });
  slide.addText(label, {
    x: x + 0.04, y: HEADER_Y + 0.04, w: w - 0.04, h: ROW_H - 0.08,
    fontFace: "Arial", fontSize: 13, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });
});

// Data rows
const ROWS = [
  { id: 1, content: "任務項目一", freq: "日(2h)", ai: "AI｜使用 AI 工具自動產出"  },
  { id: 2, content: "任務項目二", freq: "週(1h)", ai: "IT｜需開發 API 整合程式"   },
  // ... add more rows
];
const ROW_FILLS = ["F5F8FF", "FFFFFF"]; // §1 blue; replace per section

ROWS.forEach((row, i) => {
  const rowY = HEADER_Y + ROW_H * (i + 1);
  const fill = ROW_FILLS[i % 2];
  COLS.forEach(({ x, w }) => {
    slide.addShape(pres.ShapeType.rect, {
      x, y: rowY, w, h: ROW_H,
      fill: { color: fill }, line: { color: "D8D8D8", pt: 0.25 }
    });
  });
  const values = [String(row.id), row.content, row.freq, row.ai];
  values.forEach((val, ci) => {
    const { x, w } = COLS[ci];
    slide.addText(val, {
      x: x + 0.04, y: rowY + 0.04, w: w - 0.04, h: ROW_H - 0.08,
      fontFace: "Arial", fontSize: ci === 1 ? 12 : 11,
      bold: ci === 1, color: ci === 0 ? "555555" : NAVY,
      valign: "middle", margin: 0
    });
  });
});
```

## Notes

- Header fill = section accent colour; header text = white, 13 pt bold.
- Column widths can be adjusted — ensure all `x + w` values still sum to `≤ 9.5` to stay in the safe zone.
- Use Pattern F (note band) at `y=4.65` for caveats or update notes at the bottom of the slide.
