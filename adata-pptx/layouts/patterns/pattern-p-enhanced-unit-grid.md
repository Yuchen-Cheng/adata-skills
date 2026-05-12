# Layout 21 — Pattern P: Enhanced Unit Grid with Breakdown Bar

## When to Use
Pattern D（Unit Grid）的強化版：每張部門/單位卡片內增加 **ABCD 比例橫條** 與 **各類計數 legend**，在一眼即可看出「各單位的結構分佈」。適合「多單位綜合概覽 + 分類組成一頁呈現」的場景。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ ████ 部門 A  │  │ ████ 部門 B  │  │ ████ 部門 C  │           │
│  │     22       │  │     36       │  │     23       │           │
│  │  個項目      │  │  個項目      │  │  個項目      │           │
│  │ [━━━━░░░░░░] │  │ [━━━━━━━░░░] │  │ [━━━━━━░░░░] │           │
│  │ A:9 B:7 C:6  │  │ A:3 B:22 C:8 │  │ A:3 B:9 C:9  │           │
│  │ 說明文字...  │  │ 說明文字...  │  │ 說明文字...  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ ████ 部門 D  │  │ ████ 部門 E  │  │ ████ 部門 F  │           │
│  │ ...          │  │ ...          │  │ ...          │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder         | Description                                   | Example              |
|---------------------|-----------------------------------------------|----------------------|
| `deptName`          | 部門/單位名稱                                  | `部門 A`             |
| `count`             | 總項目數                                       | `22`                 |
| `desc`              | 說明文字（1 行）                               | `說明文字 / 代表作業類型` |
| `accent`            | 卡片強調色（各單位可不同）                      | `5097FF`             |
| `breakdown[]`       | 各分類計數與顏色 `[{count, color}]`            | A/B/C/D              |

## pptxgenjs Code

