"""
Excel to Markdown Converter
============================
Converts each worksheet in an Excel file into a separate Markdown file.
Handles both cell table data and shape-based flowcharts (connectors,
decision diamonds, swim lanes) rendered as Mermaid syntax.

Requirements:
  - Windows (COM automation)
  - Python 3.8+
  - pywin32  (pip install pywin32)

Usage:
  python excel_to_markdown.py --excel-file <path> [--output-dir <dir>] [--sheet <name>]
"""

import argparse
import math
import os
import re
import sys
from collections import defaultdict

import win32com.client

# ─── Shape type constants ───────────────────────────
DECISION_TYPES = {4, 63, 110}   # 菱形 / 決策
ROUNDED_TYPES = {5, 62, 116}    # 圓角矩形 / 終端


# ─── Helper functions ───────────────────────────────

def safe_get_text(shape):
    """Try multiple methods to extract text from an Excel shape."""
    # Method 1: DrawingObject.Text (most reliable)
    try:
        txt = shape.DrawingObject.Text
        if txt:
            return txt
    except Exception:
        pass
    # Method 2: TextFrame.Characters
    try:
        txt = shape.TextFrame.Characters().Text
        if txt:
            return txt
    except Exception:
        pass
    # Method 3: TextFrame2
    try:
        tf2 = shape.TextFrame2
        if tf2.HasText:
            return tf2.TextRange.Text
    except Exception:
        pass
    return ""


def make_node_id(index):
    return f"n{index}"


def sanitize_text(text):
    """Make text safe for Mermaid syntax."""
    text = text.strip()
    text = text.replace('"', "'")
    text = text.replace('\r\n', '<br>')
    text = text.replace('\r', '<br>')
    text = text.replace('\n', '<br>')
    text = re.sub(r'(<br>){3,}', '<br><br>', text)
    return text


def sanitize_filename(name):
    """Convert sheet name to a safe filename."""
    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    safe = safe.strip('. ')
    return safe or "sheet"


def mermaid_node_def(node_id, text, auto_type):
    """Generate Mermaid node definition based on shape type."""
    safe = sanitize_text(text)
    q = f'"{safe}"'
    if auto_type in DECISION_TYPES:
        return f'{node_id}{{{{{q}}}}}'     # {{text}} — diamond
    elif auto_type in ROUNDED_TYPES:
        return f'{node_id}({q})'           # (text)  — rounded rect
    else:
        return f'{node_id}[{q}]'           # [text]  — rectangle


# ─── Core conversion for a single worksheet ─────────

