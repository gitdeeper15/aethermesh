"""
Tests for aethermesh.admission.pipeline — the four-check pipeline.

Covers:
    - Check 1: Signature (valid, missing, unknown key, bad sig)
    - Check 2: DAG integrity (missing parents -> defer)
    - Check 3: Schema (malformed body -> reject)
    - Check 4: Semantics (conflict -> reject/quarantine)
    - Full pipeline (accept, reject, defer)
    - Idempotence (already admitted -> accept)

Note on the semantic check:
    Per assumption A6 (admission determinism), the semantic check is a
    pure function of the delta and its causal closure. Concurrent deltas
    (neither is an ancestor of the other) are NOT in each other's causal
    closure, so they are not checked against each other at admission time.
    Conflicts between a delta and its ancestors are detected; conflicts
    between concurrent deltas are resolved by the CRDT's deterministic
    merge (LWW, etc.) or by the higher layers.
"""

import pytest

from aethermesh.models import (
    Delta,
    DeltaKind,
    Signature,
    Verdict,
)
from aethermesh.crdt.delta_state import DeltaStateCRDT
from aethermesh.bft.provenance import (
    KeyRegistry,
    generate_keypair,
    sign_delta,
)
from aethermesh.admission.pipeline import (
    AdmissionPipeline,
    PipelineConfig,
)


@pytest.fixture
def signed_pipeline():
    priv, pub = generate_keypair()
    registry = KeyRegistry()
    registry.register("agent-1", "key-1", pub)
    pipeline = AdmissionPipeline(registry=registry)
    return {"priv": priv, "pub": pub, "registry": registry, "pipeline": pipeline}


def _make_signed(priv, body=None, kind=DeltaKind.EDIT_BODY, origin="agent-1", parents=None):
    d = Delta.create(
        body=body or {"op": "edit"},
        origin=origin,
        kind=kind,
        parents=parents or set(),
    )
    return sign_delta(d, priv, "key-1")


# =============================================================================
# Check 1: Signature
# =============================================================================

