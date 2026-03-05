#this script was created by CoPilot when running the ai prompt, as another option.  it's embedded_SQL results were pretty good

import os
import re
import sys
import math
import json
import hashlib
import difflib
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

import pandas as pd

ENTITY_REPLACEMENTS = {
    "&#13;": "\n",
    "&#10;": "\n",
    "&apos;": "'",
    "&quot;": '"',
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
}

def decode_xml_entities(s: str) -> str:
    if s is None:
        return ""
    # Tableau sometimes double-encodes; decode repeatedly until stable (bounded)
    prev = None
    cur = s
    for _ in range(5):
        prev = cur
        for k, v in ENTITY_REPLACEMENTS.items():
            cur = cur.replace(k, v)
        if cur == prev:
            break
    return cur

def normalize_sql_for_hash(sql: str) -> str:
    s = sql.lower()
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    s = re.sub(r"--[^\n]*", " ", s)
    s = re.sub(r"'([^']|'')*'", "''", s)  # collapse string literals
    s = re.sub(r"\b\d+(\.\d+)?\b", "0", s)  # collapse numerics
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sql_complexity(sql: str) -> str:
    s = sql.lower()
    score = 0
    score += len(re.findall(r"\bjoin\b", s)) * 2
    score += len(re.findall(r"\bunion\b", s)) * 3
    score += len(re.findall(r"\bselect\b", s)) * 1
    score += len(re.findall(r"\bwith\b", s)) * 3  # CTE
    score += len(re.findall(r"\bover\s*\(", s)) * 2  # window
    score += len(re.findall(r"\bpivot\b|\bunpivot\b", s)) * 4
    score += len(re.findall(r"\bcase\b", s)) * 1
    score += len(re.findall(r"\bexists\b|\bin\s*\(\s*select\b", s)) * 2
    score += len(re.findall(r"\bcross\s+database\b", s)) * 4

    # crude nesting proxy
    paren_depth = 0
    max_depth = 0
    for ch in s:
        if ch == "(":
            paren_depth += 1
            max_depth = max(max_depth, paren_depth)
        elif ch == ")":
            paren_depth = max(0, paren_depth - 1)
    score += max_depth

    if score <= 10:
        return "Low"
    if score <= 25:
        return "Medium"
    return "High"

def safe_text(e: Optional[ET.Element]) -> str:
    if e is None:
        return ""
    return decode_xml_entities("".join(e.itertext()).strip())

def findall_any_ns(root: ET.Element, tag: str) -> List[ET.Element]:
    # match regardless of namespace
    out = []
    for el in root.iter():
        if el.tag.split("}")[-1] == tag:
            out.append(el)
    return out

def attr(el: ET.Element, key: str) -> str:
    return el.attrib.get(key, "")

def nearest_caption_ancestor(el: ET.Element, max_up: int = 8) -> str:
    # ElementTree lacks parent pointers; we rebuild parent map once
    return ""  # placeholder; replaced after parent map created

def build_parent_map(root: ET.Element) -> Dict[ET.Element, ET.Element]:
    return {c: p for p in root.iter() for c in p}

def ancestor_with_attrib(el: ET.Element, parent_map: Dict[ET.Element, ET.Element],
                         keys=("caption", "name", "tablename", "table", "alias"),
                         max_up: int = 10) -> Tuple[str, str]:
    cur = el
    for _ in range(max_up):
        if cur is None:
            break
        for k in keys:
            if k in cur.attrib and cur.attrib.get(k):
                return (k, cur.attrib.get(k))
        cur = parent_map.get(cur)
    return ("", "")

def extract_datasource_connections(root: ET.Element) -> pd.DataFrame:
    rows = []
    for ds in findall_any_ns(root, "datasource"):
        ds_caption = attr(ds, "caption") or attr(ds, "name")
        # heuristic: "published" indicators sometimes live in repository-location / server tags
        repository_loc = None
        for rl in ds.iter():
            if rl.tag.split("}")[-1] == "repository-location":
                repository_loc = safe_text(rl) or json.dumps(rl.attrib) if rl.attrib else "present"
                break

        for conn in ds.iter():
            if conn.tag.split("}")[-1] == "connection":
                rows.append({
                    "Datasource Caption": ds_caption,
                    "Connection Class": attr(conn, "class"),
                    "Server": attr(conn, "server"),
                    "Database": attr(conn, "dbname") or attr(conn, "database"),
                    "Schema": attr(conn, "schema"),
                    "Authentication": attr(conn, "authentication"),
                    "Username": attr(conn, "username") or attr(conn, "user"),
                    "Port": attr(conn, "port"),
                    "ODBC Extras": attr(conn, "odbc-connect-string-extras") or attr(conn, "odbc_connect_string_extras"),
                    "Uses Extract (Y/N)": "Y" if any(x.tag.split('}')[-1] == "extract" for x in ds.iter()) else "N",
                    "Has Initial SQL (Y/N)": "Y" if any(x.tag.split('}')[-1] == "initial-sql" for x in conn.iter()) else "N",
                    "Initial SQL": "",
                    "Repository-Location Present": "Y" if repository_loc else "N",
                })
                # initial-sql can exist within connection
                for isql in conn.iter():
                    if isql.tag.split("}")[-1] == "initial-sql":
                        decoded = safe_text(isql)
                        if decoded:
                            rows[-1]["Initial SQL"] = decoded
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # Explicitly state none exists per datasource/connection if absent
    df["Initial SQL"] = df["Initial SQL"].fillna("")
    return df

