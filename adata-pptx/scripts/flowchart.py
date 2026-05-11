"""
Render flowcharts and native tables onto ADATA slides using PowerPoint built-in shapes.

Flowchart nodes use OOXML preset geometry (flowChartProcess, flowChartDecision,
flowChartTerminator, etc.).  Connectors use <p:cxnSp> with a line preset and
an arrow tailEnd.  Tables use <p:graphicFrame> with a native <a:tbl> element.

Public API
----------
render_flowchart(xml, flowchart_data, accent_color) -> str
render_table(xml, table_data, accent_color)         -> str
"""

import html
import re

# ---------------------------------------------------------------------------
# Slide / layout constants  (standard widescreen 16:9: 13.33" × 7.5")
# ---------------------------------------------------------------------------
_SLIDE_W   = 12192000   # 13.333 in  (EMU)
_SLIDE_H   = 6858000    # 7.5 in     (EMU)
_TITLE_H   = 1371600    # 1.5 in  — space reserved for title + subtitle
_MARGIN    = 457200     # 0.5 in  — horizontal / vertical margin

# ---------------------------------------------------------------------------
# Node geometry  (EMU)
# ---------------------------------------------------------------------------
_NODE_W  = 1828800    # 2.0 in  — rect / oval / para / doc / db
_NODE_H  = 548640     # 0.6 in
_DIAM_W  = 2286000    # 2.5 in  — diamond (wider to hold text)
_DIAM_H  = 914400     # 1.0 in

_SHAPE_PRST = {
    "oval":    "flowChartTerminator",   # rounded rect  — Start / End
    "rect":    "flowChartProcess",      # rectangle     — Process step
    "diamond": "flowChartDecision",     # diamond       — Decision
    "para":    "flowChartInputOutput",  # parallelogram — Input / Output
    "doc":     "flowChartDocument",     # wave-bottom   — Document
    "db":      "flowChartDatabase",     # cylinder      — Database / Storage
}

_SHAPE_SIZE = {
    "oval":    (_NODE_W, _NODE_H),
    "rect":    (_NODE_W, _NODE_H),
    "diamond": (_DIAM_W, _DIAM_H),
    "para":    (_NODE_W, _NODE_H),
    "doc":     (_NODE_W, _NODE_H),
    "db":      (_NODE_W, _NODE_H),
}

_H_GAP = 457200    # 0.5 in — gap between sibling nodes in same layer
_V_GAP = 548640    # 0.6 in — gap between layers

# ---------------------------------------------------------------------------
# ADATA brand colours
# ---------------------------------------------------------------------------
_NAVY  = "0E2841"
_WHITE = "FFFFFF"

# ---------------------------------------------------------------------------
# Layout  (BFS layering)
# ---------------------------------------------------------------------------

def _bfs_layers(nodes, edges):
    """Return {node_id: depth} using BFS from root nodes (in-degree == 0)."""
    ids      = [n["id"] for n in nodes]
    children = {i: [] for i in ids}
    in_deg   = {i: 0   for i in ids}
    for e in edges:
        f, t = e.get("from", ""), e.get("to", "")
        if f in children and t in in_deg:
            children[f].append(t)
            in_deg[t] += 1

    roots = [i for i in ids if in_deg[i] == 0] or ids[:1]
    depth = {}
    queue = [(r, 0) for r in roots]
    while queue:
        nid, d = queue.pop(0)
        if nid in depth:
            depth[nid] = max(depth[nid], d)
            continue
        depth[nid] = d
        for child in children.get(nid, []):
            queue.append((child, d + 1))
    for i in ids:
        depth.setdefault(i, 0)
    return depth


