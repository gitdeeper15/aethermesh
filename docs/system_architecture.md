# AetherProof — System Architecture

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **system architecture** of AetherProof.

Its purpose is to integrate the four foundational documents (01–04) into a single architecture that:

1. Situates AetherProof as the **third layer** in the Aether family (Git → Flow → Proof).
2. Defines the **components** of the system and their responsibilities.
3. Specifies the **interfaces** between components.
4. Establishes the **protocols** for cross-system integration.
5. States the **non-goals** and **limitations** of the architecture.
6. Records **open questions** that require empirical investigation.

This document is scoped to system architecture. Detailed algorithms are in Documents 01–04. Integration protocol details are in Document 05.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture: L1 (TLA+), L2 (Why3/Lean), L3 (SMT-LIB/Z3).

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR record structure: three identities and their relationships.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  Requirement-driven proof trace: from requirement to evidence.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Two-axis classification: semantic relationship × verification property.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifest structure: per-path trusted computing base.

---

## 3. Position in the Aether Family

### 3.1 Three-Layer Stack

```

┌─────────────────────────────────────────────────────────┐
│  AetherProof — Verification Layer                        │
│  • Specification synthesis                               │
│  • Proof obligation generation                           │
│  • Differential proving                                  │
│  • Counterexample remediation                            │
└─────────────────────┬───────────────────────────────────┘
│ protocol (Document 05)
▼
┌─────────────────────────────────────────────────────────┐
│  AetherFlow — Integration Layer                          │
│  • Lock-free merge entry                                 │
│  • Post-merge verification                               │
│  • Proactive remediation agents                          │
└─────────────────────┬───────────────────────────────────┘
│ protocol (AetherGit API)
▼
┌─────────────────────────────────────────────────────────┐
│  AetherGit — Storage Layer                               │
│  • Changeset log (append-only)                           │
│  • Content-addressed storage                             │
│  • Tiered cache topology                                 │
└─────────────────────────────────────────────────────────┘

```

### 3.2 Responsibilities by Layer

| Layer | Question | Responsibility |
|-------|----------|----------------|
| **AetherGit** | How are changes stored and transferred? | Storage, DAG, content addressing |
| **AetherFlow** | How are changes admitted, verified, and remediated? | Lock-free entry, post-merge verification, remediation |
| **AetherProof** | What conditions make behavior correct, and how are they proven? | Specification, obligations, proofs, counterexamples |

### 3.3 Methodological Independence

Each layer is **methodologically independent**:

- AetherGit requires only an append-only log.
- AetherFlow requires only a changeset log with parent pointers.
- AetherProof requires only a CSR record format and a changeset source.

**No layer is a precondition for another's formal claims.** Integration is **protocol-based**, not **code-based**.

---

## 4. AetherProof Components

### 4.1 Component Map

```

┌─────────────────────────────────────────────────────────┐
│  AetherProof                                             │
│                                                          │
│  ┌──────────────────┐   ┌──────────────────┐           │
│  │  Synthesis       │   │  Obligation      │           │
│  │  Engine          │──▶│  Generator       │           │
│  └────────┬─────────┘   └────────┬─────────┘           │
│           │                      │                      │
│           │                      ▼                      │
│           │            ┌──────────────────┐             │
│           │            │  Proof Engine    │             │
│           │            │  (Differential)  │             │
│           │            └────────┬─────────┘             │
│           │                     │                      │
│           │                     ▼                      │
│           │            ┌──────────────────┐             │
│           │            │  Discharge       │             │
│           │            │  Validator       │             │
│           │            └────────┬─────────┘             │
│           │                     │                      │
│           ▼                     ▼                      │
│  ┌──────────────────┐   ┌──────────────────┐           │
│  │  Remediation     │◀──│  Counterexample  │           │
│  │  Engine          │   │  Analyzer        │           │
│  └────────┬─────────┘   └──────────────────┘           │
│           │                                            │
│           ▼                                            │
│  ┌──────────────────┐                                  │
│  │  Changeset       │                                  │
│  │  Emitter         │──▶ AetherFlow                   │
│  └──────────────────┘                                  │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │  CSR Store (with PDG + Evidence Log)         │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘

```

### 4.2 Component Descriptions

| Component | Responsibility | Input | Output |
|-----------|----------------|-------|--------|
| **Synthesis Engine** | Generate candidate specifications from requirements and code | Requirements, code changesets | Candidate CSR records |
| **Obligation Generator** | Generate proof obligations from CSR records | CSR records | Obligations (Document 02) |
| **Proof Engine** | Discharge obligations via differential proving | Obligations, evidence | Proof evidence (Document 03) |
| **Discharge Validator** | Validate evidence and TCB Manifests | Evidence, TCB Manifests | Validated evidence |
| **Counterexample Analyzer** | Diagnose counterexamples | Refuted obligations | Diagnosed counterexamples (Document 04) |
| **Remediation Engine** | Propose and validate patches | Counterexamples | Remediation changesets |
| **Changeset Emitter** | Submit patches to AetherFlow | Remediation patches | Changesets (via Document 05 protocol) |
| **CSR Store** | Persistent storage of CSR, PDG, evidence | All of the above | Persistent state |

---

## 5. Data Flow

### 5.1 Requirement-to-Evidence Flow

