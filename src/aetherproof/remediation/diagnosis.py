"""
Diagnosis Protocol — Section 6.3 implementation.
"""

from __future__ import annotations

from aetherproof.models import Counterexample, CounterexampleType


def diagnose(
    counterexample: Counterexample,
    is_reproducible: bool = True,
    refutes_assumption: bool = False,
    is_valid_model: bool = True,
    refutes_specification: bool = False,
) -> Counterexample:
    """
    Diagnose a counterexample.

    Implements the decision tree from Section 6.3.
    """
    if not is_reproducible:
        return _update_type(counterexample, CounterexampleType.FLAKY_REFUTATION)

    if refutes_assumption:
        return _update_type(
            counterexample, CounterexampleType.ASSUMPTION_VIOLATION
        )

    if is_valid_model:
        if refutes_specification:
            return _update_type(
                counterexample, CounterexampleType.SPECIFICATION_ERROR
            )
        else:
            return _update_type(counterexample, CounterexampleType.CODE_DEFECT)
    else:
        return _update_type(counterexample, CounterexampleType.MODEL_ERROR)


def _update_type(
    counterexample: Counterexample,
    new_type: CounterexampleType,
) -> Counterexample:
    """Return a new counterexample with updated type."""
    return Counterexample(
        id=counterexample.id,
        obligation=counterexample.obligation,
        witness=counterexample.witness,
        refutation_evidence=counterexample.refutation_evidence,
        type=new_type,
        provenance=counterexample.provenance,
    )


__all__ = ["diagnose"]
