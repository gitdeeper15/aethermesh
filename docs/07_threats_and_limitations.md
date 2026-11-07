# AetherProof — Document 07: Threats and Limitations

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **threats and limitations** of AetherProof.

Its purpose is **not** to undermine the architecture, nor to claim that it is immune to failure. Its purpose is to establish:

1. A **precise taxonomy** of threats to soundness, completeness, and trust.
2. **Limitations** that are inherent to the architecture.
3. **Mitigations** for each threat, with explicit residual risk.
4. **Threats to validity** for future empirical evaluation.
5. **Open questions** that remain unanswered by the current architecture.

This document is scoped to threats and limitations. Architectural decisions are in the system architecture document. Each threat is linked to the document that defines the relevant component.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture — each layer is a potential source of threat.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR record structure — threats to record identity, artifact identity, and semantic identity.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  Semantic relations — threats to soundness and completeness propagate along these edges.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Two-axis classification — threats arise from misclassification.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifest — threats arise from incomplete TCBs.

---

## 3. Threat Taxonomy

### 3.1 Threat Categories

| Category | Description |
|----------|-------------|
| **Soundness threats** | The system may accept an invalid proof |
| **Completeness threats** | The system may reject a valid proof |
| **Trust threats** | The system may overstate the confidence of a result |
| **Specification threats** | The specification may not reflect intent |
| **Process threats** | The process may be bypassed or compromised |
| **Toolchain threats** | The tools may be incorrect or compromised |
| **Human threats** | Human reviewers may fail or be compromised |

### 3.2 Threat Table

| ID | Threat | Category | Severity | Mitigation | Residual Risk |
|----|--------|----------|----------|------------|---------------|
| T1 | Unsound proof artifact | Soundness | High | Independent checking | Low (if checker is trusted) |
| T2 | Incomplete TCB Manifest | Trust | High | Per-path TCB | Medium |
| T3 | Specification does not reflect intent | Specification | High | Human review | Medium |
| T4 | Silent assumption change | Trust | High | Assumption tracking | Low |
| T5 | Guardrail bypass | Process | High | Mandatory guardrails | Low |
| T6 | Toolchain compromise | Toolchain | High | Signed tools, TCB | Medium |
| T7 | Reviewer conflict of interest | Human | Medium | Separation of duties | Low |
| T8 | Incomplete completeness proof | Completeness | Medium | Explicit `Unknown` verdict | Medium |
| T9 | Semantic inconsistency between layers | Trust | Medium | Explicit translation classification | Medium |
| T10 | Counterexample flakiness | Soundness | Medium | Reproducibility check | Low |
| T11 | Model over-approximation | Completeness | Medium | Model validation | Medium |
| T12 | Hypothesis testing bias | Human | Medium | Blind review | Medium |
| T13 | Denial of service on proof engine | Process | Low | Bounded queues | Low |
| T14 | Audit log tampering | Process | High | Append-only, signed | Low |
| T15 | LLM-generated specification error | Specification | High | Human review | Medium |

---

## 4. Soundness Threats

### 4.1 T1 — Unsound Proof Artifact

**Description**: A proof artifact that is accepted as evidence, but that is not actually valid.

**Sources**:
- Tool bug (e.g., Z3 produces invalid `unsat` without proof).
- Proof checker bug (e.g., a kernel that accepts invalid proof terms).
- Toolchain mismatch (e.g., a proof produced with version X is checked by version Y).

**Mitigation**:
- Independent checking (Document 02, §7.2).
- TCB Manifest (Document 02, §8.1).
- Version pinning.

**Residual risk**: Low if the checker is trusted and the TCB Manifest is complete.

### 4.2 T10 — Counterexample Flakiness

**Description**: A counterexample that is not reproducible due to flaky tests or tool nondeterminism.

**Sources**:
- Flaky tests (Luo et al., 2014).
- Tool nondeterminism (e.g., timeouts).
- Environmental differences.

