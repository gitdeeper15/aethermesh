"""
AetherMesh — Admission pipeline (Pillar 3 integration).

Integrates the three BFT checks from Figure 7 of the paper into a
single admission pipeline:

    Step 2:  Signature check      (Check 1: Signature)
    Step 3:  DAG integrity check  (Check 2: DAG integrity)
    Step 4:  Schema check         (Check 3: Schema)
    Step 5:  Semantics check      (Check 4: Semantics)
    Step 6:  Join to semilattice  (if all checks pass)

A delta that fails any check is rejected (or deferred, if its parents
are missing). A delta that passes all checks is admitted.

The admission determinism requirement (A6) is respected: every check
is a pure, deterministic function of the delta and its causal closure
(not of arrival order or local clock).

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 3.3.4 and Figure 7.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from aethermesh.models import (
    AdmissionStage,
    AdmissionVerdict,
    Delta,
    Replica,
    Verdict,
)
from aethermesh.bft.provenance import ProvenanceChecker, KeyRegistry
from aethermesh.bft.invariants import StructuralChecker
from aethermesh.bft.semantic_matrix import (
    CompatibilityMatrix,
    DEFAULT_MATRIX,
    SemanticVerdict,
)


# =============================================================================
# StageResult
# =============================================================================

@dataclass(frozen=True)
class StageResult:
    """Result of one pipeline stage."""
    stage: AdmissionStage
    ok: bool
    reason: str
    verdict: Verdict  # what the stage recommends (for defer handling)


# =============================================================================
# PipelineConfig
# =============================================================================

@dataclass
class PipelineConfig:
    """
    Configuration for the admission pipeline.

    Attributes:
        max_parents:      Max parents per delta (structural bound).
        max_bytes:        Max serialized delta size (structural bound).
        reject_on_semantic_conflict:  If True, semantic CONFLICT => reject.
                                      If False, semantic CONFLICT => quarantine.
        quarantine_on_semantic_resolve: If True, semantic RESOLVE => quarantine.
        schema_validator: Optional custom schema validator (delta -> bool).
    """
    max_parents: int = 64
    max_bytes: int = 1_048_576
    reject_on_semantic_conflict: bool = True
    quarantine_on_semantic_resolve: bool = False
    schema_validator: Optional[Callable[[Delta], Tuple[bool, str]]] = None


# =============================================================================
# Default schema validator
# =============================================================================

def _default_schema_validator(delta: Delta) -> Tuple[bool, str]:
    """
    Default schema check: the delta body must be a JSON-serializable
    dict, and must contain an 'op' field (a string).
    """
    if not isinstance(delta.body, dict):
        return False, f"body must be a dict, got {type(delta.body).__name__}"
    if "op" not in delta.body:
        return False, "body missing 'op' field"
    if not isinstance(delta.body["op"], str):
        return False, f"'op' must be a string, got {type(delta.body['op']).__name__}"
    try:
        json.dumps(delta.body, sort_keys=True)
    except (TypeError, ValueError) as e:
        return False, f"body not JSON-serializable: {e}"
    return True, "ok"


# =============================================================================
# AdmissionPipeline
# =============================================================================

@dataclass
class AdmissionPipeline:
    """
    The four-check admission pipeline (Figure 7 of the paper).

    The pipeline is a pure function of (delta, replica_state):
    given the same delta and the same causal closure, every honest
    node reaches the same verdict (assumption A6).

    Attributes:
        registry:      Key registry for provenance.
        matrix:        Semantic compatibility matrix.
        config:        Pipeline configuration.
    """
    registry: KeyRegistry = field(default_factory=KeyRegistry)
    matrix: CompatibilityMatrix = field(default_factory=lambda: DEFAULT_MATRIX)
    config: PipelineConfig = field(default_factory=PipelineConfig)

    def __post_init__(self):
        self._provenance = ProvenanceChecker(registry=self.registry)
        self._structural = StructuralChecker(
            max_parents=self.config.max_parents,
            max_bytes=self.config.max_bytes,
        )
        self._schema = self.config.schema_validator or _default_schema_validator

    # -------------------------------------------------------------------------
    # The four checks
    # -------------------------------------------------------------------------

    def check_signature(self, delta: Delta) -> StageResult:
        """Check 1: Signature (Section 3.3.1)."""
        ok, reason = self._provenance.check(delta)
        verdict = Verdict.ACCEPT if ok else Verdict.REJECT
        return StageResult(AdmissionStage.SIGNATURE, ok, reason, verdict)

    def check_dag_integrity(
        self,
        delta: Delta,
        replica: Replica,
    ) -> StageResult:
        """
        Check 2: DAG integrity (Section 3.3.2).

        A delta with missing parents is DEFERRED, not rejected.
        """
        # Structural bounds first.
        ok, reason = self._structural.check(delta)
        if not ok:
            return StageResult(AdmissionStage.DAG_INTEGRITY, False, reason, Verdict.REJECT)

        # Parent presence: if any parent is missing, DEFER.
        if not replica.has_parents(delta):
            missing = [p for p in delta.parents if p not in replica.admitted]
            return StageResult(
                AdmissionStage.DAG_INTEGRITY,
                False,
                f"missing parents: {missing[:3]}",
                Verdict.DEFER,
            )

        return StageResult(AdmissionStage.DAG_INTEGRITY, True, "ok", Verdict.ACCEPT)

    def check_schema(self, delta: Delta) -> StageResult:
        """Check 3: Schema (Section 3.3.3)."""
        ok, reason = self._schema(delta)
        verdict = Verdict.ACCEPT if ok else Verdict.REJECT
        return StageResult(AdmissionStage.SCHEMA, ok, reason, verdict)

    def check_semantics(
        self,
        delta: Delta,
        replica: Replica,
    ) -> StageResult:
        """
        Check 4: Semantics (Section 3.3.3).

        The semantic check is over the causal closure of the delta
        (the delta plus its admitted ancestors).
        """
        # Compute the causal closure (delta + admitted ancestors).
        closure = [delta]
        visited = set()
        frontier = list(delta.parents)
        while frontier:
            did = frontier.pop()
            if did in visited:
                continue
            visited.add(did)
            ancestor = replica.admitted.get(did)
            if ancestor is not None:
                closure.append(ancestor)
                frontier.extend(ancestor.parents)

        verdict, reason = self.matrix.check(closure)

        if verdict == SemanticVerdict.OK:
            return StageResult(AdmissionStage.SEMANTICS, True, "ok", Verdict.ACCEPT)
        if verdict == SemanticVerdict.RESOLVE:
            if self.config.quarantine_on_semantic_resolve:
                return StageResult(AdmissionStage.SEMANTICS, False, reason, Verdict.QUARANTINE)
            return StageResult(AdmissionStage.SEMANTICS, False, reason, Verdict.REJECT)
        # CONFLICT
        if self.config.reject_on_semantic_conflict:
            return StageResult(AdmissionStage.SEMANTICS, False, reason, Verdict.REJECT)
        return StageResult(AdmissionStage.SEMANTICS, False, reason, Verdict.QUARANTINE)

    # -------------------------------------------------------------------------
    # Full pipeline
    # -------------------------------------------------------------------------

    def admit(
        self,
        delta: Delta,
        replica: Replica,
    ) -> AdmissionVerdict:
        """
        Run the full pipeline on a delta against a local replica.

        Returns an AdmissionVerdict with the final outcome.

        The pipeline short-circuits on the first failing stage.
        """
        # Idempotence: if already admitted, accept immediately.
        if delta.id in replica:
            return AdmissionVerdict(
                delta_id=delta.id,
                verdict=Verdict.ACCEPT,
                stage=None,
                reason="already admitted",
            )

        # Check 1: Signature
        r = self.check_signature(delta)
        if not r.ok:
            return AdmissionVerdict(delta.id, r.verdict, r.stage, r.reason)

        # Check 2: DAG integrity (may defer)
        r = self.check_dag_integrity(delta, replica)
        if not r.ok:
            return AdmissionVerdict(delta.id, r.verdict, r.stage, r.reason)

        # Check 3: Schema
        r = self.check_schema(delta)
        if not r.ok:
            return AdmissionVerdict(delta.id, r.verdict, r.stage, r.reason)

        # Check 4: Semantics
        r = self.check_semantics(delta, replica)
        if not r.ok:
            return AdmissionVerdict(delta.id, r.verdict, r.stage, r.reason)

        return AdmissionVerdict(
            delta_id=delta.id,
            verdict=Verdict.ACCEPT,
            stage=None,
            reason="admitted",
        )


# =============================================================================
# Convenience: build a pipeline with a fresh registry
# =============================================================================

def build_pipeline(
    registry: Optional[KeyRegistry] = None,
    config: Optional[PipelineConfig] = None,
) -> AdmissionPipeline:
    """Build an admission pipeline with sensible defaults."""
    return AdmissionPipeline(
        registry=registry or KeyRegistry(),
        config=config or PipelineConfig(),
    )
