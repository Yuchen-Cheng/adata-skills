"""
Bulk-edit ADATA slide content from a JSON data file.

Usage:
    python scripts/edit_slides.py unpacked/ slides.json [output_filename.pptx]

The JSON file describes each slide edit. Example:

{
  "cover": {
    "title_lines": ["Line 1", "Line 2"],
    "subtitle": "Subtitle text",
    "date": "2025 / 10 / 24"  // optional — defaults to today
  },
  "agenda": {
    "items": ["Section One", "Section Two", "Section Three", "Section Four"]
  },
  "dividers": {
    "slide3.xml": {
      "title": "Section Title",
      "subtitles": ["Sub 1", "Sub 2", "Sub 3"]
    }
  },
  "contents": {
    "slide4.xml": {
      "title": "Main Title",
      "subtitle": "Subtitle",
      "body": "Line 1\\nLine 2\\nLine 3"
    }
  }
}

Notes:
- Use \\n in body text to separate bullet lines.
- Chinese characters can be literal UTF-8 or XML entity encoded (&#xNNNN;).

- Run AFTER structural edits (add_slide, reorder) and codec fixes.
"""

import html
import json
import pathlib
import re
import sys
from datetime import date

# Flowchart / table renderers (same package)
try:
    from flowchart import render_flowchart, render_table
except ImportError:
    import importlib.util, pathlib as _pl
    _spec = importlib.util.spec_from_file_location(
        "flowchart",
        _pl.Path(__file__).parent / "flowchart.py"
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    render_flowchart = _mod.render_flowchart
    render_table     = _mod.render_table


def read_xml(slides_dir: pathlib.Path, filename: str) -> str:
    return (slides_dir / filename).read_text(encoding="utf-8")


def write_xml(slides_dir: pathlib.Path, filename: str, content: str):
    (slides_dir / filename).write_text(content, encoding="utf-8")


def replace_text(xml: str, old: str, new: str) -> str:
    """Replace first occurrence of <a:t>old</a:t> with <a:t>new</a:t>."""
    return xml.replace(f"<a:t>{old}</a:t>", f"<a:t>{html.escape(new)}</a:t>", 1)


# ── Cover helpers ──────────────────────────────────────────────

# The template cover title is a multi-run block:
#   2026 / ADATA BRAND / PPT Template
# We match the whole block and replace it.
_COVER_TITLE_RE = re.compile(
    r"(<a:p>\s*<a:pPr[^/]*/>\s*)"  # opening <a:p> + <a:pPr/>
    r"((?:<a:r>.*?</a:r>\s*|<a:br>.*?</a:br>\s*)*)"  # runs + breaks
    r"(<a:endParaRPr[^/]*/>\s*</a:p>)",  # closing
    re.DOTALL,
)

# The template date block: "2026 / 01 / 01"
_COVER_DATE_RUNS = re.compile(
    r"(<a:t>)2026(</a:t>.*?<a:t>)(.*?)(</a:t>.*?<a:t>)01(</a:t>.*?<a:t>)(.*?)(</a:t>.*?<a:t>)01(</a:t>)",
    re.DOTALL,
)


def _make_title_runs(lines: list[str]) -> str:
    """Build <a:r>...<a:br/>...<a:r> runs for cover title lines."""
    parts = []
    for i, line in enumerate(lines):
        lang = "en-US" if all(ord(c) < 0x2E80 for c in line) else "zh-TW"
        alt = "zh-TW" if lang == "en-US" else "en-US"
        parts.append(
            f'<a:r>\n'
            f'              <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
            f'              <a:t>{html.escape(line)}</a:t>\n'
            f'            </a:r>'
        )
        if i < len(lines) - 1:
            parts.append(
                f'<a:br>\n'
                f'              <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
                f'            </a:br>'
            )
    return "\n            ".join(parts)


def edit_cover(slides_dir: pathlib.Path, data: dict):
    xml = read_xml(slides_dir, "slide1.xml")

    # Title — replace multi-run block
    if "title_lines" in data:
        runs = _make_title_runs(data["title_lines"])
        # Find the ctrTitle shape's <a:p> and replace inner runs.
        # The template may or may not have <a:pPr/> after <a:p>.
        old_runs_pattern = re.compile(
            r"(<p:sp>.*?<p:ph type=\"ctrTitle\"[^/]*/>"
            r".*?<a:p>"
            r"(?:\s*<a:pPr[^/]*/>\s*)?)"          # optional <a:pPr/>
            r"(.*?)"
            r"(\s*<a:endParaRPr[^/]*/>\s*</a:p>)",
            re.DOTALL,
        )
        m = old_runs_pattern.search(xml)
        if m:
            xml = xml[:m.start(2)] + "\n            " + runs + "\n            " + xml[m.end(2):]

    # Subtitle
    if "subtitle" in data:
        xml = replace_text(xml, "Subtitle", data["subtitle"])

    # Date — template has "2026 / 01 / 01" split across many runs
    # Default to today's date if not specified
    date_str = data.get("date") or date.today().strftime("%Y / %m / %d")
    if date_str:
        # Parse "YYYY / MM / DD" or "YYYY/MM/DD"
        parts = [p.strip() for p in date_str.replace("/", " / ").split("/")]
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) == 3:
            year, month, day = parts
            xml = xml.replace("<a:t>2026</a:t>", f"<a:t>{year}</a:t>", 1)
            # Replace the two "01" values in the date area
            # The date area has: year / month / day where month and day are "01"
            # Replace first "01" → month, second "01" → day
            count = 0
            result = []
            i = 0
            target = "<a:t>01</a:t>"
            while i < len(xml):
                if xml[i:i+len(target)] == target and count < 2:
                    replacement = f"<a:t>{month}</a:t>" if count == 0 else f"<a:t>{day}</a:t>"
                    result.append(replacement)
                    i += len(target)
                    count += 1
                else:
                    result.append(xml[i])
                    i += 1
            xml = "".join(result)

    write_xml(slides_dir, "slide1.xml", xml)
    print("slide1.xml done (cover)")


