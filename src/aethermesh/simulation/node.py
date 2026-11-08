"""
AetherMesh — Simulated agent node.

A Node bundles together:
    - A local CRDT replica
    - A peer sampler
    - A local keypair and key registry (for signing/verifying deltas)
    - A gossip protocol instance
    - An admission pipeline

The Node is the unit of simulation. The testbed orchestrates many
nodes, a network, and a message queue to reproduce the metrics from
Section 5 of the paper.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Sections 3 and 5.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from aethermesh.models import (
    AdmissionVerdict,
    Delta,
    DeltaKind,
    PeerView,
)
from aethermesh.crdt.delta_state import DeltaStateCRDT
from aethermesh.gossip.peer_sampling import PeerSampler, ViewStatus
from aethermesh.gossip.protocol import GossipProtocol, ExchangeResult
from aethermesh.bft.provenance import (
    KeyRegistry,
    PrivateKey,
    PublicKey,
    generate_keypair,
    sign_delta,
)
from aethermesh.admission.pipeline import AdmissionPipeline, PipelineConfig


# =============================================================================
# Node
# =============================================================================

@dataclass
class Node:
    """
    A simulated AetherMesh agent.

    Attributes:
        node_id:         Unique identifier.
        crdt:            Local CRDT replica (holds admitted deltas).
        sampler:         Peer sampler (partial view of the peer set).
        registry:        Shared key registry (all public keys).
        pipeline:        Admission pipeline.
        private_key:     This node's signing key.
        public_key:      This node's verification key.
        key_id:          Identifier for this node's public key.
        created_at:      Simulated time at which the node was created.
        deltas_authored: Number of deltas this node has authored.
        deltas_received: Number of deltas this node has received.
        deltas_admitted: Number of deltas this node has admitted.
        deltas_rejected: Number of deltas this node has rejected.
        deltas_deferred: Number of deltas this node has deferred.
    """
    node_id: str
    crdt: DeltaStateCRDT = field(default_factory=lambda: DeltaStateCRDT())
    sampler: PeerSampler = field(default_factory=PeerSampler)
    registry: KeyRegistry = field(default_factory=KeyRegistry)
    pipeline: AdmissionPipeline = field(default_factory=AdmissionPipeline)
    private_key: Optional[PrivateKey] = None
    public_key: Optional[PublicKey] = None
    key_id: str = "key-1"
    created_at: float = 0.0

    # Counters
    deltas_authored: int = 0
    deltas_received: int = 0
    deltas_admitted: int = 0
    deltas_rejected: int = 0
    deltas_deferred: int = 0

    def __post_init__(self):
        # Ensure the CRDT has the correct origin.
        self.crdt.replica.origin = self.node_id
        # If no keypair was provided, generate one and register it.
        if self.private_key is None:
            self.private_key, self.public_key = generate_keypair()
            self.registry.register(self.node_id, self.key_id, self.public_key)
        # If a keypair was provided but no registry entry, add one.
        elif self.public_key is not None:
            if not self.registry.has(self.node_id, self.key_id):
                self.registry.register(self.node_id, self.key_id, self.public_key)

        # Ensure the admission pipeline uses the shared registry.
        # (The default_factory creates a pipeline with a fresh, empty
        # registry — we must replace it with one that references our
        # shared registry so that newly-added keys are visible.)
        if self.pipeline.registry is not self.registry:
            self.pipeline = AdmissionPipeline(registry=self.registry)

    # -------------------------------------------------------------------------
    # Authoring
    # -------------------------------------------------------------------------

    def create_delta(
        self,
        body: Dict,
        kind: DeltaKind,
        parents: Optional[Set[str]] = None,
    ) -> Delta:
        """
        Create, sign, and locally admit a new delta.

        Returns the signed delta (also stored in this node's CRDT).
        """
        unsigned = Delta.create(
            body=body,
            origin=self.node_id,
            kind=kind,
            parents=parents or set(),
        )
        signed = sign_delta(unsigned, self.private_key, self.key_id)
        # Locally admit immediately (no self-admission check needed).
        self.crdt.apply(signed)
        self.deltas_authored += 1
        self.deltas_admitted += 1
        return signed

    # -------------------------------------------------------------------------
    # Receiving
    # -------------------------------------------------------------------------

    def receive_delta(self, delta: Delta) -> AdmissionVerdict:
        """
        Receive a delta through the admission pipeline.

        Returns the verdict. The delta is only applied if accepted.
        """
        self.deltas_received += 1
        verdict = self.pipeline.admit(delta, self.crdt.replica)

        if verdict.accepted:
            self.crdt.apply(delta)
            self.deltas_admitted += 1
        elif verdict.verdict.value == "defer":
            self.deltas_deferred += 1
        else:
            self.deltas_rejected += 1

        return verdict

    # -------------------------------------------------------------------------
    # Gossip
    # -------------------------------------------------------------------------

    def digest(self) -> frozenset:
        """Return this node's delta digest."""
        return self.crdt.digest()

    def delta_since(self, other_digest: frozenset) -> List[Delta]:
        """Return deltas this node has that the peer does not."""
        return self.crdt.delta_since(other_digest)

    # -------------------------------------------------------------------------
    # Peer management
    # -------------------------------------------------------------------------

    def add_peer(self, peer_id: str) -> None:
        self.sampler.add_peer(peer_id)

    def remove_peer(self, peer_id: str) -> None:
        self.sampler.remove_peer(peer_id)

    def sample_peers(self, k: int) -> List[str]:
        return self.sampler.sample(k)

    # -------------------------------------------------------------------------
    # Introspection
    # -------------------------------------------------------------------------

    def state_size(self) -> int:
        return self.crdt.state_size()

    def ids(self) -> frozenset:
        return self.crdt.ids()

    def summary(self) -> Dict:
        return {
            "node_id": self.node_id,
            "state_size": self.state_size(),
            "deltas_authored": self.deltas_authored,
            "deltas_received": self.deltas_received,
            "deltas_admitted": self.deltas_admitted,
            "deltas_rejected": self.deltas_rejected,
            "deltas_deferred": self.deltas_deferred,
            "peer_view_size": len(self.sampler),
            "peer_view_status": self.sampler.status().value,
        }


# =============================================================================
# Convenience: create a cluster of nodes
# =============================================================================

def create_cluster(
    n: int,
    registry: Optional[KeyRegistry] = None,
    seed: Optional[int] = None,
) -> List[Node]:
    """
    Create n nodes, each with a keypair registered in a shared registry,
    each aware of the others (full peer view for simplicity).
    """
    rng = random.Random(seed)
    registry = registry or KeyRegistry()
    nodes: List[Node] = []

    # First pass: create nodes with their keypairs.
    for i in range(n):
        node_id = f"node-{i:03d}"
        priv, pub = generate_keypair()
        registry.register(node_id, "key-1", pub)
        nodes.append(Node(
            node_id=node_id,
            registry=registry,
            private_key=priv,
            public_key=pub,
            key_id="key-1",
        ))

    # Second pass: each node knows all others (full view).
    for node in nodes:
        for other in nodes:
            if other.node_id != node.node_id:
                node.add_peer(other.node_id)

    return nodes
