# AetherProof — Document 06: Human Review Protocol

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **human review protocol** of AetherProof.

Its purpose is **not** to automate human judgment, nor to reduce human review to a rubber-stamp. Its purpose is to establish:

1. A **precise definition** of the review roles and their authorities.
2. **Escalation triggers** that determine when human review is required.
3. **Review workflows** for each class of decision (specification change, remediation acceptance, assumption revision).
4. **Evidence requirements** that a human reviewer must consider.
5. **Decision recording** that preserves accountability.
6. **Open questions** specific to human-in-the-loop verification.

This document is scoped to human review. Automated remediation is in Document 04. Integration with AetherFlow is in Document 05.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture — human review sits at the top of the trust hierarchy.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR records are the primary objects of human review.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  Review decisions propagate along semantic relations.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Translation classifications determine review depth.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifests inform the reviewer about trust boundaries.

---

## 3. Review Roles

### 3.1 Role Definitions

| Role | Authority | Responsibility |
|------|-----------|----------------|
| **Specification Author** | Write, revise specifications | Ensure specifications reflect intent |
| **Verification Engineer** | Discharge obligations, propose patches | Ensure proofs are sound |
| **Reviewer** | Approve specification changes, accept remediations | Ensure decisions are justified |
| **Maintainer** | Merge approved changes | Ensure the repository remains coherent |
| **Auditor** | Inspect decisions, question evidence | Ensure accountability |

### 3.2 Authority Matrix

| Decision | Author | Verif. Eng. | Reviewer | Maintainer | Auditor |
|----------|--------|-------------|----------|------------|---------|
| Write spec | ✅ | ❌ | ❌ | ❌ | ❌ |
| Revise spec (minor) | ✅ | ❌ | ✅ | ❌ | ❌ |
| Revise spec (major) | ✅ | ❌ | ✅✅ | ✅ | ❌ |
| Discharge obligation | ❌ | ✅ | ❌ | ❌ | ❌ |
| Accept remediation (code) | ❌ | ✅ | ✅ | ❌ | ❌ |
| Accept remediation (spec) | ❌ | ❌ | ✅✅ | ✅ | ❌ |
| Escalate to human | ❌ | ✅ | ✅ | ❌ | ✅ |
| Merge changes | ❌ | ❌ | ❌ | ✅ | ❌ |
| Question evidence | ❌ | ❌ | ❌ | ❌ | ✅ |

**Legend**: ✅ = authority; ✅✅ = requires escalation; ❌ = no authority.

### 3.3 Separation of Duties

**Rule**: No single person may hold both **Specification Author** and **Reviewer** roles for the same specification.

**Rule**: No single person may **discharge an obligation** and **approve its own evidence**.

**Rule**: The **Maintainer** must be distinct from the **Verification Engineer** who produced the patch.

**Rationale**: Separation of duties prevents self-approval, which would undermine the integrity of the verification chain.

---

## 4. Escalation Triggers

### 4.1 Automatic Escalation

The following triggers **automatically** escalate to human review:

| Trigger | Reason | Reviewer Role |
|---------|--------|---------------|
| **Specification change** | Any change to a CSR record | Specification Author + Reviewer |
| **Assumption change** | Any modification to an assumption | Reviewer |
| **Counterexample unresolved** | Iteration bound reached (Document 04, §4.2) | Reviewer |
| **Guardrail violation** | Patch would weaken verification (Document 04, §6.4) | Reviewer + Maintainer |
| **Conflicting evidence** | Two pieces of evidence disagree | Reviewer + Auditor |
| **Unknown counterexample type** | Diagnosis inconclusive | Reviewer |
| **Axiomatic specification** | Specification marked as axiomatic | Reviewer + Auditor |
| **Trust boundary change** | A new tool is introduced into a verification path | Reviewer + Auditor |

### 4.2 Voluntary Escalation

Any role may escalate a case to human review if they believe it requires judgment beyond the automated system.

**Rule**: Voluntary escalation must be **recorded** with a reason and a timestamp.

### 4.3 Non-Escalation

The following **do not** require human review:

| Case | Why Not |
|------|---------|
| Routine obligation discharge | Automated proof is sufficient |
| Minor code patch with passing guardrails | Automated verification is sufficient |
| Evidence query | Read-only |
| Health check | Infrastructure concern |

