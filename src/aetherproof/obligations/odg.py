"""
Obligation Dependency Graph (ODG) — Section 4.3 implementation.

The ODG is a directed acyclic graph over obligations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from aetherproof.models import Obligation, Verdict


class EdgeType(str, Enum):
    """ODG edge types (Section 4.3)."""
    REQUIRES = "requires"
    REFINES = "refines"
    ASSUMES = "assumes"
    CONTRADICTS = "contradicts"


@dataclass
class ODG:
    """Obligation Dependency Graph."""
    obligations: dict[str, Obligation] = field(default_factory=dict)
    edges: list[tuple[str, str, EdgeType]] = field(default_factory=list)

    def add_obligation(self, obligation: Obligation) -> None:
        """Add an obligation to the graph."""
        self.obligations[obligation.id] = obligation

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
    ) -> None:
        """Add an edge between two obligations."""
        if source_id not in self.obligations:
            raise ValueError(f"Source obligation {source_id} not found")
        if target_id not in self.obligations:
            raise ValueError(f"Target obligation {target_id} not found")

        # Check for cycles in dependency-bearing edges
        if edge_type in (EdgeType.REQUIRES, EdgeType.REFINES, EdgeType.ASSUMES):
            if self._would_create_cycle(source_id, target_id):
                raise ValueError(
                    f"Adding edge ({source_id} -> {target_id}) "
                    f"would create a cycle (Proposition P3)"
                )

        self.edges.append((source_id, target_id, edge_type))

    def _would_create_cycle(self, source_id: str, target_id: str) -> bool:
        """Check if adding an edge would create a cycle."""
        # Simple DFS from target_id to see if we can reach source_id
        visited: set[str] = set()
        stack = [target_id]

        while stack:
            current = stack.pop()
            if current == source_id:
                return True
            if current in visited:
                continue
            visited.add(current)

            for s, t, e in self.edges:
                if s == current and e in (
                    EdgeType.REQUIRES, EdgeType.REFINES, EdgeType.ASSUMES
                ):
                    stack.append(t)

        return False

    def invalidate(self, obligation_id: str) -> list[str]:
        """
        Invalidate an obligation and all dependents.

        Returns list of invalidated obligation IDs.

        The invalidation propagates FORWARD: if O1 requires O2 (O1 depends on O2),
        then invalidating O2 invalidates O1. The edge direction is (source, target),
        meaning "source depends on target". So if we invalidate `obligation_id`,
        we need to find all `source` that point to `obligation_id` as their target.
        """
        if obligation_id not in self.obligations:
            raise ValueError(f"Obligation {obligation_id} not found")

        invalidated = []
        to_invalidate = {obligation_id}

        while to_invalidate:
            current = to_invalidate.pop()
            if current in invalidated:
                continue

            invalidated.append(current)

            # Find dependents: obligations that require/refine/assume current
            # Edge direction is (source, target), where source depends on target.
            # So if target == current, then source is a dependent.
            for s, t, e in self.edges:
                if t == current and e in (
                    EdgeType.REQUIRES, EdgeType.REFINES, EdgeType.ASSUMES
                ):
                    if s not in invalidated:
                        to_invalidate.add(s)

        return invalidated


__all__ = ["ODG", "EdgeType"]