def _compute_layout(nodes, edges, direction="TB"):
    """Return {node_id: (cx, cy)} center positions in EMU."""
    node_map = {n["id"]: n for n in nodes}
    depths   = _bfs_layers(nodes, edges)

    layers = {}
    for nid, d in depths.items():
        layers.setdefault(d, []).append(nid)
    sorted_d = sorted(layers)

    content_x0 = _MARGIN
    content_y0  = _TITLE_H + _MARGIN
    content_w   = _SLIDE_W - 2 * _MARGIN
    content_h   = _SLIDE_H - _TITLE_H - 2 * _MARGIN

    positions = {}

    if direction != "LR":   # default: TB (top-to-bottom)
        # Pre-compute per-layer height
        lh = []
        for d in sorted_d:
            h = max(_SHAPE_SIZE.get(node_map[n].get("shape", "rect"),
                                    (_NODE_W, _NODE_H))[1]
                    for n in layers[d])
            lh.append(h)
        total_h = sum(lh) + _V_GAP * max(0, len(sorted_d) - 1)
        y_off   = content_y0 + max(0, (content_h - total_h) // 2)

        for idx, d in enumerate(sorted_d):
            nids    = layers[d]
            h_layer = lh[idx]
            cy      = y_off + h_layer // 2

            widths  = [_SHAPE_SIZE.get(node_map[n].get("shape", "rect"),
                                       (_NODE_W, _NODE_H))[0] for n in nids]
            total_w = sum(widths) + _H_GAP * max(0, len(nids) - 1)
            x_cur   = content_x0 + max(0, (content_w - total_w) // 2)

            for j, nid in enumerate(nids):
                w = widths[j]
                positions[nid] = (x_cur + w // 2, cy)
                x_cur += w + _H_GAP
            y_off += h_layer + _V_GAP

    else:   # LR (left-to-right)
        lw = []
        for d in sorted_d:
            w = max(_SHAPE_SIZE.get(node_map[n].get("shape", "rect"),
                                    (_NODE_W, _NODE_H))[0]
                    for n in layers[d])
            lw.append(w)
        total_w = sum(lw) + _H_GAP * max(0, len(sorted_d) - 1)
        x_off   = content_x0 + max(0, (content_w - total_w) // 2)

        for idx, d in enumerate(sorted_d):
            nids    = layers[d]
            w_layer = lw[idx]
            cx      = x_off + w_layer // 2

            heights = [_SHAPE_SIZE.get(node_map[n].get("shape", "rect"),
                                       (_NODE_W, _NODE_H))[1] for n in nids]
            total_h = sum(heights) + _V_GAP * max(0, len(nids) - 1)
            y_cur   = content_y0 + max(0, (content_h - total_h) // 2)

            for j, nid in enumerate(nids):
                h = heights[j]
                positions[nid] = (cx, y_cur + h // 2)
                y_cur += h + _V_GAP
            x_off += w_layer + _H_GAP

    return positions


def _boundary_pt(cx, cy, shape, is_source, direction,
                 exit_count=None, max_exits=None):
    """Return (x, y) connection point on shape boundary.

    For TB layout  — sources exit bottom, targets enter top.
    For LR layout  — sources exit right, targets enter left.
    When a node has multiple outgoing edges (exit_count > 0) the second exit
    uses the right side (TB) or bottom side (LR).
    """
    w, h = _SHAPE_SIZE.get(shape, (_NODE_W, _NODE_H))
    if direction != "LR":  # TB
        if is_source:
            if exit_count and exit_count > 0:
                return (cx + w // 2, cy)   # right side for 2nd+ exit
            return (cx, cy + h // 2)       # bottom center
        else:
            return (cx, cy - h // 2)       # top center
    else:  # LR
        if is_source:
            if exit_count and exit_count > 0:
                return (cx, cy + h // 2)   # bottom for 2nd+ exit
            return (cx + w // 2, cy)       # right center
        else:
            return (cx - w // 2, cy)       # left center


# ---------------------------------------------------------------------------
# XML generation helpers
# ---------------------------------------------------------------------------

def _next_id(xml):
    """Return next available shape id (max existing + 1)."""
    ids = [int(m) for m in re.findall(r'<p:cNvPr id="(\d+)"', xml)]
    return (max(ids) if ids else 0) + 1


def _lang(text):
    return "zh-TW" if any(ord(c) >= 0x2E80 for c in text) else "en-US"


def _node_xml(node, cx, cy, shape_id, fill, line="FFFFFF", text_color="FFFFFF"):
    shape = node.get("shape", "rect")
    prst  = _SHAPE_PRST.get(shape, "flowChartProcess")
    w, h  = _SHAPE_SIZE.get(shape, (_NODE_W, _NODE_H))
    x, y  = cx - w // 2, cy - h // 2
    txt   = html.escape(node.get("text", ""))
    lg    = _lang(txt)
    alt   = "en-US" if lg == "zh-TW" else "zh-TW"
    return (
        f'<p:sp>'
        f'<p:nvSpPr>'
        f'<p:cNvPr id="{shape_id}" name="FlowNode{shape_id}"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr/>'
        f'</p:nvSpPr>'
        f'<p:spPr>'
        f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        f'</p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr anchor="ctr"/>'
        f'<a:lstStyle/>'
        f'<a:p>'
        f'<a:pPr algn="ctr"/>'
        f'<a:r>'
        f'<a:rPr lang="{lg}" altLang="{alt}" sz="1400" b="0" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{text_color}"/></a:solidFill>'
        f'</a:rPr>'
        f'<a:t>{txt}</a:t>'
        f'</a:r>'
        f'</a:p>'
        f'</p:txBody>'
        f'</p:sp>'
    )


def _connector_xml(x1, y1, x2, y2, conn_id, line_color="000000"):
    """Straight arrow connector from (x1,y1) to (x2,y2)."""
    bx  = min(x1, x2)
    by  = min(y1, y2)
    bcx = max(abs(x2 - x1), 1)
    bcy = max(abs(y2 - y1), 1)

    # Flip attributes so that tail (arrow head) is always at (x2,y2)
    go_r = x2 >= x1
    go_d = y2 >= y1
    if   go_r and go_d:    flip = ""
    elif go_r and not go_d: flip = ' flipV="1"'
    elif not go_r and go_d: flip = ' flipH="1"'
    else:                   flip = ' flipH="1" flipV="1"'

    return (
        f'<p:cxnSp>'
        f'<p:nvCxnSpPr>'
        f'<p:cNvPr id="{conn_id}" name="FlowConn{conn_id}"/>'
        f'<p:cNvCxnSpPr/>'
        f'<p:nvPr/>'
        f'</p:nvCxnSpPr>'
        f'<p:spPr>'
        f'<a:xfrm{flip}><a:off x="{bx}" y="{by}"/><a:ext cx="{bcx}" cy="{bcy}"/></a:xfrm>'
        f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
        f'<a:noFill/>'
        f'<a:ln w="25400">'
        f'<a:solidFill><a:srgbClr val="{line_color}"/></a:solidFill>'
        f'<a:tailEnd type="arrow" w="med" len="med"/>'
        f'</a:ln>'
        f'</p:spPr>'
        f'</p:cxnSp>'
    )


def _label_xml(text, mx, my, label_id, text_color=_NAVY):
    """Small transparent text box for connector edge labels."""
    lw, lh = 685800, 304800   # 0.75 in × 0.33 in
    x, y   = mx - lw // 2, my - lh // 2
    txt    = html.escape(text)
    lg     = _lang(txt)
    alt    = "en-US" if lg == "zh-TW" else "zh-TW"
    return (
        f'<p:sp>'
        f'<p:nvSpPr>'
        f'<p:cNvPr id="{label_id}" name="FlowLabel{label_id}"/>'
        f'<p:cNvSpPr txBox="1"/>'
        f'<p:nvPr/>'
        f'</p:nvSpPr>'
        f'<p:spPr>'
        f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{lw}" cy="{lh}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:noFill/>'
        f'<a:ln><a:noFill/></a:ln>'
        f'</p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr wrap="square" anchor="ctr"/>'
        f'<a:lstStyle/>'
        f'<a:p>'
        f'<a:pPr algn="ctr"/>'
        f'<a:r>'
        f'<a:rPr lang="{lg}" altLang="{alt}" sz="1200" b="1" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{text_color}"/></a:solidFill>'
        f'</a:rPr>'
        f'<a:t>{txt}</a:t>'
        f'</a:r>'
        f'</a:p>'
        f'</p:txBody>'
        f'</p:sp>'
    )


# ---------------------------------------------------------------------------
# Public: render_flowchart
# ---------------------------------------------------------------------------

def render_flowchart(xml: str, flowchart_data: dict,
                     accent_color: str = "5097FF") -> str:
    """Inject flowchart shapes + connectors into slide XML.

    flowchart_data keys:
      direction  : "TB" (default) or "LR"
      nodes      : list of {id, shape, text}
                   shape ∈ {oval, rect, diamond, para, doc, db}
      edges      : list of {from, to} or {from, to, label}
      fill_color : hex (optional, overrides accent_color for node fills)
      line_color : hex (optional, connector/border colour, default white)
      text_color : hex (optional, node text colour, default white)
    """
    nodes     = flowchart_data.get("nodes", [])
    edges     = flowchart_data.get("edges", [])
    direction = flowchart_data.get("direction", "TB").upper()
    fill      = flowchart_data.get("fill_color", accent_color)
    line_clr  = flowchart_data.get("line_color", "000000")
    txt_clr   = flowchart_data.get("text_color", _WHITE)

    if not nodes:
        return xml

    positions = _compute_layout(nodes, edges, direction)
    node_map  = {n["id"]: n for n in nodes}
    sid       = _next_id(xml)
    parts     = []

    # Track how many times a node has been used as a source (for side exits)
    exit_counts: dict[str, int] = {}

    # Connectors first — nodes rendered on top
    for edge in edges:
        fid = edge.get("from", "")
        tid = edge.get("to", "")
        if fid not in positions or tid not in positions:
            continue

        fcx, fcy = positions[fid]
        tcx, tcy = positions[tid]
        fshape   = node_map[fid].get("shape", "rect")
        tshape   = node_map[tid].get("shape", "rect")

        ec = exit_counts.get(fid, 0)
        x1, y1 = _boundary_pt(fcx, fcy, fshape, True,  direction, ec)
        x2, y2 = _boundary_pt(tcx, tcy, tshape, False, direction)
        exit_counts[fid] = ec + 1

        parts.append(_connector_xml(x1, y1, x2, y2, sid, line_clr))
        sid += 1

        lbl = edge.get("label", "")
        if lbl:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            parts.append(_label_xml(lbl, mx, my, sid))
            sid += 1

    # Node shapes
    for node in nodes:
        nid = node["id"]
        if nid not in positions:
            continue
        cx, cy = positions[nid]
        parts.append(_node_xml(node, cx, cy, sid, fill, line_clr, txt_clr))
        sid += 1

    injection = "".join(parts)
    return xml.replace("</p:spTree>", injection + "</p:spTree>", 1)


# ---------------------------------------------------------------------------
# Public: render_table
# ---------------------------------------------------------------------------

def render_table(xml: str, table_data: dict,
                 accent_color: str = "5097FF") -> str:
    """Insert a native PowerPoint table into slide XML.

    table_data keys:
      header      : list[str]   — column headers
      rows        : list[list[str]]  — data rows
      header_fill : hex (optional, default dark navy)
      col_width   : int EMU (optional, auto-sized if omitted)
    """
    header  = table_data.get("header", [])
    rows    = table_data.get("rows", [])
    hfill   = table_data.get("header_fill", _NAVY)
    n_cols  = max(len(header), max((len(r) for r in rows), default=0))

    if n_cols == 0:
        return xml

    # Table position / size
    tbl_x  = _MARGIN
    tbl_y  = _TITLE_H
    tbl_w  = _SLIDE_W - 2 * _MARGIN
    tbl_h  = _SLIDE_H - _TITLE_H - _MARGIN

    col_w    = tbl_w // n_cols if n_cols else tbl_w
    n_rows   = len(rows) + (1 if header else 0)
    row_h    = tbl_h // n_rows if n_rows else 548640

    sid = _next_id(xml)

    # tblGrid
    grid_cols = "".join(f'<a:gridCol w="{col_w}"/>' for _ in range(n_cols))

    def _cell(text, bold=False, bg=None, txt_color=_WHITE):
        t   = html.escape(str(text))
        lg  = _lang(t)
        alt = "en-US" if lg == "zh-TW" else "zh-TW"
        b   = "1" if bold else "0"
        tc_fill = (
            f'<a:solidFill><a:srgbClr val="{bg}"/></a:solidFill>' if bg else ""
        )
        return (
            f'<a:tc>'
            f'<a:txBody>'
            f'<a:bodyPr/>'
            f'<a:lstStyle/>'
            f'<a:p>'
            f'<a:pPr algn="ctr"/>'
            f'<a:r>'
            f'<a:rPr lang="{lg}" altLang="{alt}" sz="1600" b="{b}" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{txt_color}"/></a:solidFill>'
            f'</a:rPr>'
            f'<a:t>{t}</a:t>'
            f'</a:r>'
            f'</a:p>'
            f'</a:txBody>'
            f'<a:tcPr>{tc_fill}</a:tcPr>'
            f'</a:tc>'
        )

    def _row(cells_xml, h):
        return f'<a:tr h="{h}">{cells_xml}</a:tr>'

    tbl_rows = ""

    # Header row
    if header:
        padded = list(header) + [""] * (n_cols - len(header))
        cells  = "".join(
            _cell(c, bold=True, bg=hfill, txt_color=_WHITE) for c in padded
        )
        tbl_rows += _row(cells, row_h)

    # Data rows with alternating row colours
    light_gray = "E8E8E8"
    for ri, row in enumerate(rows):
        padded  = list(row) + [""] * (n_cols - len(row))
        bg      = None if ri % 2 == 0 else light_gray
        txt_c   = _NAVY
        cells   = "".join(_cell(c, bold=False, bg=bg, txt_color=txt_c) for c in padded)
        tbl_rows += _row(cells, row_h)

    tbl_xml = (
        f'<p:graphicFrame>'
        f'<p:nvGraphicFramePr>'
        f'<p:cNvPr id="{sid}" name="FlowTable{sid}"/>'
        f'<p:cNvGraphicFramePr>'
        f'<a:graphicFrameLocks noGrp="1"/>'
        f'</p:cNvGraphicFramePr>'
        f'<p:nvPr/>'
        f'</p:nvGraphicFramePr>'
        f'<p:xfrm>'
        f'<a:off x="{tbl_x}" y="{tbl_y}"/>'
        f'<a:ext cx="{tbl_w}" cy="{tbl_h}"/>'
        f'</p:xfrm>'
        f'<a:graphic>'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
        f'<a:tbl>'
        f'<a:tblPr firstRow="1" bandRow="1"/>'
        f'<a:tblGrid>{grid_cols}</a:tblGrid>'
        f'{tbl_rows}'
        f'</a:tbl>'
        f'</a:graphicData>'
        f'</a:graphic>'
        f'</p:graphicFrame>'
    )

    return xml.replace("</p:spTree>", tbl_xml + "</p:spTree>", 1)
