# Layout 11 — Pattern F: Bottom Note Band

**When to use:** Update notes, caveats, risk callouts, or any secondary information that should appear at the bottom of a content slide without overlapping the main body.

Add this **after** the main body pattern on the same slide.

## Visual Structure

```
 ╰─────────────────────────────────────────────────────────────────────╯
   ● 本次更新: 說明文字 (13pt bold, accent colour)
   說明補充文字 (12pt, #555555)
```

Position: `y=4.65`, `h=0.50` — fits above the ADATA slide's bottom branding zone (`y > 5.35`).

## Light Fill Colours (by section)

| Section | Fill colour |
|---------|------------|
| §1 Blue | `EEF4FF` |
| §2 Green | `EAFAE9` |
| §3 Orange | `FFF5E8` |
| §4 Magenta | `FFE8FF` |

## pptxgenjs Code

```javascript
const ACCENT     = "5097FF"; // replace with section colour
const LIGHT_FILL = "EEF4FF"; // replace per section (see table above)

// Rounded rectangle band
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.45, y: 4.65, w: 9.1, h: 0.50,
  fill: { color: LIGHT_FILL }, line: { color: ACCENT, pt: 0.5 },
  rectRadius: 0.06
});

// Primary note text
slide.addText("● 說明 / 注意事項 / 風險提示文字", {
  x: 0.60, y: 4.70, w: 8.8, h: 0.22,
  fontFace: "Arial", fontSize: 13, bold: true, color: ACCENT,
  valign: "middle", margin: 0
});

// Secondary note text (optional)
slide.addText("補充說明或次要資訊", {
  x: 0.60, y: 4.92, w: 8.8, h: 0.20,
  fontFace: "Arial", fontSize: 12, color: "555555",
  valign: "top", margin: 0
});
```

## Notes

- Keep total band height at `0.50"` to avoid encroaching on the ADATA branding strip below `y=5.35`.
- Omit the secondary text line if only a single note is needed (`h=0.50` is enough for one line at 13 pt).
- The `●` bullet is a literal character in the text string — do not use pptxgenjs `bullet: true` for note bands.
