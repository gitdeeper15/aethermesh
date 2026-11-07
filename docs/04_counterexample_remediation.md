# AetherProof — Document 04: Counterexample-Guided Remediation

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **counterexample-guided remediation** protocol of AetherProof.

Its purpose is **not** to claim that automated remediation can replace human judgment, nor to assert that every counterexample is a real defect. Its purpose is to establish:

1. A **precise definition** of a counterexample and its types.
2. A **diagnosis protocol** that separates real defects from specification errors.
3. A **remediation cycle** with bounded iterations and explicit escalation.
4. **Guardrails** that prevent specification gaming (test weakening, invariant relaxation, etc.).
5. A **re-verification protocol** that requires both code and specification to be re-checked.
6. **Open mathematical questions** specific to counterexample analysis.

This document is scoped to remediation after a `Refuted` verdict. System integration with AetherGit and AetherFlow is addressed in Document 05.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture that hosts remediation.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR record structure — the source of specifications that may be revised.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  A requirement-driven proof trace — showing how remediation propagates.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Two-axis classification — determines whether a refutation is sound and complete.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifest structure — records the evidence behind a refutation.

---

## 3. Definition of a Counterexample

### 3.1 Formal Definition

A **counterexample** is a tuple:

```

C = (id, obligation, witness, refutation_evidence, type, provenance)

```

| Field | Type | Description |
|-------|------|-------------|
| `id` | Identifier | Unique, stable identifier for the counterexample |
| `obligation` | ObligationID | The obligation that was refuted |
| `witness` | Model \| Trace | The concrete witness that violates the property |
| `refutation_evidence` | ProofEvidence | The evidence that the witness is valid |
| `type` | CounterexampleType | Classification (see §3.2) |
| `provenance` | Provenance | Tool, timestamp, worker |

### 3.2 Counterexample Types

| Type | Description | Remediation Direction |
|------|-------------|----------------------|
| **Code defect** | The implementation violates the specification | Patch the code |
| **Specification error** | The specification is too strong or wrong | Revise the specification |
| **Assumption violation** | A stated assumption is false in the actual environment | Revise the assumption or the environment |
| **Model error** | The proof model is inaccurate | Improve the model |
| **Flaky refutation** | The refutation is not reproducible (flaky test or tool bug) | Re-run or mitigate flakiness |
| **Unknown** | The type cannot be determined from available evidence | Escalate to human |

**Key principle**: The counterexample type is **not** determined by the tool that produced it. It is determined by the **diagnosis protocol** (§5).

---

## 4. The Remediation Cycle

### 4.1 Cycle Stages

```

┌──────────────────┐
│ 1. Counterexample│
│    Detected      │
└────────┬─────────┘
│
▼
┌──────────────────┐
│ 2. Diagnosis     │
│    (classify)    │
└────────┬─────────┘
│
▼
┌──────────────────┐
│ 3. Hypothesis    │
│    (what to fix) │
└────────┬─────────┘
│
▼
┌──────────────────┐
│ 4. Patch Proposal│
│    (code or spec)│
└────────┬─────────┘
│
▼
┌──────────────────┐
│ 5. Re-verify     │
│    (code AND spec)│
└────────┬─────────┘
│
▼
┌──────────────────┐
│ 6. Accept / Reject│
│    (bounded)     │
└──────────────────┘

```

### 4.2 Bounded Iterations

The cycle is **bounded** by a configurable maximum number of iterations (default: 3). If no resolution is found within the bound:

1. The counterexample is marked `Escalated to Human`.
2. The full history of attempts is recorded.
3. No silent acceptance of the counterexample is allowed.

### 4.3 No Silent Specification Modification

**Rule**: A remediation patch that modifies a specification must be **explicitly tagged** as a specification change, and must pass through the same review process as any other specification change (Document 01, §7).

**Rule**: A remediation patch that modifies both code and specification must be **rejected** unless the reviewer explicitly approves the specification change.

---

## 5. Diagnosis Protocol

### 5.1 Diagnosis Decision Tree

