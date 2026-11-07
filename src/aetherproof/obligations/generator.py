"""
Obligation Generator — Section 4.2 implementation.

Generates proof obligations from CSR records according to their
semantic role.
"""

from __future__ import annotations

from aetherproof.models import (
    CSRecord,
    Obligation,
    ObligationType,
    Layer,
)


def generate_obligations(record: CSRecord) -> list[Obligation]:
    """
    Generate obligations from a CSR record.

    Parameters
    ----------
    record : CSRecord
        The CSR record.

    Returns
    -------
    list[Obligation]
        Generated obligations.
    """
    if record.semantic_role == "invariant" and record.layer == Layer.L1:
        return [
            Obligation.create(
                property=f"Invariance({record.content})",
                assumptions=record.assumptions,
                source_csr=record.csr_id,
            )
        ]
    elif record.semantic_role == "contract" and record.layer == Layer.L2:
        return [
            Obligation.create(
                property=f"PrePost({record.content})",
                assumptions=record.assumptions,
                source_csr=record.csr_id,
            )
        ]
    elif record.semantic_role == "constraint" and record.layer == Layer.L3:
        return [
            Obligation.create(
                property=f"Satisfiability({record.content})",
                assumptions=record.assumptions,
                source_csr=record.csr_id,
            )
        ]
    elif record.semantic_role == "translation":
        return [
            Obligation.create(
                property=f"Consistency({record.content})",
                assumptions=record.assumptions,
                source_csr=record.csr_id,
            )
        ]
    else:
        return []


__all__ = ["generate_obligations"]
