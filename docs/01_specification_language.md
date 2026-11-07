# AetherProof — Document 01: Specification Language

**Version:** 1.0.1-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the specification language architecture of AetherProof.

Its purpose is **not** to select a single specification language, nor to claim that heterogeneous formal languages can be freely interchanged. Its purpose is to establish:

1. A **three-layer functional specification architecture** with distinct, non-substitutable roles.
2. A **Canonical Specification Representation (CSR)** that records semantic relations without asserting semantic truth.
3. **Explicit semantic relations** between specification elements, independent of layer ordering.
4. **Traceability** from requirements to specifications to proof obligations.
5. **Open mathematical questions** that define the research frontier of this project.

This document is scoped to the specification layer only. Proof obligations, differential proving, and counterexample remediation are addressed in subsequent documents.

---

## 2. Figures

The following figures illustrate the architecture defined in this document:

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer differential verification architecture of AetherProof (L1: TLA+, L2: Why3/Lean, L3: SMT-LIB/Z3). The layers are functional categories, not hierarchical levels.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  The CSR record structure with three distinct identities: Record Identity (`csr_id`), Artifact Identity (`artifact_hash`), and Semantic Identity (`semantic_id`), together with their relationships.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  A requirement-driven formal proof trace: a requirement refines to a Layer 1 invariant, which refines to Layer 2 contracts, which instantiate Layer 3 constraints.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  AetherProof formal property matrix: Axis A (Semantic Relationship) × Axis B (Verification Property), showing compatibility and incompatibility of translation classifications.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  The TCB Manifest structure for each verification path, recording tool versions, backend provers, transformations, axioms, proof artifact hashes, and known limitations.

---

## 3. Three-Layer Functional Architecture

### 3.1 Layer 1 — System-Level Properties

| Aspect | Value |
|--------|-------|
| **Language family** | TLA+ |
| **Functional scope** | System invariants, state transitions, concurrency, safety, liveness |
| **Verification mode** | Model checking (TLC), proof (TLAPS) |

### 3.2 Layer 2 — Functional Contracts

| Aspect | Value |
|--------|-------|
| **Language family** | Why3, Lean |
| **Functional scope** | Function contracts, pre/post-conditions, types, data invariants |
| **Verification mode** | Deductive verification (Why3), proof construction (Lean) |

### 3.3 Layer 3 — Logical Constraints

| Aspect | Value |
|--------|-------|
| **Language family** | SMT-LIB |
| **Functional scope** | Logical constraints, arithmetic, indices, models |
| **Verification mode** | SMT solving (e.g., Z3) |

### 3.4 Non-Substitutability Principle

The three layers are **not** interchangeable. The architecture assumes **coexistence with explicit semantic relations**, not **unification into one language**.

### 3.5 Layers Are Functional, Not Hierarchical

The three layers are **not** arranged in a fixed containment hierarchy. Relations between elements are defined by their **semantic content**, not by layer index.

---

## 4. Canonical Specification Representation (CSR)

### 4.1 Definition

The **CSR** is a typed, traceable, versioned, and semantically linked **record** of specification elements across all three layers.

### 4.2 Three Identities

| Identity | Type | Description |
|----------|------|-------------|
| **Record Identity** | `csr_id` | Stable identifier for the CSR record |
| **Artifact Identity** | `artifact_hash` | Content hash of the concrete artifact |
| **Semantic Identity** | `semantic_id` | Identifier for the meaning and assumptions |

### 4.3 The CSR is Not a Proof

The CSR does **not** assert truth. It records what specifications exist, what they mean structurally, and how they relate.

---

## 5. Semantic Relations Between Layers

### 5.1 Relation Types

| Relation | Meaning | Direction |
|----------|---------|-----------|
| `refines` | Source refines target | Source → Target |
| `instantiates` | Concrete instance of a generic specification | Instance → Generic |
| `approximates` | Source approximates target | Direction declared |
| `implies` | Logical consequence | Same layer |
| `contradicts` | Explicitly inconsistent | Symmetric |
| `depends_on` | Proof-level dependency | Dependent → Dependency |
| `supersedes` | Version replacement | New → Old |

### 5.2 Well-Formedness Rules

1. **No circular refinement**: `refines` must form a DAG.
2. **Explicit approximation**: Any `approximates` relation must include a documented `loss_description`.
3. **Contradiction recording**: A `contradicts` relation must be recorded as a **verification finding**.

---

## 6. Translation and Semantic Consistency

### 6.1 Two Orthogonal Axes

**Axis A — Semantic Relationship**: Exact / Over-approximation / Under-approximation / Partial mapping / Divergent

**Axis B — Verification Property**: Sound / Complete / Neither / Not established

### 6.2 Translation Records

Every translation is a CSR record with:
- `source`, `target`
- `semantic_relationship` (Axis A)
- `verification_property` (Axis B, relative to a named property)
- `justification`, `loss_description`, `assumptions`

### 6.3 Semantic Consistency — Provisional Definition