# ── Agenda helpers ─────────────────────────────────────────────

_AGENDA_BULLET_PPR = (
    '<a:pPr marL="268288" marR="0" lvl="0" indent="-268288" algn="l" '
    'defTabSz="914400" rtl="0" eaLnBrk="1" fontAlgn="auto" '
    'latinLnBrk="0" hangingPunct="1">\n'
    "              <a:lnSpc>\n"
    '                <a:spcPct val="90000"/>\n'
    "              </a:lnSpc>\n"
    "              <a:spcBef>\n"
    '                <a:spcPts val="1000"/>\n'
    "              </a:spcBef>\n"
    "              <a:spcAft>\n"
    '                <a:spcPts val="0"/>\n'
    "              </a:spcAft>\n"
    "              <a:buClrTx/>\n"
    "              <a:buSzTx/>\n"
    '              <a:buFont typeface="Arial" panose="020B0604020202020204" '
    'pitchFamily="34" charset="0"/>\n'
    '              <a:buChar char="&#x2022;"/>\n'
    "              <a:tabLst/>\n"
    "              <a:defRPr/>\n"
    "            </a:pPr>"
)


def edit_agenda(slides_dir: pathlib.Path, data: dict):
    xml = read_xml(slides_dir, "slide2.xml")

    items = data.get("items", [])
    # Replace existing "Subtitle" placeholders first (template has 3)
    for item in items[:3]:
        lang = "en-US" if all(ord(c) < 0x2E80 for c in item) else "zh-TW"
        xml = replace_text(xml, "Subtitle", item)

    # For items beyond 3, insert before the trailing empty paragraph
    if len(items) > 3:
        extra_paras = []
        for item in items[3:]:
            lang = "zh-TW" if any(ord(c) >= 0x2E80 for c in item) else "en-US"
            alt = "en-US" if lang == "zh-TW" else "zh-TW"
            extra_paras.append(
                f"          <a:p>\n"
                f"            {_AGENDA_BULLET_PPR}\n"
                f'            <a:r>\n'
                f'              <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
                f"              <a:t>{item}</a:t>\n"
                f"            </a:r>\n"
                f"          </a:p>"
            )
        insertion = "\n".join(extra_paras)
        # Insert before the trailing empty paragraph
        trailing = '          <a:p>\n            <a:pPr lvl="0"/>\n            <a:endParaRPr'
        xml = xml.replace(trailing, insertion + "\n" + trailing, 1)

    write_xml(slides_dir, "slide2.xml", xml)
    print("slide2.xml done (agenda)")


# ── Section divider helper ─────────────────────────────────────

def edit_divider(slides_dir: pathlib.Path, filename: str, data: dict):
    xml = read_xml(slides_dir, filename)
    xml = replace_text(xml, "Section Title", data["title"])
    for sub in data.get("subtitles", []):
        xml = replace_text(xml, "Subtitle", sub)
    write_xml(slides_dir, filename, xml)
    print(f"{filename} done (divider)")


# ── Content slide helper ───────────────────────────────────────

# Body bullet paragraph properties (built-in 項目符號)
# Standard PowerPoint margins per indent level (EMU)
_LEVEL_MARL = [228600, 685800, 1143000, 1600200]  # 0.25in, 0.75in, 1.25in, 1.75in
_INDENT     = -228600  # hanging indent


