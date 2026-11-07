"""
Invalidation Rules — Section 5.3 implementation.
"""

from __future__ import annotations

from aetherproof.proof.pdg import PDG


def invalidate(
    changeset_id: str,
    pdg: PDG,
    blast_radius: set[str] | None = None,
) -> list[str]:
    """
    Invalidate nodes affected by a changeset.

    Implements the worklist algorithm from Section 5.3.

    Parameters
    ----------
    changeset_id : str
        The changeset that triggered invalidation.
    pdg : PDG
        The proof dependency graph.
    blast_radius : set[str], optional
        Files/symbols affected by the changeset.

    Returns
    -------
    list[str]
        IDs of invalidated nodes.
    """
    invalidated: set[str] = set()
    worklist: list[str] = []

    # Seed: nodes directly invalidated by the changeset
    for s, t, e in pdg.edges:
        if s == changeset_id and e == "invalidates":
            worklist.append(t)

    # Seed: nodes within blast radius
    if blast_radius:
        for node_id, node in pdg.nodes.items():
            if node.node_type.value == "obligation":
                node_blast = node.data.get("blast_radius", set())
                if node_blast & blast_radius:
                    worklist.append(node_id)

    # Worklist fixpoint
    while worklist:
        current = worklist.pop()
        if current in invalidated:
            continue
        invalidated.add(current)

        # Propagate via derives_from
        for s, t, e in pdg.edges:
            if s == current and e == "derives_from":
                if t not in invalidated:
                    worklist.append(t)

    return list(invalidated)


__all__ = ["invalidate"]
