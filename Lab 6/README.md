# Lab 6: Code and Branch Coverage

This folder contains the Lab 6 deliverables for `SE_LAB_292`. The application
under test is a local copy of the teacher-provided bike-share rental module;
the teacher repository was used only as the read-only source application.

## Files

| File | Purpose |
| --- | --- |
| `bike_share_rental.py` | Application under test |
| `CodeCoverageTest_292_application.py` | Tests used for line/code coverage |
| `BranchCoverageTest_292_application.py` | Tests that exercise both outcomes of the application's decisions |
| `screenshots/code_coverage_report.png` | Successful line/code coverage terminal report |
| `screenshots/branch_coverage_report.png` | Successful branch coverage terminal report |
| `coverage_analysis.md` | Commands, results, and interpretation |

## Run the tests

From this folder:

```powershell
python -m pytest CodeCoverageTest_292_application.py
coverage run --source=bike_share_rental -m pytest CodeCoverageTest_292_application.py
coverage report -m

python -m pytest BranchCoverageTest_292_application.py
coverage run --branch --source=bike_share_rental -m pytest BranchCoverageTest_292_application.py
coverage report -m
```

The final reports shown in the screenshots are the successful runs after the
coverage thresholds were met. `.coverage` and cache files are intentionally not
part of the deliverables.
