"""
AetherMesh v2.0.0 — Reference Implementation

Decentralized Peer-to-Peer Agent Synchronization and State CRDTs
for Autonomous Multi-Agent Systems.

This is the reference implementation of the AetherMesh architecture
described in the v1.0.0 research paper:

    Baladi, S. (2026). AetherMesh: Decentralized Peer-to-Peer Agent
    Synchronization and State CRDTs for Autonomous Multi-Agent Systems.
    Zenodo. https://doi.org/10.5281/zenodo.24038038

The v1.0.0 paper specifies the architecture with proof sketches and
a simulated evaluation. This package (v2.0.0) provides a reference
implementation of the three pillars:

    1. CRDTs for Code and Metadata DAGs
    2. Epidemic Gossip Protocols
    3. Lightweight Byzantine Fault Tolerance

Status: Reference implementation. Preliminary results. Not a
production system. Real-world deployment has not been evaluated.
"""

from aethermesh.__version__ import __version__, __author__, __email__, __doi__, __license__

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__doi__",
    "__license__",
]