Two CSR records are **semantically consistent** with respect to a property P if there exists a translation between them classified as `Sound` (Axis B) with respect to P, and no `contradicts` relation has been recorded as a `VerificationFinding`.

**This definition is provisional.** A complete definition requires formalizing "the meaning" of a specification element and a decision procedure for checking agreement. This is **open question Q2**.

---

## 7. Requirements-to-Specification Traceability

### 7.1 Traceability Chain

```

Requirements
↓  (refines)
Specifications (CSR records)
↓  (yields)
Proof Obligations
↓  (checked by)
Proof Evidence

```

### 7.2 Traceability Requirements

1. **No orphan specifications**: Every CSR record must trace to a requirement or be marked `unformalized`.
2. **No orphan requirements**: Every requirement must be represented or marked `unformalized`.
3. **No silent modification**: Modifying a requirement must invalidate dependent CSR records and proof obligations.

---

## 8. Language and Tool Responsibilities

### 8.1 Per-Path TCB Manifest

Each verification path has its **own TCB Manifest**:

| Path | TCB Manifest Contents |
|------|----------------------|
| **TLA+ model checking** | TLC version, model configuration, state-space bound, exploration strategy |
| **TLA+ proof (TLAPS)** | TLAPS version, TLA+ kernel version, backend provers |
| **Why3 verification** | Why3 version, transformations, drivers, backend provers |
| **Lean proof** | Lean version, kernel version, imported libraries, axioms used |
| **Z3 `unsat`** | Z3 version, SMT-LIB version, proof production enabled, proof artifact hash |

**Key principle**: TCB Manifests are **explicit artifacts**, not implicit assumptions.

---

## 9. Open Mathematical Questions

| ID | Question | Status |
|----|----------|--------|
| Q1 | Under what conditions is a translation sound with respect to a property? | Open |
| Q2 | What is a mathematically precise definition of semantic consistency? | Open |
| Q3 | What is the minimal CSR structure that preserves semantic identity? | Open |
| Q4 | How should assumption dependency graphs be structured? | Open |
| Q5 | When is an approximation "good enough" for a requirement? | Open |
| Q6 | How should proof portability interact with tool diversity? | Open |
| Q7 | Can the three identities of a CSR record be reconciled mechanically? | Open |

---

## 10. Design Decisions and Deferred Commitments

### 10.1 Decisions Made

| ID | Decision |
|----|----------|
| D1 | Three functional layers (not hierarchical) |
| D2 | CSR as semantic index |
| D3 | Two-axis translation classification |
| D4 | Traceability chain from requirements to proof |
| D5 | Separate verification verdict from workflow disposition |
| D6 | Per-path TCB Manifest |
| D7 | Three CSR identities |
| D8 | Contradiction is a finding, not an escalation |

### 10.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD1 | Full CSR schema | Document 02 |
| DD2 | Proof obligation generation algorithm | Document 02 |
| DD3 | Differential proof engine | Document 03 |
| DD4 | Counterexample remediation protocol | Document 04 |
| DD5 | Integration protocol with AetherFlow | Document 05 |
| DD6 | Axiomatic CSR record approval process | Document 06 |

---

## 11. Summary

This document establishes:

1. A **three-layer functional specification architecture** (L1: TLA+, L2: Why3/Lean, L3: SMT-LIB), explicitly **not hierarchical**.
2. A **Canonical Specification Representation (CSR)** as a semantic index with **three distinct identities**.
3. **Explicit semantic relations** between layers, with **two-axis translation classification**.
4. **Traceability** from requirements to specifications to obligations.
5. **Per-path TCB Manifests** as mandatory evidence.
6. **Open mathematical questions** that define the research frontier.

The governing question of this document is:

> **How can heterogeneous specification languages express different levels of system behavior while preserving semantic consistency, traceability, and verifiable relationships across their respective proof obligations?**

**Central commitment**: The hard problem of AetherProof is **not** making TLA+, Why3, Lean, and SMT-LIB exchange data. It is **proving that what these languages mean remains consistent when a specification moves from one representation to another.** The CSR is a record of relations; it is not a proof that those relations hold.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **CSR** | Canonical Specification Representation |
| **TCB** | Trusted Computing Base |
| **TCB Manifest** | Explicit record of TCB components, versions, and assumptions |
| **TLA+** | Temporal Logic of Actions |
| **TLAPS** | TLA+ Proof System |
| **TLC** | TLA+ Model Checker |
| **Why3** | Deductive verification platform |
| **Lean** | Proof assistant |
| **SMT-LIB** | Standard for SMT problem representation |
| **Z3** | SMT solver |

---

## Appendix B — References

- Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley.
- Filliâtre, J.-C., & Paskevich, A. (2013). Why3 — Where Programs Meet Provers. *ESOP 2013*.
- de Moura, L., & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. *CADE-28*.
- de Moura, L., & Bjørner, N. (2008). Z3: An Efficient SMT Solver. *TACAS 2008*.
- Barrett, C., et al. (2010). The SMT-LIB Standard: Version 2.0.

---

**End of Document 01 (v1.0.1-draft).**