```

Requirement
↓ [Synthesis Engine]
Candidate Specification
↓ [human review → CSR record]
CSR Record
↓ [Obligation Generator]
Proof Obligation
↓ [Proof Engine]
Proof Evidence + TCB Manifest
↓ [Discharge Validator]
Verified Evidence
↓ [stored in CSR Store]
Persistent Evidence

```

### 5.2 Counterexample Flow

```

Refuted Obligation
↓ [Counterexample Analyzer]
Diagnosed Counterexample
↓ [Remediation Engine]
Patch Proposal
↓ [Guardrails]
Accepted / Rejected Patch
↓ [Changeset Emitter]
Changeset → AetherFlow

```

---

## 6. Interfaces

### 6.1 External Interfaces

| Interface | Direction | Protocol | Document |
|-----------|-----------|----------|----------|
| **AetherProof ↔ AetherFlow** | Bidirectional | Changeset + counterexample | Document 05 |
| **AetherProof ↔ AetherGit** | Read-only | Changeset DAG | AetherGit API |
| **AetherProof ↔ Human** | Bidirectional | CSR review, escalation | Human review protocol |
| **AetherProof ↔ External Tools** | Outbound | TLA+, Why3, Lean, Z3 APIs | Tool-specific |

### 6.2 Internal Interfaces

Internal interfaces are defined by the CSR Store schema and the PDG structure (Documents 01 and 03). They are not exposed externally.

---

## 7. Non-Goals

AetherProof **does not** aim to:

1. **Unify all specification languages** into one. (§3, Document 01)
2. **Replace human judgment** in specification authoring or remediation.
3. **Claim absolute correctness** of any system.
4. **Substitute LLM-generated proofs** for independently checkable evidence.
5. **Assume semantic consistency** without proof. (§6.3, Document 01)
6. **Treat layer position** as semantic refinement.
7. **Silence counterexamples** by modifying specifications silently. (§4.3, Document 04)
8. **Guarantee full automation** of remediation. (§4.2, Document 04)

---

## 8. Limitations

### 8.1 Open Research Questions

The following are **open** and shape the research frontier:

| ID | Question | Document |
|----|----------|----------|
| Q1–Q7 | Specification language (translation soundness, semantic consistency, CSR identities) | 01 |
| Q8–Q12 | Proof obligations (obligation structure, re-discharge, human review) | 02 |
| Q13–Q18 | Differential proving (PDG, reuse, cost, escalation) | 03 |
| Q19–Q24 | Counterexample remediation (diagnosis, guardrails, confluence) | 04 |

### 8.2 Architectural Constraints

| Constraint | Consequence |
|------------|-------------|
| **No implementation benchmarked** | The architecture is descriptive, not empirical |
| **No real-world deployment** | Performance, scalability, and usability are unknown |
| **No empirical validation** | The architecture's claims are structural, not measured |
| **Protocol-only integration** | Cross-system performance is unknown |

### 8.3 Known Unknowns

- **Cost**: The computational cost of differential proving at scale is unknown.
- **Scalability**: The number of obligations that can be managed is unknown.
- **Usability**: The burden on human reviewers is unknown.
- **Soundness at scale**: Whether the architecture preserves soundness under concurrent agent activity is unknown.

---

## 9. Open Questions

| ID | Question | Status |
|----|----------|--------|
| Q25 | What is the minimal viable AetherProof implementation that demonstrates the architecture? | Open |
| Q26 | How does AetherProof perform at scale (thousands of obligations, hundreds of changesets/day)? | Open |
| Q27 | What is the human review burden per changeset? | Open |
| Q28 | Can AetherProof integrate with existing CI/CD systems without modification? | Open |
| Q29 | How does AetherProof handle heterogeneous toolchains (TLA+, Why3, Lean, Z3)? | Open |
| Q30 | What is the failure mode when the synthesis engine produces incorrect specifications? | Open |

---

## 10. Design Decisions

### 10.1 Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D29 | Three-layer architecture, protocol-based integration | Methodological independence |
| D30 | CSR Store as central component | Single source of truth |
| D31 | Changeset Emitter routes all patches through AetherFlow | Unified admission |
| D32 | Human review is a first-class component | Preserves judgment |
| D33 | Non-goals are explicit | Prevents scope creep |
| D34 | Limitations are stated | Prevents overclaiming |

### 10.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD24 | Full component schema (JSON/YAML) | Future work |
| DD25 | Performance benchmarks | Future work |
| DD26 | Usability studies | Future work |
| DD27 | Toolchain integration details | Document 05 |
| DD28 | Deployment architecture | Future work |

---

## 11. Summary

This document establishes:

1. AetherProof's **position** as the verification layer of the Aether family.
2. **Components** and their responsibilities.
3. **Data flows** from requirement to evidence and from counterexample to patch.
4. **Interfaces** between AetherProof and AetherFlow, AetherGit, humans, and tools.
5. **Non-goals** and **limitations** stated explicitly.
6. **Open questions** that require empirical investigation.

The governing question of this document is:

> **What is the minimal system architecture that integrates the four foundational documents (specification, obligations, proving, remediation) into a coherent whole without overclaiming, and what are its explicit limits?**

This question is **answered structurally** by the architecture. Its **empirical** answer requires future work.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **AetherGit** | Storage layer (from prior work) |
| **AetherFlow** | Integration layer (from prior work) |
| **AetherProof** | Verification layer (this project) |
| **CSR Store** | Persistent storage of CSR records, PDG, and evidence |
| **Protocol-based integration** | Integration via interfaces, not shared code |

---

**End of system_architecture.md (v1.0.0-draft).**
