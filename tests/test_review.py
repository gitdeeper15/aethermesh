"""Tests for human review protocol."""

from aetherproof.review.roles import Role, Authority, AUTHORITY_MATRIX


def test_roles_count():
    assert len(Role) == 5


def test_authority_levels():
    assert Authority.YES.value == "yes"
    assert Authority.ESCALATE.value == "escalate"
    assert Authority.NO.value == "no"


def test_separation_of_duties():
    assert AUTHORITY_MATRIX[("write_spec", Role.SPECIFICATION_AUTHOR)] == Authority.YES
    assert AUTHORITY_MATRIX[("write_spec", Role.REVIEWER)] == Authority.NO
    assert AUTHORITY_MATRIX[("discharge_obligation", Role.VERIFICATION_ENGINEER)] == Authority.YES
    assert AUTHORITY_MATRIX[("discharge_obligation", Role.REVIEWER)] == Authority.NO


def test_maintainer_can_merge():
    assert AUTHORITY_MATRIX[("merge_changes", Role.MAINTAINER)] == Authority.YES
    assert AUTHORITY_MATRIX[("merge_changes", Role.REVIEWER)] == Authority.NO


def test_auditor_can_question_evidence():
    assert AUTHORITY_MATRIX[("question_evidence", Role.AUDITOR)] == Authority.YES
    assert AUTHORITY_MATRIX[("question_evidence", Role.REVIEWER)] == Authority.NO