def _body_bullet_ppr(level: int = 0) -> str:
    """Generate <a:pPr> for a bullet item at the given indent level."""
    marL = _LEVEL_MARL[min(level, len(_LEVEL_MARL) - 1)]
    lvl_attr = f' lvl="{level}"' if level > 0 else ''
    return (
        f'<a:pPr marL="{marL}" indent="{_INDENT}"{lvl_attr}>\n'
        '                <a:buFont typeface="Arial" panose="020B0604020202020204" '
        'pitchFamily="34" charset="0"/>\n'
        '                <a:buChar char="&#x2022;"/>\n'
        '              </a:pPr>'
    )


def _body_number_ppr(level: int = 0) -> str:
    """Generate <a:pPr> for a numbered item at the given indent level."""
    marL = _LEVEL_MARL[min(level, len(_LEVEL_MARL) - 1)]
    lvl_attr = f' lvl="{level}"' if level > 0 else ''
    return (
        f'<a:pPr marL="{marL}" indent="{_INDENT}"{lvl_attr}>\n'
        '                <a:buAutoNum type="arabicPeriod"/>\n'
        '              </a:pPr>'
    )


def _body_plain_ppr(level: int = 0) -> str:
    """Generate <a:pPr> for a plain (no-bullet) item at the given indent level."""
    if level == 0:
        return ''
    marL = _LEVEL_MARL[min(level, len(_LEVEL_MARL) - 1)]
    return (
        f'<a:pPr marL="{marL}" indent="0" lvl="{level}">\n'
        '                <a:buNone/>\n'
        '              </a:pPr>'
    )


def _make_body_paragraphs(items: list) -> str:
    """Generate <a:p> XML elements for body content with bullet/numbering and indent levels."""
    paras = []
    for item in items:
        if isinstance(item, str):
            text, item_type, level = item, "bullet", 0
        else:
            text = item["text"]
            item_type = item.get("type", "bullet")
            level = item.get("level", 0)

        text = html.escape(text)
        lang = "zh-TW" if any(ord(c) >= 0x2E80 for c in text) else "en-US"
        alt = "en-US" if lang == "zh-TW" else "zh-TW"

        if item_type == "number":
            ppr = _body_number_ppr(level)
        elif item_type == "bullet":
            ppr = _body_bullet_ppr(level)
        else:
            ppr = _body_plain_ppr(level)

        if ppr:
            # Numbered items get a tab run inserted before the text to indent content
            tab_run = (
                '              <a:r>\n'
                f'                <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
                '                <a:t>\t</a:t>\n'
                '              </a:r>\n'
            ) if item_type == "number" else ""
            para = (
                f'<a:p>\n'
                f'              {ppr}\n'
                f'{tab_run}'
                f'              <a:r>\n'
                f'                <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
                f'                <a:t>{text}</a:t>\n'
                f'              </a:r>\n'
                f'            </a:p>'
            )
        else:
            para = (
                f'<a:p>\n'
                f'              <a:r>\n'
                f'                <a:rPr lang="{lang}" altLang="{alt}" dirty="0"/>\n'
                f'                <a:t>{text}</a:t>\n'
                f'              </a:r>\n'
                f'            </a:p>'
            )
        paras.append(para)

    return "\n            ".join(paras)


def _replace_body_paragraph(xml: str, items: list) -> str:
    """Replace the <a:p> containing <a:t>Text</a:t> with structured paragraphs."""
    marker = "<a:t>Text</a:t>"
    pos = xml.find(marker)
    if pos == -1:
        return xml

    # Find enclosing <a:p>...</a:p>
    p_open = xml.rfind("<a:p>", 0, pos)
    if p_open == -1:
        p_open = xml.rfind("<a:p ", 0, pos)
    if p_open == -1:
        return xml

    p_close = xml.find("</a:p>", pos)
    if p_close == -1:
        return xml
    p_close += len("</a:p>")

    new_paras = _make_body_paragraphs(items)
    return xml[:p_open] + new_paras + xml[p_close:]


_KNOWN_ACCENTS = {"5097FF", "19C711", "FF9000", "FF47FF"}


