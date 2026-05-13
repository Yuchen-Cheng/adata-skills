# Pattern — Heatmap Matrix

**When to use:** Heat/density matrix for multi-dimensional cross-tabulation. Rows × columns grid structure. Ideal for "units × categories distribution count", "cross-dimension data comparison". Column headers colour-coded by category; row total column added; category total row at bottom.

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header                                               │
│  標題文字 / Subtitle                                              │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ 項目\類別│ ██ 類別A │ ██ 類別B │ ██ 類別C │ ██ 類別D │ ██ 合計  │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ 列項目 1 │    9     │    7     │    6     │    0     │   22     │
│ 列項目 2 │    3     │   22     │    8     │    3     │   36     │
│ 列項目 3 │    3     │    9     │    9     │    2     │   23     │
│ 列項目 4 │    0     │   18     │    1     │    1     │   20     │
│ 列項目 5 │    0     │    5     │    4     │    0     │    9     │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ ██類別合計│   16     │   61     │   28     │    6     │  111     │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

## Placeholders

| Placeholder   | Description                          | Example             |
|---------------|--------------------------------------|---------------------|
| `COLS[]`      | 欄位定義（x, w, label, headerFill）  | 類別 A–D + 合計     |
| `ROWS[]`      | 資料列（label, cells: string[]）     | `["9","7","6","0","22"]` |
| `COL_TOTALS`  | 合計列數值陣列                        | `["16","61","28","6","111"]` |
| `LIGHT_FILLS` | 各欄淡色背景（hex），與欄色同色系     | `["E8E8E8","BFD8F1",...]` |
| `ACCENT`      | 主強調色（同 section 色）             | `5097FF`            |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";

const COLS = [
  { x: 2.6,  w: 1.55, label: "類別 A", headerFill: "9E9E9E" },
  { x: 4.15, w: 1.55, label: "類別 B", headerFill: ACCENT },
  { x: 5.7,  w: 1.55, label: "類別 C", headerFill: "FF9000" },
  { x: 7.25, w: 1.55, label: "類別 D", headerFill: "FF47FF" },
  { x: 8.8,  w: 1.65, label: "合計",   headerFill: ACCENT },
];
const ROW_LABEL_X = 0.5, ROW_LABEL_W = 2.05;
const HEADER_Y = 2.0, ROW_H = 0.45;
const LIGHT_FILLS = ["E8E8E8", "BFD8F1", "FFE8CC", "F5D6F5", "EEE5F7"];

// 欄標頭列左上角儲存格
slide.addShape(pres.ShapeType.rect, {
  x: ROW_LABEL_X, y: HEADER_Y, w: ROW_LABEL_W, h: ROW_H,
  fill: { color: "222222" }, line: { color: "222222" }
});
slide.addText("項目 \\ 類別", {
  x: ROW_LABEL_X + 0.1, y: HEADER_Y + 0.08, w: ROW_LABEL_W - 0.1, h: ROW_H - 0.16,
  fontFace: "Arial", fontSize: 12, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0
});

// 欄標頭
COLS.forEach(({ x, w, label, headerFill }) => {
  slide.addShape(pres.ShapeType.rect, {
    x, y: HEADER_Y, w, h: ROW_H,
    fill: { color: headerFill }, line: { color: headerFill }
  });
  slide.addText(label, {
    x: x + 0.05, y: HEADER_Y + 0.08, w: w - 0.05, h: ROW_H - 0.16,
    fontFace: "Arial", fontSize: 12, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });
});

// 資料列
const ROWS = [
  { label: "列項目 1", cells: ["9",  "7",  "6",  "0",  "22"] },
  { label: "列項目 2", cells: ["3",  "22", "8",  "3",  "36"] },
  { label: "列項目 3", cells: ["3",  "9",  "9",  "2",  "23"] },
  { label: "列項目 4", cells: ["0",  "18", "1",  "1",  "20"] },
  { label: "列項目 5", cells: ["0",  "5",  "4",  "0",  "9"]  },
];
ROWS.forEach((row, ri) => {
  const rowY = HEADER_Y + ROW_H * (ri + 1);
  const rowFill = ri % 2 === 0 ? "F5F5F5" : "FFFFFF";
  // 列標籤
  slide.addShape(pres.ShapeType.rect, {
    x: ROW_LABEL_X, y: rowY, w: ROW_LABEL_W, h: ROW_H,
    fill: { color: rowFill }, line: { color: "DDDDDD", pt: 0.25 }
  });
  slide.addText(row.label, {
    x: ROW_LABEL_X + 0.15, y: rowY + 0.08, w: ROW_LABEL_W - 0.15, h: ROW_H - 0.16,
    fontFace: "Arial", fontSize: 12, color: NAVY, valign: "middle", margin: 0
  });
  // 資料儲存格
  COLS.forEach(({ x, w }, ci) => {
    slide.addShape(pres.ShapeType.rect, {
      x, y: rowY, w, h: ROW_H,
      fill: { color: LIGHT_FILLS[ci] }, line: { color: "DDDDDD", pt: 0.25 }
    });
    slide.addText(row.cells[ci], {
      x: x + 0.05, y: rowY + 0.08, w: w - 0.05, h: ROW_H - 0.16,
      fontFace: "Arial", fontSize: 13,
      color: ci === 4 ? ACCENT : NAVY, bold: ci === 4,
      align: "center", valign: "middle", margin: 0
    });
  });
});

// 合計列
const sumY = HEADER_Y + ROW_H * (ROWS.length + 1);
const COL_FILLS = ["9E9E9E", ACCENT, "FF9000", "FF47FF", ACCENT];
const COL_TOTALS = ["16", "61", "28", "6", "111"];
slide.addShape(pres.ShapeType.rect, {
  x: ROW_LABEL_X, y: sumY, w: ROW_LABEL_W, h: ROW_H,
  fill: { color: "222222" }, line: { color: "222222" }
});
slide.addText("類別合計", {
  x: ROW_LABEL_X + 0.15, y: sumY + 0.08, w: ROW_LABEL_W - 0.15, h: ROW_H - 0.16,
  fontFace: "Arial", fontSize: 12, bold: true, color: "FFFFFF", valign: "middle", margin: 0
});
COLS.forEach(({ x, w }, ci) => {
  slide.addShape(pres.ShapeType.rect, {
    x, y: sumY, w, h: ROW_H,
    fill: { color: COL_FILLS[ci] }, line: { color: COL_FILLS[ci] }
  });
  slide.addText(COL_TOTALS[ci], {
    x: x + 0.05, y: sumY + 0.08, w: w - 0.05, h: ROW_H - 0.16,
    fontFace: "Arial", fontSize: 13, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });
});
```

## Notes
- `ROWS` 建議 4–7 列；超過 7 列時縮小 `ROW_H` 至 0.35
- `COLS` 最後一欄（合計）用較深色強調，建議與 section accent 一致
- `LIGHT_FILLS` 各欄請使用對應欄標頭色的淡化版，保持視覺對應
- 可在儲存格內加入圖示或 emoji 強調極值（最高 / 最低）
- 搭配 Note Band pattern 在頁底補充數據說明
