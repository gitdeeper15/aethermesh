"""
AetherMesh — Join-semilattice for delta sets (Pillar 1).

Implements the bounded join-semilattice (S, ⊔, ⊥) that underlies the
CRDT state space (Definition 2, Section 4.2 of the paper):

    s_reconciled = s_i ⊔ s_j

The join operator must satisfy:

    - Commutative:  s_i ⊔ s_j = s_j ⊔ s_i
    - Associative:  (s_i ⊔ s_j) ⊔ s_k = s_i ⊔ (s_j ⊔ s_k)
    - Idempotent:   s_i ⊔ s_i = s_i
    - Inflationary: s ⊑ s ⊔ t

This module provides:

    - JoinSemilattice:  abstract base class
    - DeltaSetLattice:  concrete implementation for sets of deltas
    - verify_join_laws: exhaustive check on a finite lattice (cf. Figure 4)

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Sections 3.1.2 and 4.2.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Iterable, List, Set, Tuple, TypeVar


T = TypeVar("T")


class JoinLawError(Exception):
    """Raised when a lattice fails to satisfy one of the join laws."""
    pass


# =============================================================================
# Abstract base
# =============================================================================

class JoinSemilattice(ABC, Generic[T]):
    """
    Abstract join-semilattice (S, ⊔, ⊥).

    Subclasses must implement `join` and `bottom`, and may override
    `leq` for efficiency (default: s ⊑ t iff s ⊔ t == t).
    """

    @abstractmethod
    def join(self, a: T, b: T) -> T:
        """Binary join operator (commutative, associative, idempotent)."""
        ...

    @abstractmethod
    def bottom(self) -> T:
        """The bottom element ⊥ (identity of join)."""
        ...

    def leq(self, a: T, b: T) -> bool:
        """Partial order s ⊑ t iff s ⊔ t == t."""
        return self.join(a, b) == b

    def join_all(self, items: Iterable[T]) -> T:
        """Iterated join ⨆ over a set of elements (Definition 1)."""
        result = self.bottom()
        for item in items:
            result = self.join(result, item)
        return result


# =============================================================================
# Concrete: delta-set lattice
# =============================================================================

class DeltaSetLattice(JoinSemilattice[frozenset]):
    """
    The grow-only-set CRDT lifted to deltas (Section 3.1.1 of the paper).

    State space:  power set of the delta universe D, ordered by inclusion.
    Join:         set union.
    Bottom:       empty set.

    This is the lattice over which `Replica` operates. Its height is
    |D|, so every ascending chain is finite (assumption A3).
    """

    def join(self, a: frozenset, b: frozenset) -> frozenset:
        return a | b

    def bottom(self) -> frozenset:
        return frozenset()


# =============================================================================
# Law verification
# =============================================================================

def verify_join_laws(
    lattice: JoinSemilattice[T],
    elements: List[T],
    verbose: bool = False,
) -> Tuple[bool, List[str]]:
    """
    Exhaustively verify the three join laws on a finite set of elements.

    This mirrors the exhaustive enumeration used in Figure 4 of the
    paper, where the three join laws were checked on a seven-element
    bounded join-semilattice.

    Args:
        lattice:   A JoinSemilattice instance.
        elements:  Finite list of lattice elements to test on.
        verbose:   If True, print each violation as it is found.

    Returns:
        (ok, violations) — ok is True iff all laws hold; violations is
        a list of human-readable descriptions of any failures.
    """
    violations: List[str] = []

    # --- Commutativity: s_i ⊔ s_j == s_j ⊔ s_i ---
    for a, b in itertools.product(elements, repeat=2):
        lhs = lattice.join(a, b)
        rhs = lattice.join(b, a)
        if lhs != rhs:
            msg = f"Commutativity violated: {a} ⊔ {b} = {lhs}, but {b} ⊔ {a} = {rhs}"
            violations.append(msg)
            if verbose:
                print(msg)

    # --- Associativity: (s_i ⊔ s_j) ⊔ s_k == s_i ⊔ (s_j ⊔ s_k) ---
    for a, b, c in itertools.product(elements, repeat=3):
        lhs = lattice.join(lattice.join(a, b), c)
        rhs = lattice.join(a, lattice.join(b, c))
        if lhs != rhs:
            msg = f"Associativity violated: ({a} ⊔ {b}) ⊔ {c} = {lhs}, but {a} ⊔ ({b} ⊔ {c}) = {rhs}"
            violations.append(msg)
            if verbose:
                print(msg)

    # --- Idempotence: s_i ⊔ s_i == s_i ---
    for a in elements:
        if lattice.join(a, a) != a:
            msg = f"Idempotence violated: {a} ⊔ {a} = {lattice.join(a, a)}, expected {a}"
            violations.append(msg)
            if verbose:
                print(msg)

    # --- Bottom is identity: ⊥ ⊔ s == s and s ⊔ ⊥ == s ---
    bottom = lattice.bottom()
    for a in elements:
        if lattice.join(bottom, a) != a:
            msg = f"Bottom-left identity violated: ⊥ ⊔ {a} = {lattice.join(bottom, a)}, expected {a}"
            violations.append(msg)
            if verbose:
                print(msg)
        if lattice.join(a, bottom) != a:
            msg = f"Bottom-right identity violated: {a} ⊔ ⊥ = {lattice.join(a, bottom)}, expected {a}"
            violations.append(msg)
            if verbose:
                print(msg)

    # --- Inflationary: s ⊑ s ⊔ t ---
    for a, b in itertools.product(elements, repeat=2):
        joined = lattice.join(a, b)
        if not lattice.leq(a, joined):
            msg = f"Inflationary violated: {a} ⊑ {a} ⊔ {b} = {joined} is False"
            violations.append(msg)
            if verbose:
                print(msg)

    return (len(violations) == 0, violations)


# =============================================================================
# Convenience: build the 7-element example from Figure 4
# =============================================================================

def build_figure4_example() -> Tuple[DeltaSetLattice, List[frozenset]]:
    """
    Build the seven-element bounded join-semilattice from Figure 4 of
    the paper (Hasse diagram).

    Elements:
        ⊥ (bottom) = {}
        s1 = {a}
        s2 = {b}
        s3 = {c}
        s12 = {a, b}
        s23 = {b, c}
        ⊤ (top) = {a, b, c}

    Note: In the paper's figure, s1 ⊔ s3 = ⊤ because the only common
    upper bound is ⊤. This is exactly what DeltaSetLattice does.
    """
    lattice = DeltaSetLattice()
    bottom: frozenset = lattice.bottom()
    a, b, c = "a", "b", "c"
    s1 = frozenset([a])
    s2 = frozenset([b])
    s3 = frozenset([c])
    s12 = lattice.join(s1, s2)
    s23 = lattice.join(s2, s3)
    top = lattice.join(lattice.join(s1, s2), s3)

    elements = [bottom, s1, s2, s3, s12, s23, top]
    return lattice, elements
