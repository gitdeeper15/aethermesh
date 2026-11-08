"""
AetherMesh — Simulated network model (fair-lossy channels).

Implements the fair-lossy channel model from Section 4.0 of the paper
(assumption A1):

    A message sent infinitely often between two non-faulty nodes is
    delivered infinitely often.

In the simulator, the network is a discrete event loop that delivers
messages between nodes with configurable:
    - latency (uniform in [min_latency, max_latency])
    - drop probability (0.0 = no drops; 1.0 = every message dropped)
    - partition schedule (optional, list of (time, partition_set))

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 4.0, assumption A1.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import heapq
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# =============================================================================
# Message
# =============================================================================

@dataclass(order=True)
class _ScheduledMessage:
    """Internal: a message scheduled for delivery at a future time."""
    delivery_time: float
    sender: str = field(compare=False)
    recipient: str = field(compare=False)
    payload: Any = field(compare=False)


# =============================================================================
# Network
# =============================================================================

class Network:
    """
    A simulated fair-lossy network.

    The network maintains a priority queue of scheduled messages,
    ordered by delivery time. It also maintains a partition state:
    a set of node ids that cannot communicate with the rest.

    Attributes:
        min_latency:      Minimum one-way latency (seconds).
        max_latency:      Maximum one-way latency (seconds).
        drop_probability: Probability that any given message is dropped.
        rng:              Random source (seeded for reproducibility).
    """

    def __init__(
        self,
        min_latency: float = 0.01,
        max_latency: float = 0.05,
        drop_probability: float = 0.0,
        seed: Optional[int] = None,
    ):
        self.min_latency = min_latency
        self.max_latency = max_latency
        self.drop_probability = drop_probability
        self.rng = random.Random(seed)

        # Message queue: (delivery_time, _ScheduledMessage)
        self._queue: List[_ScheduledMessage] = []

        # Partition state: set of nodes currently partitioned from the rest
        self._partitioned: Set[str] = set()

        # Statistics
        self.messages_sent = 0
        self.messages_delivered = 0
        self.messages_dropped = 0
        self.messages_blocked_by_partition = 0

    # -------------------------------------------------------------------------
    # Sending
    # -------------------------------------------------------------------------

    def send(
        self,
        sender: str,
        recipient: str,
        payload: Any,
        send_time: float,
    ) -> bool:
        """
        Schedule a message for delivery. Returns True if it will be
        delivered (subject to drop probability and partition state).

        A message is dropped with probability `drop_probability`.
        A message is blocked if sender and recipient are on opposite
        sides of a partition.
        """
        self.messages_sent += 1

        # Partition check.
        if self._partition_blocks(sender, recipient):
            self.messages_blocked_by_partition += 1
            return False

        # Drop check.
        if self.rng.random() < self.drop_probability:
            self.messages_dropped += 1
            return False

        # Schedule delivery.
        latency = self.rng.uniform(self.min_latency, self.max_latency)
        delivery_time = send_time + latency
        msg = _ScheduledMessage(
            delivery_time=delivery_time,
            sender=sender,
            recipient=recipient,
            payload=payload,
        )
        heapq.heappush(self._queue, msg)
        return True

    # -------------------------------------------------------------------------
    # Delivery
    # -------------------------------------------------------------------------

    def next_delivery_time(self) -> Optional[float]:
        """The time of the next scheduled message, or None if empty."""
        if not self._queue:
            return None
        return self._queue[0].delivery_time

    def deliver_until(
        self,
        current_time: float,
        on_delivery: Callable[[str, str, Any], None],
    ) -> float:
        """
        Deliver all messages scheduled at or before `current_time`.

        Calls `on_delivery(sender, recipient, payload)` for each.

        Returns the time of the next scheduled message, or `current_time`
        if the queue is empty.
        """
        while self._queue and self._queue[0].delivery_time <= current_time:
            msg = heapq.heappop(self._queue)
            self.messages_delivered += 1
            on_delivery(msg.sender, msg.recipient, msg.payload)
        return self.next_delivery_time() or current_time

    # -------------------------------------------------------------------------
    # Partitions
    # -------------------------------------------------------------------------

    def set_partition(self, partitioned_nodes: Set[str]) -> None:
        """
        Set the current partition: nodes in `partitioned_nodes` cannot
        communicate with nodes outside it.
        """
        self._partitioned = set(partitioned_nodes)

    def heal_partition(self) -> None:
        """Clear the partition state."""
        self._partitioned = set()

    def _partition_blocks(self, sender: str, recipient: str) -> bool:
        """Check if a partition blocks communication between two nodes."""
        if not self._partitioned:
            return False
        sender_in = sender in self._partitioned
        recipient_in = recipient in self._partitioned
        return sender_in != recipient_in

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def stats(self) -> Dict[str, int]:
        return {
            "messages_sent": self.messages_sent,
            "messages_delivered": self.messages_delivered,
            "messages_dropped": self.messages_dropped,
            "messages_blocked_by_partition": self.messages_blocked_by_partition,
            "messages_in_flight": len(self._queue),
        }

    def reset_stats(self) -> None:
        self.messages_sent = 0
        self.messages_delivered = 0
        self.messages_dropped = 0
        self.messages_blocked_by_partition = 0


# =============================================================================
# Partition schedules
# =============================================================================

@dataclass
class PartitionEvent:
    """A scheduled partition event: at `time`, set `partitioned`."""
    time: float
    partitioned: Set[str] = field(default_factory=set)


class PartitionSchedule:
    """
    A schedule of partition events over simulated time.

    Used by the testbed to model network partitions (Section 3.2.3 of
    the paper: partition healing).

    Example:
        >>> schedule = PartitionSchedule([
        ...     PartitionEvent(time=1.0, partitioned={"n1", "n2"}),
        ...     PartitionEvent(time=2.0, partitioned=set()),  # heal
        ... ])
    """

    def __init__(self, events: List[PartitionEvent]):
        self.events = sorted(events, key=lambda e: e.time)
        self._applied_index = 0

    def apply_until(self, current_time: float, network: Network) -> None:
        """Apply all partition events with time <= current_time."""
        while self._applied_index < len(self.events):
            event = self.events[self._applied_index]
            if event.time > current_time:
                break
            network.set_partition(event.partitioned)
            self._applied_index += 1

    def reset(self) -> None:
        self._applied_index = 0
