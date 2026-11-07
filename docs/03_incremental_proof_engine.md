# AetherProof — Document 03: Incremental Differential Proof Engine

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **incremental differential proof engine** of AetherProof.

Its purpose is **not** to describe a complete theorem prover, nor to replace TLA+, Why3, Lean, or Z3. Its purpose is to establish:

1. A **precise model** of incremental proving over a changeset DAG.
2. A **proof dependency graph** (PDG) that extends the obligation DAG from Document 02.
3. **Invalidation rules** that determine when a previously-discharged obligation must be re-examined.
4. **Reuse conditions** under which a proof artifact remains valid after a code change.
5. A **cost-aware proof strategy** that balances proving effort against coverage.
6. **Open mathematical questions** specific to differential proving.

This document is scoped to the proof engine. Counterexample remediation is addressed in Document 04. System integration with AetherGit and AetherFlow is addressed in Document 05.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture that hosts the proof engine.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR record structure — the source of proof obligations.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  A requirement-driven proof trace — showing how obligations and evidence propagate.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Two-axis classification — determines which obligations are checkable and how.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifest structure — records how obligations are discharged and re-discharged.

---

## 3. The Differential Proving Problem

### 3.1 The Problem Statement

Given a repository with a set of discharged obligations, and given a new changeset `Δ`, determine:

1. Which obligations are **affected** by `Δ`.
2. Which affected obligations can be **safely reused** (evidence still valid).
3. Which affected obligations must be **re-discharged**.
4. The **minimal set** of re-discharges that restores full evidence coverage.

### 3.2 Why Differential?

Full re-proving after every change is prohibitively expensive. Differential proving exploits the structure of the changeset DAG to:

- Avoid re-proving unaffected obligations.
- Reuse valid evidence when assumptions are unchanged.
- Invalidate only the minimal necessary set.

### 3.3 The Two Failure Modes

| Failure Mode | Consequence |
|--------------|-------------|
| **Over-invalidation** | Excessive re-proving; performance degrades to full re-proving |
| **Under-invalidation** | Unsound reuse; a stale proof is treated as valid |

**AetherProof aims to minimize both**, not to eliminate one at the cost of the other.

---

## 4. Proof Dependency Graph (PDG)

### 4.1 Definition

The **Proof Dependency Graph (PDG)** extends the Obligation Dependency Graph (ODG, Document 02) with **evidence nodes** and **assumption nodes**.

```

PDG = (Obligations ∪ Evidence ∪ Assumptions, Edges)

```

### 4.2 Node Types

| Node Type | Description |
|-----------|-------------|
| **Obligation** | From Document 02 (an obligation to be discharged) |
| **Evidence** | A proof artifact, model, or human justification |
| **Assumption** | A named proposition that obligations depend on |

### 4.3 Edge Types

| Edge Type | Meaning |
|-----------|---------|
| `discharges` | Evidence → Obligation (evidence proves the obligation) |
| `depends_on` | Obligation → Assumption (obligation requires the assumption) |
| `supports` | Evidence → Evidence (one evidence piece supports another) |
| `derives_from` | Obligation → Obligation (one obligation is derived from another) |
| `invalidates` | Changeset → Node (a changeset invalidates a node) |

### 4.4 Invariants

1. **Acyclicity**: The PDG must be a DAG.
2. **Total discharge**: Every `Proven` obligation has at least one `discharges` edge from a valid evidence node.
3. **Assumption closure**: Every obligation's `depends_on` edges point to assumptions that are declared in the obligation's `assumptions` set.
4. **No orphan evidence**: Every evidence node must `discharge` at least one obligation.

---

## 5. Invalidation Rules

### 5.1 Invalidation Triggers

A node `N` in the PDG is **invalidated** when any of the following holds:

| Trigger | Affected Nodes |
|---------|----------------|
| A changeset modifies a CSR record that is `source` of `N` | `N` and all nodes reachable from `N` via `derives_from` |
| A changeset modifies an assumption that `N` `depends_on` | `N` and all nodes reachable from `N` via `derives_from` |
| A changeset modifies a proof artifact that `discharges` `N` | `N` (the evidence is stale) |
| A changeset modifies a file within the `blast_radius` of `N` | `N` and all dependents |

