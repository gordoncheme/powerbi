# Tableau TWB Parsing with Python

This document describes how to parse a Tableau `.twb` file using **Python**, starting from a machine with nothing installed and ending with structured Tableau parser results available as **JSON** and **Excel** files.

This workflow uses **Python 3.11.x** (specifically any version less than **3.13**) and assumes the parsing logic is contained in existing Python scripts named:

- `run_twb_parse.py`
- `json_to_excel.py`

---

## 1. Install Python

Start from a machine with nothing installed.

1. Open a web browser and navigate to:  
   https://www.python.org/downloads/

2. Download **Python 3.11.14** (or any **Python 3.11.x** release less than **3.13**).

3. Run the Windows installer.

4. Ensure the option **“Add Python to PATH”** is checked.

5. Complete the installation.

---

## 2. Verify Python Installation

Open **Command Prompt** and run:

```
python --version
```

Confirm that the reported version is:

```
3.11.x
```

Ensure the version is **not 3.13 or newer**.

---

## 3. Create a Working Directory

Create or choose a working directory that will contain:

- the Tableau `.twb` file
- the Python scripts
- the generated outputs

Place the Tableau `.twb` file you want to parse into this directory.

---

## 4. Place the Parser Scripts in the Directory

Ensure the following scripts are present in the same working directory:

```
run_twb_parse.py
json_to_excel.py
```

These scripts are responsible for:

- parsing the Tableau workbook
- producing a structured JSON representation
- converting that JSON into an Excel file

---

## 5. Review Script Configuration

Open `run_twb_parse.py` in a text editor.

Review:

- file locations
- target output behavior

Update any **hard-coded paths** or **target directories** so outputs are written to the desired location.

Save the file after making changes.

---

## 6. Review Excel Conversion Script

Open `json_to_excel.py` in a text editor.

Verify or update any:

- target directories
- file locations used by the script

Save the file after making changes.

---

## 7. Open Command Prompt in the Working Directory

Open **Command Prompt**.

Change the current directory to the working directory that contains:

- the `.twb` file
- the Python scripts

Example:

```
cd C:\path\to\your\working_directory
```

---

## 8. Run the Tableau Parsing Script

Execute the parsing script:

```
python run_twb_parse.py
```

The script will:

- display an opening message describing its purpose
- prompt you to enter the full path to the Tableau `.twb` file

Enter the path when prompted.

Quotes are optional.

Example:

```
C:\path\to\your\file.twb
```

The script will analyze the Tableau workbook and create a **structured JSON file** in the target directory.

---

## 9. Confirm JSON Output

Verify that the **JSON output file** has been created.

This JSON file represents the parsed Tableau workbook and serves as the **intermediate format** for further processing.

---

## 10. Convert JSON to Excel

Run the Excel conversion script:

```
python json_to_excel.py
```

This script will:

- read the previously created JSON file
- flatten the structure
- write the contents to an **Excel `.xlsx` file** in the target directory

---

## 11. Verify Final Results

Inspect the **target directory**.

You should now have:

```
parsed_workbook.json
parsed_workbook.xlsx
```

These files together represent the **Tableau parser results**.

---

## Final State

At this stage:

- **Python is installed**
- **The Tableau `.twb` file has been successfully parsed**
- **A structured JSON output has been generated**
- **The JSON has been converted into an Excel file**

You now have the complete **TWB parser results** available for analysis or downstream use.
