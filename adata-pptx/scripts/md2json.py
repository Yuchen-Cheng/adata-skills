"""
Convert a Markdown content file into slides.json for edit_slides.py.

Usage:
    python scripts/md2json.py content.md [slides.json]

Markdown format:

    ---
    title:
      - Line 1
      - Line 2
    subtitle: Subtitle text
    date: 2026/04/24          # optional — defaults to today
    ---

    ## Section Title
    - Subtopic A
    - Subtopic B
    - Subtopic C

    ### Slide Title
    > Slide subtitle

    - Bullet item 1
    - Bullet item 2

    ### Another Slide
    > Another subtitle

    1. Numbered item 1
    2. Numbered item 2

Rules:
    - ## heading  → section divider slide
    - Unordered list items after ## → divider subtitles (max 3)
    - ### heading → content slide
    - Blockquote (> ) after ### → content slide subtitle
    - Unordered list (- ) → bullet body items  (<a:buChar>)
    - Ordered list (1. ) → numbered body items (<a:buAutoNum>)
    - Plain text lines → plain paragraphs (no bullet)
"""

import json
import pathlib
import re
import sys

# Template slide mapping: section_index → (divider, content_base)
_SECTION_MAP = [
    ("slide3.xml", "slide4.xml"),
    ("slide5.xml", "slide6.xml"),
    ("slide7.xml", "slide8.xml"),
    ("slide9.xml", "slide10.xml"),
]
_FIRST_DUP_ID = 12  # duplicated slides start from slide12.xml


# ── Frontmatter parser ─────────────────────────────────────────

def _parse_frontmatter(lines):
    """Parse simple YAML-like frontmatter between --- markers.

    Returns (dict, next_line_index).
    Supports scalar values and indented list values.
    """
    if not lines or lines[0].strip() != "---":
        return {}, 0

    result = {}
    i = 1
    current_key = None
    current_list = None

    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Indented list item under a key:  "  - value"
        if re.match(r"^\s+- ", line) and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip())
            result[current_key] = current_list
            i += 1
            continue

        # Key: value
        if ":" in stripped and not stripped.startswith("-"):
            current_list = None
            key, _, val = stripped.partition(":")
            current_key = key.strip()
            val = val.strip()
            if val:
                result[current_key] = val
            # else: value may come as indented list items below

        i += 1

    return result, min(i + 1, len(lines))


# ── Table parser ──────────────────────────────────────────────

def _parse_table_lines(raw_lines):
    """Convert pipe-table lines to {"header": [...], "rows": [[...]]}.

    Recognises the separator row (---|---) and discards it.
    """
    header = []
    rows   = []
    for ln in raw_lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        # Separator row: all cells match -+ pattern
        if all(re.match(r"^-+$", c) for c in cells if c):
            continue
        if not header:
            header = cells
        else:
            rows.append(cells)
    return {"header": header, "rows": rows}


# ── Flowchart parser ───────────────────────────────────────────

def _parse_flowchart_lines(block_lines):
    """Convert flowchart DSL lines to flowchart JSON dict.

    First line (after the fence opener) may be the direction: TB or LR.
    Node definition: shape:id:text
    Edge definition: id1->id2  or  id1->id2:label
    """
    nodes     = []
    edges     = []
    direction = "TB"
    seen_ids  = set()

    for ln in block_lines:
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue

        # Direction line (TB or LR, optionally after "flowchart ")
        if re.match(r"^(TB|LR)$", ln, re.I):
            direction = ln.upper()
            continue

        # Edge: id1->id2 or id1->id2:label
        edge_m = re.match(r"^(\w+)\s*->\s*(\w+)(?::(.+))?$", ln)
        if edge_m:
            e = {"from": edge_m.group(1), "to": edge_m.group(2)}
            if edge_m.group(3):
                e["label"] = edge_m.group(3).strip()
            edges.append(e)
            continue

        # Node: shape:id:text
        node_m = re.match(r"^(\w+):(\w+):(.+)$", ln)
        if node_m:
            nid = node_m.group(2)
            if nid not in seen_ids:
                seen_ids.add(nid)
                nodes.append({
                    "id":    nid,
                    "shape": node_m.group(1),
                    "text":  node_m.group(3).strip(),
                })
            continue

    return {"direction": direction, "nodes": nodes, "edges": edges}


