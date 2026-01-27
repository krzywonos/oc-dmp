import argparse
import html
import re
import sys
from pathlib import Path

from openpyxl import load_workbook
import markdown as md

# Helpers

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8");


def md_to_html(markdown_text: str) -> str:
    return md.markdown(
        markdown_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "sane_lists",
        ],
        output_format="html5",
    );


def cell_to_str(value) -> str:
    if value is None:
        return "";
    return str(value).strip();


def heading_level_from_numbering(text: str) -> int | None:
    """
    "1. Title"     -> h1
    "1.1. Title"   -> h2
    "1.1.1. Title" -> h3
    """
    numbering = text.strip();
    matched_numbering = re.match(r"^\s*(\d+(?:\.\d+)*)\.\s+.+", numbering); # regex is AI-generated
    if not matched_numbering:
        return None;
    segments = matched_numbering.group(1).split(".");
    return max(1, min(6, len(segments)));


TRIPLE_CODE_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)\.\s*(.*)$"); # regex is AI-generated


def parse_triple_code(text: str):
    """
    Matches:
      "1.3.1. Something" or "1.3.1."
    """
    numbering = text.strip();
    matched_numbering = TRIPLE_CODE_RE.match(numbering);
    if not matched_numbering:
        return None
    major = int(matched_numbering.group(1));
    sub = int(matched_numbering.group(2));
    item = int(matched_numbering.group(3));
    rest = (matched_numbering.group(4) or "").strip();
    code = f"{major}.{sub}.{item}.";
    return {"code": code, "major": major, "sub": sub, "item": item, "rest": rest};


def normalise_type_choice(input_string: str) -> str:
    normalised_input = (input_string or "").strip().lower();
    if normalised_input == "dataset":
        return "dataset";
    if normalised_input == "software":
        return "software";
    if normalised_input == "object":
        return "object";
    return "";


def should_include_section2(sub: int, choice: str) -> bool:
    """
    Dataset  -> include 2.1.* and 2.2.*
    Software -> include 2.3.* and 2.4.*
    Object   -> include 2.5.* and 2.6.*
    Unknown  -> include all 2.*
    """
    if not choice:
        return True;
    if choice == "dataset":
        return sub in {1, 2};
    if choice == "software":
        return sub in {3, 4};
    if choice == "object":
        return sub in {5, 6};
    return True;

# Parsers

def parse_general_dmp_xlsx(path: Path) -> str:
    """
    Parses general information about DMP from general_dmp.xlsx.
    Headers are made from column A starting with cell A2.
    Paragraphs under the headers are made from subsequent columns in the same row.
    """
    workbook = load_workbook(path, data_only=True);
    worksheet = workbook.active;

    parts: list[str] = [];
    max_row = worksheet.max_row;
    max_col = worksheet.max_column;

    for row in range(2, max_row + 1):
        title = cell_to_str(worksheet.cell(row=row, column=1).value);
        if not title:
            continue;

        parts.append(f"<h3>{html.escape(title)}</h3>");

        for col in range(2, max_col + 1):
            value = cell_to_str(worksheet.cell(row=row, column=col).value);
            if not value:
                continue;
            parts.append(f"<p>{html.escape(value)}</p>");

    return "\n".join(parts);


