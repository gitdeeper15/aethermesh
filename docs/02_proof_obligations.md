# AetherProof — Document 02: Proof Obligations

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines how **proof obligations** are generated, tracked, and discharged in AetherProof.

Its purpose is **not** to prescribe a specific theorem prover, nor to claim that all properties are provable. Its purpose is to establish:

1. A **precise definition** of a proof obligation.
2. A **generation procedure** from CSR records (Document 01).
3. A **dependency structure** that supports incremental invalidation.
4. An **assumption tracking model** that prevents silent assumption changes.
5. A **discharge protocol** with per-path TCB Manifests.
6. **Open mathematical questions** specific to obligation generation.

This document is scoped to obligation generation and tracking. Differential proving is addressed in Document 03. Counterexample remediation is addressed in Document 04.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture that hosts proof obligations (from Document 01).

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR record structure — the source of proof obligations.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  A requirement-driven proof trace — showing how obligations are derived.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Two-axis classification — determines which obligations are checkable.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifest structure — records how obligations are discharged.

---

## 3. Definition of a Proof Obligation

### 3.1 Formal Definition

A **proof obligation** is a tuple:

```

O = (id, property, assumptions, source_csr, discharged_by, verdict)

```

Where:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Identifier | Unique, stable identifier for the obligation |
| `property` | Formula | The property to be proven |
| `assumptions` | Set<AssumptionID> | The assumptions under which the property must hold |
| `source_csr` | CSR-ID | The CSR record that generated this obligation |
| `discharged_by` | ProofEvidence \| ⊥ | The evidence that discharges the obligation (if any) |
| `verdict` | Verdict | `Proven` / `Refuted` / `Unknown` / `Escalated` |

### 3.2 Properties of a Proof Obligation

- **Typed**: Every obligation has a formula from a specified logic.
- **Assumption-closed**: Every obligation depends only on assumptions declared in its `assumptions` set.
- **Traceable**: Every obligation traces to a CSR record, which traces to a requirement.
- **Dischargeable**: Every obligation can be discharged by proof evidence, or left `Unknown`.

### 3.3 The Obligation is Not the Proof

An obligation is a **question**, not an answer. It becomes an answer only when discharged by evidence.

---

## 4. Generation Procedure

### 4.1 Generation from CSR Records

For each CSR record of the form:

```

csr: (layer, language, content, semantic_role, assumptions)

```

The generator produces obligations according to the following rules:

| CSR `semantic_role` | Generated Obligations |
|---------------------|----------------------|
| `invariant` (L1) | `Invariance(property, transitions, assumptions)` |
| `contract` (L2) | `PrePost(pre, post, function, assumptions)` |
| `constraint` (L3) | `Satisfiability(constraint, assumptions)` |
| `translation` | `Consistency(source, target, property, assumptions)` |

### 4.2 Generation Rules

1. **No obligation without a source**: Every obligation must trace to exactly one CSR record.
2. **No obligation without assumptions**: An obligation may declare `assumptions = ∅` only if it is tagged `axiomatic` (deferred to Document 06).
3. **No obligation without a property**: An obligation without a property is invalid.
4. **No hidden obligations**: Every generated obligation must be recorded in the CSR record's `relations` set.

### 4.3 Example: Invariance Obligation from L1 Invariant

Given a Layer 1 CSR record:

```

csr_id:      csr-L1-001
layer:       L1
language:    TLA+
semantic_role: invariant
content:     "Always (queue_length ≤ MAX)"
assumptions: {A1: MAX > 0}

```

The generator produces:

```

O-001:
property:     ∀s ∈ Reachable : queue_length(s) ≤ MAX
assumptions:  {A1}
source_csr:   csr-L1-001
discharged_by: ⊥
verdict:      Unknown

```

The obligation is then dispatched to the TLA+ model checker (TLC) or prover (TLAPS).

---

## 5. Dependency Structure

### 5.1 Obligation Dependency Graph (ODG)

Obligations are organized in a **directed acyclic graph**:

