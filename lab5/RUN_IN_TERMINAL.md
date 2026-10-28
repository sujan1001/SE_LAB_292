# Lab 5 terminal instructions

Run these commands from the repository root.

## Windows PowerShell

```powershell
cd lab5
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tax_calculator.py
python -m pylint tax_calculator.py 2>&1 | Tee-Object pylint_report_after.txt
python -m bandit -r tax_calculator.py 2>&1 | Tee-Object bandit_report_after.txt
python -m flake8 tax_calculator.py 2>&1 | Tee-Object flake8_report_after.txt
Copy-Item -Force pylint_report_after.txt pylint_report.txt
Copy-Item -Force bandit_report_after.txt bandit_report.txt
Copy-Item -Force flake8_report_after.txt flake8_report.txt
```

If PowerShell blocks activation, run the tools directly instead:

```powershell
.\.venv\Scripts\python.exe tax_calculator.py
.\.venv\Scripts\python.exe -m pylint tax_calculator.py
.\.venv\Scripts\python.exe -m bandit -r tax_calculator.py
.\.venv\Scripts\python.exe -m flake8 tax_calculator.py
```

## macOS/Linux

```bash
cd lab5
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tax_calculator.py
python -m pylint tax_calculator.py 2>&1 | tee pylint_report_after.txt
python -m bandit -r tax_calculator.py 2>&1 | tee bandit_report_after.txt
python -m flake8 tax_calculator.py 2>&1 | tee flake8_report_after.txt
cp pylint_report_after.txt pylint_report.txt
cp bandit_report_after.txt bandit_report.txt
cp flake8_report_after.txt flake8_report.txt
```

## Expected final results

- Pylint: **10.00/10**.
- Bandit: **No issues identified**; zero findings.
- Flake8: no output and exit status `0`.

The `*_before.txt` files are the untouched-source baseline. Keep them as-is so
the before/after comparison remains available.

## Optional Git commands

From the repository root, review and publish the work with:

```bash
git status
git log --oneline -5
git push origin main
```
