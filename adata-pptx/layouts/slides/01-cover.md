# Layout 01 — Cover Slide

**Background:** `slide01_cover.jpg`  
**When to use:** First slide — title, subtitle, date.

> Safe zone: keep all text within the **left 55%** of the slide (right ~40% is the ADATA geometric graphic).

## Placeholders

```
Main title:  x:0.5  y:2.0  w:5.5  h:1.8   Arial Black  66pt  #FFFFFF  bold
Subtitle:    x:0.5  y:3.9  w:5.5  h:0.8   Arial        32pt  #FFFFFF
Date:        x:0.5  y:4.9  w:5.5  h:0.5   Arial        16pt  #FFFFFF
```

## pptxgenjs Code

```javascript
const cover = pres.addSlide();
addBackground(cover, "slide01_cover.jpg");

cover.addText("Presentation Title", {
  x: 0.5, y: 2.0, w: 5.5, h: 1.8,
  fontFace: "Arial Black", fontSize: 66, bold: true, color: "FFFFFF",
  valign: "middle", margin: 0, wrap: true
});
cover.addText("Subtitle text", {
  x: 0.5, y: 3.9, w: 5.5, h: 0.8,
  fontFace: "Arial", fontSize: 32, color: "FFFFFF",
  valign: "middle", margin: 0
});
cover.addText("May 2026", {
  x: 0.5, y: 4.9, w: 5.5, h: 0.5,
  fontFace: "Arial", fontSize: 16, color: "FFFFFF",
  margin: 0
});
```
