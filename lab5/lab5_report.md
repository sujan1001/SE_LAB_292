# Lab 5 static code analysis report

## Objective

This lab applies Pylint, Bandit, and Flake8 to the income-tax calculator,
documents the baseline findings, fixes genuine quality and security issues, and
verifies the cleaned source.

## Contents

| File | Purpose |
|---|---|
| `tax_calculator.py` | Cleaned Python source. |
| `pylint_report_before.txt` / `pylint_report_after.txt` | Pylint baseline and final output. |
| `bandit_report_before.txt` / `bandit_report_after.txt` | Bandit baseline and final output. |
| `flake8_report_before.txt` / `flake8_report_after.txt` | Flake8 baseline and final output. |
| `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` | Final report filenames requested by the handout. |
| `issues.md` | Issue table with findings, severity, and fixes. |
| `reflection.md` | Four reflection answers. |
| `requirements.txt` | Analyzer and program dependencies. |
| `RUN_IN_TERMINAL.md` | Copy-paste setup and verification commands. |

## Results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.57/10 | **10.00/10** |
| Bandit | 6 findings: 2 high, 3 medium, 1 low | **0 findings** |
| Flake8 | Multiple F/E violations | **0 violations** |

## Main fixes

- Replaced unsafe XML parsing with `defusedxml`.
- Removed the unused CGI handler flagged by Bandit.
- Replaced AES-ECB with AES-GCM and a random nonce.
- Increased RSA key generation from 1024 to 2048 bits.
- Removed unused imports/variables, added docstrings, and normalized names.
- Corrected the lower-tax regime selection, age-80 exemption, and rebate/cess
  behavior found during manual review.

## Verification

The program runs successfully, the final analyzers pass, and targeted checks
cover the rebate boundary, age-80 exemption, regime selection, exact PAN
validation, XML parsing, randomized encryption, and RSA key size.