---

## 5. Review Workflows

### 5.1 Specification Change Review

```

Author proposes specification change
↓
Reviewer receives proposal + evidence (CSR record, affected obligations, proofs)
↓
Reviewer examines:
• Is the change traceable to a requirement?
• Does the change preserve semantic consistency (Document 01, §6.3)?
• Are the assumptions explicit?
• Are the affected obligations re-discharged?
↓
Reviewer decides:
• Approve → Merge (Maintainer)
• Reject → Return to Author
• Request more evidence → Return to Verif. Eng.

```

### 5.2 Remediation Acceptance Review

```

Verif. Eng. proposes patch
↓
Reviewer receives patch + counterexample + evidence
↓
Reviewer examines:
• Does the patch address the diagnosed counterexample type?
• Do the guardrails pass (Document 04, §6.4)?
• Is the patch within the blast radius?
• Does the patch weaken any specification?
↓
Reviewer decides:
• Approve → Changeset Emitter → AetherFlow
• Reject → Return to Verif. Eng.
• Escalate → Human review (Document 04, §8)

```

### 5.3 Assumption Revision Review

```

Author proposes assumption revision
↓
Reviewer receives proposal + list of dependent obligations
↓
Reviewer examines:
• Is the new assumption justified (empirical, derived, or axiomatic)?
• Are all dependent obligations re-discharged?
• Does the revision change the trust boundary?
↓
Reviewer decides:
• Approve → All dependent obligations re-discharged
• Reject → Return to Author
• Escalate → Trust boundary review

```

### 5.4 Escalation Review (from Document 04, §8)

```

System escalates case
↓
Reviewer receives escalation record (counterexample, attempts, reason)
↓
Reviewer decides one of:
• Accept counterexample → Propose fix
• Reject counterexample → Justify
• Revise specification → Specification Change Review
• Defer → Record as future work
↓
Reviewer records decision with rationale

```

---

## 6. Evidence Requirements

### 6.1 Required Evidence for Specification Change

| Evidence | Source | Purpose |
|----------|--------|---------|
| **CSR record (old and new)** | CSR Store | Compare |
| **Affected obligations** | PDG | Assess impact |
| **Re-discharged obligations** | Proof Engine | Verify soundness |
| **Traceability chain** | CSR Store | Confirm requirement link |
| **Assumption list** | CSR Store | Confirm assumption closure |

### 6.2 Required Evidence for Remediation Acceptance

| Evidence | Source | Purpose |
|----------|--------|---------|
| **Counterexample record** | Counterexample Analyzer | Understand the defect |
| **Diagnosis** | Diagnosis Protocol | Confirm counterexample type |
| **Patch diff** | Remediation Engine | Review the change |
| **Guardrail results** | Guardrails | Confirm no weakening |
| **Re-verification evidence** | Proof Engine | Confirm soundness |

### 6.3 Evidence Sufficiency

**Rule**: A reviewer may **not approve** a decision without the required evidence.

**Rule**: A reviewer **may reject** a decision on evidence insufficiency alone.

**Rule**: A reviewer **must record** why evidence is insufficient.

---

## 7. Decision Recording

### 7.1 Decision Record

Every human review decision produces a **Decision Record**:

```json
{
    "decision_id": "DR-2026-11-06-001",
    "reviewer": "reviewer-id",
    "decision_type": "specification_change | remediation | assumption_revision | escalation",
    "subject": "csr-L1-001",
    "decision": "approved | rejected | escalated",
    "rationale": "The specification change is traceable to requirement R1, and all affected obligations are re-discharged.",
    "evidence_reviewed": ["csr-L1-001-v1", "csr-L1-001-v2", "O-001", "O-002"],
    "timestamp": "2026-11-06T15:00:00Z",
    "signature": "..."
}
```

7.2 Decision Log

Decision Records are append-only and signed.

Rule: The Decision Log is checked into the repository alongside the CSR Store.

Rule: Any modification to a Decision Record must be appended as a new record (never overwritten).

7.3 Auditability

Every decision is auditable by:

1. The Auditor role (Document 06, §3).
2. The AetherFlow audit log (Document 05, §7.3).
3. The public (if the repository is public).

---

8. Human Review as Discharge Evidence

