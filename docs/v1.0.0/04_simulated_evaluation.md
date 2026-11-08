# AetherMesh — Simulated Evaluation (v1.0.0)

**Version:** 1.0.0
**Date:** 2026-11-08
**Status:** Formal Architecture Proposal with Simulated Evaluation
**Source:** Section 5 of the AetherMesh Research Paper (v1.0.0)
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)

---

## 1. Evidentiary Status

> **Every number in this document is a simulation result.**
>
> None is a measurement of a deployed system, and none should be quoted as one.

We report the values supplied by the author's simulation records **without alteration**, and we add our own analysis of those values where it bears on how they should be interpreted.

---

## 2. Testbed (Section 5.1)

The testbed is a **custom discrete simulation** of a peer-to-peer network, implemented in Python with NumPy, that instantiates between **10 and 500 autonomous agent nodes** in partitioned network topologies. Each node maintains a replica and runs the gossip and admission logic of Section 3.

### 2.1 What is reported

| Item | Reported |
|---|---|
| Scale | 10, 50, 100, 250, 500 nodes |
| Topology | Partitioned topologies |
| Simulator | Custom, Python + NumPy |
| Workload | Single-edge-node mutation (Metric 1); high-concurrency conflicting edits (Metric 2); malformed deltas (Metric 3) |
| Statistics | Averages for Metric 1 |
| Baseline | "Traditional lock-based version control" (Metric 2) |

### 2.2 What is **not** reported

| Item | Not reported |
|---|---|
| Intermediate sizes | Not evaluated |
| Sizes above 500 | Not evaluated |
| Topology generator / partition schedule / diameter | Not stated |
| Simulator source / version / random seeds | **Not included in this record** |
| Protocol parameters | Fanout `k`, period `1/r`, digest form, peer-sample size |
| Delta size and rate | Not stated |
| Number of injected deltas | **Not stated** (relevant to Metric 3) |
| Number of runs | Not stated |
| Variance, confidence intervals, percentiles | Not reported |
| Baseline implementation, lock granularity, workload equivalence | Not stated |

> The record available for this paper does **not** state several parameters that a reader would need in order to reproduce or critically assess the results. Simulator source and raw traces are **not** part of this record. We therefore treat the results as **reported figures whose provenance is the author's simulation records**, and we make **no claim** that they have been independently reproduced.

### 2.3 Network model

The network model is **simplified**:

- It does **not** reproduce real latency distributions.
- It does **not** reproduce packet loss.
- It does **not** reproduce NAT traversal.
- It does **not** reproduce adversarial network behaviour.

---

## 3. Metric 1 — State Convergence Latency (Section 5.2)

### 3.1 Definition

**Convergence Latency:** the time required for a code mutation introduced at a single edge node to propagate to, and be merged by, **99% of the network**.

### 3.2 Simulation-reported results

The average convergence time was reported as **below 450 ms for 250 nodes (420 ms)**.

| Nodes | 10 | 50 | 100 | 250 | 500 |
|---|:-:|:-:|:-:|:-:|:-:|
| Convergence time (ms), simulated | 45 | 120 | 210 | 420 | 680 |

**Figure 8(b)** (`Fig3_Gossip_Propagation.png`, panel b) shows these five points on a logarithmic x-axis, with the 450 ms and 250-node reference lines. This panel shows **simulation results as reported**; it is **not** a measurement of a deployed system.

### 3.3 Our scaling analysis

The source material described scaling as **"linear with log(n)"**. We examined that description against the five reported points, because it determines whether the logarithmic bound of Section 4.5 can be said to be supported.

We fitted **three candidate laws** by least squares (computed by us from the five values; **no other data were used**):

| Model | Fit | Quality | Observation |
|---|---|---|---|
| Linear in `ln n` | `T ≈ 156·ln n − 409` | R² = 0.85 | Predicts −50 ms at n=10; local slope per unit of ln n rises from 47 to 375 ms across the range, so the data are **not** linear in ln n. |
| Linear in `n` | `T ≈ 1.28·n + 62` | R² = 0.99 | Good fit overall, but local slope falls from 1.9 to 1.0 ms per node. |
| **Power law** | `T ≈ 8.4·n^0.70` | **R² = 0.997** (log-log) | **Best of the three**; exponent between logarithmic and linear. |

### 3.4 Result of the analysis

**The reported values are not consistent with scaling that is linear in log n.** They are better described by a sub-linear power law with an exponent near **0.70**, and the gap between the analytic estimate of Equation (4) and the reported values grows from **1.0× at n=10** to **5.5× at n=500** (Table 4.2).

> **Important caveat:**
> With only **five points** and **two or three fitted parameters**, the exponent is **imprecise**, and we do **not** claim that the true scaling law is a power law. We also do **not** know the number of runs or their variance.

What the data do support is the narrower statement that:

- In this simulation, convergence at 250 nodes was reported as **420 ms**, within the 450 ms reference.
- Latency increased by about a factor of **15** while the node count increased by a factor of **50**.

### 3.5 Hypotheses for future work (untested)

Several explanations for the super-logarithmic growth are conceivable and **none has been tested**:

- Validation work that grows with the number of deltas or peers.
- Fixed fanout over partitioned topologies whose diameter increases with n.
- Contention in the simulated message queues.
- The cost of repeated digest comparison.

We list them as hypotheses for future work (**Q22**).

The **99% threshold** itself matters: the last 1% of nodes, in the **tail** of the epidemic, can dominate the time to full convergence.

