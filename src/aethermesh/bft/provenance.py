"""
AetherMesh — Cryptographic provenance (Pillar 3, Section 3.3.1).

Every delta carries the identifier of its originating agent and a
digital signature over the delta's content hash, which in turn covers
the delta body and its parent identifiers.

We use Ed25519 (Bernstein et al., 2012). The architecture does not
depend on a particular scheme but does depend on its unforgeability
(assumption A5).

Each node maintains a local registry mapping agent identifiers to
public keys. How the registry is bootstrapped, extended, and revoked
is a trust-establishment question that the paper does not settle
(Section 7.4).

This module provides:

    - KeyRegistry:          local mapping from origin -> public key
    - generate_keypair:      Ed25519 keypair generation
    - sign_delta:            sign a delta with a private key
    - verify_delta_signature: verify a delta's signature
    - ProvenanceChecker:     the admission-stage check

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 3.3.1.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

from aethermesh.models import Delta, Signature


# =============================================================================
# Key types
# =============================================================================

PrivateKey = Ed25519PrivateKey
PublicKey = Ed25519PublicKey


# =============================================================================
# Keypair generation
# =============================================================================

def generate_keypair() -> Tuple[PrivateKey, PublicKey]:
    """
    Generate a fresh Ed25519 keypair.

    Returns:
        (private_key, public_key)
    """
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    return private, public


# =============================================================================
# KeyRegistry
# =============================================================================

@dataclass
class KeyRegistry:
    """
    Local mapping from agent identifier to public key.

    This is the trust anchor for provenance (assumption A5). How the
    registry is populated, extended, and revoked is out of scope for
    this module (Section 7.4 of the paper).

    Attributes:
        keys:   Map from origin id -> {key_id -> public key}.
    """
    keys: Dict[str, Dict[str, PublicKey]] = field(default_factory=dict)

    def register(self, origin: str, key_id: str, public_key: PublicKey) -> None:
        """Register a public key for an origin."""
        self.keys.setdefault(origin, {})[key_id] = public_key

    def lookup(self, origin: str, key_id: str) -> Optional[PublicKey]:
        """Look up a public key for an origin. Returns None if unknown."""
        return self.keys.get(origin, {}).get(key_id)

    def has(self, origin: str, key_id: str) -> bool:
        return self.lookup(origin, key_id) is not None

    def __len__(self) -> int:
        return sum(len(v) for v in self.keys.values())


# =============================================================================
# Signing
# =============================================================================

def sign_delta(
    delta: Delta,
    private_key: PrivateKey,
    key_id: str,
) -> Delta:
    """
    Sign a delta with an Ed25519 private key.

    The signature covers the delta's content hash (its id), which
    itself covers the body, parents, timestamp, origin, and kind.

    Args:
        delta:        The unsigned delta.
        private_key:  The origin's Ed25519 private key.
        key_id:       An identifier for the public key (for lookup).

    Returns:
        A copy of the delta with a Signature attached.
    """
    message = delta.content_hash
    signature_bytes = private_key.sign(message)
    return delta.with_signature(
        Signature(
            origin=delta.origin,
            key_id=key_id,
            value=signature_bytes,
        )
    )


def verify_delta_signature(
    delta: Delta,
    public_key: PublicKey,
) -> bool:
    """
    Verify a delta's signature against a public key.

    Returns True iff the signature is valid over the delta's content hash.
    """
    if delta.signature is None:
        return False
    try:
        public_key.verify(delta.signature.value, delta.content_hash)
        return True
    except InvalidSignature:
        return False


# =============================================================================
# ProvenanceChecker
# =============================================================================

@dataclass
class ProvenanceChecker:
    """
    The provenance-check stage of the admission pipeline (Check 1).

    Verifies that a delta has:
        - A signature attached.
        - A registered key for its origin.
        - A valid signature over the content hash.

    Reference: Figure 7 (step 2) and Table (Section 3.3.4) of the paper.
    """
    registry: KeyRegistry

    def check(self, delta: Delta) -> Tuple[bool, str]:
        """
        Returns (ok, reason). ok=True iff all provenance checks pass.
        """
        if delta.signature is None:
            return False, "no signature attached"
        if delta.signature.origin != delta.origin:
            return False, "signature origin does not match delta origin"
        public_key = self.registry.lookup(delta.origin, delta.signature.key_id)
        if public_key is None:
            return False, f"unknown key: origin={delta.origin} key_id={delta.signature.key_id}"
        if not verify_delta_signature(delta, public_key):
            return False, "signature verification failed"
        return True, "ok"


# =============================================================================
# Convenience: serialize/deserialize keys
# =============================================================================

def export_public_key(public_key: PublicKey) -> bytes:
    """Export a public key as raw bytes (32 bytes)."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def import_public_key(raw: bytes) -> PublicKey:
    """Import a public key from raw bytes (32 bytes)."""
    return Ed25519PublicKey.from_public_bytes(raw)
