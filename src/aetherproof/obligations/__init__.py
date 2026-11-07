"""Proof obligations and Obligation Dependency Graph (ODG)."""

from aetherproof.obligations.generator import generate_obligations
from aetherproof.obligations.odg import ODG

__all__ = ["generate_obligations", "ODG"]
