"""
Guardrails — Section 6.5 implementation.

Five guardrails against specification gaming.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ViolationType(str, Enum):
    """Guardrail violation types (Section 6.5)."""
    TEST_DELETED = "test_deleted"
    TEST_DISABLED = "test_disabled"
    TOLERANCE_WIDENED = "tolerance_widened"
    OUTSIDE_BLAST_RADIUS = "outside_blast_radius"
    SPECIFICATION_WEAKENED = "specification_weakened"


@dataclass
class Patch:
    """A proposed remediation patch."""
    files_changed: set[str]
    deleted_tests: set[str]
    disabled_tests: set[str]
    widened_assertions: list[str]
    blast_radius: set[str]
    weakens_specification: bool = False


def check_guardrails(patch: Patch) -> list[ViolationType]:
    """
    Check a patch against the five guardrails.

    Returns a list of violations (empty if patch passes).
    """
    violations = []

    if patch.deleted_tests:
        violations.append(ViolationType.TEST_DELETED)

    if patch.disabled_tests:
        violations.append(ViolationType.TEST_DISABLED)

    if patch.widened_assertions:
        violations.append(ViolationType.TOLERANCE_WIDENED)

    if not patch.files_changed.issubset(patch.blast_radius):
        violations.append(ViolationType.OUTSIDE_BLAST_RADIUS)

    if patch.weakens_specification:
        violations.append(ViolationType.SPECIFICATION_WEAKENED)

    return violations


__all__ = ["check_guardrails", "ViolationType", "Patch"]
