"""
Core data models for AetherProof v2.0.0.

Implements Definitions 1–6 from the manuscript.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─── Enums ───

class Verdict(str, Enum):
    """Verification verdict (Section 4.6)."""
    PROVEN = "proven"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


class ObligationType(str, Enum):
    """Obligation types (Section 4.2)."""
    INVARIANCE = "invariance"
    PRE_POST = "pre_post"
    SATISFIABILITY = "satisfiability"
    CONSISTENCY = "consistency"


class CounterexampleType(str, Enum):
    """Counterexample types (Section 6.1)."""
    CODE_DEFECT = "code_defect"
    SPECIFICATION_ERROR = "specification_error"
    ASSUMPTION_VIOLATION = "assumption_violation"
    MODEL_ERROR = "model_error"
    FLAKY_REFUTATION = "flaky_refutation"
    UNKNOWN = "unknown"


class Layer(str, Enum):
    """Functional layers (Section 3.1)."""
    L1 = "L1"  # System-level properties (TLA+)
    L2 = "L2"  # Functional contracts (Why3/Lean)
    L3 = "L3"  # Logical constraints (SMT-LIB/Z3)


# ─── Core Models ───

@dataclass(frozen=True)
class CSRecord:
    """
    Canonical Specification Representation (Definition 1).

    Three identities:
    - Record identity (csr_id)
    - Artifact identity (artifact_hash)
    - Semantic identity (semantic_id)
    """
    csr_id: str
    artifact_hash: str
    semantic_id: str
    layer: Layer
    language: str
    content: str
    semantic_role: str
    requirements_refs: tuple[str, ...] = field(default_factory=tuple)
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    relations: tuple[str, ...] = field(default_factory=tuple)
    version: str = "1.0.0"
    provenance: str = ""

    @classmethod
    def create(
        cls,
        layer: Layer,
        language: str,
        content: str,
        semantic_role: str,
        requirements_refs: tuple[str, ...] = (),
        assumptions: tuple[str, ...] = (),
    ) -> "CSRecord":
        """Create a new CSR record with computed identities."""
        artifact_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        semantic_id = hashlib.sha256(
            f"{semantic_role}:{content}".encode()
        ).hexdigest()[:16]
        csr_id = f"csr-{layer.value}-{artifact_hash[:8]}"

        return cls(
            csr_id=csr_id,
            artifact_hash=artifact_hash,
            semantic_id=semantic_id,
            layer=layer,
            language=language,
            content=content,
            semantic_role=semantic_role,
            requirements_refs=requirements_refs,
            assumptions=assumptions,
        )


@dataclass(frozen=True)
class Obligation:
    """
    Proof obligation (Definition 4).

    O = (id, property, assumptions, source_csr, discharged_by, verdict)
    """
    id: str
    property: str
    assumptions: tuple[str, ...]
    source_csr: str
    discharged_by: Optional[str] = None
    verdict: Verdict = Verdict.UNKNOWN

    @classmethod
    def create(
        cls,
        property: str,
        assumptions: tuple[str, ...],
        source_csr: str,
    ) -> "Obligation":
        """Create a new obligation."""
        oid = hashlib.sha256(
            f"{property}:{source_csr}".encode()
        ).hexdigest()[:16]
        return cls(
            id=f"O-{oid}",
            property=property,
            assumptions=assumptions,
            source_csr=source_csr,
        )


@dataclass(frozen=True)
class Counterexample:
    """
    Counterexample (Definition 6).

    C = (id, obligation, witness, refutation_evidence, type, provenance)
    """
    id: str
    obligation: str
    witness: str
    refutation_evidence: str
    type: CounterexampleType
    provenance: str = ""

    @classmethod
    def create(
        cls,
        obligation: str,
        witness: str,
        refutation_evidence: str,
        type: CounterexampleType = CounterexampleType.UNKNOWN,
        provenance: str = "",
    ) -> "Counterexample":
        """Create a new counterexample."""
        cid = hashlib.sha256(
            f"{obligation}:{witness}".encode()
        ).hexdigest()[:16]
        return cls(
            id=f"C-{cid}",
            obligation=obligation,
            witness=witness,
            refutation_evidence=refutation_evidence,
            type=type,
            provenance=provenance,
        )
