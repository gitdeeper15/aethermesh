# AetherMesh — Changelog

All notable changes to this research project will be documented in this file.

## [2.0.0] — 2026-11-08

### Reference Implementation

First reference implementation of the AetherMesh architecture
specified in v1.0.0.

### Added — Source Code

- `src/aethermesh/` package (15 modules, ~1,100 lines):
  - `models.py` — Delta, Replica, Signature, Verdict, DeltaKind, PeerView
  - `crdt/` — Join-semilattice, delta-state CRDT, join-law verification
  - `gossip/` — Anti-entropy protocol (5 steps), peer sampling
  - `bft/` — Ed25519 provenance, structural invariants, semantic matrix
  - `admission/` — Four-check admission pipeline
  - `simulation/` — Network (fair-lossy), Node, Testbed
  - `cli.py` — CLI (`aethermesh info|verify|simulate`)

### Added — Tests

- `tests/` package (7 files, **107 tests**, **79% coverage**)

### Added — Experiments

- `experiments/convergence_latency/` — Metric 1 (Section 5.2)
- `experiments/conflict_resolution/` — Metric 2 (Section 5.3)
- `experiments/fault_resilience/` — Metric 3 (Section 5.4)
- All three experiments reproducible via `python experiments/*/run.py`

### Added — Reports

- `REPORTS/v2.0.0/report.md` — full evaluation report

### Added — Packaging

- `pyproject.toml` — PEP 621 build config, `[build-system]`, dependencies
- `upload_aethermesh.py` — PyPI uploader (supports PyPI + TestPyPI)
- `src/aethermesh/py.typed` — PEP 561 marker

### Changed

- `VERSION`: 1.0.0 → 2.0.0
- `CITATION.cff`: 1.0.0 → 2.0.0 (version + date)
- `manifest.json`: 1.0.0 → 2.0.0
- `scientific_state.json`: 1.0.0 → 2.0.0
- `PROJECT_SUMMARY.txt`: 1.0.0 → 2.0.0
- `INVENTORY.md`: 1.0.0 → 2.0.0
- `README.md`: added PyPI badges, Installation section, v2.0.0 status

### Related Identifiers

- **Zenodo DOI**: [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)
- **PyPI**: [pypi.org/project/aethermesh](https://pypi.org/project/aethermesh/) (TBD)
- **GitHub Release**: [v2.0.0](https://github.com/gitdeeper15/aethermesh/releases/tag/v2.0.0)

### Status

| Dimension | Status |
|---|---|
| Manuscript | Complete (v1.0.0, 33 pages, PDF) |
| Implementation | ✅ Built (`src/aethermesh/`, 15 modules) |
| Tests | ✅ 107 passed, 79% coverage |
| Experiments | ✅ 3/3 completed |
| PyPI Package | ⏳ Not yet published |
| Real-world deployment | ❌ Not evaluated |
| Peer review | ❌ Not reviewed |

---

## [1.0.0] — 2026-11-08

### Formal Architecture Proposal with Simulated Evaluation

First public release of AetherMesh: the **decentralization layer** of the
Aether family.

### Added — Manuscript

- `PUBLICATION/AetherMesh_Research_Paper.pdf` — 33-page research article
  - MD5: `b1d7b2da6dda636871f9d5b3cddd855c`
  - SHA256: `bf58c4c3ebb8eb1f3430a7f8fd9d15299065b699f96b61902306f95859e2b7a2`
- `docs/figures/` — 5 figures (Fig1–Fig5)
- `docs/v1.0.0/` — 8 markdown files derived from the paper

### Added — Formal Model

- **4 Definitions:** Convergent State Transition, CRDT State Space,
  Gossip Infection Probability, Byzantine Admission Rule
- **3 Theorems** (proof sketches, not machine-checked)
- **6 Assumptions:** A1–A6

### Added — Architectural Pillars

- Pillar 1: CRDTs for Code and Metadata DAGs
- Pillar 2: Epidemic Gossip Protocols
- Pillar 3: Lightweight Byzantine Fault Tolerance

### Added — Simulated Evaluation

- 3 metrics, 10–500 nodes
- Simulated results only; no real-world deployment

### Added — Documentation

- `README.md`, `AUTHORS.md`, `CONTRIBUTING.md`, `INVENTORY.md`,
  `PROJECT_SUMMARY.txt`, `CITATION.cff`, `manifest.json`,
  `scientific_state.json`, `netlify.toml`, `.gitignore`

### Related Identifiers

- **Zenodo DOI**: [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)
- **OSF Registration**: Pending
- **GitHub Release**: [v1.0.0](https://github.com/gitdeeper15/aethermesh/releases/tag/v1.0.0)
- **PyPI**: Not published (v1.0.0 claims no implementation)

---

**Last Updated:** 2026-11-08
**Current Version:** 2.0.0
