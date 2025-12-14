import argparse;
import re;
import sys;
from pathlib import Path;
from html import escape;

from openpyxl import load_workbook;


# matches "1. Title", "0.1. Title", "2.1.3. Title" etc.
HEADING_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)\.\s*(.+?)\s*$");


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert an Excel template into a simple HTML document (headings + paragraphs)."
    );
    parser.add_argument(
        "xlsx",
        help="Path to the input .xlsx file (first sheet is used).",
    );
    parser.add_argument(
        "--additional",
        action="store_true",
        help=(
            "Include sections starting with 0.*. When enabled, the leading numbering "
            "for 0.* headings is removed in HTML."
        ),
    );

    args = parser.parse_args();

    xlsx_path = Path(args.xlsx);
    if not xlsx_path.exists():
        print(f"ERROR: Input file not found: {xlsx_path}", file=sys.stderr);
        return 2;
    if xlsx_path.suffix.lower() not in {".xlsx"}:
        print("ERROR: Please provide an .xlsx file.", file=sys.stderr);
        return 2;

    wb = load_workbook(xlsx_path);
    ws = wb.active;  # first sheet

    # output file next to input with same name
    out_path = xlsx_path.with_suffix(".html");

    parts: list[str] = [];
    parts.append("<!doctype html>");
    parts.append("<html lang='en'>");
    parts.append("<head>");
    parts.append("  <meta charset='utf-8' />");
    parts.append(f"  <title>{escape(xlsx_path.stem)}</title>");
    parts.append("  <meta name='viewport' content='width=device-width, initial-scale=1' />");
    parts.append("</head>");
    parts.append("<body>");

    # skip first row as it contains only headers
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if row_idx == 1:
            continue;

        # normalise row cells to strings/empty
        cells = [];
        for c in row:
            if c is None:
                cells.append("");
            else:
                cells.append(str(c).strip());

        # ignore empty row
        if not any(cells):
            continue;

        first = cells[0];
        if not first:
            # if no heading cell, ignore row
            continue;

        m = HEADING_RE.match(first);
        if not m:
            # if numbering scheme is wrong, default to h2
            heading_level = 2;
            heading_text = first;
            numeric_path = None;
        else:
            numeric_path = m.group(1);
            title_text = m.group(2);
            # number of dots corresponds to heading level
            total_dots = numeric_path.count(".") + 1;
            heading_level = min(6, total_dots + 1);

            # drop Argos (sub)sections if not specified by flag
            first_number = numeric_path.split(".", 1)[0];
            if not args.additional and first_number == "0":
                continue;

            # strip numbering from Argos (sub)sections if specified by flag to correspond to template
            if args.additional and first_number == "0":
                heading_text = title_text;
            else:
                # otherwise keep original heading text (with numbering)
                heading_text = first;

        parts.append(f"<h{heading_level}>{escape(heading_text)}</h{heading_level}>");

        # remaining cells become paragraphs under headings
        for cell_text in cells[1:]:
            if cell_text:
                parts.append(f"<p>{escape(cell_text)}</p>");

    parts.append("</body>");
    parts.append("</html>");

    out_path.write_text("\n".join(parts) + "\n", encoding="utf-8");
    print(f"Transformed {xlsx_path.resolve()} into {out_path.resolve()}.");
    return 0;


if __name__ == "__main__":
    raise SystemExit(main());
