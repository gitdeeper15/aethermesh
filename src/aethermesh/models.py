"""
AetherMesh — Core data models.

This module defines the fundamental data classes used across the
AetherMesh reference implementation:

    - Delta:        A signed, content-addressed change record
    - Replica:      A local replica state (set of admitted deltas)
    - PeerView:     A local view of the peer set
    - AdmissionVerdict:  Outcome of the admission pipeline
    - DeltaKind:    Operation kind for semantic compatibility
    - Signature:    A cryptographic signature
    - Verdict:      Admission decision (accept / reject / defer / quarantine)

Reference:
    Baladi, S. (2026). AetherMesh: Decentralized Peer-to-Peer Agent
    Synchronization and State CRDTs for Autonomous Multi-Agent Systems.
    Zenodo. https://doi.org/10.5281/zenodo.24038038

    Definitions 1–4 (Section 4 of the paper).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple


# =============================================================================
# Enums
# =============================================================================

class Verdict(str, Enum):
    """Admission verdict for a remote delta (Section 3.3.4 of the paper)."""
    ACCEPT = "accept"
    REJECT = "reject"
    DEFER = "defer"
    QUARANTINE = "quarantine"


class DeltaKind(str, Enum):
    """
    Operation kind for semantic compatibility matrix (Table 3.1 of the paper).
    """
    EDIT_BODY = "edit_body"
    RENAME_SYMBOL = "rename_symbol"
    DELETE_SYMBOL = "delete_symbol"
    CHANGE_SIGNATURE = "change_signature"
    EDIT_METADATA = "edit_metadata"


class AdmissionStage(str, Enum):
    """The four admission pipeline stages (Figure 7 of the paper)."""
    SIGNATURE = "signature"
    DAG_INTEGRITY = "dag_integrity"
    SCHEMA = "schema"
    SEMANTICS = "semantics"


# =============================================================================
# Signature
# =============================================================================

@dataclass(frozen=True)
class Signature:
    """
    A cryptographic signature over a delta's content hash.

    In the reference implementation we use Ed25519 (via `cryptography`),
    but the architecture is agnostic to the specific scheme
    (assumption A5).

    Attributes:
        origin:   Agent identifier of the signer.
        key_id:   Identifier of the public key used.
        value:    Raw signature bytes (hex-encoded in serialization).
    """
    origin: str
    key_id: str
    value: bytes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "origin": self.origin,
            "key_id": self.key_id,
            "value": self.value.hex(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Signature":
        return cls(
            origin=d["origin"],
            key_id=d["key_id"],
            value=bytes.fromhex(d["value"]),
        )


# =============================================================================
# Delta
# =============================================================================

@dataclass(frozen=True)
class Delta:
    """
    A signed, content-addressed change record.

    Definition 1 (Section 4.1 of the paper):
        delta_i = (body, parents, timestamp, origin, kind, signature)

    The delta's identifier is the hash of its canonical content
    (excluding the signature, which is over that hash).

    Attributes:
        body:       The change payload (opaque JSON-serializable dict).
        parents:    Identifiers of parent deltas (empty for genesis).
        timestamp:  ISO-8601 timestamp of creation.
        origin:     Agent identifier of the creator.
        kind:       Operation kind (for semantic compatibility).
        signature:  Signature by the origin over the content hash.
    """
    body: Dict[str, Any]
    parents: FrozenSet[str]
    timestamp: str
    origin: str
    kind: DeltaKind
    signature: Optional[Signature] = None

    @property
    def id(self) -> str:
        """
        Content-addressed identifier: SHA-256 of the canonical body,
        parents, timestamp, origin, and kind (excluding signature).
        """
        canonical = {
            "body": self.body,
            "parents": sorted(self.parents),
            "timestamp": self.timestamp,
            "origin": self.origin,
            "kind": self.kind.value,
        }
        raw = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @property
    def content_hash(self) -> bytes:
        """Raw SHA-256 of the canonical content (for signature verification)."""
        return bytes.fromhex(self.id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "body": self.body,
            "parents": sorted(self.parents),
            "timestamp": self.timestamp,
            "origin": self.origin,
            "kind": self.kind.value,
            "signature": self.signature.to_dict() if self.signature else None,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Delta":
        return cls(
            body=d["body"],
            parents=frozenset(d["parents"]),
            timestamp=d["timestamp"],
            origin=d["origin"],
            kind=DeltaKind(d["kind"]),
            signature=Signature.from_dict(d["signature"]) if d.get("signature") else None,
        )

    @classmethod
    def create(
        cls,
        body: Dict[str, Any],
        origin: str,
        kind: DeltaKind,
        parents: Optional[Set[str]] = None,
    ) -> "Delta":
        """Create a new unsigned delta with current timestamp."""
        return cls(
            body=body,
            parents=frozenset(parents or []),
            timestamp=datetime.now(timezone.utc).isoformat(),
            origin=origin,
            kind=kind,
            signature=None,
        )

    def with_signature(self, signature: Signature) -> "Delta":
        """Return a copy of this delta with the given signature attached."""
        return Delta(
            body=self.body,
            parents=self.parents,
            timestamp=self.timestamp,
            origin=self.origin,
            kind=self.kind,
            signature=signature,
        )


# =============================================================================
# AdmissionVerVerdict
# =============================================================================

@dataclass(frozen=True)
class AdmissionVerdict:
    """
    Outcome of the admission pipeline for a single delta.

    Attributes:
        delta_id:   The identifier of the delta that was evaluated.
        verdict:    The final verdict (accept / reject / defer / quarantine).
        stage:      The stage at which a non-accept verdict was reached.
        reason:     Human-readable explanation.
    """
    delta_id: str
    verdict: Verdict
    stage: Optional[AdmissionStage] = None
    reason: str = ""

    @property
    def accepted(self) -> bool:
        return self.verdict == Verdict.ACCEPT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "delta_id": self.delta_id,
            "verdict": self.verdict.value,
            "stage": self.stage.value if self.stage else None,
            "reason": self.reason,
        }


# =============================================================================
# Replica
# =============================================================================

@dataclass
class Replica:
    """
    A local replica state — the set of admitted deltas (Definition 1).

    The join of two replicas is simply set union (the grow-only set CRDT
    lifted to deltas; Section 3.1.1 of the paper).

    Attributes:
        admitted:  Map from delta id -> Delta (admitted deltas).
        origin:    Agent identifier of this replica's owner.
        deferred:  Deltas awaiting missing parents.
    """
    admitted: Dict[str, Delta] = field(default_factory=dict)
    origin: str = "anonymous"
    deferred: Dict[str, Delta] = field(default_factory=dict)

    def join(self, delta: Delta) -> "Replica":
        """
        Join a single admitted delta into this replica.

        Returns self (mutating in place) for chaining.
        Idempotent: joining the same delta twice has no additional effect.
        """
        self.admitted[delta.id] = delta
        return self

    def join_many(self, deltas: List[Delta]) -> "Replica":
        """Join multiple admitted deltas."""
        for d in deltas:
            self.join(d)
        return self

    def merge(self, other: "Replica") -> "Replica":
        """
        Merge another replica into this one (set union).

        The join operation is commutative, associative, and idempotent
        (Section 3.1.2 of the paper).
        """
        self.admitted.update(other.admitted)
        return self

    def __contains__(self, delta_id: str) -> bool:
        return delta_id in self.admitted

    def __len__(self) -> int:
        return len(self.admitted)

    def ids(self) -> FrozenSet[str]:
        """The set of admitted delta identifiers."""
        return frozenset(self.admitted.keys())

    def has_parents(self, delta: Delta) -> bool:
        """Check whether all parents of a delta are already admitted."""
        return all(p in self.admitted for p in delta.parents)

    def materialize(self) -> List[Delta]:
        """
        Deterministic linearization of the delta set (Section 3.1.1).

        Topological order of the parent DAG, ties broken by delta id.
        """
        # Kahn's algorithm with deterministic tie-breaking by id.
        in_degree: Dict[str, int] = {}
        children: Dict[str, List[str]] = {}

        for did, delta in self.admitted.items():
            in_degree.setdefault(did, 0)
            children.setdefault(did, [])
            for parent in delta.parents:
                if parent in self.admitted:
                    in_degree[did] += 1
                    children.setdefault(parent, []).append(did)

        # Start with deltas that have zero in-degree among admitted parents.
        ready = sorted([d for d, deg in in_degree.items() if deg == 0])
        result: List[Delta] = []

        while ready:
            did = ready.pop(0)
            result.append(self.admitted[did])
            for child in sorted(children.get(did, [])):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    ready.append(child)
            ready.sort()

        return result


# =============================================================================
# PeerView
# =============================================================================

@dataclass
class PeerView:
    """
    A local, partial view of the peer set (Section 3.2.2).

    Each node maintains a bounded sample of the total peer population,
    refreshed continuously. Selection for gossip draws from this view.

    Attributes:
        peers:     Current known peer identifiers.
        capacity:  Maximum number of peers to retain.
    """
    peers: Set[str] = field(default_factory=set)
    capacity: int = 32

    def add(self, peer_id: str) -> None:
        """Add a peer to the view, evicting if over capacity (FIFO for simplicity)."""
        if peer_id in self.peers:
            return
        if len(self.peers) >= self.capacity:
            # Deterministic eviction: remove the lexicographically smallest.
            # (In production, use random or least-recently-used.)
            self.peers.discard(min(self.peers))
        self.peers.add(peer_id)

    def remove(self, peer_id: str) -> None:
        self.peers.discard(peer_id)

    def sample(self, k: int) -> List[str]:
        """
        Select up to k peers uniformly at random.

        Uses Python's random.sample for uniform selection over the
        current view (assumption A2).
        """
        import random
        k = min(k, len(self.peers))
        if k == 0:
            return []
        return random.sample(sorted(self.peers), k)

    def __len__(self) -> int:
        return len(self.peers)

    def __contains__(self, peer_id: str) -> bool:
        return peer_id in self.peers


# =============================================================================
# Serialization helpers
# =============================================================================

def serialize_delta(delta: Delta) -> str:
    """Serialize a delta to canonical JSON (for network transmission)."""
    return json.dumps(delta.to_dict(), sort_keys=True, separators=(",", ":"))


def deserialize_delta(s: str) -> Delta:
    """Deserialize a delta from canonical JSON."""
    return Delta.from_dict(json.loads(s))
