"""
Integration Protocol — Section 7 implementation.

Ten message types (M1–M10).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class MessageType(str, Enum):
    """Ten protocol messages (Section 7.2)."""
    CHANGESET_ADMITTED = "M1"      # AetherFlow → AetherProof
    VERIFICATION_REQUEST = "M2"    # AetherFlow → AetherProof
    VERIFICATION_RESULT = "M3"     # AetherProof → AetherFlow
    COUNTEREXAMPLE_FOUND = "M4"    # AetherProof → AetherFlow
    REMEDIATION_PATCH = "M5"       # AetherProof → AetherFlow
    ESCALATION = "M6"              # AetherProof → AetherFlow
    EVIDENCE_QUERY = "M7"          # AetherFlow → AetherProof
    EVIDENCE_RESPONSE = "M8"       # AetherProof → AetherFlow
    HEALTH_CHECK = "M9"            # Both
    VERSION_NEGOTIATION = "M10"    # Both


@dataclass
class Envelope:
    """Message envelope (Section 4.1)."""
    version: str
    message_id: str
    timestamp: float
    source: str
    destination: str
    payload: dict


@dataclass
class Message:
    """A protocol message."""
    message_type: MessageType
    payload: dict
    source: str = "aetherproof"
    destination: str = "aetherflow"
    protocol_version: str = "1.0.0"

    def to_envelope(self) -> Envelope:
        """Convert to envelope."""
        return Envelope(
            version=self.protocol_version,
            message_id=f"msg-{time.time_ns()}",
            timestamp=time.time(),
            source=self.source,
            destination=self.destination,
            payload={
                "type": self.message_type.value,
                **self.payload,
            },
        )


__all__ = ["Message", "MessageType", "Envelope"]
