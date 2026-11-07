"""Tests for obligations and ODG."""

import pytest

from aetherproof.models import CSRecord, Layer, Obligation
from aetherproof.obligations.generator import generate_obligations
from aetherproof.obligations.odg import ODG, EdgeType


def test_generate_invariance_obligation():
    """Test generating invariance obligation from L1 invariant."""
    csr = CSRecord.create(
        layer=Layer.L1,
        language="TLA+",
        content="Always (queue_length <= MAX)",
        semantic_role="invariant",
        assumptions=("A1: MAX > 0",),
    )

    obligations = generate_obligations(csr)
    assert len(obligations) == 1
    assert obligations[0].property.startswith("Invariance")


def test_generate_contract_obligation():
    """Test generating contract obligation from L2 contract."""
    csr = CSRecord.create(
        layer=Layer.L2,
        language="Why3",
        content="pre: x > 0; post: result > x",
        semantic_role="contract",
    )

    obligations = generate_obligations(csr)
    assert len(obligations) == 1
    assert obligations[0].property.startswith("PrePost")


def test_generate_constraint_obligation():
    """Test generating satisfiability obligation from L3 constraint."""
    csr = CSRecord.create(
        layer=Layer.L3,
        language="SMT-LIB",
        content="(assert (> x 0))",
        semantic_role="constraint",
    )

    obligations = generate_obligations(csr)
    assert len(obligations) == 1
    assert obligations[0].property.startswith("Satisfiability")


def test_generate_translation_obligation():
    """Test generating consistency obligation from translation."""
    csr = CSRecord.create(
        layer=Layer.L1,
        language="TLA+",
        content="translation L1->L2",
        semantic_role="translation",
    )

    obligations = generate_obligations(csr)
    assert len(obligations) == 1
    assert obligations[0].property.startswith("Consistency")


def test_generate_unknown_role():
    """Test that unknown role generates no obligations."""
    csr = CSRecord.create(
        layer=Layer.L1,
        language="TLA+",
        content="unknown",
        semantic_role="unknown_role",
    )

    obligations = generate_obligations(csr)
    assert len(obligations) == 0


def test_odg_add_obligation():
    """Test adding obligations to ODG."""
    obl = Obligation.create(
        property="P1",
        assumptions=("A1",),
        source_csr="csr-1",
    )

    odg = ODG()
    odg.add_obligation(obl)

    assert len(odg.obligations) == 1
    assert obl.id in odg.obligations


def test_odg_add_edge():
    """Test adding edges to ODG."""
    obl1 = Obligation.create("P1", ("A1",), "csr-1")
    obl2 = Obligation.create("P2", ("A1",), "csr-2")

    odg = ODG()
    odg.add_obligation(obl1)
    odg.add_obligation(obl2)
    odg.add_edge(obl1.id, obl2.id, EdgeType.REQUIRES)

    assert len(odg.edges) == 1


def test_odg_cycle_detection():
    """Test that ODG rejects cycles."""
    obl1 = Obligation.create("P1", ("A1",), "csr-1")
    obl2 = Obligation.create("P2", ("A1",), "csr-2")

    odg = ODG()
    odg.add_obligation(obl1)
    odg.add_obligation(obl2)
    odg.add_edge(obl1.id, obl2.id, EdgeType.REQUIRES)

    with pytest.raises(ValueError, match="cycle"):
        odg.add_edge(obl2.id, obl1.id, EdgeType.REQUIRES)


def test_odg_invalidate():
    """Test invalidation propagates to dependents.

    Edge direction: (source, target) means "source depends on target".
    So if obl2 depends on obl1, we add edge (obl2, obl1, REQUIRES).
    Invalidating obl1 should invalidate obl2 (the dependent).
    """
    obl1 = Obligation.create("P1", ("A1",), "csr-1")
    obl2 = Obligation.create("P2", ("A1",), "csr-2")

    odg = ODG()
    odg.add_obligation(obl1)
    odg.add_obligation(obl2)
    # obl2 depends on obl1
    odg.add_edge(obl2.id, obl1.id, EdgeType.REQUIRES)

    invalidated = odg.invalidate(obl1.id)
    assert obl1.id in invalidated
    assert obl2.id in invalidated
