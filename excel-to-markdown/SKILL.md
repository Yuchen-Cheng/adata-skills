---
name: excel-to-markdown
description: "Convert Excel (.xlsx/.xls) worksheets to Markdown files. Each sheet is converted to a separate .md file containing: (1) flowchart diagrams extracted from shapes and connectors as Mermaid syntax with swim-lane subgraphs, decision labels (Yes/No), and node/edge lists; (2) table data from cell contents. Uses win32com (COM automation) on Windows to read shapes, connectors, and their connection relationships. Use this skill whenever the user asks to convert Excel to Markdown, extract flowcharts from Excel, turn Excel shapes into Mermaid diagrams, export Excel worksheets as .md files, read Excel flow diagrams, or generate documentation from Excel process maps. Also use when the user mentions spreadsheet-to-markdown, Excel diagram extraction, or process flow documentation from Excel files."
---

# Excel to Markdown Converter

Converts each worksheet in an Excel file into a separate Markdown file. Handles both **cell table data** and **shape-based flowcharts** (with connectors, decision diamonds, swim lanes).

## Requirements

- **Windows only** — uses win32com (COM automation) to read Excel shapes and connector relationships
- **Python 3.8+**
- **Dependencies**: `pywin32` (install via `pip install pywin32`)

## When to Use

- User wants to convert an Excel file's worksheets to Markdown
- User wants to extract flowcharts/process diagrams from Excel shapes into Mermaid syntax
- User wants to document Excel-based business processes as Markdown
- User has an `.xlsx` or `.xls` file with shapes, connectors, and/or table data

## How to Use

### Quick start

Run the bundled script directly — no need to read its source code:

```bash
python <skill-path>/scripts/excel_to_markdown.py --excel-file <path-to-xlsx> --output-dir <output-folder>
```

### CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--excel-file` | Yes | Path to the Excel file (.xlsx or .xls) |
| `--output-dir` | No | Directory for output .md files (default: current directory) |
| `--sheet` | No | Specific sheet name or substring to match. If omitted, converts ALL sheets |

### Examples

Convert all sheets:
```bash
python scripts/excel_to_markdown.py --excel-file "TW-Q2-PUR-001.xlsx" --output-dir ./output
```

Convert a specific sheet:
```bash
python scripts/excel_to_markdown.py --excel-file "TW-Q2-PUR-001.xlsx" --sheet "6.3" --output-dir ./output
```

### Output Format

Each sheet produces one `.md` file named after the sheet (sanitized for filesystem safety). The file contains:

#### Part 1: Flowchart & Shape Information (only if shapes with connectors exist)

- **1.1 Flowchart** — Mermaid `flowchart TD` with:
  - `subgraph` blocks for swim lanes (auto-detected from non-connected top-row shapes)
  - Decision nodes as `{{text}}` (diamonds)
  - Rounded rectangles as `(text)`
  - Regular nodes as `[text]`
  - Yes/No labels on edges originating from decision nodes (matched by direction angle)
- **1.2 Node List** — table of all nodes with ID, text, Mermaid symbol type, department
- **1.3 Edge List** — table of all connections with source, target, and labels

#### Part 2: Excel Table Data

- Cell contents from `UsedRange`, rendered as a Markdown table
- Empty columns are automatically filtered out

### How the Script Works (high-level)

1. Opens Excel via COM (`win32com.client.DispatchEx`)
2. For each target sheet:
   a. Scans all shapes — separates connectors from nodes by testing `ConnectorFormat.BeginConnected`
   b. Extracts text via `DrawingObject.Text` (most reliable) with fallbacks
   c. Resolves connector begin/end shapes, handling duplicate shape names via coordinate matching
   d. Identifies Yes/No text boxes and matches them to decision edges using direction-angle algorithm
   e. Detects swim-lane headers: non-connected shapes in the top row, assigns flow nodes by x-coordinate overlap
   f. Reads cell data from `UsedRange`
3. Generates Markdown with Mermaid flowchart and table sections
4. Closes Excel cleanly

### Troubleshooting

- **"Excel not found" error**: Ensure Microsoft Excel is installed (COM automation requires it)
- **Missing pywin32**: Run `pip install pywin32`
- **No shapes detected**: The sheet may not contain Shape objects — only table data will be output
- **Wrong swim-lane assignment**: Adjust the `TOP_TOLERANCE` constant in the script (default: 30pt)
