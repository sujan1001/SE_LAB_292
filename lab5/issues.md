# Lab 5 issue table

The baseline reports were produced from the original `tax_calculator.py` before
editing. The final reports were produced from the cleaned source with the
repository virtual environment and the same analyzer commands.

| Issue | Type | Baseline line(s) | Description | Fix approach |
|---|---|---:|---|---|
| CGIHandler import and call | Bandit B412, high | 6, 92 | The CGI handler was flagged as having security implications. It was also unused by the demo program. | Removed the unused CGI entry point and import. |
| AES ECB mode | Bandit B305, medium | 77 | ECB does not provide semantic security because equal plaintext blocks produce equal ciphertext blocks. | Replaced ECB with AES-GCM and a fresh random nonce for every encryption. |
| RSA key size 1024 | Bandit B505, medium | 83 | A 1024-bit RSA key is considered breakable. | Increased the generated signing key to 2048 bits. |
| Unsafe XML parser | Bandit B408/B318, low/medium | 5, 86 | `xml.dom.minidom` was used for untrusted Form-16 XML. | Replaced it with `defusedxml.minidom` and added structural validation for salary and TDS nodes. |
| Bare exception | Pylint W0702 / Flake8 E722 | 73 | A bare `except` hid every possible failure and could mask programming errors. | Removed the exception-based validation and used anchored `fullmatch()` validation. |
| Unused imports and variables | Pylint W0611/W0612 / Flake8 F401/F841 | 2-4, 36 | Imports and temporary variables were not used. | Removed dead imports and calculated only values that are used. |
| Naming and documentation | Pylint C0114/C0116/C0103 | 1-106 | The module and functions lacked docstrings, and names used mixed casing. | Added docstrings and renamed functions/variables to snake_case. |
| Formatting violations | Flake8 E302/E305/E501/E702 | 16, 18, 34, 36, 98, 102-106 | The source had long lines, missing blank lines, and multiple statements per line. | Reformatted the source and wrapped long expressions. |
| Incorrect regime choice | Manual correctness finding | 64-67 | `betterRegime()` selected the higher tax amount instead of the lower one. | Compare the two tax amounts and return the regime with the lower result. |
| Incorrect age-80 exemption | Manual correctness finding | 44-48 | The original `> 80` condition gave age 80 the ordinary exemption. | Use `age >= 80` for the senior exemption. |
| Rebate still charged cess | Manual correctness finding | 36-41 | Cess was calculated before the rebate zeroed the tax amount. | Return zero before applying cess when the taxable income is within the rebate limit. |

## Verification summary

- Baseline Pylint score: **4.57/10**.
- Final Pylint score: **10.00/10**.
- Baseline Bandit findings: **6** across high, medium, and low severity.
- Final Bandit findings: **0**.
- Final Flake8 findings: **0**.
