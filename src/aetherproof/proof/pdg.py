"""
Proof Dependency Graph (PDG) — Definition 5 implementation.

Extends ODG with evidence and assumption nodes.

See manuscript Section 5.2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from aetherproof.models import Obligation
from aetherproof.obligations.odg import ODG, EdgeType


class NodeType(str, Enum):
    """PDG node types (Section 5.2)."""
    OBLIGATION = "obligation"
    EVIDENCE = "evidence"
    ASSUMPTION = "assumption"
    CSR_RECORD = "csr_record"
    CHANGESET = "changeset"


@dataclass
class PDGNode:
    """A node in the PDG."""
    node_id: str
    node_type: NodeType
    data: dict = field(default_factory=dict)


@dataclass
class PDG:
    """
    Proof Dependency Graph (Definition 5).

    PDG = (Obligations ∪ Evidence ∪ Assumptions, Edges)
    """
    nodes: dict[str, PDGNode] = field(default_factory=dict)
    edges: list[tuple[str, str, str]] = field(default_factory=list)

    def add_node(self, node: PDGNode) -> None:
        """Add a node to the graph."""
        if node.node_id in self.nodes:
            raise ValueError(f"Node {node.node_id} already exists")
        self.nodes[node.node_id] = node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
    ) -> None:
        """Add an edge between two nodes."""
        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} not found")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} not found")

        self.edges.append((source_id, target_id, edge_type))

    def invalidate(self, changeset_id: str) -> list[str]:
        """Invalidate nodes affected by a changeset."""
        invalidated = []
        to_invalidate = []

        # Find seeds: nodes invalidated directly by the changeset
        for s, t, e in self.edges:
            if s == changeset_id and e == "invalidates":
                to_invalidate.append(t)

        # Propagate via derives_from
        while to_invalidate:
            current = to_invalidate.pop()
            if current in invalidated:
                continue
            invalidated.append(current)

            for s, t, e in self.edges:
                if s == current and e == "derives_from":
                    if t not in invalidated:
                        to_invalidate.append(t)

        return invalidated


__all__ = ["PDG", "PDGNode", "NodeType"]
