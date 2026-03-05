from pathlib import Path
import json
import pandas as pd
from tableau_parser import analyze_tableau_workbook


def show_opening_message() -> None:
    print(
        "This program takes a Tableau .twb file, parses its contents, "
        "and outputs two files:\n"
        "1) A structured JSON representation of the workbook\n"
        "2) An Excel (.xlsx) file created from that JSON\n"
    )


def get_twb_path() -> Path:
    path_str = input(
        'Enter full path to the .twb file (quotes optional): '
    ).strip()
    path_str = path_str.strip('"')
    return Path(path_str)


def parse_tableau_workbook(twb_path: Path) -> Path:
    result = analyze_tableau_workbook(str(twb_path))
    out_json = twb_path.with_suffix(".tableau-parser.json")
    out_json.write_text(
        result.model_dump_json(indent=4),
        encoding="utf-8",
    )
    print("created json file")
    return out_json


def flatten(obj, prefix=""):
    rows = []

    if isinstance(obj, dict):
        row = {}
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                rows.extend(flatten(v, prefix=f"{prefix}{k}."))
            else:
                row[f"{prefix}{k}"] = v
        if row:
            rows.append(row)

    elif isinstance(obj, list):
        for v in obj:
            rows.extend(flatten(v, prefix=prefix))

    return rows


def json_to_excel(json_path: Path) -> Path:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    rows = flatten(data)
    df = pd.DataFrame(rows)

    out_xlsx = json_path.with_suffix(".xlsx")
    df.to_excel(out_xlsx, index=False)

    print("created xlsx file")
    return out_xlsx


def main() -> None:
    show_opening_message()
    twb_path = get_twb_path()
    json_path = parse_tableau_workbook(twb_path)
    json_to_excel(json_path)


if __name__ == "__main__":
    main()