def convert_sheet(ws):
    """
    Convert one worksheet to Markdown string.
    Returns the Markdown content as a string.
    """
    sheet_name = ws.Name
    shape_count = ws.Shapes.Count

    # ── Phase 1: Classify shapes ────────────────────
    connector_indices = set()
    for i in range(1, shape_count + 1):
        shape = ws.Shapes.Item(i)
        try:
            cf = shape.ConnectorFormat
            _ = cf.BeginConnected
            connector_indices.add(i)
        except Exception:
            pass

    # ── Phase 2: Collect text nodes ─────────────────
    nodes = {}
    idx_by_name = {}
    for i in range(1, shape_count + 1):
        if i in connector_indices:
            continue
        shape = ws.Shapes.Item(i)
        text = safe_get_text(shape)
        if not text.strip():
            continue

        auto_type = -1
        try:
            auto_type = shape.AutoShapeType
        except Exception:
            pass

        nodes[i] = {
            "id": make_node_id(i),
            "text": text,
            "auto_type": auto_type,
            "top": shape.Top,
            "left": shape.Left,
            "width": shape.Width,
            "height": shape.Height,
            "name": shape.Name,
        }
        idx_by_name.setdefault(shape.Name, []).append(i)

    # ── Phase 3: Extract edges from connectors ──────
    edges = []
    for i in range(1, shape_count + 1):
        if i not in connector_indices:
            continue
        shape = ws.Shapes.Item(i)
        try:
            cf = shape.ConnectorFormat
        except Exception:
            continue

        begin_idx = None
        end_idx = None

        try:
            if cf.BeginConnected:
                bs = cf.BeginConnectedShape
                bname = bs.Name
                candidates = idx_by_name.get(bname, [])
                if len(candidates) == 1:
                    begin_idx = candidates[0]
                elif len(candidates) > 1:
                    btop, bleft = bs.Top, bs.Left
                    begin_idx = min(candidates,
                                    key=lambda ci: abs(nodes[ci]["top"] - btop) + abs(nodes[ci]["left"] - bleft))
        except Exception:
            pass

        try:
            if cf.EndConnected:
                es = cf.EndConnectedShape
                ename = es.Name
                candidates = idx_by_name.get(ename, [])
                if len(candidates) == 1:
                    end_idx = candidates[0]
                elif len(candidates) > 1:
                    etop, eleft = es.Top, es.Left
                    end_idx = min(candidates,
                                  key=lambda ci: abs(nodes[ci]["top"] - etop) + abs(nodes[ci]["left"] - eleft))
        except Exception:
            pass

        if begin_idx and end_idx and begin_idx in nodes and end_idx in nodes:
            label = safe_get_text(shape).strip()
            edges.append((begin_idx, end_idx, sanitize_text(label) if label else ""))

    has_flowchart = len(edges) > 0

    # ── Phase 4: Yes/No label matching ──────────────
    label_nodes = set()
    for idx, info in list(nodes.items()):
        txt = info["text"].strip().lower()
        if txt in ("yes", "no", "y", "n", "是", "否"):
            is_endpoint = any(idx == e[0] or idx == e[1] for e in edges)
            if not is_endpoint:
                label_nodes.add(idx)

    # Group labels by nearest decision node
    decision_labels = defaultdict(list)
    for label_idx in label_nodes:
        li = nodes[label_idx]
        ltxt = li["text"].strip()
        lw = li.get("width", 50)
        lh = li.get("height", 20)
        l_cx = li["left"] + lw / 2
        l_cy = li["top"] + lh / 2

        decision_sources = set()
        for bi, _, _ in edges:
            if nodes[bi]["auto_type"] in DECISION_TYPES:
                decision_sources.add(bi)

        best_dec = None
        best_dist = float("inf")
        for dec_idx in decision_sources:
            d = nodes[dec_idx]
            d_cx = d["left"] + d.get("width", 50) / 2
            d_cy = d["top"] + d.get("height", 50) / 2
            dist = math.hypot(l_cx - d_cx, l_cy - d_cy)
            if dist < best_dist:
                best_dist = dist
                best_dec = dec_idx
        if best_dec is not None and best_dist < 200:
            decision_labels[best_dec].append((label_idx, ltxt, l_cx, l_cy))

    # Match labels to edges by direction angle
    for dec_idx, labels in decision_labels.items():
        d = nodes[dec_idx]
        d_cx = d["left"] + d.get("width", 50) / 2
        d_cy = d["top"] + d.get("height", 50) / 2

        dec_edges = []
        for ei, (bi, end_i, elabel) in enumerate(edges):
            if bi == dec_idx and not elabel:
                e = nodes[end_i]
                e_cx = e["left"] + e.get("width", 50) / 2
                e_cy = e["top"] + e.get("height", 50) / 2
                angle = math.atan2(e_cy - d_cy, e_cx - d_cx)
                dec_edges.append((ei, angle))
        if not dec_edges:
            continue

        label_angles = []
        for label_idx, ltxt, l_cx, l_cy in labels:
            angle = math.atan2(l_cy - d_cy, l_cx - d_cx)
            label_angles.append((label_idx, ltxt, angle))

        pairs = []
        for li_idx, ltxt, l_angle in label_angles:
            for ei, e_angle in dec_edges:
                diff = abs(l_angle - e_angle)
                if diff > math.pi:
                    diff = 2 * math.pi - diff
                pairs.append((diff, li_idx, ltxt, ei))
        pairs.sort()

        used_edges = set()
        used_labels = set()
        for diff, li_idx, ltxt, ei in pairs:
            if li_idx in used_labels or ei in used_edges:
                continue
            bi, end_i, _ = edges[ei]
            edges[ei] = (bi, end_i, ltxt)
            used_edges.add(ei)
            used_labels.add(li_idx)

    for idx in label_nodes:
        del nodes[idx]

    # ── Phase 5: Swim-lane detection ────────────────
    connected_nodes = set()
    for bi, ei, _ in edges:
        connected_nodes.add(bi)
        connected_nodes.add(ei)

    candidate_headers = {idx: info for idx, info in nodes.items() if idx not in connected_nodes}

    header_nodes = {}
    if candidate_headers:
        min_top = min(info["top"] for info in candidate_headers.values())
        TOP_TOLERANCE = 30
        top_row = {idx: info for idx, info in candidate_headers.items()
                   if info["top"] <= min_top + TOP_TOLERANCE}
        if len(top_row) >= 2:
            header_nodes = top_row

    flow_nodes = {idx: info for idx, info in nodes.items() if idx not in header_nodes}

    lane_assignments = {}
    sorted_headers = sorted(header_nodes.items(), key=lambda x: x[1]["left"])

    if sorted_headers:
        lane_ranges = []
        header_centers = [(idx, info["left"] + info.get("width", 50) / 2) for idx, info in sorted_headers]
        for i, (hidx, hcenter) in enumerate(header_centers):
            x_min = -float("inf") if i == 0 else (header_centers[i - 1][1] + hcenter) / 2
            x_max = float("inf") if i == len(header_centers) - 1 else (hcenter + header_centers[i + 1][1]) / 2
            lane_ranges.append((hidx, x_min, x_max))

        for fidx, finfo in flow_nodes.items():
            f_center = finfo["left"] + finfo.get("width", 50) / 2
            assigned = None
            for hidx, x_min, x_max in lane_ranges:
                if x_min <= f_center <= x_max:
                    assigned = hidx
                    break
            if assigned is None:
                assigned = min(header_centers, key=lambda hc: abs(hc[1] - f_center))[0]
            lane_assignments[fidx] = assigned

    # Remove decorative (non-connected, non-header) nodes
    decorative = set()
    for fidx in list(flow_nodes.keys()):
        if fidx not in connected_nodes and fidx not in header_nodes:
            decorative.add(fidx)
    for fidx in decorative:
        del flow_nodes[fidx]
        lane_assignments.pop(fidx, None)

    # ── Phase 6: Read table data ────────────────────
    table_data = []
    try:
        used = ws.UsedRange
        if used:
            nrows = min(used.Rows.Count, 200)
            ncols = used.Columns.Count
            for r in range(1, nrows + 1):
                row = []
                for c in range(1, ncols + 1):
                    v = ws.Cells(r, c).Value
                    row.append(str(v).strip() if v else "")
                if any(row):
                    table_data.append(row)
    except Exception:
        pass

    # ── Phase 7: Build Markdown ─────────────────────
    md = []
    md.append(f"# {sheet_name}")
    md.append("")
    md.append("---")
    md.append("")

    # Part 1: Flowchart (only if shapes with connections exist)
    if has_flowchart and flow_nodes:
        md.append("# 第一部分：流程圖與圖形資訊")
        md.append("")

        # 1.1 Flowchart
        md.append("## 1.1 流程圖")
        md.append("")
        if sorted_headers:
            lane_count = len(sorted_headers)
            md.append(f"> {lane_count} 個部門以 subgraph 表示泳道歸屬。")
        md.append("")
        md.append("```mermaid")
        md.append("flowchart TD")

        sorted_flow = sorted(flow_nodes.items(), key=lambda x: (x[1]["top"], x[1]["left"]))

        if sorted_headers and lane_assignments:
            for hidx, hinfo in sorted_headers:
                lane_name = sanitize_text(hinfo["text"]).replace("<br>", " ")
                lane_id = hinfo["id"].replace("-", "_")
                md.append(f'    subgraph {lane_id}["{lane_name}"]')
                for fidx, finfo in sorted_flow:
                    if lane_assignments.get(fidx) == hidx:
                        node_def = mermaid_node_def(finfo["id"], finfo["text"], finfo["auto_type"])
                        md.append(f"        {node_def}")
                md.append("    end")
            md.append("")
        else:
            for idx, info in sorted_flow:
                node_def = mermaid_node_def(info["id"], info["text"], info["auto_type"])
                md.append(f"    {node_def}")
            md.append("")

        for bi, ei, label in edges:
            if bi not in flow_nodes or ei not in flow_nodes:
                continue
            fid = flow_nodes[bi]["id"]
            tid = flow_nodes[ei]["id"]
            if label:
                md.append(f'    {fid} -->|"{label}"| {tid}')
            else:
                md.append(f"    {fid} --> {tid}")
        md.append("```")
        md.append("")

        # 1.2 Node list
        md.append("## 1.2 節點清單")
        md.append("")
        md.append("| ID | 文字 | Mermaid 符號 | 所屬部門 |")
        md.append("| --- | --- | --- | --- |")
        for idx, info in sorted_flow:
            txt = info["text"].replace("\n", " ").replace("\r", " ").replace("|", "\\|").strip()
            at = info["auto_type"]
            if at in DECISION_TYPES:
                symbol = "菱形 (決策)"
            elif at in ROUNDED_TYPES:
                symbol = "圓角矩形"
            else:
                symbol = "矩形"
            dept = ""
            if lane_assignments.get(idx) in header_nodes:
                dept = header_nodes[lane_assignments[idx]]["text"].replace("\n", " ").strip()
            md.append(f"| {info['id']} | {txt} | {symbol} | {dept} |")
        md.append("")

        # 1.3 Edge list
        md.append("## 1.3 連線清單")
        md.append("")
        md.append("| # | 起點 | 終點 | 標籤 |")
        md.append("| --- | --- | --- | --- |")
        edge_num = 0
        for bi, ei, label in edges:
            if bi not in flow_nodes or ei not in flow_nodes:
                continue
            edge_num += 1
            ftxt = flow_nodes[bi]["text"].replace("\n", " ")[:20]
            etxt = flow_nodes[ei]["text"].replace("\n", " ")[:20]
            md.append(f"| {edge_num} | {flow_nodes[bi]['id']} ({ftxt}) | {flow_nodes[ei]['id']} ({etxt}) | {label} |")
        md.append("")

        md.append("---")
        md.append("")

    # Part 2: Table data
    if has_flowchart and flow_nodes:
        md.append("# 第二部分：Excel 表格資訊")
    else:
        md.append("# Excel 表格資訊")
    md.append("")

    if table_data:
        max_cols = max(len(r) for r in table_data)
        col_has_data = [False] * max_cols
        for row in table_data:
            for ci in range(len(row)):
                if row[ci].strip():
                    col_has_data[ci] = True
        keep_cols = [i for i in range(max_cols) if col_has_data[i]]

        if keep_cols:
            filtered = []
            for row in table_data:
                while len(row) < max_cols:
                    row.append("")
                filtered.append([row[ci] for ci in keep_cols])

            header = filtered[0]
            hdr = [h.replace("\n", " ").replace("\r", " ").strip() for h in header]
            if not any(hdr):
                if len(filtered) > 1:
                    hdr = [h.replace("\n", " ").replace("\r", " ").strip() for h in filtered[1]]
                    filtered = [filtered[0]] + filtered[2:]
                hdr = [h if h else f"欄{i+1}" for i, h in enumerate(hdr)]

            ncols_out = len(keep_cols)
            md.append("| " + " | ".join(hdr) + " |")
            md.append("| " + " | ".join(["---"] * ncols_out) + " |")

            for row in filtered[1:]:
                cells = [c.replace("\n", " ").replace("\r", " ").replace("|", "\\|").strip() for c in row]
                if not any(cells):
                    continue
                md.append("| " + " | ".join(cells) + " |")
        md.append("")
    else:
        md.append("*此工作表無表格資料*")
        md.append("")

    return "\n".join(md), {
        "sheet": sheet_name,
        "nodes": len(flow_nodes),
        "edges": len(edges),
        "lanes": len(header_nodes),
        "has_flowchart": has_flowchart,
    }


