# Pattern — Multi-Phase Roadmap Grid

**When to use:** Time-axis × phase grid-based roadmap. Ideal for "multi-phase × multi-quarter" rollout plans. Rows = phases; columns = time points (quarters/half-years). Column header row at bottom (dark background, white text); left-side phase labels colour-coded by phase.

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header                                               │
│  標題文字 / Subtitle                                              │
│         ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│         │ Q2 2026  │  │ Q3 2026  │  │ Q4 2026  │  │ 2027 H1  │ │
│ ████    ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤ │
│ Phase 0 │  項目一  │  │  項目三  │  │  項目五  │  │ 持續維運 │ │
│ IT 基礎 │  項目二  │  │  項目四  │  │          │  │          │ │
│ ████    ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤ │
│ Phase 1 │ Quick Win│  │ 全面上線 │  │ 主檔聯動 │  │ 滾動優化 │ │
│ 流程自動│  PoC     │  │  RPA     │  │  完成    │  │          │ │
│ ████    ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤ │
│ Phase 2 │  等待 IT │  │ 訪談PoC  │  │  AI 上線 │  │ 規模化   │ │
│ AI 加值 │  基礎就位│  │  啟動    │  │  驗證    │  │  推廣    │ │
│         └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder     | Description                                | Example           |
|-----------------|--------------------------------------------|-------------------|
| `QUARTERS[]`    | 欄標頭（時間標籤）                          | `Q2 2026`         |
| `PHASES[]`      | 階段列定義（label, accent, cells[]）        | Phase 0/1/2       |
| `cells[].text`  | 各儲存格文字（可含 \n 換行）                | `API 平台 PoC`    |
| `cells[].fill`  | 儲存格背景色                               | `E6F5EC`          |
| `cells[].dim`   | 是否以淡灰色呈現（表示尚未啟動）            | `true`            |

## pptxgenjs Code

```javascript
const NAVY = "0E2841";
const ROW_LABEL_X = 0.5, ROW_LABEL_W = 1.55;
const COLS_START_X = 2.15;
const COL_W = 1.7, COL_GAP = 0.02;
const ROW_H = 0.88;
const START_Y = 2.08;

const QUARTERS = ["Q2 2026", "Q3 2026", "Q4 2026", "2027 H1"];
const PHASES = [
  {
    label: "Phase 0\nIT 基礎", accent: "2EA561",
    cells: [
      { text: "項目一\n項目二",      fill: "E6F5EC" },
      { text: "項目三\n項目四",      fill: "E6F5EC" },
      { text: "項目五",             fill: "E6F5EC" },
      { text: "持續維運",            fill: "F5F5F5", dim: true },
    ]
  },
  {
    label: "Phase 1\n流程自動化", accent: "5097FF",
    cells: [
      { text: "Quick Win\nPoC",    fill: "E8F1FC" },
      { text: "全面上線\nRPA",     fill: "E8F1FC" },
      { text: "主檔聯動\n完成",    fill: "E8F1FC" },
      { text: "滾動優化",           fill: "F5F5F5", dim: true },
    ]
  },
  {
    label: "Phase 2\nAI 加值", accent: "FF9000",
    cells: [
      { text: "— 等待 IT\n基礎就位 —", fill: "F5F5F5", dim: true },
      { text: "訪談\nPoC 啟動",     fill: "EEE5F7" },
      { text: "AI 上線\nPoC 驗證",  fill: "EEE5F7" },
      { text: "規模化\n推廣",        fill: "EEE5F7" },
    ]
  },
];

// 季度標頭列
QUARTERS.forEach((q, ci) => {
  const cx = COLS_START_X + ci * (COL_W + COL_GAP);
  slide.addShape(pres.ShapeType.roundRect, {
    x: cx, y: START_Y - 0.45, w: COL_W, h: 0.38,
    fill: { color: "222222" }, line: { color: "222222" }, rectRadius: 0.04
  });
  slide.addText(q, {
    x: cx, y: START_Y - 0.45, w: COL_W, h: 0.38,
    fontFace: "Arial", fontSize: 12, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });
});

// Phase 列 + 儲存格
PHASES.forEach(({ label, accent, cells }, ri) => {
  const rowY = START_Y + ri * (ROW_H + 0.05);

  // Phase 標籤
  slide.addShape(pres.ShapeType.roundRect, {
    x: ROW_LABEL_X, y: rowY, w: ROW_LABEL_W, h: ROW_H,
    fill: { color: accent }, line: { color: accent }, rectRadius: 0.05
  });
  slide.addText(label, {
    x: ROW_LABEL_X + 0.07, y: rowY, w: ROW_LABEL_W - 0.07, h: ROW_H,
    fontFace: "Arial", fontSize: 11, bold: true, color: "FFFFFF",
    valign: "middle", margin: 0, wrap: true
  });

  // 各季度儲存格
  cells.forEach(({ text, fill, dim }, ci) => {
    const cx = COLS_START_X + ci * (COL_W + COL_GAP);
    slide.addShape(pres.ShapeType.roundRect, {
      x: cx, y: rowY, w: COL_W, h: ROW_H,
      fill: { color: fill }, line: { color: "D5D5D5", pt: 0.5 }, rectRadius: 0.04
    });
    slide.addText(text, {
      x: cx + 0.1, y: rowY + 0.1, w: COL_W - 0.2, h: ROW_H - 0.2,
      fontFace: "Arial", fontSize: dim ? 10 : 11,
      color: dim ? "999999" : NAVY,
      align: "center", valign: "middle", margin: 0, wrap: true
    });
  });
});
```

## Notes
- 欄數（季度）建議 3–5 個；欄數增加時縮小 `COL_W` 並調整 `COLS_START_X`
- Phase 列數可增減，`ROW_H` 建議 0.75–1.0"
- `dim: true` 儲存格表示「尚未啟動」，以灰色呈現，文字加破折號標示
- 若需強調某一儲存格，可加粗邊框：`line: { color: accent, pt: 1.5 }`
- 可在儲存格內用 `\n` 換行，列出 2–3 個子項目