```javascript
const NAVY = "0E2841";

function addEnhancedUnitCard(slide, pres, { x, y, deptName, count, desc, accent, breakdown }) {
  const W = 2.9, H = 1.9, HEADER_H = 0.35;
  const BAR_Y_OFFSET = 0.9;
  const BAR_H = 0.2, BAR_W = W - 0.25;

  // 卡片底板
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w: W, h: H,
    fill: { color: "FFFFFF" }, line: { color: "D0D0D0", pt: 0.5 }, rectRadius: 0.05
  });

  // 彩色標頭
  slide.addShape(pres.ShapeType.rect, {
    x, y, w: W, h: HEADER_H,
    fill: { color: accent }, line: { color: accent }
  });
  slide.addText(deptName, {
    x: x + 0.12, y: y + 0.04, w: W - 0.2, h: HEADER_H - 0.08,
    fontFace: "Arial Black", fontSize: 14, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });

  // 大型計數
  slide.addText(String(count), {
    x: x + 0.1, y: y + HEADER_H + 0.05, w: 1.0, h: 0.5,
    fontFace: "Arial Black", fontSize: 30, bold: true, color: accent,
    valign: "middle", margin: 0
  });
  slide.addText("個項目", {
    x: x + 0.1, y: y + HEADER_H + 0.55, w: 1.2, h: 0.2,
    fontFace: "Arial", fontSize: 10, color: "555555", valign: "middle", margin: 0
  });

  // ABCD 比例橫條
  const total = breakdown.reduce((s, b) => s + b.count, 0);
  let barX = x + 0.12;
  if (total > 0) {
    breakdown.forEach(({ count: bc, color }) => {
      if (bc === 0) return;
      const segW = BAR_W * (bc / total);
      slide.addShape(pres.ShapeType.rect, {
        x: barX, y: y + BAR_Y_OFFSET, w: segW, h: BAR_H,
        fill: { color }, line: { color }
      });
      barX += segW;
    });
  }

  // 各分類計數 legend（A/B/C/D）
  const CATS = ["A", "B", "C", "D"];
  const CAT_COLORS = ["9E9E9E", accent, "FF9000", "FF47FF"];
  let legX = x + 0.1;
  breakdown.forEach(({ count: bc }, idx) => {
    slide.addShape(pres.ShapeType.rect, {
      x: legX, y: y + BAR_Y_OFFSET + BAR_H + 0.04, w: 0.08, h: 0.14,
      fill: { color: CAT_COLORS[idx] }, line: { color: CAT_COLORS[idx] }
    });
    slide.addText(`${CATS[idx]}: ${bc}`, {
      x: legX + 0.1, y: y + BAR_Y_OFFSET + BAR_H + 0.04, w: 0.52, h: 0.14,
      fontFace: "Arial", fontSize: 8, color: "555555", valign: "middle", margin: 0
    });
    legX += 0.65;
  });

  // 說明文字
  slide.addText(desc, {
    x: x + 0.1, y: y + 1.55, w: W - 0.18, h: 0.3,
    fontFace: "Arial", fontSize: 10, color: NAVY,
    valign: "top", margin: 0, wrap: true
  });
}

// 第一列（上方 3 個卡片）
addEnhancedUnitCard(slide, pres, {
  x: 0.5, y: 1.7, deptName: "部門 A", count: 22,
  desc: "說明文字 / 代表作業類型", accent: "5097FF",
  breakdown: [{ count: 9, color: "9E9E9E" }, { count: 7, color: "5097FF" }, { count: 6, color: "FF9000" }, { count: 0, color: "FF47FF" }]
});
addEnhancedUnitCard(slide, pres, {
  x: 3.5, y: 1.7, deptName: "部門 B", count: 36,
  desc: "說明文字 / 代表作業類型", accent: "19C711",
  breakdown: [{ count: 3, color: "9E9E9E" }, { count: 22, color: "19C711" }, { count: 8, color: "FF9000" }, { count: 3, color: "FF47FF" }]
});
addEnhancedUnitCard(slide, pres, {
  x: 6.5, y: 1.7, deptName: "部門 C", count: 23,
  desc: "說明文字 / 代表作業類型", accent: "FF9000",
  breakdown: [{ count: 3, color: "9E9E9E" }, { count: 9, color: "FF9000" }, { count: 9, color: "5097FF" }, { count: 2, color: "FF47FF" }]
});

// 第二列（下方 3 個卡片）
addEnhancedUnitCard(slide, pres, {
  x: 0.5, y: 3.65, deptName: "部門 D", count: 20,
  desc: "說明文字 / 代表作業類型", accent: "5097FF",
  breakdown: [{ count: 0, color: "9E9E9E" }, { count: 18, color: "5097FF" }, { count: 1, color: "FF9000" }, { count: 1, color: "FF47FF" }]
});
addEnhancedUnitCard(slide, pres, {
  x: 3.5, y: 3.65, deptName: "部門 E", count: 9,
  desc: "說明文字 / 代表作業類型", accent: "19C711",
  breakdown: [{ count: 0, color: "9E9E9E" }, { count: 5, color: "19C711" }, { count: 4, color: "FF9000" }, { count: 0, color: "FF47FF" }]
});
addEnhancedUnitCard(slide, pres, {
  x: 6.5, y: 3.65, deptName: "部門 F", count: 11,
  desc: "說明文字 / 代表作業類型", accent: "FF9000",
  breakdown: [{ count: 1, color: "9E9E9E" }, { count: 5, color: "FF9000" }, { count: 5, color: "5097FF" }, { count: 0, color: "FF47FF" }]
});
```

## Notes
- `breakdown` 陣列順序固定為 [A, B, C, D]；各 `color` 建議對應固定類別色（A=灰, B=accent, C=橙, D=紫）
- `total === 0` 時橫條不繪製（已在程式碼中處理）
- 與 Pattern D 的差異：Pattern D 無比例橫條，適合純數量展示；Pattern P 適合需要展示組成結構的場景
- 函式 `addEnhancedUnitCard` 可重複調用，不限制 6 張；3 張時只調用上列，調整 `y: 2.7` 置中
- `accent` 每個單位可設定不同顏色，也可全部統一使用同一 section accent