class TestCheckSignature:
    def test_valid_signature(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"])
        result = signed_pipeline["pipeline"].check_signature(d)
        assert result.ok is True
        assert result.verdict == Verdict.ACCEPT

    def test_missing_signature(self, signed_pipeline):
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        result = signed_pipeline["pipeline"].check_signature(d)
        assert result.ok is False
        assert result.verdict == Verdict.REJECT

    def test_unknown_key(self, signed_pipeline):
        priv2, _ = generate_keypair()
        d = _make_signed(priv2)
        result = signed_pipeline["pipeline"].check_signature(d)
        assert result.ok is False
        assert result.verdict == Verdict.REJECT


# =============================================================================
# Check 2: DAG integrity
# =============================================================================

class TestCheckDAG:
    def test_no_parents(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"])
        crdt = DeltaStateCRDT(origin="local")
        result = signed_pipeline["pipeline"].check_dag_integrity(d, crdt.replica)
        assert result.ok is True

    def test_missing_parents_defer(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"], parents={"missing-parent-id"})
        crdt = DeltaStateCRDT(origin="local")
        result = signed_pipeline["pipeline"].check_dag_integrity(d, crdt.replica)
        assert result.ok is False
        assert result.verdict == Verdict.DEFER
        assert "missing parents" in result.reason

    def test_present_parents(self, signed_pipeline):
        parent = _make_signed(signed_pipeline["priv"], body={"op": "parent"})
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(parent)

        child = _make_signed(
            signed_pipeline["priv"],
            body={"op": "child"},
            parents={parent.id},
        )
        result = signed_pipeline["pipeline"].check_dag_integrity(child, crdt.replica)
        assert result.ok is True


# =============================================================================
# Check 3: Schema
# =============================================================================

class TestCheckSchema:
    def test_valid_schema(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"])
        result = signed_pipeline["pipeline"].check_schema(d)
        assert result.ok is True

    def test_missing_op_field(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"], body={"target": "x"})
        result = signed_pipeline["pipeline"].check_schema(d)
        assert result.ok is False
        assert result.verdict == Verdict.REJECT

    def test_non_string_op(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"], body={"op": 42})
        result = signed_pipeline["pipeline"].check_schema(d)
        assert result.ok is False
        assert result.verdict == Verdict.REJECT


# =============================================================================
# Check 4: Semantics (over causal closure)
# =============================================================================

class TestCheckSemantics:
    def test_single_delta_no_ancestors(self, signed_pipeline):
        """A delta with no ancestors has causal closure = itself -> OK."""
        d = _make_signed(signed_pipeline["priv"], kind=DeltaKind.EDIT_BODY)
        crdt = DeltaStateCRDT(origin="local")
        result = signed_pipeline["pipeline"].check_semantics(d, crdt.replica)
        assert result.ok is True

    def test_conflict_with_ancestor(self, signed_pipeline):
        """
        A delta that conflicts with its ancestor (in its causal closure)
        should be flagged as CONFLICT.
        """
        ancestor = _make_signed(
            signed_pipeline["priv"],
            body={"op": "edit"},
            kind=DeltaKind.EDIT_BODY,
        )
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(ancestor)

        # Child of an EDIT_BODY that is DELETE_SYMBOL -> conflict.
        child = _make_signed(
            signed_pipeline["priv"],
            body={"op": "delete"},
            kind=DeltaKind.DELETE_SYMBOL,
            parents={ancestor.id},
        )
        result = signed_pipeline["pipeline"].check_semantics(child, crdt.replica)
        assert result.ok is False
        assert result.verdict == Verdict.REJECT

    def test_resolve_with_ancestor(self, signed_pipeline):
        """A delta that RESOLVEs with its ancestor should be rejected (default config)."""
        ancestor = _make_signed(
            signed_pipeline["priv"],
            body={"op": "r1"},
            kind=DeltaKind.RENAME_SYMBOL,
        )
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(ancestor)

        child = _make_signed(
            signed_pipeline["priv"],
            body={"op": "r2"},
            kind=DeltaKind.RENAME_SYMBOL,
            parents={ancestor.id},
        )
        result = signed_pipeline["pipeline"].check_semantics(child, crdt.replica)
        # RESOLVE -> rejected (default config: reject_on_semantic_conflict=True)
        # Note: RESOLVE is not the same as CONFLICT, but default config rejects both.
        assert result.ok is False


# =============================================================================
# Full pipeline
# =============================================================================

class TestFullPipeline:
    def test_accept_valid(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"])
        crdt = DeltaStateCRDT(origin="local")
        verdict = signed_pipeline["pipeline"].admit(d, crdt.replica)
        assert verdict.verdict == Verdict.ACCEPT
        assert verdict.accepted is True

    def test_reject_unsigned(self, signed_pipeline):
        d = Delta.create(body={"op": "edit"}, origin="agent-1", kind=DeltaKind.EDIT_BODY)
        crdt = DeltaStateCRDT(origin="local")
        verdict = signed_pipeline["pipeline"].admit(d, crdt.replica)
        assert verdict.verdict == Verdict.REJECT
        assert verdict.accepted is False

    def test_defer_missing_parents(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"], parents={"missing"})
        crdt = DeltaStateCRDT(origin="local")
        verdict = signed_pipeline["pipeline"].admit(d, crdt.replica)
        assert verdict.verdict == Verdict.DEFER

    def test_idempotent_already_admitted(self, signed_pipeline):
        d = _make_signed(signed_pipeline["priv"])
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(d)
        verdict = signed_pipeline["pipeline"].admit(d, crdt.replica)
        assert verdict.verdict == Verdict.ACCEPT
        assert "already admitted" in verdict.reason

    def test_reject_conflict_with_ancestor(self, signed_pipeline):
        """A delta that conflicts with its ancestor is rejected."""
        ancestor = _make_signed(
            signed_pipeline["priv"],
            body={"op": "edit"},
            kind=DeltaKind.EDIT_BODY,
        )
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(ancestor)

        conflict = _make_signed(
            signed_pipeline["priv"],
            body={"op": "delete"},
            kind=DeltaKind.DELETE_SYMBOL,
            parents={ancestor.id},
        )
        verdict = signed_pipeline["pipeline"].admit(conflict, crdt.replica)
        assert verdict.verdict == Verdict.REJECT

    def test_accept_concurrent_edit_edit(self, signed_pipeline):
        """
        Two concurrent EDIT_BODY deltas (no parent-child) are NOT checked
        against each other. The first is admitted; the second is also
        admitted (EDIT_BODY vs EDIT_BODY is OK in the matrix).
        """
        d1 = _make_signed(signed_pipeline["priv"], body={"op": "e1"}, kind=DeltaKind.EDIT_BODY)
        d2 = _make_signed(signed_pipeline["priv"], body={"op": "e2"}, kind=DeltaKind.EDIT_BODY)
        crdt = DeltaStateCRDT(origin="local")
        crdt.apply(d1)
        verdict = signed_pipeline["pipeline"].admit(d2, crdt.replica)
        assert verdict.verdict == Verdict.ACCEPT


# =============================================================================
# Pipeline config
# =============================================================================

class TestPipelineConfig:
    def test_custom_fan_in(self):
        priv, pub = generate_keypair()
        registry = KeyRegistry()
        registry.register("agent-1", "key-1", pub)
        config = PipelineConfig(max_parents=1)
        pipeline = AdmissionPipeline(registry=registry, config=config)

        d = _make_signed(priv, parents={"p1", "p2"})
        crdt = DeltaStateCRDT(origin="local")
        verdict = pipeline.admit(d, crdt.replica)
        assert verdict.verdict == Verdict.REJECT
