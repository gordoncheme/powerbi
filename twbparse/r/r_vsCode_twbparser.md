# Tableau TWBX Parsing with R (VS Code)

This guide describes how to parse a Tableau `.twbx` file using **R**, **VS Code**, and the **twbparser** package, starting from a machine with nothing installed and ending with CSV outputs written to disk.

This workflow assumes the parsing logic is contained in an existing R script named `run_twbparser.R`.

---

## 1. Install R

1. Open a web browser and navigate to:  
   https://cran.r-project.org/bin/windows/base/

2. Click **Install R for Windows**.

3. Download the installer and run it.

4. Accept all default options.

5. If prompted for administrator privileges, install for your user.

6. Complete the installation.

---

## 2. Install Visual Studio Code

1. Navigate to:  
   https://code.visualstudio.com/

2. Download the **Windows installer**.

3. Run the installer and complete the installation using **default options**.

---

## 3. Install the R Extension in VS Code

1. Launch **Visual Studio Code**.

2. Open the **Extensions** view.

3. Search for **R**.

4. Install the extension published by **REditorSupport**.

5. Restart **VS Code** if prompted.

---

## 4. Open the Project Folder

Open the folder that contains:

- the Tableau `.twbx` file  
- the `run_twbparser.R` script

Steps:

1. Select **File → Open Folder**.
2. Choose the directory containing the files.

This folder will become the **working directory for R**.

---

## 5. Create an R Terminal in VS Code

1. Open the **Command Palette**.
2. Run the command:

```
R: Create R Terminal
```

A terminal panel will open at the bottom of VS Code with an **R prompt**.

---

## 6. Install Required R Packages

Run the following command in the **R terminal**.

Select a **CRAN mirror** if prompted.

```r
install.packages(c("twbparser", "readr", "dplyr"))
```

---

## 7. Confirm the Working Directory

Run the following commands in the **R terminal**:

```r
getwd()
list.files()
```

The output should show:

- the `.twbx` file
- `run_twbparser.R`

If they are not present:

1. Close the **R terminal**.
2. Ensure the correct folder is opened in VS Code.
3. Create the **R terminal** again.

---

## 8. Confirm the Parsing Script Exists

Ensure the file `run_twbparser.R` exists in the working directory.

This script is responsible for:

- prompting the user for inputs
- parsing the `.twbx` file using **twbparser**
- writing CSV outputs to an output folder

---

## 9. Run the Parsing Script

Execute the following command in the **R terminal**:

```r
source("run_twbparser.R")
```

---

## 10. Provide Script Inputs

When prompted by the script:

### TWBX File Path

Enter the path to the `.twbx` file.

The path may be entered:

- with quotes
- without quotes

If the `.twbx` file is located in the working directory, entering **just the filename** is sufficient.

Example:

```
example_dashboard.twbx
```

### Output Directory

When prompted for the output directory name:

Press **Enter** to accept the default unless a different name is desired.

---

## 11. Allow the Script to Complete

Allow the script to finish execution.

Progress and status messages will appear in the **R terminal**.

When finished, the script will indicate:

- processing is complete
- the name of the output directory

---

## 12. Verify the Results

Inspect the output directory created by the script in the **VS Code Explorer**.

Default output directory:

```
twbparser_out
```

This directory should contain CSV files representing extracted Tableau metadata.

Typical outputs include:

- datasources
- fields
- calculated fields
- joins
- relationships
- pages
- page summaries
- custom SQL

---

## Final State

At this point:

- **R is installed**
- **VS Code is configured**
- **Required packages are installed**
- **The Tableau `.twbx` file has been parsed**
- **The `twbparser` results are available as CSV files on disk**
