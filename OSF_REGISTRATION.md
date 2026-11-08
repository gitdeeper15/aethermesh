# AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems

---

**Registration DOI:** [10.17605/OSF.IO/9PE5V](https://doi.org/10.17605/OSF.IO/9PE5V)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 8, 2026, 12:17 PM
**Date Registered:** Nov 8, 2026, 12:17 PM
**Associated Project:** [https://osf.io/n59ay](https://osf.io/n59ay)
**Internet Archive:** [https://archive.org/details/osf-registrations-9pe5v-v1](https://archive.org/details/osf-registrations-9pe5v-v1)
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `AetherMesh_Research_Paper.pdf` (v1.0.0, 33 pages)
- `README.md`
- `REPORTS/v2.0.0/report.md`

---

## Overview

### Research questions or hypotheses

AetherMesh investigates the following structural questions:

**RQ1 (CRDT convergence):** Can a state-based CRDT join-semilattice (set union over admitted deltas) provide order-independent, idempotent, and eventually-consistent convergence for concurrent code and metadata mutations, under fair-lossy channels (A1), fair peer selection (A2), finite delta universe (A3), correct replicas (A4), cryptographic soundness (A5), and admission determinism (A6)?

**RQ2 (Gossip dissemination):** Under the constant-hazard model, does the probability that a node remains uninfected after t gossip steps decay exponentially, P_uninfected(t) ≈ e^(−βt), and what is the relationship between the epidemic's tail behavior and the fanout k?

**RQ3 (Byzantine admission):** If the number of Byzantine agents f satisfies f < n/3, do local verification predicates at each honest node block all predicate-detectable invalid deltas with probability approaching 1, and what is the committee-size bound under the Chernoff–Hoeffding inequality?

**RQ4 (Implementation):** Does a reference implementation of the tripartite architecture (CRDT + gossip + BFT) reproduce the simulated metrics reported in v1.0.0 (convergence latency, conflict-resolution overhead, fault resilience) under a controlled testbed?

These are structural questions about the composition of three known mechanisms (CRDTs, epidemic gossip, BFT-style filtering) as a single architecture for code and metadata DAGs. They are not empirical hypotheses about a deployed system.

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

AetherMesh is a formal architecture proposal (v1.0.0) with a reference implementation (v2.0.0). The v1.0.0 paper was published on Zenodo (DOI: 10.5281/zenodo.24038038) before this OSF registration. The v2.0.0 reference implementation was built alongside the paper.

No real-world deployment data exists. All numerical results in v1.0.0 and v2.0.0 are simulation results from a custom P2P testbed (10–500 nodes), not measurements of a deployed system. The simulator source, random seeds, and raw traces are included in the v2.0.0 repository (github.com/gitdeeper15/aethermesh) to support reproducibility, but were not part of the v1.0.0 paper record.

To manage unintended influences:
- The v1.0.0 paper explicitly labels theorems 1–3 as proof sketches, not machine-checked proofs.
- The v1.0.0 paper explicitly labels all numerical results as simulation results.
- The v1.0.0 paper's reconciliation notes (p. 32) document 11 departures from the supplied draft material, including softened claims.
- The v2.0.0 implementation is accompanied by 107 tests (79% coverage) and 3 reproducible experiments (experiments/*/run.py).
- No causal claims are made; the work is formal analysis plus simulation.

---

## Research Design

### Study type

Simulation study: Using existing or synthetic data to assess performance of a model, mimic operation of an existing or proposed system, or predict possible outcomes in a controlled context.

### Intention for causal interpretation

No causal relationship inferred: This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Study design

AetherMesh is a simulation study of a formal architecture for decentralized peer-to-peer synchronization. The study design has three parts:

**(1) Formal model (v1.0.0):** Four formal definitions (convergent state transition, CRDT state space as bounded join-semilattice, gossip infection probability, Byzantine admission rule), three theorems (eventual consistency, exponential dampening, Byzantine fault tolerance bound) stated with proof sketches, and six explicit assumptions (A1–A6: fair-lossy channels, fair peer selection, finite delta universe, correct replicas, cryptographic soundness, admission determinism).

**(2) Simulated evaluation (v1.0.0):** A custom discrete-event simulator (Python + NumPy) instantiates 10, 50, 100, 250, and 500 autonomous agent nodes in partitioned network topologies. Three metrics are measured:
- Metric 1: State convergence latency (time for a mutation at a single edge node to propagate to and be merged by 99% of the network).
- Metric 2: Conflict-resolution overhead (CPU and memory overhead during high-concurrency conflicting edits, compared against a lock-based baseline).
- Metric 3: Fault resilience (blocking of injected malformed deltas by the Byzantine admission pipeline).

The simulator uses a simplified network model (no real latency distributions, packet loss, NAT, or adversarial network conditions). Simulator source, random seeds, and raw traces are not included in the v1.0.0 record.

**(3) Reference implementation (v2.0.0):** A Python package (aethermesh, 15 modules, ~1,100 lines) implements the architecture. It is tested with 107 pytest tests (79% coverage) and exercised by three reproducible experiments (experiments/*/run.py) that re-run the three metrics above. The implementation follows the v1.0.0 paper; it does not claim to be a production system.

No between-subject or within-subject design applies. There are no human subjects, no randomization, and no blinding. The unit of analysis is the simulated node (10–500 per run). The same random seed (42) is used across runs for reproducibility; different seeds are not tested. The study is descriptive (it reports simulated metrics and does not infer causal effects). No ablation of the three pillars (CRDT, gossip, BFT) is performed, and no comparison with a gossip-only or consensus-based design is reported.

### Randomization

Not applicable. No randomization is involved. This is a simulation study with a fixed seed.

---

## Sampling

### Data collection procedures

AetherMesh is a simulation study, not a study of human subjects. There is no population to sample, no sampling frame, no recruitment, and no eligibility criteria.

Data collection consists of three reproducible experiments executed against a custom discrete-event simulator (Python + NumPy). Each experiment is run by a script in the repository:

- `experiments/convergence_latency/run.py` — measures state convergence latency at 99% of the network.
- `experiments/conflict_resolution/run.py` — measures conflict-resolution overhead (deadlocks, CPU, memory).
- `experiments/fault_resilience/run.py` — measures blocking of malformed deltas by the Byzantine admission pipeline.

Each script instantiates a simulated P2P network of N autonomous agent nodes (N ∈ {10, 50, 100, 250, 500}), runs gossip rounds until convergence, and writes a results.json file. The simulator source, random seeds (seed=42), and raw traces are included in the repository at github.com/gitdeeper15/aethermesh. The full paper is published on Zenodo (DOI: 10.5281/zenodo.24038038).

No real-world deployment data is collected. All numerical results are simulation results from a simplified network model (no real latency, packet loss, NAT, or adversarial conditions). The simulator is deterministic given the random seed.

Expected duration of data collection: the three experiments complete in under 5 minutes on a standard laptop (Termux / Android in the development environment).

### Sample size

This is a simulation study; the "sample size" is the number of simulated nodes per run.

Planned sample sizes:
- Experiment 1 (Convergence Latency): 5 configurations, N ∈ {10, 50, 100, 250, 500}. Each configuration is a single run (seed=42) with a single delta injected at node 0. Convergence is measured at the 99% threshold.
- Experiment 2 (Conflict Resolution): 3 configurations, N ∈ {10, 50, 100}. Each configuration injects 10 conflicting deltas (RENAME_SYMBOL) and runs 20 gossip rounds.
- Experiment 3 (Fault Resilience): 4 configurations, N = 20 fixed. Each configuration injects M ∈ {10, 50, 100, 500} malformed deltas (unsigned) and counts the block rate.

No human subjects. No between-subject or within-subject design. The unit of analysis is the simulated node. The simulator uses a full peer view (each node knows every other node), which makes convergence fast; a partial-view model would be more realistic but is not implemented.

No power analysis is performed. The sample sizes are chosen to match the v1.0.0 paper's reported figures (10–500 nodes) and to keep each experiment under 1 minute on a laptop.

### Sample size rationale

The sample sizes are chosen to match the v1.0.0 paper's simulated evaluation (10, 50, 100, 250, 500 nodes) and to demonstrate the three metrics at multiple scales. No formal power analysis is performed, because this is a simulation study, not a hypothesis test.

The convergence latency experiment uses a single delta per run to isolate the dissemination time. The conflict-resolution experiment uses 10 conflicting deltas to exercise the semantic compatibility matrix. The fault-resilience experiment uses up to 500 malformed deltas to demonstrate the admission pipeline's block rate.

The choice of seed=42 is arbitrary but fixed across runs for reproducibility. Different seeds are not tested; this is a limitation (threat T12: simulator infidelity).

### Starting and stopping rules

This is a simulation study; there is no pilot testing and no human subjects. Data collection "begins" when the script is invoked and "ends" when the script writes its results.json file.

Starting rule: a script begins when invoked via `python experiments/<name>/run.py`.

Stopping rule: a script terminates when one of the following conditions holds:
- The maximum number of gossip rounds is reached (max_rounds ∈ {20, 50, 100} depending on the experiment).
- The convergence threshold is met (99% of nodes hold the same delta set for Experiment 1).
- The injected deltas are exhausted (Experiments 2 and 3).

The simulator is deterministic given the seed; re-running a script with the same seed produces the same results.json. This is verified by the test suite (tests/test_simulation.py).

---

## Variables

### Manipulated variables

This is a simulation study; there are no treatment arms and no randomization. The following simulation parameters are manipulated across experiments:

- N (number of simulated nodes): N ∈ {10, 50, 100, 250, 500} for Experiment 1; N ∈ {10, 50, 100} for Experiment 2; N = 20 fixed for Experiment 3.
- fanout k (peers contacted per gossip round): k = 5 (fixed across all experiments).
- gossip period (seconds between rounds): 0.1 s.
- max_rounds: 100 (Experiment 1), 50 (Experiment 2), 20 (Experiment 3).
- n_malformed (number of malformed deltas injected): M ∈ {10, 50, 100, 500} for Experiment 3.
- n_conflicting_deltas (number of conflicting deltas injected): 10 for Experiment 2.
- seed (random seed): 42 (fixed across all experiments, for reproducibility).

No randomization is applied. The seed is fixed, so re-running produces identical results. No treatment arms are compared; the study is descriptive, not experimental.

### Measured variables

This is a simulation study. The measured variables are simulation outputs, not human measurements:

- Metric 1 — State convergence latency: the number of gossip rounds and the simulated time at which 99% of nodes hold the same delta set as the global union. Unit: rounds and simulated seconds.
- Metric 2 — Conflict-resolution overhead: number of blocking deadlocks (integer), number of conflicts flagged by the semantic compatibility matrix (integer), CPU overhead (percentage, informational), memory overhead (percentage, informational).
- Metric 3 — Fault resilience: number of malformed deltas injected (integer), number blocked (integer), block rate (ratio in [0,1]), number of valid deltas falsely rejected (integer, expected 0).
- Per-node counters (in the testbed): deltas_authored, deltas_received, deltas_admitted, deltas_rejected, deltas_deferred, state_size, peer_view_size.

No human subjects, no covariates, no subsetting, no exclusion criteria. The simulator reports one results.json file per experiment.

### Indices

Two derived variables are computed:

- Block rate (Experiment 3): block_rate = blocked / injected, where `blocked` is the number of malformed deltas rejected by the admission pipeline and `injected` is the total number of malformed deltas. Value in [0, 1]. A value of 1.0 means all malformed deltas were rejected.
- Convergence fraction (Experiment 1): converged_fraction = (number of nodes whose delta set equals the global union) / N. The simulator stops when converged_fraction ≥ 0.99, and reports the round and simulated time at which this threshold was first reached.

No other indices are computed. No scaling fits are computed in v2.0.0 (the v1.0.0 paper's power-law fit is a separate analysis, not part of the simulation).

---

## Analysis Plan

### Statistical models

AetherMesh does not use inferential statistical models. It is a simulation study, not a hypothesis test. There is no ANOVA, no regression, no SEM, and no p-values.

The three metrics are reported as descriptive outputs of a deterministic simulator:

- Metric 1 (Convergence Latency): for each N ∈ {10, 50, 100, 250, 500}, a single run with seed=42 reports the round and simulated time at which converged_fraction ≥ 0.99. No model is fit; the values are reported directly.
- Metric 2 (Conflict Resolution): for each N ∈ {10, 50, 100}, a single run reports the number of blocking deadlocks (expected 0 by design) and the number of conflicts flagged by the semantic compatibility matrix. No model is fit.
- Metric 3 (Fault Resilience): for N = 20 and M ∈ {10, 50, 100, 500}, a single run reports block_rate = blocked / injected. No model is fit.

No controls, no manipulation checks, no convergence criteria (in the statistical sense), no assumption tests. The simulator is deterministic given the seed; re-running produces identical results.

The v1.0.0 paper's scaling analysis (power-law fit `T ≈ 8.4·n^0.70`, R² = 0.997) is a separate descriptive fit computed by the author from five reported points, not a statistical model and not part of v2.0.0.

### Transformations

No transformations are applied. The simulator outputs integers (rounds, counts, state sizes) and floating-point values (simulated time, fractions, percentages). No centering, recoding, or transformation is performed.

Categorical variables: none. All inputs are numeric (N, fanout, seed) or fixed string identifiers (DeltaKind values: EDIT_BODY, RENAME_SYMBOL, DELETE_SYMBOL, CHANGE_SIGNATURE, EDIT_METADATA).

The metric "block_rate" is already a ratio in [0, 1]; no transformation is needed. The metric "converged_fraction" is already a ratio in [0, 1]; no transformation is needed.

### Inference criteria

No inferential criteria are used. There are no p-values, no Bayes factors, no model fit indices, and no cutoff criteria. The study is descriptive.

No one-tailed or two-tailed tests. No multiple-comparison correction. No hypothesis tests are performed.

The only "criterion" is the convergence threshold used by Metric 1: the simulator stops when converged_fraction ≥ 0.99 (i.e., 99% of nodes hold the same delta set as the global union). This threshold is a stopping rule, not an inference criterion.

### Data inclusion and exclusion

No data is excluded. All simulated nodes are included in every run. The simulator does not generate outliers, missing values, or excluded observations.

The fault-resilience experiment injects malformed deltas; these are not excluded — they are the input to the admission pipeline, and the metric (block_rate) counts how many are rejected by the pipeline. A block_rate of 1.0 means all injected malformed deltas were rejected, which is the expected outcome for the class of faults tested.

No outlier handling. No exclusion criteria. The test suite (tests/) verifies the simulator's behavior on edge cases (empty clusters, zero injected deltas), but these are tests, not data exclusions.

### Missing data

No missing data. The simulator generates every value it reports; there is no missingness. Every results.json file contains all fields for every configuration. Re-running produces identical outputs given the same seed.

### Other planned analysis

None beyond what is described above.

Possible future analyses (not planned for v2.0.0):
- Ablation of the three pillars (CRDT-only, gossip-only, BFT-only) to isolate their contributions.
- Comparison with a gossip-only baseline and a consensus-based baseline.
- Mechanized proofs of Theorems 1–3 in a proof assistant (Coq, Lean, or TLA+).
- Real-world deployment evaluation with geo-distributed machines.
- Extended Byzantine models (colluding, equivocating, withholding, Sybil).

These are open questions (Q1–Q50) in the v1.0.0 paper, not part of v2.0.0.

---

## Other

### Context and additional information

AetherMesh is the fourth layer (decentralization) of the Aether family, alongside three companion projects:

- AetherGit (storage layer): 10.5281/zenodo.23966896
- AetherFlow (integration layer): 10.5281/zenodo.23979129
- AetherProof (verification layer): 10.5281/zenodo.24013124
- AetherMesh (decentralization layer): 10.5281/zenodo.24038038 (this work)

Two versions of AetherMesh are documented:
- v1.0.0 (2026-11-08): Formal architecture proposal with simulated evaluation. 33-page paper, 4 definitions, 3 theorems (proof sketches), 6 assumptions (A1–A6), 3 architectural pillars, 15 threats (T1–T15), 50 open questions (Q1–Q50), 52 design decisions (D1–D52).
- v2.0.0 (2026-11-08): Reference implementation. 15 Python modules (~1,100 lines), 107 tests (79% coverage), 3 reproducible experiments. PyPI package: aethermesh.

The v1.0.0 paper explicitly states its evidentiary status:
- Theorems 1–3 are stated with proof sketches; none is machine-checked.
- All numerical results are simulation results from a simplified P2P testbed (10–500 nodes); no real-world deployment has been evaluated.
- The simulated Byzantine model is limited to malformed deltas.
- The paper is not peer reviewed.

The v2.0.0 reference implementation respects these limitations. It does not modify the v1.0.0 paper, does not claim to be a production system, and does not make causal claims.

Repositories:
- GitHub (primary): github.com/gitdeeper15/aethermesh
- GitLab (mirror): gitlab.com/gitdeeper15/aethermesh
- Codeberg (mirror): codeberg.org/gitdeeper15/aethermesh
- Bitbucket (mirror): bitbucket.org/gitdeeper15/aethermesh
- PyPI: pypi.org/project/aethermesh
- Zenodo: 10.5281/zenodo.24038038
- Website: aethermesh-web.netlify.app

The work builds on established theory: CRDTs (Shapiro et al., 2011), delta-state CRDTs (Almeida et al., 2018), epidemic algorithms (Demers et al., 1987), randomized rumor spreading (Karp et al., 2000), Byzantine fault tolerance (Lamport et al., 1982; Castro & Liskov, 1999), and gossip-based aggregation (Jelasity et al., 2005).

This registration is for the OSF project; the Zenodo DOI (10.5281/zenodo.24038038) is the authoritative archival record for the paper.

---

## Metadata

### Contributors

Samir Baladi

### Description

AetherMesh is the decentralization layer (fourth layer) of the Aether family: a fully decentralized peer-to-peer synchronization framework for autonomous agent networks that modify shared codebases and metadata DAGs. It replaces locking and central coordination with a tripartite architecture: (1) specialized conflict-free replicated data types (CRDTs) for code structures and semantic metadata; (2) epidemic gossip protocols for low-latency, resilient propagation; and (3) a lightweight Byzantine fault tolerance (BFT) admission layer that verifies remote deltas before they enter the local join-semilattice.

Two versions are documented:
- v1.0.0 (2026-11-08): Formal architecture proposal with simulated evaluation. 33-page paper, 4 definitions, 3 theorems (proof sketches), 6 assumptions (A1–A6), 3 architectural pillars, 3 simulated metrics, 15 threats (T1–T15), 50 open questions (Q1–Q50), 52 design decisions (D1–D52). DOI: 10.5281/zenodo.24038038
- v2.0.0 (2026-11-08): Reference implementation. 15 Python modules (~1,100 lines), 107 tests (79% coverage), 3 reproducible experiments. PyPI package: aethermesh.

Status: Reference implementation. Preliminary results. No real-world deployment has been evaluated. Theorems 1–3 are stated with proof sketches and are not machine-checked. The paper is not peer reviewed.

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Associated project

https://osf.io/n59ay

### Date Created

Nov 8, 2026, 12:17 PM

### Date registered

Nov 8, 2026, 12:17 PM

### Subjects

- Software Engineering
- Computer Sciences
- Physical Sciences and Mathematics

### Tags

- AetherMesh
- agentic software engineering
- Byzantine fault tolerance
- conflict-free replicated data types
- CRDT
- decentralized synchronization
- distributed systems
- eventual consistency
- formal methods
- gossip protocol
- multi-agent systems
- peer-to-peer

### Affiliated Institutions

No affiliated institutions

### Internet Archive link

https://archive.org/details/osf-registrations-9pe5v-v1

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/9PE5V

---

## Citations

### APA

Baladi, S. (2026, November 8). AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems. OSF. https://doi.org/10.17605/OSF.IO/9PE5V

### MLA

Baladi, Samir. "AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems." OSF, 8 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems." OSF. November 8. doi:10.17605/OSF.IO/9PE5V.

### BibTeX

```bibtex
@misc{baladi2026aethermesh_osf,
  author       = {Baladi, Samir},
  title        = {{AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems}},
  year         = {2026},
  month        = nov,
  day          = {8},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/9PE5V},
  url          = {https://doi.org/10.17605/OSF.IO/9PE5V},
  note         = {OSF Preregistration. Associated project: https://osf.io/n59ay}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-08
