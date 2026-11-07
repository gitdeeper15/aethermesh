"""
Human Review Roles — Section 8.1 implementation.

Five roles with separation of duties.
"""

from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    """Five human review roles (Section 8.1)."""
    SPECIFICATION_AUTHOR = "specification_author"
    VERIFICATION_ENGINEER = "verification_engineer"
    REVIEWER = "reviewer"
    MAINTAINER = "maintainer"
    AUDITOR = "auditor"


class Authority(str, Enum):
    """Authority levels (Section 8.1)."""
    YES = "yes"
    ESCALATE = "escalate"
    NO = "no"


# Authority matrix (Section 8.1)
AUTHORITY_MATRIX: dict[tuple[str, Role], Authority] = {
    ("write_spec", Role.SPECIFICATION_AUTHOR): Authority.YES,
    ("write_spec", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("write_spec", Role.REVIEWER): Authority.NO,
    ("write_spec", Role.MAINTAINER): Authority.NO,
    ("write_spec", Role.AUDITOR): Authority.NO,

    ("revise_spec_minor", Role.SPECIFICATION_AUTHOR): Authority.YES,
    ("revise_spec_minor", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("revise_spec_minor", Role.REVIEWER): Authority.YES,
    ("revise_spec_minor", Role.MAINTAINER): Authority.NO,
    ("revise_spec_minor", Role.AUDITOR): Authority.NO,

    ("revise_spec_major", Role.SPECIFICATION_AUTHOR): Authority.YES,
    ("revise_spec_major", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("revise_spec_major", Role.REVIEWER): Authority.ESCALATE,
    ("revise_spec_major", Role.MAINTAINER): Authority.YES,
    ("revise_spec_major", Role.AUDITOR): Authority.NO,

    ("discharge_obligation", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("discharge_obligation", Role.VERIFICATION_ENGINEER): Authority.YES,
    ("discharge_obligation", Role.REVIEWER): Authority.NO,
    ("discharge_obligation", Role.MAINTAINER): Authority.NO,
    ("discharge_obligation", Role.AUDITOR): Authority.NO,

    ("accept_remediation_code", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("accept_remediation_code", Role.VERIFICATION_ENGINEER): Authority.YES,
    ("accept_remediation_code", Role.REVIEWER): Authority.YES,
    ("accept_remediation_code", Role.MAINTAINER): Authority.NO,
    ("accept_remediation_code", Role.AUDITOR): Authority.NO,

    ("accept_remediation_spec", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("accept_remediation_spec", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("accept_remediation_spec", Role.REVIEWER): Authority.ESCALATE,
    ("accept_remediation_spec", Role.MAINTAINER): Authority.YES,
    ("accept_remediation_spec", Role.AUDITOR): Authority.NO,

    ("escalate_to_human", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("escalate_to_human", Role.VERIFICATION_ENGINEER): Authority.YES,
    ("escalate_to_human", Role.REVIEWER): Authority.YES,
    ("escalate_to_human", Role.MAINTAINER): Authority.NO,
    ("escalate_to_human", Role.AUDITOR): Authority.YES,

    ("merge_changes", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("merge_changes", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("merge_changes", Role.REVIEWER): Authority.NO,
    ("merge_changes", Role.MAINTAINER): Authority.YES,
    ("merge_changes", Role.AUDITOR): Authority.NO,

    ("question_evidence", Role.SPECIFICATION_AUTHOR): Authority.NO,
    ("question_evidence", Role.VERIFICATION_ENGINEER): Authority.NO,
    ("question_evidence", Role.REVIEWER): Authority.NO,
    ("question_evidence", Role.MAINTAINER): Authority.NO,
    ("question_evidence", Role.AUDITOR): Authority.YES,
}


__all__ = ["Role", "Authority", "AUTHORITY_MATRIX"]