# ─── Main entry point ──────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert Excel worksheets to Markdown files (with Mermaid flowcharts)."
    )
    parser.add_argument("--excel-file", required=True, help="Path to the Excel file (.xlsx/.xls)")
    parser.add_argument("--output-dir", default=".", help="Output directory for .md files (default: current dir)")
    parser.add_argument("--sheet", default=None,
                        help="Sheet name or substring to match. Omit to convert ALL sheets.")
    args = parser.parse_args()

    excel_path = os.path.abspath(args.excel_file)
    output_dir = os.path.abspath(args.output_dir)

    if not os.path.exists(excel_path):
        print(f"Error: file not found: {excel_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Opening Excel: {excel_path}")
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    try:
        wb = excel.Workbooks.Open(excel_path, ReadOnly=True)
        if wb is None:
            raise RuntimeError("Workbooks.Open returned None")
    except Exception as e:
        print(f"Cannot open file: {e}")
        try:
            excel.Quit()
        except Exception:
            pass
        sys.exit(1)

    # Determine which sheets to convert
    target_sheets = []
    for i in range(1, wb.Sheets.Count + 1):
        ws = wb.Sheets(i)
        if args.sheet:
            if args.sheet in ws.Name:
                target_sheets.append(ws)
        else:
            target_sheets.append(ws)

    if not target_sheets:
        print(f"No matching sheets found" + (f" for '{args.sheet}'" if args.sheet else ""))
        wb.Close(False)
        excel.Quit()
        sys.exit(1)

    print(f"Sheets to convert: {len(target_sheets)}")

    results = []
    for ws in target_sheets:
        print(f"\n--- Converting: {ws.Name} (shapes: {ws.Shapes.Count}) ---")
        try:
            md_content, stats = convert_sheet(ws)
            out_name = sanitize_filename(ws.Name) + ".md"
            out_path = os.path.join(output_dir, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"  -> {out_path}")
            print(f"     Lanes: {stats['lanes']}  Nodes: {stats['nodes']}  Edges: {stats['edges']}")
            results.append((ws.Name, out_path, stats))
        except Exception as e:
            print(f"  Error converting {ws.Name}: {e}")

    wb.Close(False)
    excel.Quit()
    print("\nExcel closed.")

    # Summary
    print(f"\n{'='*50}")
    print(f"Converted {len(results)}/{len(target_sheets)} sheets:")
    for name, path, stats in results:
        fc = " (with flowchart)" if stats["has_flowchart"] else ""
        print(f"  {name} -> {os.path.basename(path)}{fc}")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