8.1 Human Review as Evidence

In some cases (Document 02, §7.1), human review can discharge an obligation. This is only allowed when:

1. The obligation cannot be discharged by any automated path.
2. The human reviewer has the Reviewer role.
3. The human reviewer explicitly signs the discharge.

8.2 Evidence Format

Human review evidence is recorded as:

```json
{
    "evidence_type": "human_justification",
    "reviewer": "reviewer-id",
    "justification": "...",
    "references": ["csr-L1-001", "O-001"],
    "timestamp": "2026-11-06T15:00:00Z",
    "signature": "..."
}
```

8.3 Limitations

Rule: Human review evidence does not prove a property. It accepts a property as proven under human judgment.

Rule: Human review evidence is not portable across systems (unlike Lean proof terms).

Rule: Human review evidence must be re-validated if the specification changes.

---

9. Trust Hierarchy

9.1 Trust Levels

Level Trust Examples
Tool-verified High Lean kernel, Z3 unsat + proof artifact
Human-reviewed Medium-High Reviewer-approved specification change
Human-justified Medium Human review as discharge evidence
Empirical Medium Measurements, experiments
Axiomatic Variable Depends on justification
Unknown Low Unresolved obligations

9.2 Trust Propagation

Trust does not automatically propagate:

· A tool-verified proof is not automatically trusted if its TCB Manifest is incomplete.
· A human-reviewed change is not automatically trusted if the reviewer has a conflict of interest.
· An axiomatic assumption is not automatically trusted if it is unjustified.

Trust is explicit, not implicit.

---

10. Open Questions

ID Question Status
Q37 What is the minimal set of roles that preserves separation of duties? Open
Q38 How should reviewer conflicts of interest be detected and handled? Open
Q39 What is the cognitive burden of reviewing a specification change at scale? Open
Q40 Can human review be made auditable without slowing down the process? Open
Q41 How should human review evidence be re-validated after a specification change? Open
Q42 Can human review be partially automated (e.g., by ML-assisted triage)? Open

---

11. Design Decisions and Deferred Commitments

11.1 Decisions Made

ID Decision Rationale
D42 Five roles defined, separation of duties enforced Prevents self-approval
D43 Automatic escalation for specification changes Preserves intent
D44 Required evidence per review type Prevents blind approval
D45 Decision Records are append-only and signed Auditable
D46 Human review as discharge evidence Fallback for undecidable obligations
D47 Trust is explicit, not implicit Prevents trust erosion

11.2 Decisions Deferred

ID Deferred Question Deferred To
DD34 Reviewer identity system (SSO, keys) Future work
DD35 Conflict-of-interest detection algorithm Future work
DD36 Cognitive load studies Future work
DD37 ML-assisted triage Future work
DD38 Multi-team review workflows Future work

---

12. Summary

This document establishes:

1. Five roles (Author, Verif. Eng., Reviewer, Maintainer, Auditor) with a strict separation of duties.
2. Escalation triggers (automatic and voluntary) that determine when human review is required.
3. Review workflows for each class of decision.
4. Evidence requirements per review type.
5. Decision recording that preserves accountability.
6. Human review as discharge evidence with explicit limitations.
7. A trust hierarchy that distinguishes tool-verified, human-reviewed, and human-justified trust.

The governing question of this document is:

What is the minimal human review protocol that preserves judgment, accountability, and separation of duties without reducing human review to a rubber-stamp, and how can human review be recorded as verifiable evidence?

This question is partially answered by the structures defined here. Full answer requires future empirical work.

---

Appendix A — Glossary

Term Definition
Role A set of authorities and responsibilities
Separation of duties A principle that no single person holds conflicting roles
Escalation The act of referring a case to human review
Decision Record A signed, append-only record of a review decision
Human review evidence Evidence produced by a human reviewer
Trust hierarchy The classification of evidence by trust level

---

Appendix B — References

· Document 01: Specification Language (AetherProof, 2026).
· Document 02: Proof Obligations (AetherProof, 2026).
· Document 03: Incremental Proof Engine (AetherProof, 2026).
· Document 04: Counterexample Remediation (AetherProof, 2026).
· Document 05: Integration Protocol (AetherProof, 2026).

---

End of Document 06 (v1.0.0-draft).
