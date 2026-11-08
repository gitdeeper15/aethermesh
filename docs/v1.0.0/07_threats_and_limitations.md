# AetherMesh — Threats and Limitations (v1.0.0)

**Version:** 1.0.0
**Date:** 2026-11-08
**Status:** Formal Architecture Proposal with Simulated Evaluation
**Source:** Section 7 and Appendix D of the AetherMesh Research Paper (v1.0.0)
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)

---

## 1. Threat Taxonomy (Section 7.1)

We organize threats into **six classes**. Fifteen threats, **T1–T15**, are catalogued with mitigations and residual risk in Appendix D.

| Class | Question | Threats |
|---|---|---|
| **Soundness** | Can the architecture admit something it should not, or converge to something wrong? | T1–T3 |
| **Completeness** | Can it fail to admit or detect what it should? | T4–T5 |
| **Trust** | Do the trust assumptions hold? | T6–T8 |
| **Process** | Does it behave under load, partition, and growth? | T9–T11 |
| **Toolchain** | Do the simulator and implementation components faithfully represent the design? | T12–T13 |
| **Human** | Do operators and readers use it correctly? | T14–T15 |

---

## 2. Soundness Threats (Section 7.2)

### T1 — Admission nondeterminism

- **Threat:** A predicate that depends on local state can cause honest nodes to admit different sets and diverge permanently.
- **Mitigation:** The determinism requirement (A6) addresses this **by design**, but **nothing enforces it**.
- **Residual risk:** Medium: not mechanically enforced.

### T2 — Semantic-merge gap

- **Threat:** Individually valid deltas can combine into an invalid program.
- **Mitigation:** Compatibility matrix; higher-layer verification.
- **Residual risk:** High: matrix is coarse.

### T3 — Proof-sketch gaps

- **Threat:** Theorems 1–3 are sketches; a subtle error, for example in the treatment of fairness or deferral, may remain.
- **Mitigation:** Mechanization (future); explicit assumptions.
- **Residual risk:** Medium.

---

## 3. Completeness Threats (Section 7.3)

### T4 — Harmful but well-formed deltas

- **Threat:** A registered agent that is compromised or misaligned can submit deltas that satisfy every predicate and still do harm.
- **Mitigation:** Higher layers; review; provenance for attribution.
- **Residual risk:** High: no defence in this layer.

### T5 — False rejection

- **Threat:** An over-strict schema or matrix, or schema version skew between nodes, can reject valid deltas; because verdicts are deterministic, the rejection is consistent across nodes but may be wrong everywhere.
- **Mitigation:** Versioned schemas; quarantine option.
- **Residual risk:** Medium.

> **Note:** The simulation reported no false rejections, but it **did not test schema evolution**.

---

## 4. Trust Threats (Section 7.4)

### T6 — Key registry bootstrap or compromise

- **Threat:** Provenance is only as good as the key registry. Bootstrap, rotation, and revocation are not specified, and compromise of a key allows well-formed forged deltas under that identity.
- **Mitigation:** Rotation and revocation (unspecified); TEEs (future).
- **Residual risk:** High.

### T7 — Collusion or Sybil identities exceed n/3

- **Threat:** The `f < n/3` condition is meaningful only if identities are scarce; a Sybil attacker (Douceur, 2002) can exceed the fraction by creating identities.
- **Mitigation:** Scarce identities; quorum committee sampling.
- **Residual risk:** High under open membership.

### T8 — Eclipse or peer-sampling bias

- **Threat:** An adversary that dominates a node's peer sample can isolate it, delay dissemination, or feed it selected deltas; the uniform selection that Theorem 2 assumes is exactly what such an attack subverts.
- **Mitigation:** Partial-view refresh; diverse peers.
- **Residual risk:** Medium to high.

---

## 5. Process Threats (Section 7.5)

### T9 — Resource exhaustion

- **Threat:** Flooding with valid-looking deltas, oversized digests, or deltas with unsatisfiable parent pointers can exhaust CPU, bandwidth, or the deferral buffer.
- **Mitigation:** Per-origin rate limits; size bounds; bounded deferral. As local delivery policies, they **delay rather than reject**.
- **Residual risk:** Medium.

### T10 — History growth

- **Threat:** The delta set only grows; compaction must preserve join semantics.
- **Mitigation:** Compaction research (Q9).
- **Residual risk:** Medium.

### T11 — Long partitions

- **Threat:** After a long partition, healing may require a large merge, and the admission cost of the backlog may be considerable and **was not simulated**.
- **Mitigation:** State-based fallback; rate-limited admission.
- **Residual risk:** Unknown: not simulated.

---

## 6. Toolchain Threats (Section 7.6)

### T12 — Simulator fidelity

- **Threat:** The simulator uses a simplified network model; results may not transfer.
- **Mitigation:** Real-world evaluation (future).
- **Residual risk:** High until evaluated.

