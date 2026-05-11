"""
convert_to_adata.py — Apply ADATA brand styling to an unpacked source PPTX.

Usage:
    python scripts/convert_to_adata.py <unpacked_dir> [options]

Options:
    --dark-slides  N [N ...]   Slide indices (1-based) to treat as dark-background.
                               By default: slide 1 and the last slide are dark.
    --colors-only              Only remap hardcoded accent colors and title fonts.
                               Skip all background modifications. Use this when the
                               source already has ADATA-branded background images.
    --dry-run                  Print what would change without writing files.

What this script does:
  1. Replaces title-placeholder font → Arial Black
  2. Remaps common hardcoded accent colors to ADATA equivalents.
  3. On dark-background slides (unless --colors-only): replaces explicit background
     fill → #0E2841 and ensures text runs use #FFFFFF.
  4. On light-background slides (unless --colors-only): removes explicit solid-color
     background fills (blipFill image backgrounds are always preserved).

What this script does NOT do:
  - Replace the theme file (do that manually if the source theme is not ADATA).
  - Modify images, charts, or SmartArt interior colors.
  - Restructure or reorder slides.
"""

import argparse
import pathlib
import re
import sys

# ---------------------------------------------------------------------------
# ADATA brand colors
# ---------------------------------------------------------------------------
DARK_BG      = "0E2841"
WHITE        = "FFFFFF"
LIGHT_BG     = "FFFFFF"  # content slides default to white background
ADATA_BLUE   = "5097FF"
ADATA_GREEN  = "19C711"
ADATA_ORANGE = "FF9000"
ADATA_PINK   = "FF47FF"
ADATA_NAVY   = "0E2841"
ADATA_CYAN   = "5FE6FF"