**Mitigation**:
- Reproducibility check (Document 04, §5.2).
- Re-run failing checks against parent state.

**Residual risk**: Low if the reproducibility check is reliable.

---

## 5. Completeness Threats

### 5.1 T8 — Incomplete Completeness Proof

**Description**: The system claims to be "complete" but is not, leading to false confidence in the absence of proofs.

**Sources**:
- The system does not prove *all* properties, only some.
- The system's `Unknown` verdict is ignored.

**Mitigation**:
- Explicit `Unknown` verdict (Document 02, §8.1).
- Human review for `Unknown` obligations.

**Residual risk**: Medium if `Unknown` is treated as `Proven`.

### 5.2 T11 — Model Over-Approximation

**Description**: The proof model admits behaviors that the implementation does not, leading to false `Refuted` verdicts.

**Sources**:
- Layer 1 models (TLA+) over-approximate the actual system.
- Translation from Layer 1 to Layer 2 (Why3/Lean) over-approximates.

**Mitigation**:
- Model validation (Document 04, §5.4).
- Explicit translation classification (Document 01, §6.1).

**Residual risk**: Medium if the model is not validated.

---

## 6. Trust Threats

### 6.1 T2 — Incomplete TCB Manifest

**Description**: The TCB Manifest does not record all components used to produce a proof, leading to false confidence.

**Sources**:
- Missing tool version.
- Missing assumption.
- Missing transformation.

**Mitigation**:
- Per-path TCB Manifests (Document 02, §8.1).
- Mandatory field completion.
- Audit of TCB Manifests (Document 06, §7).

**Residual risk**: Medium if the audit is not performed.

### 6.2 T4 — Silent Assumption Change

**Description**: An assumption is changed without invalidating dependent obligations.

**Sources**:
- Tool bug (assumption change not detected).
- Human error (assumption change not recorded).
- Process bypass.

**Mitigation**:
- Assumption tracking (Document 02, §6).
- Invalidation rules (Document 03, §5).
- Signed decision records (Document 06, §7).

**Residual risk**: Low if tracking is enforced.

### 6.3 T9 — Semantic Inconsistency Between Layers

**Description**: Two layers (e.g., L1 and L2) have meanings that are inconsistent, but the inconsistency is not detected.

**Sources**:
- Translation is not sound (Document 01, §6.2).
- Translation is misclassified as `Exact` when it is `Lossy`.
- Semantic consistency is not verified.

**Mitigation**:
- Explicit translation classification (Document 01, §6.1).
- Two-axis classification (Document 01, §6.1).
- Open question Q2 (semantic consistency).

**Residual risk**: Medium if Q2 is not resolved.

---

## 7. Specification Threats

### 7.1 T3 — Specification Does Not Reflect Intent

**Description**: The specification is formally correct but does not reflect what the human actually intended.

**Sources**:
- Specification synthesized from code (bug-compatible).
- Specification written without reference to requirements.
- Specification not reviewed by human.

**Mitigation**:
- Traceability chain (Document 01, §7).
- Human review (Document 06, §5.1).
- `unformalized` marker (Document 01, §7.2).

**Residual risk**: Medium if human review is insufficient.

### 7.2 T15 — LLM-Generated Specification Error

**Description**: A specification generated by an LLM contains errors that are not caught by human review.

**Sources**:
- LLM hallucination.
- LLM bias.
- LLM overgeneralization.

**Mitigation**:
- Human review (Document 06, §5.1).
- Traceability (Document 01, §7).
- Multiple LLMs (not specified in current architecture).

**Residual risk**: High if human review is superficial.

---

## 8. Process Threats

### 8.1 T5 — Guardrail Bypass

**Description**: A remediation patch bypasses guardrails and weakens the specification or tests.

**Sources**:
- Guardrail not enforced.
- Guardrail weakened by a human.
- Guardrail circumvented by a tool.

**Mitigation**:
- Mandatory guardrails (Document 04, §6.4).
- Separation of duties (Document 06, §3.3).
- Audit (Document 06, §7).

