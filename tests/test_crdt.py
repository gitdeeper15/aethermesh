"""
Tests for aethermesh.crdt — semilattice and delta-state CRDT.

Covers:
    - Join laws (commutative, associative, idempotent)
    - Figure 4 example (7 elements)
    - DeltaStateCRDT apply/merge idempotence
    - Deferred deltas (missing parents)
    - Digest and delta_since
"""

import pytest

from aethermesh.models import Delta, DeltaKind
from aethermesh.crdt.semilattice import (
    DeltaSetLattice,
    build_figure4_example,
    verify_join_laws,
)
from aethermesh.crdt.delta_state import DeltaStateCRDT


# =============================================================================
# Join laws
# =============================================================================

class TestJoinLaws:
    def test_figure4_example_has_7_elements(self):
        _, elements = build_figure4_example()
        assert len(elements) == 7

    def test_join_laws_hold_on_figure4(self):
        lattice, elements = build_figure4_example()
        ok, violations = verify_join_laws(lattice, elements)
        assert ok is True
        assert len(violations) == 0

    def test_commutativity(self):
        lattice = DeltaSetLattice()
        a = frozenset({"x"})
        b = frozenset({"y"})
        assert lattice.join(a, b) == lattice.join(b, a)

    def test_associativity(self):
        lattice = DeltaSetLattice()
        a = frozenset({"x"})
        b = frozenset({"y"})
        c = frozenset({"z"})
        assert lattice.join(lattice.join(a, b), c) == lattice.join(a, lattice.join(b, c))

    def test_idempotence(self):
        lattice = DeltaSetLattice()
        a = frozenset({"x"})
        assert lattice.join(a, a) == a

    def test_bottom_is_identity(self):
        lattice = DeltaSetLattice()
        a = frozenset({"x"})
        bottom = lattice.bottom()
        assert lattice.join(bottom, a) == a
        assert lattice.join(a, bottom) == a

    def test_inflationary(self):
        lattice = DeltaSetLattice()
        a = frozenset({"x"})
        b = frozenset({"y"})
        assert lattice.leq(a, lattice.join(a, b))


# =============================================================================
# DeltaStateCRDT
# =============================================================================

class TestDeltaStateCRDT:
    def test_apply_single(self):
        crdt = DeltaStateCRDT(origin="a")
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        assert crdt.apply(d) is True
        assert crdt.state_size() == 1

    def test_apply_idempotent(self):
        crdt = DeltaStateCRDT(origin="a")
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        crdt.apply(d)
        assert crdt.apply(d) is False
        assert crdt.state_size() == 1

    def test_apply_many(self):
        crdt = DeltaStateCRDT(origin="a")
        deltas = [
            Delta.create(body={"op": f"edit-{i}"}, origin="a", kind=DeltaKind.EDIT_BODY)
            for i in range(5)
        ]
        count = crdt.apply_many(deltas)
        assert count == 5
        assert crdt.state_size() == 5

    def test_merge(self):
        crdt_a = DeltaStateCRDT(origin="a")
        crdt_b = DeltaStateCRDT(origin="b")

        d1 = Delta.create(body={"op": "a1"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "b1"}, origin="b", kind=DeltaKind.EDIT_BODY)
        crdt_a.apply(d1)
        crdt_b.apply(d2)

        count = crdt_a.merge(crdt_b)
        assert count == 1
        assert crdt_a.state_size() == 2

    def test_deferred_missing_parents(self):
        crdt = DeltaStateCRDT(origin="a")
        orphan = Delta.create(
            body={"op": "child"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={"missing"},
        )
        assert crdt.apply(orphan) is False
        assert crdt.state_size() == 0
        assert crdt.deferred_count() == 1

    def test_deferred_drains_when_parent_arrives(self):
        crdt = DeltaStateCRDT(origin="a")
        parent = Delta.create(body={"op": "parent"}, origin="a", kind=DeltaKind.EDIT_BODY)
        child = Delta.create(
            body={"op": "child"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={parent.id},
        )

        # Child arrives first -> deferred.
        assert crdt.apply(child) is False
        assert crdt.deferred_count() == 1

        # Parent arrives -> child is drained.
        assert crdt.apply(parent) is True
        assert crdt.state_size() == 2
        assert crdt.deferred_count() == 0

    def test_digest_and_delta_since(self):
        crdt_a = DeltaStateCRDT(origin="a")
        crdt_b = DeltaStateCRDT(origin="b")

        d1 = Delta.create(body={"op": "a1"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "b1"}, origin="b", kind=DeltaKind.EDIT_BODY)
        crdt_a.apply(d1)
        crdt_b.apply(d2)

        missing_for_b = crdt_a.delta_since(crdt_b.digest())
        assert len(missing_for_b) == 1
        assert missing_for_b[0].id == d1.id

    def test_materialize(self):
        crdt = DeltaStateCRDT(origin="a")
        parent = Delta.create(body={"op": "p"}, origin="a", kind=DeltaKind.EDIT_BODY)
        crdt.apply(parent)
        child = Delta.create(
            body={"op": "c"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={parent.id},
        )
        crdt.apply(child)

        ordered = crdt.materialize()
        assert len(ordered) == 2
        assert ordered[0].id == parent.id
        assert ordered[1].id == child.id