### 5.2 Invalidation Algorithm

```

function invalidate(Δ, PDG):
seeds = find_nodes_affected_by(Δ, PDG)
invalidated = {}

```

### 5.3 Reuse Conditions

An invalidated obligation `O` can be **reused** (i.e., its evidence remains valid) if and only if:

1. **Assumption preservation**: Every assumption in `O.assumptions` is unchanged.
2. **Evidence compatibility**: The evidence's TCB Manifest declares the same tool versions and assumptions as `O`.
3. **Property stability**: The property `O.property` has not changed.
4. **Semantic relation preservation**: Every `refines` and `approximates` relation in the path from `O` to its source CSR record is unchanged.

If any of these conditions fails, the obligation must be **re-discharged**.

---

## 6. Reuse and Re-Discharge Strategy

### 6.1 Reuse Decision Tree

```

For each invalidated obligation O:
if (assumptions_unchanged(O) and
evidence_compatible(O) and
property_stable(O) and
relations_unchanged(O)):
reuse(O)  # Mark as validated
else:
re_discharge(O)

```

### 6.2 Re-Discharge Priority

Obligations that cannot be reused are re-discharged in priority order:

1. **High priority**: Obligations on the critical path (e.g., L1 invariants that gate releases).
2. **Medium priority**: Obligations that are downstream of high-priority obligations.
3. **Low priority**: Obligations whose source CSR records are new or recently modified.

### 6.3 Re-Discharge Path Selection

For each re-discharged obligation, the engine selects a discharge path:

| Condition | Preferred Path |
|-----------|----------------|
| Property is decidable in SMT-LIB | Z3 (fast) |
| Property involves system behavior | TLA+ (TLC or TLAPS) |
| Property involves functional contracts | Why3 |
| Property requires dependent types | Lean |
| None of the above | Escalated to Human |

**Cost-aware selection**: The engine estimates proving cost before dispatching and may choose a cheaper (but weaker) path if the stronger path would exceed budget.

---

## 7. Cost-Aware Proving

### 7.1 Cost Estimation

For each obligation, the engine estimates:

| Cost Component | Estimation Method |
|----------------|-------------------|
| **SMT solving cost** | Formula size, theory complexity |
| **Model checking cost** | State-space size, bound |
| **Deductive proof cost** | Number of subgoals, complexity of lemmas |
| **Human review cost** | Manual effort (qualitative) |

### 7.2 Proof Budget

The engine operates under a **proof budget**:

```

Budget = (time_budget, cost_budget, human_attention_budget)

```

When the budget is exceeded, the engine:

1. Marks remaining obligations as `Unknown`.
2. Escalates to human review.
3. Records the budget exhaustion in the audit log.

### 7.3 Tiered Proving

The engine uses **tiered proving**:

| Tier | Tool | Cost | Strength |
|------|------|------|----------|
| **Tier 1** | Z3 | Low | Weak (only decidable theories) |
| **Tier 2** | TLC | Medium | Bounded model checking |
| **Tier 3** | Why3 | Medium-High | Deductive contracts |
| **Tier 4** | Lean | High | Full dependent types |
| **Tier 5** | Human | Very High | Any property |

The engine **starts at Tier 1** and escalates only if lower tiers fail.

---

## 8. Concurrency and Multi-Agent Proving

### 8.1 Concurrency Model

The proof engine is **decentralized**:

- Workers are **stateless** with respect to the PDG.
- The PDG is **shared** via the CSR (Document 01).
- Concurrent re-discharges of the same obligation are **idempotent**.

### 8.2 Conflict Resolution

If two workers produce **different evidence** for the same obligation:

1. Both evidences are recorded.
2. The evidence with the **stronger TCB** is preferred.
3. If TCBs are incomparable, both are retained as **alternative evidence**.
4. The choice of which evidence is "authoritative" is recorded in the audit log.

### 8.3 Deadlock and Starvation

Because workers are stateless and the PDG is a DAG, no deadlock is possible. Starvation is prevented by **priority scheduling** (Section 6.2).