def parse_data_table_xlsx(path: Path) -> str:
    """
    Parses DMP data for the research output from data_table.xlsx.
    Headers are taken from cells in the first row.
    Paragraphs for sections are taken from the cells in the same column.
    Paragraph begins with the name of the research output specified in the same row in column A.
    Section 1.3.2. is currently hard-coded, as it is acting as a switch statement for which subsection in section 2 to include.
    """
    workbook = load_workbook(path, data_only=True);

    worksheet = workbook["Main data sheet"] if "Main data sheet" in workbook.sheetnames else workbook.active;

    max_row = worksheet.max_row;
    max_col = worksheet.max_column;

    # headers from row 1, columns B..end
    col_headers: dict[int, str] = {};
    for col in range(2, max_col + 1):
        col_headers[col] = cell_to_str(worksheet.cell(row=1, column=col).value);

    # find selector column (header starts with 1.3.2.)
    selector_col = None;
    for col, header in col_headers.items():
        triple = parse_triple_code(header);
        if triple and triple["code"] == "1.3.2.":
            selector_col = col;
            break;

    parts: list[str] = [];

    for col in range(2, max_col + 1):
        header = col_headers.get(col, "");
        if not header:
            continue;

        # emit numbered headings (h1/h2/...)
        lvl = heading_level_from_numbering(header);
        if lvl is not None:
            parts.append(f"<h{lvl}>{html.escape(header)}</h{lvl}>");

        # only triple-coded columns produce row-based paragraphs
        triple = parse_triple_code(header);
        if not triple:
            continue;

        code = triple["code"];
        major = triple["major"];
        sub = triple["sub"];

        paras: list[str] = [];
        for r in range(2, max_row + 1):
            row_label = cell_to_str(worksheet.cell(row=r, column=1).value)
            if not row_label:
                continue;

            val = cell_to_str(worksheet.cell(row=r, column=col).value);
            if not val:
                continue;

            # apply special filtering to section 2 columns only
            if major == 2 and selector_col is not None:
                choice = normalise_type_choice(cell_to_str(worksheet.cell(row=r, column=selector_col).value));
                if not should_include_section2(sub=sub, choice=choice):
                    continue;

            paras.append(f"<p>{html.escape(row_label)} - {html.escape(val)}</p>");

        # only emit the <h3>code</h3> if there is something under it
        if paras:
            parts.extend(paras);

    return "\n".join(parts);


# assembly

def build_full_html(data_dir: Path) -> str:
    """
    
    """
    required = [
        "introduction.md",
        "general_dmp.xlsx",
        "data.md",
        "data_table.xlsx",
        "conclusion.md",
        "acknowledgements.md",
        "references.md",
    ];

    missing = [name for name in required if not (data_dir / name).exists()];
    if missing:
        raise FileNotFoundError(
            "Missing required input files in data directory:\n  - "
            + "\n  - ".join(missing)
        );

    parts: list[str] = [];

    parts.append(md_to_html(read_text_file(data_dir / "introduction.md")));
    parts.append(parse_general_dmp_xlsx(data_dir / "general_dmp.xlsx"));
    parts.append(md_to_html(read_text_file(data_dir / "data.md")));
    parts.append(parse_data_table_xlsx(data_dir / "data_table.xlsx"));
    parts.append(md_to_html(read_text_file(data_dir / "conclusion.md")));
    parts.append(md_to_html(read_text_file(data_dir / "acknowledgements.md")));
    parts.append(md_to_html(read_text_file(data_dir / "references.md")));

    body = "\n\n".join(parts);

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>DMP</title>
  <style>
    body {{
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.35;
      margin: 32px;
    }}
    h1, h2, h3, h4, h5, h6 {{
      margin-top: 1.1em;
      margin-bottom: 0.4em;
    }}
    p {{
      margin: 0.2em 0 0.8em 0;
      white-space: pre-wrap; /* preserves Excel line breaks */
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
""";


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate dmp.html from Markdown + Excel inputs.");
    parser.add_argument(
        "--data",
        dest="data_dir",
        default=None,
        help="Path to folder containing input files. If omitted, uses the script's directory.",
    );
    args = parser.parse_args();

    script_dir = Path(__file__).resolve().parent;
    data_dir = Path(args.data_dir).resolve() if args.data_dir else script_dir;

    try:
        html_out = build_full_html(data_dir);
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr);
        return 1;

    out_path = script_dir / "dmp.html";
    out_path.write_text(html_out, encoding="utf-8");
    print(f"Written: {out_path}");
    return 0;


if __name__ == "__main__":
    raise SystemExit(main());
