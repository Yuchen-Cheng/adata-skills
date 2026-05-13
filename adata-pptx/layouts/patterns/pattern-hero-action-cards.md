# Pattern — Hero Statement + Action Cards

**When to use:** "Conclusion" or "call-to-action" page. Upper half: large hero callout box (one-sentence core conclusion); lower half: 3 action cards (numbered badge + title + description). Perfect for: presentation closing summary, monthly report action items, project kick-off page.

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header                                               │
│  標題文字 / Subtitle                                              │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  主要結論或關鍵洞察：在此輸入一句話的核心訊息            │    │
│  │  字體大、視覺衝擊強                              [v1.0]  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                    │
│  本月 / 本期三件事                                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │
│  │ [01] 行動一  │   │ [02] 行動二  │   │ [03] 行動三  │         │
│  │ 標題         │   │ 標題         │   │ 標題         │         │
│  │              │   │              │   │              │         │
│  │ 說明文字...  │   │ 說明文字...  │   │ 說明文字...  │         │
│  └──────────────┘   └──────────────┘   └──────────────┘         │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder     | Description                              | Example                  |
|-----------------|------------------------------------------|--------------------------|
| `heroText`      | Hero callout 主文字                       | `121 項作業中…`          |
| `subHeroText`   | Hero callout 副文字（第二行，可選）       | `Phase 0→1→2 不可跳序`   |
| `badgeLabel`    | 右上角版本徽章文字（可省略）              | `v4.1 更新`              |
| `sectionLabel`  | 卡片區塊標題                              | `本月 / 本期三件事`      |
| `CARDS[]`       | 行動卡片陣列（num, numColor, title, desc）| 01–03                    |
| `ACCENT`        | 主強調色                                  | `5097FF`                 |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";

// Hero callout 框
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.5, y: 2.0, w: 9.0, h: 1.35,
  fill: { color: "EEF4FF" }, line: { color: ACCENT, pt: 1.0 }, rectRadius: 0.08
});
slide.addText("主要結論或關鍵洞察：在此輸入一句話的核心訊息，字體大、視覺衝擊強", {
  x: 0.75, y: 2.1, w: 8.5, h: 0.65,
  fontFace: "Arial Black", fontSize: 20, bold: true, color: NAVY,
  valign: "middle", margin: 0, wrap: true
});
// Hero 副文字（可選）
slide.addText("Phase 0 IT 基礎 → Phase 1 流程自動化 → Phase 2 AI 加值", {
  x: 0.75, y: 2.72, w: 8.5, h: 0.42,
  fontFace: "Arial", fontSize: 13, color: NAVY,
  valign: "middle", margin: 0, wrap: true
});

// 版本徽章（可省略）
slide.addShape(pres.ShapeType.roundRect, {
  x: 8.2, y: 2.08, w: 1.1, h: 0.28,
  fill: { color: ACCENT }, line: { color: ACCENT }, rectRadius: 0.05
});
slide.addText("v1.0 更新", {
  x: 8.2, y: 2.08, w: 1.1, h: 0.28,
  fontFace: "Arial", fontSize: 9, bold: true, color: "FFFFFF",
  align: "center", valign: "middle", margin: 0
});

// 卡片區標題
slide.addText("本月 / 本期三件事", {
  x: 0.5, y: 3.5, w: 9.0, h: 0.32,
  fontFace: "Arial", fontSize: 13, bold: true, color: NAVY,
  valign: "middle", margin: 0
});

// 3 個行動卡片
const CARDS = [
  { num: "01", numColor: "2EA561", title: "行動一標題", desc: "行動一說明文字，補充背景與具體步驟或預期產出" },
  { num: "02", numColor: ACCENT,   title: "行動二標題", desc: "行動二說明文字，補充背景與具體步驟或預期產出" },
  { num: "03", numColor: "FF9000", title: "行動三標題", desc: "行動三說明文字，補充背景與具體步驟或預期產出" },
];
const CARD_W = 2.8, CARD_H = 1.6, CARD_Y = 3.9;

CARDS.forEach(({ num, numColor, title, desc }, idx) => {
  const cx = 0.5 + idx * (CARD_W + 0.15);

  // 卡片底板
  slide.addShape(pres.ShapeType.roundRect, {
    x: cx, y: CARD_Y, w: CARD_W, h: CARD_H,
    fill: { color: "FFFFFF" }, line: { color: "E0E0E0", pt: 0.5 }, rectRadius: 0.06
  });

  // 序號徽章
  slide.addShape(pres.ShapeType.roundRect, {
    x: cx + 0.1, y: CARD_Y + 0.1, w: 0.55, h: 0.55,
    fill: { color: numColor }, line: { color: numColor }, rectRadius: 0.06
  });
  slide.addText(num, {
    x: cx + 0.1, y: CARD_Y + 0.1, w: 0.55, h: 0.55,
    fontFace: "Arial Black", fontSize: 16, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });

  // 卡片標題
  slide.addText(title, {
    x: cx + 0.75, y: CARD_Y + 0.12, w: CARD_W - 0.85, h: 0.4,
    fontFace: "Arial", fontSize: 13, bold: true, color: NAVY,
    valign: "middle", margin: 0
  });

  // 說明文字
  slide.addText(desc, {
    x: cx + 0.12, y: CARD_Y + 0.72, w: CARD_W - 0.22, h: 0.8,
    fontFace: "Arial", fontSize: 11, color: NAVY,
    valign: "top", margin: 0, wrap: true
  });
});
```

## Notes
- Hero callout 框高度 `h: 1.35` 可容納 1–2 行大文字；文字超出時縮小 `fontSize: 16`
- 版本徽章（`v1.0 更新`）可省略，刪除對應的 `addShape` + `addText` 即可
- 3 個行動卡片序號建議使用不同顏色（綠/藍/橙）以視覺區分優先序
- 如行動超過 3 個，改用 Numbered Step List pattern
- Hero 框背景色建議與 section accent 同色系的淡色（如 `EEF4FF` 對應 `5097FF`）
