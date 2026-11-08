# AetherMesh v2.0.0 — Evaluation Report

**Version:** 2.0.0
**Date:** 2026-11-08
**Record ID:** AETHERMESH-02
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)
**Author:** Samir Baladi

---

## 1. Summary

AetherMesh v2.0.0 is the **reference implementation** of the architecture
specified in AetherMesh v1.0.0. It provides:

- A working CRDT join-semilattice (`crdt/`)
- An anti-entropy gossip protocol (`gossip/`)
- A four-check Byzantine admission pipeline (`bft/` + `admission/`)
- A simulated P2P testbed (`simulation/`)
- 104 tests (pytest)
- 3 reproducible experiments (`experiments/`)

**Status:** Reference implementation. Preliminary results. Not a production
system. No real-world deployment has been evaluated.

---

## 2. What v2.0.0 Adds to v1.0.0

| v1.0.0 (paper) | v2.0.0 (this) |
|---|---|
| Formal architecture specified | Reference implementation built |
| Proof sketches (not machine-checked) | Implementation of the checked invariants |
| Simulated evaluation (reported only) | Simulated evaluation (reproducible) |
| 33-page PDF | 33-page PDF + `src/aethermesh/` + `tests/` + `experiments/` |
| No PyPI package | PyPI package `aethermesh` (version TBD) |

**The v1.0.0 paper remains the authoritative record.** v2.0.0 does not
modify the paper; it adds an implementation alongside it.

---

## 3. Implementation Status

| Module | Files | Lines | Coverage |
|---|:-:|:-:|:-:|
| `models.py` | 1 | ~140 | 69% |
| `crdt/` | 2 | ~147 | 52% |
| `gossip/` | 2 | ~141 | 67-84% |
| `bft/` | 3 | ~137 | 78-87% |
| `admission/` | 2 | ~101 | 72-92% |
| `simulation/` | 4 | ~356 | 86-94% |
| `cli.py` | 1 | ~141 | 0% (integration) |
| **Total** | **15** | **~1102** | **65%** |

**Test suite:** 104 tests across 7 files.

---

## 4. Experimental Results

### 4.1 Metric 1 — Convergence latency

From `experiments/convergence_latency/results.json`:

| Nodes | Converged at round | Total rounds | Final fraction |
|:-:|:-:|:-:|:-:|
| 10 | 1 | 1 | 100% |
| 50 | 2 | 2 | 100% |
| 100 | 1 | 1 | 100% |
| 250 | 2 | 2 | 100% |
| 500 | 1 | 1 | 100% |

**Note:** The convergence is **fast** because the testbed uses a full
peer view (every node knows every other node). In a partial-view
network (e.g., 32-peer view per node), convergence would take more rounds.

**Caveat:** This is a **simulation result**, not a measurement of a deployed system.

### 4.2 Metric 2 — Conflict resolution overhead

From `experiments/conflict_resolution/results.json`:

| Nodes | Conflicts flagged | Deadlocks | Throughput overhead |
|:-:|:-:|:-:|:-:|
| 10 | 0 | 0 | 0% |
| 50 | 0 | 0 | 0% |
| 100 | 0 | 0 | 0% |

**Note:** No deadlocks occur (CRDT join is lock-free by design). No
conflicts were flagged in this run (the conflicting deltas were concurrent,
not in each other's causal closure, so the semantic check did not flag them).

### 4.3 Metric 3 — Fault resilience

From `experiments/fault_resilience/results.json`:

| Malformed injected | Blocked | Block rate |
|:-:|:-:|:-:|
| 10 | 10 | 100% |
| 50 | 50 | 100% |
| 100 | 100 | 100% |
| 500 | 500 | 100% |

**Note:** All malformed deltas were blocked because the testbed's
`measure_fault_resilience` injects **unsigned** deltas, which fail Check 1
(signature). This matches Section 5.4 of the paper: "malformed deltas ...
are exactly the class that the checks of Section 3.3 are designed to detect."

---

## 5. What v2.0.0 Does Not Change

| Aspect | Status |
|---|---|
| v1.0.0 paper | **Unchanged.** Still the authoritative record. |
| v1.0.0 proof sketches | **Still sketches.** v2.0.0 does not machine-check them. |
| v1.0.0 assumptions A1–A6 | **Unchanged.** The implementation respects them. |
| v1.0.0 limitations | **Unchanged.** All still apply. |
| Real-world deployment | **Still not evaluated.** |

---

## 6. What v2.0.0 Enables

- **Reproducibility:** Anyone can run `pytest` and `experiments/*/run.py`.
- **Extension:** The `src/aethermesh/` package can be imported and extended.
- **Falsifiability:** The 104 tests make specific claims checkable.
- **PyPI:** The package can be installed via `pip install aethermesh`.

---

## 7. Known Limitations of v2.0.0

| # | Limitation |
|:-:|---|
| 1 | **Simulation only.** No real-world deployment has been evaluated. |
| 2 | **Full peer view.** The testbed uses a full peer view (n-1 peers per node). A partial-view model (Section 3.2.2) would be more realistic. |
| 3 | **Network model is simplified.** No real latency distributions, packet loss, NAT, or adversarial network conditions. |
| 4 | **Byzantine model is limited.** Only malformed deltas are tested. Colluding, equivocating, withholding, and Sybil adversaries are not. |
| 5 | **No ablation.** The contribution of each pillar is not isolated. |
| 6 | **No mechanized proofs.** Theorems 1–3 remain proof sketches. |
| 7 | **CLI coverage is 0%.** The CLI is tested manually (via `aethermesh info` / `aethermesh verify`), not via pytest. |

---

## 8. Reproducibility

```bash
# Install
pip install -e ".[dev,experiments]"

# Run tests
pytest

# Run experiments
python experiments/convergence_latency/run.py
python experiments/conflict_resolution/run.py
python experiments/fault_resilience/run.py

# Self-check
python -m aethermesh.cli verify
```

---

9. Comparison with AetherProof v2.0.0

Aspect AetherProof v2.0.0 AetherMesh v2.0.0
Paper 46 pages 33 pages
Modules 7 15
Tests 40 104
Coverage 79% 65%
Experiments 5 3
PyPI aetherproof-arch 0.1.0a1 aethermesh (TBD)
Real-world ❌ ❌
Peer-reviewed ❌ ❌

---

10. Contact

· Author: Samir Baladi
· ORCID: 0009-0003-8903-0029
· Email: gitdeeper@gmail.com
· Zenodo DOI: 10.5281/zenodo.24038038
· GitHub: gitdeeper15/aethermesh

---

End of Evaluation Report (v2.0.0).
