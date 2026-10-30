# Lab 6 Coverage Analysis

## Application inspected

The tested application is `bike_share_rental.py`, copied into this folder from
the teacher's public starter repository for a self-contained submission. It
contains three functions:

- `ride_cost`: validates bike type and duration, applies subscription, peak,
  bike-type, and long-ride pricing rules.
- `dock_status`: validates capacity/count and reports the dock state.
- `can_unlock`: checks active rides, age bands, and account-balance thresholds.

## Code/line coverage

The code-coverage test suite checks invalid inputs and representative valid
paths for all three functions. It reaches every executable application line,
including both return values for the subscriber short ride and every dock-state
result.

Command used:

```powershell
coverage run --source=bike_share_rental -m pytest CodeCoverageTest_292_application.py
coverage report -m
```

Result: 100% line coverage for `bike_share_rental.py`.

## Branch coverage

The branch-coverage test suite adds explicit cases for both outcomes of each
decision: invalid versus valid input, subscriber versus non-subscriber,
short versus long rides, peak versus non-peak pricing, cargo versus non-cargo,
all dock classifications, and every age/balance unlock outcome.

Command used:

```powershell
coverage run --branch --source=bike_share_rental -m pytest BranchCoverageTest_292_application.py
coverage report -m
```

Result: 100% line coverage and 100% branch coverage for
`bike_share_rental.py`.

The terminal evidence in `screenshots/` contains only successful reports at or
above the required 90% thresholds.
