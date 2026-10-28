"""Income-tax calculator used for the Lab 5 static-analysis exercise."""

import base64
import os
import re
import secrets
from collections.abc import Mapping

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from defusedxml import minidom

# Slabs as configured for this program (modelled on FY 2025-26).
STANDARD_DEDUCTION_NEW = 75_000
STANDARD_DEDUCTION_OLD = 50_000
REBATE_LIMIT_NEW = 1_200_000
CESS = 0.04
PAN_PATTERN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")
NEW_SLABS = (
    (400_000, 0.0),
    (800_000, 0.05),
    (1_200_000, 0.10),
    (1_600_000, 0.15),
    (2_000_000, 0.20),
    (2_400_000, 0.25),
    (float("inf"), 0.30),
)
OLD_SLABS = (
    (500_000, 0.05),
    (1_000_000, 0.20),
    (float("inf"), 0.30),
)


def _load_pan_encryption_key() -> bytes:
    """Load a 256-bit PAN key or create an ephemeral demo key."""
    configured_key = os.getenv("PAN_ENCRYPTION_KEY")
    if configured_key is None:
        return secrets.token_bytes(32)

    try:
        key = bytes.fromhex(configured_key)
    except ValueError as error:
        raise ValueError(
            "PAN_ENCRYPTION_KEY must contain 64 hexadecimal characters"
        ) from error

    if len(key) != 32:
        raise ValueError("PAN_ENCRYPTION_KEY must be exactly 32 bytes")
    return key


PAN_ENCRYPTION_KEY = _load_pan_encryption_key()


def _progressive_tax(
    taxable_income: int,
    slabs: tuple[tuple[float, float], ...],
    tax_free_limit: int = 0,
) -> float:
    """Calculate tax progressively across the supplied slabs."""
    total_tax = 0.0
    lower_limit = tax_free_limit

    for upper_limit, rate in slabs:
        if taxable_income <= lower_limit:
            break
        upper_bound = min(taxable_income, upper_limit)
        taxable_in_slab = upper_bound - lower_limit
        if taxable_in_slab > 0:
            total_tax += taxable_in_slab * rate
        lower_limit = max(lower_limit, upper_limit)

    return total_tax


def slab_rate(taxable_income: int) -> float:
    """Return the marginal new-regime rate for an income amount."""
    for upper_limit, rate in NEW_SLABS:
        if taxable_income <= upper_limit:
            return rate
    return NEW_SLABS[-1][1]


def new_regime_tax(salary: int) -> int:
    """Calculate tax under the configured new-regime slabs."""
    taxable_income = max(0, salary - STANDARD_DEDUCTION_NEW)
    if taxable_income <= REBATE_LIMIT_NEW:
        return 0

    tax_amount = _progressive_tax(taxable_income, NEW_SLABS)
    return int(tax_amount * (1 + CESS))


def basic_exemption(age: int) -> int:
    """Return the old-regime basic exemption for the taxpayer's age."""
    if age >= 80:
        return 500_000
    if age >= 60:
        return 300_000
    return 250_000


def old_regime_tax(
    salary: int, age: int, deductions: Mapping[str, int]
) -> int:
    """Calculate tax under the configured old-regime slabs."""
    taxable_income = max(
        0, salary - STANDARD_DEDUCTION_OLD - sum(deductions.values())
    )
    tax_amount = _progressive_tax(
        taxable_income, OLD_SLABS, basic_exemption(age)
    )
    return int(tax_amount * (1 + CESS))


def better_regime(
    salary: int, age: int, deductions: Mapping[str, int]
) -> str:
    """Return the regime with the lower calculated tax."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)
    return "new" if new_tax < old_tax else "old"


def is_valid_pan(pan: str) -> bool:
    """Return whether a PAN contains exactly ten valid characters."""
    return bool(PAN_PATTERN.fullmatch(pan))


def encrypt_pan(pan: str) -> str:
    """Encrypt a PAN with AES-GCM and return a portable ciphertext."""
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(PAN_ENCRYPTION_KEY).encrypt(
        nonce, pan.encode("utf-8"), None
    )
    return base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")


def signing_key() -> rsa.RSAPrivateKey:
    """Generate a signing key with a currently accepted RSA size."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def parse_form_16(xml_text: str) -> tuple[int, int]:
    """Read salary and TDS from a Form-16 XML string safely."""
    document = minidom.parseString(xml_text)
    salary_nodes = document.getElementsByTagName("salary")
    tds_nodes = document.getElementsByTagName("tds")

    if len(salary_nodes) != 1 or len(tds_nodes) != 1:
        raise ValueError("Form 16 must contain one salary and one tds element")
    if salary_nodes[0].firstChild is None or tds_nodes[0].firstChild is None:
        raise ValueError("Form 16 salary and tds elements cannot be empty")

    salary = int(salary_nodes[0].firstChild.data.strip())
    tds = int(tds_nodes[0].firstChild.data.strip())
    return salary, tds


def main() -> None:
    """Print representative results for the lab demonstration."""
    deductions = {"80C": 200_000, "80D": 30_000}
    print("New regime, salary 12,75,000:", new_regime_tax(1_275_000))
    print("New regime, salary 18,00,000:", new_regime_tax(1_800_000))
    print(
        "Old regime, salary 18,00,000:",
        old_regime_tax(1_800_000, 35, deductions),
    )
    print("Better regime:", better_regime(1_800_000, 35, deductions))
    print("Basic exemption at age 80:", basic_exemption(80))
    print("PAN 'ABCDE1234FXYZ' valid?", is_valid_pan("ABCDE1234FXYZ"))
    first_ciphertext = encrypt_pan("ABCDE1234F")
    second_ciphertext = encrypt_pan("ABCDE1234F")
    print(
        "PAN ciphertexts use different nonces?",
        first_ciphertext != second_ciphertext,
    )
    print(
        "Form 16:",
        parse_form_16(
            "<form16><salary>1800000</salary>"
            "<tds>150000</tds></form16>"
        ),
    )
    print("Signing key size:", signing_key().key_size)


if __name__ == "__main__":
    main()
