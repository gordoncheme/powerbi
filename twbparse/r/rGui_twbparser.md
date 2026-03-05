# Tableau TWBX Parsing with R (RGui)

This document describes how to parse a Tableau `.twbx` file using **R** and the **twbparser** package, starting from a machine with nothing installed and ending with CSV outputs written to disk.

This workflow uses **RGui only** and assumes the parsing logic is contained in an existing R script named `run_twbparser.R`.

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

## 2. Launch RGui

1. Open the **Windows Start Menu**.

2. Search for **R**.

3. Start **R x64** (or **R**).

4. The **R Console window** should appear.

---

## 3. Install Required R Packages

Run the following command in the **R console**.  
Select a **CRAN mirror** if prompted.

```r
install.packages(c("twbparser", "readr", "dplyr"))
```

---

## 4. Set the Working Directory

Set the working directory to the folder that contains:

- the Tableau `.twbx` file
- the `run_twbparser.R` script

### Option A — Using the RGui Menu

1. Select **File → Change dir…**
2. Navigate to the appropriate folder
3. Click **OK**

### Option B — Using an R Command

```r
setwd("C:/full/path/to/your/folder")
```

---

## 5. Verify the Working Directory

Run the following commands:

```r
getwd()
list.files()
```

The output should show:

- the `.twbx` file  
- `run_twbparser.R`

---

## 6. Confirm the Parsing Script Exists

Ensure the file `run_twbparser.R` exists in the working directory.

This script is responsible for:

- prompting the user for inputs
- parsing the `.twbx` file using **twbparser**
- writing CSV outputs to an output folder

---

## 7. Run the Parsing Script

Execute the following command in the **R console**:

```r
source("run_twbparser.R")
```

---

## 8. Provide Script Inputs

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

## 9. Allow the Script to Complete

Allow the script to finish execution.

Upon completion, a message will indicate:

- that processing is finished
- the name of the output directory

---

## 10. Verify the Results

Inspect the output directory created by the script.

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
- **Required packages are installed**
- **The Tableau `.twbx` file has been parsed**
- **The `twbparser` results are available as CSV files on disk**
