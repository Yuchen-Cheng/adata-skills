# Layout 13 — Pattern H: Org Chart / Hierarchy

## When to Use
組織架構圖或層級關係圖，適合呈現「專案團隊組成」、「負責人 → 子團隊 → 成員單位」的三層層級。頂部有情境說明橫幅，底部一排 SPOC 卡片（最多 5 個）。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
├──────────────────────────────────────────────────────────────────┤
│  [   情境說明橫幅（背景說明或注意事項）                    ]    │
│                      ┌───────────────┐                           │
│                      │ 專案負責人/PM │                           │
│                      │    角色說明   │                           │
│                      └───────┬───────┘                           │
│             ┌────────────────┴───────────────┐                   │
│    ┌────────┴────────┐              ┌────────┴────────┐          │
│    │   子團隊 A      │              │   子團隊 B      │          │
│    │   職責說明      │              │   職責說明      │          │
│    └─────────────────┘              └─────────────────┘          │
│  成員單位（各指派窗口 SPOC）                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                  │
│  │單位 A│ │單位 B│ │單位 C│ │單位 D│ │單位 E│                  │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘                  │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder   | Description                          | Example              |
|---------------|--------------------------------------|----------------------|
| `contextText` | 情境說明橫幅文字                      | `背景說明或注意事項` |
| `pmTitle`     | 頂部節點標題                          | `專案負責人 / PM`    |
| `pmSub`       | 頂部節點副標                          | `角色說明`           |
| `MID[]`       | 中層節點陣列（accent, title, sub）    | 子團隊 A / B         |
| `SPOCS[]`     | 底部 SPOC 卡片陣列（label, sub, accent）| 單位 A–E            |
| `ACCENT`      | 主要強調色                            | `5097FF`             |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";

// 情境說明橫幅
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.5, y: 2.0, w: 9.0, h: 0.42,
  fill: { color: "EEF4FF" }, line: { color: ACCENT, pt: 0.5 }, rectRadius: 0.04
});
slide.addText("說明文字（背景、目標、或注意事項）", {
  x: 0.7, y: 2.04, w: 8.6, h: 0.34,
  fontFace: "Arial", fontSize: 12, color: NAVY,
  valign: "middle", margin: 0
});

// 頂部 PM 節點
slide.addShape(pres.ShapeType.roundRect, {
  x: 3.25, y: 2.58, w: 3.5, h: 0.65,
  fill: { color: ACCENT }, line: { color: ACCENT }, rectRadius: 0.05
});
slide.addText("專案負責人 / PM", {
  x: 3.25, y: 2.63, w: 3.5, h: 0.32,
  fontFace: "Arial Black", fontSize: 13, bold: true, color: "FFFFFF",
  align: "center", valign: "middle", margin: 0
});
slide.addText("角色說明", {
  x: 3.25, y: 2.9, w: 3.5, h: 0.22,
  fontFace: "Arial", fontSize: 10, color: "FFFFFF",
  align: "center", valign: "middle", margin: 0
});

// 連接線（PM → 中層）
slide.addShape(pres.ShapeType.line, {
  x: 5.0, y: 3.23, w: 0.0, h: 0.27,
  line: { color: "BBBBBB", pt: 1.0 }
});
slide.addShape(pres.ShapeType.line, {
  x: 2.25, y: 3.5, w: 5.5, h: 0.0,
  line: { color: "BBBBBB", pt: 1.0 }
});
[2.25, 7.75].forEach(lx => {
  slide.addShape(pres.ShapeType.line, {
    x: lx, y: 3.5, w: 0.0, h: 0.1,
    line: { color: "BBBBBB", pt: 1.0 }
  });
});

// 中層節點
const MID = [
  { x: 1.0, accent: ACCENT,    title: "子團隊 A", sub: "職責說明" },
  { x: 6.5, accent: "FF9000",  title: "子團隊 B", sub: "職責說明" },
];
MID.forEach(({ x, accent, title, sub }) => {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y: 3.6, w: 2.5, h: 0.85,
    fill: { color: accent }, line: { color: accent }, rectRadius: 0.05
  });
  slide.addText(title, {
    x: x + 0.1, y: 3.65, w: 2.3, h: 0.32,
    fontFace: "Arial Black", fontSize: 12, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });
  slide.addText(sub, {
    x: x + 0.1, y: 3.95, w: 2.3, h: 0.28,
    fontFace: "Arial", fontSize: 10, color: "FFFFFF",
    valign: "middle", margin: 0
  });
});

// SPOC 標籤列
slide.addText("成員單位（各指派窗口 SPOC）", {
  x: 0.5, y: 4.58, w: 9.0, h: 0.28,
  fontFace: "Arial", fontSize: 12, bold: true, color: NAVY,
  valign: "middle", margin: 0
});

// 底部 SPOC 卡片（最多 5 個）
const SPOCS = [
  { label: "單位 A", sub: "SPOC 職責說明", accent: ACCENT },
  { label: "單位 B", sub: "SPOC 職責說明", accent: "19C711" },
  { label: "單位 C", sub: "SPOC 職責說明", accent: "FF9000" },
  { label: "單位 D", sub: "SPOC 職責說明", accent: "FF47FF" },
  { label: "單位 E", sub: "SPOC 職責說明", accent: ACCENT },
];
const SPOC_W = 1.6, SPOC_H = 0.9, SPOC_Y = 4.92;
SPOCS.forEach(({ label, sub, accent }, idx) => {
  const sx = 0.5 + idx * 1.7;
  slide.addShape(pres.ShapeType.roundRect, {
    x: sx, y: SPOC_Y, w: SPOC_W, h: SPOC_H,
    fill: { color: "FFFFFF" }, line: { color: "D0D0D0", pt: 0.5 }, rectRadius: 0.05
  });
  slide.addShape(pres.ShapeType.rect, {
    x: sx, y: SPOC_Y, w: SPOC_W, h: 0.3,
    fill: { color: accent }, line: { color: accent }
  });
  slide.addText(label, {
    x: sx + 0.05, y: SPOC_Y + 0.04, w: SPOC_W - 0.1, h: 0.22,
    fontFace: "Arial Black", fontSize: 11, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });
  slide.addText(sub, {
    x: sx + 0.05, y: SPOC_Y + 0.34, w: SPOC_W - 0.1, h: 0.52,
    fontFace: "Arial", fontSize: 9, color: NAVY,
    valign: "top", margin: 0, wrap: true
  });
});
```

## Notes
- 中層節點可為 1–3 個，根據組織結構調整 `x` 位置
- SPOC 卡片最多 5 個；少於 5 個時增大 `SPOC_W`（例如 4 個時改為 `w: 2.05`）
- 如不需連接線，可刪除 `addShape line` 段落，改用視覺距離呈現層級
- 底部 SPOC 卡片顏色建議與所代表的業務分類色一致
