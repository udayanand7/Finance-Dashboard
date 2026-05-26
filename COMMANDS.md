================================================================
  FINANCIAL DASHBOARD — Windows VS Code Terminal Commands
================================================================

STEP 1 — Open VS Code Terminal
--------------------------------
  In VS Code: press  Ctrl + `  (backtick)
  Make sure the terminal type is "Command Prompt" or "PowerShell"
  (You can switch at the top-right of the terminal panel)


STEP 2 — Navigate to the project folder
-----------------------------------------
  Replace the path below with wherever you unzipped the folder:

  cd C:\Users\YourName\Downloads\financial_dashboard


STEP 3 — Create a virtual environment
---------------------------------------
  python -m venv venv


STEP 4 — Activate the virtual environment
-------------------------------------------
  Command Prompt:
    venv\Scripts\activate.bat

  PowerShell:
    venv\Scripts\Activate.ps1

  You will see (venv) appear at the start of your terminal line.
  This means the virtual environment is active.

  NOTE — If PowerShell gives an error about execution policy, run:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  Then try activating again.


STEP 5 — Install required libraries
--------------------------------------
  pip install -r requirements.txt

  This installs: pandas, matplotlib, seaborn, openpyxl, numpy
  Wait for all packages to finish installing.


STEP 6 — Run the full pipeline (recommended)
----------------------------------------------
  python 05_automate.py

  This runs all 5 scripts in order automatically and produces:
  - 5 charts in reports/
  - 1 Excel summary file in reports/


  --- OR run each script individually step by step ---

  python 01_generate_data.py     <- creates data/sales_data.csv
  python 02_clean_data.py        <- cleans data, saves cleaned_data.csv
  python 03_analyze.py           <- prints analysis summaries
  python 04_visualize.py         <- saves 5 charts to reports/


STEP 7 — View your output
---------------------------
  Open the reports/ folder in File Explorer:
    start reports

  Or open a chart directly:
    start reports\01_monthly_trend.png

  Open the Excel report:
    start reports\summary_2024-01-15.xlsx
    (replace date with today's date)


================================================================
  TROUBLESHOOTING
================================================================

"python is not recognized"
  -> Install Python from https://www.python.org/downloads/
  -> During install, check "Add Python to PATH"
  -> Restart VS Code after installing

"pip is not recognized"
  -> Make sure the virtual environment is activated (Step 4)

"ModuleNotFoundError: No module named 'pandas'"
  -> Virtual environment is not activated, or install failed
  -> Run Step 4 again, then Step 5 again

Charts not showing on screen
  -> That's expected — charts are saved as PNG files to reports/
  -> Use  start reports\01_monthly_trend.png  to open them

================================================================