### T13 — Implementation faults

- **Threat:** Cryptographic library bugs, serialization differences, and schema version skew between nodes can all break the determinism that the theorems assume.
- **Mitigation:** Canonical encoding; versioning; testing.
- **Residual risk:** Medium.

---

## 7. Human Threats (Section 7.7)

### T14 — Misconfiguration

- **Threat:** Operators set fanout, period, matrix entries, and trust anchors; poor choices can degrade convergence or admit unwanted deltas.
- **Mitigation:** Defaults; review; documentation.
- **Residual risk:** Medium.

### T15 — Overreliance on simulated results

- **Threat:** Readers or downstream users may treat simulated figures as evidence of deployed performance. This paper's labelling is intended to prevent that; **it cannot enforce it**.
- **Mitigation:** Labeling throughout; Research Status Statement.
- **Residual risk:** Medium: cannot be enforced.

---

## 8. Threats to Validity (Section 7.8)

| Type | Threat | Status |
|---|---|---|
| **Internal** | Unknown simulator parameters, runs, and seeds; possible simulator artifacts; no ablation of pillars | **Open** |
| **External** | Simulated network, 10–500 nodes, malformed-delta-only adversary; no real code workloads | **Open**; results do not generalize without further evaluation |
| **Construct** | 'Convergence' measured as 99% merged, not 100%; 'invalid' means predicate-detectable; 'deadlock elimination' is partly by design | **Stated** in Section 5 |
| **Conclusion** | Five data points for scaling; no confidence intervals; proofs are sketches | **Stated** in Sections 4 and 5 |

---

## 9. Limitations (Section 7.9)

### 9.1 Architectural limitations

- The architecture provides **eventual**, **not strong**, consistency.
- It offers **no global order**.
- It filters **only predicate-detectable** invalid deltas.
- It assumes a **trustworthy key registry**.
- It **grows without compaction**.

### 9.2 Design limitations

- The **compatibility matrix**, **digest form**, **fanout policy**, **forwarding policy**, and **compaction** are **underspecified**.
- The **determinism requirement** is **not enforced mechanically**.

### 9.3 Scope limitations

- **Dynamic membership** is not treated.
- **Access control** beyond key registration is not treated.
- **Privacy of deltas** is not treated.
- **Integration with the other layers** is not treated.

> **Limitations of this section.**
> The threat catalogue is **not exhaustive** and its mitigations are **design intentions that have not been tested**. Residual risk entries are **our qualitative judgements, not measurements**.

---

## 10. When **Not** to Use AetherMesh (Section 6.3)

| Scenario | Reason |
|---|---|
| **Small, co-located teams or few agents** | A conventional central repository has lower complexity and, at this scale, probably adequate performance. |
| **Strong consistency requirements** | Unique-name allocation, exactly-once external effects, release gating, and any operation that needs a global order are **not expressible** as join-semilattice updates. |
| **Validity must hold before visibility** | If a merged program must be known to be correct before any agent can observe it, a gate before merge is required; AetherMesh admits deltas on **syntactic and compatibility grounds only**. |
| **Adversarial settings beyond the stated threat model** | Where colluding or well-funded adversaries are expected, a lightweight filter is insufficient, and consensus-based or hardware-attested designs should be considered. |
| **Constrained nodes** | Because the delta set grows without compaction (Q9), nodes with small storage budgets may not be able to hold replicas. |

---

## 11. Summary — All 15 Threats

| ID | Class | Threat | Residual risk |
|:-:|---|---|---|
| T1 | Soundness | Admission nondeterminism causes divergent admitted sets | Medium |
| T2 | Soundness | Semantic-merge gap: valid deltas combine into invalid program | High |
| T3 | Soundness | Proof sketches contain errors | Medium |
| T4 | Completeness | Well-formed but harmful deltas admitted | High |
| T5 | Completeness | False rejection from strict schema or version skew | Medium |
| T6 | Trust | Key registry bootstrap or compromise | High |
| T7 | Trust | Collusion or Sybil identities exceed n/3 | High (open membership) |
| T8 | Trust | Eclipse or peer-sampling bias | Medium to high |
| T9 | Process | Flooding, oversized digests, deferral exhaustion | Medium |
| T10 | Process | Unbounded history growth; unsafe compaction | Medium |
| T11 | Process | Costly healing after long partitions | Unknown (not simulated) |
| T12 | Toolchain | Simulator infidelity to real networks | High until evaluated |
| T13 | Toolchain | Crypto-library, serialization, or schema skew faults | Medium |
| T14 | Human | Operator misconfiguration | Medium |
| T15 | Human | Reliance on simulated results as deployed evidence | Medium |

> **Residual-risk entries are qualitative judgements by the author, offered to prioritize future work; they are not measurements.**

---

**End of Threats and Limitations (v1.0.0).**
