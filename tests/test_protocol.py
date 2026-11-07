"""Tests for integration protocol."""

from aetherproof.protocol.messages import Message, MessageType


def test_message_creation():
    msg = Message(message_type=MessageType.VERIFICATION_REQUEST,
                  payload={"obligation_id": "O-1"})
    assert msg.message_type == MessageType.VERIFICATION_REQUEST


def test_message_to_envelope():
    msg = Message(message_type=MessageType.VERIFICATION_RESULT,
                  payload={"verdict": "proven"})
    envelope = msg.to_envelope()
    assert envelope.version == "1.0.0"
    assert envelope.payload["type"] == "M3"


def test_message_types_count():
    assert len(MessageType) == 10
