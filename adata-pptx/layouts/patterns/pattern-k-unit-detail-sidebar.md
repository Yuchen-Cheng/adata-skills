# Layout 16 — Pattern K: Unit Detail Sidebar

## When to Use
左側欄（Sidebar）+ 右側條列，適合「單一單位深入分析」場景：左側顯示大型總計數字與分類 legend（A/B/C/D），右側顯示最具代表性的項目條目列（含類別徽章 + 任務名稱 + 建議文字）。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
├──────────────┬─────────────────────────────────────────────────┤
│  單位概況    │  重點項目（代表性案例）                           │
│              │                                                    │
│     22       │  ┌─┬─────────────────────────────────────────┐   │
│              │  │B│ 項目名稱一                               │   │
│  項日常工作  │  │ │ 建議/說明文字                            │   │
│  ──────────  │  └─┴─────────────────────────────────────────┘   │
│ ▌ A 純人工 9 │  ┌─┬─────────────────────────────────────────┐   │
│ ▌ B IT 流程7 │  │B│ 項目名稱二                               │   │
│ ▌ C AI 加值6 │  │ │ 建議/說明文字                            │   │
│ ▌ D 待釐清 0 │  └─┴─────────────────────────────────────────┘   │
│              │  （共 5 個條目列）                                │
└──────────────┴─────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder      | Description                              | Example            |
|------------------|------------------------------------------|--------------------|
| `totalCount`     | 左側大型數字                              | `22`               |
| `totalLabel`     | 數字下方說明文字                          | `項日常工作`       |
| `LEGEND[]`       | 分類 legend（dot, label, count, pct）     | A/B/C/D 各分類     |
| `ITEMS[]`        | 右側條目列（cat, catColor, title, note）  | 最多 6 個條目      |
| `listTitle`      | 右側欄位標題文字                          | `重點項目（代表性案例）` |
| `ACCENT`         | 主強調色                                  | `5097FF`           |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";
const SIDEBAR_X = 0.5, SIDEBAR_W = 2.8;
const LIST_X = 3.5, LIST_W = 6.05;
const TOP_Y = 2.0, H = 3.3;

// Sidebar 背景
slide.addShape(pres.ShapeType.roundRect, {
  x: SIDEBAR_X, y: TOP_Y, w: SIDEBAR_W, h: H,
  fill: { color: "F5F5F5" }, line: { color: "E0E0E0", pt: 0.5 }, rectRadius: 0.06
});

// Sidebar：標籤
slide.addText("單位概況", {
  x: SIDEBAR_X + 0.15, y: TOP_Y + 0.12, w: SIDEBAR_W - 0.3, h: 0.3,
  fontFace: "Arial", fontSize: 13, bold: true, color: "888888",
  valign: "middle", margin: 0
});

// Sidebar：大型計數
slide.addText("22", {
  x: SIDEBAR_X + 0.1, y: TOP_Y + 0.42, w: SIDEBAR_W - 0.2, h: 0.9,
  fontFace: "Arial Black", fontSize: 60, bold: true, color: NAVY,
  valign: "middle", margin: 0
});
slide.addText("項日常工作", {
  x: SIDEBAR_X + 0.15, y: TOP_Y + 1.35, w: SIDEBAR_W - 0.3, h: 0.3,
  fontFace: "Arial", fontSize: 13, color: "555555",
  valign: "middle", margin: 0
});

// Sidebar：分隔線
slide.addShape(pres.ShapeType.rect, {
  x: SIDEBAR_X + 0.15, y: TOP_Y + 1.72, w: SIDEBAR_W - 0.3, h: 0.02,
  fill: { color: "DDDDDD" }, line: { color: "DDDDDD" }
});

