"""AetherMesh — Byzantine Fault Tolerance module (Pillar 3)."""

from aethermesh.bft.provenance import (
    KeyRegistry,
    ProvenanceChecker,
    generate_keypair,
    sign_delta,
    verify_delta_signature,
)
from aethermesh.bft.invariants import (
    StructuralChecker,
    InvariantViolation,
)
from aethermesh.bft.semantic_matrix import (
    CompatibilityMatrix,
    DEFAULT_MATRIX,
    SemanticVerdict,
)

__all__ = [
    "KeyRegistry",
    "ProvenanceChecker",
    "generate_keypair",
    "sign_delta",
    "verify_delta_signature",
    "StructuralChecker",
    "InvariantViolation",
    "CompatibilityMatrix",
    "DEFAULT_MATRIX",
    "SemanticVerdict",
]
