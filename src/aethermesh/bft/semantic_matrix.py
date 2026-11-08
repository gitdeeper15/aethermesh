"""
AetherMesh — Semantic compatibility matrix (Pillar 3, Section 3.3.3).

A compatibility matrix C assigns to each pair of operation kinds a
verdict on whether concurrent deltas of those kinds that touch
overlapping targets may coexist.

The matrix is evaluated locally and cheaply, which is what makes the
admission layer lightweight. It is also coarse: it classifies operation
kinds, not program behaviour, and it cannot detect semantic breakage
that depends on program meaning.

This module provides:

    - SemanticVerdict:    enum (ok, resolve, conflict)
    - CompatibilityMatrix:  the matrix itself
    - DEFAULT_MATRIX:     the illustrative matrix from Table 3.1

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 3.3.3 and Table 3.1.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Optional, Tuple

from aethermesh.models import DeltaKind


# =============================================================================
# SemanticVerdict
# =============================================================================

class SemanticVerdict(str, Enum):
    """The three possible verdicts of the semantic compatibility matrix."""
    OK = "ok"
    RESOLVE = "resolve"    # deterministic resolution required
    CONFLICT = "conflict"  # reject or quarantine


# =============================================================================
# CompatibilityMatrix
# =============================================================================

@dataclass
class CompatibilityMatrix:
    """
    A compatibility matrix over operation kinds.

    The matrix is symmetric: C[a][b] == C[b][a] for all a, b.

    Reference: Table 3.1 of the paper.
    """
    entries: Dict[Tuple[DeltaKind, DeltaKind], SemanticVerdict] = field(
        default_factory=dict
    )

    def set(
        self,
        a: DeltaKind,
        b: DeltaKind,
        verdict: SemanticVerdict,
    ) -> None:
        """Set a matrix entry (both directions)."""
        self.entries[(a, b)] = verdict
        self.entries[(b, a)] = verdict

    def get(
        self,
        a: DeltaKind,
        b: DeltaKind,
    ) -> SemanticVerdict:
        """
        Get the verdict for a pair of kinds. Defaults to OK if unset.
        """
        return self.entries.get((a, b), SemanticVerdict.OK)

    def check(self, deltas: list) -> Tuple[SemanticVerdict, str]:
        """
        Check a set of deltas for semantic compatibility.

        Returns the worst verdict among all pairs:
            - If any pair is CONFLICT, returns CONFLICT.
            - Else if any pair is RESOLVE, returns RESOLVE.
            - Else returns OK.

        The reason string lists the conflicting pair (if any).
        """
        worst = SemanticVerdict.OK
        worst_pair: Optional[Tuple[str, str]] = None

        for i, d_i in enumerate(deltas):
            for d_j in deltas[i + 1:]:
                v = self.get(d_i.kind, d_j.kind)
                if v == SemanticVerdict.CONFLICT:
                    if worst != SemanticVerdict.CONFLICT:
                        worst = SemanticVerdict.CONFLICT
                        worst_pair = (d_i.kind.value, d_j.kind.value)
                elif v == SemanticVerdict.RESOLVE:
                    if worst == SemanticVerdict.OK:
                        worst = SemanticVerdict.RESOLVE
                        worst_pair = (d_i.kind.value, d_j.kind.value)

        if worst == SemanticVerdict.OK:
            return worst, "ok"
        if worst_pair:
            return worst, f"{worst.value}: {worst_pair[0]} vs {worst_pair[1]}"
        return worst, worst.value


# =============================================================================
# Default matrix (Table 3.1 of the paper)
# =============================================================================

def _build_default_matrix() -> CompatibilityMatrix:
    """Build the illustrative matrix from Table 3.1 of the paper."""
    m = CompatibilityMatrix()
    OK = SemanticVerdict.OK
    RESOLVE = SemanticVerdict.RESOLVE
    CONFLICT = SemanticVerdict.CONFLICT

    # Edit body
    m.set(DeltaKind.EDIT_BODY, DeltaKind.EDIT_BODY, OK)
    m.set(DeltaKind.EDIT_BODY, DeltaKind.RENAME_SYMBOL, OK)
    m.set(DeltaKind.EDIT_BODY, DeltaKind.DELETE_SYMBOL, CONFLICT)
    m.set(DeltaKind.EDIT_BODY, DeltaKind.CHANGE_SIGNATURE, OK)
    m.set(DeltaKind.EDIT_BODY, DeltaKind.EDIT_METADATA, OK)

    # Rename symbol
    m.set(DeltaKind.RENAME_SYMBOL, DeltaKind.RENAME_SYMBOL, RESOLVE)
    m.set(DeltaKind.RENAME_SYMBOL, DeltaKind.DELETE_SYMBOL, CONFLICT)
    m.set(DeltaKind.RENAME_SYMBOL, DeltaKind.CHANGE_SIGNATURE, CONFLICT)
    m.set(DeltaKind.RENAME_SYMBOL, DeltaKind.EDIT_METADATA, OK)

    # Delete symbol
    m.set(DeltaKind.DELETE_SYMBOL, DeltaKind.DELETE_SYMBOL, OK)  # idempotent
    m.set(DeltaKind.DELETE_SYMBOL, DeltaKind.CHANGE_SIGNATURE, CONFLICT)
    m.set(DeltaKind.DELETE_SYMBOL, DeltaKind.EDIT_METADATA, OK)

    # Change signature
    m.set(DeltaKind.CHANGE_SIGNATURE, DeltaKind.CHANGE_SIGNATURE, RESOLVE)
    m.set(DeltaKind.CHANGE_SIGNATURE, DeltaKind.EDIT_METADATA, OK)

    # Edit metadata
    m.set(DeltaKind.EDIT_METADATA, DeltaKind.EDIT_METADATA, RESOLVE)  # LWW

    return m


DEFAULT_MATRIX: CompatibilityMatrix = _build_default_matrix()
"""The illustrative compatibility matrix from Table 3.1 of the paper."""
