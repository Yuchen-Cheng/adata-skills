# Layout 02 — Agenda Slide

**Background:** `slide02_agenda.jpg`  
**When to use:** Table of contents / outline — list all section names.

## Placeholders

```
Title:  x:0.5  y:0.4  w:9.0  h:1.2   Arial Black  66pt  #FFFFFF  bold
Body:   x:0.5  y:1.8  w:8.5  h:3.5   Arial        28pt  #FFFFFF
```

## pptxgenjs Code

```javascript
const agenda = pres.addSlide();
addBackground(agenda, "slide02_agenda.jpg");

agenda.addText("Agenda", {
  x: 0.5, y: 0.4, w: 9.0, h: 1.2,
  fontFace: "Arial Black", fontSize: 66, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0
});
agenda.addText([
  { text: "Section 1 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 2 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 3 Name", options: { bullet: true, breakLine: true } },
  { text: "Section 4 Name", options: { bullet: true } },
], {
  x: 0.5, y: 1.8, w: 8.5, h: 3.5,
  fontFace: "Arial", fontSize: 28, color: "FFFFFF",
  valign: "top", margin: 0
});
```

## Rules

- List section names as a bulleted or numbered list, one per line, 28 pt Arial white.
- Use `bullet: true` — never unicode bullet characters (•, ◆, etc.).
