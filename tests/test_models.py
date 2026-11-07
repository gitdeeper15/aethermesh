"""Tests for core models."""

import pytest

from aetherproof.models import (
    CSRecord,
    Layer,
    Obligation,
    Verdict,
    Counterexample,
    CounterexampleType,
    ObligationType,
)


def test_csr_record_creation():
    """Test CSR record creation with three identities."""
    csr = CSRecord.create(
        layer=Layer.L1,
        language="TLA+",
        content="Always (queue_length <= MAX)",
        semantic_role="invariant",
        assumptions=("A1: MAX > 0",),
    )

    assert csr.csr_id.startswith("csr-L1-")
    assert len(csr.artifact_hash) == 16
    assert len(csr.semantic_id) == 16
    assert csr.layer == Layer.L1
    assert csr.language == "TLA+"


def test_csr_identities_distinct():
    """Test that the three identities are distinct."""
    csr = CSRecord.create(
        layer=Layer.L2,
        language="Why3",
        content="pre: x > 0; post: result > x",
        semantic_role="contract",
    )

    assert csr.csr_id != csr.artifact_hash
    assert csr.artifact_hash != csr.semantic_id
    assert csr.csr_id != csr.semantic_id


def test_obligation_creation():
    """Test obligation creation."""
    obl = Obligation.create(
        property="Invariance(Always (queue_length <= MAX))",
        assumptions=("A1",),
        source_csr="csr-L1-abc123",
    )

    assert obl.id.startswith("O-")
    assert obl.verdict == Verdict.UNKNOWN
    assert obl.discharged_by is None


def test_counterexample_creation():
    """Test counterexample creation."""
    cex = Counterexample.create(
        obligation="O-abc123",
        witness="queue_length = MAX + 1",
        refutation_evidence="model-xyz",
        type=CounterexampleType.CODE_DEFECT,
    )

    assert cex.id.startswith("C-")
    assert cex.type == CounterexampleType.CODE_DEFECT


def test_verdict_enum():
    """Test verdict enum."""
    assert Verdict.PROVEN.value == "proven"
    assert Verdict.REFUTED.value == "refuted"
    assert Verdict.UNKNOWN.value == "unknown"


def test_obligation_type_enum():
    """Test obligation type enum."""
    assert ObligationType.INVARIANCE.value == "invariance"
    assert ObligationType.PRE_POST.value == "pre_post"
    assert ObligationType.SATISFIABILITY.value == "satisfiability"
    assert ObligationType.CONSISTENCY.value == "consistency"


def test_counterexample_type_enum():
    """Test counterexample type enum."""
    assert CounterexampleType.CODE_DEFECT.value == "code_defect"
    assert CounterexampleType.SPECIFICATION_ERROR.value == "specification_error"
    assert CounterexampleType.ASSUMPTION_VIOLATION.value == "assumption_violation"
    assert CounterexampleType.MODEL_ERROR.value == "model_error"
    assert CounterexampleType.FLAKY_REFUTATION.value == "flaky_refutation"
    assert CounterexampleType.UNKNOWN.value == "unknown"