// Sidebar：ABCD Legend
const LEGEND = [
  { dot: "9E9E9E", label: "A 純人工", count: "9",  pct: "41%" },
  { dot: ACCENT,   label: "B IT 流程", count: "7",  pct: "32%" },
  { dot: "FF9000", label: "C AI 加值", count: "6",  pct: "27%" },
  { dot: "FF47FF", label: "D 待釐清",  count: "0",  pct: "0%"  },
];
LEGEND.forEach(({ dot, label, count, pct }, idx) => {
  const ly = TOP_Y + 1.85 + idx * 0.33;
  slide.addShape(pres.ShapeType.rect, {
    x: SIDEBAR_X + 0.15, y: ly + 0.04, w: 0.1, h: 0.22,
    fill: { color: dot }, line: { color: dot }
  });
  slide.addText(label, {
    x: SIDEBAR_X + 0.32, y: ly, w: 1.2, h: 0.3,
    fontFace: "Arial", fontSize: 11, color: NAVY, valign: "middle", margin: 0
  });
  slide.addText(count, {
    x: SIDEBAR_X + 1.75, y: ly, w: 0.4, h: 0.3,
    fontFace: "Arial", fontSize: 11, bold: true, color: NAVY,
    align: "right", valign: "middle", margin: 0
  });
  slide.addText(pct, {
    x: SIDEBAR_X + 2.15, y: ly, w: 0.55, h: 0.3,
    fontFace: "Arial", fontSize: 10, color: "888888",
    align: "right", valign: "middle", margin: 0
  });
});

// 右側：欄位標題
slide.addText("重點項目（代表性案例）", {
  x: LIST_X, y: TOP_Y, w: LIST_W, h: 0.3,
  fontFace: "Arial", fontSize: 13, bold: true, color: "888888",
  valign: "middle", margin: 0
});

// 右側：條目列（最多 6 個）
const ITEMS = [
  { cat: "B", catColor: ACCENT,   title: "項目名稱一", note: "建議/說明文字" },
  { cat: "B", catColor: ACCENT,   title: "項目名稱二", note: "建議/說明文字" },
  { cat: "B", catColor: ACCENT,   title: "項目名稱三", note: "建議/說明文字" },
  { cat: "C", catColor: "FF9000", title: "項目名稱四", note: "建議/說明文字" },
  { cat: "C", catColor: "FF9000", title: "項目名稱五", note: "建議/說明文字" },
];
ITEMS.forEach(({ cat, catColor, title, note }, idx) => {
  const iy = TOP_Y + 0.42 + idx * 0.58;
  slide.addShape(pres.ShapeType.roundRect, {
    x: LIST_X, y: iy, w: LIST_W, h: 0.52,
    fill: { color: "FFFFFF" }, line: { color: "E0E0E0", pt: 0.5 }, rectRadius: 0.04
  });
  // 左側類別 badge
  slide.addShape(pres.ShapeType.rect, {
    x: LIST_X, y: iy, w: 0.28, h: 0.52,
    fill: { color: catColor }, line: { color: catColor }
  });
  slide.addText(cat, {
    x: LIST_X, y: iy + 0.1, w: 0.28, h: 0.32,
    fontFace: "Arial Black", fontSize: 12, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });
  // 項目標題
  slide.addText(title, {
    x: LIST_X + 0.38, y: iy + 0.04, w: LIST_W - 0.42, h: 0.22,
    fontFace: "Arial", fontSize: 12, bold: true, color: NAVY, valign: "middle", margin: 0
  });
  // 說明文字
  slide.addText(note, {
    x: LIST_X + 0.38, y: iy + 0.26, w: LIST_W - 0.42, h: 0.22,
    fontFace: "Arial", fontSize: 11, color: "555555", valign: "middle", margin: 0
  });
});
```

## Notes
- 左側大型數字建議 2 位數以內；超過 3 位數時縮小 `fontSize: 42`
- 右側條目最多 6 個（`ITEM_H = 0.52`，總高 3.12"）；6 個以上時改 `h: 0.42`
- `cat` badge 建議使用單個大寫字母（A/B/C/D）
- Legend 中 `pct` 百分比可省略，僅顯示計數
- 本 pattern 與 Pattern G（Three-Phase Column）可搭配：使用 Pattern G 呈現整體，再用本 pattern 深入各欄位