```

Given counterexample C:
if C.witness is not reproducible:
return "Flaky refutation"
if C.refutes a stated assumption:
return "Assumption violation"
if C.witness is a valid model of the actual implementation:
if C.refutes the specification:
return "Specification error"
else:
return "Code defect"
else:
return "Model error"

```

### 5.2 Reproducibility Check

A counterexample is **reproducible** if re-running the same discharge path on the same input yields the same witness. Flaky refutations are excluded from remediation and handled separately (Document 05, §X).

### 5.3 Assumption Check

An assumption violation is detected when the counterexample's witness falsifies a stated assumption in the obligation's `assumptions` set. This is a **diagnosis**, not a defect.

### 5.4 Model Validation

A model error occurs when the counterexample's witness cannot be realized in the actual implementation. This indicates that the proof model over-approximates the implementation (an `Over-approximation` in the sense of Document 01, §6.1).

---

## 6. Patch Proposal

### 6.1 Code Patch Proposal

For a **code defect**, the remediation engine proposes a patch that:

1. Modifies the code to satisfy the specification.
2. Does not weaken the specification.
3. Does not modify tests, test infrastructure, or assertions.
4. Stays within the `blast_radius` of the obligation.

### 6.2 Specification Patch Proposal

For a **specification error**, the remediation engine proposes a patch that:

1. Revises the specification to reflect the actual intent (with justification).
2. Is tagged as a specification change.
3. Is submitted for human review before acceptance.

### 6.3 Assumption Patch Proposal

For an **assumption violation**, the remediation engine proposes one of:

1. Revise the assumption to reflect the actual environment.
2. Revise the implementation to satisfy the original assumption.
3. Mark the obligation as `Escalated` (if neither is acceptable).

### 6.4 Guardrails

Every patch proposal passes through the guardrails:

| Guardrail | Rejection Condition |
|-----------|---------------------|
| **Test integrity** | Patch deletes, disables, or modifies a failing test |
| **Assertion integrity** | Patch widens an assertion's tolerance |
| **Infrastructure integrity** | Patch modifies test infrastructure |
| **Blast radius** | Patch modifies files outside the declared blast radius |
| **Specification integrity** | Patch weakens the specification without explicit approval |

A patch that fails any guardrail is **rejected** and the cycle returns to diagnosis with a new hypothesis.

---

## 7. Re-Verification Protocol

### 7.1 Re-Verification Requirements

Every accepted patch triggers:

1. **Code re-verification**: The original obligation is re-discharged against the patched code.
2. **Specification re-verification**: If the patch modified the specification, the specification is re-validated against its source CSR record.
3. **Assumption re-verification**: If the patch modified assumptions, all dependent obligations are re-checked.

### 7.2 Re-Verification Cycle

```

For each affected obligation O:
if patch modifies O.source_csr:
re_discharge(O) with new CSR
else:
re_discharge(O) with patched code

if re_discharge(O).verdict == Refuted:
return to Remediation Cycle

```

### 7.3 Termination Conditions

The cycle terminates when:

1. All affected obligations are `Proven`.
2. The iteration bound is reached (escalate to human).
3. A guardrail violation is detected (reject the patch).

---

## 8. Escalation to Human

### 8.1 Escalation Triggers

| Trigger | Reason |
|---------|--------|
| Iteration bound reached | The engine cannot resolve the counterexample |
| Guardrail violation detected | The patch would compromise verification integrity |
| Specification change proposed | Specification changes require human approval |
| Conflicting evidence | Multiple counterexamples contradict each other |
| Unknown counterexample type | The diagnosis is inconclusive |

### 8.2 Escalation Record

Every escalation produces an **Escalation Record** with:

| Field | Content |
|-------|---------|
| `counterexample_id` | The counterexample that triggered escalation |
| `diagnosis_history` | All diagnosis attempts |
| `patch_attempts` | All patch proposals (accepted and rejected) |
| `reason` | Why escalation is required |
| `timestamp` | When escalation occurred |
| `human_decision` | To be filled by human reviewer |

