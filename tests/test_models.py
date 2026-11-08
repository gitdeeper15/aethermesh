"""
Tests for aethermesh.models — Delta, Replica, Signature, enums.

Covers:
    - Delta.id determinism and content-addressing
    - Delta immutability
    - Replica.join (idempotent, commutative, associative)
    - Replica.materialize (topological order)
    - Signature serialization
    - Verdict / DeltaKind / AdmissionStage enums
"""

import pytest

from aethermesh.models import (
    AdmissionStage,
    AdmissionVerdict,
    Delta,
    DeltaKind,
    PeerView,
    Replica,
    Signature,
    Verdict,
    deserialize_delta,
    serialize_delta,
)


# =============================================================================
# Delta
# =============================================================================

class TestDelta:
    def test_delta_id_is_deterministic(self):
        d1 = Delta(
            body={"op": "edit"},
            parents=frozenset(),
            timestamp="2026-01-01T00:00:00+00:00",
            origin="agent-1",
            kind=DeltaKind.EDIT_BODY,
        )
        d2 = Delta(
            body={"op": "edit"},
            parents=frozenset(),
            timestamp="2026-01-01T00:00:00+00:00",
            origin="agent-1",
            kind=DeltaKind.EDIT_BODY,
        )
        assert d1.id == d2.id

    def test_delta_id_changes_with_body(self):
        d1 = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "other"}, origin="a", kind=DeltaKind.EDIT_BODY)
        assert d1.id != d2.id

    def test_delta_id_changes_with_parents(self):
        d1 = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY, parents={"p1"})
        d2 = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY, parents={"p2"})
        assert d1.id != d2.id

    def test_delta_id_ignores_signature(self):
        sig = Signature(origin="a", key_id="k", value=b"\x00" * 64)
        d_unsigned = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d_signed = d_unsigned.with_signature(sig)
        assert d_unsigned.id == d_signed.id

    def test_delta_is_frozen(self):
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        with pytest.raises(Exception):
            d.origin = "b"

    def test_delta_serialization_roundtrip(self):
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        s = serialize_delta(d)
        d2 = deserialize_delta(s)
        assert d2.id == d.id
        assert d2.origin == d.origin
        assert d2.kind == d.kind


# =============================================================================
# Replica
# =============================================================================

class TestReplica:
    def test_join_single_delta(self):
        r = Replica(origin="a")
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        r.join(d)
        assert len(r) == 1
        assert d.id in r

    def test_join_is_idempotent(self):
        r = Replica(origin="a")
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        r.join(d)
        r.join(d)
        r.join(d)
        assert len(r) == 1

    def test_merge_is_commutative(self):
        r1 = Replica(origin="a")
        r2 = Replica(origin="b")
        d1 = Delta.create(body={"op": "a"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "b"}, origin="b", kind=DeltaKind.EDIT_BODY)
        r1.join(d1)
        r2.join(d2)

        merged1 = Replica(origin="x")
        merged1.join(d1).join(d2)

        merged2 = Replica(origin="x")
        merged2.join(d2).join(d1)

        assert merged1.ids() == merged2.ids()

    def test_has_parents(self):
        r = Replica(origin="a")
        parent = Delta.create(body={"op": "parent"}, origin="a", kind=DeltaKind.EDIT_BODY)
        r.join(parent)

        child = Delta.create(
            body={"op": "child"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={parent.id},
        )
        assert r.has_parents(child) is True

        orphan = Delta.create(
            body={"op": "orphan"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={"missing"},
        )
        assert r.has_parents(orphan) is False

    def test_materialize_topological(self):
        r = Replica(origin="a")
        parent = Delta.create(body={"op": "p"}, origin="a", kind=DeltaKind.EDIT_BODY)
        r.join(parent)
        child = Delta.create(
            body={"op": "c"},
            origin="a",
            kind=DeltaKind.EDIT_BODY,
            parents={parent.id},
        )
        r.join(child)

        ordered = r.materialize()
        assert len(ordered) == 2
        # Parent must come before child.
        parent_idx = next(i for i, d in enumerate(ordered) if d.id == parent.id)
        child_idx = next(i for i, d in enumerate(ordered) if d.id == child.id)
        assert parent_idx < child_idx


# =============================================================================
# Signature
# =============================================================================

class TestSignature:
    def test_signature_serialization(self):
        sig = Signature(origin="a", key_id="k", value=b"\x01\x02\x03")
        d = sig.to_dict()
        sig2 = Signature.from_dict(d)
        assert sig2.origin == sig.origin
        assert sig2.key_id == sig.key_id
        assert sig2.value == sig.value


# =============================================================================
# Enums
# =============================================================================

class TestEnums:
    def test_verdict_values(self):
        assert Verdict.ACCEPT.value == "accept"
        assert Verdict.REJECT.value == "reject"
        assert Verdict.DEFER.value == "defer"
        assert Verdict.QUARANTINE.value == "quarantine"

    def test_delta_kinds(self):
        assert DeltaKind.EDIT_BODY.value == "edit_body"
        assert DeltaKind.RENAME_SYMBOL.value == "rename_symbol"
        assert DeltaKind.DELETE_SYMBOL.value == "delete_symbol"
        assert DeltaKind.CHANGE_SIGNATURE.value == "change_signature"
        assert DeltaKind.EDIT_METADATA.value == "edit_metadata"

    def test_admission_stages(self):
        assert AdmissionStage.SIGNATURE.value == "signature"
        assert AdmissionStage.DAG_INTEGRITY.value == "dag_integrity"
        assert AdmissionStage.SCHEMA.value == "schema"
        assert AdmissionStage.SEMANTICS.value == "semantics"


# =============================================================================
# AdmissionVerdict
# =============================================================================

class TestAdmissionVerdict:
    def test_accepted_property(self):
        v = AdmissionVerdict(delta_id="x", verdict=Verdict.ACCEPT)
        assert v.accepted is True

    def test_rejected_property(self):
        v = AdmissionVerdict(delta_id="x", verdict=Verdict.REJECT)
        assert v.accepted is False


# =============================================================================
# PeerView
# =============================================================================

class TestPeerView:
    def test_add_and_sample(self):
        pv = PeerView(capacity=10)
        pv.add("p1")
        pv.add("p2")
        pv.add("p3")
        assert len(pv) == 3
        sample = pv.sample(2)
        assert len(sample) == 2

    def test_capacity_eviction(self):
        pv = PeerView(capacity=2)
        pv.add("p1")
        pv.add("p2")
        pv.add("p3")  # should evict one
        assert len(pv) == 2