# ── Markdown body parser ───────────────────────────────────────

def _parse_body_line(line):
    """Classify a body line as bullet, number, or plain, with indent level.

    Indentation is calculated from leading spaces:
      0 spaces = level 0,  2 spaces = level 1,  4 spaces = level 2, etc.
    """
    # Measure leading whitespace for indent level
    stripped = line.lstrip()
    leading = len(line) - len(line.lstrip())
    level = leading // 2  # 2 spaces per indent level

    m = re.match(r"^(\d+)\.\s+(.+)", stripped)
    if m:
        return {"type": "number", "text": m.group(2), "level": level}
    if stripped.startswith("- "):
        return {"type": "bullet", "text": stripped[2:].strip(), "level": level}
    return {"type": "plain", "text": stripped, "level": level}


# ── Main parser ────────────────────────────────────────────────

def parse_markdown(text):
    """Parse markdown content file into (cover, sections).

    Returns:
        cover: dict with title_lines, subtitle, date
        sections: list of {title, subtitles, slides: [{title, subtitle, body}]}
    """
    lines = text.split("\n")

    # Frontmatter → cover
    fm, i = _parse_frontmatter(lines)
    cover = {}
    if "title" in fm:
        t = fm["title"]
        cover["title_lines"] = t if isinstance(t, list) else [t]
    if "subtitle" in fm:
        cover["subtitle"] = fm["subtitle"]
    if "date" in fm:
        cover["date"] = fm["date"]

    # Parse sections and slides
    sections = []
    cur_sec = None
    cur_slide = None
    in_divider_subs = False

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        # Section divider: ## Title  (but not ### )
        if re.match(r"^##(?!#)\s+", stripped):
            if cur_slide and cur_sec:
                cur_sec["slides"].append(cur_slide)
                cur_slide = None
            cur_sec = {
                "title": re.sub(r"^##\s+", "", stripped),
                "subtitles": [],
                "slides": [],
            }
            sections.append(cur_sec)
            in_divider_subs = True
            i += 1
            continue

        # Content slide: ### Title
        if stripped.startswith("### "):
            if cur_slide and cur_sec:
                cur_sec["slides"].append(cur_slide)
            cur_slide = {
                "title": stripped[4:].strip(),
                "subtitle": "",
                "body": [],
            }
            in_divider_subs = False
            i += 1
            continue

        # Subtitle (blockquote) — only if no body items yet
        if (
            stripped.startswith("> ")
            and cur_slide is not None
            and not cur_slide["body"]
        ):
            cur_slide["subtitle"] = stripped[2:].strip()
            in_divider_subs = False
            i += 1
            continue

        # ── Flowchart fenced block  ```flowchart [TB|LR]
        if stripped.startswith("```flowchart") and cur_slide is not None:
            # Collect lines until closing ```
            direction_hint = stripped[len("```flowchart"):].strip().upper()
            block = []
            if direction_hint in ("TB", "LR"):
                block.append(direction_hint)
            i += 1
            while i < len(lines):
                bl = lines[i].rstrip()
                if bl.strip() == "```":
                    i += 1
                    break
                block.append(bl)
                i += 1
            cur_slide["flowchart"] = _parse_flowchart_lines(block)
            in_divider_subs = False
            continue

        # ── Markdown pipe table  | col | col |
        if stripped.startswith("|") and cur_slide is not None:
            table_lines = []
            while i < len(lines) and lines[i].rstrip().strip().startswith("|"):
                table_lines.append(lines[i].rstrip())
                i += 1
            cur_slide["table"] = _parse_table_lines(table_lines)
            in_divider_subs = False
            continue

        # Divider subtitles (- items right after ##, before any ###)
        if in_divider_subs and stripped.startswith("- ") and cur_sec is not None:
            cur_sec["subtitles"].append(stripped[2:].strip())
            i += 1
            continue

        # Body content items
        if cur_slide is not None and stripped:
            cur_slide["body"].append(_parse_body_line(line))
            in_divider_subs = False

        i += 1

    # Flush last slide
    if cur_slide and cur_sec:
        cur_sec["slides"].append(cur_slide)

    return cover, sections


