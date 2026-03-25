# Power BI Cleanup & Hardening Workflow

## 1. Final Preparation
1. **Finalize the report**
2. **Save a pbix copy** for clean up

## 2. Model Cleanup (MK Measure Killer)
1. **Run MK**
2. **WARNING** some columns/ measures may be used in external queries (e.g., power automate, excel) that measure killer can't see.  As a rule of thumb, save DAX queries used in PowerAutomate, in the DAX query editor in power bi desktop; review these for dependencies downstream

### 2.1 OPTION TMDL Replacement (High Risk / High Reward)
> _“The brave — clean it all”_

1. **PBI**: Save as **pbip**
2. **MK**: Analyze
3. **MK**: Export **clean TMDL**
4. **File Explorer**: Replace the TMDL  
   (`xxxxx.SemanticModel\definition`)
5. **Review report function**; data will need refreshed
6. **Save back as pbix**
7. **⚠️ Warning**: unintended consequences  
   - e.g., disappearing **M-code functions** in Power Query

### 2.2 DAX Reduction (Calc Columns + Measures)
1. **Review unused DAX** in _Kill DAX Artificacts_
2. **Kill selected DAX artifacts**  
   - From **MK**  
   - **Acts directly on the model**
   - Can "restore"

### 2.3 M Code Reduction (by table)
1. **Remove columns** with large impact that will never be used
2. **Evaluate removal** of other columns
3. Columns are only **“killed” in M code**  
4. Use _Kill columns_ to obtain the M code with removed columns
   - _Date/ Datetime columns are kept if CALENDARAUTO is used_
6. Replace the M code in Power Query manually
5. **Recommended:** "remove other columns" to keep only the columns desired

### 2.4 Hide What Remains
1. **Hide everything** else that isn’t being used  
   - From **MK** using _Hide artifacts_
   - **Acts on the model**

## 3. Validation
1. **Review pbix** for proper function

## 4. Best Practice Analysis (Tabular Editor Best Practice Analyzer)
1. **Save copy of MK-cleaned pbix for TE application**
1. **Run TE BPA**
   1. Review **BPA rules** for fine tuning rules
   2. **Apply fix script**, **ignore item**, or **ignore rule**
   3. **Save TE** for changes to take effect

## 5. Final Verification
1. **Review pbix** for proper function
2. **Save MK-cleaned, TE_BPA'd, pbix** as final

## 6. Deployment
1. **Publish**
