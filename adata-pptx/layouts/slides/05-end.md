# Layout 05 — End / Blank Slide

**Background:** `slide11_blank.jpg`  
**When to use:** Closing slide — thank-you, Q&A, or simply end the deck.

## Placeholders

No mandatory text placeholders. Optionally add a centred thank-you line.

```
Optional thank-you:  x:0  y:2.3  w:100%  h:1.0   Arial Black  40pt  #FFFFFF  bold  centre-aligned
```

## pptxgenjs Code

```javascript
const end = pres.addSlide();
addBackground(end, "slide11_blank.jpg");

// Optional centred thank-you text:
end.addText("Thank You", {
  x: 0, y: 2.3, w: "100%", h: 1.0,
  fontFace: "Arial Black", fontSize: 40, bold: true, color: "FFFFFF",
  align: "center", valign: "middle", margin: 0
});
```
