"""
Remediation Cycle — Section 6.2 implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from aetherproof.models import Counterexample
from aetherproof.remediation.diagnosis import diagnose
from aetherproof.remediation.guardrails import check_guardrails, Patch


@dataclass
class RemediationCycle:
    """
    Bounded remediation cycle (Section 6.2).

    Six stages:
    1. Counterexample detected
    2. Diagnosis
    3. Hypothesis
    4. Patch proposal
    5. Re-verify
    6. Accept/reject
    """
    max_iterations: int = 3
    iteration: int = 0
    history: list[dict] = field(default_factory=list)

    def run(
        self,
        counterexample: Counterexample,
        patch_proposer,
        re_verifier,
    ) -> dict:
        """
        Run the remediation cycle.

        Parameters
        ----------
        counterexample : Counterexample
            The counterexample to remediate.
        patch_proposer : callable
            Function that proposes patches.
        re_verifier : callable
            Function that re-verifies patches.

        Returns
        -------
        dict
            Cycle result with status.
        """
        while self.iteration < self.max_iterations:
            self.iteration += 1

            # Stage 1-2: Diagnose
            diagnosed = diagnose(counterexample)

            # Stage 3: Hypothesis (what to fix)
            # Stage 4: Patch proposal
            patch = patch_proposer(diagnosed)

            if patch is None:
                return {
                    "status": "escalated",
                    "reason": "No patch proposed",
                    "iterations": self.iteration,
                }

            # Stage 5: Check guardrails
            violations = check_guardrails(patch)
            if violations:
                self.history.append({
                    "iteration": self.iteration,
                    "violations": [v.value for v in violations],
                })
                return {
                    "status": "rejected",
                    "reason": "Guardrail violation",
                    "violations": [v.value for v in violations],
                    "iterations": self.iteration,
                }

            # Stage 5: Re-verify
            result = re_verifier(patch)

            if result.get("verified"):
                return {
                    "status": "accepted",
                    "patch": patch,
                    "iterations": self.iteration,
                }

            self.history.append({
                "iteration": self.iteration,
                "result": result,
            })

        return {
            "status": "escalated",
            "reason": "Iteration bound reached",
            "iterations": self.iteration,
        }


__all__ = ["RemediationCycle"]
