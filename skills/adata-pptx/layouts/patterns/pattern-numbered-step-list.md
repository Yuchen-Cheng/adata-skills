# Pattern — Numbered Step List

**When to use:** Numbered action plan. Ideal for "step-by-step rollout plan", "seven-step execution", "action priority sequence". Each row: coloured rounded-corner number badge + timeline tag + bold title + description. Up to 7 steps fit neatly on a slide.

## Visual Structure

```
┌──────────────────────────────────────────────────────────────────┐
│  Section Tag Header                                               │
│  標題文字 / Subtitle                                              │
│                                                                    │
│  ┌──┐  本月內  步驟一標題（加粗、強調色）                        │
│  │01│          說明文字：補充背景與具體執行方式                   │
│  └──┘                                                             │
│  ┌──┐  本月內  步驟二標題                                        │
│  │02│          說明文字                                           │
│  └──┘                                                             │
│  ┌──┐  Q2 內   步驟三標題                                        │
│  │03│          說明文字                                           │
│  └──┘                                                             │
│  ... （最多 7 步）                                                │
└──────────────────────────────────────────────────────────────────┘
```

## Placeholders

| Placeholder    | Description                            | Example          |
|----------------|----------------------------------------|------------------|
| `STEPS[]`      | 步驟陣列（num, time, title, desc）      | 01–07            |
| `num`          | 步驟序號（`"01"` 至 `"07"`）           | `"01"`           |
| `time`         | 時程標籤（短文字）                       | `"本月內"` / `"Q2 內"` |
| `title`        | 步驟標題（粗體）                         | `步驟一標題`     |
| `desc`         | 說明文字（可換行）                       | `說明文字...`    |
| `ACCENT`       | 數字徽章顏色                             | `5097FF`         |

## pptxgenjs Code

```javascript
const ACCENT = "5097FF"; // 替換為本節顏色
const NAVY = "0E2841";

const STEPS = [
  { num: "01", time: "本月內", title: "步驟一標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "02", time: "本月內", title: "步驟二標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "03", time: "本月內", title: "步驟三標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "04", time: "本月內", title: "步驟四標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "05", time: "Q2 內",  title: "步驟五標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "06", time: "Q3 內",  title: "步驟六標題", desc: "說明文字：補充背景與具體執行方式" },
  { num: "07", time: "Q4 內",  title: "步驟七標題", desc: "說明文字：補充背景與具體執行方式" },
];

const STEP_H = 0.48, STEP_Y_START = 2.0;
const BADGE_W = 0.52, BADGE_H = 0.5;
const TIME_W = 0.85, TITLE_X = 2.0;

STEPS.forEach(({ num, time, title, desc }, idx) => {
  const sy = STEP_Y_START + idx * (STEP_H + 0.04);

  // 序號徽章
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: sy, w: BADGE_W, h: BADGE_H,
    fill: { color: ACCENT }, line: { color: ACCENT }, rectRadius: 0.06
  });
  slide.addText(num, {
    x: 0.5, y: sy + 0.04, w: BADGE_W, h: BADGE_H - 0.08,
    fontFace: "Arial Black", fontSize: 15, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });

  // 時程標籤
  slide.addText(time, {
    x: 1.15, y: sy + 0.04, w: TIME_W, h: 0.22,
    fontFace: "Arial", fontSize: 11, color: "888888",
    valign: "middle", margin: 0
  });

  // 步驟標題
  slide.addText(title, {
    x: TITLE_X, y: sy + 0.02, w: 7.45, h: 0.22,
    fontFace: "Arial", fontSize: 13, bold: true, color: ACCENT,
    valign: "middle", margin: 0
  });

  // 說明文字
  slide.addText(desc, {
    x: 1.15, y: sy + 0.25, w: 8.45, h: 0.22,
    fontFace: "Arial", fontSize: 11, color: NAVY,
    valign: "middle", margin: 0
  });
});
```

## Notes
- 7 個步驟時總高度約 3.6"，從 `y=2.0` 可完整呈現
- 步驟少於 7 個時可增大行間距（`STEP_H + 0.1` 至 `+0.2`）
- `time` 欄位可改為里程碑（`M1`）、優先級（`P1`）等任何短標籤
- 若步驟無順序性，可改用 Unit Grid pattern 呈現
- 數字徽章顏色可按時程分段（如前 3 個用 accent、後 4 個用灰色）
