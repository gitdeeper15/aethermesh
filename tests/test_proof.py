"""Tests for proof engine and PDG."""

import pytest

from aetherproof.models import Obligation, Verdict
from aetherproof.proof.pdg import PDG, PDGNode, NodeType
from aetherproof.proof.invalidation import invalidate
from aetherproof.proof.engine import ProofEngine


def test_pdg_add_node():
    """Test adding nodes to PDG."""
    pdg = PDG()
    node = PDGNode(node_id="O-1", node_type=NodeType.OBLIGATION, data={"property": "P1"})
    pdg.add_node(node)
    assert "O-1" in pdg.nodes


def test_pdg_add_duplicate_node():
    """Test that adding a duplicate node raises an error."""
    pdg = PDG()
    node = PDGNode(node_id="O-1", node_type=NodeType.OBLIGATION)
    pdg.add_node(node)
    with pytest.raises(ValueError, match="already exists"):
        pdg.add_node(node)


def test_pdg_invalidate():
    """Test PDG invalidation via derives_from."""
    pdg = PDG()
    pdg.add_node(PDGNode("O-1", NodeType.OBLIGATION))
    pdg.add_node(PDGNode("O-2", NodeType.OBLIGATION))
    pdg.add_node(PDGNode("cs-1", NodeType.CHANGESET))

    pdg.add_edge("cs-1", "O-1", "invalidates")
    pdg.add_edge("O-1", "O-2", "derives_from")

    invalidated = pdg.invalidate("cs-1")
    assert "O-1" in invalidated
    assert "O-2" in invalidated


def test_proof_engine_discharge():
    """Test proof engine discharge."""
    pdg = PDG()
    engine = ProofEngine(pdg=pdg)
    obl = Obligation.create("P1", ("A1",), "csr-1")
    discharged = engine.discharge(obl, "proof-term-xyz")
    assert discharged.verdict == Verdict.PROVEN
    assert discharged.discharged_by == "proof-term-xyz"


def test_proof_engine_refute():
    """Test proof engine refute."""
    pdg = PDG()
    engine = ProofEngine(pdg=pdg)
    obl = Obligation.create("P1", ("A1",), "csr-1")
    refuted = engine.refute(obl, "counterexample-xyz")
    assert refuted.verdict == Verdict.REFUTED
    assert refuted.discharged_by == "counterexample-xyz"