def extract_relation_sql_blocks(root: ET.Element) -> pd.DataFrame:
    parent_map = build_parent_map(root)
    rows = []
    for rel in findall_any_ns(root, "relation"):
        if attr(rel, "type") == "text":
            sql_raw = safe_text(rel)
            sql_decoded = decode_xml_entities(sql_raw)
            k, v = ancestor_with_attrib(rel, parent_map)
            logical_hint = v

            rows.append({
                "Logical Table / Object": logical_hint,
                "SQL Definition": sql_decoded,
                "SQL Type": "Embedded Custom SQL",
                "Estimated Complexity": sql_complexity(sql_decoded),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # De-dup exact
    df["Normalized SQL"] = df["SQL Definition"].map(normalize_sql_for_hash)
    df["SQL Hash"] = df["Normalized SQL"].map(lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest())
    return df

def extract_worksheets_and_dependencies(root: ET.Element) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # worksheet -> datasource -> fields -> referenced table-ish attributes if present
    ws_rows = []
    dep_rows = []
    for ws in findall_any_ns(root, "worksheet"):
        ws_name = attr(ws, "name")
        # datasource-dependencies may exist under worksheet
        for dd in ws.iter():
            if dd.tag.split("}")[-1] == "datasource-dependencies":
                for col in dd.iter():
                    if col.tag.split("}")[-1] in ("column", "field"):
                        dep_rows.append({
                            "Worksheet": ws_name,
                            "Datasource": attr(col, "datasource"),
                            "Field Name": attr(col, "name") or attr(col, "caption"),
                            "Table": attr(col, "table") or attr(col, "tablename") or attr(col, "remote-name"),
                            "Role": attr(col, "role"),
                        })
        ws_rows.append({"Worksheet": ws_name})
    return (pd.DataFrame(ws_rows), pd.DataFrame(dep_rows))

def extract_dashboards_and_sheets(root: ET.Element) -> pd.DataFrame:
    # Dashboards are usually in <dashboard> with <zone> references to worksheets.
    rows = []
    dashboards = findall_any_ns(root, "dashboard")
    for db in dashboards:
        db_name = attr(db, "name")
        # find worksheet references inside dashboard zones
        for z in db.iter():
            if z.tag.split("}")[-1] == "zone":
                ws_ref = attr(z, "name") or attr(z, "worksheet")
                if ws_ref:
                    rows.append({"Dashboard": db_name, "Sheet": ws_ref})
    return pd.DataFrame(rows)

def extract_modern_relationships(root: ET.Element) -> pd.DataFrame:
    # Best-effort: look for <relationship> elements
    rows = []
    parent_map = build_parent_map(root)

    for rel in findall_any_ns(root, "relationship"):
        # Attempt to find left/right table captions and clause fields
        left = attr(rel, "left") or ""
        right = attr(rel, "right") or ""
        rtype = attr(rel, "type") or attr(rel, "relationship-type") or ""

        # Sometimes clauses are nested <clause> <expression> etc.
        join_field = ""
        operator = ""
        for clause in rel.iter():
            tag = clause.tag.split("}")[-1]
            if tag in ("clause", "join", "expression"):
                # Pull any meaningful attributes
                join_field = join_field or (attr(clause, "field") or attr(clause, "column") or "")
                operator = operator or (attr(clause, "op") or attr(clause, "operator") or "")

        # If left/right not present, climb for hints
        if not left or not right:
            _, hint = ancestor_with_attrib(rel, parent_map)
            if hint and not (left or right):
                left = hint

        if left or right or rtype:
            rows.append({
                "Left Logical Table": left,
                "Relationship Type": rtype,
                "Join Field": join_field,
                "Operator": operator,
                "Right Logical Table": right,
            })
    return pd.DataFrame(rows)

def build_dashboard_logical_table_mapping(dash_df: pd.DataFrame, dep_df: pd.DataFrame) -> pd.DataFrame:
    # Deterministic mapping per your rule: Worksheet -> Field -> table -> Logical Table
    # We only have "table-ish" tokens; map "Table" tokens to "Logical Table" by identity here,
    # and let you refine if you also provide a parser output that includes r_fields.table_clean.
    if dash_df.empty and dep_df.empty:
        return pd.DataFrame(columns=["Dashboard","Sheet","Datasource","Logical Table (logical-layer caption)"])

    merged = dash_df.merge(dep_df, left_on="Sheet", right_on="Worksheet", how="left")
    merged["Logical Table (logical-layer caption)"] = merged["Table"].fillna("")
    out = merged[["Dashboard", "Sheet", "Datasource", "Logical Table (logical-layer caption)"]].drop_duplicates()
    out = out[out["Logical Table (logical-layer caption)"] != ""]
    return out

def near_duplicate_groups(df_sql: pd.DataFrame, threshold: float = 0.92) -> List[List[int]]:
    # group near-duplicates using normalized SQL similarity
    norms = df_sql["Normalized SQL"].tolist()
    used = set()
    groups = []
    for i in range(len(norms)):
        if i in used:
            continue
        g = [i]
        used.add(i)
        for j in range(i+1, len(norms)):
            if j in used:
                continue
            r = difflib.SequenceMatcher(a=norms[i], b=norms[j]).ratio()
            if r >= threshold:
                g.append(j)
                used.add(j)
        if len(g) > 1:
            groups.append(g)
    return groups

def main(twb_path: str, out_dir: str, write_sql_files: bool = False):
    os.makedirs(out_dir, exist_ok=True)
    tree = ET.parse(twb_path)
    root = tree.getroot()

    conn_df = extract_datasource_connections(root)
    sql_df = extract_relation_sql_blocks(root)
    dash_df = extract_dashboards_and_sheets(root)
    ws_df, dep_df = extract_worksheets_and_dependencies(root)
    rel_df = extract_modern_relationships(root)

    mapping_df = build_dashboard_logical_table_mapping(dash_df, dep_df)

    summary = {
        "datasources_processed": int(conn_df["Datasource Caption"].nunique()) if not conn_df.empty else 0,
        "connections_rows": int(len(conn_df)),
        "dashboards_found": int(dash_df["Dashboard"].nunique()) if not dash_df.empty else 0,
        "dashboard_sheet_pairs": int(len(dash_df)),
        "worksheets_found": int(ws_df["Worksheet"].nunique()) if not ws_df.empty else 0,
        "dependency_rows": int(len(dep_df)),
        "sql_blocks_extracted": int(len(sql_df)),
        "relationship_rows": int(len(rel_df)),
    }

    # Duplicate & near-duplicate SQL reporting
    dup_counts = {}
    near_dups = []
    if not sql_df.empty:
        dup_counts = sql_df["SQL Hash"].value_counts().to_dict()
        exact_dups = {h:c for h,c in dup_counts.items() if c > 1}

        groups = near_duplicate_groups(sql_df, threshold=0.92)
        for g in groups:
            near_dups.append({
                "group_size": len(g),
                "rows": g,
                "hashes": [sql_df.loc[idx, "SQL Hash"] for idx in g],
                "objects": [sql_df.loc[idx, "Logical Table / Object"] for idx in g],
            })

        summary["exact_duplicate_sql_hashes"] = len(exact_dups)
        summary["near_duplicate_groups"] = len(near_dups)

    # Write Excel workbook
    xlsx_path = os.path.join(out_dir, "tableau_twb_extraction.xlsx")
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as w:
        mapping_df.to_excel(w, sheet_name="Dashboard_LogicalTable_Map", index=False)
        if not sql_df.empty:
            sql_export = sql_df.drop(columns=["Normalized SQL"], errors="ignore")
            sql_export.to_excel(w, sheet_name="Embedded_SQL", index=False)
        conn_df.to_excel(w, sheet_name="Connection_Details", index=False)
        rel_df.to_excel(w, sheet_name="Logical_Relationships", index=False)
        dep_df.to_excel(w, sheet_name="Worksheet_Dependencies", index=False)
        pd.DataFrame([summary]).to_excel(w, sheet_name="Summary_Counts", index=False)

    # Optional: write one .sql file per logical object label (best-effort)
    if write_sql_files and not sql_df.empty:
        sql_out_dir = os.path.join(out_dir, "sql_by_object")
        os.makedirs(sql_out_dir, exist_ok=True)
        for obj, g in sql_df.groupby("Logical Table / Object"):
            label = obj.strip() or "UnknownObject"
            safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", label)[:120]
            p = os.path.join(sql_out_dir, f"{safe}.sql")
            with open(p, "w", encoding="utf-8") as f:
                for _, row in g.iterrows():
                    f.write(row["SQL Definition"].rstrip() + "\n\n-- ======\n\n")

    # Write duplicate report JSON
    dup_path = os.path.join(out_dir, "sql_duplicates.json")
    with open(dup_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "near_duplicate_groups": near_dups}, f, indent=2)

    print("Wrote:", xlsx_path)
    print("Wrote:", dup_path)
    print("Summary:", json.dumps(summary, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tableau_twb_extract.py <workbook.twb> <output_dir> [--write-sql-files]")
        sys.exit(1)
    twb = sys.argv[1]
    out = sys.argv[2]
    write_sql = "--write-sql-files" in sys.argv[3:]
    main(twb, out, write_sql_files=write_sql)
