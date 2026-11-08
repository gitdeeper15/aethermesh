"""
Tests for aethermesh.gossip — protocol and peer sampling.

Covers:
    - Anti-entropy exchange (5 steps)
    - Convergence after one exchange
    - Multi-peer gossip round
    - Peer sampler (add, remove, sample, capacity)
    - ExchangeResult fields
"""

import pytest

from aethermesh.models import Delta, DeltaKind
from aethermesh.crdt.delta_state import DeltaStateCRDT
from aethermesh.gossip.protocol import (
    GossipProtocol,
    GossipStep,
    build_exchange_trace,
)
from aethermesh.gossip.peer_sampling import (
    PeerSampler,
    ViewStatus,
    build_sampler,
)


# =============================================================================
# GossipProtocol
# =============================================================================

class TestGossipProtocol:
    def test_exchange_converges_in_one_round(self):
        a = DeltaStateCRDT(origin="a")
        b = DeltaStateCRDT(origin="b")

        d1 = Delta.create(body={"op": "a1"}, origin="a", kind=DeltaKind.EDIT_BODY)
        d2 = Delta.create(body={"op": "b1"}, origin="b", kind=DeltaKind.EDIT_BODY)
        a.apply(d1)
        b.apply(d2)

        proto = GossipProtocol()
        result = proto.exchange(a, b)

        assert a.state_size() == 2
        assert b.state_size() == 2
        assert a.ids() == b.ids()
        assert result.deltas_a_to_b == 1
        assert result.deltas_b_to_a == 1

    def test_exchange_no_changes_when_identical(self):
        a = DeltaStateCRDT(origin="a")
        b = DeltaStateCRDT(origin="b")
        d = Delta.create(body={"op": "shared"}, origin="a", kind=DeltaKind.EDIT_BODY)
        a.apply(d)
        b.apply(d)

        proto = GossipProtocol()
        result = proto.exchange(a, b)

        assert result.deltas_a_to_b == 0
        assert result.deltas_b_to_a == 0

    def test_exchange_steps_completed(self):
        a = DeltaStateCRDT(origin="a")
        b = DeltaStateCRDT(origin="b")
        d = Delta.create(body={"op": "x"}, origin="a", kind=DeltaKind.EDIT_BODY)
        a.apply(d)

        proto = GossipProtocol()
        result = proto.exchange(a, b)

        assert result.steps_completed == 5

    def test_gossip_round_fanout(self):
        a = DeltaStateCRDT(origin="a")
        peers = {}
        for i in range(5):
            pid = f"peer-{i}"
            p = DeltaStateCRDT(origin=pid)
            peers[pid] = p

        proto = GossipProtocol()
        results = proto.gossip_round(a, peers, fanout=3)
        assert len(results) == 3

    def test_gossip_round_zero_fanout(self):
        a = DeltaStateCRDT(origin="a")
        peers = {"p1": DeltaStateCRDT(origin="p1")}

        proto = GossipProtocol()
        results = proto.gossip_round(a, peers, fanout=0)
        assert results == []


# =============================================================================
# PeerSampler
# =============================================================================

class TestPeerSampler:
    def test_add_peer(self):
        s = PeerSampler(capacity=10)
        assert s.add_peer("p1") is True
        assert "p1" in s
        assert len(s) == 1

    def test_add_existing_peer(self):
        s = PeerSampler(capacity=10)
        s.add_peer("p1")
        assert s.add_peer("p1") is False
        assert len(s) == 1

    def test_remove_peer(self):
        s = PeerSampler(capacity=10)
        s.add_peer("p1")
        assert s.remove_peer("p1") is True
        assert "p1" not in s

    def test_remove_missing_peer(self):
        s = PeerSampler(capacity=10)
        assert s.remove_peer("missing") is False

    def test_sample_k(self):
        s = build_sampler(["p1", "p2", "p3", "p4", "p5"], capacity=10, seed=42)
        sample = s.sample(3)
        assert len(sample) == 3
        assert all(p in s for p in sample)

    def test_sample_more_than_available(self):
        s = build_sampler(["p1", "p2"], capacity=10, seed=42)
        sample = s.sample(10)
        assert len(sample) == 2

    def test_sample_empty(self):
        s = PeerSampler(capacity=10)
        assert s.sample(3) == []

    def test_capacity_eviction(self):
        s = PeerSampler(capacity=3)
        s.add_peer("p1")
        s.add_peer("p2")
        s.add_peer("p3")
        s.add_peer("p4")  # should evict one
        assert len(s) == 3

    def test_status(self):
        s = PeerSampler(capacity=3)
        assert s.status() == ViewStatus.EMPTY
        s.add_peer("p1")
        assert s.status() == ViewStatus.PARTIAL
        s.add_peer("p2")
        s.add_peer("p3")
        assert s.status() == ViewStatus.FULL

    def test_clear(self):
        s = build_sampler(["p1", "p2"], capacity=10)
        s.clear()
        assert len(s) == 0