### 8.3 Human Decision Options

The human reviewer can:

1. **Accept** the counterexample as a real defect and propose a fix.
2. **Reject** the counterexample as spurious (with justification).
3. **Revise** the specification (with new traceability).
4. **Defer** the counterexample to future work (with justification).

---

## 9. Integration with AetherFlow

### 9.1 Remediation as Changeset

Every remediation patch is a **changeset** submitted to AetherFlow's admission protocol. It is verified and remediated by the same mechanisms as any other changeset.

### 9.2 Guardrails Shared

The guardrails in this document (§6.4) are a **superset** of AetherFlow's guardrails (Document 04, §4.4 in the AetherFlow manuscript). AetherProof adds:

- Specification integrity checks.
- Assumption change tracking.
- Counterexample-specific validation.

### 9.3 Feedback Loop

AetherProof feeds **counterexample classes** back to AetherFlow to improve:

- Attribution precision (which changesets are likely culprits).
- Verification prioritization (which changesets need deeper analysis).
- Remediation strategy (which tier is likely to succeed).

---

## 10. Open Mathematical Questions

| ID | Question | Status |
|----|----------|--------|
| Q19 | What is the minimal diagnosis protocol that distinguishes code defects from specification errors? | Open |
| Q20 | When is a counterexample "reproducible enough" to be actionable? | Open |
| Q21 | How should conflicting counterexamples be resolved? | Open |
| Q22 | What is the maximum iteration bound that preserves soundness? | Open |
| Q23 | How should guardrails be formalized to prevent specification gaming? | Open |
| Q24 | Can the remediation cycle be made confluent (order-independent)? | Open |

---

## 11. Design Decisions and Deferred Commitments

### 11.1 Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D22 | Counterexample type is diagnosed, not assumed | Prevents misclassification |
| D23 | Remediation cycle is bounded | Prevents infinite loops |
| D24 | Specification changes are explicitly tagged | Prevents silent modification |
| D25 | Guardrails are mandatory | Prevents test weakening |
| D26 | Re-verification requires code AND spec | Prevents incomplete fixes |
| D27 | Escalation is a valid outcome | Preserves human judgment |
| D28 | Remediation is a changeset | Integrates with AetherFlow |

### 11.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD19 | Full counterexample schema (JSON/YAML) | Document 05 |
| DD20 | Remediation patch format | Document 05 |
| DD21 | Integration protocol with AetherFlow | Document 05 |
| DD22 | Human review as discharge evidence | Document 06 |
| DD23 | Axiomatic specification approval process | Document 06 |

---

## 12. Summary

This document establishes:

1. A **precise definition** of a counterexample with six types.
2. A **diagnosis protocol** that separates real defects from specification errors.
3. A **bounded remediation cycle** with explicit escalation.
4. **Guardrails** that prevent specification gaming.
5. A **re-verification protocol** requiring both code and specification to be re-checked.
6. **Integration** with AetherFlow for remediation as changeset.
7. **Open mathematical questions** specific to counterexample analysis.

The governing question of this document is:

> **Given a counterexample C and a remediation engine, how can the engine determine whether C indicates a code defect, a specification error, or an assumption violation, and how can it propose and validate a remediation without compromising verification integrity?**

This question is **partially answered** by the structures defined here. Full answer requires Documents 05–06.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **Counterexample** | A witness that refutes a property |
| **Diagnosis** | The process of classifying a counterexample |
| **Remediation** | The process of proposing and validating a patch |
| **Guardrail** | A rule that prevents a patch from compromising verification |
| **Escalation** | The act of referring a case to human review |

---

## Appendix B — References

- Document 01: Specification Language (AetherProof, 2026).
- Document 02: Proof Obligations (AetherProof, 2026).
- Document 03: Incremental Proof Engine (AetherProof, 2026).
- Le Goues, C., et al. (2012). GenProg: A Generic Method for Automatic Software Repair. *IEEE TSE*.
- Jimenez, C. E., et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR 2024*.

---

**End of Document 04 (v1.0.0-draft).**