**Residual risk**: Low if guardrails are enforced.

### 8.2 T13 — Denial of Service on Proof Engine

**Description**: An adversary floods the proof engine with obligations, causing it to fail or time out.

**Sources**:
- Malicious changesets.
- Buggy synthesis engine.
- Infinite loop in a proof tool.

**Mitigation**:
- Bounded queues (Document 05, §6.3).
- Proof budget (Document 03, §7.2).
- Rate limiting (not specified in current architecture).

**Residual risk**: Low if queues are bounded.

### 8.3 T14 — Audit Log Tampering

**Description**: The audit log is modified to hide a decision.

**Sources**:
- Malicious maintainer.
- Bug in append-only implementation.
- Storage corruption.

**Mitigation**:
- Append-only (Document 06, §7.2).
- Signed (Document 06, §7.2).
- Hash-chained (not specified in current architecture).

**Residual risk**: Low if hash-chaining is implemented.

---

## 9. Toolchain Threats

### 9.1 T6 — Toolchain Compromise

**Description**: A tool in the verification path is compromised, producing invalid proofs or invalid TCB Manifests.

**Sources**:
- Supply chain attack.
- Malicious tool update.
- Misconfiguration.

**Mitigation**:
- Signed tools (not specified in current architecture).
- TCB Manifest (Document 02, §8.1).
- Version pinning.
- Independent checking.

**Residual risk**: Medium if tool signing is not implemented.

---

## 10. Human Threats

### 10.1 T7 — Reviewer Conflict of Interest

**Description**: A reviewer has a conflict of interest (e.g., they authored the specification being reviewed) and approves a change that should be rejected.

**Sources**:
- Separation of duties not enforced.
- Reviewer unaware of conflict.

**Mitigation**:
- Separation of duties (Document 06, §3.3).
- Conflict-of-interest disclosure (not specified in current architecture).

**Residual risk**: Low if separation of duties is enforced.

### 10.2 T12 — Hypothesis Testing Bias

**Description**: A human reviewer (or the system) has a bias toward accepting or rejecting a hypothesis, leading to wrong diagnosis.

**Sources**:
- Confirmation bias.
- Anchoring bias.
- Groupthink.

**Mitigation**:
- Blind review (not specified in current architecture).
- Multiple reviewers (not specified in current architecture).
- Structured diagnosis protocol (Document 04, §5).

**Residual risk**: Medium if review is not blind or multi-person.

---

## 11. Threats to Validity (for Future Empirical Evaluation)

### 11.1 Internal Validity

| Threat | Description |
|--------|-------------|
| **Selection bias** | If the benchmark repositories are not representative, results may not generalize. |
| **Measurement bias** | If the metrics (e.g., proof time) are measured incorrectly, results may be misleading. |
| **Confounding factors** | Tool performance may depend on many factors not controlled in the experiment. |
| **Experimenter bias** | The experimenter may unconsciously influence results. |

### 11.2 External Validity

| Threat | Description |
|--------|-------------|
| **Population validity** | The benchmark repositories may not represent all codebases. |
| **Ecological validity** | The experimental setting may differ from real-world usage. |
| **Temporal validity** | Results may not hold over time as tools and repositories evolve. |

### 11.3 Construct Validity

| Threat | Description |
|--------|-------------|
| **Metric validity** | The metrics (e.g., "proof coverage") may not measure what they claim to measure. |
| **Definition validity** | The definitions (e.g., "semantic consistency") may not capture the intended concept. |

### 11.4 Conclusion Validity

| Threat | Description |
|--------|-------------|
| **Statistical validity** | The sample size may be insufficient for statistical significance. |
| **Causal validity** | Correlation may be mistaken for causation. |

---

## 12. Limitations

### 12.1 Architectural Limitations