```

ODG = (Obligations, Edges)

```

Where an edge `(O₁, O₂)` means: **O₂ depends on O₁'s verdict being `Proven`.**

### 5.2 Edge Types

| Edge Type | Meaning |
|-----------|---------|
| `requires` | O₂ requires O₁ to be `Proven` before it can be discharged |
| `refines` | O₂ is a refinement of O₁ |
| `assumes` | O₂ assumes O₁ as a hypothesis |
| `contradicts` | O₂ contradicts O₁ (both cannot be `Proven`) |

### 5.3 Invariant: No Cyclic Dependencies

The ODG must be a DAG. Cycles indicate a design error in the CSR records and must be resolved before obligation generation.

### 5.4 Incremental Invalidation

When an obligation's verdict changes from `Proven` to `Unknown` (for example, because a source CSR record changed), all obligations that transitively depend on it must be invalidated.

**Invalidation rule**: If `verdict(O₁) ≠ Proven` and there exists an edge `(O₁ → O₂)`, then `verdict(O₂) := Unknown`.

---

## 6. Assumption Tracking

### 6.1 Definition of an Assumption

An **assumption** is a named proposition that an obligation depends on, but does not itself prove.

```

A = (id, statement, source, verified_by)

```

| Field | Type | Description |
|-------|------|-------------|
| `id` | AssumptionID | Unique identifier |
| `statement` | Formula | The proposition assumed to hold |
| `source` | CSR-ID \| AxiomID \| RequirementID | Where the assumption comes from |
| `verified_by` | ProofEvidence \| ⊥ | How the assumption is verified (if at all) |

### 6.2 Assumption Classes

| Class | Description |
|-------|-------------|
| **Axiomatic** | Taken as given, no proof required |
| **Empirical** | Verified by experiment or measurement |
| **Derived** | Proven from other assumptions or obligations |
| **Environment** | Assumed about the environment (e.g., "the clock is monotonic") |

### 6.3 Assumption Change Management

**Rule**: Changing an assumption's statement requires invalidating every obligation that depends on it.

**Rule**: Adding an assumption to an obligation requires recording the addition in the CSR record's `assumptions` set.

**Rule**: Removing an assumption from an obligation is allowed only if no obligation depends on it.

### 6.4 Silent Assumption Prevention

An obligation must declare its assumptions explicitly. The system must:

1. Reject any proof evidence whose TCB Manifest does not declare the same assumptions as the obligation.
2. Log every assumption change with a timestamp and a diff.
3. Prevent assumption changes from being committed without explicit human or tool approval.

---

## 7. Discharge Protocol

### 7.1 Discharge Paths

An obligation can be discharged by any of the following paths:

| Path | Tool | Produces |
|------|------|----------|
| `TLA+ model checking` | TLC | Bounded exploration (may be `Unknown` beyond bound) |
| `TLA+ proof` | TLAPS | Proof term (checkable by TLA+ kernel) |
| `Why3 verification` | Why3 + backend provers | Proof obligations discharged by provers |
| `Lean proof` | Lean | Proof term (checkable by Lean kernel) |
| `SMT solving` | Z3 + proof checker | `unsat` + proof artifact (if produced) |
| `Human review` | Human | `Escalated` with human-written justification |

### 7.2 Discharge Requirements

Every discharge must satisfy:

1. **Assumption match**: The TCB Manifest's assumptions must be a subset of the obligation's assumptions.
2. **TCB completeness**: The TCB Manifest must record all components used to discharge the obligation.
3. **Evidence artifact**: The discharge must produce an artifact (proof term, model, or human justification) that is stored as proof evidence.
4. **Independent checkability**: The evidence must be independently checkable by a component **not** used to produce it (when possible).

### 7.3 Failure to Discharge

If no path discharges the obligation:

1. The verdict remains `Unknown`.
2. The workflow disposition becomes `Further Analysis` or `Escalated to Human`.
3. The obligation is recorded in the failure log with its attempt history.

---

## 8. Verdict and Workflow Disposition

