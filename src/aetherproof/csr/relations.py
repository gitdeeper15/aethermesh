"""
Semantic Relations — Definition 2 implementation.

Seven typed relations: refines, instantiates, approximates, implies,
contradicts, depends_on, supersedes.

See manuscript Section 3.3.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RelationType(str, Enum):
    """Seven semantic relations (Section 3.3)."""
    REFINES = "refines"
    INSTANTIATES = "instantiates"
    APPROXIMATES = "approximates"
    IMPLIES = "implies"
    CONTRADICTS = "contradicts"
    DEPENDS_ON = "depends_on"
    SUPERSEDES = "supersedes"


@dataclass(frozen=True)
class SemanticRelation:
    """A semantic relation between two CSR records."""
    source: str  # csr_id
    target: str  # csr_id
    relation_type: RelationType
    loss_description: Optional[str] = None  # required for approximates
    justification: str = ""

    def __post_init__(self):
        if self.relation_type == RelationType.APPROXIMATES:
            if not self.loss_description:
                raise ValueError(
                    "approximates relation requires a loss_description "
                    "(Section 3.3.1)"
                )


__all__ = ["SemanticRelation", "RelationType"]
