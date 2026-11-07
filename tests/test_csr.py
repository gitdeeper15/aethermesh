"""Tests for CSR and semantic relations."""

import pytest

from aetherproof.csr.relations import SemanticRelation, RelationType


def test_relation_creation():
    """Test semantic relation creation."""
    rel = SemanticRelation(
        source="csr-L1-abc",
        target="csr-L2-def",
        relation_type=RelationType.REFINES,
        justification="L2 contract refines L1 invariant",
    )

    assert rel.source == "csr-L1-abc"
    assert rel.target == "csr-L2-def"
    assert rel.relation_type == RelationType.REFINES


def test_approximates_requires_loss_description():
    """Test that approximates requires loss_description."""
    with pytest.raises(ValueError, match="loss_description"):
        SemanticRelation(
            source="csr-L2-abc",
            target="csr-L3-def",
            relation_type=RelationType.APPROXIMATES,
        )


def test_approximates_with_loss_description():
    """Test approximates with loss_description."""
    rel = SemanticRelation(
        source="csr-L2-abc",
        target="csr-L3-def",
        relation_type=RelationType.APPROXIMATES,
        loss_description="Machine integers vs mathematical integers",
    )

    assert rel.loss_description is not None


def test_all_relation_types():
    """Test all seven relation types."""
    assert RelationType.REFINES.value == "refines"
    assert RelationType.INSTANTIATES.value == "instantiates"
    assert RelationType.APPROXIMATES.value == "approximates"
    assert RelationType.IMPLIES.value == "implies"
    assert RelationType.CONTRADICTS.value == "contradicts"
    assert RelationType.DEPENDS_ON.value == "depends_on"
    assert RelationType.SUPERSEDES.value == "supersedes"


def test_relation_types_count():
    """Test that there are exactly 7 relation types."""
    assert len(RelationType) == 7