---

## 9. Validation and Audit

### 9.1 Proof Evidence Record

Every discharge produces a **Proof Evidence Record** with:

| Field | Content |
|-------|---------|
| `obligation_id` | The obligation discharged |
| `evidence_type` | `proof_term` / `model` / `human_justification` |
| `evidence_artifact` | Path or hash of the evidence |
| `tcb_manifest` | The TCB Manifest used |
| `timestamp` | When the discharge occurred |
| `worker_id` | Which worker produced the evidence |
| `validation_status` | `valid` / `stale` / `disputed` |

### 9.2 Audit Log

Every PDG mutation (invalidation, reuse, re-discharge) is recorded in an **append-only audit log**. The log is checked into the repository alongside the CSR records.

### 9.3 Re-validation

Periodically, a **re-validation pass** checks that:

1. Every `Proven` obligation has a valid evidence record.
2. Every evidence record's TCB Manifest is still accurate.
3. No assumptions have been silently changed.

---

## 10. Open Mathematical Questions

| ID | Question | Status |
|----|----------|--------|
| Q13 | What is the minimal PDG structure that supports sound invalidation and reuse? | Open |
| Q14 | Under what conditions can evidence be reused across changesets without re-discharge? | Open |
| Q15 | How should cost be estimated for complex obligations? | Open |
| Q16 | When should the engine escalate to a higher tier vs. accept `Unknown`? | Open |
| Q17 | How should conflicting evidence be resolved? | Open |
| Q18 | Can re-validation be made incremental? | Open |

---

## 11. Design Decisions and Deferred Commitments

### 11.1 Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D15 | PDG extends ODG with evidence and assumptions | Complete dependency model |
| D16 | Invalidation propagates via `derives_from` edges | Minimal necessary set |
| D17 | Reuse requires assumption preservation and evidence compatibility | Soundness |
| D18 | Tiered proving with escalation | Cost-effective |
| D19 | Concurrency model is decentralized and stateless | Scalability |
| D20 | Audit log is append-only and checked in | Reproducibility |
| D21 | Re-validation is periodic, not continuous | Practical |

### 11.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD13 | Full PDG schema (JSON/YAML) | Document 04 |
| DD14 | Cost estimation formulas | Document 04 |
| DD15 | Counterexample representation | Document 04 |
| DD16 | Remediation protocol | Document 04 |
| DD17 | Integration protocol with AetherFlow | Document 05 |
| DD18 | Human review as discharge evidence | Document 06 |

---

## 12. Summary

This document establishes:

1. A **precise model** of incremental proving over a changeset DAG.
2. A **Proof Dependency Graph (PDG)** that extends the obligation DAG from Document 02.
3. **Invalidation rules** that determine when a discharged obligation must be re-examined.
4. **Reuse conditions** under which a proof artifact remains valid after a code change.
5. A **cost-aware proof strategy** with tiered proving.
6. **Concurrency and audit** models for decentralized proving.
7. **Open mathematical questions** specific to differential proving.

The governing question of this document is:

> **Given a changeset Δ and a PDG of discharged obligations, what is the minimal set of re-discharges required to restore full evidence coverage, and how can that set be computed soundly and efficiently?**

This question is **partially answered** by the structures defined here. Full answer requires Documents 04–06.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **PDG** | Proof Dependency Graph |
| **Invalidation** | The act of marking a node as no longer valid |
| **Reuse** | The act of treating invalidated evidence as still valid |
| **Re-discharge** | The act of producing new evidence for an obligation |
| **Proof Budget** | A bound on time, cost, and human attention |
| **Tier** | A level of proving strength (Tier 1 = weakest, Tier 5 = human) |

---

## Appendix B — References

- Document 01: Specification Language (AetherProof, 2026).
- Document 02: Proof Obligations (AetherProof, 2026).
- Klein, G., et al. (2009). seL4: Formal Verification of an OS Kernel. *SOSP 2009*.
- Klein, G., et al. (2014). Comprehensive Formal Verification of an OS Microkernel. *ACM TOCS*.

---

**End of Document 03 (v1.0.0-draft).**
