"""
AetherMesh — Delta-state CRDT (Pillar 1).

Implements delta-state replication (Section 3.1.3 of the paper).

AetherMesh uses delta-state replication as its default: nodes ship
deltas that are themselves lattice elements, so duplication and
reordering remain harmless, and fall back to full-state exchange only
when a digest comparison indicates that incremental repair would cost
more than a state transfer.

This module provides:

    - DeltaStateCRDT:  the main CRDT class, operating on a Replica

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Sections 3.1.1 and 3.1.3.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

from aethermesh.models import Delta, Replica
from aethermesh.crdt.semilattice import DeltaSetLattice


class DeltaStateCRDT:
    """
    A delta-state CRDT over a `Replica`.

    The CRDT wraps a `Replica` (which holds the admitted delta set)
    and provides delta-based operations:

        - apply(delta):        join a single delta (idempotent)
        - apply_many(deltas):  join multiple deltas
        - merge(other):        join another CRDT's replica
        - delta_since(digest): the deltas the peer is missing
        - digest():            compact summary of local state
        - full_state():        the entire admitted set (fallback)

    The delta set lattice is the grow-only-set CRDT lifted to deltas
    (Section 3.1.1), with set union as join.
    """

    def __init__(self, origin: str = "anonymous"):
        self.replica = Replica(origin=origin)
        self._lattice = DeltaSetLattice()

    # -------------------------------------------------------------------------
    # Core operations
    # -------------------------------------------------------------------------

    def apply(self, delta: Delta) -> bool:
        """
        Join a single delta into the local replica.

        Returns True if the delta was newly admitted, False if it was
        already present (idempotence) or deferred (missing parents).

        A delta with missing parents is deferred (Section 3.3.2) — it is
        not rejected.
        """
        if delta.id in self.replica:
            return False

        if not self.replica.has_parents(delta):
            self.replica.deferred[delta.id] = delta
            return False

        self.replica.join(delta)
        self._try_drain_deferred()
        return True

    def apply_many(self, deltas: Iterable[Delta]) -> int:
        """Apply multiple deltas. Returns the count of newly admitted."""
        count = 0
        for d in deltas:
            if self.apply(d):
                count += 1
        return count

    def merge(self, other: "DeltaStateCRDT") -> int:
        """
        Merge another CRDT's replica into this one (set union).

        Returns the count of newly admitted deltas.
        """
        count = 0
        for did in other.replica.ids() - self.replica.ids():
            delta = other.replica.admitted[did]
            if self.apply(delta):
                count += 1
        return count

    # -------------------------------------------------------------------------
    # Delta exchange (Section 3.2.1)
    # -------------------------------------------------------------------------

    def digest(self) -> FrozenSet[str]:
        """
        A compact summary of local state: the set of admitted delta ids.

        In production, this would be compressed into a version vector,
        Merkle tree, or Bloom filter (Section 3.2.1). For the reference
        implementation we use the raw id set, which is exact.
        """
        return self.replica.ids()

    def delta_since(self, peer_digest: FrozenSet[str]) -> List[Delta]:
        """
        The deltas this replica has that the peer does not.

        Used in step 2 of the anti-entropy exchange (Figure 5): the
        responder returns "digest + list of deltas A appears to lack".
        """
        missing = self.replica.ids() - peer_digest
        return [self.replica.admitted[did] for did in missing]

    def full_state(self) -> List[Delta]:
        """
        The entire admitted set (state-based fallback).

        Used when a digest comparison indicates that incremental repair
        would cost more than a state transfer (Section 3.1.3).
        """
        return list(self.replica.admitted.values())

    # -------------------------------------------------------------------------
    # Deferred deltas (Section 3.3.2)
    # -------------------------------------------------------------------------

    def _try_drain_deferred(self) -> None:
        """
        Retry deferred deltas whose parents may now be present.

        Called after each successful join.
        """
        progress = True
        while progress:
            progress = False
            ready = [
                d for d in self.replica.deferred.values()
                if self.replica.has_parents(d)
            ]
            for d in ready:
                del self.replica.deferred[d.id]
                self.replica.join(d)
                progress = True

    def deferred_count(self) -> int:
        """Number of deltas currently deferred (missing parents)."""
        return len(self.replica.deferred)

    # -------------------------------------------------------------------------
    # Materialization
    # -------------------------------------------------------------------------

    def materialize(self) -> List[Delta]:
        """Deterministic linearization of the admitted delta set."""
        return self.replica.materialize()

    # -------------------------------------------------------------------------
    # Introspection
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.replica)

    def __contains__(self, delta_id: str) -> bool:
        return delta_id in self.replica

    def ids(self) -> FrozenSet[str]:
        return self.replica.ids()

    def state_size(self) -> int:
        """Number of admitted deltas."""
        return len(self.replica)


# =============================================================================
# Sanity check on the join laws (Figure 4 example)
# =============================================================================

if __name__ == "__main__":
    from aethermesh.crdt.semilattice import build_figure4_example, verify_join_laws

    lattice, elements = build_figure4_example()
    ok, violations = verify_join_laws(lattice, elements)
    print(f"Lattice elements: {len(elements)}")
    print(f"Join laws hold: {ok}")
    if violations:
        for v in violations[:5]:
            print(f"  - {v}")
