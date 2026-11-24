# R9.6 test runbook — when Work is unavailable

All scripts use Python's standard library. Python 3.11 or later is recommended. No pip install is required for the R9.6 audit, SVG generation, or unit tests.

## Preferred: GitHub Actions

The branch contains .github/workflows/r96-audit.yml. Pushing a commit to this branch should trigger the pipeline automatically.

The pipeline runs R7 → R9.3 → R9.1/R9.2 → R9.4 → R9.5 → R9.6 SVG generation → unit tests, then commits regenerated CSV/SVG outputs back to this branch. It never pushes to main.

If the run does not start:
1. Open the repository on GitHub.
2. Select the Actions tab.
3. If GitHub displays an enable/allow prompt, enable Actions for the repository.
4. Open the R9.6 workflow and inspect the latest run.
5. If the workflow is not listed, check that .github/workflows/r96-audit.yml exists on the branch and that Actions are permitted by repository settings.

## Local Windows PowerShell

From the repository root:

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python 06_S0_Calculation/r7_s0_co2_scenarios.py
python 06_S0_Calculation/r9_3_ncm622_battery_lci.py
python 06_S0_Calculation/r9_3_legacy_beijing_bus_lci.py
python 06_S0_Calculation/r9_lci_foreground.py
python 06_S0_Calculation/r9_lci_passenger_car_module.py
python 06_S0_Calculation/r9_lci_bus_use_module.py
python 06_S0_Calculation/r9_4_integrate_lci.py
python 06_S0_Calculation/r9_5_sensitivity.py
python 06_S0_Calculation/r9_6_generate_figures.py
python -m unittest discover -s tests -v
~~~

If PowerShell blocks activation, either run Set-ExecutionPolicy -Scope Process Bypass for the current terminal, or skip activation and call the virtual-environment interpreter directly:

~~~powershell
.\.venv\Scripts\python.exe 06_S0_Calculation/r7_s0_co2_scenarios.py
~~~

Run the remaining commands with the same interpreter.

## Local Windows CMD

~~~cmd
py -3.11 -m venv .venv
.venv\Scripts\python.exe 06_S0_Calculation/r7_s0_co2_scenarios.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_3_ncm622_battery_lci.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_3_legacy_beijing_bus_lci.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_lci_foreground.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_lci_passenger_car_module.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_lci_bus_use_module.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_4_integrate_lci.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_5_sensitivity.py
.venv\Scripts\python.exe 06_S0_Calculation/r9_6_generate_figures.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
~~~

## What to send back if a test fails

Do not edit generated CSVs by hand. Send:
- the workflow run URL or the full terminal error;
- the failing step name;
- the first traceback line and the final 20–30 lines of output;
- if the failure concerns a CSV, its header plus the first two data rows.

I can then correct the script on this branch and rerun the audit. Do not merge this branch into main as part of the test.