| Limitation | Description |
|------------|-------------|
| **No implementation benchmarked** | The architecture is descriptive, not empirical. |
| **No real-world deployment** | Performance, scalability, and usability are unknown. |
| **No empirical validation** | The architecture's claims are structural, not measured. |
| **Protocol-only integration** | Cross-system performance is unknown. |

### 12.2 Design Limitations

| Limitation | Description |
|------------|-------------|
| **No universal specification language** | The three layers are not interchangeable. |
| **No automated specification synthesis from intent** | Specifications require human review. |
| **No automated proof of specification correctness** | Specifications may not reflect intent. |
| **No fully automated remediation** | Human review is required for specification changes. |

### 12.3 Scope Limitations

| Limitation | Description |
|------------|-------------|
| **Scope limited to formal properties** | Empirical properties (e.g., performance) are not covered. |
| **Scope limited to code** | Data, configuration, and infrastructure are not covered. |
| **Scope limited to synchronous systems** | Distributed and asynchronous systems are partially covered. |

---

## 13. Open Questions

| ID | Question | Status |
|----|----------|--------|
| Q43 | Can tool signing be implemented without breaking existing workflows? | Open |
| Q44 | Can conflict-of-interest disclosure be automated? | Open |
| Q45 | Can blind review be implemented without losing traceability? | Open |
| Q46 | How should the architecture handle toolchain evolution? | Open |
| Q47 | How should `Unknown` obligations be prioritized for human review? | Open |
| Q48 | What is the maximum acceptable latency for human review? | Open |
| Q49 | Can the architecture be extended to distributed systems? | Open |
| Q50 | Can the architecture be extended to empirical properties (performance)? | Open |

---

## 14. Design Decisions and Deferred Commitments

### 14.1 Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D48 | Threats are explicitly catalogued | Prevents hiding |
| D49 | Limitations are explicitly stated | Prevents overclaiming |
| D50 | Residual risk is acknowledged | Prevents false confidence |
| D51 | Threats to validity are catalogued | Prepares for empirical evaluation |
| D52 | Open questions are listed | Defines research agenda |

### 14.2 Decisions Deferred

| ID | Deferred Question | Deferred To |
|----|-------------------|-------------|
| DD39 | Tool signing implementation | Future work |
| DD40 | Conflict-of-interest automation | Future work |
| DD41 | Blind review implementation | Future work |
| DD42 | Distributed systems extension | Future work |
| DD43 | Empirical properties extension | Future work |

---

## 15. Summary

This document establishes:

1. A **precise taxonomy** of threats (15 threats across 7 categories).
2. **Mitigations** and **residual risks** for each threat.
3. **Limitations** that are inherent to the architecture.
4. **Threats to validity** for future empirical evaluation.
5. **Open questions** that remain unanswered.

The governing question of this document is:

> **What are the threats and limitations of AetherProof, and how can they be mitigated, acknowledged, or deferred without overclaiming the architecture's capabilities?**

This question is **answered structurally** by the catalogues. Its **empirical** answer requires future work.

---

## Appendix A — Glossary

| Term | Definition |
|------|------------|
| **Soundness** | The property that if the system says "proven," then the property is true |
| **Completeness** | The property that if the property is true, then the system can prove it |
| **Trust** | The degree of confidence in a result |
| **Residual risk** | The risk that remains after mitigation |
| **Threats to validity** | Factors that may invalidate empirical results |

---

## Appendix B — References

- Document 01: Specification Language (AetherProof, 2026).
- Document 02: Proof Obligations (AetherProof, 2026).
- Document 03: Incremental Proof Engine (AetherProof, 2026).
- Document 04: Counterexample Remediation (AetherProof, 2026).
- Document 05: Integration Protocol (AetherProof, 2026).
- Document 06: Human Review Protocol (AetherProof, 2026).
- Luo, Q., et al. (2014). An Empirical Analysis of Flaky Tests. *FSE 2014*.
- Klein, G., et al. (2009). seL4: Formal Verification of an OS Kernel. *SOSP 2009*.

---

**End of Document 07 (v1.0.0-draft).**
