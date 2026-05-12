# Layout 15 — Pattern J: Two-Column Comparison

## When to Use
左右兩欄對比清單，適合呈現「A 類型 vs B 類型」、「AI 處理 vs 人力專注」、「Track A vs Track B」等二元對比。每欄含彩色標頭 + 多行條目列 + 右側標籤徽章。底部可加結論橫幅。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
│  [ 情境說明橫幅（背景說明）                                 ]    │
│                                                                    │
│  ┌────────────────────┐   ┌────────────────────┐                 │
│  │ ████ 欄位標題 A    │   │ ████ 欄位標題 B    │                 │
│  ├────────────────────┤   ├────────────────────┤                 │
│  │ 條目一        標籤 │   │ 條目一        標籤 │                 │
│  │ 條目二        標籤 │   │ 條目二        標籤 │                 │
│  │ 條目三        標籤 │   │ 條目三        標籤 │                 │
│  │ 條目四        標籤 │   │ 條目四        標籤 │                 │
│  │ 條目五        標籤 │   │ 條目五        標籤 │                 │
│  └────────────────────┘   └────────────────────┘                 │
│  [ ● 結論：補充整體說明或關鍵洞察文字                      ]    │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder    | Description                          | Example               |
|----------------|--------------------------------------|-----------------------|
| `ACCENT_L`     | 左欄強調色                            | `5097FF`              |
| `ACCENT_R`     | 右欄強調色                            | `19C711`              |
| `title`        | 各欄標題文字                          | `欄位標題 A`          |
| `items[].label`| 條目文字                              | `條目說明文字`        |
| `items[].badge`| 右側標籤文字（可為數字或短文字）      | `−30%`                |
| `contextText`  | 頂部情境橫幅文字                      | `背景說明`            |
| `conclusionText`| 底部結論文字                         | `結論：...`           |

## pptxgenjs Code

```javascript
const ACCENT_L = "5097FF"; // 左欄顏色
const ACCENT_R = "19C711"; // 右欄顏色
const NAVY = "0E2841";
const PANEL_W = 4.4;
const LEFT_X = 0.5, RIGHT_X = 5.05;

// 情境說明橫幅
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.5, y: 2.0, w: 9.0, h: 0.42,
  fill: { color: "EEF4FF" }, line: { color: ACCENT_L, pt: 0.5 }, rectRadius: 0.04
});
slide.addText("背景說明或核心邏輯：補充說明兩欄比較的關係", {
  x: 0.7, y: 2.04, w: 8.6, h: 0.34,
  fontFace: "Arial", fontSize: 12, color: NAVY, valign: "middle", margin: 0
});

// 兩欄面板（左 / 右）
[
  {
    x: LEFT_X, accent: ACCENT_L,
    title: "欄位標題 A（例：AI 可處理）",
    items: [
      { label: "條目說明一", badge: "標籤" },
      { label: "條目說明二", badge: "標籤" },
      { label: "條目說明三", badge: "標籤" },
      { label: "條目說明四", badge: "標籤" },
      { label: "條目說明五", badge: "標籤" },
    ]
  },
  {
    x: RIGHT_X, accent: ACCENT_R,
    title: "欄位標題 B（例：人力專注）",
    items: [
      { label: "條目說明一", badge: "標籤" },
      { label: "條目說明二", badge: "標籤" },
      { label: "條目說明三", badge: "標籤" },
      { label: "條目說明四", badge: "標籤" },
      { label: "條目說明五", badge: "標籤" },
    ]
  },
].forEach(({ x, accent, title, items }) => {
  const HEADER_H = 0.42;

  // 欄標頭
  slide.addShape(pres.ShapeType.roundRect, {
    x, y: 2.58, w: PANEL_W, h: HEADER_H,
    fill: { color: accent }, line: { color: accent }, rectRadius: 0.05
  });
  slide.addText(title, {
    x: x + 0.1, y: 2.62, w: PANEL_W - 0.2, h: HEADER_H - 0.08,
    fontFace: "Arial", fontSize: 13, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });

  // 條目列
  items.forEach(({ label, badge }, idx) => {
    const iy = 3.07 + idx * 0.4;
    slide.addShape(pres.ShapeType.roundRect, {
      x, y: iy, w: PANEL_W, h: 0.35,
      fill: { color: "F8F8F8" }, line: { color: "E0E0E0", pt: 0.25 }, rectRadius: 0.03
    });
    slide.addText(label, {
      x: x + 0.12, y: iy + 0.04, w: PANEL_W - 1.0, h: 0.27,
      fontFace: "Arial", fontSize: 12, color: NAVY, valign: "middle", margin: 0
    });
    slide.addText(badge, {
      x: x + PANEL_W - 0.85, y: iy + 0.04, w: 0.8, h: 0.27,
      fontFace: "Arial", fontSize: 10, bold: true, color: accent,
      align: "right", valign: "middle", margin: 0
    });
  });
});

// 底部結論橫幅
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.5, y: 5.1, w: 9.0, h: 0.38,
  fill: { color: "F0F0F0" }, line: { color: "CCCCCC", pt: 0.5 }, rectRadius: 0.05
});
slide.addText("● 結論：補充整體說明或關鍵洞察文字", {
  x: 0.7, y: 5.12, w: 8.6, h: 0.3,
  fontFace: "Arial", fontSize: 12, bold: true, color: NAVY, valign: "middle", margin: 0
});
```

## Notes
- 每欄最多 6 個條目；超過時縮小條目高度 `h: 0.32`
- `badge` 可為數值（`−30%`）、短文字（`已完成`）或空字串
- 如左右欄無對比關係（僅平行呈現），兩欄可使用相同顏色
- 底部結論橫幅可省略，改用 Pattern F（Note Band）
- 情境說明橫幅可省略，讓兩欄從 `y: 2.0` 直接開始
