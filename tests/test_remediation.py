"""Tests for counterexample remediation."""

import pytest

from aetherproof.models import Counterexample, CounterexampleType
from aetherproof.remediation.diagnosis import diagnose
from aetherproof.remediation.guardrails import check_guardrails, Patch, ViolationType


def test_diagnose_code_defect():
    cex = Counterexample.create("O-1", "x = -1", "model-1")
    diagnosed = diagnose(cex, is_reproducible=True, refutes_assumption=False,
                         is_valid_model=True, refutes_specification=False)
    assert diagnosed.type == CounterexampleType.CODE_DEFECT


def test_diagnose_specification_error():
    cex = Counterexample.create("O-1", "x = -1", "model-1")
    diagnosed = diagnose(cex, is_reproducible=True, refutes_assumption=False,
                         is_valid_model=True, refutes_specification=True)
    assert diagnosed.type == CounterexampleType.SPECIFICATION_ERROR


def test_diagnose_flaky_refutation():
    cex = Counterexample.create("O-1", "x = -1", "model-1")
    diagnosed = diagnose(cex, is_reproducible=False)
    assert diagnosed.type == CounterexampleType.FLAKY_REFUTATION


def test_guardrails_pass():
    patch = Patch(files_changed={"src/main.py"}, deleted_tests=set(),
                  disabled_tests=set(), widened_assertions=[],
                  blast_radius={"src/main.py", "tests/"})
    violations = check_guardrails(patch)
    assert len(violations) == 0


def test_guardrails_test_deleted():
    patch = Patch(files_changed={"src/main.py"}, deleted_tests={"test_foo"},
                  disabled_tests=set(), widened_assertions=[],
                  blast_radius={"src/main.py"})
    violations = check_guardrails(patch)
    assert ViolationType.TEST_DELETED in violations


def test_guardrails_outside_blast_radius():
    patch = Patch(files_changed={"src/other.py"}, deleted_tests=set(),
                  disabled_tests=set(), widened_assertions=[],
                  blast_radius={"src/main.py"})
    violations = check_guardrails(patch)
    assert ViolationType.OUTSIDE_BLAST_RADIUS in violations
