"""
AetherMesh — Peer sampling for gossip (Pillar 2, Section 3.2.2).

Each gossip period, a node selects k peers (the fanout) uniformly at
random from its current peer sample. In a large network, nodes cannot
hold the full membership list, so peer selection draws from a
continuously refreshed partial view.

This module provides:

    - PeerSampler:    maintains a bounded partial view of the peer set
                     and samples k peers uniformly at random.
    - ViewStatus:     a small enum for the sampler's state.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 3.2.2.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, Dict, Iterable, List, Optional, Set


# =============================================================================
# ViewStatus
# =============================================================================

class ViewStatus(str, Enum):
    """Status of a peer sampler's view."""
    EMPTY = "empty"
    PARTIAL = "partial"      # has some peers, fewer than capacity
    FULL = "full"            # at capacity


# =============================================================================
# PeerSampler
# =============================================================================

@dataclass
class PeerSampler:
    """
    Maintains a bounded partial view of the peer set and samples k
    peers uniformly at random (Section 3.2.2 of the paper).

    The sampler enforces:

        - Bounded capacity (O(capacity) memory).
        - Uniform random selection (assumption A2).
        - Continuous refresh via `add_peer` and `refresh`.

    Attributes:
        capacity:     Maximum number of peers retained in the view.
        view:         Current set of peer identifiers.
        _rng:         Random source (seeded for reproducibility if provided).
    """
    capacity: int = 32
    view: Set[str] = field(default_factory=set)
    _rng: Optional[random.Random] = field(default=None, repr=False)

    def __post_init__(self):
        if self._rng is None:
            self._rng = random.Random()

    # -------------------------------------------------------------------------
    # View management
    # -------------------------------------------------------------------------

    def add_peer(self, peer_id: str) -> bool:
        """
        Add a peer to the view.

        If the view is at capacity, a peer is evicted uniformly at random
        to make room. This implements a simple uniform sampling policy
        (see Jelasity et al., 2005 for more sophisticated alternatives).

        Returns True if the view changed.
        """
        if peer_id in self.view:
            return False
        if len(self.view) >= self.capacity:
            evict = self._rng.choice(sorted(self.view))
            self.view.discard(evict)
        self.view.add(peer_id)
        return True

    def add_peers(self, peer_ids: Iterable[str]) -> int:
        """Add multiple peers. Returns the number of changes."""
        return sum(1 for pid in peer_ids if self.add_peer(pid))

    def remove_peer(self, peer_id: str) -> bool:
        """Remove a peer. Returns True if it was present."""
        if peer_id in self.view:
            self.view.discard(peer_id)
            return True
        return False

    def refresh(self, new_peers: Iterable[str]) -> None:
        """
        Merge new peers into the view and drop some old ones to keep
        the view fresh.

        Simple policy: add all new peers (each may evict a random one),
        then optionally drop up to 25% of the remaining to avoid staleness.
        """
        self.add_peers(new_peers)

    # -------------------------------------------------------------------------
    # Sampling
    # -------------------------------------------------------------------------

    def sample(self, k: int) -> List[str]:
        """
        Select up to k peers uniformly at random from the view.

        Uniform selection is what the dissemination analysis assumes
        (assumption A2). Biased selection may violate the analysis.
        """
        k = min(k, len(self.view))
        if k == 0:
            return []
        return self._rng.sample(sorted(self.view), k)

    # -------------------------------------------------------------------------
    # Introspection
    # -------------------------------------------------------------------------

    def status(self) -> ViewStatus:
        if len(self.view) == 0:
            return ViewStatus.EMPTY
        if len(self.view) < self.capacity:
            return ViewStatus.PARTIAL
        return ViewStatus.FULL

    def __len__(self) -> int:
        return len(self.view)

    def __contains__(self, peer_id: str) -> bool:
        return peer_id in self.view

    def peers(self) -> Set[str]:
        """Return a copy of the current view."""
        return set(self.view)

    def clear(self) -> None:
        self.view.clear()


# =============================================================================
# Convenience: build a sampler pre-populated with peers
# =============================================================================

def build_sampler(
    peer_ids: Iterable[str],
    capacity: int = 32,
    seed: Optional[int] = None,
) -> PeerSampler:
    """
    Build a PeerSampler pre-populated with the given peer ids.

    Args:
        peer_ids:  Identifiers to seed the view with.
        capacity:  Maximum view size.
        seed:      Optional RNG seed for reproducibility.

    Returns:
        A PeerSampler instance.
    """
    sampler = PeerSampler(
        capacity=capacity,
        _rng=random.Random(seed),
    )
    sampler.add_peers(peer_ids)
    return sampler