### 8.1 Two Orthogonal Axes

| Axis | Values |
|------|--------|
| **Verification Verdict** | `Proven` / `Refuted` / `Unknown` |
| **Workflow Disposition** | `Completed` / `Remediation Required` / `Further Analysis` / `Escalated to Human` |

### 8.2 Mapping (Non-Automatic)

| Verdict | Typical Disposition |
|---------|---------------------|
| `Proven` | `Completed` |
| `Refuted` | `Remediation Required` |
| `Unknown` | `Further Analysis` or `Escalated to Human` |
| Any | `Escalated to Human` (if authority policy requires) |

**Clarification**: The mapping is not automatic. A `Refuted` verdict may be `Escalated to Human` instead of `Remediation Required` if the refuting counterexample is disputed.

---

## 9. Open Mathematical Questions

| ID | Question | Status |
|----|----------|--------|
| Q8 | What is the minimal obligation structure that preserves traceability? | Open |
| Q9 | Under what conditions can an obligation be safely re-discharged after an assumption change? | Open |
| Q10 | How should the ODG be structured to support efficient incremental invalidation? | Open |
| Q11 | When is a bounded model checking result `Unknown` acceptable as a discharge? | Open |
| Q12 | How should human review be encoded as discharge evidence? | Open |

These questions are **open** and shape the research frontier of this document.

---

## 10. Design Decisions and Deferred Commitments

### 10.1 Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D9 | Obligations are tuples with explicit assumptions | Assumption tracking is mandatory |
| D10 | ODG is a DAG | Cyclic dependencies indicate design errors |
| D11 | Assumption changes invalidate dependent obligations | Prevents silent assumption change |
| D12 | Discharge requires TCB Manifest | TCB is explicit, not implicit |
| D13 | Verdict and disposition are orthogonal | Logical truth ≠ workflow state |
| D14 | Failure to discharge is recorded, not hidden | Unknown is a valid verdict |

### 10.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD7 | Full obligation schema (JSON/YAML) | Document 03 |
| DD8 | Differential proving algorithm | Document 03 |
| DD9 | Counterexample representation | Document 04 |
| DD10 | Remediation protocol | Document 04 |
| DD11 | Axiomatic obligation approval process | Document 06 |
| DD12 | Human review as discharge evidence | Document 06 |

---

## 11. Summary

This document establishes:

1. A **precise definition** of a proof obligation as a tuple with explicit assumptions.
2. A **generation procedure** from CSR records (Document 01).
3. A **dependency graph** (ODG) that supports incremental invalidation.
4. An **assumption tracking model** that prevents silent assumption changes.
5. A **discharge protocol** with per-path TCB Manifests.
6. A **separation** of verification verdict from workflow disposition.
7. **Open mathematical questions** specific to obligation generation.

The governing question of this document is:

> **Given a set of CSR records, how are proof obligations generated, tracked, and discharged such that every obligation remains traceable to a requirement, every assumption is explicit, and every discharge is independently checkable?**

This question is **partially answered** by the structures defined here. Full answer requires Documents 03–06.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **Obligation** | A tuple (id, property, assumptions, source, evidence, verdict) |
| **ODG** | Obligation Dependency Graph |
| **Discharge** | The act of producing evidence that satisfies an obligation |
| **TCB Manifest** | Explicit record of TCB components for a discharge |
| **Verdict** | `Proven` / `Refuted` / `Unknown` |
| **Disposition** | Workflow state: `Completed` / `Remediation Required` / `Further Analysis` / `Escalated to Human` |

---

## Appendix B — References

- Document 01: Specification Language (AetherProof, 2026).
- Lamport, L. (2002). *Specifying Systems*. Addison-Wesley.
- Filliâtre, J.-C., & Paskevich, A. (2013). Why3 — Where Programs Meet Provers. *ESOP 2013*.
- de Moura, L., & Ullrich, S. (2021). The Lean 4 Theorem Prover. *CADE-28*.

---

**End of Document 02 (v1.0.0-draft).**
