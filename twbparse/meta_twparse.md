# Tableau Workbook Migration Analysis — Orchestrated Workflow (Python + R + AI)

This document describes the overall orchestration workflow for performing a deterministic, enterprise-grade technical extraction and migration assessment of a Tableau workbook in preparation for conversion to Power BI, Fabric, or another modern BI platform.

This document does **not** contain detailed execution steps for Python parsing, R parsing, or AI analysis. Instead, it explains **how and when to use each tool**, and how their outputs are combined to produce the final migration assessment.

The user is expected to follow three separate instruction documents:

- **Python parsing instructions** (`py_parse`)
- **R parsing instructions** (`r_parse`)
- **AI analysis instructions and prompt** (`ai_parse`)

This document defines the **order of operations**, **required artifacts**, and **handoff points** between those steps.

---

# Overall Objective

The objective of this workflow is to perform a **complete technical extraction and migration assessment** of a Tableau workbook so that it can be rebuilt in **Power BI, Fabric, or another modern BI platform**.

The final outcome must support a **deterministic migration** and include:

- Dashboard → Sheet → Datasource → Logical Table mapping  
- Full embedded SQL inventory  
- Datasource connection and initial-SQL details  
- Logical table relationship model  
- Migration complexity and effort assessment  

---

# High-Level Workflow Summary

The workflow consists of **three sequential phases**:

1. **Python parsing** (structure-first extraction)  
2. **R parsing** (Tableau-native metadata extraction)  
3. **AI analysis** (synthesis and migration assessment)  

Each phase produces artifacts that are **required inputs to the next phase**.

---

# Phase 0 — Required Tableau Preparation (Mandatory)

Before any parsing is performed, the user must complete the **Tableau preparation steps** defined in the **AI analysis instructions**.

These include, at minimum:

- Replacing all **published datasources** with **embedded datasources**
- Switching extracts to **LIVE connections** if SQL detail is required
- Saving the workbook as a **`.twb` file** (not `.twbx`)

If these steps are skipped, **SQL, connection details, and relationship definitions may be incomplete or inaccessible**, and the migration assessment will be **invalid**.

---

# Phase 1 — Python Parsing (`py_parse`)

The first execution phase uses **Python** to produce a **normalized, machine-readable structural representation** of the Tableau workbook.

To perform this step:

- Follow the **Python parsing instruction document**
- Use **Python 3.11.x** (less than **3.13**)
- Execute `run_twb_parse.py` to generate a structured JSON representation of the `.twb` file
- Execute `json_to_excel.py` to convert the JSON into an Excel workbook

### Primary Outputs from this Phase

- Python-generated **JSON file** representing the Tableau object model  
- Python-generated **Excel file** derived from that JSON  

These outputs serve as the **authoritative structural reference** for:

- dashboards  
- worksheets  
- datasources  
- logical tables  
- SQL blocks  

Do **not proceed to the next phase** until Python parsing outputs have been **successfully generated and verified**.

---

# Phase 2 — R Parsing (`r_parse`)

The second execution phase uses **R** to extract **Tableau-native metadata** using the `twbparser` library.

To perform this step:

- Follow the **R parsing instruction document**
- Use the **same `.twb` file** used in Python parsing
- Execute `run_twbparser.R` to generate structured CSV outputs

### Primary Outputs from this Phase

- Datasource metadata CSV  
- Field and calculated field CSVs  
- Logical relationship CSVs  
- Page and dashboard metadata CSVs  
- Custom SQL extraction CSVs  

These outputs provide **Tableau-specific semantics** that complement the **Python structural model**.

Do **not modify Python outputs during this phase**.  
Python and R outputs must remain **independently reproducible**.

---

# Phase 3 — AI Analysis (`ai_parse`)

The final execution phase uses **AI** to synthesize the Python outputs, R outputs, and Tableau XML into a **migration-ready technical assessment**.

To perform this step:

- Follow the **AI analysis instruction document**
- Use the provided **AI prompt exactly as specified**
- Provide the AI with the following artifacts:

### Required Inputs

- The `.twb` file (**preferred**), or the TWB XML saved as `.txt` or `.docx`
- Python parser **JSON output**
- Python parser **Excel output**
- R parser **CSV outputs**
- (Optional) **Example results**

---

# AI Analysis Outputs

The AI uses these inputs to produce:

- Dashboard → Sheet → Datasource → Logical Table mappings  
- Fully decoded embedded SQL inventory  
- Datasource connection and initial-SQL reports  
- Logical table relationship models  
- Migration complexity and effort assessment  
- Power BI **star schema recommendations and migration order**

The AI output is the **final synthesis layer** and should **not be generated without validated Python and R inputs**.

---

# Final Deliverables

At the completion of all three phases, the user will have:

- **Python parser results** (JSON and Excel)  
- **R parser results** (CSV metadata extracts)  
- **AI-generated migration assessment and structured outputs**

Together, these artifacts form a **complete, deterministic foundation** for:

- Tableau → Power BI conversion planning  
- Implementation sequencing  
- Risk assessment  

---

# Completion State

When all referenced instruction documents have been executed **in order** and their outputs combined via **AI analysis**, the user has successfully completed the **end-to-end Tableau workbook extraction and migration assessment workflow**.

At this point, the **`twb_parser` results from Python, R, and AI are complete** and ready to be used for **Tableau to Power BI conversion planning and execution**.

---

Provide your feedback on **BizChat**.
