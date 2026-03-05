
# Objective

Perform a complete technical extraction and migration assessment of a Tableau workbook so that it can be rebuilt in Power BI, Fabric, or another modern BI platform.

The goal is to extract:

1) Dashboard → Sheet → Datasource → Logical Table mapping  
2) All embedded SQL  
3) All datasource connection details (including initial-SQL if present)  
4) Logical table relationships  
5) Migration complexity assessment  

The output should support a deterministic, enterprise-grade migration.

---

# CRITICAL PREPARATION STEP (REQUIRED FOR FULL SQL EXTRACTION)

Before providing the workbook:

1) Replace ALL published datasources with local (embedded) copies:
   - In Tableau Desktop:
     - Data → Replace Data Source (if needed)
     - Convert published datasource to embedded
   - Ensure the datasource is no longer pointing to Tableau Server

2) If SQL detail is required:
   - Switch extracts to LIVE connections
   - Extracts can hide connection-level SQL and physical query detail

3) Save the workbook as:
   - `.twb` (NOT `.twbx`)
   - This separates dashboard structure from embedded extract and image content
   - `.twb` exposes full XML clearly for deterministic parsing

Without these steps:
- Published datasource SQL will NOT be visible
- Initial-SQL may NOT be accessible
- Physical join definitions may be incomplete

---

# Required Output

## 1) Dashboard → Logical Table Mapping

Return a structured table:

Dashboard | Sheet | Datasource | Logical Table (logical-layer caption)

Rules:
- Logical tables must reflect ObjectModelTableType caption names
- Do NOT use legacy “Custom SQL Query1” names
- Only include logical-layer tables
- Exclude unused logical tables

Also provide:
1) Excel workbook of the mapping
2) Identification of logical tables unused in the analyzed dashboards
3) Optional relationship diagram

---

## 2) Embedded SQL Inventory

Return a structured table:

Logical Table / Object | SQL Definition | SQL Type | Estimated Complexity | Used in Worksheets

Where:
- Logical Table / Object = ObjectModelTableType caption (preferred)
- SQL Definition = Fully decoded SQL (no XML entities such as &#13;, &apos;, &amp;)
- SQL Type = Embedded Custom SQL / Legacy Custom SQL / Initial SQL / Extract SQL
- Estimated Complexity = Low / Medium / High
- Used in Worksheets = If determinable

Also provide:
1) Excel workbook containing all embedded SQL
2) One `.sql` file per logical table (if requested)
3) Count of total SQL blocks extracted
4) Identification of duplicate or near-duplicate SQL blocks

---

## 3) Datasource Connection Detail Report

Return a structured table:

Datasource Caption | Connection Class | Server | Database | Schema | Authentication | Username | Port | ODBC Extras | Uses Extract (Y/N) | Has Initial SQL (Y/N)

If `<initial-sql>` exists:
- Extract and decode it
- Associate it to the correct datasource

If no `<initial-sql>` exists:
- Explicitly state that none exists

Also provide:
1) Excel workbook of connection details
2) Identification of embedded vs previously published datasources
3) Extract vs Live summary
4) Security observations (embedded credentials, plaintext servers)

---

## 4) Logical Table Relationships

Return a structured table:

Left Logical Table | Relationship Type | Join Field | Operator | Right Logical Table

Based only on modern logical layer (relationship model), not physical joins.

Also provide:
- Optional diagram of relationships
- Fact vs Dimension classification (if inferable)
- Relationship cardinality inference (if inferable)

---

## 5) Migration Assessment

Provide:

1) Fact vs Dimension classification
2) Estimated migration effort per logical table (Low / Medium / High)
3) Identification of:
   - Complex PIVOT logic
   - Nested subqueries
   - Cross-database joins
   - Session-dependent logic
4) Recommended Power BI star schema structure
5) Suggested migration order (priority list)
6) Estimated overall migration complexity rating

---

# Knowledge Sources (User Must Provide One or More)

User must provide AFTER performing preparation steps:

- `.twb` file (preferred)
- TWB XML saved as `.txt`
- TWB XML saved as `.docx`

Optional:
- Embedded `.tds` file (if datasource separated)
- Python `tableau_parser` output
- R `twbparser` outputs

---

# Required Extraction Method

## Logical Table Mapping

If raw field references are not provided via parser:
→ Extract worksheet field references directly from TWB XML (`<datasource-dependencies>`)

Map:
Worksheet → Field → r_fields.table_clean → Logical Table

Exclude:
- Physical joins
- Legacy custom SQL names
- Unused logical tables

---

## Embedded SQL

Search entire XML for:

- `<relation type='text'>`

Extract:
- Logical table caption
- Full SQL block
- Decode XML entities:
  - &#13;
  - &apos;
  - &amp;

Preserve formatting.

---

## Initial SQL

Search entire XML for:

- `<initial-sql>`

If present:
- Extract and decode
- Associate to correct datasource

If absent:
- Explicitly report none exists

---

## Connection Details

Within each `<datasource>` block, extract from `<connection>`:

- class
- server
- dbname
- schema
- authentication
- username
- port
- odbc-connect-string-extras
- connection type
- extract vs live indicator

Return one row per connection if multiple exist.

---

# Exclusions

Do NOT:
- Attempt to reconstruct physical database DDL
- Infer SQL Server view definitions
- Include worksheet layout or UI formatting
- Include physical join XML unless explicitly requested

---

# Expected Behavior

If XML is large:
- Process deterministically
- Confirm number of SQL blocks extracted
- Confirm number of datasources processed
- Confirm number of logical tables identified

If datasources remain published:
- Explicitly report that SQL and connection details are not accessible
- Instruct user to embed datasource and resubmit

---

# Optional Follow-Up Questions

After extraction, ask:

- Would you like CREATE VIEW wrappers generated?
- Would you like DAX translation for calculations?
- Would you like a migration cost estimate?
- Would you like security risk scoring?
- Would you like a technical debt assessment?
