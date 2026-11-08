"""
Tests for aethermesh.bft — provenance, invariants, semantic matrix.

Covers:
    - Ed25519 keypair generation and signing/verification
    - KeyRegistry (register, lookup, has)
    - ProvenanceChecker (valid, missing sig, unknown key, bad sig)
    - StructuralChecker (fan-in, size bounds)
    - CompatibilityMatrix (ok, resolve, conflict)
    - DEFAULT_MATRIX entries
"""

import pytest

from aethermesh.models import Delta, DeltaKind, Signature
from aethermesh.bft.provenance import (
    KeyRegistry,
    ProvenanceChecker,
    generate_keypair,
    sign_delta,
    verify_delta_signature,
    export_public_key,
    import_public_key,
)
from aethermesh.bft.invariants import (
    InvariantViolation,
    StructuralChecker,
)
from aethermesh.bft.semantic_matrix import (
    CompatibilityMatrix,
    DEFAULT_MATRIX,
    SemanticVerdict,
)


# =============================================================================
# Keypair and signing
# =============================================================================

class TestSigning:
    def test_generate_keypair(self):
        priv, pub = generate_keypair()
        assert priv is not None
        assert pub is not None

    def test_sign_and_verify(self):
        priv, pub = generate_keypair()
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        d_signed = sign_delta(d, priv, "key-1")
        assert d_signed.signature is not None
        assert verify_delta_signature(d_signed, pub) is True

    def test_verify_fails_with_wrong_key(self):
        priv1, pub1 = generate_keypair()
        priv2, pub2 = generate_keypair()
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        d_signed = sign_delta(d, priv1, "key-1")
        assert verify_delta_signature(d_signed, pub2) is False

    def test_verify_fails_without_signature(self):
        _, pub = generate_keypair()
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        assert verify_delta_signature(d, pub) is False

    def test_public_key_roundtrip(self):
        _, pub = generate_keypair()
        raw = export_public_key(pub)
        assert len(raw) == 32
        pub2 = import_public_key(raw)
        assert pub2 is not None


# =============================================================================
# KeyRegistry
# =============================================================================

class TestKeyRegistry:
    def test_register_and_lookup(self):
        reg = KeyRegistry()
        _, pub = generate_keypair()
        reg.register("agent-1", "key-1", pub)
        assert reg.lookup("agent-1", "key-1") == pub
        assert reg.has("agent-1", "key-1") is True

    def test_lookup_missing(self):
        reg = KeyRegistry()
        assert reg.lookup("agent-x", "key-y") is None
        assert reg.has("agent-x", "key-y") is False


# =============================================================================
# ProvenanceChecker
# =============================================================================

class TestProvenanceChecker:
    def test_valid_delta(self):
        priv, pub = generate_keypair()
        reg = KeyRegistry()
        reg.register("agent-1", "key-1", pub)
        checker = ProvenanceChecker(registry=reg)
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        d_signed = sign_delta(d, priv, "key-1")
        ok, reason = checker.check(d_signed)
        assert ok is True
        assert reason == "ok"

    def test_no_signature(self):
        _, pub = generate_keypair()
        reg = KeyRegistry()
        reg.register("agent-1", "key-1", pub)
        checker = ProvenanceChecker(registry=reg)
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        ok, reason = checker.check(d)
        assert ok is False
        assert "no signature" in reason

    def test_unknown_key(self):
        priv, _ = generate_keypair()
        reg = KeyRegistry()  # empty
        checker = ProvenanceChecker(registry=reg)
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        d_signed = sign_delta(d, priv, "key-1")
        ok, reason = checker.check(d_signed)
        assert ok is False
        assert "unknown key" in reason

    def test_bad_signature(self):
        _, pub = generate_keypair()
        reg = KeyRegistry()
        reg.register("agent-1", "key-1", pub)
        checker = ProvenanceChecker(registry=reg)
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        bad_sig = Signature(origin="agent-1", key_id="key-1", value=b"\x00" * 64)
        d_bad = d.with_signature(bad_sig)
        ok, reason = checker.check(d_bad)
        assert ok is False
        assert "verification failed" in reason


# =============================================================================
# StructuralChecker
# =============================================================================

class TestStructuralChecker:
    def test_valid_delta(self):
        checker = StructuralChecker()
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        ok, reason = checker.check(d)
        assert ok is True

    def test_fan_in_exceeded(self):
        checker = StructuralChecker(max_parents=2)
        parents = {f"p{i}" for i in range(3)}
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY, parents=parents)
        ok, reason = checker.check(d)
        assert ok is False
        assert "fan-in" in reason

    def test_size_exceeded(self):
        checker = StructuralChecker(max_bytes=100)
        d = Delta.create(body={"op": "x" * 500}, origin="a", kind=DeltaKind.EDIT_BODY)
        ok, reason = checker.check(d)
        assert ok is False
        assert "size" in reason


# =============================================================================
# CompatibilityMatrix
# =============================================================================

class TestCompatibilityMatrix:
    def test_default_matrix_edit_body_vs_edit_body(self):
        assert DEFAULT_MATRIX.get(DeltaKind.EDIT_BODY, DeltaKind.EDIT_BODY) == SemanticVerdict.OK

    def test_default_matrix_edit_vs_delete(self):
        assert DEFAULT_MATRIX.get(DeltaKind.EDIT_BODY, DeltaKind.DELETE_SYMBOL) == SemanticVerdict.CONFLICT

    def test_default_matrix_rename_vs_rename(self):
        assert DEFAULT_MATRIX.get(DeltaKind.RENAME_SYMBOL, DeltaKind.RENAME_SYMBOL) == SemanticVerdict.RESOLVE

    def test_default_matrix_delete_vs_delete(self):
        assert DEFAULT_MATRIX.get(DeltaKind.DELETE_SYMBOL, DeltaKind.DELETE_SYMBOL) == SemanticVerdict.OK

    def test_check_returns_ok(self):
        d = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        verdict, reason = DEFAULT_MATRIX.check([d])
        assert verdict == SemanticVerdict.OK

    def test_check_returns_conflict(self):
        d1 = Delta.create(body={"op": "edit"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "delete"}, origin="a", kind=DeltaKind.DELETE_SYMBOL)
        verdict, reason = DEFAULT_MATRIX.check([d1, d2])
        assert verdict == SemanticVerdict.CONFLICT

    def test_check_returns_resolve(self):
        d1 = Delta.create(body={"op": "rename1"}, origin="a", kind=DeltaKind.RENAME_SYMBOL)
        d2 = Delta.create(body={"op": "rename2"}, origin="a", kind=DeltaKind.RENAME_SYMBOL)
        verdict, reason = DEFAULT_MATRIX.check([d1, d2])
        assert verdict == SemanticVerdict.RESOLVE
