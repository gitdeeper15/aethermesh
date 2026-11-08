"""
AetherMesh — Epidemic gossip protocol (Pillar 2).

Implements the five-step anti-entropy exchange from Figure 5 of the
paper (Section 3.2.1):

    Step 1:  DIGEST(A)  — A sends its version summary
    Step 2:  DIGEST(B) + missing-list  — B replies with digest + deltas A lacks
    Step 3:  DELTA-REQUEST(ids)  — A requests the deltas (or pushes if B lacks)
    Step 4:  DELTA-BATCH  — B sends requested deltas, each signed
    Step 5:  local verification + join  — A admits and joins each delta

The exchange is symmetric: the same five steps apply in the reverse
direction, so each side ends up with the deltas the other had.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 3.2.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, FrozenSet, List, Optional

from aethermesh.crdt.delta_state import DeltaStateCRDT
from aethermesh.models import AdmissionVerdict, Delta


# =============================================================================
# Enums and message types
# =============================================================================

class GossipStep(str, Enum):
    """The five anti-entropy exchange steps (Figure 5 of the paper)."""
    INITIATOR_DIGEST = "1_initiator_digest"
    RESPONDER_DIGEST_AND_DIFF = "2_responder_digest_and_diff"
    DELTA_REQUEST = "3_delta_request"
    DELTA_BATCH = "4_delta_batch"
    VERIFY_AND_JOIN = "5_verify_and_join"


@dataclass(frozen=True)
class GossipMessage:
    """
    A single gossip message in the exchange.

    Attributes:
        step:      Which step this message belongs to.
        sender:    Origin agent identifier.
        payload:   Message-specific data (digest, delta ids, or deltas).
    """
    step: GossipStep
    sender: str
    payload: Dict


@dataclass
class ExchangeResult:
    """
    Outcome of one complete anti-entropy exchange between two peers.

    Attributes:
        peer_a:             Agent id of the initiating peer.
        peer_b:             Agent id of the responding peer.
        deltas_a_to_b:      Deltas A sent to B (B was missing).
        deltas_b_to_a:      Deltas B sent to A (A was missing).
        admitted_at_a:      Verdicts for deltas A received.
        admitted_at_b:      Verdicts for deltas B received.
        bytes_sent:         Approximate payload size (informational).
        steps_completed:    Number of steps that completed successfully.
    """
    peer_a: str
    peer_b: str
    deltas_a_to_b: int = 0
    deltas_b_to_a: int = 0
    admitted_at_a: List[AdmissionVerdict] = field(default_factory=list)
    admitted_at_b: List[AdmissionVerdict] = field(default_factory=list)
    bytes_sent: int = 0
    steps_completed: int = 0


# =============================================================================
# Admission function type
# =============================================================================

AdmissionFn = Callable[[Delta, DeltaStateCRDT], AdmissionVerdict]
"""A function that takes a delta and a local CRDT and returns a verdict."""


def _default_admit(delta: Delta, crdt: DeltaStateCRDT) -> AdmissionVerdict:
    """Default admission: accept everything (used for pure gossip tests)."""
    from aethermesh.models import Verdict
    return AdmissionVerdict(
        delta_id=delta.id,
        verdict=Verdict.ACCEPT,
        reason="default admit (no BFT layer attached)",
    )


# =============================================================================
# GossipProtocol
# =============================================================================

class GossipProtocol:
    """
    Runs the five-step anti-entropy exchange between two peers.

    The protocol is stateless with respect to the peers themselves;
    the caller is responsible for providing the two DeltaStateCRDT
    instances and (optionally) an admission function.

    If an admission function is not provided, all deltas are admitted
    (which is useful for testing pure gossip convergence without BFT).

    Reference: Section 3.2 of the paper.
    """

    def __init__(
        self,
        admit_fn: Optional[AdmissionFn] = None,
        digest_size_bytes: int = 32,  # informational only
    ):
        self.admit_fn = admit_fn or _default_admit
        self.digest_size_bytes = digest_size_bytes

    # -------------------------------------------------------------------------
    # The 5-step exchange
    # -------------------------------------------------------------------------

    def exchange(
        self,
        crdt_a: DeltaStateCRDT,
        crdt_b: DeltaStateCRDT,
    ) -> ExchangeResult:
        """
        Run one complete anti-entropy exchange between peers A and B.

        The exchange is symmetric: after the exchange, both peers hold
        the union of their previously admitted deltas (subject to the
        admission policy).

        Returns an ExchangeResult summarizing what was exchanged.
        """
        result = ExchangeResult(
            peer_a=crdt_a.replica.origin,
            peer_b=crdt_b.replica.origin,
        )

        # --- Step 1: initiator digest (A -> B) ---
        digest_a: FrozenSet[str] = crdt_a.digest()
        result.bytes_sent += len(digest_a) * self.digest_size_bytes
        result.steps_completed += 1

        # --- Step 2: responder digest + difference list (B -> A) ---
        digest_b: FrozenSet[str] = crdt_b.digest()
        missing_at_a_ids: FrozenSet[str] = digest_b - digest_a
        missing_at_b_ids: FrozenSet[str] = digest_a - digest_b
        result.bytes_sent += len(digest_b) * self.digest_size_bytes
        result.steps_completed += 1

        # --- Step 3: delta request (A -> B for missing at A; B -> A for missing at B) ---
        # In practice, both directions are requested simultaneously.
        # We serialize the exchange for clarity.
        result.steps_completed += 1

        # --- Step 4: delta batch (B -> A) ---
        deltas_for_a: List[Delta] = [
            crdt_b.replica.admitted[did]
            for did in missing_at_a_ids
        ]
        # And (A -> B)
        deltas_for_b: List[Delta] = [
            crdt_a.replica.admitted[did]
            for did in missing_at_b_ids
        ]
        result.bytes_sent += _estimate_bytes(deltas_for_a) + _estimate_bytes(deltas_for_b)
        result.deltas_b_to_a = len(deltas_for_a)
        result.deltas_a_to_b = len(deltas_for_b)
        result.steps_completed += 1

        # --- Step 5a: A receives deltas from B, verifies, joins ---
        for delta in deltas_for_a:
            verdict = self.admit_fn(delta, crdt_a)
            result.admitted_at_a.append(verdict)
            if verdict.accepted:
                crdt_a.apply(delta)

        # --- Step 5b: B receives deltas from A, verifies, joins ---
        for delta in deltas_for_b:
            verdict = self.admit_fn(delta, crdt_b)
            result.admitted_at_b.append(verdict)
            if verdict.accepted:
                crdt_b.apply(delta)

        result.steps_completed += 1

        return result

    # -------------------------------------------------------------------------
    # Multi-peer round
    # -------------------------------------------------------------------------

    def gossip_round(
        self,
        crdt: DeltaStateCRDT,
        peers: Dict[str, DeltaStateCRDT],
        fanout: int,
        rng: Optional[random.Random] = None,
    ) -> List[ExchangeResult]:
        """
        Run one gossip round from `crdt` to `fanout` random peers.

        Args:
            crdt:    The local replica initiating the round.
            peers:   Map from peer id -> peer's DeltaStateCRDT.
            fanout:  Number of peers to contact (k in the paper).
            rng:     Optional random.Random for reproducibility.

        Returns:
            List of ExchangeResult (one per contacted peer).
        """
        if fanout <= 0 or not peers:
            return []

        rng = rng or random.Random()
        peer_ids = sorted(peers.keys())
        k = min(fanout, len(peer_ids))
        selected = rng.sample(peer_ids, k)

        results = []
        for peer_id in selected:
            result = self.exchange(crdt, peers[peer_id])
            results.append(result)
        return results


# =============================================================================
# Helpers
# =============================================================================

def _estimate_bytes(deltas: List[Delta]) -> int:
    """
    Rough estimate of serialized delta size (informational only).

    Actual serialization is done by `models.serialize_delta`, but for
    the exchange-result accounting we use a simple heuristic:
    ~32 bytes for the hash + ~64 bytes for the body + overhead.
    """
    return len(deltas) * 96


def build_exchange_trace(result: ExchangeResult) -> List[GossipMessage]:
    """
    Reconstruct an ordered message trace from an ExchangeResult.

    Useful for logging and for testing. The trace is a simplified
    reconstruction — it does not carry the actual delta payloads.
    """
    trace: List[GossipMessage] = [
        GossipMessage(
            step=GossipStep.INITIATOR_DIGEST,
            sender=result.peer_a,
            payload={"digest_from": result.peer_a},
        ),
        GossipMessage(
            step=GossipStep.RESPONDER_DIGEST_AND_DIFF,
            sender=result.peer_b,
            payload={"digest_from": result.peer_b, "missing_at_a": result.deltas_b_to_a},
        ),
        GossipMessage(
            step=GossipStep.DELTA_REQUEST,
            sender=result.peer_a,
            payload={"requested": result.deltas_b_to_a},
        ),
        GossipMessage(
            step=GossipStep.DELTA_BATCH,
            sender=result.peer_b,
            payload={"count": result.deltas_b_to_a},
        ),
        GossipMessage(
            step=GossipStep.VERIFY_AND_JOIN,
            sender=result.peer_a,
            payload={"admitted": sum(1 for v in result.admitted_at_a if v.accepted)},
        ),
    ]
    return trace