# Hardcoded colors → ADATA equivalent
# Keys are lowercase 6-digit hex.  Add more mappings as needed.
COLOR_MAP = {
    # Common PMO/Office purple → ADATA magenta
    "6b2fa5": ADATA_PINK,
    "7030a0": ADATA_PINK,
    "6633cc": ADATA_PINK,
    "5c2d91": ADATA_PINK,
    # Light purple tints → light blue tint
    "eee5f7": "E0ECFF",
    "e8d5f5": "E0ECFF",
    "dccef2": "E0ECFF",
    # Custom blues → ADATA blue
    "1f77d0": ADATA_BLUE,
    "2f71b5": ADATA_BLUE,
    "0070c0": ADATA_BLUE,
    "4472c4": ADATA_BLUE,
    "2e75b6": ADATA_BLUE,
    # Custom greens → ADATA green
    "2ea561": ADATA_GREEN,
    "00b050": ADATA_GREEN,
    "70ad47": ADATA_GREEN,
    # Custom oranges → ADATA orange
    "e68a00": ADATA_ORANGE,
    "ed7d31": ADATA_ORANGE,
    "ff6600": ADATA_ORANGE,
    # Teal → ADATA cyan
    "0096a0": ADATA_CYAN,
    "00b0f0": ADATA_CYAN,
    # Deep blues / navies → ADATA navy
    "003366": DARK_BG,
    "003399": DARK_BG,
    "1f3864": DARK_BG,
    "1f497d": DARK_BG,
    "243f60": DARK_BG,
    "17375e": DARK_BG,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_SRGB_RE = re.compile(r'(<a:srgbClr\s+val=")([0-9a-fA-F]{6})(")', re.IGNORECASE)
_LATIN_RE = re.compile(r'(<a:latin\s[^>]*typeface=")[^"]*(")', re.IGNORECASE)
_LATIN_BARE_RE = re.compile(r'(<a:latin\s+typeface=")[^"]*(")', re.IGNORECASE)


def remap_colors(xml: str) -> tuple[str, int]:
    """Replace hardcoded colors using COLOR_MAP. Returns (new_xml, count)."""
    count = 0
    def _replacer(m):
        nonlocal count
        orig = m.group(2).lower()
        if orig in COLOR_MAP:
            count += 1
            return m.group(1) + COLOR_MAP[orig] + m.group(3)
        return m.group(0)
    new_xml = _SRGB_RE.sub(_replacer, xml)
    return new_xml, count


def apply_title_styling(xml: str, is_dark: bool) -> tuple[str, int]:
    """
    Apply ADATA title and subtitle styling to the appropriate shapes in a slide.

    Title detection (in priority order):
      1. <p:ph type="title"> or <p:ph type="ctrTitle"> — authoritative
      2. Shape with y-offset in top 30% of slide AND meaningful text
         (position heuristic for slides without proper title placeholders)

    Subtitle detection:
      <p:ph type="subTitle"> or <p:ph type="body"> with idx=1

    Skipped shapes: footers (ftr), datetime (dt), slideNum placeholders.

    Applied styling per background type:
      Dark slide  → Arial Black font + WHITE (#FFFFFF) text color
      Light slide → Arial Black font + NAVY (#0E2841) text color

    Subtitle on light slide → NAVY; subtitle on dark slide → WHITE.
    """
    title_color    = WHITE    if is_dark else ADATA_NAVY
    subtitle_color = WHITE    if is_dark else ADATA_NAVY
    count = 0

    sp_pattern    = re.compile(r'<p:sp\b.*?</p:sp>', re.DOTALL)
    ph_title_re   = re.compile(r'<p:ph\s[^>]*type="(title|ctrTitle)"', re.IGNORECASE)
    ph_sub_re     = re.compile(r'<p:ph\s[^>]*type="(subTitle|body)"', re.IGNORECASE)
    ph_skip_re    = re.compile(r'<p:ph\s[^>]*type="(ftr|dt|sldNum)"', re.IGNORECASE)
    ph_body_idx_re= re.compile(r'<p:ph\b[^>]*idx="([2-9]|\d{2,})"', re.IGNORECASE)
    off_y_re      = re.compile(r'<a:off\s[^>]*y="(\d+)"')
    rpr_fill_re   = re.compile(r'(<a:rPr\b.*?)(</a:rPr>)', re.DOTALL)
    solidfill_re  = re.compile(r'<a:solidFill>\s*<a:srgbClr val="[0-9a-fA-F]{6}"\s*/>\s*</a:solidFill>', re.DOTALL)
    # Standard widescreen slide height 6858000 EMU; top 30% ≈ 2057400
    TITLE_Y_LIMIT = 2057400

    def _set_run_color(sp_xml: str, color: str) -> str:
        """Replace or insert explicit text color in all <a:rPr> runs of a shape."""
        def patch_rpr(rm):
            rpr = rm.group(1)
            closing = rm.group(2)
            # Replace existing solidFill inside rPr
            new_rpr, n = solidfill_re.subn(
                f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>', rpr
            )
            if n == 0:
                # No solidFill present — inject one before the closing tag
                new_rpr = rpr + f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            return new_rpr + closing
        return rpr_fill_re.sub(patch_rpr, sp_xml)

    def style_shape(sp_xml: str, color: str) -> tuple[str, int]:
        """Apply Arial Black + color to a shape. Returns (new_xml, change_count)."""
        c = 0

        def fix_latin(lm):
            nonlocal c
            c += 1
            return lm.group(1) + "Arial Black" + lm.group(2)

        new_sp = _LATIN_RE.sub(fix_latin, sp_xml)
        new_sp = _LATIN_BARE_RE.sub(fix_latin, new_sp)
        new_sp = _set_run_color(new_sp, color)
        if new_sp != sp_xml:
            c = max(c, 1)
        return new_sp, c

    def process_sp(m):
        nonlocal count
        sp_xml = m.group(0)

        # Always skip footer/datetime/slideNum placeholders
        if ph_skip_re.search(sp_xml):
            return sp_xml

        # Classify shape
        if ph_title_re.search(sp_xml):
            role = "title"
        elif ph_sub_re.search(sp_xml) and not ph_body_idx_re.search(sp_xml):
            role = "subtitle"
        else:
            # Position heuristic: top 30% of slide, non-placeholder or unlabeled box
            pos_m = off_y_re.search(sp_xml)
            if pos_m and int(pos_m.group(1)) < TITLE_Y_LIMIT:
                # Must contain meaningful text (≥4 chars in at least one run)
                texts = re.findall(r'<a:t>([^<]{4,})</a:t>', sp_xml)
                if texts:
                    role = "title"
                else:
                    return sp_xml
            else:
                return sp_xml

        target_color = title_color if role == "title" else subtitle_color
        new_sp, c = style_shape(sp_xml, target_color)
        count += c
        return new_sp

    new_xml = sp_pattern.sub(process_sp, xml)
    return new_xml, count


def set_background_dark(xml: str) -> tuple[str, int]:
    """
    Replace or insert a dark (#0E2841) solid background fill on a slide.
    Targets the <p:bg> block inside <p:cSld>.
    """
    bg_block = (
        "<p:bg>"
        "<p:bgPr>"
        "<a:solidFill>"
        f"<a:srgbClr val=\"{DARK_BG}\"/>"
        "</a:solidFill>"
        "<a:effectLst/>"
        "</p:bgPr>"
        "</p:bg>"
    )

    existing_bg_re = re.compile(r'<p:bg\b.*?</p:bg>', re.DOTALL)

    if existing_bg_re.search(xml):
        new_xml, n = existing_bg_re.subn(bg_block, xml)
        return new_xml, n
    else:
        # Insert after <p:cSld ...>
        csld_re = re.compile(r'(<p:cSld[^>]*>)', re.DOTALL)
        new_xml, n = csld_re.subn(r'\1' + bg_block, xml, count=1)
        return new_xml, n


def ensure_white_text_in_dark_slide(xml: str) -> tuple[str, int]:
    """
    On dark slides, any explicit black or very dark text color → white.
    Only touches srgbClr values that are very dark (luminance < 20%).
    """
    count = 0
    dark_colors = {
        "000000", "1a1a1a", "333333", "0e2841",
        "212121", "404040", "222222", "111111",
    }

    def _replacer(m):
        nonlocal count
        val = m.group(2).lower()
        if val in dark_colors:
            count += 1
            return m.group(1) + WHITE + m.group(3)
        return m.group(0)

    new_xml = _SRGB_RE.sub(_replacer, xml)
    return new_xml, count


def remove_explicit_background(xml: str) -> tuple[str, int]:
    """
    On light-background slides, remove any explicit <p:bg> so the slide master
    controls the background (usually white/light gray).
    """
    bg_re = re.compile(r'\s*<p:bg\b.*?</p:bg>', re.DOTALL)
    new_xml, n = bg_re.subn("", xml)
    return new_xml, n


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def get_slide_count(unpacked: pathlib.Path) -> int:
    slides = sorted(unpacked.glob("ppt/slides/slide*.xml"),
                    key=lambda p: int(re.search(r'\d+', p.stem).group()))
    return len(slides)


def get_slide_files(unpacked: pathlib.Path) -> list[pathlib.Path]:
    return sorted(unpacked.glob("ppt/slides/slide*.xml"),
                  key=lambda p: int(re.search(r'\d+', p.stem).group()))


def main():
    parser = argparse.ArgumentParser(description="Apply ADATA brand style to unpacked PPTX.")
    parser.add_argument("unpacked_dir", help="Path to unpacked PPTX directory")
    parser.add_argument("--dark-slides", nargs="+", type=int, metavar="N",
                        help="1-based slide indices to treat as dark background. "
                             "Default: first and last slide.")
    parser.add_argument("--colors-only", action="store_true",
                        help="Only remap hardcoded accent colors and title fonts. "
                             "Skip all background modifications. Use when source "
                             "already has ADATA-branded background images.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without writing files.")
    args = parser.parse_args()

    unpacked = pathlib.Path(args.unpacked_dir)
    if not unpacked.is_dir():
        print(f"ERROR: '{unpacked}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    slides = get_slide_files(unpacked)
    n_slides = len(slides)
    if n_slides == 0:
        print("ERROR: No slide files found.", file=sys.stderr)
        sys.exit(1)

    # Determine dark-background slide indices (1-based)
    if args.dark_slides:
        dark_indices = set(args.dark_slides)
    else:
        dark_indices = {1, n_slides}  # cover + closing

    if args.colors_only:
        print(f"Processing {n_slides} slides in COLORS-ONLY mode (backgrounds untouched).")
    else:
        print(f"Processing {n_slides} slides. Dark-background slides: {sorted(dark_indices)}")
    if args.dry_run:
        print("DRY RUN — no files will be written.\n")

    total_font_changes = 0
    total_color_changes = 0
    total_bg_changes = 0
    total_text_changes = 0

    for i, slide_path in enumerate(slides, start=1):
        xml = slide_path.read_text(encoding="utf-8")
        original = xml
        is_dark = i in dark_indices

        label = f"[slide {i:02d} {'DARK' if is_dark else 'LIGHT'}]"

        # 1. Remap hardcoded accent colors
        xml, nc = remap_colors(xml)
        total_color_changes += nc

        # 2. Title/subtitle styling: Arial Black + correct color per background type
        xml, nf = apply_title_styling(xml, is_dark)
        total_font_changes += nf

        # 3. Background
        if args.colors_only:
            nb = 0
            nt = 0
        elif is_dark:
            xml, nb = set_background_dark(xml)
            xml, nt = ensure_white_text_in_dark_slide(xml)
            total_text_changes += nt
        else:
            xml, nb = remove_explicit_background(xml)
            nt = 0
        total_bg_changes += nb

        changed = xml != original
        if changed:
            summary_parts = []
            if nf:  summary_parts.append(f"{nf} font(s)")
            if nc:  summary_parts.append(f"{nc} color(s)")
            if nb:  summary_parts.append(f"bg")
            if nt:  summary_parts.append(f"{nt} text color(s)")
            print(f"  {label} {slide_path.name}: changed {', '.join(summary_parts)}")
            if not args.dry_run:
                slide_path.write_text(xml, encoding="utf-8")
        else:
            print(f"  {label} {slide_path.name}: no changes")

    print()
    print("Summary:")
    print(f"  Title/subtitle styling  : {total_font_changes}")
    print(f"  Hardcoded color remaps  : {total_color_changes}")
    print(f"  Background changes      : {total_bg_changes}")
    print(f"  Dark-slide text fixes   : {total_text_changes}")
    if args.dry_run:
        print("\nDRY RUN complete — no files written.")
    else:
        print("\nDone. Run scripts/clean.py and scripts/office/pack.py next.")


if __name__ == "__main__":
    main()