def _accent_from_xml(xml: str) -> str:
    """Detect section accent colour from the slide XML (title lstStyle)."""
    for m in re.finditer(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', xml):
        if m.group(1).upper() in _KNOWN_ACCENTS:
            return m.group(1)
    return "5097FF"


def edit_content(slides_dir: pathlib.Path, filename: str, data: dict):
    xml = read_xml(slides_dir, filename)
    xml = replace_text(xml, "Main Title", data["title"])
    xml = replace_text(xml, "Subtitle", data.get("subtitle", ""))

    if "flowchart" in data:
        # Clear body placeholder text, then inject native PPT shapes
        xml = replace_text(xml, "Text", "")
        accent = _accent_from_xml(xml)
        xml = render_flowchart(xml, data["flowchart"], accent)

    elif "table" in data:
        # Clear body placeholder text, then inject native PPT table
        xml = replace_text(xml, "Text", "")
        accent = _accent_from_xml(xml)
        xml = render_table(xml, data["table"], accent)

    else:
        body = data.get("body", [])
        if isinstance(body, str):
            # Legacy: newline-separated string → bullet items
            items = [{"type": "bullet", "text": line}
                     for line in body.split("\n") if line.strip()]
        elif isinstance(body, list):
            items = body
        else:
            items = []

        if items:
            xml = _replace_body_paragraph(xml, items)
        else:
            xml = replace_text(xml, "Text", "")

    write_xml(slides_dir, filename, xml)
    print(f"{filename} done (content)")


# ── Main ───────────────────────────────────────────────────────

def _update_slide_count(unpacked: pathlib.Path):
    """Update <Slides>N</Slides> in docProps/app.xml to match presentation.xml."""
    pres_xml = (unpacked / "ppt" / "presentation.xml").read_text(encoding="utf-8")
    count = len(re.findall(r"<p:sldId\b", pres_xml))

    app_path = unpacked / "docProps" / "app.xml"
    if not app_path.exists():
        return
    app_xml = app_path.read_text(encoding="utf-8")
    app_xml = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{count}</Slides>", app_xml)
    app_path.write_text(app_xml, encoding="utf-8")
    print(f"docProps/app.xml updated: <Slides>{count}</Slides>")


def _reorder_slides(unpacked: pathlib.Path, slide_order: list):
    """Reorder <p:sldId> entries in presentation.xml to match slide_order.

    Entries not in slide_order are removed (unused template section pairs).
    """
    pres_path = unpacked / "ppt" / "presentation.xml"
    pres_content = pres_path.read_text(encoding="utf-8")

    # Build rId -> slide filename map from .rels
    rels_path = unpacked / "ppt" / "_rels" / "presentation.xml.rels"
    rels_content = rels_path.read_text(encoding="utf-8")
    rid_to_slide = {}
    for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="slides/([^"]+)"', rels_content):
        rid_to_slide[m.group(1)] = m.group(2)
    slide_to_rid = {v: k for k, v in rid_to_slide.items()}

    # Build rId -> full sldId tag map
    tag_map = {}
    for m in re.finditer(r'(<p:sldId id="\d+" r:id="(rId\d+)"/>)', pres_content):
        tag_map[m.group(2)] = m.group(1)

    # Build new sldIdLst content in the desired order
    new_entries = []
    for slide in slide_order:
        rid = slide_to_rid.get(slide)
        if rid and rid in tag_map:
            new_entries.append(f"    {tag_map[rid]}")

    new_sldIdLst = "\n".join(new_entries)

    pres_content = re.sub(
        r"(<p:sldIdLst>).*?(</p:sldIdLst>)",
        r"\1\n" + new_sldIdLst + r"\n  \2",
        pres_content,
        flags=re.DOTALL,
    )

    pres_path.write_text(pres_content, encoding="utf-8")
    print(f"Reordered {len(new_entries)} slides in presentation.xml")


def main():
    if len(sys.argv) < 3:
        print("Usage: python edit_slides.py <unpacked_dir> <slides.json> [output_filename.pptx]")
        print("       python edit_slides.py unpacked/ slides.json My-Deck.pptx")
        sys.exit(1)

    unpacked = pathlib.Path(sys.argv[1])
    slides_dir = unpacked / "ppt" / "slides"
    data_file = pathlib.Path(sys.argv[2])
    output_filename = sys.argv[3] if len(sys.argv) >= 4 else "output.pptx"

    data = json.loads(data_file.read_text(encoding="utf-8"))

    if "cover" in data:
        edit_cover(slides_dir, data["cover"])

    if "agenda" in data:
        edit_agenda(slides_dir, data["agenda"])

    for filename, d in data.get("dividers", {}).items():
        edit_divider(slides_dir, filename, d)

    for filename, d in data.get("contents", {}).items():
        edit_content(slides_dir, filename, d)

    if "slide_order" in data:
        _reorder_slides(unpacked, data["slide_order"])

    _update_slide_count(unpacked)

    print(f"\nAll slides edited successfully!")
    print(f"Output filename: {output_filename}")


if __name__ == "__main__":
    main()
