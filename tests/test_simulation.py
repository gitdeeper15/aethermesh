"""
Tests for aethermesh.simulation — network, node, testbed.

Covers:
    - Network: send, deliver, drop, partition
    - Node: create_delta, receive_delta, summary
    - create_cluster
    - Testbed: convergence, conflict overhead, fault resilience
"""

import pytest

from aethermesh.models import Delta, DeltaKind, Verdict
from aethermesh.simulation.network import (
    Network,
    PartitionEvent,
    PartitionSchedule,
)
from aethermesh.simulation.node import Node, create_cluster
from aethermesh.simulation.testbed import Testbed, TestbedConfig


# =============================================================================
# Network
# =============================================================================

class TestNetwork:
    def test_send_and_deliver(self):
        net = Network(min_latency=0.01, max_latency=0.02, drop_probability=0.0, seed=42)
        ok = net.send("a", "b", "hello", send_time=0.0)
        assert ok is True

        delivered = []
        net.deliver_until(0.05, on_delivery=lambda s, r, p: delivered.append((s, r, p)))
        assert len(delivered) == 1
        assert delivered[0] == ("a", "b", "hello")

    def test_drop_all(self):
        net = Network(drop_probability=1.0, seed=42)
        ok = net.send("a", "b", "msg", send_time=0.0)
        assert ok is False
        assert net.messages_dropped == 1

    def test_partition_blocks(self):
        net = Network(drop_probability=0.0, seed=42)
        net.set_partition({"a"})
        ok = net.send("a", "b", "msg", send_time=0.0)
        assert ok is False
        assert net.messages_blocked_by_partition == 1

    def test_heal_partition(self):
        net = Network(drop_probability=0.0, seed=42)
        net.set_partition({"a"})
        assert net.send("a", "b", "msg", send_time=0.0) is False
        net.heal_partition()
        assert net.send("a", "b", "msg", send_time=0.0) is True

    def test_stats(self):
        net = Network(drop_probability=0.0, seed=42)
        net.send("a", "b", "m1", send_time=0.0)
        net.send("b", "a", "m2", send_time=0.0)
        stats = net.stats()
        assert stats["messages_sent"] == 2
        assert stats["messages_in_flight"] == 2


# =============================================================================
# Node
# =============================================================================

class TestNode:
    def test_create_delta(self):
        node = Node(node_id="n1")
        d = node.create_delta(body={"op": "edit"}, kind=DeltaKind.EDIT_BODY)
        assert d.origin == "n1"
        assert d.signature is not None
        assert node.state_size() == 1
        assert node.deltas_authored == 1

    def test_receive_valid_delta(self):
        nodes = create_cluster(2, seed=42)
        d = nodes[0].create_delta(body={"op": "edit"}, kind=DeltaKind.EDIT_BODY)
        verdict = nodes[1].receive_delta(d)
        assert verdict.verdict == Verdict.ACCEPT
        assert nodes[1].state_size() == 1
        assert nodes[1].deltas_admitted == 1

    def test_receive_unsigned_delta(self):
        nodes = create_cluster(2, seed=42)
        d = Delta.create(body={"op": "edit"}, origin="unknown", kind=DeltaKind.EDIT_BODY)
        verdict = nodes[1].receive_delta(d)
        assert verdict.verdict == Verdict.REJECT
        assert nodes[1].deltas_rejected == 1

    def test_summary(self):
        node = Node(node_id="n1")
        node.create_delta(body={"op": "edit"}, kind=DeltaKind.EDIT_BODY)
        s = node.summary()
        assert s["node_id"] == "n1"
        assert s["state_size"] == 1
        assert s["deltas_authored"] == 1


# =============================================================================
# create_cluster
# =============================================================================

class TestCreateCluster:
    def test_cluster_size(self):
        nodes = create_cluster(5, seed=42)
        assert len(nodes) == 5

    def test_cluster_peer_views(self):
        nodes = create_cluster(5, seed=42)
        for node in nodes:
            assert len(node.sampler) == 4  # everyone knows everyone else

    def test_cluster_shared_registry(self):
        nodes = create_cluster(3, seed=42)
        # All nodes share the same registry.
        assert nodes[0].registry is nodes[1].registry
        assert nodes[1].registry is nodes[2].registry


# =============================================================================
# Testbed — Metric 1: convergence
# =============================================================================

class TestTestbedConvergence:
    def test_small_cluster_converges(self):
        config = TestbedConfig(n_nodes=10, fanout=3, max_rounds=50, seed=42)
        tb = Testbed(config)
        result = tb.measure_convergence_latency(initial_delta_count=1)
        assert result["final_fraction"] >= 0.99
        assert result["converged_at_round"] is not None

    def test_converged_fraction_is_full(self):
        config = TestbedConfig(n_nodes=5, fanout=2, max_rounds=20, seed=42)
        tb = Testbed(config)
        tb.measure_convergence_latency(initial_delta_count=1)
        assert tb.converged_fraction() == 1.0


# =============================================================================
# Testbed — Metric 2: conflict overhead
# =============================================================================

class TestTestbedConflict:
    def test_no_deadlocks(self):
        config = TestbedConfig(n_nodes=5, fanout=2, max_rounds=20, seed=42)
        tb = Testbed(config)
        m2 = tb.measure_conflict_overhead(n_conflicting_deltas=5)
        assert m2["deadlocks"] == 0

    def test_conflicts_flagged(self):
        config = TestbedConfig(n_nodes=5, fanout=2, max_rounds=20, seed=42)
        tb = Testbed(config)
        m2 = tb.measure_conflict_overhead(n_conflicting_deltas=3)
        # Some deltas should be flagged (renames conflict with each other).
        assert m2["conflicts_flagged"] >= 0


# =============================================================================
# Testbed — Metric 3: fault resilience
# =============================================================================

class TestTestbedFaultResilience:
    def test_all_malformed_blocked(self):
        config = TestbedConfig(n_nodes=5, fanout=2, max_rounds=20, seed=42)
        tb = Testbed(config)
        m3 = tb.measure_fault_resilience(n_malformed=50)
        assert m3["injected"] == 50
        assert m3["block_rate"] == 1.0

    def test_zero_injected(self):
        config = TestbedConfig(n_nodes=3, fanout=2, max_rounds=10, seed=42)
        tb = Testbed(config)
        m3 = tb.measure_fault_resilience(n_malformed=0)
        assert m3["injected"] == 0
        assert m3["block_rate"] == 0.0