**Figure 9** (`Fig6_Scaling_Analysis.png`) shows the five simulation-reported points with the three fitted laws and the analytic scaling of Equation (4) for `k = 5`, `r = 10 Hz`. Fits and the analytic curve are **computed by us**; only the five points are **simulation-reported**.

---

## 4. Metric 2 — Conflict Resolution Overhead (Section 5.3)

### 4.1 Definition

**Conflict Resolution Overhead:** CPU and memory overhead during high-concurrency conflicting edits.

### 4.2 Simulation-reported results

- The CRDT-based join **eliminated 100% of blocking deadlocks** relative to a traditional lock-based version control baseline.
- **CPU overhead** was **below 5%** during peak conflict.
- **Memory overhead** was **below 10%** above baseline.

### 4.3 Interpretation

The **deadlock result** should be understood as a **property of the design** more than as an empirical finding:

- A join over a semilattice does not acquire locks and cannot block on one.
- So the absence of lock deadlocks **follows from the architecture**, and the simulation confirms that the simulated implementation did not introduce locking.
- The comparison with a lock-based system presupposes that the baseline deadlocked at a **non-zero rate** under the workload, **which the record does not state**.

The **CPU and memory figures** are expressed relative to a "baseline" whose **definition is not given**, and the figures are **upper bounds** ("below") rather than point estimates. They should be read as indicating that **no large overhead was observed in the simulation**, not as a cost model.

### 4.4 Scope note

Conflict resolution in AetherMesh does **not remove** semantic conflicts; it makes the merge **deterministic**.

Conflicts flagged by the compatibility matrix (Table 3.1) **remain conflicts in the program sense**, and the simulation does **not assess** how many such conflicts arise or how they are resolved.

---

## 5. Metric 3 — Fault Resilience (Section 5.4)

### 5.1 Definition

**Fault Resilience:** network resilience under Byzantine injection of malformed deltas.

### 5.2 Simulation-reported results

- The Pillar 3 verification layer **blocked 100% of invalid state transitions**.
- **Throughput overhead** was **below 2%**.
- **No valid deltas were rejected** (0% false positives).

### 5.3 Interpretation

**Malformed deltas** — that is, deltas with bad signatures, broken structure, or schema violations — are **exactly the class** that the checks of Section 3.3 are designed to detect, so **rejection of all of them is the expected outcome**. The result is a **check that the simulated pipeline is wired correctly**, not evidence of resilience against adversaries who produce well-formed deltas.

> **Missing denominator:** The record does **not** state **how many deltas were injected**.

If `N` malformed deltas were injected and none was admitted, the **one-sided 95% upper confidence bound** on the admission probability is approximately `3/N` (the "rule of three"). For example:

- `N = 1,000` would bound it near **0.3%**.
- `N = 100` would bound it near **3%**.

**Without `N`**, the claim of "100%" has **no denominator**, and we recommend that any future report state it.

---

## 6. Summary Table (Section 5.5)

| # | Metric | Simulation-reported result | Reading |
|:-:|---|---|---|
| 1 | **State convergence latency** | 420 ms at 250 nodes (below 450 ms); 45–680 ms over 10–500 nodes | Reported; scaling is **not** log-linear (Section 3) |
| 2 | **Conflict-resolution overhead** | No blocking deadlocks; CPU < 5%; memory < 10% | Deadlock-freedom follows from design; overhead baseline undefined |
| 3 | **Fault resilience** | All injected malformed deltas blocked; 0% false positives; throughput overhead < 2% | Pipeline check for **predicate-detectable** faults; **number injected unreported** |

---

## 7. Limitations (Section 5.6)

| # | Limitation |
|:-:|---|
| 1 | **Simulated data.** No real-world deployment has been evaluated, and no result in this section is a measurement of a deployed system. |
| 2 | **Scale.** The testbed covers 10–500 nodes; behaviour at thousands of nodes is unknown, and the observed super-logarithmic growth suggests that extrapolation would be unsafe. |
| 3 | **Simplified network model.** No real latency, packet loss, churn, NAT, or adversarial network conditions. |
| 4 | **Byzantine model.** Limited to malformed deltas. Colluding adversaries, equivocation, replay, withholding, flooding, and Sybil identities were not evaluated. |
| 5 | **Missing statistics.** Number of runs, variance, and confidence intervals are not reported; simulator source and seeds are not included. |
| 6 | **No ablation.** The contribution of each pillar to latency and overhead was not isolated, and no comparison with a gossip-only or a consensus-based design was reported. |

> **Limitations of this section.**
> This section reports what was supplied and analyses it; it does **not add new experiments**. Our scaling analysis uses **five data points** and is **descriptive only**.

---

## 8. What the Evaluation Does and Does Not Support

### 8.1 Supported (narrow) claims

- In the simulation, convergence at 250 nodes was reported as **420 ms**, within the 450 ms reference.
- The simulated pipeline **did not admit** any of the injected malformed deltas.
- **No blocking deadlocks** occurred in the simulated CRDT-based merge.

### 8.2 Not supported

- **Real-world performance** of any deployed system.
- **Adversarial robustness** beyond malformed deltas.
- **Semantic validity** of merged programs.
- **Scaling law** as definitively power-law (only that it is not log-linear).
- **Cost model** for CPU or memory (only upper bounds).
- **Statistical significance** of any result (no variance, no runs, no confidence intervals reported).

---

**End of Simulated Evaluation (v1.0.0).**