# ── JSON builder ───────────────────────────────────────────────

def build_json(cover, sections):
    """Build slides.json structure from parsed content.

    Returns (result_dict, dup_commands).
    dup_commands: list of base slide filenames to duplicate.
    Supports unlimited sections — sections beyond 4 duplicate template
    pairs with cycling accent colours (Blue→Green→Orange→Magenta).
    """
    result = {}
    if cover:
        result["cover"] = cover
    if sections:
        result["agenda"] = {"items": [s["title"] for s in sections]}

    dividers = {}
    contents = {}
    dup_commands = []
    slide_order = ["slide1.xml", "slide2.xml"]  # cover + agenda
    next_dup_id = _FIRST_DUP_ID

    for sec_idx, section in enumerate(sections):
        if sec_idx < len(_SECTION_MAP):
            # Use built-in template pair
            div_file, content_base = _SECTION_MAP[sec_idx]
        else:
            # Cycle through template pairs to preserve accent colours
            template_idx = sec_idx % len(_SECTION_MAP)
            template_div, template_content = _SECTION_MAP[template_idx]

            div_file = f"slide{next_dup_id}.xml"
            dup_commands.append(template_div)
            next_dup_id += 1

            content_base = f"slide{next_dup_id}.xml"
            dup_commands.append(template_content)
            next_dup_id += 1

        dividers[div_file] = {
            "title": section["title"],
            "subtitles": section["subtitles"][:3],
        }
        slide_order.append(div_file)

        for sl_idx, slide in enumerate(section["slides"]):
            if sl_idx == 0:
                slide_file = content_base
            else:
                slide_file = f"slide{next_dup_id}.xml"
                if sec_idx < len(_SECTION_MAP):
                    dup_commands.append(content_base)
                else:
                    template_idx = sec_idx % len(_SECTION_MAP)
                    dup_commands.append(_SECTION_MAP[template_idx][1])
                next_dup_id += 1

            contents[slide_file] = slide
            slide_order.append(slide_file)

    slide_order.append("slide11.xml")  # closing

    result["dividers"] = dividers
    result["contents"] = contents
    result["slide_order"] = slide_order
    return result, dup_commands


# ── CLI ────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python md2json.py <content.md> [slides.json]")
        sys.exit(1)

    md_path = pathlib.Path(sys.argv[1])
    json_path = (
        pathlib.Path(sys.argv[2]) if len(sys.argv) >= 3 else pathlib.Path("slides.json")
    )

    text = md_path.read_text(encoding="utf-8")
    cover, sections = parse_markdown(text)
    result, dup_commands = build_json(cover, sections)

    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Created {json_path}")

    # Summary
    n = 2  # cover + agenda
    for sec in sections:
        n += 1 + len(sec["slides"])  # divider + content slides
    n += 1  # closing
    print(f"Slides: {n} (cover + agenda + {len(sections)} sections + closing)")

    if dup_commands:
        print(f"\nDuplicate commands ({len(dup_commands)}):")
        for base in dup_commands:
            print(f"  python scripts/add_slide.py unpacked/ {base}")

    unused = list(range(len(sections), min(len(sections), 4), 1))
    if len(sections) < 4:
        unused = list(range(len(sections), 4))
    else:
        unused = []
    if unused:
        print(f"\nDelete unused section pairs:")
        for idx in unused:
            d, c = _SECTION_MAP[idx]
            print(f"  {d}, {c}")


if __name__ == "__main__":
    main()
