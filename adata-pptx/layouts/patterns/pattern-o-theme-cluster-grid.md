# Layout 20 — Pattern O: Theme Cluster Grid (2×3)

## When to Use
主題聚類卡片，以 2 列 × 3 欄的網格呈現「6 個議題分群」、「6 大主題分析」、「跨單位需求分類」。與 Pattern D（Unit Grid）不同之處：每張卡片著重「主題內容 + 計數 badge + 分布說明」，標頭顏色可依分群意義設定。

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header (Pattern A)                                   │
│  標題文字 / Subtitle                                              │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ ████ 主題一  │  │ ████ 主題二  │  │ ████ 主題三  │           │
│  │          14 項│  │          11 項│  │           6 項│          │
│  │ 說明文字...  │  │ 說明文字...  │  │ 說明文字...  │           │
│  │ 單位：A、B、C│  │ 單位：B、C   │  │ 單位：A、C   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ ████ 主題四  │  │ ████ 主題五  │  │ ████ 主題六  │           │
│  │           5 項│  │           4 項│  │           2 項│          │
│  │ 說明文字...  │  │ 說明文字...  │  │ 說明文字...  │           │
│  │ 單位：A、D   │  │ 單位：B      │  │ 單位：C      │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder        | Description                            | Example          |
|--------------------|----------------------------------------|------------------|
| `THEMES[]`         | 6 個主題卡片定義                        | 主題一–六        |
| `title`            | 卡片主題名稱                            | `主題一`         |
| `count`            | 右側計數文字                            | `14 項`          |
| `content`          | 主題說明文字（1–2 行）                  | `說明文字...`    |
| `dist`             | 分布說明（涵蓋單位或來源）              | `單位：A、B、C`  |
| `headerColor`      | 標頭填色（依主題類型）                  | `5097FF`         |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";
const CARD_W = 2.8, CARD_H = 1.45;
const HEADER_H = 0.42;

const THEMES = [
  { x: 0.5, y: 2.05, headerColor: ACCENT,    title: "主題一", count: "14 項", content: "說明文字：描述此主題的核心內容", dist: "單位：A、B、C" },
  { x: 3.5, y: 2.05, headerColor: ACCENT,    title: "主題二", count: "11 項", content: "說明文字：描述此主題的核心內容", dist: "單位：B、C"   },
  { x: 6.5, y: 2.05, headerColor: ACCENT,    title: "主題三", count: "6 項",  content: "說明文字：描述此主題的核心內容", dist: "單位：A、C"   },
  { x: 0.5, y: 3.6,  headerColor: "FF9000",  title: "主題四", count: "5 項",  content: "說明文字：描述此主題的核心內容", dist: "單位：A、D"   },
  { x: 3.5, y: 3.6,  headerColor: "FF9000",  title: "主題五", count: "4 項",  content: "說明文字：描述此主題的核心內容", dist: "單位：B"      },
  { x: 6.5, y: 3.6,  headerColor: "19C711",  title: "主題六", count: "2 項",  content: "說明文字：描述此主題的核心內容", dist: "單位：C"      },
];

THEMES.forEach(({ x, y, headerColor, title, count, content, dist }) => {
  // 卡片底板
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w: CARD_W, h: CARD_H,
    fill: { color: "FFFFFF" }, line: { color: "D0D0D0", pt: 0.5 }, rectRadius: 0.05
  });

  // 彩色標頭
  slide.addShape(pres.ShapeType.rect, {
    x, y, w: CARD_W, h: HEADER_H,
    fill: { color: headerColor }, line: { color: headerColor }
  });

  // 標題（標頭左側）
  slide.addText(title, {
    x: x + 0.12, y: y + 0.05, w: CARD_W - 1.1, h: HEADER_H - 0.1,
    fontFace: "Arial Black", fontSize: 13, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0
  });

  // 計數 badge（標頭右側）
  slide.addText(count, {
    x: x + CARD_W - 0.95, y: y + 0.05, w: 0.9, h: HEADER_H - 0.1,
    fontFace: "Arial", fontSize: 11, bold: true, color: "FFFFFF",
    align: "right", valign: "middle", margin: 0
  });

  // 說明文字
  slide.addText(content, {
    x: x + 0.1, y: y + HEADER_H + 0.08, w: CARD_W - 0.2, h: 0.55,
    fontFace: "Arial", fontSize: 11, color: NAVY,
    valign: "top", margin: 0, wrap: true
  });

  // 分布說明（底部小字）
  slide.addText(dist, {
    x: x + 0.1, y: y + HEADER_H + 0.68, w: CARD_W - 0.2, h: 0.28,
    fontFace: "Arial", fontSize: 10, color: "777777",
    valign: "middle", margin: 0
  });
});
```

## Notes
- 6 張卡片排列為 2 列 × 3 欄；3 張時改單列 (`y: 2.7`)，4 張時改 2×2
- `headerColor` 可依主題分群使用不同顏色（同色系表示同類）
- `count` 建議格式為「N 項」；也可改為「N%」或「N 個」
- `dist` 行（分布說明）可省略，改為第 2 行說明文字
- 與 Pattern D（Unit Grid）差異：Pattern D 以「部門」為單位，Pattern O 以「主題/議題」為單位
