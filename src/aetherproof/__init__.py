"""
AetherProof v2.0.0 — Empirical Implementation of the Formal Architecture.

Reference implementation of the formal architecture specified in:

    Baladi, S. (2026). AetherProof: Autonomous Formal Verification and
    Invariant Synthesis for Multi-Agent Software Ecosystems.
    Zenodo. https://doi.org/10.5281/zenodo.24013124

This is a reference implementation, not a production system.
No real-world deployment has been evaluated.
"""

from aetherproof.__version__ import __version__

from aetherproof.models import (
    CSRecord,
    Obligation,
    Counterexample,
    Verdict,
    ObligationType,
    CounterexampleType,
    Layer,
)
from aetherproof.csr.record import CSRRecord
from aetherproof.csr.relations import SemanticRelation, RelationType
from aetherproof.obligations.generator import generate_obligations
from aetherproof.obligations.odg import ODG, EdgeType
from aetherproof.proof.pdg import PDG, PDGNode, NodeType
from aetherproof.proof.invalidation import invalidate
from aetherproof.proof.engine import ProofEngine
from aetherproof.remediation.diagnosis import diagnose
from aetherproof.remediation.guardrails import check_guardrails, ViolationType, Patch
from aetherproof.remediation.cycle import RemediationCycle
from aetherproof.protocol.messages import Message, MessageType, Envelope
from aetherproof.review.roles import Role, Authority, AUTHORITY_MATRIX

__all__ = [
    "__version__",
    # Models
    "CSRecord",
    "Obligation",
    "Counterexample",
    "Verdict",
    "ObligationType",
    "CounterexampleType",
    "Layer",
    # CSR
    "CSRRecord",
    "SemanticRelation",
    "RelationType",
    # Obligations
    "generate_obligations",
    "ODG",
    "EdgeType",
    # Proof
    "PDG",
    "PDGNode",
    "NodeType",
    "invalidate",
    "ProofEngine",
    # Remediation
    "diagnose",
    "check_guardrails",
    "ViolationType",
    "Patch",
    "RemediationCycle",
    # Protocol
    "Message",
    "MessageType",
    "Envelope",
    # Review
    "Role",
    "Authority",
    "AUTHORITY_MATRIX",
]
