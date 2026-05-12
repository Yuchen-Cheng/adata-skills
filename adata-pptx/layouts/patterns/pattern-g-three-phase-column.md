# Layout 12 — Pattern G: Three-Phase Column

## When to Use
三個並排垂直欄位，適合呈現「三階段推進」、「三平台架構」、「三層策略」等需要橫向對比的內容。每欄含：彩色標頭 + 說明副標 + 條列內容 + 底部 tag。欄間以箭頭連結，強調順序性。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
├───────────────┐    ┌───────────────┐    ┌───────────────┐        │
│ ████ Phase 0  │ ▶  │ ████ Phase 1  │ ▶  │ ████ Phase 2  │        │
│ Q2 2026       │    │ Q2–Q3 2026    │    │ Q3–Q4 2026    │        │
├───────────────┤    ├───────────────┤    ├───────────────┤        │
│ ▸ 項目說明一  │    │ ▸ 項目說明一  │    │ ▸ 項目說明一  │        │
│ ▸ 項目說明二  │    │ ▸ 項目說明二  │    │ ▸ 項目說明二  │        │
│ ▸ 項目說明三  │    │ ▸ 項目說明三  │    │ ▸ 項目說明三  │        │
│               │    │               │    │               │        │
│ [  底部 tag ] │    │ [ 底部 tag  ] │    │ [ 底部 tag  ] │        │
└───────────────┘    └───────────────┘    └───────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder   | Description                           | Example          |
|---------------|---------------------------------------|------------------|
| `PHASES`      | 三個欄位的設定陣列（label, sub, items, tag） | Phase 0 / 1 / 2  |
| `accent`      | 每欄強調色 (hex)                       | `2EA561`         |
| `label`       | 欄位標題                               | `Phase 0 IT 基礎` |
| `sub`         | 欄位副標（時程或說明）                 | `Q2 2026`        |
| `items[]`     | 最多 4 個條列文字                      | `API 平台 PoC`   |
| `tag`         | 底部分類 tag 文字                      | `基礎建設`       |
| `tagColor`    | 底部 tag 顏色                          | `2EA561`         |

## pptxgenjs Code

```javascript
const PHASES = [
  {
    x: 0.5, accent: "2EA561", label: "Phase 0", sub: "Q2 2026",
    items: ["項目說明一", "項目說明二", "項目說明三"],
    tag: "基礎建設", tagColor: "2EA561"
  },
  {
    x: 3.35, accent: "5097FF", label: "Phase 1", sub: "Q2–Q3 2026",
    items: ["項目說明一", "項目說明二", "項目說明三"],
    tag: "流程自動化", tagColor: "5097FF"
  },
  {
    x: 6.2, accent: "FF9000", label: "Phase 2", sub: "Q3–Q4 2026",
    items: ["項目說明一", "項目說明二", "項目說明三"],
    tag: "AI 加值", tagColor: "FF9000"
  },
];

const COL_W = 2.7;
const HEADER_Y = 2.0, HEADER_H = 0.6;
const BODY_Y = 2.65, BODY_H = 1.85;
const TAG_Y = 4.6, TAG_H = 0.35;
const NAVY = "0E2841";

PHASES.forEach(({ x, accent, label, sub, items, tag, tagColor }) => {
  // Header rounded rect
  slide.addShape(pres.ShapeType.roundRect, {
    x, y: HEADER_Y, w: COL_W, h: HEADER_H,
    fill: { color: accent }, line: { color: accent }, rectRadius: 0.05
  });
  slide.addText(label, {
    x: x + 0.1, y: HEADER_Y + 0.04, w: COL_W - 0.2, h: 0.28,
    fontFace: "Arial Black", fontSize: 14, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });
  slide.addText(sub, {
    x: x + 0.1, y: HEADER_Y + 0.3, w: COL_W - 0.2, h: 0.22,
    fontFace: "Arial", fontSize: 11, color: "FFFFFF",
    valign: "middle", margin: 0
  });

  // Body area
  slide.addShape(pres.ShapeType.roundRect, {
    x, y: BODY_Y, w: COL_W, h: BODY_H,
    fill: { color: "F5F5F5" }, line: { color: "E0E0E0", pt: 0.5 }, rectRadius: 0.05
  });
  items.forEach((item, idx) => {
    slide.addText("▸ " + item, {
      x: x + 0.12, y: BODY_Y + 0.15 + idx * 0.5, w: COL_W - 0.22, h: 0.45,
      fontFace: "Arial", fontSize: 12, color: NAVY,
      valign: "top", margin: 0, wrap: true
    });
  });

  // Bottom tag
  slide.addShape(pres.ShapeType.roundRect, {
    x: x + 0.35, y: TAG_Y, w: COL_W - 0.7, h: TAG_H,
    fill: { color: tagColor }, line: { color: tagColor }, rectRadius: 0.06
  });
  slide.addText(tag, {
    x: x + 0.35, y: TAG_Y, w: COL_W - 0.7, h: TAG_H,
    fontFace: "Arial", fontSize: 11, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });
});

// Arrows between phases
[3.23, 6.08].forEach(arrowX => {
  slide.addShape(pres.ShapeType.rightArrow, {
    x: arrowX, y: 3.4, w: 0.1, h: 0.35,
    fill: { color: "CCCCCC" }, line: { color: "CCCCCC" }
  });
});
```

## Notes
- 三欄等寬 (w=2.7)，總寬 9.0"，間距由箭頭連結
- `items` 建議 3–4 條；超過 4 條時縮小字體至 10pt
- 若無順序性（非流程）可省略箭頭，三欄獨立呈現
- 底部 tag 可省略，改為頁底 Pattern F note band
- 欲強調「平行」而非「順序」時，三欄可使用相同顏色
