# Lab 5 reflection

## 1. What is the purpose of each static-analysis tool?

Pylint acts as a broad code-quality reviewer. It checks naming, documentation,
unused code, control flow, and maintainability concerns. Flake8 focuses on
Python syntax and PEP 8 formatting, so it catches issues such as unused imports,
long lines, missing blank lines, and multiple statements on one line. Bandit
looks specifically for security-sensitive patterns, such as weak cryptography,
unsafe XML parsing, and risky modules.

## 2. Which findings were the most important, and why?

The highest-priority findings were the high-severity CGIHandler warnings and the
cryptography findings. ECB mode could reveal repeated patterns, a 1024-bit RSA
key is too weak for a new signing operation, and untrusted XML should not be
parsed with the standard library's vulnerable parser. These issues could affect
confidentiality or integrity, so they were fixed before style-only findings.

## 3. How did static analysis improve the program?

The tools made the source easier to read and safer to change by exposing dead
imports, unused variables, inconsistent names, missing documentation, and
formatting problems. The review also encouraged a manual behavior check, which
found that the original regime comparison chose the higher tax, age 80 received
the wrong exemption, and the rebate path still applied cess. The final code is
more explicit, progressively calculates slabs, validates XML structure, and
uses authenticated encryption.

## 4. What are the limitations of static analysis, and what would you do next?

Static analysis cannot prove that tax rules are legally current or that every
input and business case is correct. It also cannot replace runtime tests,
dependency review, secret-management practices, or human review. Next I would
add unit tests for slab boundaries, rebate boundaries, age 60/80 boundaries,
malformed XML, and PAN validation; run the tests in continuous integration; and
provide a persistent production key through a secret manager rather than the
ephemeral demo fallback used when no environment key is configured.
