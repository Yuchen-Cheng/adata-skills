# Editing Presentations

## Source Conversion Details

> **Use this section when the source is an existing PPTX file.** Read [SKILL.md → Source Conversion Mode](SKILL.md#source-conversion-mode保留內容只改樣式) first for the overview.

### Step-by-step: Applying ADATA Style to a Source PPTX

#### 1. Unpack both files

```bash
python scripts/office/unpack.py source.pptx source-unpacked/
python scripts/office/unpack.py adata-template/adata-template.pptx adata-unpacked/
```

#### 2. Replace the theme

The theme file controls all scheme-based colors. Replacing it makes every element that references a theme color automatically adopt ADATA branding.

```bash
# Windows (PowerShell)
Copy-Item adata-unpacked/ppt/theme/theme1.xml source-unpacked/ppt/theme/theme1.xml -Force

# Linux/macOS
cp adata-unpacked/ppt/theme/theme1.xml source-unpacked/ppt/theme/theme1.xml
```

> After this step, pack a test copy and open in PowerPoint to see how much changed automatically. Most scheme-colored shapes will already be ADATA colors.

#### 3. Run the conversion script

```bash
python scripts/convert_to_adata.py source-unpacked/
```

The script handles:
- Title-level fonts → `Arial Black` (detects title placeholders by `type="title"` or `type="ctrTitle"`)
- Background fills on dark-bg slides → `#0E2841`
- Hardcoded dark blue text on light slides → `#0E2841`
- Hardcoded white text on dark slides → `#FFFFFF` (no change needed; leaves as-is)
- Reports a summary of all changes made

#### 4. Manually inspect and fix remaining issues

After running the script, some slides may need hand-editing. Common cases:

**Slide classified as wrong background type:**

The script uses slide index heuristics (slide 1 = dark, last slide = dark, everything else = light). Override by editing `<p:bg>` in the specific slide XML:

Dark background:
```xml
<p:bg>
  <p:bgPr>
    <a:solidFill>
      <a:srgbClr val="0E2841"/>
    </a:solidFill>
  </p:bgPr>
</p:bg>
```

Light background (remove explicit `<p:bg>` entirely — let the slide master handle it):
```xml
<!-- Delete the entire <p:bg>...</p:bg> block -->
```

**Title font not changed (font defined in slide master, not in slide XML):**

These are already controlled by the ADATA slide master/layout after theme replacement — no action needed. If you see a non-Arial-Black title after visual QA, check if the slide XML has an explicit override:

```xml
<!-- Find and remove or update this in the title run: -->
<a:rPr ...>
  <a:latin typeface="SomeOtherFont"/>   <!-- ← change to Arial Black or delete -->
</a:rPr>
```

**Hardcoded accent color that was not replaced:**

Find the color in slide XML: search for `<a:srgbClr val="XXXXXX"/>` and replace manually using the mapping table in SKILL.md.

**Low-contrast text after background change:**

If a slide background was changed to dark (`#0E2841`) but text remains dark:

```xml
<!-- Change text run color to white: -->
<a:solidFill>
  <a:srgbClr val="FFFFFF"/>
</a:solidFill>
```

#### 5. Clean and pack

```bash
python scripts/clean.py source-unpacked/
python scripts/office/pack.py source-unpacked/ output-adata.pptx --original source.pptx
```

---

## Template-Based Workflow

When using an existing presentation as a template:

1. **Analyze existing slides**:
   ```bash
   python scripts/thumbnail.py template.pptx
   python -m markitdown template.pptx
   ```
   Review `thumbnails.jpg` to see layouts, and markitdown output to see placeholder text.

2. **Plan slide mapping**: For each content section, choose a template slide.

   ⚠️ **USE VARIED LAYOUTS** — monotonous presentations are a common failure mode. Don't default to basic title + bullet slides. Actively seek out:
   - Multi-column layouts (2-column, 3-column)
   - Image + text combinations
   - Full-bleed images with text overlay
   - Quote or callout slides
   - Section dividers
   - Stat/number callouts
   - Icon grids or icon + text rows

   **Avoid:** Repeating the same text-heavy layout for every slide.

   Match content type to layout style (e.g., key points → bullet slide, team info → multi-column, testimonials → quote slide).

3. **Unpack**: `python scripts/office/unpack.py template.pptx unpacked/`

4. **Build presentation** (do this yourself, not with subagents):
   - Delete unwanted slides (remove from `<p:sldIdLst>`)
   - Duplicate slides you want to reuse (`add_slide.py`)
   - Reorder slides in `<p:sldIdLst>`
   - **Complete all structural changes before step 5**

5. **Edit content**: Update text in each `slide{N}.xml`.
   **Use subagents here if available** — slides are separate XML files, so subagents can edit in parallel.

6. **Clean**: `python scripts/clean.py unpacked/`

7. **Pack**: `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

---

## Scripts

| Script | Purpose |
|--------|---------|
| `unpack.py` | Extract and pretty-print PPTX |
| `add_slide.py` | Duplicate slide or create from layout |
| `clean.py` | Remove orphaned files |
| `pack.py` | Repack with validation |
| `thumbnail.py` | Create visual grid of slides |

### unpack.py

```bash
python scripts/office/unpack.py input.pptx unpacked/
```

Extracts PPTX, pretty-prints XML, escapes smart quotes.

### add_slide.py

```bash
python scripts/add_slide.py unpacked/ slide2.xml      # Duplicate slide
python scripts/add_slide.py unpacked/ slideLayout2.xml # From layout
```

Prints `<p:sldId>` to add to `<p:sldIdLst>` at desired position.

### clean.py

```bash
python scripts/clean.py unpacked/
```

Removes slides not in `<p:sldIdLst>`, unreferenced media, orphaned rels.

### pack.py

```bash
python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

Validates, repairs, condenses XML, re-encodes smart quotes.

### thumbnail.py

```bash
python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]
```

Creates `thumbnails.jpg` with slide filenames as labels. Default 3 columns, max 12 per grid.

**Use for template analysis only** (choosing layouts). For visual QA, use `soffice` + `pdftoppm` to create full-resolution individual slide images—see SKILL.md.

---

## Slide Operations

Slide order is in `ppt/presentation.xml` → `<p:sldIdLst>`.

**Reorder**: Rearrange `<p:sldId>` elements.

**Delete**: Remove `<p:sldId>`, then run `clean.py`.

**Add**: Use `add_slide.py`. Never manually copy slide files—the script handles notes references, Content_Types.xml, and relationship IDs that manual copying misses.

---

## Editing Content

**Subagents:** If available, use them here (after completing step 4). Each slide is a separate XML file, so subagents can edit in parallel. In your prompt to subagents, include:
- The slide file path(s) to edit
- **"Use the Edit tool for all changes"**
- The formatting rules and common pitfalls below

For each slide:
1. Read the slide's XML
2. Identify ALL placeholder content—text, images, charts, icons, captions
3. Replace each placeholder with final content

**Use the Edit tool, not sed or Python scripts.** The Edit tool forces specificity about what to replace and where, yielding better reliability.

### Formatting Rules

- **Bold all headers, subheadings, and inline labels**: Use `b="1"` on `<a:rPr>`. This includes:
  - Slide titles
  - Section headers within a slide
  - Inline labels like (e.g.: "Status:", "Description:") at the start of a line
- **Never use unicode bullets (•)**: Use proper list formatting with `<a:buChar>` or `<a:buAutoNum>`
- **Bullet consistency**: Let bullets inherit from the layout. Only specify `<a:buChar>` or `<a:buNone>`.

---

## Common Pitfalls

### Template Adaptation

When source content has fewer items than the template:
- **Remove excess elements entirely** (images, shapes, text boxes), don't just clear text
- Check for orphaned visuals after clearing text content
- Run visual QA to catch mismatched counts

When replacing text with different length content:
- **Shorter replacements**: Usually safe
- **Longer replacements**: May overflow or wrap unexpectedly
- Test with visual QA after text changes
- Consider truncating or splitting content to fit the template's design constraints

**Template slots ≠ Source items**: If template has 4 team members but source has 3 users, delete the 4th member's entire group (image + text boxes), not just the text.

### Multi-Item Content

If source has multiple items (numbered lists, multiple sections), create separate `<a:p>` elements for each — **never concatenate into one string**.

**❌ WRONG** — all items in one paragraph:
```xml
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

**✅ CORRECT** — separate paragraphs with bold headers:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 2</a:t></a:r>
</a:p>
<!-- continue pattern -->
```

Copy `<a:pPr>` from the original paragraph to preserve line spacing. Use `b="1"` on headers.

### Smart Quotes

Handled automatically by unpack/pack. But the Edit tool converts smart quotes to ASCII.

**When adding new text with quotes, use XML entities:**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

| Character | Name | Unicode | XML Entity |
|-----------|------|---------|------------|
| `“` | Left double quote | U+201C | `&#x201C;` |
| `”` | Right double quote | U+201D | `&#x201D;` |
| `‘` | Left single quote | U+2018 | `&#x2018;` |
| `’` | Right single quote | U+2019 | `&#x2019;` |

### XML Special Characters

Any literal `<`, `>`, or `&` in text content **will break the XML** and cause PowerPoint to reject the file.
Always escape them before writing into `<a:t>`:

| Character | Escaped form |
|-----------|-------------|
| `<`       | `&lt;`      |
| `>`       | `&gt;`      |
| `&`       | `&amp;`     |
| `"`       | `&quot;`    |

Example: "latency < 0.1 ms & tested" → `latency &lt; 0.1 ms &amp; tested`

### Template Content Type (`.potx` → `.pptx`)

If the template file was originally a `.potx`, its `[Content_Types].xml` declares:

```xml
ContentType="application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
```

This causes `markitdown` (and some validators) to reject the file. Fix it immediately after unpacking:

```python
import re, pathlib

ct = pathlib.Path("unpacked/[Content_Types].xml")
ct.write_text(
    ct.read_text(encoding="utf-8").replace(
        "presentationml.template.main+xml",
        "presentationml.presentation.main+xml"
    ),
    encoding="utf-8"
)
```

Run this **before** any content editing.

### Stubborn Placeholder Text (`dirty="0"`)

Some slides have placeholder runs marked `dirty="0"` or with `<a:pPr lvl="0"/>`, which causes the text to survive a naive string-replace. If a placeholder still shows after editing, use a Python script to force-clear all text runs in the affected text box:

```python
import re, pathlib

xml = pathlib.Path("unpacked/ppt/slides/slideN.xml").read_text(encoding="utf-8")
# Target the specific txBody that still holds placeholder text and wipe its <a:t> nodes
xml = re.sub(r'(<a:t>)(PLACEHOLDER_TEXT)(</a:t>)', r'\1\3', xml)
pathlib.Path("unpacked/ppt/slides/slideN.xml").write_text(xml, encoding="utf-8")
```

Or, if the entire text box should be blank, remove all `<a:t>` content inside that `<p:txBody>`.

### Section Divider Subtitle Length

The section divider layout reserves a fixed-height box for subtitles. Long subtitles **wrap and overflow**:

- **Hard limit: ≤ 8 Chinese characters per subtitle line**
- If the source content is longer, abbreviate (e.g., "XPG GAMMIX S70 Blade 規格解析" → "S70 Blade 規格解析")
- Check wrapping in Visual QA — this issue is invisible in the XML

### Section Divider Title Font Size

Chinese section titles longer than ~6 characters may wrap inside the title box because the lstStyle font size is fixed at 6600 (66 pt). If the title wraps to 3+ lines:

1. Open `unpacked/ppt/slides/slideN.xml`
2. Find `<a:lstStyle>` inside the title `<p:txBody>`
3. Reduce the `<a:sz>` value (e.g., `val="6600"` → `val="5200"`)

Verify with Visual QA after changing.

### Cover Slide Date Placeholder

The cover slide contains a date field driven by `<p:fldType type="datetime"/>`. It auto-populates with today's date and **cannot be left as-is** if you want a specific date or no date.

To set a specific date, replace the `<a:fldId>` field element with a plain `<a:r>` run:

```xml
<!-- Remove this -->
<a:fldId .../>

<!-- Add this instead -->
<a:r>
  <a:rPr lang="zh-TW" .../>
  <a:t>2026 / 01</a:t>
</a:r>
```

To clear the date entirely, remove all `<a:r>` and `<a:fld>` elements from that `<a:p>` paragraph, leaving only `<a:pPr>` and `<a:endParaRPr>`.

### Other

- **Whitespace**: Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces
- **XML parsing**: Use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)
